#!/usr/local/bin/suid-python --virtualenv
"""
Pseudo-SQL system to interogate FIS and OpenERP.
"""
from __future__ import print_function, unicode_literals

from VSS.BBxXlate import fisData as fd
from VSS.BBxXlate.bbxfile import TableError
from abc import ABCMeta, abstractmethod, abstractproperty
from aenum import Enum, auto
from antipathy import Path
from ast import literal_eval
from collections import defaultdict, OrderedDict
from fislib import schema as fis_schema
from fnx_script_support import all_equal, translator
from itertools import cycle
from openerplib import get_connection, get_records, AttrDict, Binary, Query, Many2One, MissingTable, CSV
from traceback import print_exc

import dbf
import os
import pprint
import re
import socket
import sys
import time

from scription import *

try:
    from xmlrpclib import Fault
except ImportError:
    from xmlrpc.client import Fault


virtual_env = os.environ['VIRTUAL_ENV']
config = OrmFile(Path('%s/config/fnx.ini' % virtual_env), types={'_path':Path})
env = config.env
PRODUCT_FORECAST = '/FIS/data/product_forecast.txt'

## Globals

class SQLState(Enum):
    START = auto()
    SELECT = auto()
    FROM = auto()
    JOIN = auto()
    ON = auto()
    WHERE = auto()
    ORDER_BY = auto()
    TO = auto()

( START,
  # DIFF, DIFF_FROM, DIFF_WHERE, DIFF_ORDERBY,
  SELECT, SELECT_FROM, SELECT_JOIN, SELECT_ON, SELECT_WHERE, SELECT_ORDERBY, SELECT_TO,
  ) = SQLState

SINGLE_QUOTE = "'"
COMMA = ","
BACKSLASH = "\\"

TEST = [
        'xml_id',
        'hr_insurance_choice_ids/year_month',
        'hr_insurance_choice_ids/medical',
        'hr_insurance_choice_ids/dental',
        'hr_insurance_choice_ids/vision',
        'hr_insurance_choice_ids/life',
        'name_related',
        'home_country_id/name',
        'home_country_id/code',
        ]

TEST_DOMAIN = [('name_related','in',['Abraham S. Cohen','Aurelia Garcia'])]

ALL_ACTIVE = [(1,'=',1)]

SHOW_ID = False

numbers = {
    '0':    'zero',
    '1':    'one',
    '2':    'two',
    '3':    'three',
    '4':    'four',
    '5':    'five',
    '6':    'six',
    '7':    'seven',
    '8':    'eight',
    '9':    'nine',
    '10':   'ten',
    '1st':  'first',
    '2nd':  'second',
    '3rd':  'third',
    '4th':  'fourth',
    '5th':  'fifth',
    '6th':  'sixth',
    '7th':  'seventh',
    '8th':  'eighth',
    '9th':  'ninth',
    '10th': 'tenth',
    }

common = {
    'account':      'acct',
    'adjustment':   'adj',
    'allocated':    'alctd',
    'allowance':    'allwnc',
    'amount':       'amt',
    'authority':    'auth',
    'average':      'avg',
    'beginning':    'bgng',
    'category':     'cat',
    'center':       'ctr',
    'centering':    'ctr',
    'check':        'chk',
    'cost':         'cst',
    'credit':       'cr',
    'credits':      'crs',
    'customer':     'cust',
    'debit':        'dr',
    'debits':       'drs',
    'department':   'dept',
    'description':  'desc',
    'discount':     'disc',
    'each':         'ea',
    'ingredient':   'ingr',
    'kosher':       'kshr',
    'length':       'len',
    'level':        'lvl',
    'invoice':      'inv',
    'maximum':      'max',
    'mesg':         'msg',
    'method':       'mthd',
    'minimum':      'min',
    'number':       'no',
    'numbers':      'nos',
    'payment':      'pymt',
    'package':      'pkg',
    'packaging':    'pkgg',
    'price':        'prc',
    'product':      'prod',
    'production':   'prod',
    'position':     'pos',
    'quantity':     'qty',
    'redemption':   'rdmtn',
    'revision':     'rev',
    'rounding':     'rndg',
    'sequence':     'seq',
    'stock':        'stk',
    'string':       'str',
    'transaction':  'trans',
    'warehouse':    'wrhse',
    'wholesale':    'whlsl',
    }

uncommon = {
    'adjust':       'adj',
    'company':      'comp',
    'formula':      'frml',
    'other':        'oth',
    'total':        'ttl',
    }

table_keys = {
          8: (  8, 'CNVZD0', r'D010(.)'),                        # customer terms
         11: ( 11, 'CNVZas', r'as10(..)'),                       # product category
         33: ( 33, 'CSMS', r'10(......) '),                      # customer
         34: ( 34, 'CSMSS', r'10(......)1....'),                 # customer ship-to
         27: ( 27, 'CNVZSV', r'SV10(..)'),                       # carrier
         47: ( 47, 'CNVZZ', r'Z(...)'),                          # sales rep
         74: ( 74, 'EMP1', r'10(.....)'),                        # employee
         65: ( 65, 'VNMS', r'10(......)'),                       # purchasers
         97: ( 97, 'CNVZaa', r'aa10(.)'),                        # product location
        135: (135, 'NVTY', r'(......)101000    101\*\*'),        # products
        163: (163, 'POSM', r'10(......)'),                       # vendors
        192: (192, 'CNVZO1', r'O110(......)'),                   # transmitter number
        257: (257, 'CNVZK', r'K(....)'),                         # sales rep
        262: (262, 'ARCI', r'10(......)......'),                 # customer product list
        320: (320, 'IFMS', r'10(..........).....0'),             # product formula
        322: (322, 'IFDT', r'10(..........).....0...'),          # product ingredients
        328: (328, 'IFPP0', r'10(......)000010000'),             # production order formula
        329: (329, 'IFPP1', r'10(......)000011...'),             # production order ingredients
        341: (341, 'CNVZf', r'f10(..)'),                         # production lines

        'arci'  : (262, 'ARCI', r'10(......)......'),            # customer product list
        'cnvzaa': ( 97, 'CNVZaa', r'aa10(.)'),                   # product location
        'cnvzas': ( 11, 'CNVZas', r'as10(..)'),                  # product category
        'cnvzd0': (  8, 'CNVZD0', r'D010(.)'),                   # customer terms
        'cnvzf' : (341, 'CNVZf', r'f10(..)'),                    # production lines
        'cnvzo1': (192, 'CNVZO1', r'O110(......)'),              # transmitter number
        'cnvzsv': ( 27, 'CNVZSV', r'SV10(..)'),                  # carrier
        'cnvzk' : (257, 'CNVZK', r'K(....)'),                    # sales rep
        'cnvzz' : ( 47, 'CNVZZ', r'Z(...)'),                     # sales rep
        'csms'  : ( 33, 'CSMS', r'10(......) '),                 # customer
        'csmss' : ( 34, 'CSMSS', r'10(......)1....'),            # customer ship-to
        'emp1'  : ( 74, 'EMP1', r'10(.....)'),                   # employee
        'ifms'  : (320, 'IFMS', r'10(..........).....0'),        # product formula
        'ifdt'  : (322, 'IFDT', r'10(..........).....0...'),     # product ingredients
        'ifpp0' : (328, 'IFPP0', r'10(......)000010000'),        # production order formula
        'ifpp1' : (329, 'IFPP1', r'10(......)000011...'),        # production order ingredients
        'nvty'  : (135, 'NVTY', r'(......)101000    101\*\*'),   # products
        'posm'  : (163, 'POSM', r'10(......)'),                  # vendors
        'vnms'  : ( 65, 'VNMS', r'10(......)'),                  # purchasers
        }

## API

@Script(
        hostname=('host to connect to'),
        database=('database to query'),
        show_ids=('show record/field ids', FLAG, None),
        )
def main(hostname, database, show_ids=False):
    global oe, SHOW_ID
    SHOW_ID = show_ids
    try:
        oe = get_connection(
                hostname=hostname or config.openerp.host,
                database=database or config.openerp.db,
                login=config.openerp.user,
                password=config.openerp.pw,
                )
    except socket.error:
        oe = None

@Command(
        command=('sql command', REQUIRED),
        separator=('insert blank line between records', FLAG),
        wrap=Spec('field name and width of fields to wrap [ignored in .xls and .csv output]', MULTI),
        quiet=Spec('do not display output', FLAG),
        dev=Spec('use in-development routines', FLAG),
        sheet=Spec('sheet name if writing excel file', OPTION, None),
        )
@Alias('fis-oe')
def sql(command, separator, wrap, quiet, dev, sheet):
    """
    Query FIS/OpenERP databases.

    SELECT field_name [, field_name [, ...]]
        FROM table
        [WHERE ... | subquery ]
        [ORDER BY field1 [ASC|DESC] [, field2 [ASC|DESC] [, ...]]]
        [TO file]

    DESCRIBE table
        [ORDER BY field1]

    UPDATE table
        SET field_name=... [, field_name=... [...]]
        [WHERE ...]

    INSERT INTO table
        (field1, field2, ...)
        VALUES
        (value1, value2, ...)
        [UPDATE ON field1 [, field [...]]]

    INSERT INTO table FILE <filename>

    DELETE FROM table
        [WHERE ...]

    DIFF field_name [, field_name [, ...]]
        FROM table
        [WHERE ...]
        [ORDER BY field1 [ASC|DESC] [, field2 [ASC|DESC] [, ...]]]

    REPORT report-name
        [FROM table]
        [WHERE ...]
        [TO file]
    """
    if quiet:
        global script_verbosity
        script_verbosity = -1
    if isinstance(wrap, tuple):
        wrap = dict(
            (k, int(v))
            for item in wrap
            for k, v in (item.split(':'), )
            )
    command = command.strip(' ;')
    try:
        # get a query object, which has a `records` attribute with all matches
        if dev:
            sql = SQL(command)
            query = sql.execute()
        else:
            query = Table.query(command)
            # table = Table.query(command)
            # query = table.query
        print('q --> %s' % (query, ), verbose=2)
    except SQLError as e:
        help(str(e))
    except NotImplementedError as e:
        abort(str(e))
    if query is not None:
        print(query.name)
        model_name = sheet or query.name or command
        to_file = query.to_file
        fields = query.fields
        query = query
        if to_file:
            if to_file.endswith('.xls'):
                write_xls(model_name, query, fields, to_file, separator)
            elif to_file.endswith('.csv'):
                write_csv(model_name, query, fields, to_file, separator)
            elif to_file.endswith('.txt') or to_file == '-':
                for field, length in wrap.items():
                    pass
                write_txt(model_name, query, fields, to_file, separator, wrap)
            else:
                abort('unknown file type: %r' % to_file)
        echo(query.status)

# OpenERP commands
def _module_name(text):
    module, name = text.split('.')
    return module, name


@Command(
        module=Spec('module of table', ),
        table=Spec('table to process names for', ),
        name=Spec('module.table for name template', type=_module_name),
        domain=Spec('record selection', OPTION, force_default=ALL_ACTIVE, type=literal_eval),
        field=Spec('which field to use for `tag` and `name` methods', OPTION),
        method=Spec(
            'method of unique name generation [default: id]',
            OPTION,
            choices=['id','tag','name'],
            force_default='id',
            ),

        )
def add_imd(module, table, name, domain, field, method):
    """
    OE: add ir.model.data names for data export (not for use with FIS data).
    """
    ensure_oe()
    print(module, table, name, domain, field, method, sep='\n', verbose=2)
    if method == 'id':
        if field and field != 'id':
            abort('field %r not valid with METHOD `id`' % (field, ))
        field = 'id'
    elif field == 'id':
        abort('cannot use the `id` field with METHOD `%s`' % (method, ))
    elif field is None:
        abort('field must be specified for METHOD `%s`' % (method, ))
    target_table = oe.get_model(table)
    _rec_name = target_table._rec_name
    if _rec_name not in target_table._columns:
        _rec_name = 'id'
    fields = list(set(['id', field, _rec_name]))
    dot_table = table
    q = Query(oe.get_model(dot_table), domain=domain, fields=fields[:])
    imd = oe.get_model('ir.model.data')
    func = imd_methods[method]
    imd_module, imd_table = name
    existing_imd = Query(
            imd,
            domain=[('module','=',module),('model','=',dot_table),('res_id','in',q.id_map.keys())],
            fields=['id','name','res_id','model','module'],
            )
    existing_ids = dict(
            (r.res_id, r.name)
            for r in existing_imd.records
            )
    existing_names = dict(
            (r.name, r)
            for r in existing_imd.records
            )
    # check for pre-existing alternate names
    print('existing ids:', existing_ids.keys(), verbose=3)
    template = '%s_%%s' % (imd_table, )
    for r in ViewProgress(q.records, view_type='bar'):
        name = template % (func(r, field), )
        dedupe_name = '%s_%s' % (name, r.id)
        print("%7s  %25s  %s" % (r.id, r[field], name), verbose=2)
        print('checking id:', r.id, verbose=3)
        if r.id in existing_ids:
            current_name = existing_ids[r.id]
            if current_name not in (name, dedupe_name):
                if input("\n%s already set --- change %r to %r?" % (r[_rec_name], current_name, name)):
                    imd.write(r.id, {'name': name})
            continue
        if name in existing_names:
            imd_problem = existing_names[name]
            real_problem = q.id_map[imd_problem.res_id]
            print(
                    'attempting to assign %r to %s:%s [%s] which is already taken by %s:%s [%s]... adding id'
                        % (name, r.id, r[_rec_name], r[field], real_problem.id, real_problem[_rec_name], real_problem[field]),
                    verbose=2,
                    )
            name = '%s_%s' % (name, r.id)
        try:
            new_id = imd.create(dict(module=imd_module, name=name, model=dot_table, res_id=r.id))
            existing_ids[new_id] = name
            existing_names[name] = AttrDict(id=new_id, name=name, res_id=r.id, model=dot_table, module=imd_module)
        except Fault as e:
            problem = imd.read([('name','=',name)])
            if problem:
                abort('%s already exists' % (problem[0], ))
            abort('unable to create %s.%s:\n(%s)' % (imd_module, name, str(e)))
    echo('done')


@Command(
        table=("show exports for TABLE", )
        )
@Alias('list')
def list_exports(table=None):
    """
    OE: list reports created via "export".
    """
    ensure_oe()
    for export in get_records(oe, 'ir.exports'):
        if table and export.resource != table:
            continue
        echo('%-60s [%s]' % (export.name, export.resource))


@Command(
        name=Spec('name pattern to match [wildcard: %]', REQUIRED),
        fields=Spec('fields to look up in relevant model', REQUIRED),
        ignore_case=Spec('use case-insensitive search', FLAG),
        exact=Spec('do not add wildcard to front/back of name', FLAG),
        )
def imd(name, ignore_case, exact, *fields):
    """
    OE: return matching ir.model.data records, combined with field data from target model/record.
    """
    ensure_oe()
    like = '=ilike' if ignore_case else '=like'
    if not exact and '%' not in name:
        name = "%%%s%%" % name
    query = FISTable('ir.model.data').query(
            fields=['module','name','model','res_id','display_name'],
            to_file='',
            domain=[('name', like, name)],
            order='',
            distinct=False,
            separator=False,
            wrap=(),
            _constraints=[],
            )
    models = {}
    for rec in query:
        models.setdefault(rec.model, []).append(rec.res_id)
    for model, ids in models.items():
        model_records = dict(
                (r.id, r)
                for r in get_records(oe, model, ids=ids, fields=fields)
                )
        for q_rec in query:
            if q_rec.model == model:
                model_rec = model_records[q_rec.res_id]
                for f in fields:
                    q_rec[f] = model_rec[f]
    rows = [['module','name','model','res_id','display_name'] + list(fields), None]
    for q in query:
        rows.append([
            q.module, q.name, q.model, q.res_id, q.display_name,
            ] + [q[f] for f in fields]
            )
    echo(rows, border='table')


@Command(
        code=Spec('transmitter code to look up')
        )
def transmitter(code):
    """
    OE: return basic information about <transmitter code>.
    """
    ensure_oe()
    FISTable('fis.transmitter_code').query(
            fields=['transmitter_no','transmitter_name','ship_to_id'],
            to_file='-',
            domain=[('transmitter_no','like',code)],
            order='',
            distinct=False,
            separator=False,
            wrap=(),
            _constraints=[],
            )


@Command(
        table=Spec('table to examine'),
        )
def show_relations(table):
    """
    OE: show tables that link to TABLE and that TABLE links to.
    """
    ensure_oe()
    ir_model_fields = oe.get_model('ir.model.fields')
    try:
        oe.get_model(table)
    except MissingTable:
        abort("'%s' does not exist" % table)
    from_fields = ir_model_fields.read([('relation','=',table)], fields=['model','name'])
    echo(from_fields, end='\n\n')
    to_fields = ir_model_fields.read([('model','=',table),('relation','!=',False)], fields=['name','relation'])
    echo(to_fields, end='\n\n')
    results = [('upstream','table','downstream'), None]
    results.append((
        '\n'.join('%s.%s' % (r.model, r.name) for r in sorted(from_fields, key=lambda d: (d.model, d.name))),
        table,
        '\n'.join('%s.%s' % (r.relation, r.name) for r in sorted(to_fields, key=lambda d: (d.relation, d.name)) if r.relation), 
        ))
    echo(results, border='table')

# FIS commands
@Command(
        filenum=Spec('file abbreviation or number to operate on', REQUIRED),
        keymatch=Spec('key template to select individual records', REQUIRED, default=None),
        key=Spec('key of desired record', MULTIREQ, default=()),
        full=Spec('show all fields', FLAG),
        color=Spec('use color output', FLAG),
        summary=Spec('show summary only', FLAG,),
        )
def diff(filenum, keymatch, key, full, color, summary):
    """
    FIS: show specified records diffed with their older version.
    """
    # easier color names
    white, red, green, cyan = Color.FG_White, Color.FG_Red, Color.FG_Green, Color.FG_Cyan
    bold, all_reset = Color.Bright, Color.AllReset
    #
    if filenum.isdigit():
        filenum = int(filenum)
    fis_table = fd.fisData(filenum, keymatch=keymatch)
    fis_table_old = fd.fisData(filenum, keymatch=keymatch, data_path=config.network.fis_data_local_old_path)
    print('using files: %s (%d) and %s (%d)' %(fis_table.filename, len(fis_table), fis_table_old.filename, len(fis_table_old)), verbose=2)
    new_records = []
    old_records = []
    if keymatch and key:
        # user specified record to diff
        print('keymatch and key specified', verbose=2)
        for k in key:
            new_records.append(fis_table.get(k))
            old_records.append(fis_table_old.get(k))
        data_width = 0
    elif keymatch or key:
        abort('must specify both KEYMATCH and KEY if either is given')
    else:
        print('looking for all changed records', verbose=2)
        # lock in data widths
        data_width = max(fis_table.field_widths)
        # find all changed records
        new_records = []
        old_records = []
        old_records_map = {}
        new_records_map = {}
        for rec in fis_table_old.values():
            old_records_map[rec.rec[0]] = rec
        for rec in fis_table.values():
            new_records_map[rec.rec[0]] = rec
        all_recs = set(new_records_map.keys() + old_records_map.keys())
        for key in all_recs:
            new_rec = new_records_map.get(key)
            old_rec = old_records_map.get(key)
            if new_rec != old_rec:
                new_records.append(new_records_map.get(key))
                old_records.append(old_records_map.get(key))
    added = deleted = changed = 0
    for old_rec, new_rec in zip(old_records, new_records):
        if new_rec is None and old_rec is None:
            echo('record %r does not exist' % (key, ))
        elif new_rec is None:
            deleted += 1
            if not summary:
                echo(old_rec)
                echo('record has been DELETED')
        elif old_rec is None:
            added += 1
            if not summary:
                echo(new_rec)
                echo('record has been ADDED')
        else:
            # only show key fields and changed fields, unless user specified --full
            key_field_pre = fis_table.datamap[0]
            changed_fields = []
            field_changed = False
            for field_meta in fis_table.fieldlist:
                index, desc, _, spec, _ = field_meta
                old_data = old_rec[spec]
                new_data = new_rec[spec]
                if spec.startswith(key_field_pre):
                    changed_fields.append((index.split('_')[1], spec, old_data, new_data, desc))
                    data_width = max(data_width, len(old_data), len(new_data))
                elif old_data != new_data or full:
                    field_changed = True
                    changed_fields.append((index.split('_')[1], spec, old_data, new_data, desc))
                    data_width = max(data_width, len(str(old_data)), len(str(new_data)))
            if field_changed:
                changed += 1
            if summary:
                continue
            data_width = 30
            lines = []
            def select_color(row):
                old, new = row[2:4]
                if old == new:
                    return white, white, white|bold, white|bold, white
                else:
                    return white, white, red, green, white
            string_template = ColorTemplate(
                    '%%3s | %%-12s | %%-%ds | %%-%ds | %%s' % (data_width, data_width),
                    default_color=all_reset+cyan,
                    select_colors=select_color,
                    )
            numeric_template = ColorTemplate(
                    '%%3s | %%-12s | %%%ds | %%%ds | %%s' % (data_width, data_width),
                    default_color=all_reset+cyan,
                    select_colors=select_color,
                    )
            for line in changed_fields:
                index, spec, old, new, desc = line
                if '$' in spec:
                    lines.append(string_template(index, spec, old, new, desc))
                else:
                    lines.append(numeric_template(index, spec, old, new, desc))
            echo('\n'.join(lines))
            if os.isatty(sys.stdout.fileno()):
                try:
                    raw_input('press <enter> to continue')
                except KeyboardInterrupt:
                    abort('\n<Ctrl-C>, aborting')
    echo('\nAdded:   %4d' % added)
    echo('Deleted: %4d' % deleted)
    echo('Changed: %4d' % changed)


@Command(
        start=Spec('where to start checking', OPTION),
        )
def integrity_check(start=1):
    """
    FIS: check tables for key/record mismatches.
    """
    i = start - 1
    while 'checking more tables':
        if i > 400:
            break
        i += 1
        try:
            table = fd.fisData(i)
        except TableError:
            cls, exc, tb = sys.exc_info()
            error('%10s  [%3d]:  %s' % (exc.filename, i, exc.__class__.__name__))
        except KeyError:
            pass
        else:
            if table.corrupted:
                error('%10s  [%3d]: %7d records,  %4d corrupted' % (table.filename, i, len(table), table.corrupted))
            else:
                print('%10s  [%3d]: %7d records' % (table.filename, i, len(table)))


@Command(
        filenum=Spec('file abbreviation or number to operate on', default='all', type=unicode.upper),
        which=Spec('which field to display', default='all', type=unicode.upper),
        )
def field_check(filenum, which):
    """
    FIS: checks numeric fields for bad values.
    """
    if filenum != 'all':
        if filenum.isdigit():
            filenum = int(filenum)
        files = [filenum]
    else:
        files = [k for k in fd.tables if isinstance(k, (int, long))]
    for filenum in files:
        print('file: %s' % (filenum,), end=' ', verbose=0)
        try:
            table = fd.fisData(filenum)
        except TableError, exc:
            print('<%s>' % exc.__doc__, verbose=0)
            continue
        print(table.datamap)
        if which != 'all':
            fields = [which]
        else:
            fields = [f for f in table.datamap if '$' not in f]
        print('(%d records, %d numeric fields)' % (len(table), len(fields)), end='  ', verbose=0)
        ints = floats = 0
        bad_values = defaultdict(lambda: defaultdict(int))
        for record in table.values():
            for field in fields:
                val = record[field]
                try:
                    int(val)
                    ints += 1
                except ValueError:
                    try:
                        float(val)
                        floats += 1
                    except ValueError:
                        bad_values[field][val] += 1
        print('-- int: %s  --  float: %s' % (ints, floats), verbose=0)
        if bad_values:
            for field, values in bad_values.items():
                print('     %s: %s' % (field, ', '.join(repr(v) for v in values.items())), verbose=0)
        table.release()


@Command(
    quick=('use local copy of product descriptions', FLAG),
    update=Spec('update OpenERP cross references',  FLAG),
    items=Spec('item number to look up', MULTI, usage='ITEM'),
    )
def product_description(quick, update, *items):
    """
    FIS: retrieve and save the latest product descriptions.
    """
    if not quick:
        # get the data
        print('getting data')
        with user_ids(0, 0):
            job = Execute(
                    'ssh %(host)s cat %(file)s' % {
                        'host': config.openerp.full_description_host,
                        'file': config.openerp.full_description_path,
                        },
                    pty=True,
                    )
        if job.returncode or job.stderr:
            abort(job.stderr, returncode=job.returncode)
        else:
            with open(config.network.fis_data_local_path/'product_descriptions.txt', 'w') as f:
                f.write(job.stdout)
            print('data saved')
    if items:
        # display the requested items
        print('reading data')
        with open(config.network.fis_data_local_path/'product_descriptions.txt') as f:
            lines = f.read().strip().split('\n')
        print('looking for item(s)')
        for line in lines:
            match = re.match('(.{40})  \((\d{6})\)  (.*)$', line)
            if match:
                fis_desc, item_code, full_desc = match.groups()
                if fis_desc in items:
                    echo('%s:  %s' % (item_code, full_desc))
    if update:
        abort('update not currently supported')
        print('updating -all- cross-reference codes')
        cross_ref = oe.get_model('fis_integration.customer_product_cross_reference')
        current_items = dict(
                (r.fis_code, r.id)
                for r in get_records(
                    cross_ref,
                    domain=[('list_code','=','-all-')],
                    ))
        print('  %d existing items' % len(current_items))
        #
        # TODO
        # method of getting saleable items has changed -- this section needs to move
        # to another function
        #
        # get saleable items from OpenERP
        saleable_items = dict(
                (r.xml_id, r.id)
                for r in get_records(
                    product,
                    domain=[('sale_ok','=',True),('active','=',True),('fis_availability_code','=','Y')],
                    fields=['id','xml_id']),
                    )
        new = updated = 0
        for fis_code, product_id in ViewProgress(saleable_items.items()):
                print('  code: %r' % (fis_code, ), verbose=3)
                values = {
                        'key': '-all--%s' % (fis_code, ),
                        'list_code': '-all-',
                        'fis_code': fis_code,
                        'fis_product_id': product_id,
                        'customer_product_code': fis_code,
                        'source': 'fis',
                        }
                crossref_id = current_items.pop(fis_code, None)
                if crossref_id is None:
                    # create it
                    cross_ref.create(values)
                    new += 1
                else:
                    # update it
                    cross_ref.write(crossref_id, values)
                    updated += 1
        removed = len(current_items)
        if current_items:
            print('removing %d cross references' % len(current_items))
            cross_ref.unlink(current_items.values())
        print('%d existing/updated items\n%d added items\n%d deleted items' %
                (updated, new, removed)
                )


@Command(
    items=Spec('item number to look up', MULTI, usage='ITEM'),
    )
def product_forecast(*items):
    """
    FIS: retrieve and save the latest forecast data for ITEMS (default is all).
    """
    if not items:
        items = []
        nvty = fd.fisData('NVTY1', keymatch="%s101000    101**")   # 135
        for item_rec in ViewProgress(
                nvty,
                'getting %d item numbers' % len(nvty),
                view_type='bar',
            ):
            items.append(item_rec[F135.item_id])
        print('%d items retrieved' % len(items), verbose=2)
    else:
        items = list(items)
    items = items
    items = ViewProgress(
            (i+'\n' for i in items + ['exit']),
            'communicating with 11.111',
            view_type='bar',
            total=len(items),
            )
    start = time.time()
    with user_ids(0, 0):
        result = Execute(
                'ssh 192.168.11.111 /usr/local/bin/fis-query forecast',
                pty=True,
                input=items,
                password_timeout=0,
                )
    stop = time.time()
    minutes, seconds = divmod(stop-start, 60)
    hours, minutes = divmod(minutes, 60)
    print('time with 11.111: %d:%d:%d' % (hours, minutes, seconds))
    output = [l for l in result.stdout.strip().split('\n') if len(l.split(':')) == 3]
    with open(PRODUCT_FORECAST, 'w') as f:
        for line in ViewProgress(output):
            f.write(line+'\n')
    if script_verbosity >= 2:
        print('\n'.join(output), verbose=2)


@Command(
        filenum=Spec('file abbreviation or number to operate on', ),
        template=Spec('exact, subset (%s), or regex template to match many records to', force_default=None),
        code=Spec('code to match with template', force_default=None, type=lambda s: s and tuple(s.split(',') or s)),
        fields=Spec('specific fields to display [default: all]', MULTI, type=int),
        dbf_name=Spec('dbf to create with data', OPTION),
        tabular=Spec('save output in tab-delimited mode [default: dump_<filenum>]', OPTION, None, default='dump'),
        regex=Spec('template is a re match', FLAG, abbrev=('r', 're')),
        test=Spec('output in format usable by test_scripts', FLAG, abbrev=None),
        check_old=Spec('use older version of data files', FLAG, None),
        table=Spec('show output in a table', FLAG, None),
        )
def records(filenum, template, code, fields, dbf_name, tabular, regex, test, check_old, table):
    """
    FIS: display complete records according to criteria.
    """
    print('fields requested: %s' % (fields, ))
    print('template: %r' % (template, ))
    print('code given: %r' % (code, ))
    show_table = table
    if filenum.isdigit():
        filenum = int(filenum)
    else:
        filenum = filenum.lower()
    if template and not code:
        template, code = None, tuple(template.split(','))
    if template is None:
        filenum, table_name, template = table_keys.get(filenum, (None, None, None))
        if template is None:
            # if not isinstance(filenum, int):
            abort('no default template exists for %r' % filenum)
        if code is not None:
            regex = True
    print('template: %r' % (template, ))
    print('code given: %r' % (code, ))
    target_path = check_old and config.network.fis_data_local_old_path or None
    if regex:
        if not code:
            abort('CODE required for REGEX match')
        code = code[0]
        fis_table = fd.fisData(filenum, rematch=template, data_path=target_path)
        print('using regex and file', fis_table.filename, 'in', target_path or config.network.fis_data_local_path)
        records = fis_table.get_rekey(code) or []
    else:
        fis_table = fd.fisData(filenum, subset=template, data_path=target_path)
        print('using subset and file', fis_table.filename, 'in', target_path or config.network.fis_data_local_path)
        records = [v for k, v in fis_table.get_subset(code)]
    if test:
        try:
            enum = getattr(fis_schema, 'F%d' % fis_table.number)
        except AttributeError:
            abort('Table %r has no file number, unable to generate test output' % fis_table.filename)
    print('  found %d records' % (len(records), ))
    used_fields = []
    table_names = []
    if records:
        # get field defs now, may be needed for dbf creation
        record = records[0]
        print('widths:', record._widths, verbose=2)
        # max_data_width = record._width
        max_spec_width = 0
        field_widths = []
        dbf_types = []
        dbf_names = []
        if fields:
            fis_fields = [(i-1, record.fieldlist[i-1]) for i in fields]
        else:
            fis_fields = list(enumerate(record.fieldlist))
        for i, row in fis_fields:
            # j = i + 1
            print('checking for %d' % (i, ), end='... ', verbose=2)
            # if not fields or i in fields:
            print('keeping', end='', verbose=2)
            name, spec = row[1:4:2]
            if not name.strip() or name.strip().lower() == '(open)':
                continue
            table_names.append(name)
            max_spec_width = max(max_spec_width, len(spec.strip()))
            width = fis_table.field_widths[i]
            field_widths.append(width)
            field_name = convert_name(name, 10, dbf_names)
            dbf_names.append(field_name)
            name = convert_name(name, 50)
            if '$' in spec:
                dbf_types.append('%s C(%d)' % (field_name, width))
                used_fields.append((i, str))
            else:
                dbf_types.append('%s N(17,5)' % field_name)
                used_fields.append((i, float))
            print(verbose=2)
        if dbf_name:
            print('dbf fields:\n  ', '\n   '.join(dbf_types))
            table = dbf.Table(dbf_name, dbf_types).open(dbf.READ_WRITE)
    try:
        fields = [t[0] for t in used_fields]
        print('fields: %r' % (fields, ), border='flag', verbose=2)
        output = []
        for record in records:
            field_data = tuple(record[i] for i in fields)
            output.append(field_data)
            # for i, row in enumerate(fis_fields):
            lines = format_record(record, fields)
            if test:
                for i, datum in zip(fields, field_data):
                    echo('%s: %s,' % (enum[i-1], repr(datum).strip('u')))
            elif not dbf_name and not tabular and not show_table and not test and lines:
                echo('\n'.join(lines))
                try:
                    ans = input('[Continue|Quit]', default='continue')
                    if ans == 'quit':
                        raise KeyboardInterrupt
                except KeyboardInterrupt:
                    raise SystemExit(1)
            elif dbf_name:
                data = []
                for i, (_, converter) in enumerate(used_fields):
                    print(i, converter, verbose=3)
                    # cnv = converter[1]
                    data.append(converter(field_data[i]))
                print('field data:', data, verbose=3)
                table.append(tuple(data))
            if not dbf_name and not tabular:
                echo()
        if tabular:
            if tabular == 'dump':
                tabular = 'dump_%03d' % filenum
            with open(tabular,'w') as fh:
                for record in output:
                    fh.write("\t".join(map(str,record))+"\n")
        if show_table:
            if table_names:
                echo([table_names, None] + output, border='table')
            else:
                error('no records found')
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        if records and dbf_name:
            table.close()


@Command(
        filenum=Spec('file abbreviation or number to display', ),
        output=Spec('output type', choices=['dump','enum'], default='dump'),
        number=Spec('number to use for enum output (when using an abbr for FILENUM)', OPTION, type=int),
        )
def schema(filenum, output, number):
    """
    FIS: show schema for selected table.
    """
    if filenum.isdigit():
        filenum = int(filenum)
    table = fd.tables[filenum]
    if output == 'dump':
        max_width = 0
        for field in table['fields']:
            max_width = max(max_width, len(field[1]))
        max_width += 10
        echo(table['name'], table['desc'], table['filenum'])
        dotted = True
        field_num = 0
        last_field = None
        for i, field in enumerate(table['fields']):
            if not i % 3:
                dotted = not dotted
            name = '  ' + field[1]
            spec = field[3]
            current_field = spec.split('(')[0]
            if current_field != last_field or current_field.lower() == 'i':
                field_num += 1
                last_field = current_field
                display_field_num = '%2d' % field_num
            if dotted:
                name += '.' * (max_width - len(name))
            else:
                name += ' ' * (max_width - len(name))
            echo('%3d  %s' % (i+1, display_field_num), name, spec)
            display_field_num = '  '
    elif output == 'enum':
        echo('class F%d(FISenum):' % (number or table['filenum']))
        echo('    """')
        echo('    %s - %s' % (table['name'], table['desc'].strip('-')))
        echo('    """')
        echo('    #')
        echo('    _init_ = "value sequence"')
        echo('    _order_ = lambda m: m.sequence')
        echo('    #')
        lines = []
        for i, field in enumerate(table['fields']):
            name, spec = field[1:4:2]
            comment = name
            name = convert_name(name, 50)
            lines.append((name, spec, i, comment))
        #calculate widths
        max_name = max([len(n) for n, s, i, c in lines])
        max_spec = max([len(s) for n, s, i, c in lines]) + 2
        for name, spec, fld, comment in lines:
            if name:
                echo('    %-*s = %r, %*d     # %s' % (max_name, name, spec, max_spec-len(spec)+1, fld, comment))
            else:
                echo(' ' * (max_name + max_spec + 16), '# %s %s' % (comment, spec))
    else:
        abort('unknown output type: %s' % output)


@Command()
def tables():
    """
    FIS: list tables.
    """
    keys = [k for k in fd.tables.keys() if isinstance(k, (int,long))]
    # template = '%4d: %s%s'
    numerical = True
    if not keys:
        # only alpha table names
        keys = [k for k in fd.tables.keys()]
        # template = '%s: %s'
        numerical = False
    keys.sort()
    for k in keys:
        t = fd.tables[k]
        if numerical:
            echo('%4d: %s%s' % (k, t['name'], t['desc']))
        else:
            echo('%-7s: %s%s' % (k, t['name'], t['desc']))


@Command(
        filenum=Spec('file abbreviation or number to operate on', ),
        subset=Spec('subset template to match many records to', ),
        code=Spec('code to match with template', force_default='', type=lambda s: s and tuple(s.split(',') or s)),
        fields=Spec('specific fields to display', MULTI, type=int),
        counts=Spec('only show counts', FLAG, None),
        )
def values(filenum, subset, code, fields, counts):
    """
    FIS: show all values for selected fields.
    """
    if not fields:
        abort('no FIELDS specified')
    # adjust for zero-based numbering
    fields = [i-1 for i in fields]
    if filenum.isdigit():
        filenum = int(filenum)
    fis_table = fd.fisData(filenum, subset=subset)
    table_spec = fd.tables[filenum]
    table_fields = []
    for i, row in enumerate(table_spec['fields']):
        if i not in fields:
            continue
        name, spec = row[1:4:2]
        table_fields.append((name, spec, set()))
    for rec in [v for k, v in fis_table.get_subset(code)]:
        for name, spec, values in table_fields:
            values.add(rec[spec])
    for name, spec, values in table_fields:
        if counts:
            print('%-23s:  %7d' % (name, len(values)), verbose=0)
        else:
            print('%s:  ' % name, ', '.join([repr(v) for v in sorted(values)]), verbose=0)
    if counts:
        print('%-23s:  %7d' % ('Total Records', len(fis_table)), verbose=0)


@Command()
def self_test():
    """
    Perform various tests.

    - record matching for sql select
    """
    # records = [
    #         dict(id=1, name='Ethan', age=646, city='Rosalia'),
    #         dict(id=2, name='Garrett', age=38, city='Spokane'),
    #         dict(id=3, name='Elizabeth', age=38, city='Spokane'),
    #         dict(id=4, name='William Kuth', age=21, city='rosalia'),
    #         dict(id=5, name='Cecilie kuth', age=17, city='Rosalia'),
    #         dict(id=6, name='jillian kuth', age=13, city='ROSALIA'),
    #         ]
    #
    import test
    test

## helpers

alnum = translator(keep='abcdefghijklmnopqrstuvwxyz0123456789')
alnum_space = translator(to=' ', keep='abcdefghijklmnopqrstuvwxyz0123456789 ')

imd_methods = {
        'id': lambda rec,_: '%05d' % (rec.id, ),
        'tag': lambda rec,field: alnum(rec[field].lower()),
        'name': lambda rec,field: ''.join(w[0] for w in alnum_space(rec[field].lower())),
        }


class abstractclassmethod(classmethod):
    __isabstractmethod__ = True
    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)

def convert_name(name, max_len, existing_names=()):
    original_name = name
    name = name.lower()
    if '(' in name:
        name = name.split('(')[0]
    name = name.replace('.', '')
    for text in (' code', ' codes'):
        if name.endswith(text):
            name = name[:-len(text)+1] + 'id' + ('', 's')[text[-1] == 's']
            break
    pieces = name.split()
    if pieces and pieces[0].isdigit() and pieces[1:2] == ['spaces']:
        pieces = pieces[2:]
    for i, p in enumerate(pieces):
        if len(p) == 3 and '/' in p:
            pieces[i] = p[0] + p[2]
    name = ' '.join(pieces)
    if name.startswith(('key type', 'key group')):
        name = 'key type'
    members = []
    # name substitution
    for i, piece in enumerate(re.sub('\W+', ' ', name).split()):
        if i == 0 and piece[0].isdigit():
            piece = numbers.get(piece, piece)
        else:
            piece = common.get(piece, piece)
        members.append(piece)
    # shrink further as necessary
    def no_under(names):
        return ''.join(names)
    def pop_under(names):
        # if we get down to only one name, just trim it to desired size
        if len(names) == 1:
            return names[0][:max_len]
        names.pop()
        return '_'.join(names)
    name = '_'.join(members)
    shrinker = cycle([no_under, pop_under])
    # shrink name if needed
    if len(name) > max_len:
        # first try uncommon abbr
        for i, m in enumerate(members):
            members[i] = uncommon.get(m, m)
        name = '_'.join(members)
    while len(name) > max_len:
        func = next(shrinker)
        name = func(members)
    # check for name already being used
    for suffix in range(1, 10):
        if name not in existing_names:
            break
        else:
            suffix = str(suffix)
            name = name[:-1] + suffix
    else:
        # name still taken
        raise Exception(
                'unable to convert %r\nexisting names: '
                % (original_name, ', '.join(existing_names)
                ))
    return name

def convert_set(clausa):
    """
    Converts the SET clause of an UPDATE command.
    """
    values = {}
    while clausa:
        # e.g. login = 'ethan'
        #      id=201
        #      blah = null, this = 'that'
        print('set', clausa, verbose=3)
        try:
            field, op, value, clausa = re.match(
                    "^"
                    "(\w+)"
                    "\s*(=)\s*"
                    "("
                        "'[^']*'"
                        "|"
                        "[^ ]*"
                        ")"
                    "\s*"
                    "(.*?)\s*"
                    "$",
                    clausa,
                    ).groups()
            print('\nfield: %r\nop: %r\nvalue: %r\nclausa: %r\n' % (field, op, value, clausa), verbose=2)
            if not (field and op and value):
                raise ValueError
        except (ValueError, AttributeError):
            raise ValueError('malformed SET clause')
        else:
            lval = value.lower()
            if (
                    value[0] == value[-1] == '"'
                 or value[0] == value[-1] == "'"
                 ):
                value = eval(value)
            elif lval in ('t', 'true'):
                value = True
            elif lval in ('f', 'false'):
                value = False
            elif lval == 'none':
                value = False
            elif lval == 'null':
                value = False
            else:
                try:
                    oval = value
                    value = eval(value)
                except Exception:
                    raise ValueError('cannot use/convert data: %r' % (oval, ))
            values[field] = value
            if clausa.startswith(','):
                clausa = clausa[1:].lstrip()
    return values

def convert_where(clausa, alias=None, infix=False, strip_quotes=True):
    """
    Converts the WHERE clause of an SQL command.
    """
    def subquery(match):
        print('subquery:', match, verbose=2)
        command = match.group()[1:-1]
        echo(command, verbose=0)
        if not command.upper().startswith(('SELECT ','COUNT ')):
            raise ValueError('subquery must be SELECT or COUNT')
        if command.upper().startswith('COUNT '):
            return str(sql_count(command, separator=False))
        else:  # SELECT
            result = sql_select(command, separator=False, wrap=(), _internal='subquery')
            if not result:
                return '[]'
            fields = result.records[0].keys()
            if len(fields) == 1:
                # must be id
                return str([r.id for r in result])
            elif len(fields) == 2:
                fields.remove('id')
                field = fields.pop()
                return str([r[field] for r in result])
            else:
                raise ValueError('only one field can be returned from subqueries')
    if alias is None:
        alias = {}
    print('subquery: %r,  clausa: %r' % (subquery, clausa), verbose=2)
    clausa = re.sub(r"\(.*\)", subquery, clausa)
    print('after subquery: %r' % (clausa, ), verbose=2)

    std_match = Var(lambda clausa: re.match(
            r"^(\S+)\s*(is not|is|not in|in|like|=like|not like|ilike|=ilike|not ilike|<=|>=|!=|==?|<|>)\s*('(?:[^'\\]|\\.)*?'|\[[^]]*\]|\S*)\s*(.*?)\s*$",
            clausa,
            flags=re.I
            ))
    enh_match = Var(lambda clausa: re.match(
            r"^(\w+)\((\S+)\)\s*(<=|>=|!=|=|<|>)\s*('(?:[^'\\]|\\.)*?'|\S*)\s*(.*?)\s*$",
            clausa,
            flags=re.I
            ))
    date_match = Var(lambda clausa: re.match(
            r"\d\d\d\d-\d\d-\d\d$",
            clausa,
            ))
    donde = []
    constraints = []
    while clausa:
        # e.g. WHERE login = 'ethan'
        #      WHERE id=201
        #      WHERE blah is not null AND this = 'that'
        #      WHERE count(fis_portal_logins) > 1
        #      WHERE 'Warehouse notes' is not null  (future enhancement)
        #      WHERE id in (SELECT res_id FROM ir.model.data WHERE name =like 'F074_%_res_partner')
        print('clausa: %r' % (clausa, ), verbose=3)
        if std_match(clausa):
            field, op, condition, clausa = std_match().groups()
            print('\nfield: %r\nop: %r\ncond: %r\nwhere: %r\n' % (field, op, condition, clausa), verbose=3)
            if not (field and op and condition):
                raise ValueError('std: malformed WHERE clause')
            if op == '==':
                op = '='
            lop = op.lower()
            lcond = condition.lower()
            if (
                    condition[0] == condition[-1] == '"'
                 or condition[0] == condition[-1] == "'"
                 ):
                if strip_quotes:
                    condition = condition[1:-1]
            elif lcond in ('t', 'true'):
                condition = True
            elif lcond in ('f', 'false'):
                condition = False
            elif lcond == 'none':
                condition = None
            elif lcond == 'null':
                pass
            elif lcond[0] == '[' and lcond[-1] == ']':
                condition = literal_eval(condition)
            elif date_match(lcond):
                condition = lcond.replace('-','')
            else:
                try:
                    condition = int(condition)
                except ValueError:
                    try:
                        condition = float(condition)
                    except ValueError:
                        raise ValueError('unknown data type: %r %r' % (type(condition), condition))
            if condition is not False and condition == 0:
                condition = 0.0
            elif (lop, lcond) == ('is', 'null'):
                op, condition = '=', False
            elif (lop, lcond) == ('is not', 'null'):
                op, condition = '!=', False
            donde.append((alias.get(field,field),op,condition))
            if clausa.lower().startswith('or '):
                if infix:
                    donde.append('|')
                else:
                    donde.insert(0, '|')
                clausa = clausa[3:]
            elif clausa.lower().startswith('and '):
                if infix:
                    donde.append('&')
                else:
                    donde.insert(0, '&')
                clausa = clausa[4:]
        elif enh_match(clausa):
            function, field, op, condition, clausa = enh_match().groups()
            print('\nfunction: %r\nfield: %r\nop: %r\ncond: %r\nwhere: %r\n' % (function, field, op, condition, clausa), verbose=3)
            if not (function and field and op and condition):
                raise ValueError('enh: malformed WHERE clause')
            func = function.lower()
            if func.startswith('count'):
                if op == '=':
                    op = '=='
                func = length(alias.get(field,field), op, condition)
                constraints.append(func)
                donde.append((1,'=',1))
            else:
                raise ValueError('unknown command in WHERE clause: %r' % function)
        else:
            raise ValueError('malformed WHERE clause')
    return donde, constraints

class counter(object):

    def __init__(self, start=0):
        self.value = start

    def __iter__(self):
        return self

    def __next__(self):
        current = self.value
        self.value += 1
        return current

    next = __next__

def ensure_oe():
    """
    abort if OpenERP is unavailable
    """
    if oe is None:
        abort('OpenERP is not running; only FIS functions/tables available.')

class ExpandedRow(object):
    "converts an ordered dict into an ordered list of lists"

    def __init__(self, fields, record):
        # fields = [
        #   'xml_id',
        #   'hr_insurance_choice_ids/year_month',
        #   'hr_insurance_choice_ids/medical',
        #   'hr_insurance_choice_ids/dental',
        #   'hr_insurance_choice_ids/vision',
        #   'hr_insurance_choice_ids/life',
        #   'name_related',
        #   'home_country_id/name',
        #   'home_country_id/code',
        #   'user_ids',
        #   'user_ids/partner_id',
        #   ]
        #
        # record = {
        #   'id': 8274
        #   'xml_id': 1374,
        #   'hr_insurance_choice_ids': [
        #           {
        #            'id': 810,
        #            'year_month': '2018-07',
        #            'medical':'children',
        #            'dental':'children',
        #            'vision':'children',
        #            'life':'self',
        #           },
        #           {
        #            'id': 81820,
        #            'year_month': '2018-06',
        #            'medical':'children',
        #            'dental':'children',
        #            'vision':'children',
        #            'life':'self',
        #           }],
        #   'name_related': 'Vishan Vishal Dimri',
        #   'home_country_id': {'id':235, 'name':'United States', 'code':'US'},
        #   'user_ids': [
        #           AttrDict(id=960, partner_id=Many2One(id=51540, name='Heb 063 Healthy Living'),
        #               groups_id=[90, 229], alias_id=1090,
        #               ),
        #           ],
        #   }
        print('ExpandedRow.__init__: fields ->', fields, '  record ->', record, verbose=4)
        rows = []
        row = []
        cache = {}
        iter_fields = []
        for fld in fields:
            fld = fld.split('/',1)[0]
            if fld not in iter_fields:
                iter_fields.append(fld)
        for k in iter_fields:
            v = record[k]
            print('checking %s -> %r' % (k, v), verbose=4)
            cache[k] = set()
            if any([f.startswith(k+'/') for f in fields]):
                sub_fields = []
                for f in fields:
                    if f == k:
                        sub_fields.append('<self>')
                    elif f.startswith(k+'/'):
                        sub_fields.append(f.split('/', 1)[1])
                if v:
                    # many2one = dict
                    # x2many = list
                    if isinstance(v, (list, tuple)):
                        sub_row = []
                        for er in [ExpandedRow(sub_fields, w) for w in v]:
                            for sr in er:
                                sub_row.append(tuple(sr))
                    elif isinstance(v, AttrDict):
                        if v:
                            sub_row = [[v[f] for f in sub_fields]]
                        else:
                            sub_row = [[None] * len(sub_fields)]
                    else:
                        raise TypeError('invalid type: %r [%r]' % (type(v), v))
                else:
                    sub_row = [[None] * len(sub_fields)]
                print('adding subrow', sub_row, verbose=4)
                row.append(sub_row)
            elif k in fields:
                # must go after subfield checking
                print('  adding element ->', k, verbose=4)
                row.append(v)
            print('intermediate row ->', row, verbose=4)
        print('final row ->', row, verbose=4)
        for i in counter():
            line = []
            remaining = False
            for item in row:
                if not isinstance(item, list):
                    if i:
                        # not first line
                        line.append(None)
                    else:
                        # first line
                        line.append(item)
                else:
                    if len(item) > i:
                        line.extend([item[i]])
                        remaining = True
                    else:
                        if item:
                            line.extend([None] * len(item))
                        else:
                            line.extend([None])
            print('processed row ->', line, verbose=3)
            rows.append(line)
            if not remaining:
                break
        if rows:
            last_row = rows[-1]
            if all([c is None for c in last_row]):
                rows.pop()
        self.rows = rows

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)

    def __repr__(self):
        return repr(self.rows)

def format_record(record, fields=None):
    # record: the fis record to format
    # fields: list of ints, or list of (int, record)s
    lines = []
    name_width = 11
    value_width = 40
    mask_width = 0
    fieldlist = record.fieldlist
    if not fields:
        fields = range(len(record.fieldlist))
    # for i, row in enumerate(record.fieldlist):
    #     if i in fields:
    for i in fields:
        row = fieldlist[i]
        name_width = max(len(row[3]), name_width)
        value_width = max(len(str(record[row[3]]).rstrip()), value_width)
        mask_width = max(len(str(fieldlist[i][4])), mask_width)
        print(
                'field %d -> name width: %d   value width: %d   mask wdith: %d'
                    % (i, name_width, value_width, mask_width),
                verbose=4,
                )
    print(verbose=4)
    # for i, row in enumerate(record.fieldlist):
    #     if i in fields:
    for i in fields:
        row = fieldlist[i]
        value = record[row[3]]
        if isinstance(value, basestring):
            value = value.replace('\0', u'\u2400')
            leading_spaces = 0
            for ch in value:
                if ch != ' ':
                    break
                leading_spaces += 1
            value = leading_spaces * u'\u2422' + value.lstrip()
            if u'\u2422' in value or u'\u2400' in value:
                echo('value is:', value)
        print('field %d -> %r' % (i, value), verbose=4)
        if '$' in row[3] and not fieldlist[i][4]:
            lines.append('%5d | %*s | %*s | %*s | %s' % (i+1, -name_width, row[3], mask_width, fieldlist[i][4], -value_width, value, row[1]))
        else:
            lines.append('%5d | %*s | %*s | %*s | %s' % (i+1, -name_width, row[3], mask_width, fieldlist[i][4], value_width, value, row[1]))
    return lines

def html2text(html, wrap):
    html = html.replace('<br>', '\n').replace('<p>', '\n').replace('<div>', '\n')
    for tag in (
            '</br>',
            '</p>', '</div>',
            '<b>', '</b>',
            '<span>', '</span>',
            '<i>', '</i>',
            ):
        tmp = []
        html = html.replace(tag, '')
    if wrap:
        while html:
            target = wrap
            while len(html) > target and html[target] not in ' \n\t':
                target -= 1
                if target <= 10:
                    target = wrap
                    break
            tmp.append(html[:target].strip())
            html = html[target:]
        html = '\n'.join(tmp)
    html = html.replace('\n\n', '\n').replace('\n\n', '\n').strip()
    html = html.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return html

def length(field, op, cond):
    d = {}
    exec("def length(rec):\n  return len(rec['%s']) %s %s" % (field, op, cond), d)
    return d['length']

def maybe_lower(value):
    if isinstance(value, basestring):
        value = value.lower()
    return value

def normalize_field_names(model, fields):
        # currently unused
        #
        # make sure top-level fields are db names, not user names
        ambiguous_fields = {}
        model_strings = {}
        model_fields = set()
        for field_name, field_def in model.fields_get().items():
            print('adding: %r' % (field_name, ), verbose=2)
            model_fields.add(field_name)
            string = field_def['string'].lower()
            if string in model_strings:
                model_strings[string] = None
                ambiguous_fields.setdefault(string, []).append(field_name)
            else:
                model_strings[string] = field_name
        actual_fields = []
        for fld in fields:
            fld = fld.lower()
            extra = None
            db_f = None
            if '/' in fld:
                fld, extra = fld.split('/', 1)
            if fld[0] != "'" or fld[-1] != "'":
                # unquoted fields should be db names, but fall back to user names if not found
                if fld in model_fields:
                    db_f = fld
            if db_f is None:
                if fld[0] == fld[-1] == "'":
                    # remove enclosing quotes
                    fld = fld[1:-1]
                if fld in ambiguous_fields:
                    raise ValueError('%r could be any of: %s' % ','.join(ambiguous_fields[string]))
                elif fld not in model_strings:
                    raise ValueError('unknown field: %r' % (fld, ))
                else:
                    db_f = model_strings[fld]
            if extra is not None:
                db_f += '/' + extra
            actual_fields.append(db_f)
            assert len(actual_fields) == len(fields), "fields/actual_fields length mismatch:\n%r\n%r" % (fields, actual_fields)
            fields[:] = actual_fields

def oe_export(name, domain=ALL_ACTIVE, table=None, to_file=None):
    if to_file[-4:].lower() not in ('.txt', '.csv', '.xls') and to_file != '-':
        raise ValueError('unknown file type for %s' % to_file)
    found = []
    for export in get_records(oe, 'ir.exports', domain=[('name','=',name)]):
        found.append(export.resource)
        if table and export.resource == table:
            break
    else:
        # no exact match, check only one match found
        if not found:
            raise ValueError('no export found with name of %r' % (name, ))
        elif len(found) > 1:
            raise ValueError('multiple matches for %r:\npossible tables: %s'
                    % (name, ', '.join(found)))
    # at this point, export is the one we want
    table = export.resource
    fields_ids = export.export_fields
    fields = [
            f['name']
            for f in get_records(
                oe,
                'ir.exports.line',
                domain=[('id','in',fields_ids)],
                fields=['name'],
                )]
    q = Query(oe.get_model(table), domain=domain, fields=fields[:])
    #
    if to_file.endswith('.xls'):
        write_xls(export.name, q, fields, to_file)
    elif to_file.endswith('.csv'):
        write_csv(export.name, q, fields, to_file)
    elif to_file.endswith('.txt') or to_file == '-':
        write_txt(export.name, q, fields, to_file)

def write_xls(sheet_name, query, fields, file, separator=False):
    import xlwt
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(sheet_name)
    #
    for i, field_name in enumerate(fields):
        worksheet.write(0, i, query.names[field_name] or field_name.upper())
        worksheet.col(i).width = 8000 # around 220 pixels
        # TODO: calculate width base on column contents
    #
    i = 0
    for r in query.records:
        print(r, verbose=3)
        if separator:
            i += 1
        er = ExpandedRow(fields, r)
        for row in er:
            i += 1
            ci_bump = 0
            for cell_index, cell_value in enumerate(row):
                if isinstance(cell_value, Many2One):
                    cell_value = str(cell_value)
                    # print('skipping m2o', cell_value, verbose=4)
                elif isinstance(cell_value, (list, tuple)):
                    print('cell_value ->', cell_value, verbose=4)
                    for cv in cell_value:
                        if isinstance(cv, Many2One):
                            worksheet.write(i, cell_index+ci_bump, cv)
                        elif cv:
                            cv = re.sub(r"\r", r" ", cv)
                            cv = re.sub(r'"', r'\"', cv)
                            cv = '%s' % cv
                            worksheet.write(i, cell_index+ci_bump, cv)
                        else:
                            worksheet.write(i, cell_index+ci_bump, '')
                        ci_bump += 1
                    continue
                elif isinstance(cell_value, basestring):
                    cell_value = re.sub(r"\r", r" ", cell_value)
                    cell_value = re.sub(r'"', r'\"', cell_value)
                    cell_value = '%s' % cell_value
                elif cell_value in (False, None):
                    cell_value = ''
                elif cell_value is True:
                    cell_value = 'True'
                elif isinstance(cell_value, dbf.Date):
                    cell_value = cell_value._date
                elif isinstance(cell_value, dbf.DateTime):
                    cell_value = cell_value.replace(tzinfo=None)._datetime
                worksheet.write(i, cell_index, cell_value)
    workbook.save(file)

def write_csv(table, query, fields, file, separator=False):
    lines = []
    line = []
    print('field count:', len(fields), fields, verbose=3)
    for field_name in fields:
        line.append(field_name)
    print(repr(line), verbose=4)
    lines.append(','.join(line))
    #
    for r in query.records:
        if separator:
            lines.append('')
        er = ExpandedRow(fields, r)
        for row in er:
            line = []
            for cell_value in row:
                if isinstance(cell_value, Many2One):
                    cell_value = str(cell_value)
                    # print('skipping m2o', cell_value, verbose=4)
                elif isinstance(cell_value, (list, tuple)):
                    print('cell_value [sequence] ->', cell_value, verbose=4)
                    for cv in cell_value:
                        if cv:
                            if isinstance(cv, basestring):
                                cv = re.sub("\r", r" ", cv)
                                cv = re.sub(r'"', r'""', cv)
                                cv = cv.replace('\\','\\\\')
                                cv = re.sub('\n', r'\\n', cv)
                                cv = '"%s"' % cv
                                line.append(cv)
                            elif isinstance(cv, bool):
                                line.append(str(int(cv)))
                            elif cv is None:
                                line.append('')
                            elif isinstance(cv, Binary):
                                line.append('b64"%s"' % cv.to_base64())
                            else:
                                line.append(str(cv))
                        else:
                            line.append('')
                    continue
                elif isinstance(cell_value, basestring):
                    print('cell_value [basestring] ->', cell_value, verbose=4)
                    cell_value = re.sub("\r", r" ", cell_value)
                    cell_value = re.sub(r'"', r'""', cell_value)
                    cell_value = cell_value.replace('\\', '\\\\')
                    cell_value = re.sub('\n', r'\\n', cell_value)
                    cell_value = r'"%s"' % cell_value
                elif isinstance(cell_value, Binary):
                    cell_value = '"%s"' % cell_value.to_base64()
                elif isinstance(cell_value, bool):
                    cell_value = int(cell_value)
                elif cell_value is None:
                    cell_value = ''
                line.append(str(cell_value))
            lines.append(','.join(line))
    print('\n'.join([repr(l) for l in lines]), verbose=4)
    with open(file, 'wb') as output:
        output.write('\n'.join(lines).encode('utf8'))

def write_txt(table, query, fields, file, separator=False, wrap=None,):
    lines = []
    line = []
    print('field count:', len(fields), fields, verbose=4)
    for field_name in fields:
        field_header = field_name.upper()
        aliases = getattr(query, 'aliases', {})
        if script_verbosity:
            field_header += "\n%s" % aliases.get(field_name, field_name)
        line.append(field_header)
        # line.append('%s\n%s' % (query.names[field_name] or field_name.upper(), field_name))
    lines.append(line)
    #
    for r in query.records:
        if separator:
            lines.append(None)
        print(r, verbose=4)
        er = ExpandedRow(fields, r)
        [print(r, verbose=4) for r in er]
        for row in er:
            print('post pre-process row ->', row, verbose=3)
            line = []
            for field_name, (cell_index, cell_value) in zip(fields, enumerate(row)):
                if isinstance(cell_value, Many2One):
                    if SHOW_ID:
                        line.append('[%6s] %s' % (cell_value.id, cell_value.name))
                    else:
                        line.append(cell_value.essence())
                elif isinstance(cell_value, (list, tuple)):
                    for cv in cell_value:
                        if isinstance(cv, Many2One):
                            if SHOW_ID:
                                line.append('[%6s] %s' % (cv.id, cv.name))
                            else:
                                line.append(cv.essence())
                        elif isinstance(cv, basestring):
                            cv = '%s' % cv
                            line.append(cv)
                        elif cv is None:
                            line.append('')
                        else:
                            line.append(cv)
                elif isinstance(cell_value, basestring):
                    cell_value = '%s' % cell_value
                    line.append(cell_value)
                elif cell_value is None:
                    line.append('')
                else:
                    line.append(cell_value)
                if field_name in wrap:
                    wrap_value = wrap[field_name]
                    line[-1] = html2text(line[-1], wrap_value)
            print('post post-process line ->', line, verbose=3)
            lines.append(line)
    if not separator:
        lines.insert(1, None)
    if file == '-':
        echo(lines, border='table')
    else:
        with open(file, 'w') as out:
            echo(lines, border='table', file=out)

class SQLError(Exception):
    """
    Error in SQL statement.
    """

class Table(object):
    """
    FIS or OpenERP table.

    Subclasses must also provide the following attributes:
    - fields
    """
    __metaclass__ = ABCMeta
    tables = {}
    command_table_pat = r"(COUNT\s*FROM|DELETE\s*FROM|DESCRIBE|DIFF .*? FROM|REPORT .*? FROM|SELECT .*? FROM|INSERT INTO|UPDATE)\s*(\S*)"

    def __new__(cls, table_name):
        """
        Select the FISTable or OpenERPTable depending on table_name.
        """
        if '.' in table_name:
            table = super(Table, OpenERPTable).__new__(OpenERPTable, table_name)
        else:
            table = super(Table, FISTable).__new__(FISTable, table_name)
        return table

    def __getattr__(self, name):
        return getattr(self.table, name)

    @abstractmethod
    def __init__(self, table_name):
        """
        Represent an FIS or OpenERP table.
        """

    @abstractproperty
    def fields(self):
        """
        Names and definitions of the table's fields as a dict.
        """

    @abstractclassmethod
    def query(cls, command):
        """
        Extract command and primary table, then call cls.query to process.
        """
        try:
            cmd, table_name = re.match(cls.command_table_pat, command, re.I).groups()
        except AttributeError:
            raise SQLError('command and/or table missing from query')
        table = cls(table_name)
        method = getattr(table, 'sql_%s' % cmd.lower().split()[0])
        print('%s.%s --> ' % (table.name, method.__name__), end='', verbose=2)
        q = method(command)
        print(q, verbose=2)
        if not isinstance(q, (Query, SimpleQuery)):
            raise TypeError('%r did not return a (Simple)Query, but a %r' % (method.__name__, type(q).__name__))
        return q
        # table.query = q
        # return table

    @abstractmethod
    def sql_count(self, command):
        """
        Return count of records matching criteria.
        """

    @abstractmethod
    def sql_delete(self, command):
        """
        Remove records from table.
        """

    @abstractmethod
    def sql_describe(self, command):
        """
        Show layout of table.
        """

    @abstractmethod
    def sql_diff(self, command):
        pass

    @abstractmethod
    def sql_insert(self, command):
        pass

    @abstractmethod
    def sql_select(self, command):
        pass

    @abstractmethod
    def sql_update(self, command):
        pass

class FISTable(Table):
    """
    Handle interactions with FIS table.
    """
    def __init__(self, table_name):
        print('FIS table %r' % table_name)
        if table_name.isdigit():
            table = int(table_name)
            source_name = 'filenum'
        else:
            table = table_name.lower()
            source_name = 'name'
        print('FIS table %r' % table)
        if table in table_keys:
            print(0)
            self.num, self.name, self.pat = table_keys[table]
        else:
            print(1)
            if table not in fd.tables:
                print(2)
                for desc in fd.tables.values():
                    print(3)
                    if table == maybe_lower(desc[source_name]):
                        print(4)
                        table = desc['filenum']
                        break
                else:
                    print(5)
                    raise ValueError('table %r not found' % table_name)
            print(6)
            print('FIS table %r' % table)
            table = fd.tables[table]
            self.num = table['filenum']
            self.name = table['name']
            self.pat = ''
            # count = 0
            # for _, _, _, spec, _ in table['fields']:
            #     if spec.startswith('An$'):
            #         count += int(spec.split(',')[1].strip(')'))
            # self.pat = '.' * count
        self.table = fd.fisData(self.num)
        print('%3s: %s --> %r' % (self.num, self.name, self.table), verbose=2)
        # get human-usable field names
        fields_by_name = {}
        fields_by_number = {}
        print('getting fields', verbose=2)
        for i, field in enumerate(self.table.fieldlist, start=1):
            name, spec = field[1:4:2]
            comment = name
            name = convert_name(name, 50)
            fields_by_name[name] = i, name, spec, comment
            fields_by_number[i] = i, name, spec, comment
            print(repr(i), name, spec, comment, verbose=4)
        self._fields_by_name = fields_by_name
        self._fields_by_number = fields_by_number

    @property
    def fields(self):
        return self._fields_by_name.copy()

    @property
    def fields_by_number(self):
        return self._fields_by_number.copy()

    def query(self, fields, to_file='-', domain=ALL_ACTIVE, order=(), distinct=False, separator=False, wrap=(), _constraints=()):
        """

        """

    def create_filter(self, domain, aliases):
        """
        Determine if the record should be included in the result set.
        """
        #
        # ['&','&','|','&',('id','=',99),('name','ilike','ethan'),('age','>',25),('gender','!=','female'),('eye_color','in',['green','brown'])]
        #
        # AND ('id','=',99),('name','ilike','ethan')
        #
        # OR  ('age','>',25)
        #
        # AND ('gender','!=','female')
        #
        # AND ('eye_color','in',['green','brown'])
        #
        root = Node()
        stack = [root]
        print('domain:', domain, verbose=2)
        for clause in domain:
            print('  stack:', stack, verbose=3)
            print('  clause:', clause, verbose=3)
            current_node = stack[-1]
            if isinstance(clause, tuple) and len(clause) == 3:
                field, op, target = clause
                field = aliases[field]
                current_node.add((field, op, target))
                if current_node.complete:
                    stack.pop()
                continue
            elif clause == '&':
                new_node = And()
            elif clause == '|':
                new_node = Or()
            elif clause == '!':
                new_node = Not()
            else:
                raise ValueError('clauses must be &, |, !, or three-element tuples')
            current_node.add(new_node)
            if current_node.complete:
                stack.pop()
            stack.append(new_node)
        return root


    def _records(self, fields, aliases, where, constraints):
        print('fields requested: %s' % (fields, ), verbose=2)
        print('where: %r' % (where, ), verbose=2)
        print('constraints: %r' % (constraints, ), verbose=2)
        filter = self.create_filter(where, aliases)
        print('filter:', filter, verbose=2)
        records = []
        for k, v in self.table.items():
            if filter(v):
                print(k, sep='\n', verbose=4)
                if all(c(v) for c in constraints):
                    row = []
                    for f in fields:
                        if f == 'id' and 'id' not in aliases:
                            continue
                        row.append(v[aliases[f]])
                    records.append(AttrDict(*zip(fields, row)))
        return records

    def sql_count(self, command):
        temp = command.split()
        if len(temp) > 1 and temp[1].upper() == 'FROM':
            temp.insert(1, 'id')
            command = ' '.join(temp)
        query = self.sql_select(command, _internal=True)
        sq = SimpleQuery(self.name, ('table', 'count'))
        sq.records.append(AttrDict(table=self.table.name, count=len(query)))
        sq.status = "COUNT %s" % len(query)
        return sq

    def sql_delete(self, command):
        """
        Not supported.
        """
        raise NotImplementedError('cannot delete records from FIS tables')

    def sql_describe(self, command, _internal=''):
        """
        DESCRIBE table
            [ORDER BY (name|index)]
        """
        order_match = Var(lambda hs: re.search(r'ORDER\s*BY\s*(name|index)\s*$', hs, re.I)) 
        index = 0
        if order_match(command):
            order ,= order_match.groups()
            if order.lower() == 'name':
                index = 1
            elif order.lower() == 'index':
                index = 0
            else:
                raise ValueError('unknown ORDER BY: %r' % order)
        defs = sorted(self.fields.values(), key=lambda t: t[index])
        sq = SimpleQuery(self.name, ('index', 'name','spec','comment'))
        for d in defs:
            sq.records.append(AttrDict(*zip(('index','name','spec','comment'), d)))
        sq.status = "DESCRIBE 1"
        return sq

    def sql_diff(self, command):
        pass

    def sql_insert(self, command):
        """
        Not supported.
        """
        raise ValueError('cannot insert records into FIS tables')

    def sql_select(self, command, _internal=''):
        """
        SELECT field_name [AS name1][, field_name [AS name2][, ...]]
            FROM table
            [WHERE ...]
            [ORDER BY field1 [ASC|DESC] [, field2 [ASC|DESC] [, ...]]]
            [TO file]
        """
        as_match = Var(lambda sel: re.match(r'(\S+)\s+AS\s+(\S+)', sel, re.I)) 
        table_match = Var(lambda sel: re.match(r'(\S+)\s+AS\s+(\S+)\b(.*)', sel, re.I)) 
        table_alias = {}
        field_alias = {}
        fields = []
        header = []
        print('getting table description', verbose=2)
        for desc in self.sql_describe('order by index', _internal=True):
            if desc['name']:
                # field_alias_master[row[0]] = row[0], row[1]
                # field_alias_master[row[1]] = row[0], row[1]
                field_alias[str(desc['index'])] = desc['spec']
                field_alias[desc['name']] = desc['spec']
                fields.append(desc['name'])
        imprimido = '-'
        orden = ''
        clausa = ''
        donde = []
        distinta = False
        print('command: %r' % (command, ), verbose=3)
        command = ' '.join(command.split())
        print('command: %r' % (command, ), verbose=2)
        if not re.search(r' from ', command, flags=re.I):
            raise ValueError('FROM not specified')
        if command.split()[-2].lower() == 'to':
            imprimido = command.split()[-1]
            command = ' '.join(command.split()[:-2])
        #
        # get SELECT fields
        #
        seleccion, resto = re.split(r' from ', command, maxsplit=1, flags=re.I)
        print('0 SELECT: %r   REST: %r' % (seleccion, resto), verbose=3)
        seleccion = seleccion.split()[1:]
        if not seleccion:
            raise ValueError('missing fields')
        if seleccion[0].upper() == 'DISTINCT':
            distinta = True
            seleccion.pop(0)
        if not seleccion:
            raise ValueError('missing fields')
        # get field names if * specified
        if seleccion == ['*']:
            seleccion = sorted(fields)
        else:
            seleccion = [s.strip() for s in ' '.join(seleccion).split(',')]
        for i, field in enumerate(seleccion):
            if as_match(field):
                field, alias = as_match.groups()
                bbx_index = field_alias[field]
                field_alias[alias] = bbx_index
                seleccion[i] = alias
                if SHOW_ID:
                    if field.isdigit:
                        header.append('%s - %s' % (self._fields_by_number[int(field)][0], alias))
                    else:
                        header.append('%s - %s' % (self._fields_by_name[int(field)][0], alias))
                else:
                    header.append(alias)
            elif field == 'id':
                # phony field used for COUNTing
                pass
            else:
                if field.isdigit():
                    alias = self._fields_by_number[int(field)][1]
                    if SHOW_ID:
                        header.append('%s - %s' % (field, self._fields_by_number[int(field)][1]))
                    else:
                        header.append(alias)
                else:
                    alias = self._fields_by_name[field][1]
                    if SHOW_ID:
                        header.append('%s - %s' % (self._fields_by_name[field][0], field))
                    else:
                        header.append(alias)

                bbx_index = field_alias[field]
                field_alias[alias] = bbx_index
                seleccion[i] = alias
        #
        #
        # get FROM table: `res.users` or `res.users u`
        #
        if table_match(resto):
            table, alias, resto = table_match.groups()
            table_alias[alias] = table
            resto = resto.split()
            resto.insert(0, alias)
        else:
            resto = resto.split()
        desde, resto = resto[0], resto[1:]
        print('0 FROM: %r   REST: %r' % (desde, resto), verbose=3)
        if desde.upper() in ('', 'WHERE', 'ORDER'):
            raise ValueError('missing table')
        # check for alias
        if resto and resto[0].upper() not in ('', 'WHERE', 'ORDER'):
            alias, resto = resto[0], resto[1:]
            print('0 ALIAS: %r   REST: %r' % (alias, resto), verbose=3)
            table_alias[alias] = desde
            desde = alias
        if table_alias.get(desde, desde) not in self.tables:
            self.tables[desde] = Table(table_alias.get(desde,desde))
        # table = self.tables[desde]
        if resto:
            if resto[0].upper() == 'WHERE':
                resto = resto[1:]
                if not resto or ' '.join(resto[:2]).upper() == 'ORDER BY':
                    raise ValueError('missing WHERE clause')
                resto = ' '.join(resto)
                if re.search(r' ORDER BY ', resto, flags=re.I):
                    clausa, resto = re.split(r' ORDER BY ', resto, maxsplit=1, flags=re.I)
                    resto = 'ORDER BY ' + resto
                    # clausa, orden = re.split(r' ORDER BY ', resto, maxsplit=1, flags=re.I)
                    # print('-1 orden being set to', repr(orden), verbose=2)
                else:
                    clausa, resto = resto, ''
                clausa = clausa.strip()
                # orden = orden.strip()
                # print('-2 orden being set to', repr(orden), verbose=2)
                resto = resto.split()
            if ' '.join(resto[:2]).upper() == 'ORDER BY':
                orden = [o.strip() for o in ' '.join(resto[2:]).split(',')]
                print('-3 orden being set to', repr(orden), verbose=2)
                resto = []
            if resto:
                raise ValueError('malformed query [%r]' % (' '.join(resto), ))
        print('1 WHERE', repr(clausa), verbose=2)
        print('1 ORDER BY', repr(orden), verbose=2)
        print('1 TO', repr(imprimido), verbose=2)
        # normalize_field_names(desde, seleccion, clausa, orden)
        print('1 FROM', repr(desde), verbose=2)
        #
        # and get WHERE clause
        #
        donde, constraints = convert_where(clausa)
        if _internal:
            imprimido = ''
        print('2 WHERE', repr(donde), verbose=2)
        print('2 ORDER BY', repr(orden), verbose=2)
        print('2 TO', repr(imprimido), verbose=2)
        print('2 CONSTRAINTS', repr(constraints), verbose=2)
        #
        # at this point we have the fields, and the table -- get the records
        #
        sq = SimpleQuery(self.name, header, aliases=field_alias)
        print('getting records', verbose=2)
        sq.records.extend(self._records(seleccion, field_alias, donde, constraints))
        print('sorting records')
        for o in reversed(orden):
            o = o.split()
            if len(o) == 1:
                o.append('ASC')
            f, d = o    # field, direction
            if d.upper() == 'ASC':
                sq.records.sort(key=lambda r: r[f])
            else:
                sq.records.sort(key=lambda r: r[f], reverse=True)
        sq.status = "SELECT %s" % len(sq.records)
        return sq

    def sql_update(self, command):
        """
        Not supported.
        """
        raise NotImplementedError('cannot update records in FIS tables')

class OpenERPTable(Table):
    """
    Handle interactions with OpenERP model.
    """
    def __init__(self, table_name):
        ensure_oe()
        if table_name not in self.tables:
            self.tables[table_name] = oe.get_model(table_name)
        self.table = self.tables[table_name]
        self.name = self.table.model_name

    @property
    def fields(self):
        return self.table._all_columns.copy()

    def query(self, command):
        """
        Process records matching criteria.
        """
        check_command = ' '.join(command.lower().split())
        if check_command.startswith('select '):
            self.query = self.sql_select(command)
        elif check_command.startswith('count '):
            self.query = self.sql_count(command)
        elif check_command.startswith('describe '):
            self.query = self.sql_describe(command)
        elif check_command.startswith('update '):
            self.query = self.sql_update(command)
        elif check_command.startswith('insert into '):
            self.query = self.sql_insert(command)
        elif check_command.startswith('delete from '):
            self.query = self.sql_delete(command)
        elif check_command.startswith('diff '):
            self.query = self.sql_diff(command)
        else:
            raise SQLError('invalid command: %r...' % check_command[:13])
        return self

    def sql_count(self, command):
        """
        COUNT
            FROM table
            [WHERE ...]
            [ORDER BY field1 [ASC|DESC] [, field2 [ASC|DESC] [, ...]]]
            [TO file] # ignored
        """
        temp = command.split()
        if len(temp) > 1 and temp[1].upper() == 'FROM':
            temp.insert(1, 'id')
            command = ' '.join(temp)
        query = self.sql_select(command, _internal=True)
        sq = SimpleQuery(self.name, ('table', 'count'))
        sq.records.append(AttrDict(table=self.table.model_name, count=len(query)))
        sq.status = "COUNT %s" % len(query)
        return sq

    def sql_delete(self, command):
        """
        DELETE FROM table
            [WHERE ...]
        """
        global tables
        tables = {}
        pieces = command.split()
        if len(pieces) < 3:
            raise ValueError('table not specified')
        table = pieces[2]
        try:
            tables[table] = table = oe.get_model(table)
        except Fault as exc:
            if "doesn't exist" in exc.faultCode:
                raise ValueError('unknown table %r' % (table, ))
            raise
        if len(pieces) > 3 and pieces[3].lower() != 'where':
            raise ValueError('malformed command -- missing WHERE keyword')
        where_clause = ' '.join(pieces[4:])
        domain, constraints = convert_where(where_clause)
        if constraints:
            raise ValueError('constraints not supported in DELETE command')
        #
        # have all the info, make the changes
        #
        print('domain: %r' % (domain, ), verbose=2)
        ids = table.search(domain)
        if not ids:
            echo('no records found matching %r' % (where_clause, ))
        print('deleting %d records from %s' % (len(ids), table._name), verbose=2)
        table.unlink(ids)
        sq = SimpleQuery(self.name, ('table', 'count'))
        sq.records.append(AttrDict(table=self.table.model_name, count=len(ids)))
        sq.status = "DELETE %s" % len(ids)
        return sq

    def sql_describe(self, command):
        """
        DESCRIBE table
            [ORDER BY field]
        """
        command = command.lower()
        if ' order by ' in command:
            orden = command.split(' order by ')[1].strip()
            if orden not in ('field','display','type','help'):
                raise ValueError('ORDER BY must be one of field, display, type, or help [ %r ]')
            sort = {
                'field': lambda t: t[0],
                'display': lambda t: t[1]['string'],
                'type': lambda t: t[1]['type'],
                'help': lambda t: t[1]['help'],
                }[orden]
        else:
            sort = lambda t: t[0]
        seleccion = sorted(self.table._all_columns.items(), key=sort)
        # table = [('Field','Display','Type','Detail','Help'), None]
        sq = SimpleQuery(self.name, ('field','display','type','detail','help'))
        for field, desc in seleccion:
            display = desc['string']
            help = desc.get('help') or ''
            type = desc['type']
            details = []
            if 'function' in desc:
                details.append('function %s: %s' % (type, desc['function']))
            if type in ('one2many', 'many2one', 'many2many'):
                relation = desc.get('relation')
                if relation:
                    if type == 'one2many':
                        reverse = desc.get('relation_field')
                        if reverse:
                            relation = '%s, %s' % (relation, reverse)
                    details.append('relation: %s' % relation)
                domain = desc.get('domain')
                if domain:
                    if isinstance(domain, (bytes, str)):
                        domain = literal_eval(domain)
                    details.append('domain: %s' % '\n        '.join([str(d) for d in domain]))
                context = desc.get('context')
                if context:
                    if isinstance(context, (bytes, str)):
                        context = literal_eval(context)
                    details.append('context: %s' % '\n         '.join(['%s=%r' % (k, v) for k, v in context.items()]))
            for info in ('digits', 'selection', 'size', 'states'):
                data = desc.get(info)
                if data:
                    if isinstance(data, list) and info in ('selection', 'states'):
                        data = '|'.join([t[1] for t in data if t[1]])
                    # if info in wrap:
                    #     data = html2text(data, wrap[info])
                    # else:
                    #     try:
                    #         if len(data) > 40:
                    #             data = data[:37] + '...'
                    #     except TypeError:
                    #         pass
                    details.append('%s: %s' % (info, data))
            details = '\n'.join(details)
            sq.records.append(AttrDict(
                    field=field, display=display, type=type, detail=details, help=help
                    ))
        sq.status = "DESCRIBE 1"
        return sq

    def sql_diff(self, command):
        """
        use SELECT to get all records/fields, then diff them
        """
        changed_only = False
        if command.upper().startswith('DIFF ^ '):
            changed_only = True
            command = command[:5] + '*' + command[6:]
        query = self.sql_select(command, _internal='-binary -html')
        if not query.records:
            raise ValueError('no records found')
        if len(query.records) == 1:
            # if only one record, display all fields
            changed_only = False
        sq = SimpleQuery(self.name, ['fields \ ids']+[rec['id'] for rec in query.records], record_layout='column')
        fields = query.records[1].keys()
        fields.remove('id')
        for field in fields:
            row = []
            for record in query.records:
                row.append(record[field])
            no_diff = all_equal(row)
            if changed_only and no_diff:
                continue
            final_row = []
            for cell_value in row:
                if isinstance(cell_value, Many2One):
                    final_row.append('[%6s] %s' % (cell_value.id, cell_value.name))
                elif isinstance(cell_value, (list, tuple)):
                    new_value = []
                    for cv in cell_value:
                        if isinstance(cv, Many2One):
                            new_value.append('[%6s] %s' % (cv.id, cv.name))
                        elif isinstance(cv, basestring):
                            cv = '%s' % cv
                            new_value.append(cv)
                        elif cv is None:
                            new_value.append('')
                        else:
                            new_value.append(cv)
                    final_row.append('\n'.join(new_value))
                else:
                    final_row.append(cell_value)
            final_row.insert(0, '%s %s' % ('^ '[no_diff], field))
            sq.records.append(final_row)
        sq.status = "DIFF %s" % (len(sq.records)-1)
        return sq

    def sql_insert(self, command):
        """
        INSERT INTO table (field1, field2, field3, ...) VALUES (val1, val2, val3, ...)
        INSERT INTO table FILE <filename.csv>
        """
        # use re to isolate fields and values
        fv_match = Var(lambda c: re.match(r" *INSERT +INTO +(.*) +\((.*)\) +VALUES +\((.*)\)( *UPDATE ON *)?(.*)?", c, re.I))
        fl_match = Var(lambda c: re.match(r" *INSERT +INTO +(.*) +FILE +(\S*)( *UPDATE ON *)?(.*)?", c, re.I))
        if not fv_match(command) and not fl_match(command):
            raise ValueError('malformed command; use --help for help')
        elif fv_match():
            table, fields, values, verb, key = fv_match.groups()
            fields = [f.strip() for f in fields.split(',') if f != ',']
            print('%r -- %r -- %r -- %r -- %r' % (table, fields, values, verb, key), verbose=4)
            data = [literal_eval(values)]
        elif fl_match():
            table, csv_file, verb, key = fl_match.groups()
            try:
                csv = CSV(csv_file)
            except (IOError, OSError) as exc:
                raise ValueError("problem with %r -- <%r>" % (csv_file, repr(exc), ))
            fields = csv.header
            print('%r -- %r -- %r -- %r' % (table, csv_file, verb, key), verbose=4)
            data = list(csv)
        if verb and (verb.strip().lower() != 'update on' or not key):
            raise ValueError('invalid UPDATE ON clause')
        if key and key not in fields:
            raise ValueError('key %r no in FIELDS')
        try:
            table = oe.get_model(table)
        except Fault as exc:
            if "doesn't exist" in exc.faultCode:
                raise ValueError('unknown table %r' % (table, ))
            raise
        if not all_equal(data, test=lambda r,l=len(fields): len(r) == l):
            # print('fields: %r\nvalues: %r' % (fields, values), verbose=2)
            raise ValueError('fields/values mismatch')
        # create the record(s)
        insert_count = 0
        update_count = 0
        for row in data:
            values = dict(zip(fields, row))
            if key:
                # try update operation first
                records = table.search([(key,'=',values[key])])
                if records:
                    table.write(records[0], values)
                    update_count += 1
                    continue
            # either no key, or record doesn't exist
            try:
                print('creating', values, verbose=2)
                table.create(values)
            except Exception as exc:
                raise
                error('unable to create:\n', pprint.pformat(values))
                raise ValueError(repr(exc))
            insert_count += 1
        sq = SimpleQuery(self.name, ('table','inserted','updated'))
        sq.records.append(AttrDict(table=self.table.model_name, inserted=insert_count, updated=update_count))
        sq.status = "INSERT %s / UPDATE %s" % (insert_count, update_count)
        return sq

    def sql_select(self, command, _internal=''):
        """
        SELECT field_name [AS name1][, field_name [AS name2][, ...]]
            FROM table
            [WHERE ...]
            [ORDER BY field1 [ASC|DESC] [, field2 [ASC|DESC] [, ...]]]
            [TO file]
        """
        as_match = Var(lambda sel: re.match(r'(\S+)\s+AS\s+(\S+)', sel, re.I)) 
        header = []
        field_alias = {}        # {alias_name: field_name}
        imprimido = '-'
        orden = ''
        clausa = ''
        donde = []
        distinta = False
        print('command: %r' % (command, ), verbose=3)
        command = ' '.join(command.split())
        print('command: %r' % (command, ), verbose=2)
        if not re.search(r' from ', command, flags=re.I):
            raise ValueError('FROM not specified')
        if command.split()[-2].lower() == 'to':
            imprimido = command.split()[-1]
            command = ' '.join(command.split()[:-2])
        #
        # get SELECT fields
        #
        seleccion, resto = re.split(r' from ', command, maxsplit=1, flags=re.I)
        seleccion = seleccion.split()[1:]
        if not seleccion:
            raise ValueError('missing fields')
        if seleccion[0].upper() == 'DISTINCT':
            distinta = True
            seleccion.pop(0)
        if not seleccion:
            raise ValueError('missing fields')
        if seleccion != ['*']:
            seleccion = [s.strip() for s in ' '.join(seleccion).split(',')]
            if SHOW_ID and 'id' not in [s.lower() for s in seleccion]:
                seleccion.insert(0, 'id')


        for i, field in enumerate(seleccion):
            if as_match(field):
                field, alias = as_match.groups()
                field_alias[alias] = field
                seleccion[i] = alias
                header.append(alias)
            else:
                header.append(field)

                
        print('SELECT:', seleccion, verbose=2)
        #
        #
        # get FROM table
        #
        resto = resto.split()
        desde, resto = resto[0], resto[1:]
        if desde.upper() in ('', 'WHERE', 'ORDER'):
            raise ValueError('missing table')
        self.tables[desde] = table = Table(desde)
        if resto:
            if resto[0].upper() == 'WHERE':
                resto = resto[1:]
                if not resto or ' '.join(resto[:2]).upper() == 'ORDER BY':
                    raise ValueError('missing WHERE clause')
                resto = ' '.join(resto)
                if re.search(r' ORDER BY ', resto, flags=re.I):
                    clausa, orden = re.split(r' ORDER BY ', resto, maxsplit=1, flags=re.I)
                else:
                    clausa = resto
                clausa = clausa.strip()
                orden = orden.strip()
                resto = []
            if ' '.join(resto[:2]).upper() == 'ORDER BY':
                orden = ' '.join(resto[2:])
                resto = []
            if resto:
                raise ValueError('malformed query [%r]' % (resto, ))
        # get field names if * specified
        if seleccion == ['*']:
            # fields = list(model._all_columns.keys())
            fields = list(table.fields.keys())
            if isinstance(table, OpenERPTable):
                if '-binary' in _internal:
                    for field in table._binary_fields:
                        fields.remove(field)
                if '-x2many' in _internal:
                    for field in table._x2many_fields:
                        fields.remove(field)
                if '-html' in _internal:
                    for field in table._html_fields:
                        fields.remove(field)
            fields.remove('id')
            seleccion = ['id'] + sorted(fields)
            header = seleccion[:]
            print('SELECT:', seleccion, verbose=2)
        #
        # TODO: now make sure all field names are db and not user
        #
        print('WHERE', clausa, verbose=2)
        print('ORDER BY', orden, verbose=2)
        print('TO', imprimido, verbose=2)
        # normalize_field_names(desde, seleccion, clausa, orden)
        print('FROM', desde, verbose=2)
        #
        # and get WHERE clause
        #
        donde, constraints = convert_where(clausa, field_alias)
        if _internal:
            imprimido = ''
        print('WHERE', donde, verbose=2)
        print('ORDER BY', orden, verbose=2)
        print('TO', imprimido, verbose=2)
        print('CONSTRAINTS', constraints, verbose=2)
        #
        # at this point we have the fields, and the table -- hand off to _adhoc()
        #
        fields = list(seleccion)
        echo(header)
        echo(fields)
        echo(donde)

        query = Query(
                self.table,
                fields=fields[:],
                aliases=field_alias,
                domain=donde or ALL_ACTIVE,
                order=orden,
                unique=distinta,
                to_file = imprimido,
                constraints=constraints,
                )
        query.status = 'SELECT %d' % len(query)
        query.fields = header
        query.alias = field_alias
        return query

    def sql_update(self, command):
        """
        UPDATE table
            SET field_name=... [, field_name=... [...]]
            [WHERE ...]
        """
        global tables
        tables = {}
        pieces = command.split()
        if len(pieces) < 2:
            raise ValueError('table not specified')
        table = pieces[1]
        try:
            tables[table] = table = oe.get_model(table)
        except Fault as exc:
            if "doesn't exist" in exc.faultCode:
                raise ValueError('unknown table %r' % (table, ))
            raise
        if len(pieces) < 3 or pieces[2].lower() != 'set':
            raise ValueError('malformed command -- missing SET keyword')
        command = ' '.join(pieces[3:])
        try:
            where_index = command.lower().index(' where ')
            where_clause = command[where_index+7:]
            set_clause = command[:where_index]
        except ValueError:
            if command.lower().endswith(' where'):
                raise ValueError('malformed command -- missing WHERE parameters')
            where_clause = []
            set_clause = command
        print('where clause: %r' % (where_clause, ), verbose=2)
        values = convert_set(set_clause)
        if not values:
            raise ValueError('malformed command -- no changes specified')
        if where_clause:
            domain, constraints = convert_where(where_clause)
        else:
            domain = constraints = []
        if constraints:
            raise ValueError('constraints not supported in UPDATE command')
        #
        # have all the info, make the changes
        #
        print('domain: %r' % (domain, ), verbose=2)
        ids = table.search(domain)
        print('writing\n  %r\nto %s for ids\n%r' % (values, table._name, ids), verbose=2)
        table.write(ids, values)
        sq = SimpleQuery(self.name, ('table', 'updated'))
        sq.records.append(AttrDict(table=self.table.model_name, updated=len(ids)))
        sq.status = 'UPDATE %d' % len(ids)
        return sq

class ResultsTable(Table):
    """
    Results table
    """
    def __init__(self, header, fields):
        self.header = header
        self.fields = fields

    def __repr__(self):
        return "ResultsTable(header=%r, fields=%r)" % (self.header, self.fields)

    def query(self, fields, to_file='-', domain=ALL_ACTIVE, order=(), distinct=False, separator=False, wrap=(), _constraints=()):
        """

        """

    def sql_count(self, command):
        temp = command.split()
        if len(temp) > 1 and temp[1].upper() == 'FROM':
            temp.insert(1, 'id')
            command = ' '.join(temp)
        query = self.sql_select(command, _internal=True)
        sq = SimpleQuery(('table', 'count'))
        sq.records.append(AttrDict(table=self.table.name, count=len(query)))
        sq.status = "COUNT %s" % len(query)
        return sq

    def sql_delete(self, command):
        """
        Not supported.
        """
        raise NotImplementedError('cannot delete records from FIS tables')

    def sql_describe(self, command, _internal=''):
        """
        DESCRIBE table
            [ORDER BY (name|index)]
        """
        order_match = Var(lambda hs: re.search(r'ORDER\s*BY\s*(name|index)\s*$', hs, re.I)) 
        index = 0
        if order_match(command):
            order ,= order_match.groups()
            if order.lower() == 'name':
                index = 1
            elif order.lower() == 'index':
                index = 0
            else:
                raise ValueError('unknown ORDER BY: %r' % order)
        defs = sorted(self.fields.values(), key=lambda t: t[index])
        sq = SimpleQuery(('index', 'name','spec','comment'))
        for d in defs:
            sq.records.append(AttrDict(*zip(('index','name','spec','comment'), d)))
        sq.status = "DESCRIBE 1"
        return sq

    def sql_diff(self, command):
        pass

    def sql_insert(self, command):
        """
        Not supported.
        """
        raise ValueError('cannot insert records into FIS tables')

    def sql_select(self, command, _internal=''):
        """
        SELECT field_name [AS name1][, field_name [AS name2][, ...]]
            FROM table
            [WHERE ...]
            [ORDER BY field1 [ASC|DESC] [, field2 [ASC|DESC] [, ...]]]
            [TO file]
        """
        as_match = Var(lambda sel: re.match(r'(\S+)\s+AS\s+(\S+)', sel, re.I)) 
        table_match = Var(lambda sel: re.match(r'(\S+)\s+AS\s+(\S+)\b(.*)', sel, re.I)) 
        table_alias = {}
        field_alias = {}
        fields = []
        header = []
        print('getting table description', verbose=2)
        for desc in self.sql_describe('order by index', _internal=True):
            if desc['name']:
                # field_alias_master[row[0]] = row[0], row[1]
                # field_alias_master[row[1]] = row[0], row[1]
                field_alias[str(desc['index'])] = desc['spec']
                field_alias[desc['name']] = desc['spec']
                fields.append(desc['name'])
        imprimido = '-'
        orden = ''
        clausa = ''
        donde = []
        distinta = False
        print('command: %r' % (command, ), verbose=3)
        command = ' '.join(command.split())
        print('command: %r' % (command, ), verbose=2)
        if not re.search(r' from ', command, flags=re.I):
            raise ValueError('FROM not specified')
        if command.split()[-2].lower() == 'to':
            imprimido = command.split()[-1]
            command = ' '.join(command.split()[:-2])
        #
        # get SELECT fields
        #
        seleccion, resto = re.split(r' from ', command, maxsplit=1, flags=re.I)
        print('0 SELECT: %r   REST: %r' % (seleccion, resto), verbose=3)
        seleccion = seleccion.split()[1:]
        if not seleccion:
            raise ValueError('missing fields')
        if seleccion[0].upper() == 'DISTINCT':
            distinta = True
            seleccion.pop(0)
        if not seleccion:
            raise ValueError('missing fields')
        # get field names if * specified
        if seleccion == ['*']:
            seleccion = sorted(fields)
        else:
            seleccion = [s.strip() for s in ' '.join(seleccion).split(',')]
        for i, field in enumerate(seleccion):
            if as_match(field):
                field, alias = as_match.groups()
                bbx_index = field_alias[field]
                field_alias[alias] = bbx_index
                seleccion[i] = alias
                if SHOW_ID:
                    if field.isdigit:
                        header.append('%s - %s' % (self._fields_by_number[int(field)][0], alias))
                    else:
                        header.append('%s - %s' % (self._fields_by_name[int(field)][0], alias))
                else:
                    header.append(alias)
            elif field == 'id':
                # phony field used for COUNTing
                pass
            else:
                if field.isdigit():
                    alias = self._fields_by_number[int(field)][1]
                    if SHOW_ID:
                        header.append('%s - %s' % (field, self._fields_by_number[int(field)][1]))
                    else:
                        header.append(alias)
                else:
                    alias = self._fields_by_name[field][1]
                    if SHOW_ID:
                        header.append('%s - %s' % (self._fields_by_name[field][0], field))
                    else:
                        header.append(alias)

                bbx_index = field_alias[field]
                field_alias[alias] = bbx_index
                seleccion[i] = alias
        #
        #
        # get FROM table: `res.users` or `res.users u`
        #
        if table_match(resto):
            table, alias, resto = table_match.groups()
            table_alias[alias] = table
            resto = resto.split()
            resto.insert(0, alias)
        else:
            resto = resto.split()
        desde, resto = resto[0], resto[1:]
        print('0 FROM: %r   REST: %r' % (desde, resto), verbose=3)
        if desde.upper() in ('', 'WHERE', 'ORDER'):
            raise ValueError('missing table')
        # check for alias
        if resto and resto[0].upper() not in ('', 'WHERE', 'ORDER'):
            alias, resto = resto[0], resto[1:]
            print('0 ALIAS: %r   REST: %r' % (alias, resto), verbose=3)
            table_alias[alias] = desde
            desde = alias
        if table_alias.get(desde, desde) not in self.tables:
            self.tables[desde] = Table(table_alias.get(desde,desde))
        # table = self.tables[desde]
        if resto:
            if resto[0].upper() == 'WHERE':
                resto = resto[1:]
                if not resto or ' '.join(resto[:2]).upper() == 'ORDER BY':
                    raise ValueError('missing WHERE clause')
                resto = ' '.join(resto)
                if re.search(r' ORDER BY ', resto, flags=re.I):
                    clausa, orden = re.split(r' ORDER BY ', resto, maxsplit=1, flags=re.I)
                else:
                    clausa = resto
                clausa = clausa.strip()
                orden = orden.strip()
                resto = []
            if ' '.join(resto[:2]).upper() == 'ORDER BY':
                orden = ' '.join(resto[2:])
                resto = []
            if resto:
                raise ValueError('malformed query [%r]' % (resto, ))
        print('WHERE', clausa, verbose=2)
        print('ORDER BY', orden, verbose=2)
        print('TO', imprimido, verbose=2)
        # normalize_field_names(desde, seleccion, clausa, orden)
        print('FROM', desde, verbose=2)
        #
        # and get WHERE clause
        #
        donde, constraints = convert_where(clausa)
        if _internal:
            imprimido = ''
        print('WHERE', donde, verbose=2)
        print('ORDER BY', orden, verbose=2)
        print('TO', imprimido, verbose=2)
        print('CONSTRAINTS', constraints, verbose=2)
        #
        # at this point we have the fields, and the table -- get the records
        #
        sq = SimpleQuery(header, aliases=field_alias)
        print('getting records', verbose=2)
        sq.records.extend(self._records(seleccion, field_alias, donde, constraints))
        sq.status = "SELECT %s" % len(sq.records)
        return sq

    def sql_update(self, command):
        """
        Not supported.
        """
        raise NotImplementedError('cannot update records in FIS tables')

class Node(object):
    #
    max_clauses = 1

    def __init__(self):
        self.clauses = []

    def __nonzero__(self):
        if result is None:
            raise ValueError("truthiness of %s has not been determined")
        return result
    __bool__ = __nonzero__

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.clauses)

    @property
    def complete(self):
        return len(self.clauses) == self.max_clauses

    def add(self, clause):
        if len(self.clauses) < self.max_clauses:
            self.clauses.append(clause)
        else:
            raise Exception('too many clauses for %r' % self)

    def process(self, record):
        for i, clause in enumerate(self.clauses, start=1):
            if isinstance(clause, tuple):
                field, op, target = clause
                field = record[field]
                result = self.operators[op](field, target)
            elif isinstance(clause, Node):
                result = clause.process(record)
            if i == 1:
                if type(self) is Node:
                    return result
                elif type(self) is Not:
                    return not result
                elif type(self) is And and result is False:
                    return False
                elif type(self) is Or and result is True:
                    return True
            else:
                # i = 2
                return result
        else:
            return True
    __call__ = process

    @staticmethod
    def _is_not(field, target):
        return field != target
    _not_equal = _is_not

    @staticmethod
    def _is(field, target):
        return field == target
    _equal = _is

    @staticmethod
    def _not_in(field, target):
        return target not in field
    _not_like = _not_in

    @staticmethod
    def _in(field, target):
        if isinstance(target, (tuple, list)):
            return field in target
        else:
            return target in field
    _like = _in

    @staticmethod
    def _ilike(field, target):
        return target.lower() in field.lower()

    @staticmethod
    def _not_ilike(field, target):
        return target.lower() not in field.lower()

    @staticmethod
    def _equals_like(field, target):
        p_count = target.count('%')
        if '%' not in target:
            return field == target
        elif p_count == 1:
            if target[0] == '%':
                return field.endswith(target[1:])
            elif target[-1] == '%':
                return field.startswith(target[:-1])
            else:
                start, end = target.split('%')
                return field.startswith(start) and field.endswith(end)
        elif p_count == 2:
            if '%%' in target:
                target = target.replace('%%','%')
                return field == target
            elif target[0] == target[-1] == '%':
                return target[1:-1] in field
            else:
                raise ValueError('invalid % placement -- %r' % target)
        else:
            # figure out where the string bits are
            pieces = target.split('%')
            new_pieces = []
            last = None
            for p in pieces:
                if p:
                    new_pieces.append(p)
                else:
                    if last != '':
                        new_pieces.append(p)
                    else:
                        # two blanks in a row means a doubled %
                        new_pieces.pop()
                        p = '%'
                        new_pieces.append(p)
                last = p
            # join any segments separated by %-signs
            pieces = new_pieces
            while '%' in pieces:
                index = pieces.index('%')
                if index == 0:
                    pieces[0:2] = ['%' + pieces[1]]
                elif index == len(pieces) - 1:
                    pieces[-2:] = [pieces[-2] + '%']
                else:
                    pieces[index-1:index+2] = [pieces[index-1] + '%' + pieces[index+1]]
            if len(pieces) == 1:
                # containment
                return pieces[0] in field
            elif len(pieces) != 2:
                raise ValueError("too many %%-signs in %r -- use %%%% for literal %%'s" % target)
            minimum = len(pieces[0]) + len(pieces[1])
            if len(field) < minimum:
                return False
            return field.startswith(pieces[0]) and field.endswith(pieces[1])

    @staticmethod
    def _equals_ilike(field, target):
        field = field.lower()
        target = target.lower()
        p_count = target.count('%')
        if '%' not in target:
            return field == target
        elif p_count == 1:
            if target[0] == '%':
                return field.endswith(target[1:])
            elif target[-1] == '%':
                return field.startswith(target[:-1])
            else:
                start, end = target.split('%')
                return field.startswith(start) and field.endswith(end)
        elif p_count == 2:
            if '%%' in target:
                target = target.replace('%%','%')
                return field == target
            elif target[0] == target[-1] == '%':
                return target[1:-1] in field
            else:
                raise ValueError('invalid % placement -- %r' % target)
        else:
            # figure out where the string bits are
            pieces = target.split('%')
            new_pieces = []
            last = None
            for p in pieces:
                if p:
                    new_pieces.append(p)
                else:
                    if last != '':
                        new_pieces.append(p)
                    else:
                        # two blanks in a row means a doubled %
                        new_pieces.pop()
                        p = '%'
                        new_pieces.append(p)
                last = p
            # join any segments separated by %-signs
            pieces = new_pieces
            while '%' in pieces:
                index = pieces.index('%')
                if index == 0:
                    pieces[0:2] = ['%' + pieces[1]]
                elif index == len(pieces) - 1:
                    pieces[-2:] = [pieces[-2] + '%']
                else:
                    pieces[index-1:index+2] = [pieces[index-1] + '%' + pieces[index+1]]
            if len(pieces) == 1:
                # containment
                return pieces[0] in field
            elif len(pieces) != 2:
                raise ValueError("too many %%-signs in %r -- use %%%% for literal %%'s" % target)
            minimum = len(pieces[0]) + len(pieces[1])
            if len(field) < minimum:
                return False
            return field.startswith(pieces[0]) and field.endswith(pieces[1])

    @staticmethod
    def _less_than_or_equal(field, target):
        return field <= target

    @staticmethod
    def _greater_than_or_equal(field, target):
        return field >= target

    @staticmethod
    def _less_than(field, target):
        return field < target

    @staticmethod
    def _greater_than(field, target):
        return field > target

    operators = {
            '=':        _equal.__func__,
            '!=':       _not_equal.__func__,
            '<':        _less_than.__func__,
            '<=':       _less_than_or_equal.__func__,
            '>=':       _greater_than_or_equal.__func__,
            '>':        _greater_than.__func__,
            'is':       _is.__func__,
            'is not':   _is_not.__func__,
            'in':       _in.__func__,
            'not in':   _not_in.__func__,
            'like':     _like.__func__,
            'not like': _not_like.__func__,
            'ilike':    _ilike.__func__,
            'not ilike':_not_ilike.__func__,
            '=like':    _equals_like.__func__,
            '=ilike':   _equals_ilike.__func__,
            }


class And(Node):
    #
    max_clauses = 2
    #
    def evaluate(self):
        if result is None:
            field, op, target = self.clauses[-1]
            field = self.record[field]
            if not operators[op](field, target):
                # if any term is False, the whole thing is False
                self.result = False
            elif len(self.clauses) == self.max_clauses:
                self.result = True


class Or(Node):
    #
    max_clauses = 2
    #
    def evaluate(self):
        if result is None:
            field, op, target = self.clauses[-1]
            field = self.record[field]
            if operators[op](field, target):
                # if any term is False, the whole thing is False
                self.result = True
            elif len(self.clauses) == self.max_clauses:
                self.result = False


class Not(Node):
    #
    max_clauses = 1
    #
    def evaluate(self):
        field, op, target = self.clauses[0]
        field = self.record[field]
        self.result = not operators[op](field, target)


class Join(object):
    def __init__(self, join_type, condition, left_table=None, right_table=None):
        if join_type not in (
                'INNER JOIN', 'OUTER JOIN', 'FULL JOIN',
                'LEFT JOIN', 'RIGHT JOIN',
                'CROSS JOIN',
            ):
            raise ValueError('invalid JOIN type: %r' % (join_type, ))
        self.type = join_type
        self.condition = condition
        self.left_table = left_table
        self.right_table = right_table

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.type, self.condition)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.condition == other.condition

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type != other.type or self.condition != other.condition


    def add_condition(self, condition):
        self.condition += ' ' + condition


class SimpleQuery(object):
    """
    Presents same attributes as openerplib.utils.query.
    """
    def __init__(self, name, fields, aliases=None, record_layout='row'):
        self.fields = fields
        self.aliases = aliases or {}
        self.order = fields[:]
        self.to_file = '-'
        self.records = []
        self.orientation = record_layout
        self.status = None
        self.name = name

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)

    def __repr__(self):
        return "SimpleQuery(name=%r, fields=%r, aliases=%r)" % (
                self.name,
                self.fields,
                self.aliases,
                )


class ResultTable(object):
    def __init__(self, header, fields, aliases, file):
        self.header = []                                                            # fields that are part of the result set
        self.fields = []                                                            # field used only for conditions
        self.rows = []                                                              # the merged data


class TrackingDict(object):
    def __init__(self):
        self.data = {}
    def __eq__(self, other):
        return self.data == other
    def __getattr__(self, name):
        return getattr(self.data, name)
    def __getitem__(self, name):
        return self.data[name]
    def __repr__(self):
        return repr(self.data)
    def __setitem__(self, name, value):
        if '.' in name:
            raise ValueError('ah ha!')
        else:
            setattr(self.data, name, value)

class SQL(object):
    """
    Holds all the bits for an SQL query.

    - tables used
      - fields
      - match conditions
      - use unmatched records?
    - fields used per table
    """
    def __init__(self, statement, debug=False):
        print('__INIT__', verbose=2)
        self.primary_table = None
        self.select = []
        self.tables = {}                                                            # tables used in query
        self.fields = OrderedDict()                                                 # fields used in query
        self.joins = {}
        self.where = ''
        self.orders = []
        self.to = '-'
        self.conditions = []                                                        # how tables are linked together
        self.queries = []
        self.aliases = {}
        self.table_by_field_alias = {}
        self.raw_statement = statement
        self._final_statement = []
        self.words = []
        self.offset = 0
        self.complete = False
        self.command = None
        try:
            self.parse()
            self.q_start()
            if not self.complete:
                raise ValueError('SQL statement incomplete')
            self.process()
        except Exception:
            if debug:
                print_exc()
            else:
                raise

    def __repr__(self):
        return self.statement

    def __str__(self):
        return '\n'.join([
                "Statement: %r" % ' '.join(self._final_statement),
                "Tables:    %r" % self.tables,
                "Fields:    %r" % self.fields,
                "Queries:   %s" % '\n           '.join([repr(q) for q in self.queries]),
                "Joins:     %s" % '\n           '.join([repr(j) for j in self.joins]),
                "TbFA:      %r" % self.table_by_field_alias,
                ])

    @property
    def statement(self):
        return ' '.join(self._final_statement).replace(' , ',', ')

    def execute(self):
        """
        query tables and return result
        """
        print('EXECUTE', verbose=2)
        print('QUERY: %r' % self.queries[0], verbose=2)
        primary = Table.query(self.queries[0])
        if len(self.queries) == 1:
            return primary
        sq = SimpleQuery('/'.join(self.tables.values()), self.select)
        for field in self.select:
            if field in primary.aliases:
                sq.aliases[field] = '%s:%s' % (primary.name, primary.aliases[field])
        joining = []
        for query in self.queries[1:]:
            print('QUERY: %r' % query, verbose=2)
            keys = re.findall(r"%\((\w+)\)s", query)
            values = {}
            for k in keys:
                values[k] = list(set([r[k] for r in primary]))
            secondary = Table.query(query % values)
            joining.append(secondary)
            for field in self.select:
                if field in secondary.aliases:
                    sq.aliases[field] = '%s:%s' % (secondary.name, secondary.aliases[field])
        import pdb; pdb.set_trace()
        return sq

    def parse(self):
        """
        get next "word" in statement
        """
        print('PARSE', verbose=2)
        statement = self.raw_statement
        offset = i = 0
        while True:
            alpha = None
            esc = False
            quote = False
            word = []
            for i, ch in enumerate(statement[offset:]):
                if esc:
                    word.append(ch)
                    esc = False
                    continue
                elif quote:
                    word.append(ch)
                    if ch == SINGLE_QUOTE:
                        quote = False
                        isalpha = False
                    continue
                elif ch in ' ' and not word:
                    continue
                elif ch in ' ' and word:
                    break
                #
                if ch == BACKSLASH:
                    esc = True
                    continue
                elif ch == SINGLE_QUOTE:
                    word.append(ch)
                    quote = True
                    isalpha = True
                    continue
                #
                if word:
                    if alpha and ch.isalnum() or ch in '._':
                        word.append(ch)
                    elif not alpha and not ch.isalnum() and ch not in '._':
                        word.append(ch)
                    else:
                        # switching from/to symbols (e.g. = < +)
                        break
                else:
                    word.append(ch)
                    alpha = ch.isalnum() or ch in '._'
            self.words.append(''.join(word))
            offset += (i + (ch in ' ')) or 1
            if offset + 1 >= len(self.raw_statement):
                break
        print('PARSED: %r' % self.words, verbose=3)

    def process(self):
        print('PROCESS', verbose=2)
        # if single table query, fix up self.fields
        if len(self.tables) == 1:
            try:
                self.fields[self.primary_table] = self.fields.pop(None)
            except:
                raise ValueError(3453, self.tables, self.primary_table, self.fields)
        queries = self.queries
        pt = self.primary_table
        for table, fields in self.fields.items():
            for alias in fields:
                self.table_by_field_alias[alias] = table
        # add primary query
        query = ['SELECT']
        fields = []
        t_name = self.tables[pt]
        for alias, field in self.fields[pt].items():
            if alias == field:
                fields.append(field)
            else:
                fields.append('%s as %s' % (field, alias))
        query.append(', '.join(fields))
        query.append('FROM')
        query.append(t_name)
        # TODO: add WHEREs, skip ORDER BYs
        self.split_wheres()
        if self.where:
            query.append('WHERE')
            query.append(self.where)
        # and the ORDER BY
        if self.orders:
            query.append('ORDER BY')
            query.append(', '.join(self.orders))
        queries.append(' '.join(query))
        # now add any other tables
        for t_alias, t_name in self.tables.items():
            if t_alias == pt:
                continue
            query = ['SELECT']
            fields = []
            for alias, field in self.fields[t_alias].items():
                if alias == field:
                    fields.append(field)
                else:
                    fields.append('%s as %s' % (field, alias))
            query.append(', '.join(fields))
            query.append('FROM')
            query.append(t_name)
            query.append('WHERE')
            # interpret JOIN clause
            join = self.joins[t_alias]
            try:
                field1, op, field2 = join.condition.split()[:3]
            except ValueError:
                raise ValueError('unable to split %r' % (join, ))
            if op != '=':
                raise ValueError('only the equals operator is supported for joins (%r)' % (join, ))
            if '.' in field1:
                table1, field1 = field1.split('.')
            else:
                table1 = self.table_by_field_alias[field1]
            if '.' in field2:
                table2, field2 = field2.split('.')
            else:
                table2 = self.table_by_field_alias[field2]
            if table1 == pt:
                if table2 != t_alias:
                    raise ValueError('JOINing table not listed in JOIN condition (%r)' % (join, ))
                search_field = field2
                found_field = field1
            elif table2 == pt:
                if table1 != t_alias:
                    raise ValueError('JOINing table not listed in JOIN condition (%r)' % (join, ))
                search_field = field1
                found_field = field2
            else:
                raise ValueError('primary table %r not listed in JOIN condition (%r)' % (pt, join))
            query.append('%s in %%(%s)s' % (search_field, found_field))
            queries.append(' '.join(query))

    def split_wheres(self):
        print('split_wheres(): %r' % (self.where, ), verbose=3)
        print('joins: %r' % (self.joins, ), verbose=3)
        print('primary table: %r' % (self.primary_table, ), verbose=3)
        print('tables: %r' % (self.tables, ), verbose=3)
        print('fields: %r' % (self.fields ), verbose=3)
        wheres, conditions = convert_where(self.where, infix=True, strip_quotes=False)
        print('wheres: %r\nconditions: %r' % (wheres, conditions), verbose=3)
        new_where = []
        last_table = None
        last_join = ''
        for clause in wheres:
            if isinstance(clause, basestring) and clause in '|&':
                last_join = clause
                continue
            field, op, cond = clause
            current_table = self.table_by_field_alias[field]
            print('current table: %r' % (current_table, ), verbose=3)
            if last_join == '|':
                # make sure last table and this one are the same
                if last_table != current_table:
                    raise ValueError('WHERE: must use AND between fields from different tables')
            if current_table == self.primary_table:
                if new_where:
                    new_where.append(('or','and')[last_join in '&'])
                new_where.append('%s %s %s' % clause)
            else:
                self.joins[current_table].add_condition(('or ','and ')[last_join in '&'] + '%s %s %s' % clause)
        self.where = ' '.join(new_where)

    def q_from(self, peos):                                                         # possible end of statement?
        print('Q_FROM', verbose=2)
        # valid end state
        # oe tables will have periods in them
        self.complete = False
        tables_acquired = False
        last_table = None
        alias = False                                                               # True=required, None=optional, False=no
        comma_needed = False
        i = 0
        for i, word in enumerate(self.words[self.offset:], start=1):
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            pair = '%s %s' % (word.upper(), next_word)
            if word.upper() in ('JOIN', 'WHERE', 'TO'):
                self._final_statement[-1] = self._final_statement[-1].upper()
                if last_table is not None:
                    self.tables[last_table] = last_table
                    self.primary_table = last_table
                if self._final_statement[-1] == 'JOIN':
                    self._final_statement[-1] = 'INNER JOIN'
                break
            elif pair in ('CROSS JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 'FULL JOIN', 'ORDER BY'):
                word = pair.replace(' ','_')
                self._final_statement[-1] = pair
                i += 1
                if last_table is not None:
                    self.tables[last_table] = last_table
                    self.primary_table = last_table
                break
            if comma_needed and word != COMMA:
                raise ValueError('comma missing between field definitions')
            elif word == COMMA:
                if alias:
                    raise ValueError('missing alias for %r' % last_table)
                raise ValueError('only one table supported in FROM clause')
            elif word.upper() == 'AS':
                self._final_statement.pop()
                alias = True
            elif alias in (None, True):
                self.tables[word] = last_table
                self.primary_table = word
                alias = False
                last_table = None
                comma_needed = True
            else:
                # this is a table
                last_table = word
                alias = None
                tables_acquired = True
        else:
            # loop exhausted, nothing after tables
            self.offset += i
            if last_table is not None:
                self.tables[last_table] = last_table
                self.primary_table = last_table
            # sanity checks
            if alias:
                raise ValueError('missing alias for %r' % last_table)
            if not tables_acquired:
                raise ValueError('no tables in FROM clause')
            if not peos:
                raise ValueError('incomplete SQL statement')
            else:
                self.complete = True
                return
        # sanity checks
        self.offset += i
        if alias:
            raise ValueError('missing alias for %r' % last_table)
        if not tables_acquired:
            raise ValueError('no tables in FROM clause')
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method(peos=True)

    def q_join(self, peos):
        # SELECT Orders.OrderID, Customers.CustomerName, Shippers.ShipperName
        # FROM ((Orders
        # INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID)
        # INNER JOIN Shippers ON Orders.ShipperID = Shippers.ShipperID);
        print('Q_JOIN', verbose=2)
        join_type = self._final_statement[-1]
        self.complete = False
        joins_acquired = False
        try:
            word1, word2, word3 = self.words[self.offset:self.offset+3]
            self._final_statement.append(word1)
        except ValueError:
            raise ValueError('incomplete SQL statement')
        # get table and (possibly) alias
        if word2.upper() == 'AS':
            table = word3
            self.tables[word3] = word1
            self._final_statement.append(word3)
            self.offset += 4
        elif word3.upper() == 'ON':
            table = word2
            self.tables[word2] = word1
            self._final_statement.append(word2)
            self.offset += 3
        else:
            table = word1
            self.tables[word1] = word1
            self.offset += 2
        # double check that ON was the next word
        if self.words[self.offset-1].upper() != 'ON':
            raise ValueError('only JOIN ... ON is currently supported')
        self._final_statement.append('ON')
        # self.offset should now be pointing to the word after ON
        condition = []
        i = 0
        for i, word in enumerate(self.words[self.offset:], start=1):
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            pair = '%s %s' % (word.upper(), next_word)
            if word.upper() in ('WHERE', 'TO', 'JOIN'):
                self._final_statement[-1] = self._final_statement[-1].upper()
                if self._final_statement[-1] == 'JOIN':
                    self._final_statement[-1] = 'INNER JOIN'
                break
            elif pair in ('CROSS JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 'FULL JOIN', 'ORDER BY'):
                word = pair.replace(' ','_')
                self._final_statement[-1] = pair
                i += 1
                break
            # must be part of the condition
            # might it be a field name/alias?
            if word not in (
                    "is not", "is", "not in", "in", "like", "=like", "not like", "ilike", "=ilike", "not ilike",
                    "<=", ">=", "=", "!=", "==?", "<|>",
                ):
                # if word.count('.') == 1:
                #     table, field = word.split('.')
                #     if table in self.tables:
                #         fields_by_alias = self.fields.setdefault(table, {})
                #         for alias, name in fields_by_alias.items():
                #             if field == alias:
                #                 break
                #             elif field == name:
                #                 word = alias
                #                 break
                #         else:
                #             word = field
                #             fields_by_alias[word] = word
                if '.' not in word:
                    # get table name from field name/alias
                    field = word
                    table = self.table_by_field_alias[field]
                else:
                    # get aliased names for both table and field
                    table, field = word.rsplit('.', 1)
                    # if table == 'p':
                    #     raise Exception('word: %r  split: %r   self.fields: %r' % (word, (table, field), self.fields))
                    if table not in self.fields:
                        for table_alias, table_name in self.tables.items():
                            if table == table_name:
                                table = table_alias
                                break
                        else:
                            raise SQLError('table %r not in query' % table)
                    else:
                        join_table = self.fields[table]
                        if field not in join_table:
                            for field_alias, field_name in join_table.items():
                                if field_name == field:
                                    field = field_alias
                                    break
                            else:
                                join_table[field] = field
                    word = '%s.%s' % (table, field)
            condition.append(word)
        else:
            # loop exhausted, no further clauses
            self.offset += i
            # sanity checks
            if not condition:
                raise ValueError('no ON condition in JOIN clause')
            if not peos:
                raise ValueError('incomplete SQL statement')
            else:
                self.joins[table] = Join(join_type, ' '.join(condition))
                self.complete = True
                return
        self.offset += i
        # sanity checks
        if not condition:
            raise ValueError('no ON condition in JOIN clause')
        self.joins[table] = Join(join_type, ' '.join(condition))
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method(peos=True)

    def q_order_by(self, peos):
        print('Q_ORDER_BY', verbose=2)
        self.complete = False
        order_acquired = False
        last_field = None
        order_seen = False
        comma_needed = False
        i = 0
        print(self.words[self.offset:], verbose=2)
        for i, word in enumerate(self.words[self.offset:], start=1):
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            if (
                    word.upper() == 'TO'
                    and next_word not in ('ASC','DESC')
                ):
                self._final_statement[-1] = self._final_statement[-1].upper()
                break
            if comma_needed and word != COMMA:
                raise ValueError('comma missing between order specifications [next word: %r]' % word)
            elif word == COMMA:
                last_field = None
                order_seen = False
                comma_needed = False
            elif last_field is not None and word.upper() in ('ASC', 'DESC'):
                if order_seen:
                    raise ValueError('ASC/DESC can only be specified once per field')
                order_seen = True
                self._final_statement[-1] = self._final_statement[-1].upper()
                self.orders[-1] = '%s %s' % (self.orders[-1], word.upper())
                last_field = None
                comma_needed = True
            elif last_field is not None:
                raise ValueError('comma missing between order specifications [next word: %r]' % word)
            else:
                last_field = word
                self.orders.append(last_field)
                order_acquired = True
        else:
            # loop exhausted, nothing after order
            self.offset += i
            # sanity checks
            if not order_acquired:
                raise ValueError('no ORDER BY fields in clause')
            if not peos:
                raise ValueError('incomplete SQL statement')
            else:
                self.complete = True
                echo('order by:', self.orders)
                return
        self.offset += i
        echo('order by:', self.orders)
        # sanity checks
        if not order_acquired:
            raise ValueError('no ORDER BY fields in clause')
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method(peos=True)

    def q_select(self):
        """
        get and save fields
        """
        # possibilities:
        # - a_field
        # - a_table.a_field
        # - as
        # - comma
        # - star
        print('Q_SELECT', verbose=2)
        self.complete = False
        fields_acquired = False
        last_field = None
        last_table = None
        alias = False
        comma_needed = False
        star_seen = False
        i = 0
        for i, word in enumerate(self.words[self.offset:], start=1):
            print(i, word, verbose=3)
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            if word.upper() == 'FROM':
                print('FROM', verbose=3)
                if last_field is not None:
                    self.fields.setdefault(last_table, OrderedDict())[last_field] = last_field
                    if last_table is None:
                        self.select.append(last_field)
                    else:
                        self.select.append('%s.%s' % (last_table, last_field))
                self._final_statement[-1] = self._final_statement[-1].upper()
                break
            if comma_needed and word != COMMA:
                raise ValueError('comma missing between field definitions')
            elif word == COMMA:
                print('COMMA', verbose=3)
                if alias:
                    raise ValueError('missing alias for %r' % last_field)
                if last_field is not None:
                    self.fields.setdefault(last_table, OrderedDict())[last_field] = last_field
                    if last_table is None:
                        self.select.append(last_field)
                    else:
                        self.select.append('%s.%s' % (last_table, last_field))
                last_field = None
                alias = False
                comma_needed = False
            elif word.upper() == 'AS':
                print('AS', verbose=3)
                self._final_statement.pop()
                alias = True
            elif '.' in word:
                print('PERIOD')
                if alias:
                    raise ValueError('aliases cannot contain periods [%r]' % word)
                table, field = word.rsplit('.', 1)
                self.tables[table] = table
                # self.fields.setdefault(table, OrderedDict())[field] = field
                last_field = field
                last_table = table
                alias = None
                fields_acquired=True
            elif alias in (None, True):
                print('alias is %r' % alias, verbose=3)
                self.fields.setdefault(last_table, OrderedDict())[word] = last_field
                self.select.append(word)
                alias = False
                last_field = None
                last_table = None
                comma_needed = True
            else:
                print('saving field name %r' % word, verbose=3)
                assert last_table is None
                if last_field is not None:
                    self.fields.setdefault(last_table, OrderedDict())[word] = word
                last_field = word
                last_table = None
                alias = None
                fields_acquired=True
        else:
            # `FROM` not found
            raise ValueError('missing FROM')
        self.offset += i
        # sanity checks
        if alias:
            raise ValueError('missing alias for %r' % last_field)
        if not fields_acquired:
            raise ValueError('no fields specified')
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method(peos=True)

    def q_start(self):
        print('Q_START', verbose=2)
        word = self.words[0]
        self.offset = 1
        if word.upper() not in (
                'COUNT', 'DELETE', 'DESCRIBE', 'DIFF', 'INSERT', 'SELECT', 'UPDATE',
            ):
            raise ValueError('unknown command: %r' % word)
        self.command = word.upper()
        self._final_statement.append(word.upper())
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method()

    def q_to(self, peos):
        print('Q_TO', verbose=2)
        word = self.words[self.offset:self.offset+1]
        if not word:
            raise ValueError('no TO destination')
        word = word[0]
        self._final_statement.append(word)
        self.to = word
        self.offset += 1
        word = self.words[self.offset:self.offset+1]
        if word:
            raise ValueError('extra TO parameters')
        self.complete = True
        return

    def q_where(self, peos):
        print('Q_WHERE', verbose=2)
        self.complete = False
        wheres_acquired = False
        condition = []
        i = 0
        for i, word in enumerate(self.words[self.offset:], start=1):
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            pair = '%s %s' % (word.upper(), next_word)
            if word.upper() == 'TO':
                self._final_statement[-1] = self._final_statement[-1].upper()
                break
            elif pair == 'ORDER BY':
                word = pair.replace(' ','_')
                self._final_statement[-1] = pair
                i += 1
                break
            # must be part of the condition
            condition.append(word)
        else:
            # loop exhausted, no further clauses
            self.offset += i
            # sanity checks
            if not condition:
                raise ValueError('no WHERE condition')
            if not peos:
                raise ValueError('incomplete SQL statement')
            else:
                self.where = ' '.join(condition)
                self.complete = True
                return
        self.offset += i
        # sanity checks
        if not condition:
            raise ValueError('no WHERE condition')
        self.where = ' '.join(condition)
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method(peos=True)

class SQLTable(object):
    def __init__(self, statement):
        self.name = ''                                                              # plain text name
        self.model = ''                                                             # oelib model or fis table
        self.fields = []                                                            # fields to fetch
        self.aliases = {}                                                           # field aliases
        self.conditions = []                                                        # record filters
        tokens = tokenize(statement)
        if not tokens:
            raise ValueError('nothing to process')
        # get command to process
        token = tokens.pop(0)
        if token not in (COUNT, DELETE, DESCRIBE, DIFF, INSERT, SELECT, UPDATE):
            raise ValueError('unknown command: %r' % token)

    def select(self):
        pass

## tokenizer

class Token(object):

    def __init__(self, name, payload=None):
        self.name = name
        self.payload = payload

    def __repr__(self):
        if self.payload is not None:
            return "Token(%r, payload=%r)" % (self.name, self.payload)
        else:
            return "Token(%r)" % self.name

    def __str__(self):
        if self.payload is not None:
            return "%s(%r)" % (self.name, self.payload)
        else:
            return self.name
        

for name in (
            'COUNT', 'DELETE', 'DESCRIBE', 'DIFF', 'INSERT', 'SELECT', 'UPDATE',
            'AS', 'FROM', 'JOIN', 'ON', 'WHERE', 'ORDER BY', 'ASC', 'DESC', 'TO'
            'INTO', 'VALUES', 'SET',
            ):
    module[name] = Token(name)



class Parser(object):
    pass

class Word(Parser):
    pass

#
# class NoValue(Enum):
#
#     def __repr__(self):
#         return '<%s.%s>' % (self.__class__.__name__, self.name)
#
#
# class Node(object):
#     "base object"
#
#     parent = None
#     children = []
#
#
# class Select(Node):
#     fields = []
#
#
# class From(Node):
#     table = None
#
#
# class Where(Node):
#     criteria = None
#
#
# class OrderBy(Node):
#     fields = None
#
#
# class ParseState(NoValue):
#     SELECT = auto()
#     FROM = auto()
#     WHERE = auto()
#     ORDER_BY = auto()
#
#     # def __init__(self, value):
#     #     if len(self.__class__):
#     #         # make links
#     #         all = list(self.__class__)
#     #         first, previous = all[0], all[-1]
#     #         first.beats = self
#     #         self.beats = previous
#
#
#
# def parse_sql(command):
#     # get rid of leading/trailing whitespace
#     command = command.strip()
#     # state = ParseState.SELECT
#     words = []
#     while command:
#         word, command = next_word(command)
#         words.append(word)
#     print(words)
#
# whitespace = ' \t\n'
#
# def next_word(command):
#     "a word either has no spaces, or is surrounded by single quotes"
#     print(command)
#     word = []
#     quoted = False
#     escape = False
#     end = False
#     for i, ch in enumerate(command):
#         if end and ch not in whitespace:
#             raise ValueError('run-on word after quote')
#         if escape:
#             if ch not in "'\\":
#                 raise ValueError("only ' and \\ can be escaped")
#             word.append(ch)
#             escape = False
#             continue
#         if ch in whitespace:
#             break
#         if ch == '\\':
#             escape = True
#             continue
#         if ch == "'":
#             if quoted:
#                 # end of word
#                 end = True
#                 word.append(ch)
#                 continue
#             if word:
#                 # embedded not allowed without escaping
#                 print(repr(word))
#                 raise ValueError('embedded quotes must be escaped')
#             word.append(ch)
#             quoted = True
#             continue
#         word.append(ch)
#     command = command[i+1:].lstrip()
#     return ''.join(word), command

Run()
