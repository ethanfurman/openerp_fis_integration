from __future__ import print_function
from aenum import NamedTuple
from antipathy import Path
import dbf
from .sql import EMPTY, SQL, convert_where, Join, SQLTableParams, SQLError
from .sql import Table, FISTable, OpenERPTable, GenericTable, DbfTable
from .sql import oe
from enhlib.misc import zip
from openerplib.utils import AttrDict
import os
import sys
import tempfile
import unittest

# globals

class SQLParams(NamedTuple):
    input = 0, "raw input from user"
    statement = 1, "converted input"
    header = 2, "report fields and their order"
    tables = 3, "tables used"
    joins = 4, "table joins (with conditions)", []
    where = 5, "conditions on table(s)", ''
    orders = 6, "order by clauses", []
    to = 7, "where to send output", '-'
    primary_table = 8, "main/first table in SQL query"
    table_by_field_alias = 9, "get table by looking up alias"


class TestCase(unittest.TestCase):

    run_so_far = []

    def __init__(self, *args, **kwds):
        regex = getattr(self, 'assertRaisesRegex', None)
        if regex is None:
            self.assertRaisesRegex = getattr(self, 'assertRaisesRegexp')
        super(TestCase, self).__init__(*args, **kwds)


def ensure_oe(test):
    def wrapper(*args, **kwds):
        if oe is None:
            raise RuntimeError('OpenERP is not running')
        return test(*args, **kwds)
    return wrapper

class TestTables(TestCase):

    def test_FIS(self):
        FISTable.query("select employee_no from EMP1")
        Table.query("select employee_no from EMP1")

    @ensure_oe
    def test_OpenERP(self):
        OpenERPTable.query("select id, name from res.users where login='admin' order by name")
        Table.query("select id, name from res.users where login='admin' order by name")

    def test_Generic(self):
        GenericTable.query('select * from customer order by last')
        Table.query('select * from customer order by last')

    def test_DBF(self):
        with PrepDBF('customer'):
            DbfTable.query('select * from dbf_customer order by last')
            Table.query('select * from dbf_customer order by last')

    def test_SQL(self):
        SQL("select xml_id, name, fis_name from product.product where xml_id = '' order by name")
        SQL("select xml_id, name, fis_name from product.product p where xml_id = '' order by name")


class PrepDBF(object):
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.filename.unlink()
    def __init__(self, source):
        # get temp name for dbf table
        fh, fn = tempfile.mkstemp(suffix='.dbf')
        os.close(fh)
        self.filename = Path(fn)
        # construct field layout for dbf table
        fields = []
        src_table = Table.tables[source]
        for fn, ft in src_table.types.items():
            if ft in ('str','unicode'):
                fd = 'C(32)'
            elif ft == 'int':
                fd = 'N(3,0'
            elif ft == 'float':
                fd = 'N(7,3)'
            else:
                raise ValueError('unknown type: %r' % ft)
            fields.append('%s %s' % (fn, fd))
        dst_table = dbf.Table(self.filename, fields).open(dbf.READ_WRITE)
        # copy data into dbf table
        for row in src_table:
            dst_table.append(row)
        dst_table.close()
        # and load into Table.tables
        Table.from_data('dbf_%s'%source, data=self.filename)


# Tests


# class Test(TestCase):
#     def test_multiple_star(self):
#         query = SQL("select * from customer join invoice on customer.cust_id = invoice.cust_id").execute()
#         for row in query:
#             print(row)


class TestSQL(TestCase):
    #
    statements = (
            SQLParams(  # 0
                input='select * from res.users',
                statement='SELECT * FROM res.users',
                header=['*'],
                tables={'res.users': SQLTableParams(
                                                    alias='res.users',
                                                    table_name='res.users',
                                                    fields={'*': '*'},
                                                    query='SELECT * FROM res.users',
                                                    )},
                to='-',
                primary_table = 'res.users',
                table_by_field_alias = {'*': 'res.users'},
                ),
            SQLParams(  # 1
                input='select name desc from NVTY',
                statement='SELECT name desc FROM NVTY',
                header=['desc'],
                tables={'NVTY': SQLTableParams(
                                                    alias='NVTY',
                                                    table_name='NVTY',
                                                    fields={'desc':'name'},
                                                    query='SELECT name as desc FROM NVTY',
                                                    )},
                primary_table = 'NVTY',
                table_by_field_alias = {'desc': 'NVTY'},
                ),
            SQLParams(  # 2
                input='select name, desc from NVTY',
                statement='SELECT name, desc FROM NVTY',
                header=['name','desc'],
                tables={'NVTY': SQLTableParams(
                                                    alias='NVTY',
                                                    table_name='NVTY',
                                                    fields={'desc':'desc', 'name':'name'},
                                                    query='SELECT name, desc FROM NVTY',
                                                    )},
                primary_table = 'NVTY',
                table_by_field_alias = {'desc': 'NVTY', 'name': 'NVTY'},
                ),
            SQLParams(  # 3
                input="select item_id from 135 where item_id like '1000'",
                statement="SELECT item_id FROM 135 WHERE item_id like '1000'",
                header=['item_id'],
                tables={'135': SQLTableParams(
                                                alias='135',
                                                table_name='135',
                                                fields={'item_id':'item_id'},
                                                query="SELECT item_id FROM 135 WHERE item_id like '1000'",
                                                )},
                where="item_id like '1000'",
                primary_table = '135',
                table_by_field_alias = {'item_id': '135'},
                ),
            SQLParams(  # 4
                input='select name n, desc from nvty inv order by item_no',
                statement='SELECT name n, desc FROM nvty inv ORDER BY item_no',
                header=['n','desc'],
                tables={'inv': SQLTableParams(
                                                alias='inv',
                                                table_name='nvty',
                                                fields={'n':'name', 'desc':'desc', 'item_no':'item_no'},
                                                query='SELECT name as n, desc, item_no FROM nvty',
                                                )},
                orders=['item_no'],
                to='-',
                primary_table = 'inv',
                table_by_field_alias = {'n': 'inv', 'desc': 'inv', 'item_no': 'inv'},
                ),
            SQLParams(  # 5
                input='select * from order',
                statement='SELECT * FROM order',
                header=['*'],
                tables={'order': SQLTableParams(
                                                alias='order',
                                                table_name='order',
                                                fields={'*':'*'},
                                                query='SELECT * FROM order',
                                                )},
                primary_table = 'order',
                table_by_field_alias = {'*': 'order'},
                ),
            SQLParams(  # 6
                input='select n.item_id, p.that_id as that, p.this_id this from nvty n join product p on n.item_id=p.item_id order by n.item_id',
                statement='SELECT n.item_id, p.that_id that, p.this_id this FROM nvty n INNER JOIN product p ON n.item_id = p.item_id ORDER BY n.item_id',
                header=['n.item_id','that','this'],
                tables={'n':SQLTableParams(
                                                alias='n',
                                                table_name='nvty',
                                                fields={'item_id':'item_id'},
                                                query='SELECT item_id FROM nvty',
                                                ),
                        'p':SQLTableParams(
                                                alias='p',
                                                table_name='product',
                                                fields={'that':'that_id', 'this':'this_id', 'item_id':'item_id'},
                                                query='SELECT that_id as that, this_id as this, item_id FROM product',
                                                ),
                        },
                joins=[Join('INNER JOIN', 'p', 'n.item_id = p.item_id')],
                orders=['n.item_id'],
                primary_table = 'n',
                table_by_field_alias={'n.item_id':'n', 'that':'p', 'this':'p', 'p.item_id':'p'},
                ),
            SQLParams(  # 7
                input='select n.item_id, p.that_id from nvty n join product p on n.item_id=p.item_id order by n.item',
                statement='SELECT n.item_id, p.that_id FROM nvty n INNER JOIN product p ON n.item_id = p.item_id ORDER BY n.item',
                header=['n.item_id','p.that_id'],
                tables={'n':SQLTableParams(
                                                alias='n',
                                                table_name='nvty',
                                                fields={'item_id':'item_id', 'item':'item'},
                                                query='SELECT item_id, item FROM nvty',
                                                ),
                        'p':SQLTableParams(
                                                alias='p',
                                                table_name='product',
                                                fields={'that_id':'that_id', 'item_id':'item_id'},
                                                query='SELECT that_id, item_id FROM product',
                                                ),
                        },
                joins=[Join('INNER JOIN', 'p', 'n.item_id = p.item_id')],
                orders=['n.item'],
                primary_table = 'n',
                table_by_field_alias={'n.item_id':'n', 'p.that_id':'p', 'p.item_id':'p', 'n.item':'n'},
                ),
            SQLParams(  # 8
                input='select name, desc from NVTY to test.csv',
                statement='SELECT name, desc FROM NVTY TO test.csv',
                header=['name','desc'],
                tables={'NVTY':SQLTableParams(
                                                alias='NVTY',
                                                table_name='NVTY',
                                                fields={'name':'name', 'desc':'desc'},
                                                query='SELECT name, desc FROM NVTY',
                                                ),
                        },
                to='test.csv',
                primary_table = 'NVTY',
                table_by_field_alias={'name':'NVTY', 'desc':'NVTY'},
                ),
            SQLParams(  # 9
                input="select n.item item, n.cost product_cost, n.shipping_meth shipping, s.cost as shipping_cost "
                       "from inventory as n "
                       "join shipping s on shipping=s.shipping_method "
                       "where item like 'plum' and product_cost < 10.0 and shipping_cost > 5.0 "
                       "order by item "
                       "to info.csv",
                statement="SELECT n.item item, n.cost product_cost, n.shipping_meth shipping, s.cost shipping_cost "
                       "FROM inventory n "
                       "INNER JOIN shipping s ON shipping = s.shipping_method "
                       "WHERE item like 'plum' and product_cost < 10.0 and shipping_cost > 5.0 "
                       "ORDER BY item "
                       "TO info.csv",
                header=['item','product_cost','shipping','shipping_cost'],
                tables={'n':SQLTableParams(
                                                alias='n',
                                                table_name='inventory',
                                                fields={'item':'item', 'product_cost':'cost', 'shipping':'shipping_meth'},
                                                query="SELECT item, cost as product_cost, shipping_meth as shipping "
                                                      "FROM inventory",
                                                ),
                        's':SQLTableParams(
                                                alias='s',
                                                table_name='shipping',
                                                fields={'shipping_cost':'cost', 'shipping_method':'shipping_method'},
                                                query='SELECT cost as shipping_cost, shipping_method FROM shipping',
                                                ),
                        },
                joins=[Join('INNER JOIN', 's', 'shipping = s.shipping_method')],
                orders=['item'],
                to='info.csv',
                where="item like 'plum' and product_cost < 10.0 and shipping_cost > 5.0",
                primary_table = 'n',
                table_by_field_alias={'item':'n', 'product_cost':'n', 'shipping':'n', 'shipping_cost':'s', 's.shipping_method':'s'},
                ),
            SQLParams(  # 10
                input="select n.item item, n.cost product_cost, n.shipping_meth shipping, s.cost as shipping_cost "
                       "from inventory as n "
                       "join shipping s on n.shipping_meth=s.shipping_method and n.warehouse_id = '1000'"
                       "where item like 'plum' and product_cost < 10.0 and shipping_cost > 5.0 "
                       "order by item "
                       "to info.csv",
                statement="SELECT n.item item, n.cost product_cost, n.shipping_meth shipping, s.cost shipping_cost "
                       "FROM inventory n "
                       "INNER JOIN shipping s ON n.shipping_meth = s.shipping_method and n.warehouse_id = '1000' "
                       "WHERE item like 'plum' and product_cost < 10.0 and shipping_cost > 5.0 "
                       "ORDER BY item "
                       "TO info.csv",
                header=['item','product_cost','shipping','shipping_cost'],
                tables={'n':SQLTableParams(
                                                alias='n',
                                                table_name='inventory',
                                                fields={'item':'item', 'product_cost':'cost', 'shipping':'shipping_meth', 'warehouse_id':'warehouse_id'},
                                                query="SELECT item, cost as product_cost, shipping_meth as shipping, warehouse_id "
                                                      "FROM inventory WHERE warehouse_id = '1000'"
                                                ),
                        's':SQLTableParams(
                                                alias='s',
                                                table_name='shipping',
                                                fields={'shipping_cost':'cost', 'shipping_method':'shipping_method'},
                                                query="SELECT cost as shipping_cost, shipping_method FROM shipping",
                                                ),
                        },
                joins=[Join('INNER JOIN', 's', 'n.shipping_meth = s.shipping_method')],
                where="item like 'plum' and product_cost < 10.0 and shipping_cost > 5.0",
                orders=['item'],
                to='info.csv',
                primary_table='n',
                table_by_field_alias={'item':'n', 'product_cost':'n', 'shipping':'n', 'n.shipping_meth':'n', 'n.warehouse_id':'n',
                                      'shipping_cost':'s', 's.shipping_method':'s'},
                ),
            SQLParams(  # 11
                input="select res.users.xml_id user_id, hr.employee.xml_id emp_id, hr.employee.name "
                        "from res.users "
                        "join hr.employee on user_id=emp_id",
                statement="SELECT res.users.xml_id user_id, hr.employee.xml_id emp_id, hr.employee.name "
                        "FROM res.users "
                        "INNER JOIN hr.employee ON user_id = emp_id",
                header=['user_id','emp_id','hr.employee.name',],
                tables={'res.users':SQLTableParams(
                                                alias='res.users',
                                                table_name='res.users',
                                                fields={'user_id':'xml_id'},
                                                query="SELECT xml_id as user_id FROM res.users",
                                                ),
                        'hr.employee':SQLTableParams(
                                                alias='hr.employee',
                                                table_name='hr.employee',
                                                fields={'emp_id':'xml_id', 'name':'name'},
                                                query="SELECT xml_id as emp_id, name FROM hr.employee",
                                                ),
                        },
                joins=[Join('INNER JOIN', 'hr.employee', 'user_id = emp_id')],
                primary_table = 'res.users',
                table_by_field_alias={'user_id':'res.users', 'emp_id':'hr.employee', 'hr.employee.name':'hr.employee'}
                ),
            SQLParams(  # 12
                input="select n.item, p.formula, d.item ingred "
                        "from 135 n "
                        "right join 322 p on n.item_id=p.formula_id "
                        "left join 323 d on d.formula_id=p.formula_id "
                        "where n.item_id like '1000' "
                        "order by n.item, p.formula desc, ingred",
                statement="SELECT n.item, p.formula, d.item ingred "
                        "FROM 135 n "
                        "RIGHT JOIN 322 p ON n.item_id = p.formula_id "
                        "LEFT JOIN 323 d ON d.formula_id = p.formula_id "
                        "WHERE n.item_id like '1000' "
                        "ORDER BY n.item, p.formula DESC, ingred",
                header=['n.item', 'p.formula', 'ingred'],
                tables={'n': SQLTableParams(
                                                alias='n',
                                                table_name='135',
                                                fields={'item':'item', 'item_id':'item_id'},
                                                query="SELECT item, item_id FROM 135",
                                                ),
                        'p': SQLTableParams(
                                                alias='p',
                                                table_name='322',
                                                fields={'formula':'formula', 'formula_id':'formula_id'},
                                                query="SELECT formula, formula_id FROM 322",
                                                ),
                        'd': SQLTableParams(
                                                alias='d',
                                                table_name='323',
                                                fields={'ingred':'item', 'formula_id':'formula_id'},
                                                query="SELECT item as ingred, formula_id FROM 323",
                                                ),
                        },
                joins=[
                        Join('RIGHT JOIN', 'p', 'n.item_id = p.formula_id'),
                        Join('LEFT JOIN', 'd', 'd.formula_id = p.formula_id'),
                        ],
                where="n.item_id like '1000'",
                orders=['n.item','p.formula DESC','ingred'],
                primary_table = 'n',
                table_by_field_alias={'n.item':'n', 'n.item_id':'n',
                                      'p.formula':'p', 'p.formula_id':'p',
                                      'ingred':'d', 'd.formula_id':'d'},
                ),
            SQLParams(  # 13
                input='select n.name, n.desc from NVTY n',
                statement='SELECT n.name, n.desc FROM NVTY n',
                header=['n.name','n.desc'],
                tables={'n': SQLTableParams(
                                                    alias='n',
                                                    table_name='NVTY',
                                                    fields={'desc':'desc', 'name':'name'},
                                                    query='SELECT name, desc FROM NVTY',
                                                    )},
                primary_table = 'n',
                table_by_field_alias = {'n.desc': 'n', 'n.name': 'n'},
                ),
            SQLParams(  # 14
                input="select xml_id, name, fis_name from product.product where xml_id != '' order by name",
                statement="SELECT xml_id, name, fis_name FROM product.product WHERE xml_id != '' ORDER BY name",
                header=['xml_id','name','fis_name'],
                tables={'product.product': SQLTableParams(
                                                    alias='product.product',
                                                    table_name='product.product',
                                                    fields={'xml_id':'xml_id', 'name':'name', 'fis_name':'fis_name'},
                                                    query="SELECT xml_id, name, fis_name FROM product.product WHERE xml_id != ''",
                                                    )},
                where="xml_id != ''",
                orders=['name'],
                primary_table = 'product.product',
                table_by_field_alias = {'xml_id':'product.product', 'name':'product.product', 'fis_name':'product.product'},
                ),
            # SQLParams(  # 15
            #     input="select n.item, p.formula, d.item ingred from 135 n left join "
            #             "(322 p left join 323 d on d.formula_id=p.formula_id) "
            #             "on n.item_id=p.formula_id and n.item_id like '1000' "
            #             "order by n.item, p.formula desc, ingred",
            #     statement="SELECT n.item, p.formula, d.item ingred FROM 135 n LEFT JOIN "
            #             "(322 p LEFT JOIN 323 d on d.formula_id = p.formula_id) "
            #             "ON n.item_id = p.formula_id and n.item_id like '1000' "
            #             "ORDER BY n.item, p.formula DESC, ingred",
            #     header=['n.item', 'p.formula', 'ingred'],
            #     tables={
            #             'n': SQLTableParams(
            #                                     alias='n',
            #                                     table_name='135',
            #                                     fields={'item':'item', 'item_id':'item_id'},
            #                                     query="SELECT item, item_id FROM 135",
            #                                     ),
            #             'p': SQLTableParams(
            #                                     alias='p',
            #                                     table_name='322',
            #                                     fields={'formula':'formula', 'formula_id':'formula_id'},
            #                                     query="SELECT formula, formula_id FROM 322",
            #                                     ),
            #             'd': SQLTableParams(
            #                                     alias='d',
            #                                     table_name='323',
            #                                     fields={'ingred':'item', 'formula_id':'formula_id'},
            #                                     query="SELECT item as ingred, formula_id FROM 323",
            #                                     ),
            #             },
            #     joins=[
            #             Join('RIGHT JOIN', 'p', 'n.item_id = p.formula_id'),
            #             Join('LEFT JOIN', 'd', 'd.formula_id = p.formula_id'),
            #             ],
            #     where="n.item_id like '1000'",
            #     orders=['n.item','p.formula DESC','ingred'],
            #     primary_table = 'n',
            #     table_by_field_alias={'n.item':'n', 'n.item_id':'n',
            #                           'p.formula':'p', 'p.formula_id':'p',
            #                           'ingred':'d', 'd.formula_id':'d'},
            #     ),
            )

    def _test_creation(self, params):
        sql = SQL(params.input)
        # print()
        # print(sql)
        # print(params)
        # print('---')
        self.assertEqual(sql.raw_statement, params.input)
        self.assertEqual(sql.statement, params.statement)
        self.assertEqual(sql.header, params.header)
        self.assertEqual(sql.tables, params.tables)
        self.assertEqual(sql.table_by_field_alias, params.table_by_field_alias)
        self.assertEqual(sql.joins, params.joins)
        self.assertEqual(sql.where, params.where)
        self.assertEqual(sql.orders, params.orders)
        self.assertEqual(sql.to, params.to)
        self.assertEqual(sql.primary_table, params.primary_table)

    def _convert_primary_records(self, sq, table_alias):
        new_sq = sq.as_template(sq.name)
        for rec in sq:
            values = {}
            for field, value in rec.items():
                values[sq.aliases[field]] = rec[field]
            new_sq.add_record(values)
        return new_sq

    def test_iteration(self):
        expected = [
            ('I-101', 97.01),
            ('I-103', 11.99),
            ('I-106', 55.62),
            ]
        for rec, exp in zip(
                SQL("select inv_id, total from invoice where cust_id='C-001'"),
                expected,
                fillvalue=None
                ):
            self.assertEqual(rec, exp)

    def test_joins(self):
        # join
        query = SQL('select c.last, i.inv_id, i.total from customer c join invoice i on c.cust_id=i.cust_id').execute()
        expected = [
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        query = SQL('select c.last, i.inv_id, i.total from invoice i join customer c on i.cust_id=c.cust_id').execute()
        expected = [
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        # inner
        query = SQL('select c.last, i.inv_id, i.total from customer c inner join invoice i on c.cust_id=i.cust_id order by i.inv_id').execute()
        expected = [
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        query = SQL('select c.last, i.inv_id, i.total from invoice i inner join customer c on i.cust_id=c.cust_id order by i.inv_id').execute()
        expected = [
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        # full
        query = SQL('select c.last, i.inv_id, i.total from customer c full join invoice i on c.cust_id=i.cust_id order by c.last').execute()
        expected = [
                AttrDict([('c.last',EMPTY), ('i.inv_id','I-110'), ('i.total',8.97)]),
                AttrDict([('c.last','Cordosa'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Giannini'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Godshall'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last','Winchester'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','van Sebille'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        query = SQL('select c.last, i.inv_id, i.total from invoice i full join customer c on c.cust_id=i.cust_id order by c.last').execute()
        expected = [
                AttrDict([('c.last',EMPTY), ('i.inv_id','I-110'), ('i.total',8.97)]),
                AttrDict([('c.last','Cordosa'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Giannini'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Godshall'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last','Winchester'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','van Sebille'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        # outer
        query = SQL('select c.last, i.inv_id, i.total from customer c outer join invoice i on c.cust_id=i.cust_id order by c.last').execute()
        expected = [
                AttrDict([('c.last',EMPTY), ('i.inv_id','I-110'), ('i.total',8.97)]),
                AttrDict([('c.last','Cordosa'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Giannini'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Godshall'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Winchester'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','van Sebille'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        query = SQL('select c.last, i.inv_id, i.total from invoice i outer join customer c on c.cust_id=i.cust_id order by c.last').execute()
        expected = [
                AttrDict([('c.last',EMPTY), ('i.inv_id','I-110'), ('i.total',8.97)]),
                AttrDict([('c.last','Cordosa'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Giannini'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Godshall'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Winchester'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','van Sebille'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        # left
        query = SQL('select c.last, i.inv_id, i.total from customer c left join invoice i on c.cust_id=i.cust_id order by c.last').execute()
        expected = [
                AttrDict([('c.last','Cordosa'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Giannini'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Godshall'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last','Winchester'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','van Sebille'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        query = SQL('select c.last, i.inv_id, i.total from invoice i left join customer c on c.cust_id=i.cust_id order by i.inv_id').execute()
        expected = [
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last',EMPTY), ('i.inv_id','I-110'), ('i.total',8.97)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        # right
        query = SQL('select c.last, i.inv_id, i.total from customer c right join invoice i on c.cust_id=i.cust_id order by i.inv_id').execute()
        expected = [
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last',EMPTY), ('i.inv_id','I-110'), ('i.total',8.97)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        query = SQL('select c.last, i.inv_id, i.total from invoice i right join customer c on c.cust_id=i.cust_id order by c.last').execute()
        expected = [
                AttrDict([('c.last','Cordosa'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-101'), ('i.total',97.01)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-103'), ('i.total',11.99)]),
                AttrDict([('c.last','Furman'), ('i.inv_id','I-106'), ('i.total',55.62)]),
                AttrDict([('c.last','Giannini'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Godshall'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','Joleson'), ('i.inv_id','I-102'), ('i.total',133.79)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-111'), ('i.total',99.53)]),
                AttrDict([('c.last','Longsworth'), ('i.inv_id','I-113'), ('i.total',116.45)]),
                AttrDict([('c.last','Rodriguez'), ('i.inv_id','I-117'), ('i.total',0.0)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-104'), ('i.total',12.34)]),
                AttrDict([('c.last','Tolstoy'), ('i.inv_id','I-108'), ('i.total',74.08)]),
                AttrDict([('c.last','Winchester'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                AttrDict([('c.last','van Sebille'), ('i.inv_id',EMPTY), ('i.total',EMPTY)]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)
        # cross
        query = SQL('select a.side as side1, b.side as side2 from d4 as a cross join d4 as b').execute()
        expected = [
                AttrDict(side1=1, side2=1),
                AttrDict(side1=1, side2=2),
                AttrDict(side1=1, side2=3),
                AttrDict(side1=1, side2=4),
                AttrDict(side1=2, side2=1),
                AttrDict(side1=2, side2=2),
                AttrDict(side1=2, side2=3),
                AttrDict(side1=2, side2=4),
                AttrDict(side1=3, side2=1),
                AttrDict(side1=3, side2=2),
                AttrDict(side1=3, side2=3),
                AttrDict(side1=3, side2=4),
                AttrDict(side1=4, side2=1),
                AttrDict(side1=4, side2=2),
                AttrDict(side1=4, side2=3),
                AttrDict(side1=4, side2=4),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)

    def test_multiple_star(self):
        query = SQL("select * from customer c join invoice i on c.cust_id = i.cust_id").execute()
        expected = [
                AttrDict([('c.middle', 'A'), ('c.last', 'Furman'), ('c.cust_id', 'C-001'), ('c.first', 'Ethan'), ('i.total', 97.01), ('i.cust_id', 'C-001'), ('i.inv_id', 'I-101'), ('i.purch_date', '2024-01-05')]),
                AttrDict([('i.total', 11.99), ('i.cust_id', 'C-001'), ('i.inv_id', 'I-103'), ('i.purch_date', '2024-05-20'), ('c.middle', 'A'), ('c.last', 'Furman'), ('c.cust_id', 'C-001'), ('c.first', 'Ethan')]),
                AttrDict([('i.total', 55.62), ('i.cust_id', 'C-001'), ('i.inv_id', 'I-106'), ('i.purch_date', '2024-05-20'), ('c.middle', 'A'), ('c.last', 'Furman'), ('c.cust_id', 'C-001'), ('c.first', 'Ethan')]),
                AttrDict([('i.total', 133.79), ('i.cust_id', 'C-007'), ('i.inv_id', 'I-102'), ('i.purch_date', '2024-02-01'), ('c.middle', 'Dee'), ('c.last', 'Joleson'), ('c.cust_id', 'C-007'), ('c.first', 'Jonathan')]),
                AttrDict([('i.total', 99.53), ('i.cust_id', 'C-008'), ('i.inv_id', 'I-111'), ('i.purch_date', '2024-07-31'), ('c.middle', 'Mario'), ('c.last', 'Longsworth'), ('c.cust_id', 'C-008'), ('c.first', 'William')]),
                AttrDict([('i.total', 116.45), ('i.cust_id', 'C-008'), ('i.inv_id', 'I-113'), ('i.purch_date', '2024-10-12'), ('c.middle', 'Mario'), ('c.last', 'Longsworth'), ('c.cust_id', 'C-008'), ('c.first', 'William')]),
                AttrDict([('i.total', 0.0), ('i.cust_id', 'C-012'), ('i.inv_id', 'I-117'), ('i.purch_date', '2024-12-13'), ('c.middle', 'Espinosa'), ('c.last', 'Rodriguez'), ('c.cust_id', 'C-012'), ('c.first', 'Yolanda')]),
                AttrDict([('i.total', 12.34), ('i.cust_id', 'C-013'), ('i.inv_id', 'I-104'), ('i.purch_date', '2024-03-16'), ('c.middle', 'K'), ('c.last', 'Tolstoy'), ('c.cust_id', 'C-013'), ('c.first', 'Arnesto')]),
                AttrDict([('i.total', 74.08), ('i.cust_id', 'C-013'), ('i.inv_id', 'I-108'), ('i.purch_date', '2024-07-31'), ('c.middle', 'K'), ('c.last', 'Tolstoy'), ('c.cust_id', 'C-013'), ('c.first', 'Arnesto')]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)

    def test_single_star(self):
        query = SQL("select * from customer").execute()
        expected = [
                AttrDict([('middle', 'A'), ('last', 'Furman'), ('cust_id', 'C-001'), ('first', 'Ethan')]),
                AttrDict([('middle', 'B'), ('last', 'Cordosa'), ('cust_id', 'C-002'), ('first', 'Alyssa')]),
                AttrDict([('middle', 'C'), ('last', 'Godshall'), ('cust_id', 'C-004'), ('first', 'Tony')]),
                AttrDict([('middle', ''), ('last', 'van Sebille'), ('cust_id', 'C-005'), ('first', 'Emile')]),
                AttrDict([('middle', ''), ('last', 'Giannini'), ('cust_id', 'C-006'), ('first', 'Ron')]),
                AttrDict([('middle', 'Dee'), ('last', 'Joleson'), ('cust_id', 'C-007'), ('first', 'Jonathan')]),
                AttrDict([('middle', 'Mario'), ('last', 'Longsworth'), ('cust_id', 'C-008'), ('first', 'William')]),
                AttrDict([('middle', 'Nathanial'), ('last', 'Winchester'), ('cust_id', 'C-010'), ('first', 'Charlie')]),
                AttrDict([('middle', 'Espinosa'), ('last', 'Rodriguez'), ('cust_id', 'C-012'), ('first', 'Yolanda')]),
                AttrDict([('middle', 'K'), ('last', 'Tolstoy'), ('cust_id', 'C-013'), ('first', 'Arnesto')]),
                ]
        for res, exp in zip(query, expected, fillvalue=None):
            self.assertEqual(res._asdict(), exp)

    def test_statements(self):
        for i, s in enumerate(self.statements):
            try:
                self._test_creation(s)
            except Exception:
                t, e, tb = sys.exc_info()
                raise t('%s  (failed on iteration %d)' % (e, i), None, tb)

    def test_statement_errors(self):
        self.assertRaisesRegex(
                SQLError,
                'item_id',
                SQL,
                "select n.item_id item, n.wrhse_no warehouse from 135 n where item_id='006047' and wrhse_no='3000'",
                )
        self.assertRaisesRegex(
                SQLError,
                'unknown table',
                SQL,
                "select n.item_id item, n.wrhse_no warehouse from 135 n where n.item_id='006047' and p.wrhse_no='3000'",
                )
        self.assertRaisesRegex(
                SQLError,
                'no fields specified for table',
                SQL,
                "select n.item_id item, n.wrhse_no warehouse from 135 where n.item_id='006047' and p.wrhse_no='3000'",
                )


class TestMisc(TestCase):
    #
    def test_where(self):
        self.assertEqual(
                convert_where('this = 20'),
                ([('this', '=', 20)], []),
                )
        self.assertEqual(
                convert_where('this = 20', infix=True),
                ([('this', '=', 20)], []),
                )
        self.assertEqual(
                convert_where('this=20 and that="who"'),
                (['&',('this','=',20),('that','=','who')], []),
                )
        self.assertEqual(
                convert_where('this=20 and that="who"', infix=True),
                ([('this','=',20),'&',('that','=','who')], []),
                )
        self.assertEqual(
                convert_where('this=20 or these<44 and that="who"'),
                (['&','|',('this','=',20),('these','<',44),('that','=','who')], []),
                )
        self.assertEqual(
                convert_where('this=20 or these<44 and that="who"', infix=True),
                ([('this','=',20),'|',('these','<',44),'&',('that','=','who')], []),
                )


## generic test table data

Table.from_data(
        name='customer',
        fields=['cust_id','first','middle','last'],
        data=[
            dict(first='Ethan', middle='A', last='Furman', cust_id='C-001'),
            dict(first='Alyssa', middle='B', last='Cordosa', cust_id='C-002'),
            dict(first='Tony', middle='C', last='Godshall', cust_id='C-004'),
            dict(first='Emile', middle='', last='van Sebille', cust_id='C-005'),
            dict(first='Ron', middle='', last='Giannini', cust_id='C-006'),
            dict(first='Jonathan', middle='Dee', last='Joleson', cust_id='C-007'),
            dict(first='William', middle='Mario', last='Longsworth', cust_id='C-008'),
            dict(first='Charlie', middle='Nathanial', last='Winchester', cust_id='C-010'),
            dict(first='Yolanda', middle='Espinosa', last='Rodriguez', cust_id='C-012'),
            dict(first='Arnesto', middle='K', last='Tolstoy', cust_id='C-013'),
            ])

Table.from_data(
        name='address',
        fields=['cust_id','street','city','state','zip'],
        data=[
            dict(cust_id='', street='123 Main St', city='Anytown', state='AK', zip='99991'),
            dict(cust_id='C-001', street='814 Cedaroak St', city='Saint Helens', state='OR', zip='98225'),
            dict(cust_id='C-001', street='1014 S Summit Ave', city='Rosalia', state='WA', zip='99170'),
            dict(cust_id='C-003', street='456 Primary Blvd', city='Everytown', state='RI', zip='00001'),
            dict(cust_id='C-006', street='423 Salinas Rd', city='Royal Oaks', state='', zip=''),
            dict(cust_id='C-007', street='8192 Secondary Lp', city='Circlet', state='MI', zip='32166'),
            dict(cust_id='C-008', street='700 Elevenses Ln', city='Doublee', state='SD', zip='71942'),
            dict(cust_id='C-009', street='513 NE 7th Way', city='St Louis', state='OK', zip='44267'),
            dict(cust_id='C-012', street='', city='Albaqurque', state='NM', zip=''),
            dict(cust_id='C-013', street='34345 S Dickey Prairie Rd', city='', state='', zip='98123'),
            ])

Table.from_data(
        name='invoice',
        fields=['inv_id','cust_id','purch_date','total'],
        data=[
            dict(inv_id='I-101', cust_id='C-001', purch_date='2024-01-05', total=97.01),
            dict(inv_id='I-102', cust_id='C-007', purch_date='2024-02-01', total=133.79),
            dict(inv_id='I-103', cust_id='C-001', purch_date='2024-05-20', total=11.99),
            dict(inv_id='I-104', cust_id='C-013', purch_date='2024-03-16', total=12.34),
            dict(inv_id='I-106', cust_id='C-001', purch_date='2024-05-20', total=55.62),
            dict(inv_id='I-108', cust_id='C-013', purch_date='2024-07-31', total=74.08),
            dict(inv_id='I-110', cust_id='C-003', purch_date='2024-05-20', total=8.97),
            dict(inv_id='I-111', cust_id='C-008', purch_date='2024-07-31', total=99.53),
            dict(inv_id='I-113', cust_id='C-008', purch_date='2024-10-12', total=116.45),
            dict(inv_id='I-117', cust_id='C-012', purch_date='2024-12-13', total=0.00),
            ])

Table.from_data(
        name='invoice_line',
        fields=['inv_id','product_id','qty','cost','total'],
        data=[
            dict(inv_id='I-101', product_id='14FW', qty=3, cost=0.25, total=0.75),
            dict(inv_id='I-101', product_id='38LW', qty=6, cost=0.31, total=1.86),
            dict(inv_id='I-102', product_id='4BLT', qty=9, cost=0.44, total=3.96),
            dict(inv_id='I-103', product_id='248CDR', qty=11, cost=4.23, total=46.53),
            dict(inv_id='I-104', product_id='1GP', qty=2, cost=27.89, total=55.78),
            dict(inv_id='I-105', product_id='PBR', qty=1, cost=4.99, total=4.99),
            dict(inv_id='I-106', product_id='SP', qty=10, cost=0.99, total=9.90),
            dict(inv_id='I-106', product_id='DC', qty=1, cost=13.39, total=13.39),
            dict(inv_id='I-106', product_id='WAX', qty=2, cost=12.99, total=25.98),
            dict(inv_id='I-108', product_id='OIL', qty=5, cost=17.99, total=89.95),
            dict(inv_id='I-108', product_id='1GP', qty=3, cost=27.89, total=83.67),
            dict(inv_id='I-110', product_id='OIL', qty=1, cost=17.99, total=17.99),
            dict(inv_id='I-111', product_id='DC', qty=2, cost=13.39, total=26.78),
            dict(inv_id='I-113', product_id='PBR', qty=5, cost=4.99, total=24.95),
            dict(inv_id='I-117', product_id='WAX', qty=3, cost=12.99, total=38.97),
            dict(inv_id='I-117', product_id='OIL', qty=9, cost=17.99, total=161.91),
            dict(inv_id='I-117', product_id='PBR', qty=1, cost=4.99, total=4.99),
            ])

Table.from_data(
        name='product',
        fields=['product_id','desc','price'],
        data=[
            dict(desc='1/4" flat washer', product_id='14FW', price=0.25),
            dict(desc='3/8" lock washer', product_id='38LW', price=0.31),
            dict(desc='4" bolt', product_id='4BLT', price=0.44),
            dict(desc='2" x 4" x 8\' cedar', product_id='248CDR', price=4.23),
            dict(desc='1 gallon paint', product_id='1GP', price=27.89),
            dict(desc='paint brush roll', product_id='PBR', price=4.99),
            dict(desc='sand paper', product_id='SP', price=0.99),
            dict(desc='drop cloth', product_id='DC', price=13.39),
            dict(desc='wax', product_id='WAX', price=12.99),
            dict(desc='oil', product_id='OIL', price=17.99),
            ])

Table.from_data(
        name='d4',
        fields=['side'],
        data=[
            dict(side=1),
            dict(side=2),
            dict(side=3),
            dict(side=4),
            ])


