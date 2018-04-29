from __future__ import print_function
from collections import defaultdict
from sys import exc_info

from aenum import Enum
from dbf import Date
from openerplib import DEFAULT_SERVER_DATE_FORMAT, Many2One, get_records
from scription import print
from VSS.address import PostalCode
from VSS.utils import LazyClassAttr

def pfm(values):
    "prepare values dict for marshalling"
    result = {}
    for k, v in values.items():
        if v is None:
            result[k] = False
        elif isinstance(v, Date):
            result[k] = v.strftime(DEFAULT_SERVER_DATE_FORMAT)
        elif isinstance(v, Many2One):
            result[k] = v.id
        elif isinstance(v, PostalCode):
            result[k] = v.code
        elif isinstance(v, Enum):
            result[k] = v.value
        else:
            result[k] = v
    return result

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
            if new_rec[field] != old_rec[field]:
                changed_values.append((field, old_rec[field], new_rec[field]))
        if changed_values:
            changes.append((old_rec, new_rec, changed_values))
    return changes, added, deleted

def compare_fis_records(old_records, new_records, enum_schema, address_fields, ignore=lambda r: False):
    # get changed records as list of
    # (old_record, new_record, [(enum_schema_member, old_value, new_value), (...), ...]) tuples
    try:
        if issubclass(enum_schema, Enum):
            enum = enum_schema
    except TypeError:
            enum = type(enum_schema[0])
    key_fields_name = list(enum)[0].fis_name
    key_fields = [m for m in enum if m.fis_name == key_fields_name]
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
            if self.raise_on_exception:
                raise
            cls, exc, tb = exc_info()
            self.errors[self.abbr].append('FIS ID %s:%s create caused exception %r' % (self.module, key, exc))
            return False

    def delete(self, ids, context=None):
        if context is None:
            context = self.context
        try:
            return self.table.unlink(ids)
        except Exception:
            if self.raise_on_exception:
                raise
            cls, exc, tb = exc_info()
            self.errors[self.abbr].append('%s: deleting ID(s) %s caused exception %r' % (self.module, ', '.join([str(n) for n in ids]), exc))
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
            if self.raise_on_exception:
                raise
            cls, exc, tb = exc_info()
            self.errors[self.abbr].append('FIS ID %s:%s write caused exception %r' % (self.module, key, exc))
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


