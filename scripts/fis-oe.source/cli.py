"""
Pseudo-SQL system to interogate FIS and OpenERP.
"""
from __future__ import print_function, unicode_literals

from antipathy import Path
from ast import literal_eval
from collections import defaultdict
from enhlib.text import translator
from enhlib.misc import baseinteger, basestring
from fislib import schema as fis_schema
from fislib.schema import F135
from fis_oe.sql import ALL_ACTIVE, Fault, FISTable, SQL, SQLError, Table, convert_name, ensure_fis, init_fis
from fis_oe import sql as sequel
from openerplib import get_connection, get_records, AttrDict, Query, MissingTable
import threading
from traceback import format_exception

import dbf
import io
import os
import re
import shutil
import socket
import sys
import time

from scription import *


virtual_env = os.environ.get('VIRTUAL_ENV', '/opt/openerp')
PRODUCT_FORECAST = Path('/FIS/data/product_forecast.txt')
oe = None

## Globals

SHOW_ID = False

__version__ = "0.9"

## API

@Script(
        hostname=Spec('host to connect to', OPTION, ('host',)),
        database=Spec('database to query', OPTION, ('db', )),
        show_ids=Spec('show record/field ids', FLAG, None),
        fis_location=Spec('which files to use for FIS queries', OPTION, None, choices=['local','remote']),
        )
def main(hostname, database, show_ids, fis_location):
    # determine which mode to operate in:
    # - local FIS files available?
    # - OpenERP URL responsive?
    #
    # first, get config file(s) from
    # - $virtual_env/config
    # - /etc/openerp
    #
    global oe, SHOW_ID, LOCAL_FIS, config, fd, TableError
    SHOW_ID = show_ids
    config = Path('%s/config/fnx.ini' % virtual_env)
    if config.exists():
        config = OrmFile(config, types={'_path':Path})
    else:
        abort('unable to find config file')
    sections = [s[0] for s in config]
    if 'openerp' in sections:
        try:
            oe = get_connection(
                    hostname=hostname or config.openerp.host,
                    database=database or config.openerp.db,
                    login=config.openerp.user,
                    password=config.openerp.pw,
                    )
        except socket.error:
            pass
    LOCAL_FIS = False
    if 'fis_imports' in sections:
        if fis_location != 'remote':
            LOCAL_FIS = True
    sequel.init_fis()
    sequel.oe = oe
    sequel.script_verbosity = script_verbosity
    sequel.SHOW_ID = SHOW_ID
    sequel.ensure_oe = ensure_oe
    from fis_oe.sql import fd, TableError

@Command(
        command=('sql command', REQUIRED),
        separator=('insert blank line between records', FLAG),
        wrap=Spec('field name and width of fields to wrap [ignored in .xls and .csv output]', MULTI),
        quiet=Spec('do not display output', FLAG),
        legacy=Spec('use use original code', FLAG),
        sheet=Spec('sheet name if writing excel file', OPTION, None),
        )
@Alias('fis-oe','fis-oe2','fis-oe3')
def sql(command, separator, wrap, quiet, legacy, sheet):
    """
     Query FIS/OpenERP databases.

    SELECT field_name [, field_name [, ...]]
        FROM table
        [JOIN table ON ...]
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
        [JOIN ...]
        [WHERE ...]
        [ORDER BY ...]

    REPORT report-name
        [FROM table]
        [WHERE ...]
        [TO file]
    """
    if quiet:
        global script_verbosity
        script_verbosity = -1
    if isinstance(wrap, tuple):
        wrap = dict([
            (k, int(v))
            for item in wrap
            for k, v in (item.split(':'), )
            ])
    command = command.strip(' ;')
    try:
        # get a query object, which has a `records` attribute with all matches
        if legacy or not command.upper().startswith('SELECT '):
            query = Table.query(command)
        else:
            sql = SQL(command)
            query = sql.execute()
        print('q --> %s' % (query, ), verbose=2)
    except SQLError as e:
        help(str(e))
    except NotImplementedError as e:
        abort(str(e))
    if query is not None:
        print(sheet or command)
        model_name = sheet or command
        to_file = query.to_file
        fields = query.fields
        query = query
        if to_file:
            if to_file.endswith('.xls'):
                sequel.write_xls(model_name, query, fields, to_file, separator)
            elif to_file.endswith('.csv'):
                sequel.write_csv(model_name, query, fields, to_file, separator)
            elif to_file.endswith('.txt') or to_file == '-':
                for field, length in wrap.items():
                    pass
                sequel.write_txt(model_name, query, fields, to_file, separator, wrap)
            else:
                abort('unknown file type: %r' % to_file)
        echo(query.status)

@Command(
        ip=Spec('address to serve on', REQUIRED),
        port=Spec('port to serve on', OPTION, type=int),
        log_file=Spec('name of file to log to [default: stderr]', OPTION),
        )
def serve(ip, port, log_file):
    """
    Run an FIS SQL server on PORT with logging to LOG-FILE
    """
    try:
        from SocketServer import ThreadingTCPServer, TCPServer, StreamRequestHandler
    except ImportError:
        from socketserver import ThreadingTCPServer, TCPServer, StreamRequestHandler

    class FISSQLServer(ThreadingTCPServer):
        #
        allow_reuse_address = 1
        is_empty_log = False
        log_name = None
        log_file = None
        log_lock = threading.Lock()
        #
        def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, log_file=None, msg_location=None):
            self.msg_location = msg_location or os.getcwd()
            self.log_name = log_file
            self.prep_log_file()
            self.today = time.localtime(time.time())[:3]
            TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        #
        def emit_message(self, msg, timestamp):
            with self.log_lock:
                if isinstance(msg, bytes):
                    msg = msg.decode('utf-8')
                if self.log_file is None:
                    stderr.write(msg)
                else:
                    # time to rotate the file?
                    now = time.localtime(timestamp)[:3]
                    if not self.is_empty_log and self.today != now:
                        self.log_file.close()
                        new_name = '%s.%04d%02d%02d' % ((self.log_name, ) + self.today)
                        dirs, filename = os.path.split(self.log_name)
                        shutil.move(self.log_name, os.path.join(dirs, new_name))
                        self.log_file = io.open(self.log_name, 'a', encoding='utf-8')
                        self.today = now
                    self.log_file.write(msg)
                    self.log_file.flush()
        #
        def handle_error(self, request, client_address):
            timestamp = time.time()
            cls, exc, tb = sys.exc_info()
            frames = format_exception(cls, exc, tb)
            keep = False
            lines = []
            for f in frames:
                if keep or 'pulse.pyz' in f:
                    keep = True
                    lines.append(f)
            if self.log_file is not None:
                error(''.join(lines).strip(), border='box')
            lines.insert(0, '-'*50+'\n')
            lines.append('-'*50+'\n')
            self.emit_message(''.join(lines).strip()+'\n', timestamp)
        #
        def prep_log_file(self):
            if self.log_name is None:
                return
            dirs, filename = os.path.split(self.log_name)
            if not os.path.exists(dirs):
                os.path.mkdirs(dirs)
            if not os.path.exists(self.log_name):
                self.is_empty_log = True
            self.log_file = io.open(self.log_name, 'a', encoding='utf-8')
        #
        def server_bind(self):
            """Override server_bind to store the server name."""
            TCPServer.server_bind(self)
            host, port = self.socket.getsockname()[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port

    class FISSQLRequestHandler(StreamRequestHandler):
        """
        FIS SQL request handler.
        """
        server_version = "FISSQL/" + __version__
        protocol_version = 'CSV/1.0'
        #
        def handle(self):
            command = self.rfile.read()
            echo(command)
            self.wfile.write(command + '\n')
        #
        def log_message(self, format, *args):
            """
            Log an arbitrary message.
            """
            timestamp = time.time()
            message = "%s - - [%s] %s\n" % (
                    self.client_address[0],
                    self.log_date_time_string(timestamp),
                    format % args)
            self.server.emit_message(message, timestamp)
        #
        def log_date_time_string(self, timestamp=None):
            """
            Return the current time formatted for logging.
            """
            if timestamp is None:
                timestamp = time.time()
            year, month, day, hh, mm, ss, x, y, z = time.localtime(timestamp)
            s = "%02d/%3s/%04d %02d:%02d:%02d" % (
                    day, self.monthname[month], year, hh, mm, ss)
            return s

    ensure_fis()
    fissql = FISSQLServer(
            (ip, port),
            FISSQLRequestHandler,
            log_file=log_file,
            )
    sa = fissql.socket.getsockname()
    echo("Serving FIS SQL on", sa[0], "port", sa[1], "...")
    fissql.serve_forever()

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
    existing_ids = dict([
            (r.res_id, r.name)
            for r in existing_imd.records
            ])
    existing_names = dict([
            (r.name, r)
            for r in existing_imd.records
            ])
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
        model_records = dict([
                (r.id, r)
                for r in get_records(oe, model, ids=ids, fields=fields)
                ])
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

@Command(
        populate=Spec("update product's Related Products field", FLAG),
        clear=Spec("remove Related Products entries", FLAG),
        )
def related_products(populate, clear):
    """
    update product's Related Products field
    """
    related = {}
    cleared = populated = 0
    product = oe.get_model('product.product')
    if clear:
        for item in Table.query("select id, name, fis_related_product_ids from product.product where xml_id != ''"):
            if item.fis_related_product_ids:
                product.write(
                        [item.id],
                        {'fis_related_product_ids': [(5,ri.id) for ri in item.fis_related_product_ids]},
                        context={'related product loop':True},
                        )
                cleared += 1

    if populate:
        for item in Table.query("select id, name, fis_related_product_ids from product.product where xml_id != ''"):
            print(item, verbose=2)
            related.setdefault(item.name, set()).add(item)
        for name, items in related.items():
            if len(items) < 2:
                continue
            for item in items:
                ids = [i.id for i in items if i.id != item.id and i.id not in item.fis_related_product_ids]
                product.write(
                        [item.id],
                        {'fis_related_product_ids': [(4,i) for i in ids]},
                        context={'related product loop':True},
                        )
                populated += 1
    print('cleared:   %5d\npopulated: %5d' % (cleared, populated))


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
        files = [k for k in fd.tables if isinstance(k, baseinteger)]
    for filenum in files:
        print('file: %s' % (filenum,), end=' ', verbose=0)
        try:
            table = fd.fisData(filenum)
        except TableError as exc:
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
            match = re.match(r'(.{40})  \((\d{6})\)  (.*)$', line)
            if match:
                fis_desc, item_code, full_desc = match.groups()
                if fis_desc in items:
                    echo('%s:  %s' % (item_code, full_desc))
    if update:
        abort('update not currently supported')
        print('updating -all- cross-reference codes')
        cross_ref = oe.get_model('fis_integration.customer_product_cross_reference')
        current_items = dict([
                (r.fis_code, r.id)
                for r in get_records(
                    cross_ref,
                    domain=[('list_code','=','-all-')],
                    )])
        print('  %d existing items' % len(current_items))
        #
        # TODO
        # method of getting saleable items has changed -- this section needs to move
        # to another function
        #
        # get saleable items from OpenERP
        saleable_items = dict([
                (r.xml_id, r.id)
                for r in get_records(
                    'product.product',
                    domain=[('sale_ok','=',True),('active','=',True),('fis_availability_code','=','Y')],
                    fields=['id','xml_id'],
                    )])
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
        show_raw=Spec('show raw record', FLAG, None),
        )
def records(filenum, template, code, fields, dbf_name, tabular, regex, test, check_old, table, show_raw):
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
        filenum, table_name, template = sequel.table_keys.get(filenum, (None, None, None))
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
        print('using subset %r and file %r' % (template, fis_table.filename))
        records = [v for k, v in fis_table.get_subset(code)]
    if test:
        try:
            enum = getattr(fis_schema, 'F%d' % fis_table.number)
        except AttributeError:
            abort('Table %r has no file number, unable to generate test output' % fis_table.filename)
    print('found %d records' % (len(records), ))
    used_fields = []
    table_names = []
    if records:
        # get field defs now, may be needed for dbf creation
        record = records[0]
        print('widths:', record._widths, verbose=2)
        max_value_width = max(record._widths)
        # max_data_width = record._width
        field_widths = []
        dbf_types = []
        dbf_names = []
        if fields:
            fis_fields = [(i-1, record.fieldlist[i-1]) for i in fields]
        else:
            fis_fields = list(enumerate(record.fieldlist))
        for i, row in fis_fields:
            name, spec = row[1:4:2]
            if not name.strip() or name.strip().lower() == '(open)':
                continue
            table_names.append(name)
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
            lines = format_record(record, fields, max_value_width)
            if test:
                for i, datum in zip(fields, field_data):
                    echo('%s: %s,' % (enum[i-1], repr(datum).strip('u')))
            elif not dbf_name and not tabular and not show_table and not test and lines:
                if show_raw:
                    echo(record.rec, '\n')
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
    keys = [k for k in fd.tables.keys() if isinstance(k, baseinteger)]
    # template = '%4d: %s%s'
    numerical = True
    if len(keys) < 10:
        # go with alpha table names
        keys = [k for k in fd.tables.keys() if not isinstance(k, baseinteger)]
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


@Command(
        tests=Spec('tests to run [default: all]', nargs='*'),
        )
def self_test(*tests):
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
    from fis_oe import test
    import unittest
    test
    unittest.main(module='fis_oe.test', exit=True)


## helpers

alnum = translator(keep='abcdefghijklmnopqrstuvwxyz0123456789')
alnum_space = translator(to=' ', keep='abcdefghijklmnopqrstuvwxyz0123456789 ')

imd_methods = {
        'id': lambda rec,_: '%05d' % (rec.id, ),
        'tag': lambda rec,field: alnum(rec[field].lower()),
        'name': lambda rec,field: ''.join(w[0] for w in alnum_space(rec[field].lower())),
        }

def ensure_oe():
    """
    abort if OpenERP is unavailable
    """
    if oe is None:
        abort('OpenERP is not running; only FIS functions/tables available.')

def format_record(record, fields=None, max_width=None):
    # record: the fis record to format
    # fields: list of ints, or list of (int, record)s
    lines = []
    name_width = 11
    value_width = max_width or 40
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


