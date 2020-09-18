from __future__ import print_function
from collections import defaultdict
from sys import exc_info

import errno
import os
import re
import warnings

from abc import ABCMeta, abstractmethod
from aenum import Enum
from antipathy import Path
from dbf import Date, DateTime, Time, Table, READ_WRITE
from dbf import NoneType, NullType, Char, Logical
from openerplib import DEFAULT_SERVER_DATE_FORMAT, get_records, get_xid_records, XidRec
from openerplib import Fault, PropertyNames, IDEquality, Many2One, SetOnce
from scription import print, echo, error, ViewProgress, script_verbosity, abort
from traceback import format_exception
from VSS.address import cszk, normalize_address, Rise, Sift, AddrCase, NameCase, PostalCode
from VSS.BBxXlate.fisData import fisData
from VSS.utils import LazyClassAttr, grouped_by_column

virtualenv = os.environ['VIRTUAL_ENV']
odoo_erp = 1 if 'odoo' in virtualenv else 0

 # keep pyflakes happy
script_verbosity
abort

@PropertyNames
class XmlLink(IDEquality):
    """
    create singleton object, allow fields to be set only once
    """

    xml_id = SetOnce()
    id = SetOnce()
    _cache = {}
    # "host" is set by SynchronizeType

    def __new__(cls, xml_id, id=None):
        if xml_id not in cls._cache.setdefault(cls, {}):
            obj = super(XmlLink, cls).__new__(cls)
            obj.xml_id = xml_id
            if id is not None:
                obj.id = id
            cls._cache[cls][xml_id] = obj
        return cls._cache[cls][xml_id]

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
                    'OE_KEY', 'FIS_IGNORE_RECORD',
                ):
                if getattr(cls, setting, None) is None:
                    missing.append(setting)
            
            for setting in ('OE_FIELDS', 'OE_FIELDS_LONG'):
                if getattr(cls, setting, None):
                    break
            else:
                missing.append('OE_FIELDS, OE_FIELDS_LONG, and/or OE_FIELDS_QUICK')
            if missing:
                raise TypeError('%s: missing attribute(s):\n\t%s'
                        % (cls_name, '\n\t'.join(missing)),
                        )
            # fill in missing settings
            if getattr(cls, 'OE_FIELDS', None):
                if getattr(cls, 'OE_FIELDS_LONG', None):
                    raise TypeError('cannot specify both OE_FIELDS and OE_FIELDS_LONG')
                if getattr(cls, 'OE_FIELDS_QUICK', None):
                    raise TypeError('cannot specify both OE_FIELDS and OE_FIELDS_QUICK')
                setattr(cls, 'OE_FIELDS_LONG', cls.OE_FIELDS)
            if not getattr(cls, 'OE_FIELDS_QUICK', None):
                setattr(cls, 'OE_FIELDS_QUICK', cls.OE_FIELDS_LONG)
            # create XmlLinks if needed
            for name, obj in clsdict.items():
                if obj is XmlLink:
                    obj = type(name, (XmlLink, ), {'host':cls, })
                    setattr(cls, name, obj)
                    setattr(cls, 'XmlLink', obj)
                    # there should only be one XmlLink -- this makes sure the
                    # class breaks sooner rather than later
                    break
        return cls

SynchronizeABC = SynchronizeType('SynchronizeABC', (object, ), {})

class Synchronize(SynchronizeABC):

    FIS_SCHEMA = ()
    FIS_IGNORE_RECORD = lambda self, rec: False
    OE_KEY_MODULE = None
    FIELDS_CHECK_IGNORE = ()
    def FIS_IGNORE_RECORD(self, rec):
        if self.extra.get('key_filter') is not None:
            if self.extra['key_filter'] == rec[self.FIS_KEY]:
                return False
            return True
        return False

    get_fis_table = staticmethod(fisData)
    get_xid_records = staticmethod(get_xid_records)

    def __init__(self, connect, config, extra=None):
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
            OE_KEY_MODULE       -> module field value or field and value, if any
            FIELDS_CHECK_IGNORE -> fields to ignore during integrity check
        """
        self.erp = connect
        self.config = config
        self.context = {'fis-updates': True, 'active_test': False}
        self.model = self.erp.get_model(self.OE)
        self.ir_model_data = self.erp.get_model('ir.model.data')
        self.extra = extra or {}
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
        self.need_normalized = {}
        # the counts
        self.changed_count = 0
        self.added_count = 0
        self.deleted_count = 0

    @classmethod
    def calc_xid(cls, key):
        imd_name = '%s_%s_%s' % (cls.F, key, cls.IMD)
        return imd_name.replace('-','_').replace(':','_')

    def categorize(self):
        """
        split records into changed, added, and deleted groups
        """
        print('categorizing...')
        print('fis record keys: %r\noe record keys:  %r' % (self.fis_records.keys(), self.oe_records.keys()), verbose=3)
        all_keys = set(list(self.fis_records.keys()) + list(self.oe_records.keys()))
        print('all keys: %r' % (all_keys, ), verbose=3)
        change_records = 0
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
                if 'active' in old and not old.active:
                    # record is already inactive, ignore
                    continue
                # no matching FIS record, so delete/deactivate the OE record
                self.remove_records[key] = old
            else:
                # we have an old and a new record -- update the FIS record with
                # relevant fields from the OE record
                self.normalize_records(new, old)
                if new == old:
                    # no changes, move on
                    continue
                changes = {}
                for field in self.OE_FIELDS:
                    if old[field] != new[field]:
                        if not old[field] and not new[field]:
                            echo('[%s] %r:  %r != %r' % (key, field, old[field], new[field]), border='flag')
                        new_value = new[field]
                        if isinstance(new_value, list):
                            new_value = tuple(new_value)
                        changes[field] = new_value
                try:
                    self.changed_records.setdefault(
                            tuple(sorted(changes.items())),
                            list(),
                            ).append(old)
                except TypeError:
                    print(changes)
                    raise
                change_records += 1
        print('  %d records to be added' % len(self.new_records))
        for rec in self.new_records.values()[:10]:
            print('    %r' % rec, verbose=2)
        print('  %d changes to be made across %d records' % (len(self.changed_records), change_records))
        for changes, records in self.changed_records.items()[:10]:
            print('    %r\n      %r' % (changes, records[0]), verbose=2)
        print('  %d records to be deleted' % len(self.remove_records))
        for rec in self.remove_records.values()[:10]:
            print('    %r' % rec, verbose=2)

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
        fis_records = self.fis_records
        self.open_fis_tables()
        for entry in ViewProgress(
                self.fis_table.values(),
                message='converting $total FIS records',
            ):
            for rec in self.convert_fis_rec(entry):
                if rec is None:
                    continue
                key = rec[self.OE_KEY]
                if key in fis_records:
                    fis_dupes.setdefault(key, []).append(rec)
                fis_records[key] = rec
        # load openerp records
        oe_dupes = {}
        domain = []
        if self.OE_KEY_MODULE:
            value = self.OE_KEY_MODULE
            module = 'module'
            if isinstance(value, tuple):
                module, value = value
            domain.append((module,'=',self.OE_KEY_MODULE))
        oe_records = self.oe_records
        print('retrieving OE records...')
        for rec in ViewProgress(
                get_records(
                    self.erp, self.OE,
                    domain=domain,
                    fields=self.OE_FIELDS_LONG,
                    type=XidRec,
                    ),
                message='converting $total OE records',
                view_type='percent',
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
        self.normalize_fis()
        # compare FIS records to OpenERP records
        all_keys = sorted(set(list(fis_records.keys()) + list(oe_records.keys())))
        for key in ViewProgress(
                all_keys,
                message='comparing $total records',
                view_type='percent',
            ):
            fis_rec = fis_records.get(key)
            oe_rec = oe_records.get(key)
            if fis_rec is None:
                errors.setdefault(key, {})['fis'] = 'missing'
            elif oe_rec is None:
                errors.setdefault(key, {})['oe'] = 'missing'
            else:
                self.normalize_records(fis_rec, oe_rec)
                for field in self.FIELDS_CHECK_IGNORE:
                    del fis_rec[field]
                    del oe_rec[field]
                if fis_rec != oe_rec:
                    fis_diff = []
                    oe_diff = []
                    check_fields = [
                            f
                            for f in self.OE_FIELDS_QUICK
                            if f not in self.FIELDS_CHECK_IGNORE
                            ]
                    for field in check_fields:
                        try:
                            fis_val = fis_rec[field]
                        except KeyError:
                            error(fis_rec, oe_rec, border='box')
                            raise KeyError('%s: no FIS key named %r' % (self.__class__.__name__, field))
                        try:
                            oe_val = oe_rec[field]
                        except KeyError:
                            error(fis_rec, None, oe_rec, border='box')
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
                table.append((
                    repr(key).replace(' ','\\s').replace('\t','\\t')[2:-1] or '<empty key>',
                    errors[key].get('fis', ''),
                    errors[key].get('oe', ''))
                    )
            echo('%s - %s' % (self.__class__.__name__, self.OE))
            echo(table, border='table')

    def close_dbf_log(self):
        """
        close file and delete if empty
        """
        self.record_log.close()
        if not self.record_log:
            table = Path(self.record_log.filename)
            memo = Path(self.record_log.memoname)
            if table.exists():
                table.unlink()
            if memo.exists():
                memo.unlink()

    @abstractmethod
    def convert_fis_rec(self, record):
        """
        return a tuple of (XidRec, ...) suitable for OE
        """
        pass

    def create_dbf_log(self):
        """
        create dbf

        field names come from the class
        field specs come from the model
        """
        # create dbf log file
        path = Path(os.environ.get('VIRTUAL_ENV') or '')
        if path:
            path /= 'var/log/sync-updates'
            if not path.exists():
                path.mkdir()
        specs = ['action_ C(7)', 'failure_ M null']
        names = []
        for name in ('id',self.OE_KEY,'name','street','street2','city','state_id','zip','country_id'):
            if name in names:
                # self.OE_KEY is also 'name'
                continue
            if name in self.model._as_dbf:
                names.append(name)
        for name in sorted(self.model._as_dbf):
            if name not in names:
                names.append(name)
        specs.extend([
                '%s null' % self.model._as_dbf[name].spec
                for name in names
                if name in self.OE_FIELDS_LONG
                ])
        self.dbf_fields = dict(
                (name, dns.name)
                for name, dns in self.model._as_dbf.items()
                if name in self.OE_FIELDS_LONG
                )
        self.record_log = Table(
                filename=get_next_filename(
                    '%s/%03d_%s-%s.dbf'
                    % (path, self.TN, self.FN, Date.today().strftime('%Y-%m-%d'))
                    ),
                field_specs=specs,
                codepage='utf8',
                default_data_types=dict(
                        C=(Char, NoneType, NullType),
                        L=(Logical, NoneType, NullType),
                        D=(Date, NoneType, NullType),
                        T=(DateTime, NoneType, NullType),
                        M=(Char, NoneType, NullType),
                        ),
                dbf_type='vfp',
                ).open(READ_WRITE)

    def fis_long_load(self):
        """
        when complete, all needed FIS and OE records are ready for processing
        (loads entire FIS table and all possible OE records)
        """
        self.open_fis_tables()
        print(self.fis_table.filename, verbose=2)
        print('loading current FIS data...', end=' ')
        oe_module = self.OE_KEY_MODULE
        for entry in self.fis_table.values():
            for rec in self.convert_fis_rec(entry, use_ignore=True):
                key = rec[self.OE_KEY]
                if oe_module:
                    key = oe_module, key
                self.fis_records[key] = rec
        print('%d records retrieved' % len(self.fis_records))
        print('  ', '\n   '.join(str(r) for r in self.fis_records.values()), verbose=3)
        return None

    def fis_quick_load(self):
        """
        when complete, all needed FIS and OE records are ready for processing
        (looks for changes between current and most recent FIS files)
        """
        self.open_fis_tables()
        print(self.fis_table.filename, verbose=2)
        print(self.old_fis_table.filename, verbose=2)
        print('loading current and most recent FIS data...', end=' ')
        changes, added, deleted = self.get_fis_changes()
        print('%d and %d records loaded' % (len(self.fis_table), len(self.old_fis_table)))
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

        key, if not specified, defaults to all the key fields for that table
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
        print('    xid_names ->', xid_names[:10], verbose=2)
        records = self.ir_model_data.search_read([
                ('module','=','fis'),
                ('name','in',xid_names),
                ],
                fields=['res_id'],
                )
        print('    %d records found' % len(records), verbose=2)
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

    def log(self, action, *records):
        result = []
        for rec in records:
            # values = {'action_': action, 'id': Null}
            values = {'action_': action}
            for k, v in rec.items():
                if k.endswith('_'):
                    dbf_field = k
                else:
                    dbf_field = self.dbf_fields[k]
                if isinstance(v, Many2One):
                    v = v.name if v.id else None
                elif isinstance(v, XmlLink):
                    v = v.xml_id if v.id else None
                elif isinstance(v, basestring):
                    if not v: v = None
                elif isinstance(v, (bool, int, long, float)):
                    pass
                elif isinstance(v, (Date, DateTime, Time, NoneType)):
                    v = v if v else None
                elif isinstance(v, (list, tuple)) and v:
                    lines = []
                    for links in grouped_by_column(v, 3):
                        lines.append('%-10s %-10s %-10s' % links)
                    v = '\n'.join(lines)
                else:
                    v = str(v) if v else None
                values[dbf_field] = v
            if action in ('change','delete'):
                values['id'] = rec.id
            self.record_log.append(values)
            result.append(self.record_log.last_record)
        return result

    def log_exc(self, exc, record):
        values = {'failure_': str(exc).replace('\\n','\n')}
        values.update(record)
        self.log('failed', *(values, ))

    def normalize_fis(self):
        """
        override this method if fis records need extra work
        """
        print('normalizing...')
        if not(self.fis_records):
            return
        fields = []
        rec = self.fis_records.values()[0]
        for field_name, value in rec.items():
            if isinstance(value, XmlLink):
                fields.append((field_name, value.host))
        if not fields:
            return
        else:
            print('  ', ', '.join([f[0] for f in fields]), verbose=2)
        for field_name, host in ViewProgress(
                fields,
                message='updating $total field(s)',
            ):
            # host = CSMS
            # host.OE = 'res.partner'
            # host.OE_KEY = 'xml_id'
            # host.OE_KEY_MODULE = 'F33'
            needed = {}
            for rec in self.fis_records.values():
                value = rec[field_name]
                if value is None or value.id:
                    continue
                # value.xml_id = 'HE477'
                # value.id = None
                needed[value.xml_id] = value
            print('  needed:', sorted(needed.keys()[:10]), verbose=2)
            model = host.OE
            key = host.OE_KEY
            print('  model: %r\n  key: %r' % (model, key), verbose=2)
            oe_records = dict(
                    (r[key], r.id)
                    for r in get_records(
                        self.erp, model,
                        ids=self.ids_from_fis_ids(
                            host.calc_xid,
                            [p.xml_id for p in needed.values()],
                            ),
                        fields=['id', key],
                        context=self.context,
                        ))
            print('  found:', sorted(oe_records.items()[:10]), verbose=2)
            for xml_id, link in needed.items():
                link.id = oe_records.get(xml_id, None)
                if link.id is None:
                    self.need_normalized[xml_id] = link

    def normalize_records(self, fis_rec, oe_rec):
        fis_rec.id = oe_rec.id
        fis_rec._imd = oe_rec._imd

    def oe_load_data(self, xid_names=None):
        """
        load oe records using ir.model.data
        restrict by names
        """
        print('loading OE data...', end=' ')
        if xid_names:
            domain = [
                    ('module','=','fis'),
                    ('name','in',xid_names),
                    ]
        elif self.extra.get('key_filter') is not None:
            domain=[
                ('module','=','fis'),
                ('model','=',self.OE),
                ('name','=like','%s_%s_%s' % (self.F, self.extra['key_filter'], self.IMD),)
                ]

        else:
            domain=[
                ('module','=','fis'),
                ('model','=',self.OE),
                ('name','=like','%s_%%_%s' % (self.F, self.IMD),)
                ]
        module = self.OE_KEY_MODULE
        key = self.OE_KEY
        for rec in self.get_xid_records(
                self.erp,
                domain,
                self.OE_FIELDS,
                context=self.context,
            ):
            if self.extra.get('key_filter') is not None:
                if self.extra['key_filter'] != rec[self.OE_KEY]:
                    continue
            key = rec[self.OE_KEY]
            if module:
                key = module, key
            self.oe_records[key] = rec 
        print('%d records retrieved' % len(self.oe_records))

    def open_fis_tables(self):
        self.fis_table = self.get_fis_table(self.TN, rematch=self.RE)
        self.old_fis_table = self.get_fis_table(
                self.TN,
                rematch=self.RE,
                data_path=self.config.network.fis_data_local_old_path,
                )

    def record_additions(self):
        """
        create new records in OE
        """
        for key, rec in ViewProgress(
                sorted(self.new_records.items()),
                message='adding $total records...',
                view_type='percent',
            ):
            [log_record] = self.log('add', rec)
            try:
                # make sure an x2many fields are in the correct format
                for key, value in rec.items():
                    if key in self.model._x2many_fields:
                        if not value:
                            rec[key] = [(5, )]
                        else:
                            ids = []
                            for x in value:
                                if isinstance(x, IDEquality):
                                    x = x.id
                                ids.append(x)
                            rec[key] = [(6, 0, ids)]
                new_id = self.model.create(rec)
                with log_record:
                    log_record.id = new_id
            except Exception as exc:
                raise
                vals = {self.OE_KEY: rec[self.OE_KEY]}
                if self.OE_KEY_MODULE:
                    value = self.OE_KEY_MODULE
                    module = 'module'
                    if isinstance(value, tuple):
                        module, value = value
                    vals[module] = value
                self.log_exc(exc, vals)
                continue
            self.added_count += 1
            rec.id = new_id
            self.oe_records[key] = rec
            if rec[self.OE_KEY] in self.need_normalized:
                link = self.need_normalized.pop(rec[self.OE_KEY])
                link.id = new_id

    def record_changes(self):
        """
        commit all changes to OE
        """
        for changes, records in ViewProgress(
                self.changed_records.items(),
                message='recording $total change groups...',
                view_type='percent',
            ):
            changes = dict(changes)
            ids = [r.id for r in records]
            self.log('delta', changes)
            self.log('change', *records)
            try:
                # ensure x2m fields are passed correctly
                field_names = changes.keys()
                for fn in field_names:
                    if fn in self.model._x2many_fields:
                        value = changes[fn]
                        if not value:
                            changes[fn] = [(5, )]
                        else:
                            value_ids = []
                            for x in value:
                                if isinstance(x, IDEquality):
                                    x = x.id
                                value_ids.append(x)
                            changes[fn] = [(6, 0, value_ids)]
                self.model.write(ids, changes)
                self.changed_count += len(ids)
            except Fault as exc:
                self.log_exc(exc, changes)

    def record_deletions(self):
        """
        remove all deletions from OE
        """
        # try the fast method first
        try:
            print('attempting quick delete/deactivate of %d records' % len(self.remove_records))
            ids = [r.id for r in self.remove_records.values()]
            if 'active' in self.OE_FIELDS:
                action = 'deactivate'
                self.model.write(ids, {'active': False})
            else:
                action = 'delete'
                self.model.unlink(ids)
            oe_records = self.oe_records.copy()
            self.oe_records.clear()
            self.oe_records.update(dict(
                (k, v)
                for k, v in oe_records.items()
                if k not in self.remove_records
                ))
            self.deleted_count += len(self.remove_records)
            self.log(action, *self.remove_records.values())
        except Fault:
            # that didn't work, do it the slow way
            for key, rec in ViewProgress(
                    self.remove_records.items(),
                    message='recording $total deletions',
                    view_type='percent',
                ):
                self.log(action, rec)
                try:
                    if action == 'deactivate':
                        self.model.write(rec.id, {'active': False})
                    else:
                        self.model.unlink(rec.id)
                    self.deleted_count += 1
                    self.oe_records.pop(key)
                except Fault as exc:
                    vals = {self.OE_KEY: rec[self.OE_KEY]}
                    if self.OE_KEY_MODULE:
                        value = self.OE_KEY_MODULE
                        module = 'module'
                        if isinstance(value, tuple):
                            module, value = value
                    vals[module] = value
                    self.log_exc(exc, vals)

    def reify(self, fields=[]):
        """
        generate all XmlLinks, and attach OE fields to them
        """
        for rec in self.get_xid_records(
                self.erp,
                domain=[
                    ('module','=','fis'),
                    ('model','=',self.OE),
                    ('name','=like','%s_%%_%s' % (self.F, self.IMD),)
                    ],
                fields=list(set(fields + ['id', self.OE_KEY])),
                context=self.context,
            ):
            link = self.XmlLink(rec[self.OE_KEY], rec.id)
            for f in fields:
                setattr(link, f, rec[f])

    def run(self, method):
        #
        # get the "old" data from:
        # - quick -> old fis file
        # - full -> current OpenERP data
        #
        print('=' * 80)
        self.create_dbf_log()
        try:
            print('processing %s...' % self.FN)
            if method == 'quick':
                self.load_fis_data = self.fis_quick_load
                self.OE_FIELDS = self.OE_FIELDS_QUICK
            elif method == 'full':
                self.load_fis_data = self.fis_long_load
                self.OE_FIELDS = self.OE_FIELDS_LONG
            elif method == 'check':
                self.OE_FIELDS = self.OE_FIELDS_LONG
                self.check_integrity()
                return
            elif method == 'imd-update':
                self.OE_FIELDS = self.OE_FIELDS_QUICK
                self.update_imd()
                return
            else:
                raise ValueError('unknown METHOD: %r' % (method, ))
            names = self.load_fis_data()    # load fis data
            self.oe_load_data(names)        # load oe data
            self.normalize_fis()                # adjust fis data as needed
            self.categorize()               # split into changed, added, deleted groups
            self.record_additions()
            self.record_changes()
            self.record_deletions()
        finally:
            if method in ('quick', 'full'):
                print()
                print('%d mappings added\n%d mappings changed\n%d mappings %s'
                        % (
                            self.added_count,
                            self.changed_count,
                            self.deleted_count,
                            ('deleted','deactivated')['active' in self.OE_FIELDS],
                            ),
                        border='box',
                        )
            self.close_dbf_log()

    def update_imd(self):
        updated = 0
        self.oe_load_data()
        # self.oe_records now has all records that have ir.model.data names
        xid_names = dict(
                (r.name, r)
                for r in self.ir_model_data.search_read(
                    domain=[
                        ('module','=','fis'),
                        ('model','=',self.OE),
                        ('name','=like','%s_%%_%s' % (self.F, self.IMD),)
                        ],
                    fields=['name','model','res_id','display_name'],
                    ))
        ids = [r.id for r in self.oe_records.values()]
        needed_fields = ['id', self.OE_KEY]
        domain = [('id','not in',ids)]
        if self.OE_KEY_MODULE:
            value = self.OE_KEY_MODULE
            module = 'module'
            if isinstance(value, tuple):
                module, value = value
            domain.append((module,'=',value))
        bare_oe_records = get_records(
                self.erp,
                self.OE,
                domain=domain,
                fields=needed_fields,
                )
        for rec in ViewProgress(
                bare_oe_records,
                message='$total possible records found',
                view_type='percent',
            ):
            xid_name = self.calc_xid(rec[self.OE_KEY])
            if xid_name in xid_names:
                error(
                    '[%(id)s] %(key)s: %(xid_name)s already taken by [%(existing_id)s] %(display_name)s'
                    % {
                        'id': rec.id,
                        'key': rec[self.OE_KEY],
                        'xid_name': xid_name,
                        'existing_id': xid_names[xid_name].res_id,
                        'display_name': xid_names[xid_name].display_name,
                        })
                continue
            self.ir_model_data.create({
                    'module': 'fis',
                    'name': xid_name,
                    'model': self.OE,
                    'res_id': rec.id,
                    })
            xid_names.update(dict(
                    (r.name, r)
                    for r in self.ir_model_data.search_read(
                        domain=[
                            ('module','=','fis'),
                            ('name','=',xid_name),
                            ],
                        fields=['name','model','res_id','display_name'],
                        )))
            updated += 1
        print('%d records added to ir.model.data' % updated)

class SynchronizeAddress(Synchronize):

    def __init__(self, connect, config, state_recs, country_recs, *args, **kwds):

        self.state_recs = state_recs
        self.country_recs = country_recs
        super(SynchronizeAddress, self).__init__(connect, config, *args, **kwds)

    def normalize_records(self, fis_rec=None, oe_rec=None):
        super(SynchronizeAddress, self).normalize_records(fis_rec, oe_rec)
        if 'fis_updated_by_user' in self.OE_FIELDS:
            fis_rec.fis_updated_by_user = oe_rec.fis_updated_by_user
            user_updates = fis_rec.fis_updated_by_user or ''
            try:
                if 'A' in user_updates:
                    # drop all the address fields
                    oe_rec.use_parent_address = None
                    oe_rec.street = oe_rec.street2 = None
                    oe_rec.city = oe_rec.state_id = oe_rec.zip = oe_rec.country_id = None
                    fis_rec.use_parent_address = None
                    fis_rec.street = fis_rec.street2 = None
                    fis_rec.city = fis_rec.state_id = fis_rec.zip = fis_rec.country_id = None
                if 'N' in user_updates:
                    oe_rec.name = None
                    fis_rec.name = None
                if 'S' in user_updates:
                    oe_rec.specials_notification = None
                    fis_rec.specials_notification = None
            except AttributeError:
                error(oe_rec, fis_rec, sep='\n---\n', border='box')
                raise

    def process_address(self, schema, fis_rec, home=False):
        result = {}
        address_lines = (fis_rec[schema.addr1], fis_rec[schema.addr2], fis_rec[schema.addr3])
        print('\naddress lines:\n1: %r\n2: %r\n3: %r\r' % address_lines, sep='\n', border='overline', verbose=3)
        addr1, addr2, addr3 = Sift(*address_lines)
        addr2, city, state, postal, country = cszk(addr2, addr3)
        addr3 = None
        addr1 = normalize_address(addr1)
        addr2 = normalize_address(addr2)
        addr1, addr2 = AddrCase(Rise(addr1, addr2))
        city = NameCase(city)
        state, country = NameCase(state), NameCase(country)
        print('   -----\n1: %r\n2: %r\nc: %r   s: %r   z: %r\nk: %r' % (addr1, addr2, city, state, postal, country), verbose=3)
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
        result[sf] = addr1 or None
        result[s2f] = addr2 or None
        result[cf] = city or None
        result[zf] = postal or None
        result[sidf] = None
        result[kidf] = None
        if valid_address:
            if state:
                result[sidf] = self.state_recs[state][0]
                result[kidf] = country = self.state_recs[state][1]
            elif country:
                country_id = self.country_recs.get(country, None)
                if country_id:
                    result[kidf] = country_id
                elif city:
                    city += ', ' + country
                    result[cf] = city
                else:
                    city = country
                    result[cf] = city
        zip_code = result[zf]
        if isinstance(zip_code, dict) or isinstance(zip_code, (str, unicode)) and 'code' in zip_code:
            print('invalid zip code in:\n%s' % fis_rec)
            raise SystemExit(1)
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
        except IOError as exc1:
            try:
                lines = self.label_text('TT',".91100")
            except IOError as exc2:
                lines = []
                if exc1.errno not in (errno.ENOENT, error.ENOTDIR):   # no such file or directory / not a directory
                    warnings.warn('item %r: %s' % (self.item_code, exc1))
                elif exc2.errno not in (errno.ENOENT, errno.ENOTDIR):
                    warnings.warn('item %r: %s' % (self.item_code, exc1))
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


def get_next_filename(name, limit=99):
    """
    adds numbers to file name until succesfully opened; stops at limit
    """
    file = Path(name)
    for i in range(10000):
        try:
            target = file.parent / file.base + '.%02d' % i + file.ext
            fh = os.open(target, os.O_CREAT | os.O_EXCL)
            os.close(fh)
            return target
        except OSError:
            pass
    else:
        raise IOError('unable to create file for %s' % name)


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

