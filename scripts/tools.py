from __future__ import print_function
from collections import defaultdict
from sys import exc_info
import os
import re

from abc import ABCMeta, abstractmethod
from aenum import Enum
from dbf import Date
from openerplib import DEFAULT_SERVER_DATE_FORMAT, get_records, get_xid_records
from openerplib import PropertyNames, IDEquality, SetOnce
from scription import print, echo, error
from traceback import format_exception
from VSS.address import cszk, normalize_address, Rise, Sift, AddrCase, NameCase, PostalCode
from VSS.BBxXlate.fisData import fisData
from VSS.utils import LazyClassAttr

@PropertyNames
class XmlLink(IDEquality):
    """
    create singleton object, allow fields to be set only once
    """

    xml_id = SetOnce()
    id = SetOnce()
    _cache = {}

    def __new__(cls, xml_id):
        if xml_id not in cls._cache.setdefault(cls.__name__, {}):
            obj = super(XmlLink, cls).__new__(cls)
            obj.xml_id = xml_id
            cls._cache[cls.__name__][xml_id] = obj
        return cls._cache[cls.__name__][xml_id]

    def __repr__(self):
        return "%s(id=%r, xml_id=%r)" % (self.__class__.__name__, self.id, self.xml_id)


Synchronize = None

class SynchronizeType(ABCMeta):

    def __new__(metacls, cls_name, bases, clsdict):
        cls = super(SynchronizeType, metacls).__new__(metacls, cls_name, bases, clsdict)
        if not cls_name.startswith('Synchronize'):
            try:
                absmethods = list(cls.__abstractmethods__)
                if absmethods:
                    absmethods_str = ', '.join('%r' % method for method in absmethods)
                    plural = 's' if len(absmethods) > 1 else ''
                    raise TypeError(
                        "cannot instantiate abstract class %r"
                        " with abstract method%s %s" 
                        % (cls_name, plural, absmethods_str)
                        )
            except AttributeError:
                pass
            # verify presence of class settings
            missing = []
            for setting in (
                    'TN', 'FN', 'RE', 'OE', 'F', 'IMD',
                    'OE_KEY', 'OE_FIELDS_LONG', 'FIS_IGNORE_RECORD',
                ):
                if getattr(cls, setting, None) is None:
                    missing.append(setting)
            if missing:
                raise TypeError('%s: missing attribute(s):\n\t%s'
                        % (cls_name, '\n\t'.join(missing)),
                        )
            # fill in missing settings
            for req, opt in (
                    ('OE_FIELDS_LONG', 'OE_FIELDS_QUICK'),
                ):
                if not getattr(cls, opt, None):
                    setattr(cls, opt, req)
            # create XmlLinks if needed
            for name, obj in clsdict.items():
                if obj is XmlLink:
                    obj = type(name, (XmlLink, ), {'host':cls, })
                    setattr(cls, name, obj)
        return cls

SynchronizeABC = SynchronizeType('SynchronizeABC', (object, ), {})

class Synchronize(SynchronizeABC):

    FIS_SCHEMA = ()
    FIS_IGNORE_RECORD = lambda self, rec: False
    OE_KEY_MODULE = None
    OE_NORMALIZE_FIELDS = ()

    def __init__(self, connect, config):
        """
        class level variables that need to be set

            TN  -> FIS table number
            FN  -> FIS table file name
            RE  -> re.match for selecting FIS records
            OE  -> OE model name
            F   -> formated table number, used as prefix for imd name [ 'F262' or 'F163_F65' ]
            IMD -> (Odoo) table name, used as suffix for imd name
            OE_KEY              -> key field in OE tables
            OE_FIELDS_LONG      -> OE fields to fetch for long comparisons

        If needed:

            FIS_SCHEMA          -> FIS fields to use for quick comparisons
            FIS_IGNORE_RECORD   -> function to determine if FIS record should be skipped
            OE_FIELDS_QUICK     -> OE fields to fetch for quick comparisons
            OE_KEY_MODULE       -> module field, if any
        """
        self.oe = connect
        self.config = config
        self.context = {'fis-updates': True, 'active_test': False}
        self.model = self.oe.get_model(self.OE)
        self.ir_model_data = self.oe.get_model('ir.model.data')
        #
        # get the "old" data from:
        # - quick -> old fis file
        # - full -> current OpenERP data
        #
        self.oe_records = {}
        self.fis_records = {}
        self.changed_records = {}
        self.new_records = {}
        self.remove_records = {}
        # the counts
        self.changed_count = 0
        self.added_count = 0
        self.deleted_count = 0

    @classmethod
    def calc_xid(cls, key):
        imd_name = '%s_%s_%s' % (cls.F, key, cls.IMD)
        return imd_name.replace('-','_')

    def categorize(self):
        """
        split records into changed, added, and deleted groups
        """
        print('  categorizing...')
        all_keys = set(list(self.fis_records.keys()) + list(self.oe_records.keys()))
        for key in sorted(all_keys):
            old = self.oe_records.get(key)
            new = self.fis_records.get(key)
            if old is new is None:
                # not sure how this happened, but it looks like we can ignore it
                continue
            elif old is None:
                # no matching OE record, so add the FIS record
                self.new_records[key] = new
            elif new is None:
                # no matching FIS record, so delete the OE record
                self.remove_records[key] = old
            else:
                # we have an old and a new record -- update the new record with the `id` field
                new.id = old.id
                new._imd = old._imd
                if new == old:
                    # no changes, move on
                    continue
                changes = {}
                for field in self.OE_FIELDS:
                    if old[field] != new[field]:
                        changes[field] = new[field]
                self.changed_records.setdefault(
                        tuple(sorted(changes.items())),
                        list,
                        ).append(new.id)

    def check_integrity(self):
        """
        perform integrity checks on FIS and OpenERP data

        - no duplicate keys in FIS
        - no duplicate keys in OE
        - each record in FIS matches a record in OE
        - vice versa
        """
        errors = {}
        # load fis records
        fis_dupes = {}
        fis_records = {}
        self.open_fis_tables()
        for entry in self.fis_table.values():
            for rec in self.convert_fis_rec(entry):
                key = rec[self.OE_KEY]
                if key in fis_records:
                    fis_dupes.setdefault(key, []).append(rec)
                fis_records[key] = rec
        # load openerp records
        oe_dupes = {}
        domain = []
        if self.OE_KEY_MODULE:
            domain.append(('module','=',self.OE_KEY_MODULE))
        oe_records = {}
        for rec in get_records(
                self.oe, self.OE,       # oe is connection, OE is model name
                domain=domain,
                fields=self.OE_FIELDS_LONG,
            ):
            key = rec[self.OE_KEY]
            if key in oe_records:
                oe_dupes.setdefault(key, []).append(rec)
            oe_records[key] = rec
        # verify fis records
        for dupe_key in fis_dupes:
            # hopefully, they are all equal
            unique = [fis_records[dupe_key]]
            dupes = fis_dupes[dupe_key]
            for rec in dupes:
                if rec not in unique:
                    unique.append(rec)
            if len(unique) == 1:
                errors.setdefault(dupe_key, {})['fis'] = '%d identical records' % (1 + len(dupes))
                errors.setdefault(dupe_key, {})['identical'] = True
            else:
                errors.setdefault(dupe_key, {})['fis'] = (
                        '%d different records amongst %d identical records'
                            % (len(unique), 1+(len(dupes)))
                            )
                errors.setdefault(dupe_key, {})['identical'] = False
        # verify openerp records
        for dupe_key in oe_dupes:
            # hopefully, they are all equal
            unique = [oe_records[dupe_key]]
            dupes = oe_dupes[dupe_key]
            for rec in dupes:
                if rec not in unique:
                    unique.append(rec)
            if len(unique) == 1:
                errors.setdefault(dupe_key, {})['oe'] = '%d identical records' % (1 + len(dupes))
            else:
                errors.setdefault(dupe_key, {})['oe'] = (
                        '%d different records amongst %d identical records'
                            % (len(unique), 1+(len(dupes)))
                            )
        # normalize FIS records
        self.normalize()
        # compare FIS records to OpenERP records
        all_keys = sorted(list(fis_records.keys()) + list(oe_records.keys()))
        for key in all_keys:
            fis_rec = fis_records.get(key)
            oe_rec = oe_records.get(key)
            if fis_rec is None:
                errors.setdefault(key, {})['fis'] = 'missing'
            elif oe_rec is None:
                errors.setdefault(key, {})['oe'] = 'missing'
            else:
                fis_rec.id = oe_rec.id
                if fis_rec != oe_rec:
                    fis_diff = []
                    oe_diff = []
                    for field in self.OE_NORMALIZE_FIELDS:
                        self.normalize(fis_rec, oe_rec, field)
                    for field in self.OE_FIELDS_QUICK:
                        try:
                            fis_val = fis_rec[field]
                        except KeyError:
                            raise KeyError('%s: no FIS key named %r' % (self.__class__.__name__, field))
                        try:
                            oe_val = oe_rec[field]
                        except KeyError:
                            raise KeyError('%s: no OE key named %r' % (self.__class__.__name__, field))
                        if fis_val != oe_val:
                            fis_diff.append('%s->  %s' % (field, fis_val))
                            oe_diff.append('%s' % (oe_val, ))
                    if fis_diff:
                        string = '\n'.join(fis_diff)
                        prev = errors.setdefault(key, {}).setdefault('fis', None)
                        if prev is not None:
                            string = prev + '\n' + string
                        errors[key]['fis'] = string
                    if oe_diff:
                        string = '\n'.join(oe_diff)
                        prev = errors.setdefault(key, {}).setdefault('oe', None)
                        if prev is not None:
                            string = prev + '\n' + string
                        errors[key]['oe'] = string
        if not errors:
            echo('FIS and OpenERP records for %s/%d match (%d total)' % (self.FN.upper(), self.TN, len(all_keys)))
        else:
            table = [('xml id', 'FIS', 'OpenERP'), None]
            for key, values in sorted(errors.items()):
                table.append((repr(key)[2:-1], errors[key].get('fis', ''), errors[key].get('oe', '')))
            echo(self.__class__.__name__)
            echo(table, border='table')
    
    def compare_fis_records(self, key=None):
        # get changed records as list of
        # (old_record, new_record, [(enum_schema_member, old_value, new_value), (...), ...]) tuples
        try:
            if issubclass(self.FIS_SCHEMA, Enum):
                enum = self.FIS_SCHEMA
        except TypeError:
                enum = type(self.FIS_SCHEMA[0])
        if key is None:
            key_fields_name = list(enum)[0].fis_name
            key_fields = [m for m in enum if m.fis_name == key_fields_name]
        else:
            key_fields = key
        try:
            address_fields = enum['addr1'], enum['addr2'], enum['addr3']
        except AttributeError:
            address_fields = ()
        enum_schema = [m for m in self.FIS_SCHEMA if m not in address_fields]
        changes = []
        added = []
        deleted = []
        old_records_map = {}
        new_records_map = {}
        for rec in self.old_fis_table.values():
            key = []
            for f in key_fields:
                key.append(rec[f])
            key = tuple(key)
            old_records_map[key] = rec
        for rec in self.fis_table.values():
            key = []
            for f in key_fields:
                key.append(rec[f])
            key = tuple(key)
            new_records_map[key] = rec
        all_recs = set(new_records_map.keys() + old_records_map.keys())
        ignore = self.FIS_IGNORE_RECORD
        for key in all_recs:
            changed_values = []
            new_rec = new_records_map.get(key)
            old_rec = old_records_map.get(key)
            if new_rec and ignore(new_rec):
                continue
            if old_rec and ignore(old_rec):
                continue
            if new_rec == old_rec:
                continue
            if new_rec is None:
                deleted.append(old_rec)
                continue
            if old_rec is None:
                added.append(new_rec)
                continue
            for field in address_fields:
                if new_rec[field] != old_rec[field]:
                    # add all the address fields and dump out of the loop
                    for field in address_fields:
                        changed_values.append((field, old_rec[field], new_rec[field]))
                    break
            for field in enum_schema:
                if new_rec[field] != old_rec[field]:
                    changed_values.append((field, old_rec[field], new_rec[field]))
            if changed_values:
                changes.append((old_rec, new_rec, changed_values))
        return changes, added, deleted

    @abstractmethod
    def convert_fis_rec(self, record):
        """
        return a tuple of (XidRec, ...) suitable for OE
        """
        pass

    def fis_long_load(self):
        """
        when complete, all needed FIS and OE records are ready for processing
        (loads entire FIS table and all possible OE records)
        """
        self.open_fis_tables()
        print(self.fis_table.filename, verbose=2)
        print(self.old_fis_table.filename, verbose=2)
        print('loading current FIS and OE data...')
        oe_module = self.OE_KEY_MODULE
        for entry in self.fis_table.values():
            for rec in self.convert_fis_rec(entry):
                key = rec[self.OE_KEY]
                if oe_module:
                    key = oe_module, key
                self.fis_records[key] = rec
        return None

    def fis_quick_load(self):
        """
        when complete, all needed FIS and OE records are ready for processing
        (looks for changes between current and most recent FIS files)
        """
        self.open_fis_tables()
        print(self.fis_table.filename, verbose=2)
        print(self.old_fis_table.filename, verbose=2)
        print('loading current and most recent FIS tables...')
        changes, added, deleted = self.get_changed_fis_records(
                self.old_fis_table.values(),
                self.fis_table.values(),
                enum_schema=self.FIS_SCHEMA,
                address_fields=self.FIS_ADDRESS_FIELDS,
                ignore=self.FIS_IGNORE_RECORD,
                )
        imd_names = set()
        oe_module = self.OE_KEY_MODULE
        for old, new, diffs in self.changes:
            old_entries = self.convert_fis_rec(old)
            new_entries = self.convert_fis_rec(new)
            for old_rec, new_rec in zip(old_entries, new_entries):
                if old_rec != new_rec:
                    key = new_rec[self.OE_KEY]
                    if oe_module:
                        key = oe_module, key
                    self.fis_records[key] = new_rec
                    imd_names.add(new_rec._imd.name)
        for entry in added:
            for rec in self.convert_fis_rec(entry):
                key = rec[self.OE_KEY]
                if oe_module:
                    key = oe_module, key
                self.fis_records[key] = rec
                imd_names.add(rec._imd.name)
        for entry in deleted:
            for rec in self.convert_fis_rec(entry):
                key = rec[self.OE_KEY]
                if oe_module:
                    key = oe_module, key
                self.fis_records[key] = rec
                imd_names.add(rec._imd.name)
        return imd_names

    def get_fis_changes(self, key=None):
        """
        compare the current and old versions of an FIS table

        key, if not spacified, defaults to all the key fields for that table
        return changed, added, and deleted records
        """
        # get changed records as list of
        # (old_record, new_record, [(enum_schema_member, old_value, new_value), (...), ...]) tuples
        try:
            if issubclass(self.fis_schema, Enum):
                enum = self.fis_schema
        except TypeError:
                enum = type(self.fis_schema[0])
        if key is None:
            key_fields_name = list(enum)[0].fis_name
            key_fields = [m for m in enum if m.fis_name == key_fields_name]
        else:
            key_fields = key
        address_fields = self.FIS_ADDRESS_FIELDS
        enum_schema = [m for m in self.fis_schema if m not in address_fields]
        changes = []
        added = []
        deleted = []
        old_records_map = {}
        new_records_map = {}
        for rec in self.old_fis_table:
            key = []
            for f in key_fields:
                key.append(rec[f])
            key = tuple(key)
            old_records_map[key] = rec
        for rec in self.fis_table:
            key = []
            for f in key_fields:
                key.append(rec[f])
            key = tuple(key)
            new_records_map[key] = rec
        all_recs = set(new_records_map.keys() + old_records_map.keys())
        ignore = self.FIS_IGNORE_RECORD
        for key in all_recs:
            changed_values = []
            new_rec = new_records_map.get(key)
            old_rec = old_records_map.get(key)
            if new_rec and ignore(new_rec):
                new_rec = None
            if old_rec and ignore(old_rec):
                old_rec = None
            if new_rec == old_rec:
                continue
            if new_rec is None:
                deleted.append(old_rec)
                continue
            if old_rec is None:
                added.append(new_rec)
                continue
            for field in address_fields:
                if new_rec[field] != old_rec[field]:
                    # add all the address fields and dump out of the loop
                    for field in address_fields:
                        changed_values.append((field, old_rec[field], new_rec[field]))
                    break
            for field in enum_schema:
                if new_rec[field] != old_rec[field]:
                    changed_values.append((field, old_rec[field], new_rec[field]))
            if changed_values:
                changes.append((old_rec, new_rec, changed_values))
        return changes, added, deleted

    # @abstractmethod
    # def get_oe_keys(self):
    #     """
    #     method to extract all needed keys to match records with OE
    #     """

    def ids_from_fis_ids(self, convert, fis_ids):
        xid_names = [convert(fid) for fid in fis_ids]
        records = self.ir_model_data.search_read([
                ('module','=','fis'),
                ('name','in',xid_names),
                ],
                fields=['res_id'],
                )
        return [r.res_id for r in records]

    def ids_from_fis_records(self, *dicts):
        xid_names = list(set([
                r._imd.name
                for d in dicts
                for r in d.values()
                ]))
        records = self.ir_model_data.search([
                ('module','=','fis'),
                ('name','in',xid_names),
                ])
        return [r.res_id for r in records]


    def imd_domain_from_fis_records(self, *dicts):
        xid_names = list(set([
                r._imd.name
                for d in dicts
                for r in d.values()
                ]))
        return [
                ('module','=','fis'),
                ('name','in',xid_names),
                ]

    def oe_load_data(self, xid_names=None):
        """
        load oe records using ir.model.data
        restrict by names
        """
        print('loading OE data')
        if xid_names:
            domain = [
                    ('module','=','fis'),
                    ('name','in',xid_names),
                    ]
        else:
            domain=[
                ('module','=','fis'),
                ('model','=',self.OE),
                ('name','=like','%s_%%_%s' % (self.F, self.IMD),)
                ]
        self.oe_records = dict(
                (r.key, r)
                for r in get_xid_records(
                    self.oe,
                    domain,
                    self.OE_FIELDS,
                    context=self.context,
                    ))

    def open_fis_tables(self):
        print('gathering data')
        self.fis_table = fisData(self.TN, rematch=self.RE)
        self.old_fis_table = fisData(
                self.TN,
                rematch=self.RE,
                data_path=self.config.network.fis_data_local_old_path,
                )

    def normalize(self):
        """
        override this method if fis records need extra work
        """
        if not(self.fis_records):
            return
        fields = []
        rec = self.fis_records.values()[0]
        for field_name, value in rec.items():
            if isinstance(value, XmlLink):
                fields.append((field_name, value.host))
        for field_name, host in fields:
            # host = CSMS
            # host.OE = 'res.partner'
            # host.OE_KEY = 'xml_id'
            # host.OE_KEY_MODULE = 'F33'
            needed = {}
            for rec in self.fis_records.values():
                value = rec[field_name]
                # value.xml_id = 'HE477'
                # value.id = None
                needed[value.xml_id] = value
            model = host.OE
            field = host.OE_KEY
            oe_records = dict(
                    (r[field], r.id)
                    for r in get_records(
                        self.oe, model,
                        ids=self.ids_from_fis_ids(
                            host.calc_xid,
                            [p.xml_id for p in needed.values()],
                            ),
                        fields=['id', field],
                        context=self.context,
                        ))
            for xml_id, link in needed.items():
                link.id = oe_records.get(xml_id, False)

    def record_additions(self):
        """
        create new records in OE
        """
        for key, rec in self.new_records.items():
            print('key: %r\nrec: %r' % (key, rec))
            new_id = self.model.create(rec)
            rec.id = new_id
            self.all_oe_items[key] = rec
        self.added_count += len(self.new_records)

    def record_changes(self):
        """
        commit all changes to OE
        """
        print('  recording changes...')
        for changes, ids in self.changed_records.items():
            changes = dict(changes)
            self.model.write(ids, changes)
            self.changed_count += len(ids)

    def record_deletions(self):
        """
        remove all deletions from OE
        """
        print('  recording deletions...')
        ids = [rec.id for rec in self.remove_records.values()]
        self.model.unlink(ids)
        for key in self.remove_records.keys():
            self.oe_records.pop(key)
        self.deleted_count += len(self.remove_records)

    def run(self, method):
        #
        # get the "old" data from:
        # - quick -> old fis file
        # - full -> current OpenERP data
        #
        print('processing %s...' % self.FN)
        if method == 'quick':
            self.load_fis_data = self.fis_quick_load
            self.OE_FIELDS = self.OE_FIELDS_QUICK
        elif method == 'full':
            self.load_fis_data = self.fis_long_load
            self.OE_FIELDS = self.OE_FIELDS_LONG
        elif method == 'check':
            self.check_integrity()
            return
        else:
            raise ValueError('unknown METHOD: %r' % (method, ))
        names = self.load_fis_data()    # load fis data
        self.oe_load_data(names)        # load oe data
        self.normalize()                # adjust fis data as needed
        self.categorize()               # split into changed, added, deleted groups
        self.record_additions()
        self.record_changes()
        self.record_deletions()
        print('%d mappings changed\n%d mappings added\n%d mappings %s'
                % (self.changed_count, self.added_count, self.deleted_count, 'deleted'),
                border='box',
                )

class SynchronizeAddress(Synchronize):

    def __init__(self, connect, config, state_recs, country_recs):

        self.state_recs = state_recs
        self.country_recs = country_recs
        super(SynchronizeAddress, self).__init__(connect, config)

    def normalize(self, fis_rec=None, oe_rec=None, field=None):
        if field is None and oe_rec is None and fis_rec is None:
            return super(SynchronizeAddress, self).normalize()
        elif field == 'fis_updated_by_user':
            user_updates = oe_rec.fis_updated_by_user or ''
            fis_rec.fis_updated_by_user = oe_rec.fis_updated_by_user
            if 'A' in user_updates:
                # drop all the address fields
                del oe_rec.use_parent_address
                del oe_rec.street, oe_rec.street2
                del oe_rec.city, oe_rec.state_id, oe_rec.zip, oe_rec.country_id
                del fis_rec.use_parent_address
                del fis_rec.street, fis_rec.street2
                del fis_rec.city, fis_rec.state_id, fis_rec.zip, fis_rec.country_id
            if 'N' in user_updates:
                del oe_rec.name
                del fis_rec.name
            if 'S' in user_updates:
                del oe_rec.specials_notification
                del fis_rec.specials_notification

    def process_address(self, schema, fis_rec, home=False):
        result = {}
        address_lines = (fis_rec[schema.addr1], fis_rec[schema.addr2], fis_rec[schema.addr3])
        addr1, addr2, addr3 = Sift(*address_lines)
        addr2, city, state, postal, country = cszk(addr2, addr3)
        addr3 = False
        addr1 = normalize_address(addr1)
        addr2 = normalize_address(addr2)
        addr1, addr2 = AddrCase(Rise(addr1, addr2))
        city = NameCase(city)
        state, country = NameCase(state), NameCase(country)
        valid_address = True
        if not (addr1 or addr2) or not (city or state or country):
            # just use the FIS data without processing
            addr1, addr2, city = Rise(*address_lines)
            state = country = ''
            postal = PostalCode('', '')
            valid_address = False
        if home:
            sf = 'home_street'
            s2f = 'home_street2'
            cf = 'home_city'
            sidf = 'home_state_id'
            zf = 'home_zip'
            kidf = 'home_country_id'
        else:
            sf = 'street'
            s2f = 'street2'
            cf = 'city'
            sidf = 'state_id'
            zf = 'zip'
            kidf = 'country_id'
        result[sf] = addr1 or False
        result[s2f] = addr2 or False
        result[cf] = city or False
        result[zf] = postal or False
        result[sidf] = False
        result[kidf] = False
        if valid_address:
            if state:
                result[sidf] = self.state_recs[state][0]
                result[kidf] = country = self.state_recs[state][2]
            elif country:
                country_id = self.country_recs.get(country, False)
                if country_id:
                    result[kidf] = country_id
                elif city:
                    city += ', ' + country
                    result[cf] = city
                else:
                    city = country
                    result[cf] = city
        return result


def pfm(values):
    "prepare values dict for marshalling"
    result = {}
    for k, v in values.items():
        if not v:
            result[k] = False
        elif isinstance(v, Date):
            result[k] = v.strftime(DEFAULT_SERVER_DATE_FORMAT)
        elif isinstance(v, IDEquality):
            result[k] = v.id
        elif isinstance(v, PostalCode):
            result[k] = v.code
        elif isinstance(v, Enum):
            result[k] = v.value
        else:
            result[k] = v
    return result

def close_enough(old_rec, new_rec):
    # if float values are close enough, copy the old one to the new one
    for field_name in old_rec.keys():
        old_value = old_rec[field_name]
        new_value = new_rec[field_name]
        ov_is_float = isinstance(old_value, float)
        nv_is_float = isinstance(new_value, float)
        if ov_is_float and nv_is_float:
            if old_value - 0.000001 <= new_value <= old_value + 0.000001:
                new_rec[field_name] = old_value
    # now compare to see if equal
    if old_rec != new_rec:
        return False
    return True

def combine_by_value(old_records, new_records):
    all_keys = set(old_records.keys() + new_records.keys())
    changed_map = defaultdict(list)
    for key in all_keys:
        old_rec = old_records[key]
        new_rec = new_records[key]
        rec_key = []
        for oe_field, new_value in new_rec.items():
            if oe_field in ['xml_id', 'module', 'id']:
                continue
            old_value = old_rec[oe_field]
            if old_value != new_value:
                if isinstance(new_value, list):
                    new_value = tuple(new_value)
                rec_key.append((oe_field, new_value))
        if rec_key:
            changed_map[tuple(rec_key)].append(new_rec)
    return changed_map

def compare_records(old_records, new_records, ignore=lambda r: False):
    # get changed records as list of
    # (old_record, new_record, [(enum_schema_member, old_value, new_value), (...), ...]) tuples
    changes = []
    added = []
    deleted = []
    old_records_map = {}
    new_records_map = {}
    for rec in old_records:
        key = rec.module, rec.xml_id
        old_records_map[key] = rec
    for rec in new_records:
        key = rec.module, rec.xml_id
        new_records_map[key] = rec
    all_recs = set(new_records_map.keys() + old_records_map.keys())
    for key in all_recs:
        changed_values = []
        new_rec = new_records_map.get(key)
        old_rec = old_records_map.get(key)
        if new_rec == old_rec:
            continue
        if new_rec is None:
            deleted.append(old_rec)
            continue
        if old_rec is None:
            added.append(new_rec)
            continue
        if ignore(new_rec):
            continue
        assert set(new_rec.keys()) == set(old_rec.keys()), 'key mismatch'
        for field in new_rec.keys():
            new_value = new_rec[field]
            old_value = old_rec[field]
            if (new_value or old_value) and new_value != old_value:
                changed_values.append((field, old_rec[field], new_rec[field]))
        if changed_values:
            changes.append((old_rec, new_rec, changed_values))
    return changes, added, deleted

def compare_fis_records(old_records, new_records, enum_schema, address_fields, ignore=lambda r: False, key=None):
    # get changed records as list of
    # (old_record, new_record, [(enum_schema_member, old_value, new_value), (...), ...]) tuples
    try:
        if issubclass(enum_schema, Enum):
            enum = enum_schema
    except TypeError:
            enum = type(enum_schema[0])
    if key is None:
        key_fields_name = list(enum)[0].fis_name
        key_fields = [m for m in enum if m.fis_name == key_fields_name]
    else:
        key_fields = key
    if address_fields is None:
        address_fields = ()
    enum_schema = [m for m in enum_schema if m not in address_fields]
    changes = []
    added = []
    deleted = []
    old_records_map = {}
    new_records_map = {}
    for rec in old_records:
        key = []
        for f in key_fields:
            key.append(rec[f])
        key = tuple(key)
        old_records_map[key] = rec
    for rec in new_records:
        key = []
        for f in key_fields:
            key.append(rec[f])
        key = tuple(key)
        new_records_map[key] = rec
    all_recs = set(new_records_map.keys() + old_records_map.keys())
    for key in all_recs:
        changed_values = []
        new_rec = new_records_map.get(key)
        old_rec = old_records_map.get(key)
        if new_rec and ignore(new_rec):
            continue
        if old_rec and ignore(old_rec):
            continue
        if new_rec == old_rec:
            continue
        if new_rec is None:
            deleted.append(old_rec)
            continue
        if old_rec is None:
            added.append(new_rec)
            continue
        for field in address_fields:
            if new_rec[field] != old_rec[field]:
                # add all the address fields and dump out of the loop
                for field in address_fields:
                    changed_values.append((field, old_rec[field], new_rec[field]))
                break
        for field in enum_schema:
            if new_rec[field] != old_rec[field]:
                changed_values.append((field, old_rec[field], new_rec[field]))
        if changed_values:
            changes.append((old_rec, new_rec, changed_values))
    return changes, added, deleted


class Model(object):

    models = []
    errors = defaultdict(list)

    def __init__(self, table, abbr, module, context, raise_on_exception=False):
        self.models.append(self)
        self.table = table
        self.abbr = abbr
        self.module = module
        self.context = context
        self.raise_on_exception = raise_on_exception

    def __getattr__(self, name):
        return getattr(self.table, name)

    def error(self, msg):
        self.errors[self.abbr].append(msg)

    def create(self, key, values, context=None):
        if context is None:
            context = self.context
        try:
            return self.table.create(pfm(values), context=context)
        except Exception:
            cls, exc, tb = exc_info()
            self.errors[self.abbr].append('FIS ID %s:%s create with\n%r\n caused exception\n%s' % (self.module, key, values, exc))
            if self.raise_on_exception:
                raise
            return False

    def delete(self, ids, context=None):
        if context is None:
            context = self.context
        try:
            return self.table.unlink(ids)
        except Exception:
            cls, exc, tb = exc_info()
            self.errors[self.abbr].append('%s: deleting ID(s) %s caused exception %r' % (self.module, ', '.join([str(n) for n in ids]), exc))
            if self.raise_on_exception:
                raise
            return False

    unlink = delete

    def read(self, **kwds):
        if 'context' not in kwds:
            kwds['context'] = self.context
        return get_records(self.table, **kwds)

    def search(self, domain, context=None):
        if context is None:
            context = self.context
        return self.table.search(domain, context=context)

    def write(self, key, ids, values, context=None):
        if context is None:
            context = self.context
        try:
            print('writing to %s using %s\n and %s' % (ids, pfm(values), context), border='box', verbose=3)
            self.table.write(ids, pfm(values), context=context)
            return True
        except Exception:
            cls, exc, tb = exc_info()
            self.errors[self.abbr].append('FIS ID %s:%s write with\n%r\ncaused exception\n%s' % (self.module, key, values, exc))
            if self.raise_on_exception:
                raise
            return False


class FISenum(str, Enum):

    _init_ = 'value sequence'
    _order_ = lambda m: m.sequence

    FIS_names = LazyClassAttr(set, name='FIS_names')

    def __new__(cls, value, *args):
        enum = str.__new__(cls, value)
        if '(' in value:
            fis_name, segment = value.split('(', 1)
            segment = segment.strip(' )')
        else:
            fis_name = value
            segment = None
        enum.fis_name = fis_name
        enum.segment = segment
        enum.__class__.FIS_names.add(fis_name)
        return enum

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self._name_)


class allow_exception(object):

    def __init__(self, *allowed):
        self.allowed = allowed

    def __enter__(self):
        return self

    def __exit__(self, cls, exc, tb):
        if isinstance(exc, self.allowed):
            # print error for future reference
            error(''.join(format_exception(*exc_info())).strip(), border='box')
            return True
        return False


class ProductLabelDescription(object):

    ingredients_text = ''
    recipe_text = ''

    def __init__(self, item_code, label_dir='/mnt/labeltime/Labels'):
        self.item_code = item_code
        self.label_dir = label_dir
        self.process()

    def label_text(self, label_type, leadin):
        lines = [
                line.strip()
                for line in open(self.label_file(label_type), 'rb').read().split("\r")
                if re.match(leadin, line) and line[15:].strip()
                ]
        return lines

    def label_file(self, label_type):
        filename = r'%s/%s/%s%s.spl' % (self.label_dir, self.item_code, self.item_code, label_type)
        if label_type.upper() == 'CC' and os.path.isfile("%so-r-i-g" % filename):
            return "%so-r-i-g" % filename
        if os.path.isfile(filename):
            return filename
        return filename        

    def process(self):
        try:
            lines = self.label_text('B',".91100")
        except:
            try:
                lines = self.label_text('TT',".91100")
            except:
                lines = []
        lines.sort()
        found = None
        self.ingredients = []
        self.ingredientLines = []
        for line in lines:
            if line[15:].startswith("INGREDIENTS:"):
                found = line[:7]
            if line[:7] == found:
                txt = line[15:]
                self.ingredients.append(txt)
                self.ingredientLines.append(line)
        ingr_text = []
        instr_text = []
        target = ingr_text
        for fragment in self.ingredients:
            for sentinel in recipe_sentinels:
                if re.match(sentinel, fragment, re.I):
                    target = instr_text
                    break
            else:
                for sentinal in new_line_sentinels:
                    if re.match(sentinal, fragment, re.I):
                        target.append('\n')
                        break
                else:
                    target.append(' ')
            target.append(fragment)
        ingr_text = ''.join(ingr_text)
        instr_text = ''.join(instr_text)
        self.ingredients_text = ingr_text.strip().replace('\xac', ' ')
        self.recipe_text = instr_text.strip().replace('\xac', ' ')
        return self.ingredients_text


recipe_sentinels = (
        'Cooking',
        'COOKING',
        'DIRECTIONS',
        'INSTRUCTIONS',
        'RECIPE',
        'SUGGESTED',
        )

new_line_sentinels = (
        'ANTIOXIDANTS',
        'CONTAINS',
        'Manufactured',
        '\(May contain',
        'CAUTION',
        'COUNTRY',
        '[A-Z]+ MAY CONTAIN',
        'Product processed',
        '\d\d?%',
        
        )

