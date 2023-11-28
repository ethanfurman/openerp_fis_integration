from collections import defaultdict
from aenum import NamedTuple
from antipathy import Path
from dbf import Date, DateTime
from fnx_fs.fields import files
from scription import Execute, OrmFile, TimeoutError
from fnx import date
from fnx.oe import dynamic_page_stub
from .xid import xmlid
from openerp import SUPERUSER_ID as SU, CONFIG_DIR, ROOT_DIR
from openerp.exceptions import ERPError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, Period, self_ids, self_uid, NamedLock, get_ids
import os
from osv import osv, fields
from pandaemonium import PidLockFile, AlreadyLocked
from PIL import Image
from xaml import Xaml
import logging
import re
import threading

_logger = logging.getLogger(__name__)

OWN_STOCK = 12  # Physical Locations / Your Company / Stock

LLC_lock = threading.Lock()
LLC_backup_file = Path(ROOT_DIR)/'var/openerp/fis_integration.LabelLinkCtl.txt'
with LLC_lock:
    if not LLC_backup_file.dirs.exists():
        LLC_backup_file.dirs.mkdir()
    if not LLC_backup_file.exists():
        open(LLC_backup_file, 'w').close()
    with open(LLC_backup_file) as llc:
        LLC_text = llc.read().strip().split('\n')
LLC_OVERRIDE = Path(ROOT_DIR)/'var/openerp/fis_integration.LabelLinkCtl.override'
LLC_SOURCE = Path('/mnt/labeltime/Labels/LabelLinkCtl')
LLC_PID_FILE = Path('/opt/openerp/var/run/test_mnt_labeltime.pid')

PRODUCT_LABEL_URL = Path("https://openerp.sunridgefarms.com/fis/product/label/")
PRODUCT_LABEL_BMP_LOCATION = Path("/mnt/labeltime/Labels/")
PRODUCT_LABEL_PNG_LOCATION = Path("/PNG_labels/")
IMAGE_ALTERNATES = {'MK': 'CC', 'B': ('PKG', '')}

NamedLock = NamedLock()

class Prop65(fields.SelectionEnum):
    _order_ = 'none reproductive cancer both'
    none = 'N - free of / below trigger level'
    reproductive = 'R - can cause reproductive harm'
    cancer = 'C - can cause cancer'
    both = 'B - can cause cancer and/or reproductive harm'

class TrademarkStatus(fields.SelectionEnum):
    _order_ = 'dead dying renewing aging active'
    dead = 'Dead'
    dying = 'Almost Expired'
    renewing = 'Renewing'
    aging = 'Nearing Expiration'
    active = 'Active'

class TrademarkStatusKey(NamedTuple):
    priority = 0, 'most severe status (e.g. dying is more severe than aging)'
    state = 1, 'status of state trademark'
    federal = 2, 'status of federal trademark'
    def values(self):
        res = {}
        for i, field in enumerate(('trademark_state', 'state_trademark_state', 'federal_trademark_state')):
            if self[i] is not False:
                res[field] = self[i]
        return res

class TrademarkExpiry(NamedTuple):
    id = 0, 'record id'
    state = 1, 'trademark expiration at the state level', False
    federal = 2, 'trademark expiration at the federal level', False
    def earliest(self):
        if not self.state:
            return self.federal
        elif not self.federal:
            return self.state
        else:
            (self.state, self.federal)[self.state > self.federal]

class ForecastDetail(NamedTuple):
    produced = 0, None, 0.0
    purchased = 1, None, 0.0
    consumed = 2, None, 0.0
    sold = 3, None, 0.0

class Forecast(NamedTuple):
    item = 0, None, ''
    day_10 = 1, None, ForecastDetail()
    day_21 = 2, None, ForecastDetail()

class ProductAvailability(fields.SelectionEnum):
    _order_ = 'no yes sales'
    no =  'N', ''
    yes = 'Y', 'Customers and Sales'
    sales = 'S', 'Sales Only'

def _get_category_records(key_table, cr, uid, ids, context=None):
    if isinstance(ids, (int, long)):
        ids = [ids]
    # first, add each record in ids
    result = set(ids)
    # then add all child records
    for record in key_table.browse(cr, uid, ids, context=context):
        children = record.child_id
        while children:
            child = children.pop()
            result.add(child.id)
            children.extend(child.child_id)
    return list(result)

class product_category(xmlid, osv.Model):
    "makes external_id visible and searchable"
    _name = 'product.category'
    _inherit = 'product.category'

    _columns = {
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'fis_shelf_life': fields.float('Shelf life (mos)'),
        }


class product_available_at(xmlid, osv.Model):
    "tracks availablility options for products"
    _name = 'product.available_at'
    _description = 'Product Location'

    def _get_products(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        product = self.pool.get('product.product')
        for available in self.read(cr, uid, ids, fields=['xml_id'], context=context):
            result[available['id']] = product.search(
                    cr, uid,
                    [('fis_availability_code','=',available['xml_id'])],
                    context=context,
                    )
        return result

    _columns = {
        'name' : fields.char('Availability', size=50),
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'available': fields.selection(ProductAvailability, 'Available for resale?'),
        'product_ids' : fields.function(
            _get_products,
            relation='product.product',
            fields_id='fis_availability_code',
            type='one2many',
            string='Products',
            ),
        }


class product_template(osv.Model):
    _name = "product.template"
    _inherit = 'product.template'

    _columns = {
        'fis_name': fields.char('FIS Name', size=128, select=True),
        'warranty': fields.float("Shelf Life (mos)", digits=(16,3),),
        }


class product_product(xmlid, osv.Model):
    'Adds Available column and shipped_as columns'
    _name = 'product.product'
    _inherit = ['product.product', 'fnx_fs.fs']

    _fnxfs_path = 'product'
    _fnxfs_path_fields = ['xml_id', 'name']

    # trademark_expiry
    # trademark_state
    # trademark_renewal
    def _trademark_state(self, cr, uid, ids, field_names, arg, context=None):
        #
        # returns id_res of
        # {
        #   <id> : {
        #           'trademark_state': <value>,
        #           'state_trademark_state': <value>,
        #           'federal_trademark_state': <value>,
        #           }}
        #
        # or bulk_res of
        # {
        #   <status, status, status> : [<id>, <id>, ...]
        # }
        #
        if isinstance(ids, (int, long)):
            ids = [ids]
        id_res = defaultdict(dict)
        bulk_res = defaultdict(list)
        records = self.read(
                cr, uid, ids,
                fields=[
                    'id', 'trademark_state',
                    'state_trademark_expiry', 'state_trademark_renewal', 'state_trademark_state',
                    'federal_trademark_expiry', 'federal_trademark_renewal', 'federal_trademark_state',
                    ],
                context=context,
                )
        today = date(
                fields.date.context_today(self, cr, uid, context=context),
                DEFAULT_SERVER_DATE_FORMAT,
                )
        for rec in records:
            rec_id = rec['id']
            state_expiry = date(rec['state_trademark_expiry'], DEFAULT_SERVER_DATE_FORMAT)
            state_renewal = date(rec['state_trademark_renewal'], DEFAULT_SERVER_DATE_FORMAT)
            federal_expiry = date(rec['federal_trademark_expiry'], DEFAULT_SERVER_DATE_FORMAT)
            federal_renewal = date(rec['federal_trademark_renewal'], DEFAULT_SERVER_DATE_FORMAT)
            ts = sts = fts = False
            if state_expiry:
                expiry_gap = state_expiry - today
                if expiry_gap > Period.Week26:
                    sts = TrademarkStatus.active
                elif state_renewal and today < state_expiry and today - state_renewal < Period.Week13:
                    sts = TrademarkStatus.renewing
                elif expiry_gap > Period.Week13:
                    sts = TrademarkStatus.aging
                elif state_expiry > today:
                    sts = TrademarkStatus.dying
                else:
                    sts = TrademarkStatus.dead
            if federal_expiry:
                expiry_gap = federal_expiry - today
                if expiry_gap > Period.Week26:
                    fts = TrademarkStatus.active
                elif federal_renewal and today < federal_expiry and today - federal_renewal < Period.Week13:
                    fts = TrademarkStatus.renewing
                elif expiry_gap > Period.Week13:
                    fts = TrademarkStatus.aging
                elif federal_expiry > today:
                    fts = TrademarkStatus.dying
                else:
                    fts = TrademarkStatus.dead
            if state_expiry and federal_expiry:
                ts = min(sts, fts)
            elif state_expiry:
                ts = sts
            elif federal_expiry:
                ts = fts
            key = []
            for new_status, field in (
                    (ts, 'trademark_state'),
                    (sts, 'state_trademark_state'),
                    (fts, 'federal_trademark_state'),
                ):
                if field in field_names and new_status != rec[field]:
                    id_res[rec_id][field] = new_status
                    key.append(new_status)
                else:
                    key.append(False)
            bulk_res[TrademarkStatusKey(*key)].append(rec_id)
        if arg == 'bulk':
            return bulk_res
        else:
            return id_res

    def _trademark_expiry(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for datom in self.read(
                cr, uid, ids,
                fields=['state_trademark_expiry', 'federal_trademark_expiry'],
                context=context,
            ):
            expiry = TrademarkExpiry(
                    datom['id'],
                    datom['state_trademark_expiry'],
                    datom['federal_trademark_expiry'],
                    )
            res[expiry.id] = expiry.earliest()
        return res

    def _cost_link(self, cr, uid, ids, field_name, arg, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        result = {}
        htmlContentList = [ ]
        for id in ids:
            htmlContentList.append('''
                    <div id="cost_content"></div>
                    <script type="text/javascript">
                        ajaxpage('http://labeltime:9000/costing/','cost_content');
                    </script>
                    ''')
            result[id] = dynamic_page_stub % "".join(htmlContentList)
        return result

    def _get_orderable(self, cr, uid, ids, field_name, arg, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if user.has_group('base.group_sale_salesman'):
            target = [ProductAvailability.yes.db, ProductAvailability.sales.db]
        elif user.has_group('portal.group_portal'):
            target = [ProductAvailability.yes.db, ]
        aa_codes = [
                aa['xml_id']
                for aa in self.pool
                        .get('product.available_at')
                        .read(cr, uid, [('available','in',target)], fields=['xml_id'], context=context)
                ]
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}.fromkeys(ids, False)
        for rec in self.read(cr, uid, ids, fields=['fis_availability_code'], context=context):
            if rec['fis_availability_code'] in aa_codes:
                res[rec['id']] = True
        return res

    def _search_orderable(self, cr, uid, obj, name, criterion, context=None):
        # return ids that are orderable by the current user
        # current user is either a salesperson or a portal customer
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if user.has_group('base.group_sale_salesman'):
            target = [ProductAvailability.yes.db, ProductAvailability.sales.db]
        elif user.has_group('portal.group_portal'):
            target = [ProductAvailability.yes.db, ]
        aa_codes = [
                aa['xml_id']
                for aa in self.pool
                        .get('product.available_at')
                        .read(cr, uid, [('available','in',target)], fields=['xml_id'], context=context)
                ]
        if criterion[0][1:] in [('=',True),('!=',False)]:
            op = 'in'
        elif criterion[0][1:] in [('=',False),('!=',True)]:
            op = 'not in'
        else:
            _logger.error('unknown domain: %r', criterion)
            return []
        ids = self.search(cr, uid, [('fis_availability_code',op,aa_codes)], context=context)
        return [('id','in',ids)]

    def _label_links(self, cr, uid, ids, field_name, arg, context=None):
        xml_ids = self.get_xml_id_map(cr, uid, module='F135', ids=ids, context=context)
        result = {}.fromkeys(ids)
        try:
            LabelLinks, use_cache = get_LLC()
        except Exception:
            _logger.exception('error fetching/processing LabelLinkCtl')
            # use the hard-coded display links
            LabelLinks = (
                ("1","%sB.bmp","left"),
                ("1","%sNI.bmp","right"),
                ("2","%sMK.bmp","center"),
                )
        # group images by rows
        for xml_id, id in xml_ids.items():
            raw_rows = defaultdict(list)
            for row, link, align, width in LabelLinks:
                header = False
                link = Path(link)
                if link.count('%s') == 1:
                    link %= '%s/%s' % (xml_id, xml_id)
                    ts_link = add_timestamp(link, use_cache)
                    if ts_link is None:
                        continue
                    remote_link = PRODUCT_LABEL_URL + ts_link
                elif link.count('%s') == 0:
                    header = 'oe_header'
                    ts_link = add_timestamp(link, use_cache)
                    if ts_link is None:
                        continue
                    remote_link = PRODUCT_LABEL_URL + ts_link
                else:
                    _logger.error('unknown link template: %r', link)
                    continue
                raw_rows[int(row)].append((link, remote_link, align, width, header))
            width_rows = calc_width(raw_rows)
            doc = Xaml(LabelLinkTab).document.pages[0]
            tab = doc.string(rows = width_rows)
            result[id] = tab
        return result

    def _get_availability_codes(self, cr, uid, context=None):
        available_at = self.pool.get('product.available_at')
        records = available_at.read(cr, uid, [('id','!=',0)], fields=['xml_id','name'], context=context)
        result = [(r['xml_id'], '%s - %s' % (r['xml_id'], r['name'])) for r in records]
        return result

    _columns = {
        # overridden openerp fields
        'lst_price' : fields.float(
            string='FIS "A" Price',
            digits=(15,3),
            help='per-case price',
            ),
        'price': fields.float(
            string='Unit Price',
            digits=(15,3),
            help='FIS per-unit price',
            ),
        # added fields
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'fis_shipping_size': fields.char('Shipped as', size=50, oldname='shipped_as'),
        'fis_availability_code': fields.selection(
            _get_availability_codes,
            'Availability',
            oldname='fis_availability_id',
            ),
        'spcl_ship_instr': fields.text('Special Shipping Instructions'),
        'fis_location': fields.char('Location', size=6),
        'fis_qty_on_hand': fields.float(
            string='Quantity On Hand',
            help="Current quantity of products according to FIS.",
            oldname='qty_available',
            ),
        'fis_qty_makeable': fields.float(
            string='Immediately Producible',
            digits=(15,3),
            help="How much can be made with current inventory.",
            ),
        'label_server_stub': fields.function(
            _label_links,
            string='Current Labels',
            type='html',
            method=True,
            ),
        'cost_server_stub': fields.function(
            _cost_link,
            string='Item Costs',
            type='html',
            method=True,
            ),
        # 'cost_customer': fields.function(
        #     lambda *a: {},
        #     string="Customer to check costs for",
        #     type='many2one',
        #     method=False,
        #     readonly=True,
        #     ),
        'label_text': fields.text('Label Text'),
        'docs': fields.html('Documents'),
        'trademarks': fields.char(string='Trademark', size=2, oldname='trademark'),
        'trademark_expiry': fields.function(
            _trademark_expiry,
            type='date',
            string='Expiration date',
            store={
                'product.product': (
                    lambda s, c, u, ids, ctx=None: ids,
                    ['state_trademark_expiry', 'federal_trademark_expiry'],
                    10,
                    ),
                },
            ),
        'trademark_state': fields.function(
            _trademark_state,
            fnct_inv=True,
            multi='trademark',
            type='selection',
            string='Trademark status',
            selection = TrademarkStatus,
            store={
                'product.product': (
                    lambda table, cr, uid, ids, ctx: ids,
                    [   'state_trademark_expiry', 'state_trademark_renewal',
                        'federal_trademark_expiry', 'federal_trademark_renewal',
                        ],
                    10,
                )},
            ),
        'state_trademark': fields.char('State Trademark', size=128),
        'state_trademark_no': fields.char('State Registration #', size=128),
        'state_trademark_class_ids': fields.many2many(
                'fis_integration.trademark.class',
                'product_trademark_class_rel', 'product_id', 'class_id',
                string='State Trademark Class',
                old_name='state_trademark_class',
                ),
        'state_trademark_expiry': fields.date('State Trademark expires', oldname='trademark_expiry_year'),
        'state_trademark_renewal': fields.date('State Trademark renewal submitted', oldname='trademark_renewal_date'),
        'state_trademark_state': fields.function(
            _trademark_state,
            fnct_inv=True,
            multi='trademark',
            type='selection',
            string='State Trademark Status',
            selection = TrademarkStatus,
            store={
                'product.product': (
                    lambda table, cr, uid, ids, ctx: ids,
                    ['state_trademark_expiry', 'state_trademark_renewal'],
                    10,
                )},
            oldname='trademark_state',
            ),
        'federal_trademark': fields.char('Federal Registration', size=128),
        'federal_trademark_no': fields.char('Federal Registration #', size=128),
        'federal_trademark_expiry': fields.date('Federal Registration expires'),
        'federal_trademark_renewal': fields.date('Federal Registration renewal submitted'),
        'federal_trademark_state': fields.function(
            _trademark_state,
            fnct_inv=True,
            multi='trademark',
            type='selection',
            string='Federal Registration status',
            selection = TrademarkStatus,
            store={
                'product.product': (
                    lambda table, cr, uid, ids, ctx: ids,
                    ['federal_trademark_expiry', 'federal_trademark_renewal'],
                    10,
                )},
            ),
        'fis_qty_produced': fields.float(
            string='Quantity Produced Today',
            ),
        'fis_qty_consumed': fields.float(
            string='Quantity Used Today',
            ),
        'fis_qty_purchased': fields.float(
            string='Quantity Received Today',
            ),
        'fis_qty_sold': fields.float(
            string='Quantity Sold today',
            ),
        'fis_qty_available': fields.float(
            string='Quantity Available Today',
            oldname='virtual_available',
            ),
        'fis_10_day_produced': fields.float(
            string='10-day Production',
            help="Qty produced in the next 10 days.",
            oldname='incoming_qty',
            ),
        'fis_10_day_consumed': fields.float(
            string='10-day Consumption',
            help="Qty consumed in the next 10 days.",
            oldname='outgoing_qty',
            ),
        'fis_10_day_purchased': fields.float(
            string='10-day Purchases',
            help='Qty purchased in the next 10 days.',
            oldname='makeable_qty',
            ),
        'fis_10_day_sold': fields.float(
            string='10-day Sales',
            help="Qty sold in the next 10 days.",
            oldname='nf_incoming_qty',
            ),
        'fis_10_day_available': fields.float(
            string='10-day Available',
            help='Qty available in the next 10 days',
            ),
        'fis_21_day_produced': fields.float(
            string='21-day Production',
            help="Qty produced in the next 21 days.",
            oldname='nf_outgoing_qty',
            ),
        'fis_21_day_consumed': fields.float(
            string='21-day Consumption',
            help="Qty consumed in the next 21 days.",
            oldname='nf_qty_available',
            ),
        'fis_21_day_purchased': fields.float(
            string='21-day Purchases',
            help='Qty purchased in the next 21 days.',
            ),
        'fis_21_day_sold': fields.float(
            string='21-day Sales',
            help="Qty sold in the next 21 days.",
            oldname='imm_available',
            ),
        'fis_21_day_available': fields.float(
            string='21-day Available',
            help='Qty available in the next 21 days',
            ),
        'fis_web_active': fields.boolean('Active on Web'),
        'fis_web_ingredients': fields.text('Ingredients (Web)'),
        'fis_web_tagline': fields.text('Tagline (Web)'),
        'fis_web_prep_instructions': fields.text('Preparation (Web)'),
        'fis_web_keywords': fields.many2many(
                'fis.product.keywords',
                'fis_product_web_keyword_rel', 'keyword_id', 'product_id',
                string='Keywords',
                ),
        'fnxfs_files': files('general', string='Available Files'),
        'prop65': fields.selection(Prop65, string='Req. Prop 65 warning'),
        'prop65_info': fields.text('Addl. Prop 65 info'),
        'fis_product_orderable': fields.function(
            _get_orderable,
            fnct_search=_search_orderable,
            string='Orderable',
            type='boolean',
            ),
        }

    _defaults = {
            'sale_ok': False,
            }

    def update_trademark_state(self, cr, uid, ids=None, arg=None, context=None):
        if ids is None:
            ids = self.search(cr, uid, [('trademarks','!=',False)], context=context)
        res = self._trademark_state(
                cr, uid, ids,
                field_names=['trademark_state','state_trademark_state','federal_trademark_state'],
                arg='bulk',
                context=context,
                )
        # res = {days_left: [ids], ...}
        for states, ids in res.items():
            # states is a TrademarkStatusKey, and values() will give us the needed update dictionary
            values = states.values()
            if values:
                success = self.write(cr, uid, ids, values, context=context)
                if not success:
                    return success
        return True

    def onchange_trademark(self, cr, uid, ids, trademark, expiry, renewal, field, context=None):
        today = date(fields.date.context_today(self, cr, uid, context=context))
        result = {}
        result['value'] = values = {}
        if not expiry:
            values[field] = TrademarkStatus.dead
        else:
            expiry = date(expiry)
            renewal = date(renewal)
            expiry_gap = expiry - today
            if expiry_gap > Period.Week26:
                sts = TrademarkStatus.active
            elif renewal and today < expiry and today - renewal < Period.Week13:
                sts = TrademarkStatus.renewing
            elif expiry_gap > Period.Week13:
                sts = TrademarkStatus.aging
            elif expiry > today:
                sts = TrademarkStatus.dying
            else:
                sts = TrademarkStatus.dead
            values[field] = sts
        return result

    def fnxfs_folder_name(self, records):
        "return name of folder to hold related files"
        res = {}
        for record in records:
            res[record['id']] = record['xml_id'] or ("%s-%d" % (record['name'], record['id']))
        return res

    def _get_descriptions(self):
        res = {}
        config = OrmFile(Path(CONFIG_DIR)/'fnx.ini', section='openerp')
        job = Execute(
                'sudo ssh %(host)s cat %(file)s' % {
                    'host': config.full_description_host,
                    'file': config.full_description_path,
                    },
                pty=True,
                password=config.pw,
                )
        text = job.stdout.split('\n')
        for line in text:
            match = re.match('(.{40})  \((\d{6})\)  (.*)$', line)
            if match is None:
                continue
            fis_desc, item_code, full_desc = match.groups()
            res[item_code] = full_desc
        return res


    def _get_forecast_quantities(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, [('id','!=',0)], fields=['id', 'xml_id', 'module'], context=context)
        res = dict([(d['xml_id'], None) for d in data if (d['id'] and d['module'] == 'F135')])
        job = Execute('/usr/local/bin/fis-query forecast --all')
        if job.stderr or job.returncode:
            raise ERPError('job failed', job.stderr or 'unknown cause (returncode: %d)' % job.returncode)
        for line in job.stdout.split('\n'):
            if not line.strip():
                continue
            try:
                line = line.split(' - ')[1]
            except IndexError:
                _logger.error('problem with forecast line: %r', repr(line))
                raise
            if 'ERROR' in line:
                continue
            item_code, _10_day, _21_day = line.split(':')
            if item_code not in res:
                continue
            prod_in, purch, prod_out, sold = _10_day.split()[2:6]
            prod_in = float(prod_in)
            purch = float(purch)
            prod_out = -(float(prod_out))
            sold = -(float(sold))
            _10_day = ForecastDetail(prod_in, purch, prod_out, sold)
            prod_in, purch, prod_out, sold = _21_day.split()[2:6]
            prod_in = float(prod_in)
            purch = float(purch)
            prod_out = -(float(prod_out))
            sold = -(float(sold))
            _21_day = ForecastDetail(prod_in, purch, prod_out, sold)
            res[item_code] = Forecast(item_code, _10_day, _21_day)
        return res

class production_line(xmlid, osv.Model):
    "production line"
    _name = 'fis_integration.production_line'
    _order = 'name'

    def _get_name(self, cr, uid, ids, field_name, args, context=None):
        values = {}
        for id in ids:
            current = self.browse(cr, uid, id, context=context)
            values[id] = '%s - %s' % (current.xml_id, current.desc)
        return values

    _columns = {
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'desc': fields.char('Description', size=30),
        'name': fields.function(
            _get_name,
            arg=(),
            string='Name',
            type='char',
            method=True,
            store={
                'fis_integration.production_line': (lambda s, c, u, ids, ctx: ids, ['desc'], 20),
                }
            ),
        }


class product_traffic(osv.Model):
    _name = 'fis_integration.product_traffic'
    _description = 'low product'
    _order = 'date desc'
    _inherit = ['mail.thread']
    _mirrors = {'product_id': ['description', 'categ_id']}

    def _check_already_open(self, cr, uid, ids):
        products = set()
        for rec in self.browse(cr, SU, [None]):
            if rec.state in (False, 'done'):
                continue
            if rec.product_id in products:
                return False
            products.add(rec.product_id)
        return True

    def _delete_stale_entries(self, cr, uid, arg=None, context=None):
        'zombifies entries that have been in the seen state for longer than 20 days'
        today = Date.today()
        cart = []
        for rec in self.browse(cr, uid, context=context):
            if (
                rec.purchase_comment_date and
                ((today - Date(rec.purchase_comment_date)).days > 20)
                ):
                cart.append(rec.id)
        if cart:
            self.write(cr, uid, cart, {'state': False}, context=context)
        return True

    _columns = {
        'date': fields.date('Date Created'),
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'sales_comment': fields.selection(
            (('low', 'getting low'), ('out', 'sold out')),
            'Sales Comment',
            track_visibility='change_only',
            ),
        'purchase_comment': fields.text('Purchase Comment', track_visibility='change_only'),
        'state': fields.selection(
            (('new','New'), ('seen', 'Seen'), ('ordered','On Order'), ('done', 'Received')),
            'Status',
            track_visibility='change_only',
            ),
        'purchase_comment_available': fields.selection(
            (('no',''), ('yes','Yes')),
            'Purchasing comment available?',
            ),
        'purchase_comment_date': fields.date('Purchasing updated'),
        }

    _defaults = {
        'date': lambda s, c, u, ctx=None: fields.date.today(s, c),
        'state': lambda *a: 'new'
        }

    _constraints = [
        (lambda s, *a: s._check_already_open(*a), '\nOpen item already exists', ['product_id']),
        ]

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        ctx['mail_track_initial'] = True
        if values.get('purchase_comment'):
            values['purchase_comment_available'] = 'yes'
            values['purchase_comment_date'] = fields.date.today(self, cr)
            values['state'] = 'seen'
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        follower_ids = [u.id for u in user.company_id.traffic_followers_ids]
        if follower_ids:
            values['message_follower_user_ids'] = follower_ids
        return super(product_traffic, self).create(cr, uid, values, context=ctx)

    def mark_as(self, cr, uid, ids, state, context=None):
        return self.write(cr, uid, ids, {'state': state}, context=context)

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record.id, record.product_id.name))
        return res

    def write(self, cr, uid, ids, values, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        if ('purchase_comment' in values or 'state' in values) and ids:
            pc = values.get('purchase_comment')
            s = values.get('state')
            for rec in self.browse(cr, uid, ids, context=context):
                vals = values.copy()
                if pc is not None:
                    if pc:
                        vals['purchase_comment_available'] = 'yes'
                        vals['purchase_comment_date'] = fields.date.today(self, cr)
                        if rec.state == 'new':
                            vals['state'] = 'seen'
                    else:
                        vals['purchase_comment_available'] = 'no'
                        vals['purchase_comment_date'] = False
                        if rec.state == 'seen':
                            vals['state'] = 'new'
                if s not in (None, 'new', 'seen'):
                    vals['purchase_comment_date'] = fields.date.today(self, cr)
                if not super(product_traffic, self).write(cr, uid, rec.id, vals, context=context):
                    return False
            return True
        return super(product_traffic, self).write(cr, uid, ids, values, context=context)


class product_trademark_class(osv.Model):
    _name = 'fis_integration.trademark.class'
    _description = 'State trademark class'
    _order = 'number'
    _rec_name = 'name'

    def _calc_name(self, cr, uid, ids, field_name=None, arg=None, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}
        if not ids or field_name != 'name':
            return res
        for rec in self.read(cr, uid, ids, fields=['number','category'], context=context):
            res[rec['id']] = '%s: %s' % (rec['number'], rec['category'])
        return res

    _columns = {
        'name': fields.function(
            _calc_name,
            type='char',
            size=64,
            store={
                'fis_integration.trademark.class':
                        (lambda s, c, u, ids, ctx=None: ids, ['number','category'], 10),
                        }),
        'number': fields.integer('Number', size=12, required=True),
        'category': fields.char('Category', size=64, required=True),
        'description': fields.text('Class description', required=True, oldname='name'),
        }


class product_fis2customer(osv.Model):
    _name = 'fis_integration.customer_product_cross_reference'
    _description = 'fis product code to customer product code (F262)'
    _rec_name = 'complete_name'

    def _calc_name(self, cr, uid, ids, field, unknown_none, context=None):
        res = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        product = self.pool.get('product.product')
        cross_refs = self.read(
                cr, uid, ids,
                fields=['id','customer_product_code','fis_product_id','fis_code','fis_product_size'],
                context=context,
                )
        product_ids = [d['fis_product_id'][0] for d in cross_refs if d['fis_product_id']]
        if not product_ids:
            return res
        products = dict([
            (p['xml_id'], p)
            for p in product.read(
                cr, uid, product_ids,
                fields=['id','xml_id','name','fis_shipping_size'],
                context=context,
                )])
        for ref in cross_refs:
            res[ref['id']] = ('[%s] %s - %s' % (
                    ref['customer_product_code'],
                    products[ref['fis_code']]['name'],
                    products[ref['fis_code']]['fis_shipping_size'],
                    )).strip(' -')
        return res

    def _get_product_dependent_ids(product_product, cr, uid, ids, context=None):
        self = product_product.pool.get('fis_integration.customer_product_cross_reference')
        self_ids = self.search(cr, uid, [('fis_product_id','in',ids)], context=context)
        return self_ids

    _columns = {
        'complete_name': fields.function(
            _calc_name,
            string='Name',
            type='char',
            size=512,
            store={
                'fis_integration.customer_product_cross_reference':
                    (self_ids, ['customer_product_code'], 10),
                'product.product':
                    (_get_product_dependent_ids, ['name','fis_shipping_size'], 10),
                    },
            ),
        'key': fields.char('Key', size=13, help='used to sync with external source'),
        'list_code': fields.char('List', size=6),
        'fis_code': fields.char('FIS product code', size=6),
        'partner_id': fields.many2one('res.partner', 'Customer'),
        'fis_product_id': fields.many2one('product.product', 'Product'),
        'fis_product_size': fields.related(
            'fis_product_id','fis_shipping_size',
            string='Sold per',
            type='char',
            size=50,
            ),
        'fis_product_orderable': fields.related(
            'fis_product_id','fis_product_orderable',
            string='Orderable by',
            type='boolean',
            ),
        'customer_product_code': fields.char('Code', size=15),
        'source': fields.selection((
            ('fis', 'FIS'), ('salesinq', 'SalesInq'),
            ),
            string='Data Source',
            order='definition',
            ),
        }

    # def unlink(self, cr, uid, ids, context=None):
    #     raise ERPError('illegal operation','deleting fis_integration.customer_product_cross_reference records is not supported')


class product_online_order(osv.Model):
    _name = 'fis_integration.online_order'

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer'),
        'partner_xml_id': fields.char('FIS ID', size=11),
        'user_id': fields.many2one('res.users', 'Order placed by',),
        'partner_crossref_list': fields.related(
            'user_id','fis_product_cross_ref_code',
            string='Cross-reference list',
            type='char',
            size=6,
            ),
        'transmitter_id': fields.many2one('fis.transmitter_code', 'Transmitter #'),
        'transmitter_no': fields.char('Transmitter #', size=6),
        'item_ids': fields.one2many(
            'fis_integration.online_order_item', 'order_id',
            string='Items',
            ),
        'new_item_ids': fields.one2many(
            'fis_integration.online_order_item', 'order_id',
            string='Items',
            ),
        'show_req_ship_date': fields.related(
            'user_id','fis_online_order_show_req_ship_date',
            type='boolean',
            string='Show Requested Ship Date',
            ),
        'req_ship_date': fields.date('Requested Ship Date'),
        'show_po_number': fields.related(
            'user_id', 'fis_online_order_show_po_number',
            type='boolean',
            string='Show PO #',
            ),
        'po_number': fields.char('PO #', size=10),
        'portal_customer': fields.boolean('Portal customer order', help='False if order placed by sales person'),
        'restricted': fields.boolean('Restricted Ordering'),
        }

    _defaults = {
        'user_id': self_uid,
        }

    def create(self, cr, uid, vals, context=None):
        # the partner_id passed in is the record to use as the ship-to record; this will usually be an
        #   F34 record, but can be an F33 record when a different ship-to address does not exist; it
        #   has been set either by `onload` or by `button_place_order_by_salesperson`
        # transmitter_id
        user, user_type = self.user_and_type(cr, uid, context=context)
        if user_type not in ('sales', 'portal'):
            # we shouldn't get here, as a user who is not a sales person nor
            # a portal customer should not be able to:
            # - login to the portal
            # - see a customer record
            raise ERPError(
                    'System Error',
                    'please notify tech support',
                    )
        item_ids = vals.get('item_ids', [])
        item_ids.extend(vals.get('new_item_ids', []))
        valid_item_ids = []
        for instruction in item_ids:
            if instruction[0] == 0:
                valid_item_ids.append(instruction)
        vals['item_ids'] = valid_item_ids
        vals.pop('new_item_ids', None)
        if not valid_item_ids:
            raise ERPError(
                    'Missing Items',
                    'no items listed',
                    )
        transmitter = self.pool.get('fis.transmitter_code').browse(cr, SU, vals['transmitter_id'])
        lines = ['%s-%s' % (vals['partner_xml_id'], transmitter.transmitter_no)]
        po_number = vals.get('po_number')
        req_ship_date = vals.get('req_ship_date')
        if po_number:
            po_number = ('0000000000' + po_number)[-10:]
            lines.append('PON-%s' % (po_number, ))
        if req_ship_date:
            yy, mm, dd = req_ship_date[2:].split('-')
            lines.append('RSD-%s%s%s' % (mm, dd, yy))
        # {
        #   'req_ship_date': False,
        #   'valid_item_ids': [
        #           [0, False, {
        #                   'product_desc': 'Almonds - Dry Roasted & Lightly Salted SunRidge NonGMO Verified',
        #                   'order_id': 5874L,
        #                   'partner_product_id': 241355,
        #                   'partner_product_code': '70184',
        #                   'product_fis_id': '001042',
        #                   'partner_list_code': 'HE447',
        #                   'quantity': 1,
        #                   }],
        #           [0, False, ...],
        #           ],
        #   'partner_crossref_list': 'HE447',
        #   'po_number': False,
        #   'show_req_ship_date': False,
        #   'show_po_number': False,
        #   'partner_id': 47170,
        #   },
        #
        for command, _, item in valid_item_ids:
            lines.append('%s - %s' % (
                item['product_fis_id'],
                item['quantity'],
                ))
        filename = '/home/openerp/sandbox/openerp/var/fis_integration/orders/%s' % vals['partner_id']
        with open_next_file(filename) as f:
            f.write('\n'.join(lines))
            f.write('\n')
        new_id = super(product_online_order, self).create(cr, uid, vals, context=context)
        filename = '/home/openerp/sandbox/openerp/var/fis_integration/orders/%s.txt' % new_id
        Path(f.name).move(filename)
        return new_id

    def onchange_transmitter_id(self, cr, uid, ids, transmitter_id, context=None):
        transmitter = self.pool.get('fis.transmitter_code').browse(cr, SU, transmitter_id, context=context)
        return {'value': {'transmitter_no': transmitter.transmitter_no}}

    def onload(self, cr, uid, ids, partner_id, context=None):
        """
        make changes solely on the user id and (possibly) the partner id

        context will always be None, so determine actions on whether:
        - the user has the Portal access bit
        - the user has the Salesperson access bit
        - the user has neither
        """
        res = {'value': {}}
        user, user_type = self.user_and_type(cr, uid, context=context)
        if user_type == 'sales':
            # by leaving res empty, the defaults from res.partner.button_place_order_by_salesperson
            # will not be overridden
            ship_to = self.pool.get('res.partner').browse(cr, SU, partner_id, context=context)
            transmitter_ids = get_ids(ship_to,'fis_transmitter_ids')
            res['domain'] = {
                    'transmitter_id': [('id','in',transmitter_ids)],
                    }
        elif user_type == 'portal':
            cr.execute("""
                    SELECT DISTINCT list_code
                    FROM fis_integration_customer_product_cross_reference
                    WHERE source='fis'
                    """)
            restricted_accounts = [t[0] for t in cr.fetchall()]
            fis_partner = user.fis_partner_id
            if fis_partner and user.fis_product_cross_ref_code:
                res['value']['partner_id'] = fis_partner.id
                res['value']['partner_xml_id'] = fis_partner.xml_id
                res['value']['partner_crossref_list'] = user.fis_product_cross_ref_code
                res['value']['show_req_ship_date'] = user.fis_online_order_show_req_ship_date
                res['value']['show_po_number'] = user.fis_online_order_show_po_number
                res['value']['transmitter_id'] = user.fis_transmitter_id.id
                res['value']['transmitter_no'] = user.fis_transmitter_id.transmitter_no
                res['value']['portal_customer'] = True
                res['value']['restricted'] = user.fis_product_cross_ref_code in restricted_accounts
            else:
                res['value']['partner_id'] = False
                res['value']['partner_crossref_list'] = False
                res['warning'] = {
                        'title': 'Invalid setup',
                        'message': 'This account has not been set up for orders',
                        }
        else:
            # we shouldn't get here, as a user who is not a sales person nor
            # a portal customer should not be able to:
            # - login to the portal
            # - see a customer record
            res['value']['partner_id'] = False
            res['value']['partner_crossref_list'] = False
            res['warning'] = {
                    'title': 'Access Denied',
                    'message': 'You do not have permission to place orders.',
                    }
        return res

    def user_and_type(self, cr, uid, context=None):
        res_users = self.pool.get('res.users')
        user = res_users.browse(cr, SU, uid, context=context)
        if user.has_group('base.group_sale_salesman'):
            type = 'sales'
        elif user.has_group('portal.group_portal'):
            type = 'portal'
        else:
            type = 'other'
        return user, type

    def button_place_order(self, cr, uid, ids, context=None):
        _, user_type = self.user_and_type(cr, uid, context=context)
        if user_type == 'portal':
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                'params': {'wait': True},
                }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'history_back',
                }


class product_online_orders_item(osv.Model):
    _name = 'fis_integration.online_order_item'
    _rec_name = 'product_fis_id'

    _columns = {
        'order_id': fields.many2one(
            'fis_integration.online_order',
            string='Order ID',
            ),
        'partner_product_id': fields.many2one(
            'fis_integration.customer_product_cross_reference',
            string='Product',
            ),
        'partner_list_code': fields.related(
            'partner_product_id', 'list_code',
            string='List',
            type='char',
            size=6,
            ),
        'partner_product_code': fields.char('Customer product code', size=6),
        'quantity': fields.integer('Quantity'),
        'product_desc': fields.char('Item', size=128),
        'product_fis_id': fields.char('FIS ID', size=6),
        }

    def onchange_product(
            self, cr, uid, ids,
            partner_product_id, partner_list_code, item_type,
            context=None,
        ):
        """
        updates hidden fields with product information and ensures separate old vs new items
        """
        if not partner_product_id:
            return {
                'value': {
                        'partner_product_code': False,
                        'product_desc': False,
                        'product_fis_id': False,
                        }
                    }
        #
        cross_ref = self.pool.get('fis_integration.customer_product_cross_reference')
        product = cross_ref.browse(cr, uid, partner_product_id, context=context)
        value = {
                'partner_product_code': product.customer_product_code,
                'product_desc': product.fis_product_id.name,
                'product_fis_id': product.fis_code,
                }
        return {'value': value}


class product_keywords(osv.Model):
    _name = 'fis.product.keywords'

    _columns = {
        'name': fields.char('Keyword', size=64),
        'product_ids': fields.many2many(
            'product.product',
            'fis_product_web_keyword_rel', 'product_id', 'keyword_id',
            string='Products',
            ),
        }

def get_LLC():
    "retrieve LLC file and update local cache"
    # if TEST_LLC is set, use testing copy below
    global LLC_text
    llc_override = False
    use_cache = False
    label_link_lines = LLC_text     # default
    if LLC_OVERRIDE.exists():
        llc_override = True
        with open(LLC_OVERRIDE) as llc:
            label_link_lines = llc.read().strip().split('\n')
    elif LLC_PID_FILE.exists():
        use_cache = True
    else:
        # attempt to get LabelLinkCtl from labeltime
        try:
            with PidLockFile(LLC_PID_FILE, timeout=1):
                cat = Execute('cat %s' % LLC_SOURCE, timeout=10)
            if not cat.returncode:
                label_link_lines = cat.stdout.strip().split('\n')
            else:
                _logger.warning('attempt to read %r failed with %r and %r',
                        LLC_SOURCE,
                        cat.returncode,
                        cat.stderr and cat.stderr.strip().split('\n')[-1] or 'unknown',
                        )
        except (AlreadyLocked, TimeoutError):
            use_cache = True
        except Exception:
            _logger.exception('failed to read %r', LLC_SOURCE)
    # validate LabelLinkCtl file
    LabelLinks = []
    for link_line in label_link_lines:
        pieces = [piece.strip() for piece in link_line.split(",")]
        pieces = (pieces + [None])[:4]
        if pieces[-1] is not None:
            try:
                pieces[-1] = int(pieces[-1].strip('%'))
            except ValueError:
                _logger.error('unable to convert width of %r in %r', pieces[-1], link_line)
                pieces[-1] = None
        link = pieces[0].replace('Plone/LabelDirectory/', '')
        if link.count('%s') == 2:
            # abort with exception if this fails
            link % ('a', 'test')
            if link.startswith('%s/'):
                link = link[3:]
        pieces[0] = link
        LabelLinks.append(pieces)
    if label_link_lines != LLC_text and not llc_override:
        # store current lines at module level
        LLC_text = label_link_lines
        # then attempt to update cached file
        if LLC_lock.acquire(False):
            try:
                with open(LLC_backup_file, 'w') as llc:
                    llc.write('\n'.join(label_link_lines))
            except:
                _logger.exception('failed to update LabelLinkCtl cached file')
            LLC_lock.release()
    _logger.warning('get_LLC --> %r', (LabelLinks, use_cache))
    return LabelLinks, use_cache

def add_timestamp(file, use_cache):
    "adds timestamp to filename portion of file"
    src_file = Path(file)
    possibles = [src_file]
    last_suffix = src_file.stem[6:]
    target_png_file = PRODUCT_LABEL_PNG_LOCATION / src_file.stem + '.png'
    tgt_ts = target_png_file.exists() and target_png_file.stat().st_mtime or None
    for key, value in IMAGE_ALTERNATES.items():
        if src_file.base.upper().endswith(key):
            if isinstance(value, basestring):
                value = (value, )
            for new_suffix in value:
                src_file = src_file.dirname / re.sub(last_suffix+'$', new_suffix, src_file.base) + src_file.ext
                possibles.append(src_file)
                last_suffix = new_suffix
            break
    with NamedLock(target_png_file):
        timestamp = None
        for src_file in possibles:
            if use_cache:
                _logger.debug('using cache, aborting search')
                # this can only happen the first time through
                break
            target_bmp_file = PRODUCT_LABEL_BMP_LOCATION / src_file
            if target_bmp_file.exists() and target_bmp_file.isfile() and target_bmp_file.stat().st_size:
                src_ts = target_bmp_file.stat().st_mtime
                if not tgt_ts or tgt_ts < src_ts:
                    try:
                        copy_image(target_bmp_file, target_png_file)
                    except Exception:
                        _logger.exception('failure converting %r to %r', target_bmp_file, target_png_file)
                        if target_png_file.exists():
                            target_png_file.unlink()
                        continue
                    try:
                        if not target_png_file.stat().st_size:
                            target_png_file.unlink()
                            continue
                        target_png_file.chmod(0o666)
                        target_png_file.touch(reference=target_bmp_file)
                    except Exception:
                        _logger.exception('unable to update permissions/timestamp for %s' % target_png_file)
                timestamp = '-' + DateTime.fromtimestamp(src_ts).strftime('%Y-%m-%dT%H:%M:%S')
                break
        if timestamp is None:
            if tgt_ts is None:
                return None
            timestamp = '-' + DateTime.fromtimestamp(tgt_ts).strftime('%Y-%m-%dT%H:%M:%S')
        ts_file = target_png_file.stem + timestamp + '.png'
        return ts_file

def copy_image(source, target):
    # img = Image.open(target_bmp_file).save(target_png_file)
    img = Image.open(source)
    #
    if img.format == 'BMP' and len(img.getbands()) == 1:
        # remove empty space at bottom of label
        width, height = img.size
        l, t, r, b = img.getbbox(img.crop(box=(0, 0, width, height-10)))
        if b < height-36:   # save at least 1/2"
            img = img.crop(box=(0, 0, width, b))
    #
    img.save(target)

def calc_width(src_rows):
    "return tuple of rows (target, width, align, header)"
    # incoming -> {row #: [(link, remote_link, align, header), (l, r, a), ...]}
    res = []
    for seq, images in sorted(src_rows.items()):
        row = []
        # images are either 2x4 or 4x4...
        # open each image to see which it is
        single = len(images) == 1
        for link, remote_link, align, width, header in images:
            if single:
                align = 'center'
            try:
                if width is not None:
                    percent = width
                else:
                    with Image.open(PRODUCT_LABEL_PNG_LOCATION / link.stem + '.png') as image:
                        scale = 1200.0 / image.height
                        new_width = scale * image.width
                        percent = min(int(new_width / 1800 * 100), 100)
            except IOError:
                percent = 0
            row.append((remote_link, '%s%%' % percent, align, header))
        res.append(row)
    return res

def open_next_file(filename):
    """
    adds numbers to file name until succesfully opened; stops at 99
    """
    for i in range(100):
        try:
            target = filename + '.%02d' % (i, )
            fh = os.open(target, os.O_CREAT | os.O_EXCL)
            os.close(fh)
            return open(target, 'w')
        except OSError:
            pass
    else:
        raise ERPError('File Conflicts', 'unable to create order file')

LabelLinkTab = """\
!!! html
-for row in args.rows:
    ~div 
        -for target, width, align, oe_header in row:
            -if oe_header:
                ~img src=target width=width align=align oe_header
            -else:
                ~img src=target width=width align=align
    ~br
"""
