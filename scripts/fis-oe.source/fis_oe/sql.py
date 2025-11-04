from __future__ import print_function, unicode_literals

from aenum import Enum, NamedTuple, auto
from antipathy import Path
from ast import literal_eval
from collections import OrderedDict
from enhlib.itertools import all_equal
from enhlib.misc import basestring, str, zip
from fislib.BBxXlate.schema import table_keys
from fislib.utils import fix_date
from itertools import cycle
from openerplib import get_connection, get_records, AttrDict, Binary, Query, Many2One, CSV
from scription import OrmFile, Singleton, Var, echo, error, print
from traceback import print_exc

import dbf
import os
import pprint
import re
import socket

try:
    from xmlrpclib import Fault
except ImportError:
    from xmlrpc.client import Fault

## globals

fd = TableError = None
virtual_env = Path(os.environ.get('VIRTUAL_ENV', '/opt/openerp'))

def init_fis():
    global fd, TableError
    try:
        from fislib.BBxXlate import fisData as fd
        from fislib.BBxXlate.bbxfile import TableError
        fd.init()
    except IOError as e:
        error(e)
        fd = TableError = None

class PlainEnum(Enum):
    def __repr__(self):
        return self.name


# class BytesEnum(bytes, PlainEnum):
#     pass
#

class Char(str, PlainEnum):
    _order_ = 'SINGLE_QUOTE COMMA BACKSLASH LPAREN RPAREN'
    SINGLE_QUOTE = "'"
    COMMA = ","
    BACKSLASH = "\\"
    LPAREN = '('
    RPAREN = ')'
SINGLE_QUOTE, COMMA, BACKSLASH, LPAREN, RPAREN = Char


class SQLState(PlainEnum):
    _order_ = 'START SELECT FROM JOIN ON WHERE ORDER_BY TO'
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


class Clause(PlainEnum):
    _order_ = 'FIELD OP CONSTANT CONJUNCTION'
    FIELD = auto()
    OP = auto()
    CONSTANT = auto()
    CONJUNCTION = auto()
FIELD, OP, CONSTANT, CONJUNCTION = Clause

@Singleton
class EMPTY(object):
    def __repr__(self):
        return 'EMPTY'
    def __str__(self):
        return ''
    def __bool__(self):
        return False
    __nonzero__ = __bool__
    def __add__(self, other):
        return other
    __radd__ = __add__

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

oe = script_verbosity = SHOW_ID = None

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

## functions

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
    if not name:
        return name
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
    if name.endswith('%'):
        if name[-2:-1] == ' ':
            name = name[:-1] + 'percent'
        else:
            name = name[:-1] + '_percent'
    elif name.startswith('%'):
        if name[1:2] == ' ':
            name = 'percent' % name[1:]
        else:
            name = 'percent_' % name[1:]
    elif '%' in name:
        name = name.replace('%', 'percent')
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
            suffix = '_%s' % suffix
            if name[-1].isdigit():
                name = name[:-1]
            if name[-1] == '_':
                name = name[:-1]
            name += suffix
    else:
        # name still taken
        raise Exception(
                'unable to convert %r (final attempt: %r)\nexisting names: %r'
                % (original_name, name, ', '.join(existing_names)
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
        print('set', clausa, verbose=4)
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
            print('\nfield: %r\nop: %r\nvalue: %r\nclausa: %r\n' % (field, op, value, clausa), verbose=3)
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

def convert_where(clausa, alias=None, infix=False, strip_quotes=True, null=False):
    """
    Converts the WHERE clause of an SQL command.
    """
    def subquery(match):
        print('subquery:', match, verbose=3)
        command = match.group()[1:-1]
        print(command, verbose=3)
        if not command.upper().startswith(('SELECT ','COUNT ')):
            raise ValueError('subquery must be SELECT or COUNT')
        if command.upper().startswith('COUNT '):
            return str(Table.query(command, separator=False))
        else:  # SELECT
            result = Table.query(command, separator=False, wrap=(), _internal='subquery')
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
    print('subquery: %r,  clausa: %r' % (subquery, clausa), verbose=3)
    clausa = re.sub(r"\(.*\)", subquery, clausa)
    print('after subquery: %r' % (clausa, ), verbose=3)

    std_match = Var(lambda clausa: re.match(
            r"^(\S+)\s*(<=|>=|!=|=|<|>|\bis\s+not\b\b|\bis\b|\bnot\s+in\b|\bin\b|\blike\b|\b=like\b|\bnot\s+like\b|\bilike\b|\b=ilike\b|\bnot\s+ilike\b)\s*('(?:[^'\\]|\\.)*?'|\[[^]]*\]|\S*)\s*(.*?)\s*$",
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
        print('clausa: %r' % (clausa, ), verbose=4)
        if std_match(clausa):
            field, op, condition, clausa = std_match().groups()
            print('\nfield: %r\nop: %r\ncond: %r\nwhere: %r\n' % (field, op, condition, clausa), verbose=4)
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
                op, condition = '=', null
            elif (lop, lcond) == ('is not', 'null'):
                op, condition = '!=', null
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
            print('\nfunction: %r\nfield: %r\nop: %r\ncond: %r\nwhere: %r\n' % (function, field, op, condition, clausa), verbose=4)
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

def create_filter(domain, aliased=None):
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
    if aliased is None:
        aliased = {}
    print('domain:', domain, verbose=3)
    for clause in domain:
        # print('  stack:', stack, verbose=4)
        # print('  clause:', clause, verbose=4)
        current_node = stack[-1]
        if isinstance(clause, tuple) and len(clause) == 3:
            field, op, target = clause
            field = aliased.get(field, field)
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

def ensure_fis():
    """
    abort if FIS files missing
    """
    if fd is None:
        init_fis()
        if fd is None:
            # no files
            raise RuntimeError('FIS files not available')


def ensure_oe():
    """
    abort if OpenERP is unavailable
    """
    global oe
    if oe is None:
        if virtual_env.exists('config/fnx.ini'):
            config = OrmFile(virtual_env/'config/fnx.ini', types={'_path':Path})
        else:
            # assume being called outside of cli; look in /etc for the config
            config = OrmFile('/etc/fnx.ini', types={'_path':Path})
        try:
            oe = get_connection(
                    hostname=config.openerp.host,
                    database=config.openerp.db,
                    login=config.openerp.user,
                    password=config.openerp.pw,
                    )
        except socket.error:
            raise RuntimeError('OpenERP not accessible')

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
        print('ExpandedRow.__init__: fields ->', fields, '  record ->', record, verbose=5)
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
            print('checking %s -> %r' % (k, v), verbose=5)
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
                print('adding subrow', sub_row, verbose=5)
                row.append(sub_row)
            elif k in fields:
                # must go after subfield checking
                print('  adding element ->', k, verbose=5)
                row.append(v)
            print('intermediate row ->', row, verbose=5)
        print('final row ->', row, verbose=5)
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
            print('processed row ->', line, verbose=5)
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

def is_keyword(word):
    return word in ('null', 'false', 'true')

def is_numeric(word):
    try:
        float(word)
        return True
    except ValueError:
        return False

def is_quoted(word):
    return len(word) > 1 and word[0] == word[-1] == SINGLE_QUOTE

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
            print('adding: %r' % (field_name, ), verbose=3)
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
        print(r, verbose=4)
        if separator:
            i += 1
        er = ExpandedRow(fields, r)
        for row in er:
            i += 1
            ci_bump = 0
            for cell_index, cell_value in enumerate(row):
                if isinstance(cell_value, Many2One):
                    cell_value = str(cell_value)
                    # print('skipping m2o', cell_value, verbose=5)
                elif isinstance(cell_value, (list, tuple)):
                    print('cell_value ->', cell_value, verbose=5)
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
    print('field count:', len(fields), fields, verbose=4)
    for field_name in fields:
        line.append(field_name)
    print(repr(line), verbose=5)
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
                    # print('skipping m2o', cell_value, verbose=5)
                elif isinstance(cell_value, (list, tuple)):
                    print('cell_value [sequence] ->', cell_value, verbose=5)
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
                    print('cell_value [basestring] ->', cell_value, verbose=5)
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
    print('\n'.join([repr(l) for l in lines]), verbose=5)
    with open(file, 'wb') as output:
        output.write('\n'.join(lines).encode('utf8'))

def write_txt(table, query, fields, file, separator=False, wrap=None,):
    lines = []
    line = []
    print('field count:', len(fields), fields, verbose=5)
    for field_name in fields:
        field_header = field_name.upper()
        aliased = getattr(query, 'aliases', {})
        if script_verbosity:
            field_header += "\n%s" % aliased.get(field_name, field_name)
        line.append(field_header)
        # line.append('%s\n%s' % (query.names[field_name] or field_name.upper(), field_name))
    lines.append(line)
    #
    for r in query.records:
        if separator:
            lines.append(None)
        print(r, verbose=5)
        er = ExpandedRow(fields, r)
        [print(r, verbose=5) for r in er]
        for row in er:
            print('post pre-process row ->', row, verbose=5)
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
            print('post post-process line ->', line, verbose=5)
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
    FIS, OpenERP, or Generic table.

    Subclasses must also provide the following attributes:
    - fields
    """
    _inited = False
    tables = {}
    command_table_pat = r"(COUNT\s*FROM|DELETE\s*FROM|DESCRIBE|DIFF .*? FROM|REPORT .*? FROM|SELECT .*? FROM|INSERT INTO|UPDATE)\s*(\S*)"

    def __new__(cls, table_name):
        """
        Select FISTable, OpenERPTable, or Generic depending on table_name.
        """
        if table_name not in cls.tables:
            if '.' in table_name:
                # table = super(Table, OpenERPTable).__new__(OpenERPTable, table_name)
                 table = OpenERPTable.__new__(OpenERPTable, table_name)
            else:
                # table = super(Table, FISTable).__new__(FISTable, table_name)
                table = FISTable.__new__(FISTable, table_name)
            cls.tables[table_name] = table
        return cls.tables[table_name]

    def __getattr__(self, name):
        """
        Mirror any attributes on a contained table
        """
        return getattr(self.table, name)

    def __iter__(self):
        for row in self.table:
            yield row

    @property
    def fields(self):
        """
        Names/definitions of the table's fields.
        """
        return self._fields.copy()

    @classmethod
    def from_data(cls, name, fields=None, types=None, data=None):
        print('name: %r  fields: %r  data: %r' % (name, fields, data), verbose=4)
        if isinstance(data, (str, Path)) and data.endswith('.dbf'):
            print(0, verbose=4)
            data = dbf.Table(data, default_data_types='enhanced').open(dbf.READ_ONLY)
            fields = dict([(k, k) for k in data.field_names])
            print('fields: %r' % (fields, ), verbose=4)
            table = object.__new__(DbfTable)
        else:
            print(1, verbose=4)
            if name in cls.tables:
                raise NameError('table %r already exists' % name)
            # if rows in data are simple tuples, header must be specified
            # otherwise, rows must be namedtuples, attrdicts, or something else supporting getitem access
            if fields is None:
                if data is None:
                    raise ValueError('fields must be given when table is empty')
                fields = list(data.keys())
            if isinstance(fields, (list, tuple)):
                fields = OrderedDict([(k, k) for k in fields])
            if data and type(data[0]) is tuple:
                old_data, data = data, []
                for row in old_data:
                    data.append(dict(zip(fields, row)))
            table = object.__new__(GenericTable)
        if types is None and data:
            types = OrderedDict.fromkeys(fields.keys(), str)
            undef = set(fields.keys())
            for rec in data:
                for f in list(undef):
                    if rec[f] is not None:
                        types[f] = type(rec[f]).__name__
                        undef.remove(f)
                if not undef:
                    break
            for f in undef:
                # use dummy value for missing types
                types[f] = ''
        table.name = name
        table._fields = fields
        table.table = data
        table.types = types
        cls.tables[name] = table
        return table

    @classmethod
    def query(cls, command):
        """
        Extract command and primary table, then call cls.sql_* to process.
        """
        try:
            cmd, table_name = re.match(cls.command_table_pat, command, re.I).groups()
        except AttributeError:
            raise SQLError('command and/or table missing from query')
        print('%r  %r' % (cmd, table_name), verbose=3)
        table = cls(table_name)
        print(repr(table), verbose=5)
        method = getattr(table, 'sql_%s' % cmd.lower().split()[0])
        q = method(command)
        if not isinstance(q, (Query, SimpleQuery)):
            raise TypeError('%r did not return a (Simple)Query, but a %r' % (method.__name__, type(q).__name__))
        return q

    def sql_count(self, command):
        raise SQLError('cannot count records')

    def sql_delete(self, command):
        raise NotImplementedError('cannot delete records')

    def sql_describe(self, command):
        raise SQLError('cannot describe table')

    def sql_diff(self, command):
        raise SQLError('cannot diff records')

    def sql_insert(self, command):
        raise SQLError('cannot insert records')

    def sql_select(self, command):
        raise SQLError('cannot select records')

    def sql_update(self, command):
        raise NotImplementedError('cannot update records')

class FISTable(Table):
    """
    Handle interactions with FIS table.
    """
    def __new__(cls, table_name):
        print('looking for FIS table %r' % table_name, verbose=2)
        # if self._inited:
        #     return
        # self._inited = True
        ensure_fis()
        self = object.__new__(FISTable)
        if table_name.isdigit():
            table = int(table_name)
            source_name = 'filenum'
        else:
            table = table_name.lower()
            source_name = 'name'
        if table in table_keys:
            self.num, self.name, self.pat = table_keys[table]
        else:
            if table not in fd.tables:
                for desc in fd.tables.values():
                    if table == maybe_lower(desc[source_name]):
                        table = desc['filenum'] or desc['name']
                        break
                else:
                    raise SQLError('table %r not found' % table_name)
            table = fd.tables[table]
            self.num = table['filenum']
            self.name = table['name']
            self.pat = ''
            # count = 0
            # for _, _, _, spec, _ in table['fields']:
            #     if spec.startswith('An$'):
            #         count += int(spec.split(',')[1].strip(')'))
            # self.pat = '.' * count
        self.table = fd.fisData(self.num or self.name)
        print('   found %s with %d records using pattern %r'
                % (self.table.filename, len(self.table), self.pat),
                verbose=2,
                )
        # get human-usable field names
        fields_by_name = {}
        fields_by_number = {}
        fields_and_alias = {}
        for i, field in enumerate(self.table.fieldlist, start=1):
            name, spec = field[1:4:2]
            comment = name
            name = convert_name(name, 50, fields_by_name)
            fields_by_name[name] = i, name, spec, comment
            fields_by_number[i] = i, name, spec, comment
            fields_and_alias[name] = spec
            fields_and_alias[str(i)] = spec
        self._fields_by_name = fields_by_name
        self._fields_by_number = fields_by_number
        self._fields_and_alias = fields_and_alias
        return self

    @property
    def fields(self):
        return self._fields_by_name.copy()

    @property
    def fields_and_alias(self):
        return self._fields_and_alias.copy()

    @property
    def fields_by_number(self):
        return self._fields_by_number.copy()

    def _records(self, fields, aliased, where, constraints):
        filter = create_filter(where, aliased)
        records = []
        for k, v in self.table.items():
            if filter(v):
                if all(c(v) for c in constraints):
                    row = []
                    for f in fields:
                        if f == 'id' and 'id' not in aliased:
                            continue
                        row.append(v[aliased[f]])
                    records.append(dict(zip(fields, row)))
        return records

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
                raise SQLError('unknown ORDER BY: %r' % order)
        defs = sorted(self._fields_by_number.values(), key=lambda t: t[index])
        sq = SimpleQuery(('index', 'name','spec','comment'))
        for d in defs:
            sq.records.append(AttrDict(*zip(('index','name','spec','comment'), d)))
        sq.status = "DESCRIBE %s%s" % (self.name, self.table.desc)
        return sq

    def sql_diff(self, command):
        pass

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
        field_verbose = self.fields_and_alias
        fields = self.fields.keys()
        header = []
        imprimido = '-'
        orden = ''
        clausa = ''
        donde = []
        distinta = False
        command = ' '.join(command.split())
        if not re.search(r' from ', command, flags=re.I):
            raise SQLError('FROM not specified')
        if command.split()[-2].lower() == 'to':
            imprimido = command.split()[-1]
            command = ' '.join(command.split()[:-2])
        #
        # get SELECT fields
        #
        seleccion, resto = re.split(r' from ', command, maxsplit=1, flags=re.I)
        seleccion = seleccion.split()[1:]
        if not seleccion:
            raise SQLError('missing fields')
        if seleccion[0].upper() == 'DISTINCT':
            distinta = True
            distinta # XXX
            seleccion.pop(0)
        if not seleccion:
            raise SQLError('missing fields')
        # get field names if * specified
        if seleccion == ['*']:
            seleccion = sorted(fields)
        else:
            seleccion = [s.strip() for s in ' '.join(seleccion).split(',')]
        for i, field in enumerate(seleccion):
            if as_match(field):
                field, alias = as_match.groups()
                bbx_index = field_verbose[field]
                field_verbose[alias] = bbx_index
                seleccion[i] = alias
                header.append(alias)
            elif field == 'id':
                # phony field used for COUNTing
                pass
            else:
                alias = self._fields_by_name[field][1]
                header.append(alias)
                bbx_index = field_verbose[field]
                field_verbose[alias] = bbx_index
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
        if desde.upper() in ('', 'WHERE', 'ORDER'):
            raise SQLError('missing table')
        # check for alias
        if resto and resto[0].upper() not in ('', 'WHERE', 'ORDER'):
            alias, resto = resto[0], resto[1:]
            table_alias[alias] = desde
            desde = alias
        # if table_alias.get(desde, desde) not in self.tables:
        #     self.tables[desde] = Table(table_alias.get(desde,desde))
        # table = self.tables[desde]
        if resto:
            if resto[0].upper() == 'WHERE':
                resto = resto[1:]
                if not resto or ' '.join(resto[:2]).upper() == 'ORDER BY':
                    raise SQLError('missing WHERE clause')
                resto = ' '.join(resto)
                if re.search(r' ORDER BY ', resto, flags=re.I):
                    clausa, resto = re.split(r' ORDER BY ', resto, maxsplit=1, flags=re.I)
                    resto = 'ORDER BY ' + resto
                    # clausa, orden = re.split(r' ORDER BY ', resto, maxsplit=1, flags=re.I)
                else:
                    clausa, resto = resto, ''
                clausa = clausa.strip()
                resto = resto.split()
            if ' '.join(resto[:2]).upper() == 'ORDER BY':
                orden = [o.strip() for o in ' '.join(resto[2:]).split(',')]
                resto = []
            if resto:
                raise SQLError('malformed query [%r]' % (' '.join(resto), ))
        #
        # and get WHERE clause
        #
        donde, constraints = convert_where(clausa)
        if _internal:
            imprimido = ''
        #
        # at this point we have the fields, and the table -- get the records
        #
        sq = SimpleQuery(header, aliased=field_verbose, to=imprimido)
        sq.records.extend(self._records(seleccion, field_verbose, donde, constraints))
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

class OpenERPTable(Table):
    """
    Handle interactions with OpenERP model.
    """
    def __new__(cls, table_name):
        ensure_oe()
        self = object.__new__(OpenERPTable)
        self.table = oe.get_model(table_name)
        self.name = self.table.model_name
        return self

    @property
    def fields(self):
        return self.table._all_columns.copy()

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
        sq = SimpleQuery(('table', 'count'))
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
            raise SQLError('table not specified')
        table = pieces[2]
        try:
            tables[table] = table = oe.get_model(table)
        except Fault as exc:
            if "doesn't exist" in exc.faultCode:
                raise SQLError('unknown table %r' % (table, ))
            raise
        if len(pieces) > 3 and pieces[3].lower() != 'where':
            raise SQLError('malformed command -- missing WHERE keyword')
        where_clause = ' '.join(pieces[4:])
        domain, constraints = convert_where(where_clause)
        if constraints:
            raise SQLError('constraints not supported in DELETE command')
        #
        # have all the info, make the changes
        #
        print('domain: %r' % (domain, ), verbose=3)
        ids = table.search(domain)
        if not ids:
            echo('no records found matching %r' % (where_clause, ))
        print('deleting %d records from %s' % (len(ids), table._name), verbose=3)
        table.unlink(ids)
        sq = SimpleQuery(('table', 'count'))
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
                raise SQLError('ORDER BY must be one of field, display, type, or help [ %r ]')
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
        sq = SimpleQuery(('field','display','type','detail','help'))
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
        sq = SimpleQuery(['fields \ ids']+[rec['id'] for rec in query.records], record_layout='column')
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
            raise SQLError('malformed command; use --help for help')
        elif fv_match():
            table, fields, values, verb, key = fv_match.groups()
            fields = [f.strip() for f in fields.split(',') if f != ',']
            print('%r -- %r -- %r -- %r -- %r' % (table, fields, values, verb, key), verbose=5)
            data = [literal_eval(values)]
        elif fl_match():
            table, csv_file, verb, key = fl_match.groups()
            try:
                csv = CSV(csv_file)
            except (IOError, OSError) as exc:
                raise ValueError("problem with %r -- <%r>" % (csv_file, repr(exc), ))
            fields = csv.header
            print('%r -- %r -- %r -- %r' % (table, csv_file, verb, key), verbose=5)
            data = list(csv)
        if verb and (verb.strip().lower() != 'update on' or not key):
            raise SQLError('invalid UPDATE ON clause')
        if key and key not in fields:
            raise SQLError('key %r not in FIELDS')
        try:
            table = oe.get_model(table)
        except Fault as exc:
            if "doesn't exist" in exc.faultCode:
                raise SQLError('unknown table %r' % (table, ))
            raise
        if not all_equal(data, test=lambda r,l=len(fields): len(r) == l):
            # print('fields: %r\nvalues: %r' % (fields, values), verbose=3)
            raise SQLError('fields/values mismatch')
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
                print('creating', values, verbose=3)
                table.create(values)
            except Exception as exc:
                raise
                error('unable to create:\n', pprint.pformat(values))
                raise ValueError(repr(exc))
            insert_count += 1
        sq = SimpleQuery(('table','inserted','updated'))
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
        field_verbose = {}        # {alias_name: field_name}
        imprimido = '-'
        orden = ''
        clausa = ''
        donde = []
        distinta = False
        print('command: %r' % (command, ), verbose=4)
        command = ' '.join(command.split())
        print('command: %r' % (command, ), verbose=3)
        if not re.search(r' from ', command, flags=re.I):
            raise SQLError('FROM not specified')
        if command.split()[-2].lower() == 'to':
            imprimido = command.split()[-1]
            command = ' '.join(command.split()[:-2])
        #
        # get SELECT fields
        #
        seleccion, resto = re.split(r' from ', command, maxsplit=1, flags=re.I)
        seleccion = seleccion.split()[1:]
        if not seleccion:
            raise SQLError('missing fields')
        if seleccion[0].upper() == 'DISTINCT':
            distinta = True
            seleccion.pop(0)
        if not seleccion:
            raise SQLError('missing fields')
        if seleccion != ['*']:
            seleccion = [s.strip() for s in ' '.join(seleccion).split(',')]
            if SHOW_ID and 'id' not in [s.lower() for s in seleccion]:
                seleccion.insert(0, 'id')
        #
        for i, field in enumerate(seleccion):
            if as_match(field):
                field, alias = as_match.groups()
                field_verbose[alias] = field
                seleccion[i] = alias
                header.append(alias)
            else:
                header.append(field)
        print('SELECT:', seleccion, verbose=3)
        #
        #
        # get FROM table
        #
        resto = resto.split()
        desde, resto = resto[0], resto[1:]
        if desde.upper() in ('', 'WHERE', 'ORDER'):
            raise SQLError('missing table')
        # self.tables[desde] = Table(desde)
        if resto:
            if resto[0].upper() == 'WHERE':
                resto = resto[1:]
                if not resto or ' '.join(resto[:2]).upper() == 'ORDER BY':
                    raise SQLError('missing WHERE clause')
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
                raise SQLError('malformed query [%r]' % (resto, ))
        # get field names if * specified
        if seleccion == ['*']:
            fields = list(self.fields.keys())
            if '-binary' in _internal:
                for field in self.table._binary_fields:
                    fields.remove(field)
            if '-x2many' in _internal:
                for field in self.table._x2many_fields:
                    fields.remove(field)
            if '-html' in _internal:
                for field in self.table._html_fields:
                    fields.remove(field)
            fields.remove('id')
            seleccion = ['id'] + sorted(fields)
            header = seleccion[:]
            print('SELECT:', seleccion, verbose=3)
        #
        # TODO: now make sure all field names are db and not user
        #
        print('WHERE', clausa, verbose=3)
        print('ORDER BY', orden, verbose=3)
        print('TO', imprimido, verbose=3)
        # normalize_field_names(desde, seleccion, clausa, orden)
        print('FROM', desde, verbose=3)
        #
        # and get WHERE clause
        #
        donde, constraints = convert_where(clausa, field_verbose)
        if _internal:
            imprimido = ''
        print('WHERE', donde, verbose=3)
        print('ORDER BY', orden, verbose=3)
        print('TO', imprimido, verbose=3)
        print('--CONSTRAINTS', constraints, verbose=3)
        #
        # at this point we have the fields, and the table -- hand off to _adhoc()
        #
        fields = list(seleccion)

        query = Query(
                self.table,
                fields=fields[:],
                aliases=field_verbose,
                domain=donde or ALL_ACTIVE,
                order=orden,
                unique=distinta,
                to_file = imprimido,
                constraints=constraints,
                )
        query.status = 'SELECT %d' % len(query)
        query.fields = header
        query.alias = field_verbose
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
            raise SQLError('table not specified')
        table = pieces[1]
        try:
            tables[table] = table = oe.get_model(table)
        except Fault as exc:
            if "doesn't exist" in exc.faultCode:
                raise SQLError('unknown table %r' % (table, ))
            raise
        if len(pieces) < 3 or pieces[2].lower() != 'set':
            raise SQLError('malformed command -- missing SET keyword')
        command = ' '.join(pieces[3:])
        try:
            where_index = command.lower().index(' where ')
            where_clause = command[where_index+7:]
            set_clause = command[:where_index]
        except ValueError:
            if command.lower().endswith(' where'):
                raise SQLError('malformed command -- missing WHERE parameters')
            where_clause = []
            set_clause = command
        print('where clause: %r' % (where_clause, ), verbose=3)
        values = convert_set(set_clause)
        if not values:
            raise SQLError('malformed command -- no changes specified')
        if where_clause:
            domain, constraints = convert_where(where_clause)
        else:
            domain = constraints = []
        if constraints:
            raise SQLError('constraints not supported in UPDATE command')
        #
        # have all the info, make the changes
        #
        print('domain: %r' % (domain, ), verbose=3)
        ids = table.search(domain)
        print('writing\n  %r\nto %s for ids\n%r' % (values, table._name, ids), verbose=3)
        table.write(ids, values)
        sq = SimpleQuery(('table', 'updated'))
        sq.records.append(AttrDict(table=self.table.model_name, updated=len(ids)))
        sq.status = 'UPDATE %d' % len(ids)
        return sq

class GenericTable(Table):
    """
    Generic table
    """
    def __repr__(self):
        return "GenericTable(name=%r, fields=%r)" % (self.name, self._fields.keys())

    def _records(self, fields, aliased, where, constraints):
        # print('fields requested: %s' % (fields, ), verbose=3)
        # print('where: %r' % (where, ), verbose=3)
        # print('constraints: %r' % (constraints, ), verbose=3)
        filter = create_filter(where, aliased)
        print('filter:', filter, verbose=3)
        print('aliased:', aliased, verbose=3)
        records = []
        for r in self.table:
            if filter(r):
                if all(c(r) for c in constraints):
                    row = []
                    for f in fields:
                        if f == 'id' and 'id' not in aliased:
                            continue
                        row.append(r[aliased.get(f,f)])
                    records.append(OrderedDict(zip(fields, row)))
        return records

    def sql_count(self, command):
        temp = command.split()
        if len(temp) > 1 and temp[1].upper() == 'FROM':
            temp.insert(1, 'id')
            command = ' '.join(temp)
        query = self.sql_select(command, _internal=True)
        sq = SimpleQuery(('table', 'count'))
        sq.records.append(AttrDict(table=self.name, count=len(query)))
        sq.status = "COUNT %s" % len(query)
        return sq

    def sql_describe(self, command, _internal=''):
        """
        DESCRIBE table
        """
        if self.types is None and self.table:
            undef = set(self.fields.keys())
            for rec in self.table:
                for f in undef:
                    if rec[f] is not None:
                        self.types[f] = type(rec[f]).__name__
                        undef.remove(f)
                if not undef:
                    break
            for f in undef:
                # use dummy value for missing types
                self.types[f] = ''
        index = 0
        defs = sorted(self.fields.values(), key=lambda t: t[index])
        sq = SimpleQuery(('index', 'name','spec','comment'))
        for d in defs:
            sq.records.append(AttrDict(*zip(('index','name','spec','comment'), d)))
        sq.status = "DESCRIBE 1"
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
        table_match = Var(lambda sel: re.match(r'(\S+)\s+AS\s+(\S+)\b(.*)', sel, re.I)) 
        table_alias = {}
        field_alias = {}
        fields = self._fields.keys()
        header = []
        imprimido = '-'
        orden = ''
        clausa = ''
        donde = []
        distinta = False
        command = ' '.join(command.split())
        if not re.search(r' from ', command, flags=re.I):
            raise SQLError('FROM not specified')
        if command.split()[-2].lower() == 'to':
            imprimido = command.split()[-1]
            command = ' '.join(command.split()[:-2])
        #
        # get SELECT fields
        #
        seleccion, resto = re.split(r' from ', command, maxsplit=1, flags=re.I)
        print('SELECT: %r   REST: %r' % (seleccion, resto), verbose=4)
        seleccion = seleccion.split()[1:]
        if not seleccion:
            raise SQLError('missing fields')
        if seleccion[0].upper() == 'DISTINCT':
            distinta = True
            distinta # XXX
            seleccion.pop(0)
        if not seleccion:
            raise SQLError('missing fields')
        # get field names if * specified
        if seleccion == ['*']:
            seleccion = fields
        else:
            seleccion = [s.strip() for s in ' '.join(seleccion).split(',')]
        for i, field in enumerate(seleccion):
            if as_match(field):
                field, alias = as_match.groups()
                field_alias[alias] = field
                seleccion[i] = alias
                header.append(alias)
            elif field == 'id' and 'id' not in fields:
                # phony field used for COUNTing
                pass
            else:
                field_alias[field] = field
                header.append(field)
        print('SELECT:', seleccion, verbose=3)
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
        print('0 FROM: %r   REST: %r' % (desde, resto), verbose=4)
        if desde.upper() in ('', 'WHERE', 'ORDER'):
            raise SQLError('missing table')
        # check for alias
        if resto and resto[0].upper() not in ('', 'WHERE', 'ORDER'):
            alias, resto = resto[0], resto[1:]
            print('0 ALIAS: %r   REST: %r' % (alias, resto), verbose=4)
            table_alias[alias] = desde
            desde = alias
        # if table_alias.get(desde, desde) not in self.tables:
        #     self.tables[desde] = Table(table_alias.get(desde,desde))
        # table = self.tables[desde]
        if resto:
            if resto[0].upper() == 'WHERE':
                resto = resto[1:]
                if not resto or ' '.join(resto[:2]).upper() == 'ORDER BY':
                    raise SQLError('missing WHERE clause')
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
                raise SQLError('malformed query [%r]' % (resto, ))
        print('WHERE', clausa, verbose=3)
        print('ORDER BY', orden, verbose=3)
        print('TO', imprimido, verbose=3)
        # normalize_field_names(desde, seleccion, clausa, orden)
        print('FROM', desde, verbose=3)
        #
        # and get WHERE clause
        #
        donde, constraints = convert_where(clausa)
        if _internal:
            imprimido = ''
        print('WHERE', donde, verbose=3)
        print('ORDER BY', orden, verbose=3)
        print('TO', imprimido, verbose=3)
        print('CONSTRAINTS', constraints, verbose=3)
        print('ALIASES', field_alias, verbose=3)
        #
        # at this point we have the fields, and the table -- get the records
        #
        sq = SimpleQuery(header, aliased=field_alias, to=imprimido)
        print('getting records', verbose=3)
        sq.records.extend(self._records(seleccion, field_alias, donde, constraints))
        sq.status = "SELECT %s" % len(sq.records)
        return sq

class DbfTable(GenericTable):
    """
    dbf.Table wrapper
    """
    def __repr__(self):
        return "DbfTable(name=%r, fields=%r)" % (self.name, self.table.field_names)

    def sql_describe(self, command, _internal=''):
        """
        DESCRIBE table
        """
        defs = [dfn.split(' ', 1)[1] for dfn in self.table.structure()]
        sq = SimpleQuery(('index', 'name','spec','comment'))
        for i, (fn, dfn) in enumerate(zip(self.table.field_names, defs)):
            sq.records.append(AttrDict(index=i, name=fn, spec=dfn, comment=None))
        sq.status = "DESCRIBE 1"
        return sq


class Node(object):
    #
    max_clauses = 1

    def __init__(self):
        self.clauses = []
        self.result = None

    def __nonzero__(self):
        if self.result is None:
            raise ValueError("truthiness of %s has not been determined")
        return self.result
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
        # print('Node.process: %r' % (record, ), verbose=4)
        for i, clause in enumerate(self.clauses, start=1):
            if isinstance(clause, tuple):
                field, op, target = clause
                print('looking for %r of %r in %r' % (field, record[field], record), verbose=4)
                field = record[field]
                self.result = self.operators[op](field, target)
            elif isinstance(clause, Node):
                self.result = clause.process(record)
            if i == 1:
                if type(self) is Node:
                    return self.result
                elif type(self) is Not:
                    return not self.result
                elif type(self) is And and self.result is False:
                    return False
                elif type(self) is Or and self.result is True:
                    return True
            else:
                # i = 2
                return self.result
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
        if self.result is None:
            field, op, target = self.clauses[-1]
            field = self.record[field]
            if not self.operators[op](field, target):
                # if any term is False, the whole thing is False
                self.result = False
            elif len(self.clauses) == self.max_clauses:
                self.result = True


class Or(Node):
    #
    max_clauses = 2
    #
    def evaluate(self):
        if self.result is None:
            field, op, target = self.clauses[-1]
            field = self.record[field]
            if self.operators[op](field, target):
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
        self.result = not self.operators[op](field, target)


class Join(object):
    def __init__(self, join_type, table, condition):
        if join_type not in (
                'INNER JOIN', 'OUTER JOIN', 'FULL JOIN',
                'LEFT JOIN', 'RIGHT JOIN',
                'CROSS JOIN',
            ):
            raise ValueError('invalid JOIN type: %r' % (join_type, ))
        self.type = join_type
        self.table_name = table
        self.condition = condition
        if join_type == 'CROSS JOIN':
            if condition:
                raise SQLError('invalid JOIN condition: %r' % (condition, ))
        elif not self.condition_match(condition):
            raise SQLError('invalid JOIN condition: %r' % (condition, ))

    def __call__(self, current_sq, records, table_by_field, header_mapping):
        # current_sq is the existing records
        # records are the new records to join (aka the right table)
        method = getattr(self, self.type.lower().replace(' ','_'))
        return method(current_sq, records, table_by_field, header_mapping)

    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__.__name__, self.type, self.table_name, self.condition)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.table_name == other.table_name and self.condition == other.condition

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type != other.type or self.table_name != other.table_name or self.condition != other.condition

    condition_match = Var(lambda condition: re.match(
                r"^(\S+)\s*(is not|is|not in|in|like|=like|not like|ilike|=ilike|not ilike|<=|>=|!=|=)\s*(\S+)$",
                condition,
                flags=re.I
                ))

    def _left_right(self, table_by_field, field1, field2):
        if table_by_field.get(field1, None) == self.table_name:
            left_name = field2
            right_name = field1
            if table_by_field.get(field2, None) == self.table_name:
                raise SQLError('0 - invalid JOIN condition: %r' % self.condition)
        elif table_by_field.get(field2, None) == self.table_name:
            left_name = field1
            right_name = field2
        else:
            raise SQLError('1 - invalid JOIN condition: %r' % self.condition)
        return left_name, right_name

    def cross_join(self, left_sq, right_sq, table_by_field, header_mapping):
        sq = left_sq.as_template()
        for left_rec in left_sq:
            for right_rec in right_sq:
                new_rec = left_rec.copy()
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
        return sq

    def full_join(self, left_sq, right_sq, table_by_field, header_mapping):
        """
        keep every merged record
        """
        sq = left_sq.as_template()
        field1, op, field2 = self.condition_match(self.condition).groups()
        print('table name: %r' % self.table_name, verbose=3)
        print(' - '.join([repr(t) for t in (field1, op, field2)]), verbose=4)
        if op != '=':
            raise SQLError('JOIN only allows "=" for joining records')
        left_name, right_name = self._left_right(table_by_field, field1, field2)
        right_sq.records.sort(key=lambda r: r[right_name])
        left_sq.records.sort(key=lambda r: r[left_name])
        i = j = 0
        last_left_rec = None
        last_left_index = last_right_index = None
        found = False
        while i < len(left_sq) or j < len(right_sq):
            if i < len(left_sq):
                left_rec = left_sq.records[i]
            else:
                left_rec = EMPTY
            if i != last_left_index and last_left_rec == left_rec[left_name]:
                j = last_right_index
            if j < len(right_sq):
                right_rec = right_sq.records[j]
            else:
                right_rec = EMPTY
            left_data = left_rec and left_rec[left_name]
            right_data = right_rec and right_rec[right_name]
            if right_data is EMPTY:
                i += 1
                if not found:
                    sq.add_record(left_rec)
                found = False
            elif left_data is EMPTY:
                j += 1
                new_rec = {}
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
            elif left_data < right_data:
                i += 1
                if not found:
                    sq.add_record(left_rec)
                found = False
            elif left_data > right_data:
                j += 1
                if not found:
                    new_rec = {}
                    for field, value in right_rec.items():
                        new_rec[field] = value
                    sq.add_record(new_rec)
                last_right_index = None
                found = False
            else:
                # they are equal
                found = True
                last_left_index = i
                # if last_right_index is None:
                if last_left_rec != left_data:
                    last_right_index = j
                last_left_rec = left_rec[left_name]
                new_rec = left_rec.copy()
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
                j += 1
        return sq

    def left_join(self, left_sq, right_sq, table_by_field, header_mapping):
        """
        all records in left_sq will be included, along with any matches in right_sq
        """
        sq = left_sq.as_template()
        field1, op, field2 = self.condition_match(self.condition).groups()
        print('table name: %r' % self.table_name, verbose=3)
        print(' - '.join([repr(t) for t in (field1, op, field2)]), verbose=4)
        if op != '=':
            raise SQLError('JOIN only allows "=" for joining records')
        left_name, right_name = self._left_right(table_by_field, field1, field2)
        right_sq.records.sort(key=lambda r: r[right_name])
        left_sq.records.sort(key=lambda r: r[left_name])
        i = j = 0
        last_left_rec = None
        last_right_index = None
        last_left_index = 0
        found = False
        while i < len(left_sq):
            left_rec = left_sq.records[i]
            if i != last_left_index and last_left_rec == left_rec[left_name] and last_right_index is not None:
                j = last_right_index
            if j < len(right_sq):
                right_rec = right_sq.records[j]
            else:
                right_rec = EMPTY
            if right_rec is EMPTY or left_rec[left_name] < right_rec[right_name]:
                # no right match possible, add left record
                i += 1
                if not found:
                    sq.add_record(left_rec)
                found = False
            elif left_rec[left_name] > right_rec[right_name]:
                j += 1
                last_right_index = None
                found = False
            else:
                # they are equal
                found = True
                last_left_index = i
                last_left_rec = left_rec[left_name]
                if last_right_index is None:
                    last_right_index = j
                new_rec = left_rec.copy()
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
                j += 1
        return sq

    def inner_join(self, left_sq, right_sq, table_by_field, header_mapping):
        """
        keep all merged records that have data from both tables
        """
        sq = left_sq.as_template()
        field1, op, field2 = self.condition_match(self.condition).groups()
        if op != '=':
            raise SQLError('JOIN only allows "=" for joining records')
        left_name, right_name = self._left_right(table_by_field, field1, field2)
        print('left field: %r   right field: %r' % (left_name, right_name), verbose=3)
        right_sq.records.sort(key=lambda r: r[right_name])
        left_sq.records.sort(key=lambda r: r[left_name])
        i = j = 0
        last_left_index = last_right_index = None
        while i < len(left_sq):
            left_rec = left_sq.records[i]
            right_rec = right_sq.records[j]
            print('%r  vs  %r' % (left_rec, right_rec), verbose=4)
            if left_rec[left_name] < right_rec[right_name]:
                i += 1
                if last_right_index is not None:
                    j = last_right_index
            elif left_rec[left_name] > right_rec[right_name]:
                if last_left_index is None:
                    # haven't found a match yet
                    j += 1
                elif i == last_left_index + 1:
                    # only one match on left side
                    j += 1
                    last_left_index = last_right_index = None
                elif last_right_index is not None:
                    # left record is same as previous left record and matched right record
                    i = last_left_index + 1  # record after first match on left
                    j = last_right_index     # record of first match on right
                else:
                    pass

            else:
                # they are equal
                last_left_index = i
                if last_right_index is None:
                    last_right_index = j
                new_rec = left_rec.copy()
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
                j += 1
                # check if right_rec is worn out; if yes, increment i instead
                if j == len(right_sq):
                    j -= 1
                    i += 1
        return sq

    def outer_join(self, left_sq, right_sq, table_by_field, header_mapping):
        """
        keep merged records with no match from the other table
        """
        def next_ne(records, index, field, target):
            while index < len(records) and records[index][field] == target:
                index += 1
            return index
        sq = left_sq.as_template()
        field1, op, field2 = self.condition_match(self.condition).groups()
        print('table name: %r' % self.table_name, verbose=3)
        print(' - '.join([repr(t) for t in (field1, op, field2)]), verbose=4)
        if op != '=':
            raise SQLError('JOIN only allows "=" for joining records')
        left_name, right_name = self._left_right(table_by_field, field1, field2)
        right_sq.records.sort(key=lambda r: r[right_name])
        left_sq.records.sort(key=lambda r: r[left_name])
        i = j = 0
        while i < len(left_sq) or j < len(right_sq):
            if i < len(left_sq):
                left_rec = left_sq.records[i]
            else:
                left_rec = EMPTY
            if j < len(right_sq):
                right_rec = right_sq.records[j]
            else:
                right_rec = EMPTY
            left_data = left_rec and left_rec[left_name]
            right_data = right_rec and right_rec[right_name]
            if right_data is EMPTY:
                print('2 adding LEFT', verbose=4)
                sq.add_record(left_rec)
                i += 1
            elif left_data is EMPTY:
                print('3 adding RIGHT', verbose=4)
                new_rec = {}
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
                j += 1
            elif left_data < right_data:
                print('4 adding LEFT', verbose=4)
                sq.add_record(left_rec)
                i += 1
            elif left_data > right_data:
                print('5 adding RIGHT', verbose=4)
                new_rec = {}
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
                j += 1
            else:
                # they are equal, skip 'em
                print('6 skipping  i=%r  j=%r' % (i, j), verbose=4)
                i = next_ne(left_sq.records, i, left_name, left_data)
                j = next_ne(right_sq.records, j, right_name, right_data)
                print('            i=%r j=%r' % (i, j), verbose=4)
        return sq

    def right_join(self, left_sq, right_sq, table_by_field, header_mapping):
        """
        all records in right_sq will be included, along with any matches in left_sq
        """
        sq = left_sq.as_template()
        field1, op, field2 = self.condition_match(self.condition).groups()
        if op != '=':
            raise SQLError('JOIN only allows "=" for joining records')
        left_name, right_name = self._left_right(table_by_field, field1, field2)
        right_sq.records.sort(key=lambda r: r[right_name])
        left_sq.records.sort(key=lambda r: r[left_name])
        i = j = 0
        last_right_rec = None
        last_left_index = None
        last_right_index = 0
        found = False
        while i < len(right_sq):
            right_rec = right_sq.records[i]
            if i != last_right_index and last_right_rec == right_rec[right_name] and last_left_index is not None:
                j = last_left_index
            if j < len(left_sq):
                left_rec = left_sq.records[j]
            else:
                left_rec = EMPTY
            if left_rec is EMPTY or right_rec[right_name] < left_rec[left_name]:
                i += 1
                if not found:
                    new_rec = {}
                    for field, value in right_rec.items():
                        new_rec[field] = value
                    sq.add_record(new_rec)
                found = False
            elif right_rec[right_name] > left_rec[left_name]:
                j += 1
                last_left_index = None
                found = False
            else:
                found = True
                last_right_index = i
                last_right_rec = right_rec[right_name]
                if last_left_index is None:
                    last_left_index = j
                new_rec = left_rec.copy()
                for field, value in right_rec.items():
                    new_rec[field] = value
                sq.add_record(new_rec)
                j += 1
        print('FINAL i, j VALUEs: %d, %r' % (i, j), verbose=4)
        return sq


class SimpleQuery(object):
    """
    Presents same attributes as openerplib.utils.query.
    """
    def __init__(self, fields, aliased=None, record_layout='row', to='-'):
        # fields: list of final field names (could be aliases)
        # aliased: complete table/field name, along with any functions used
        print('SQ fields=%r' % (fields, ), verbose=3)
        if isinstance(fields, tuple):
            fields = list(fields)
        if not isinstance(fields, list):
            raise ValueError('fields should be a list, not %r' % (fields, ))
        self.fields = fields
        self.aliases = aliased or {}
        self.to_file = to
        self.records = []
        self.orientation = record_layout
        self.status = None

    def __iter__(self):
        return iter(self.records)

    def __len__(self):
        return len(self.records)

    def __repr__(self):
        return "SimpleQuery(fields=%r, aliases=%r)" % (
                self.fields,
                self.aliases,
                )

    def add_record(self, values):
        print('ADDING %r into %r' % (values, self.fields), verbose=4)
        new_record = {}.fromkeys(self.fields, EMPTY)
        new_record.update(values)
        self.records.append(new_record)

    def as_template(self):
        new_sq = self.__class__(self.fields[:], self.aliases.copy(), self.orientation, self.to_file)
        return new_sq

    def finalize(self, fields):
        """
        recreate each row with only the specified fields as a NamedTuple
        """
        nt = NamedTuple('record', ((f, i, '', EMPTY) for i, f in enumerate(fields)))
        if fields != self.fields:
            self.fields = fields
        records = self.records
        for i, rec in enumerate(records):
            records[i] = nt(**dict((f, rec[f]) for f in fields))


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

    - SELECT fields for display
    - tables used  (SQLTableParams)
      - fields  {'alias': 'field name'}
      - where conditions "some_field = some_value"
    - fields/aliases mapping to tables  {'n.alias': SQLTableParams('n')}
    - joins  (Join(type=..., left_table=..., level=..., conditions=...))
    - group by
    - order
    - output

    NB: Both fields and tables can have multiple aliases, in which case they
    are considered to be different fields/tables.
    """
    transforms = {
            'date':       lambda t: fix_date(t, format='ymd'),
            'strip_html': lambda t: '\n'.join(re.sub('<.+?>', '', t).split()),
            }
    aggregates = {
            'avg':   lambda field, records: (sum([r[field] for r in records]) / len(records)) if records else None,
            'count': lambda field, records: len(records) if field == '*' else sum([bool(r[field]) for r in records]),
            'list':  lambda field, records: '\n'.join([str(r[field]) for r in records if r[field]]),
            'max':   lambda field, records: max([r[field] for r in records]),
            'min':   lambda field, records: min([r[field] for r in records]),
            'sum':   lambda field, records: sum([r[field] for r in records]),
            }
    def __init__(self, statement, debug=False):
        print('__INIT__', verbose=3)
        print(repr(statement), verbose=4)
        self.primary_table = None
        self.header = []                                                            # selected fields for final display
        self.tables = OrderedDict()                                                 # {'table_alias': SQLTableParams}
        self.fields = set()                                                         # {'field_name': ['alias1','alias2',...]}
        self.field_aliases = {}                                                     # {'alias':'field', 'alias':field', ...}
        self.joins = []
        self.where = ''
        self.one_where = ''                                                         # the where if only one table in query
        self.distinct = False
        self.orders = []
        self.groups = []
        self.to = '-'
        self.conditions = []                                                        # how tables are linked together
        self.strict_fields = False                                                  # whether table prefixes are required
        self.table_by_field_alias = {}
        self.raw_statement = statement.strip()
        self._final_statement = []
        self.words = []
        self.offset = 0
        self.complete = False
        self.command = None
        self.final = False                                                          # if final changes have been made in self.execute()
        try:
            self.parse()
            self.q_start()
            if not self.complete:
                raise SQLError('SQL statement incomplete')
            self.process()
        except Exception:
            if debug:
                print_exc()
            else:
                raise

    def __iter__(self):
        return iter(self.execute())

    def __repr__(self):
        return self.statement

    def __str__(self):
        return '\n'.join([
                "Statement: %r" % ' '.join(self._final_statement),
                "Tables:    %r" % self.tables,
                "Fields:    %r" % self.fields,
                "Queries:   %s" % '\n           '.join([repr(tp.query) for tp in self.tables.values()]),
                "Joins:     %s" % '\n           '.join([repr(j) for j in self.joins]),
                "TbFA:      %r" % self.table_by_field_alias,
                ])

    @property
    def statement(self):
        return ' '.join(self._final_statement).replace(' , ',', ')

    def _get_tp_from(self, term1, term2):
        for term in (term1, term2):
            try:
                return self.tables[self.table_by_field_alias[term]]
            except KeyError:
                pass
            try:
                return self.tables[self.table_by_field_alias[split_tbl(term)]]
            except (KeyError, ValueError):
                continue
        raise SQLError('unable to find table from %r or %r' % (term1, term2))

    def _parse_where_term(self, word, pair):
        print('_parse_where_term: %r %r' % (word, pair), verbose=4)
        skip = False
        if pair.lower() in ("is not","not in","not like","not ilike"):
            print('lower 2', verbose=4)
            ct = OP
            skip = True
            word = pair
        elif word.lower() in ("is", "in", "like", "=like", "ilike", "=ilike", "<", ">", "<=", ">=", "=", "!=", "==?", "<|>"):
            print('lower 1', verbose=4)
            ct = OP
        elif word.lower() in ('and', 'or'):
            print('lower 3', verbose=4)
            ct = CONJUNCTION
        else:
            print('else 1', verbose=4)
            # field or constant
            #
            # constants are quoted, numeric, or keywords null, true, false
            if is_quoted(word) or is_numeric(word) or is_keyword(word):
                # definitely a constant
                ct = CONSTANT
            else:
                # probably a field
                ct = FIELD
                try:
                    if '.' not in word:
                        # get table name from field name/alias
                        field = word
                        table = self.table_by_field_alias[field]
                    else:
                        # get aliased names for both table and field
                        table, field = split_tbl_fn(word)
                        if word not in self.table_by_field_alias:
                            self.table_by_field_alias[word] = table
                        if table not in self.tables:
                            raise SQLError('unknown table %r in %r' % (table, word))
                        else:
                            print('1: tables: %r' % self.tables, verbose=4)
                            join_tp = self.tables[table]
                            print('join_tp: %r' %  join_tp, verbose=4)
                            print('SQL.fields: %r' % self.fields)
                            if word not in self.fields:
                                join_tp.fields.setdefault(field, []).append(word)
                                self.fields.add(word)
                            field_dests = join_tp.fields[split_fn(word)]
                            if word not in field_dests:
                                field_dests.append(word)
                            print('join_tp: %r' %  join_tp, verbose=4)
                        word = '%s.%s' % (table, field)
                except KeyError:
                    pass
                    # nope, a constant after all!
                    # ct = CONSTANT
        print('final type: %r' % ct, verbose=4)
        return ct, word, skip

    def _register_field(self, name, table=None):
        # name could be a simple field or a dotted-field/alias
        use_table = False
        alias, field = name, self.field_aliases.get(name, name)
        # get matching table and param structure
        if '.' in field:
            table = split_tbl(field)
            use_table = True
        elif field in self.table_by_field_alias:
            table = self.table_by_field_alias[field]
        elif table is not None:
            pass
        elif table is None:
            assert len(self.tables) == 1, "table not specified, and more than one"
            table = list(self.tables)[0]
        else:
            assert False, "hmmm..."
        fn = split_fn(field)
        tp = self.tables[table]
        a = fn
        if use_table:
            a = '%s.%s' % (tp.alias, fn)
        # check alias, then field
        for f in (alias, field):
            if f in self.fields:
                break
        else:
            # nothing found, add original name (possibly with table prefix)
            self.fields.add(a)
        # make sure original name is recorded in field destination list
        field_dests = tp.fields.setdefault(fn, [])
        if name not in field_dests:
            field_dests.append(name)
        self.table_by_field_alias[name] = table

    def execute(self):
        """
        query tables and return result
        """
        print('EXECUTE', verbose=3)
        print(self, verbose=3)
        # pull state into local vars
        starred = '*' in self.table_by_field_alias
        multi_tables = len(self.tables) > 1
        #
        # do all the queries
        results = {}
        sq_fields = []
        star_fields = []
        header_aliases = {}
        for tp in self.tables.values():

            r = Table.query(tp.query)
            if starred:
                table = ''
                if multi_tables:
                    table = tp.alias + '.'
                star_fields.extend(['%s%s' % (table, f) for f in r.fields])
                new_fields = []
                for f in r.fields:
                    name = '%s%s' % (table, f)
                    full_name = '%s.%s' % (tp.alias, f)
                    new_fields.append(name)
                    header_aliases[name] = full_name
                    self._register_field(name, tp.alias)
            else:
                new_fields = []
                for field, aliases in tp.fields.items():
                    new_fields.extend(aliases)
                    sq_fields.extend(aliases)
                    for a in aliases:
                        header_aliases[a] = '%s.%s' % (tp.alias, field)
            new_sq = SimpleQuery(new_fields)
            for rec in r:
                new_rec = {}
                for field, aliases in tp.fields.items():
                    if field == '*':
                        continue
                    for a in aliases:
                        new_rec[a] = rec[field]
                new_sq.add_record(new_rec)
            r = new_sq
            results[tp.alias] = r

            print('r: %r' % r, verbose=4)
            print('r.aliases: %r' % r.aliases, verbose=4)
            print('r.fields: %r' % r.fields, verbose=4)
            print('star fields: %r' % star_fields, verbose=4)
            for field, transform in tp.transforms.items():
                if transform not in self.transforms:
                    raise SQLError('unknown function: %r' % (transform, ))
                for rec in r:
                    rec[field] = self.transforms[transform](rec[field])
        if starred:
            self.header = star_fields
        #
        sq = SimpleQuery(star_fields or sq_fields, header_aliases, to=self.to)
        #
        # process primary table
        primary = results[self.primary_table]
        for row in primary:
            sq.add_record(row)
        #
        # merge with joins
        for join in self.joins:
            sq = join(
                    sq,
                    results[join.table_name],
                    self.table_by_field_alias,
                    header_aliases,
                    )
        print('sq records after joins: %d' % len(sq), verbose=4)
        # process WHERE
        print('WHERE: %r' % self.where, verbose=4)
        if self.where and len(self.tables) > 1:
            # if only one table, WHERE clause was included in query
            #
            # create alias mapping in the format expected by convert_where of
            # alias_name:field_name
            domain, constraints = convert_where(self.where, null=EMPTY)
            filter = create_filter(domain)
            records = []
            for rec in sq:
                if filter(rec):
                    if all(c(rec) for c in constraints):
                        records.append(rec)
            sq.records = records
        print('sq records after where: %d' % len(sq), verbose=4)
        # process GROUP BY
        print('GROUP BY: %r' % self.groups, verbose=4)
        if self.groups:
            all_aggs = {}
            for tp in self.tables.values():
                all_aggs.update(tp.aggregates)
            key = self.make_key(self.groups)
            groups = {}
            for rec in sq.records:
                current = key(rec)
                groups.setdefault(current, []).append(rec)
            # pick one record from each group
            sq.records = []
            for recs in groups.values():
                final_rec = recs[0]
                for field, agg in all_aggs.items():
                    final_rec[field] = self.aggregates[agg](field, recs)
                sq.records.append(final_rec)
        # process ORDER BY
        print('ORDER BY: %r' % self.orders, verbose=1)
        if self.orders:
            print('sorting records', verbose=1)
            for o in reversed(self.orders):
                o = o.split()
                if len(o) == 1:
                    o.append('ASC')
                f, d = o    # field, direction
                if d.upper() == 'ASC':
                    sq.records.sort(key=lambda r: r[f])
                else:
                    sq.records.sort(key=lambda r: r[f], reverse=True)
        sq.finalize(self.header)
        sq.status = "%s %d" % (self.command, len(sq.records))
        return sq

    def make_key(self, fields):
        """
        make a sorting key using the fields provided
        """
        def key(rec):
            ans = ()
            for f in fields:
                ans += rec[f],
            return ans
        return key

    def parse(self):
        """
        get next "word" in statement
        """
        print('PARSE', verbose=3)
        statement = self.raw_statement
        offset = i = 0
        while True:
            alpha = False
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
                        alpha = False
                        self.words.append(''.join(word))
                        word = []
                    continue
                elif ch in ' \t\n' and not word:
                    continue
                elif ch in ' \t\n' and word:
                    break
                elif word and word[-1] == RPAREN:
                    alpha = False
                    self.words.append(''.join(word))
                    word = []
                #
                if ch == BACKSLASH:
                    esc = True
                    continue
                elif ch == SINGLE_QUOTE:
                    if word:
                        self.words.append(''.join(word))
                        word = []
                    word.append(ch)
                    quote = True
                    alpha = ch.isalnum() or ch in '._'
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
            if ''.join(word).strip():
                self.words.append(''.join(word))
            offset += i or 1
            if offset + 1 >= len(self.raw_statement):
                break
        print('PARSED: %r' % self.words, verbose=4)

    def process(self):
        print('PROCESS', verbose=3)
        print(self.statement, verbose=3)
        pt = self.primary_table
        print('tbfa: %r' % self.table_by_field_alias, verbose=4)
        for field_name, table_name in self.table_by_field_alias.items():
            print('fn: %r   -   tn: %r' % (field_name, table_name), verbose=4)
            if table_name is None:
                self.table_by_field_alias[field_name] = pt
        print('tbfa: %r' % self.table_by_field_alias, verbose=4)
        # add primary query
        query = ['SELECT']
        if len(self.tables) == 1 and self.distinct:
            query.append('DISTINCT')
        fields = []
        tp = self.tables[pt]
        print('tp: %r' % tp, verbose=4)
        if '*' in self.table_by_field_alias:
            fields.append('*')
        else:
            fields.extend(list(tp.fields))
        query.append(', '.join(fields))
        query.append('FROM')
        query.append(tp.table_name)
        if len(self.tables) == 1 and self.one_where:
            query.append('WHERE')
            query.append(self.one_where)
        print('main query: %r' % query, verbose=4)
        print('query already in tp: %r' % tp.query, verbose=4)
        tp.query = ' '.join(query)
        # now add any other tables
        for alias, tp in self.tables.items():
            if alias == pt:
                continue
            query = ['SELECT']
            fields = []
            if '*' in self.table_by_field_alias:
                fields.append('*')
            else:
                fields.extend(list(tp.fields))
            query.append(', '.join(fields))
            query.append('FROM')
            if tp.table_name is None:
                raise SQLError('missing full table name for table %r' % tp.alias)
            query.append(tp.table_name)
            print(query, verbose=4)
            tp.query = ' '.join(query)
            print('FINAL tp query: %r' % tp.query, verbose=4)

    def q_delete(self):
        print('Q_DELETE', verbose=3)
        # not a valid end state as a
        # WHERE clause is required (non-standard)
        i =  0
        for i, word in enumerate(self.words[self.offset+i:], start=i+1):
            print(i, word, verbose=4)
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            if word.upper() == 'FROM':
                print('FROM', verbose=4)
                self._final_statement[-1] = self._final_statement[-1].upper()
                break
            else:
                raise SQLError('FROM must follow DELETE')
        else:
            # loop exhausted, FROM not seen
            raise SQLError('FROM must follow DELETE')
        self.offset += i
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method(peos=False, from_delete=True)

    def q_from(self, peos, from_delete=False):                                      # possible end of statement?
        """
        Get primary table (possibly only table).
        """
        print('Q_FROM (peos=%r, from_delete=%r)' % (peos, from_delete), verbose=3)
        # valid end state
        # oe tables will have periods in them
        self.complete = False
        tables = self.tables
        tables_acquired = False
        last_table = None
        alias = False                                                               # True=required, None=optional, False=no
        comma_needed = False
        if from_delete:
            allowed_words = ('WHERE', )
            allowed_pairs = ()
        else:
            allowed_words = ('JOIN', 'WHERE', 'TO')
            allowed_pairs = ('CROSS JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 'FULL JOIN', 'ORDER BY', 'GROUP BY')
        i = 0
        for i, word in enumerate(self.words[self.offset:], start=1):
            print('%d: %r' % (i, word), verbose=4)
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            pair = '%s %s' % (word.upper(), next_word)
            if word.upper() in allowed_words:
                print('   single: %r' % word, verbose=4)
                self._final_statement[-1] = self._final_statement[-1].upper()
                if self._final_statement[-1] == 'JOIN':
                    self._final_statement[-1] = 'INNER JOIN'
                break
            elif pair in allowed_pairs:
                print('   double: %r' % pair, verbose=4)
                word = pair.replace(' ','_')
                self._final_statement[-1] = pair
                i += 1
                break
            if comma_needed and word != COMMA:
                raise SQLError('comma missing between table definitions')
            elif word == COMMA:
                print('   comma', verbose=4)
                if alias:
                    raise SQLError('missing alias for %r' % last_table)
                raise SQLError('only one table supported in FROM clause')
            elif word.upper() == 'AS':
                print('   as', verbose=4)
                self._final_statement.pop()
                alias = True
            elif alias in (None, True):                                             # `alias is None` means two adjacent names without AS
                print('   alias trigger: %r' % alias, verbose=4)
                # `word` is the alias, `last_table` is the actual name
                if None in tables:
                    tp = tables.pop(None)
                    tp.alias = word
                    tables[word] = tp
                else:
                    tp = tables.setdefault(word, SQLTableParams(word))
                tp.table_name = last_table
                self.primary_table = word
                alias = False
                last_table = None
                comma_needed = True
            else:
                print('   table: %r' % word, verbose=4)
                # this is a table
                last_table = word
                alias = None
                tables_acquired = True
        else:
            # loop exhausted, only one table given
            print('   loop exhausted, no break', verbose=4)
            word = None

        # clean up
        if not from_delete and last_table is not None:
            if None in tables:
                tp = tables.pop(None)
            else:
                try:
                    tp = tables.pop(last_table)
                except KeyError:
                    raise SQLError('no fields specified for table %r' % last_table)
            tp.alias = last_table
            tp.table_name = last_table
            tables[last_table] = tp
            self.primary_table = last_table
        for field, table_name in self.table_by_field_alias.items():
            if table_name is None:
                self.table_by_field_alias[field] = tp.alias

        # more sanity checks
        print('break seen, word=%r' % word, verbose=4)
        self.offset += i
        if alias:
            raise SQLError('missing alias for %r' % last_table)
        if not tables_acquired:
            raise SQLError('no tables in FROM clause')
        print('4 tbfa: %r' % self.table_by_field_alias, verbose=4)
        print('5 tables: %r' % tables, verbose=4)
        if word is not None:
            if word.endswith('_JOIN'):
                word = 'JOIN'
            next_method = getattr(self, 'q_%s' % word.lower())
            next_method(peos=True)
        else:
            self.complete = True

    def q_group_by(self, peos):
        """
        randomly return one record for each group
        """
        print('Q_GROUP_BY (peos=%r)' % peos, verbose=3)
        self.complete = False
        group_acquired = False
        last_field = None
        comma_needed = False
        i = 0
        print(self.words[self.offset:], verbose=3)
        allowed_words = ('HAVING', )
        allowed_pairs = ('ORDER BY', )
        for i, word in enumerate(self.words[self.offset:], start=1):
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            pair = '%s %s' % (word.upper(), next_word)
            if word.upper() in allowed_words:
                print('   single: %r' % word, verbose=4)
                self._final_statement[-1] = self._final_statement[-1].upper()
                break
            elif pair in allowed_pairs:
                print('   double: %r' % pair, verbose=4)
                word = pair.replace(' ','_')
                self._final_statement[-1] = pair
                i += 1
                break
            if comma_needed and word != COMMA:
                raise SQLError('comma missing between group by specifications [next word: %r]' % word)
            elif word == COMMA:
                last_field = None
                comma_needed = False
            elif last_field is not None:
                raise SQLError('comma missing between group by specifications [next word: %r]' % word)
            else:
                last_field = word
                self._register_field(last_field)
                self.groups.append(last_field)
                group_acquired = True
        else:
            # loop exhausted, no other clauses after group by
            word = None
            if not peos:
                raise SQLError('incomplete SQL statement')
            else:
                self.complete = True
        self.offset += i
        # sanity checks
        if not group_acquired:
            raise SQLError('no GROUP BY fields in clause')
        if word is not None:
            next_method = getattr(self, 'q_%s' % word.lower())
            next_method(peos=True)

    def q_join(self, peos):
        """
        Get linked tables.
        """
        # SELECT Orders.OrderID, Customers.CustomerName, Shippers.ShipperName
        # FROM ((Orders
        # INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID)
        # INNER JOIN Shippers ON Orders.ShipperID = Shippers.ShipperID);
        print('Q_JOIN', verbose=3)
        tables = self.tables
        print('0: tables: %r' % tables, verbose=4)
        join_type = self._final_statement[-1]
        self.complete = False
        try:
            word1, word2, word3 = self.words[self.offset:self.offset+3]
            self._final_statement.append(word1)
        except ValueError:
            raise SQLError('incomplete SQL statement')
        # get table and (possibly) alias
        if word2.upper() == 'AS':
            table_name = word1
            alias = word3
            self._final_statement.append(word3)
            self.offset += 4
        elif word3.upper() == 'ON':
            table_name = word1
            alias = word2
            self._final_statement.append(word2)
            self.offset += 3
        else:
            table_name = word1
            alias = word1
            self.offset += 2
        # fix up self.tables
        if alias in tables:
            left_tp = tables[alias]
            left_tp.table_name = table_name
        else:
            left_tp = SQLTableParams(alias, table_name)
            tables[alias] = left_tp
        # double check that ON was the next word
        if join_type != 'CROSS JOIN':
            if self.words[self.offset-1].upper() != 'ON':
                raise SQLError('only JOIN ... ON is currently supported')
            self._final_statement.append('ON')
        # self.offset should now be pointing to the word after ON
        condition = []
        condition_type = []
        i = 0
        skip = False
        for i, word in enumerate(self.words[self.offset:], start=1):
            print('%d: %r' % (i, word), verbose=4)
            self._final_statement.append(word)
            if skip:
                skip = False
                print('skipping', verbose=4)
                continue
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            pair = '%s %s' % (word.upper(), next_word)
            if word.upper() in ('WHERE', 'TO', 'JOIN'):
                print('upper 1', verbose=4)
                self._final_statement[-1] = self._final_statement[-1].upper()
                if self._final_statement[-1] == 'JOIN':
                    self._final_statement[-1] = 'INNER JOIN'
                break
            elif pair in ('CROSS JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 'FULL JOIN', 'ORDER BY', 'GROUP BY'):
                print('upper 2', verbose=4)
                word = pair.replace(' ','_')
                self._final_statement[-1] = pair
                i += 1
                break
            # must be part of the condition
            # what type is it?
            ct, word, skip = self._parse_where_term(word, pair)
            # combine sequential constants
            if condition and ct is CONSTANT and condition_type[-1] is CONSTANT:
                prev_word = condition.pop()
                condition.append('%s %s' % (prev_word, word))
            else:
                condition.append(word)
                condition_type.append(ct)
        else:
            # loop exhausted, no further clauses
            word = None
            if not peos:
                raise SQLError('incomplete SQL statement')
            else:
                self.complete = True

        # optimization: move constant clauses to appropriate table's WHERE clause
        print('optimizing %r' % condition, verbose=4)
        print(condition_type, verbose=4)
        new_condition = []
        last_conjunction = None
        last_tp = None
        j = 0
        while j < len(condition):
            ct1 = condition_type[j]
            if ct1 is CONJUNCTION:
                if last_conjunction is not None:
                    raise SQLError('%r cannot follow %r' % (ct1, last_conjunction))
                last_conjunction = condition[j].upper()
                j += 1
            print(condition_type[j:j+3], verbose=4)
            ct1, _, ct2 = condition_type[j:j+3]
            if ct1 is CONSTANT or ct2 is CONSTANT:
                term1, op, term2 = condition[j:j+3]
                where_tp = self._get_tp_from(term1, term2)
                print('where_tp: %r' % where_tp.where, verbose=4)
                print('condition: %r' % condition[j:j+3], verbose=4)
                if last_tp is not None and last_conjunction == 'OR' and where_tp != last_tp:
                    raise SQLError('constant conditions from different tables must be separated by OR')
                if where_tp.where:
                    where_tp.where.append(last_conjunction)
                if ct1 is FIELD:
                    if term1 not in self.table_by_field_alias:
                        # field has not already been added via SELECT, it had better include the table
                        self.table_by_field_alias[term1] = split_tbl(term1)
                    term1 = split_fn(term1)
                else:
                    if term2 not in self.table_by_field_alias:
                        self.table_by_field_alias[term2] = split_tbl(term2)
                    term2 = split_fn(term2)
                where_tp.where.append(term1)
                where_tp.where.append(op)
                where_tp.where.append(term2)
                print('where_tp: %r' % where_tp.where, verbose=4)
                print('where_tp: %r' % where_tp.query, verbose=4)
            else:
                if last_conjunction is not None:
                    new_condition.append(last_conjunction)
                new_condition.extend(condition[j:j+3])
                last_tp = None
            last_conjunction = None
            j += 3
        condition = new_condition


        print('TBFA: %r' % self.table_by_field_alias, verbose=4)
        self.offset += i
        # sanity checks
        if not condition and join_type != 'CROSS JOIN':
            raise SQLError('no ON condition in JOIN clause')
        self.joins.append(Join(join_type, left_tp.alias, ' '.join(condition)))
        print('joins: %r' % self.joins, verbose=4)

        if word is not None:
            if word.endswith('_JOIN'):
                word = 'JOIN'
            next_method = getattr(self, 'q_%s' % word.lower())
            next_method(peos=True)

    def q_order_by(self, peos):
        """
        Get sorting order for final results.
        """
        print('Q_ORDER_BY', verbose=3)
        self.complete = False
        order_acquired = False
        last_field = None
        order_seen = False
        comma_needed = False
        i = 0
        print(self.words[self.offset:], verbose=3)
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
                raise SQLError('comma missing between order specifications [next word: %r]' % word)
            elif word == COMMA:
                last_field = None
                order_seen = False
                comma_needed = False
            elif last_field is not None and word.upper() in ('ASC', 'DESC'):
                if order_seen:
                    raise SQLError('ASC/DESC can only be specified once per field')
                order_seen = True
                self._final_statement[-1] = self._final_statement[-1].upper()
                self.orders[-1] = '%s %s' % (self.orders[-1], word.upper())
                last_field = None
                comma_needed = True
            elif last_field is not None:
                raise SQLError('comma missing between order specifications [next word: %r]' % word)
            else:
                last_field = word
                self._register_field(last_field)
                self.orders.append(last_field)
                order_acquired = True
        else:
            # loop exhausted, nothing after order
            word = None
            if not peos:
                raise SQLError('incomplete SQL statement')
            else:
                self.complete = True

        self.offset += i
        # sanity checks
        if not order_acquired:
            raise SQLError('no ORDER BY fields in clause')
        if word is not None:
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
        print('Q_SELECT', verbose=3)
        self.complete = False
        fields_acquired = False
        last_field = None
        last_table = None
        alias = False
        comma_needed = False
        tables = self.tables
        tables[None] = tp = SQLTableParams(None)
        i = 0
        if self.words[self.offset+i].upper() == 'DISTINCT':
            self._final_statement.append('DISTINCT')
            self.distinct = True
            i += 1
        for i, word in enumerate(self.words[self.offset+i:], start=i+1):
            print(i, word, verbose=4)
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '').upper()
            if word.upper() == 'FROM':
                print('FROM', verbose=4)
                if last_field is not None:
                    # last_field -> [table.]field_name
                    field_name = split_fn(last_field)
                    tables[last_table].fields.setdefault(field_name, []).append(last_field)
                    self.fields.add(last_field)
                    if last_table is None:
                        if tp.alias is not None:
                            raise ValueError("tp.alias should be None (%r)" % tp)
                    self.header.append(last_field)
                    self.table_by_field_alias[last_field] = last_table
                self._final_statement[-1] = self._final_statement[-1].upper()
                break
            if comma_needed and word != COMMA:
                raise SQLError('comma missing between field definitions')
            elif word == COMMA:
                print('COMMA', verbose=4)
                if alias:
                    raise SQLError('missing alias for %r' % last_field)
                if last_field is not None:
                    # last_field -> [table.]field_name

                    field_name = split_fn(last_field)
                    tables[last_table].fields.setdefault(field_name, []).append(last_field)
                    self.fields.add(last_field)
                    self.table_by_field_alias[last_field] = last_table
                    self.header.append(last_field)
                last_field = None
                last_table = None
                alias = False
                comma_needed = False
            elif word == LPAREN:
                print('LPAREN', verbose=4)
                print('moving %r from field to func' % last_field, verbose=4)
                func = last_field
                last_field = None
                alias = False
            elif word == RPAREN:
                print('RPAREN', verbose=4)
                print('saving %s(%s)' % (func, last_field), verbose=4)
                if func in self.transforms:
                    tp.transforms[last_field] = func
                elif func in self.aggregates:
                    tp.aggregates[last_field] = func
                else:
                    raise SQLError('unknown function: %r' % (func, ))
                func = None
            elif word.upper() == 'AS':
                print('AS', verbose=4)
                self._final_statement.pop()
                alias = True
            elif '.' in word:
                # word should be a table.field pair
                print('PERIOD', verbose=3)
                if alias in (None, True):
                    raise SQLError('aliases cannot contain periods [%r]' % word)
                table, field = word.rsplit('.', 1)
                if None in tables:
                    tp = tables.pop(None)
                    if tp.fields:
                        # cannot have fields already
                        raise SQLError('cannot mix table.field syntax with plain field syntax')
                    # first field, update table alias
                    tp.alias = table
                    tables[table] = tp
                else:
                    for tp in tables.values():
                        if tp.alias == table:
                            # already exists
                            break
                    else:
                        tp = SQLTableParams(table)
                        tables[table] = tp
                # tp is the current (not-None) table
                last_field = word   # use alias
                last_table = table
                alias = None
                fields_acquired=True
                self.strict_fields = True
            elif alias in (None, True):
                # word -> alias for field
                # last_field -> [table.]field_name
                print('alias is %r' % alias, verbose=4)
                print('1 tbfa: %r' % self.table_by_field_alias, verbose=4)
                field_name = split_fn(last_field)
                self.table_by_field_alias[word] = last_table
                tables[last_table].fields.setdefault(field_name, []).append(word)
                self.fields.add(last_field)
                self.field_aliases[word] = last_field
                self.header.append(word)
                # update functions, if any
                if last_field in tp.transforms:
                    tpt = tp.transforms
                    print('renaming %r parameter from %r to %r' % (tpt[last_field], last_field, word), verbose=4)
                    tpt[word] = tpt.pop(last_field)
                elif last_field in tp.aggregates:
                    agg = tp.aggregates
                    print('renaming %r parameter from %r to %r' % (agg[last_field], last_field, word), verbose=4)
                    agg[word] = agg.pop(last_field)
                alias = False
                last_field = None
                last_table = None
                comma_needed = True
                print('2 tbfa: %r' % self.table_by_field_alias, verbose=4)
                print('2 tables: %r' % self.tables, verbose=4)
            else:
                # word -> field name or function
                print('saving name %r' % word, verbose=4)
                if last_table is not None and func is None:
                    raise SQLError('cannot mix table.field syntax with plain field syntax')
                last_field = word
                alias = None
                fields_acquired=True
        else:
            # `FROM` not found
            raise SQLError('missing FROM')
        self.offset += i
        # sanity checks
        if alias:
            raise SQLError('missing alias for %r' % last_field)
        if not fields_acquired:
            raise SQLError('no fields specified')
        print('3 tables: %r' % tables, verbose=4)
        print('3 tbfa: %r' % self.table_by_field_alias, verbose=4)
        print('3 stmnt: %r  %r' % (self.statement, self._final_statement), verbose=4)
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method(peos=True)

    def q_start(self):
        """
        Determine command to run.
        """
        print('Q_START', verbose=3)
        word = self.words[0]
        self.offset = 1
        if word.upper() not in (
                'COUNT', 'DELETE', 'DESCRIBE', 'DIFF', 'INSERT', 'SELECT', 'UPDATE',
            ):
            raise SQLError('unknown command: %r' % word)
        self.command = word.upper()
        self._final_statement.append(word.upper())
        next_method = getattr(self, 'q_%s' % word.lower())
        next_method()

    def q_to(self, peos):
        """
        Where to send final results.
        """
        print('Q_TO', verbose=3)
        word = self.words[self.offset:self.offset+1]
        if not word:
            raise SQLError('no TO destination')
        word = word[0]
        self._final_statement.append(word)
        self.to = word
        self.offset += 1
        word = self.words[self.offset:self.offset+1]
        if word:
            raise SQLError('extra TO parameters')
        self.complete = True
        return

    def q_where(self, peos):
        """
        Get filter to select records.
        """
        print('Q_WHERE (tables=%r)' % self.tables, verbose=3)
        self.complete = False
        wheres_acquired = False
        wheres_acquired # XXX
        condition = []
        condition_type = []
        one_where = []
        i = 0
        skip = False
        for i, word in enumerate(self.words[self.offset:], start=1):
            print('%d: %r' % (i, word), verbose=4)
            if skip:
                skip = False
                print('skipping', verbose=4)
                continue
            self._final_statement.append(word)
            next_word = self.words[self.offset+i:self.offset+i+1]
            next_word = (next_word and next_word[0] or '')
            pair = '%s %s' % (word, next_word)
            if word.upper() == 'TO':
                self._final_statement[-1] = self._final_statement[-1].upper()
                break
            elif pair.upper() in ('ORDER BY', 'GROUP BY'):
                word = pair.replace(' ','_')
                self._final_statement[-1] = pair.upper()
                i += 1
                break

            # must be part of the condition
            # what type is it?
            ct, word, skip = self._parse_where_term(word, pair)
            print('ct: %r;  word: %r;  skip: %r' % (ct, word, skip), verbose=4)
            # combine sequential constants
            if condition and ct is CONSTANT and condition_type[-1] is CONSTANT:
                prev_word = condition.pop()
                condition.append('%s %s' % (prev_word, word))
            else:
                condition.append(word)
                condition_type.append(ct)

        else:
            # loop exhausted, no further clauses
            word = None
            if not peos:
                raise SQLError('incomplete SQL statement')
            else:
                self.complete = True
        self.offset += i
        # sanity checks
        if not condition:
            raise SQLError('no WHERE condition')
        # valid field checks
        for term, ct in zip(condition, condition_type):
            if ct is FIELD:
                if '.' in term:
                    if len(self.tables) == 1:
                        field_table = split_tbl(term)
                        if self.primary_table == field_table:
                            term = split_fn(term)
                        else:
                            raise SQLError('unknown table %r in %r' % (field_table, term))
                elif self.strict_fields and term not in self.table_by_field_alias:
                    raise SQLError('field %r missing table prefix' % term)
            one_where.append(term)
        # done
        self.where = ' '.join(condition)
        self.one_where = ' '.join(one_where)
        print('self.where: %r' % self.where, verbose=4)
        if word is not None:
            next_method = getattr(self, 'q_%s' % word.lower())
            next_method(peos=True)

class SQLTableParams(object):
    """
    contains everything needed to query one table
    """
    def __init__(self, alias, table_name=None, fields=None, conditions=None, query=None, transforms=None, aggregates=None):
        self.alias = alias                                                          # plain text name (might be actual)
        self.table_name = table_name                                                # real name (could be same as .alias)
        self.fields = fields or OrderedDict()                                       # fields to fetch `{alias:field}`
        self.conditions = conditions or []                                          # record filters
        self._query = query
        self.where = []
        self.transforms = transforms or {}
        self.aggregates = aggregates or {}
        self.having = []

    def __repr__(self):
        if self.alias == self.table_name:
            return "%s(%r, %r)" % (self.__class__.__name__, self.alias, self.fields)
        else:
            return "%s(%r, %r, %r)" % (self.__class__.__name__, self.alias, self.table_name, self.fields)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            not_equal = []
            if self.alias != other.alias: not_equal.append('a: %r != %r' % (self.alias, other.alias))
            if self.table_name != other.table_name: not_equal.append('t: %r != %r' % (self.table_name, other.table_name))
            if self.fields != other.fields: not_equal.append('f: %r != %r' % (self.fields, other.fields))
            if self.conditions != other.conditions: not_equal.append('c: %r != %r' % (self.conditions, other.conditions))
            if self.query != other.query: not_equal.append('q: %r != %r' % (self.query, other.query))
            if self.transforms != other.transforms: not_equal.append('q: %r != %r' % (self.transforms, other.transforms))
            if not_equal:
                raise Exception('  -  '.join(not_equal))
            return (
                    self.alias == other.alias
                and self.table_name == other.table_name
                and self.fields == other.fields
                and self.conditions == other.conditions
                and self.query == other.query
                and self.transforms == other.transforms
                )
        else:
            return False

    def __ne__(self, other):
        return not self == other

    @property
    def query(self):
        if self.where:
            return '%s WHERE %s' % (self._query, ' '.join(self.where))
        else:
            return self._query

    @query.setter
    def query(self, value):
        self._query = value


def split_fn(field):
    """
    field -> [table.]field
    """
    return field.rsplit('.',1)[-1]

def split_tbl(field):
    """
    field -> [table.]field
    """
    table, field = field.rsplit('.',1)
    return table

def split_tbl_fn(field):
    """
    field -> table.field
    """
    table, field = field.rsplit('.',1)
    return table, field


## SQL Query examples
#
#    List all the companies, and include all their departments, and all their employees.
#    Note that some companies don't have any departments yet, but make sure you include
#    them as well. Make sure you only retrieve departments that have employees, but always
#    list all companies.
#
# SELECT *
# FROM Company
#      LEFT JOIN (
#          Department INNER JOIN Employee ON Department.ID = Employee.DepartmentID
#      ) ON Company.ID = Department.CompanyID
#
#
# SELECT *
# FROM Company
#      LEFT JOIN (
#          Department INNER JOIN Employee ON Department.ID = Employee.DepartmentID
#      ) ON Company.ID = Department.CompanyID AND Department.Name LIKE '%X%'
#
#
