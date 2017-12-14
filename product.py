from collections import defaultdict
from aenum import NamedTuple
from dbf import Date
from fis_integration.fis_schema import F11, F97, F135, F341
from scription import Execute
from VSS.BBxXlate.fisData import fisData
from VSS.address import NameCase
from fnx import date
from fnx.oe import dynamic_page_stub, static_page_stub
from fnx.xid import xmlid
from openerp import SUPERUSER_ID
from openerp.addons.product.product import sanitize_ean13
from openerp.exceptions import ERPError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, Period
from osv import osv, fields
from scripts import recipe
import logging
import re

_logger = logging.getLogger(__name__)

OWN_STOCK = 12  # Physical Locations / Your Company / Stock

LabelLinks = (
    "Plone/LabelDirectory/%s/%sB.bmp",
    "Plone/LabelDirectory/%s/%sNI.bmp",
    "Plone/LabelDirectory/%s/%sMK.bmp",
    )

class ForecastDetail(NamedTuple):
    produced = 0, None, 0.0
    purchased = 1, None, 0.0
    consumed = 2, None, 0.0
    sold = 3, None, 0.0

class Forecast(NamedTuple):
    item = 0, None, ''
    day_10 = 1, None, ForecastDetail()
    day_21 = 2, None, ForecastDetail()

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
    _order = 'complete_name'

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'complete_name': fields.function(
            _name_get_fnc,
            type="char",
            string='Name',
            store={ 'product.category': (_get_category_records, ['name', 'parent_id'], 10) },
            ),
        }

    def fis_updates(self, cr, uid, *args):
        _logger.info("product.category.fis_updates starting...")
        module = 'F11'
        xml_id_map = self.get_xml_id_map(cr, uid, module=module)
        category_recs = dict((r.id, r) for r in self.browse(cr, uid, xml_id_map.values()))
        category_codes = {}
        for key, id in xml_id_map.items():
            rec = category_recs[id]
            category_codes[key] = dict(name=rec.name, id=rec.id, parent_id=rec.parent_id)
        cnvz = fisData(11, keymatch='as10%s')
        for i in (1, 2):
            for category_rec in cnvz:
                result = {}
                result['xml_id'] = key = category_rec[F11.code].strip()
                result['module'] = 'F11'
                if len(key) != i:
                    continue
                name = re.sub('sunridge', 'SunRidge', category_rec[F11.desc].title(), flags=re.I)
                if len(key) == 1:
                    name = key + ' - ' + name.strip('- ')
                result['name'] = name
                if key in category_codes:
                    result['parent_id'] = category_codes[key]['parent_id']['id']
                    self.write(cr, uid, category_codes[key]['id'], result)
                else:
                    if len(key) == 1:
                        result['parent_id'] = 2
                    else:
                        try:
                            result['parent_id'] = category_codes[key[:1]]['id']
                        except KeyError:
                            result['parent_id'] = category_codes['9']['id']
                    new_id = self.create(cr, uid, result)
                    category_codes[key] = dict(name=result['name'], id=new_id, parent_id=result['parent_id'])
        _logger.info(self._name +  " done!")
        return True


class product_available_at(xmlid, osv.Model):
    "tracks availablility options for products"
    _name = 'product.available_at'
    _description = 'Product Location'

    _columns = {
        'name' : fields.char('Availability', size=50),
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'product_ids' : fields.one2many(
            'product.product',
            'avail',
            'Products',
            ),
        }

    def fis_updates(self, cr, uid, *args):
        _logger.info("product.available_at.auto-update starting...")
        module = 'F97'
        avail_codes = self.get_xml_id_map(cr, uid, module=module)
        cnvz = fisData(97, keymatch='aa10%s')
        for avail_rec in cnvz:
            result = {}
            result['xml_id'] = key = avail_rec[F97.code].upper()
            result['module'] = module
            result['name'] = re.sub('sunridge', 'SunRidge', avail_rec[F97.desc].title(), flags=re.I)
            if key in avail_codes:
                self.write(cr, uid, avail_codes[key], result)
            else:
                new_id = self.create(cr, uid, result)
                avail_codes[key] = new_id
        _logger.info(self._name + " done!")
        return True


class product_template(osv.Model):
    _name = "product.template"
    _inherit = 'product.template'

    _columns = {
        'warranty': fields.float("Shelf Life (mos)", digits=(16,3),),
        }


class product_product(xmlid, osv.Model):
    'Adds Available column and shipped_as columns'
    _name = 'product.product'
    _inherit = 'product.product'

    # trademark_expiry_year
    # trademark_state
    # trademark_renewal_date
    def _trademark_state(self, cr, uid, ids, field_names, arg, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}
        records = self.read(
                cr, uid, ids,
                fields=['id', 'trademark_expiry_year', 'trademark_renewal_date'],
                context=context,
                )
        dates = defaultdict(list)
        renewals = {}
        for rec in records:
            dates[rec['trademark_expiry_year']].append(rec['id'])
            renewals[rec['id']] = rec['trademark_renewal_date']
        # convert list of records to dict of id -> renewal
        records = dict([(r['id'], r['trademark_renewal_date']) for r in records])
        today = Date.strptime(
                fields.date.context_today(self, cr, uid, context=context),
                DEFAULT_SERVER_DATE_FORMAT,
                )
        for expiry_year, ids in dates.items():
            renewal_ids = []
            # try:
            #     expiry_date = Date.strptime(expiry_date, DEFAULT_SERVER_DATE_FORMAT)
            # except ValueError:
            #     days_left = 0
            # else:
            #     days_left = max((expiry_date - today).days, 0)
            if expiry_year > today.year:
                # all green and good to go!
                state = 'active'
            elif expiry_year < today.year:
                # all dead
                state = 'dead'
            else:
                # either dying or renewing
                state = 'dying'
                ids, original_ids = [], ids
                for id in original_ids:
                    renewal = records[id]
                    if renewal and (today - date(renewal)) < Period.Week7:
                        # if renewal date is in the last 13 weeks
                        renewal_ids.append(id)
                    else:
                        # otherwise it's dying
                        ids.append(id)
            if arg == 'bulk':
                res[state] = ids
                res['renewing'] = renewal_ids
            else:
                for id in ids:
                    res[id] = state
                for id in renewal_ids:
                    res[id] = 'renewing'
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

    def _label_links(self, cr, uid, ids, field_name, arg, context=None):
        xml_ids = self.get_xml_id_map(cr, uid, module='F135', ids=ids, context=context)
        result = {}
        htmlContentList = []
        for xml_id, id in xml_ids.items():
            htmlContentList.append('''<img src="%s" width=55%% align="left"/>''' % (LabelLinks[0] % (xml_id, xml_id)))
            htmlContentList.append('''<img src="%s" width=35%% align="right"/><br>''' % (LabelLinks[1] % (xml_id, xml_id)))
            htmlContentList.append('''<br><img src="%s" width=100%% /><br>''' % (LabelLinks[2] % (xml_id, xml_id)))
            result[id] = static_page_stub % "".join(htmlContentList)
        return result

    _columns = {
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'shipped_as': fields.char('Shipped as', size=50),
        'avail': fields.many2one(
            'product.available_at',
            'Availability',
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
        'trademark': fields.char(string='Trademark', size=2),
        'trademark_expiry_year': fields.integer('Trademark Expires', help="Expiry Year"),
        'trademark_state': fields.function(
                _trademark_state,
                fnct_inv=True,
                type='selection',
                string='Trademark Status',
                sort_order='definition',
                selection = (
                    ('active', 'Active'),
                    ('dying', 'Expiring'),
                    ('renewing', 'Renewing'),
                    ('dead', 'Dead'),
                    ),
                store={
                    'product.product': (
                        lambda table, cr, uid, ids, ctx: ids,
                        ['trademark_expiry_year', 'trademark_renewal_date'],
                        10,
                    )},
                ),
        'trademark_renewal_date': fields.date('Trademark renewal submitted'),
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
            oldname='virtual_available',
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
        }

    def update_trademark_state(self, cr, uid, ids=None, arg=None, context=None):
        print repr(ids)
        if ids is None:
            ids = self.search(cr, uid, [('trademark','!=',False)], context=context)
        print repr(ids)
        res = self._trademark_state(cr, uid, ids, field_names=None, arg='bulk', context=context)
        from pprint import pprint; pprint(res)
        # res = {days_left: [ids], ...}
        for state, ids in res.items():
            print '%s: %r' % (state, ids)
            success = self.write(cr, uid, ids, {'trademark_state': state}, context=context)
            if not success:
                return success
        print 'done'
        return True

    def onchange_trademark(self, cr, uid, ids, year, renewal, context=None):
        today = date(fields.date.context_today(self, cr, uid, context=context))
        result = {}
        result['value'] = values = {}
        if year > today.year:
            values['trademark_state'] = 'active'
        elif year < today.year:
            values['trademark_state'] = 'dead'
        else:
            # either dying or renewing
            if renewal and (today - date(renewal)) < Period.Week7:
                # if renewal date is in the last 13 weeks
                values['trademark_state'] = 'renewing'
            else:
                # otherwise it's dying
                values['trademark_state'] = 'dying'
        return result

    def fis_updates(self, cr, uid, *args):
        """
        scans FIS product table and either updates product info or
        adds new products to table
        """
        # get the tables we'll need
        _logger.info("product.product.fis_updates starting...")
        product_module = 'F135'
        category_module = 'F11'
        location_module = 'F97'
        prod_cat = self.pool.get('product.category')
        prod_avail = self.pool.get('product.available_at')
        prod_items = self
        ir_model_data = self.pool.get('ir.model.data')
        # and the cleaning category
        cleaning_cat = ir_model_data.get_object_reference(cr, uid, 'fnx_pd', 'pd_cleaning')[1]
        # create a mapping of id -> res_id for available_at (location)
        avail_ids = prod_avail.search(cr, uid, [('module','=',location_module)])
        avail_recs = prod_avail.browse(cr, uid, avail_ids)
        avail_codes = dict([(r['xml_id'], r['id']) for r in avail_recs])
        # create a mapping of id -> res_id for categories
        cat_ids = prod_cat.search(cr, uid, [('module','=',category_module)])
        cat_recs = prod_cat.browse(cr, uid, cat_ids)
        cat_codes = dict([(r.xml_id, r.id) for r in cat_recs])
        # create a mapping of id -> res_id for product items
        prod_xml_id_map = self.get_xml_id_map(cr, uid, module=product_module)
        prod_recs = prod_items.browse(cr, uid, prod_xml_id_map.values())
        synced_prods = {}
        unsynced_prods = {}
        for rec in prod_recs:
            if rec.xml_id:
                synced_prods[rec.xml_id] = rec
            elif rec.default_code:
                unsynced_prods[rec.default_code] = rec
        nvty = fisData(135, keymatch='%s101000    101**')
        cnvz = fisData(11, keymatch='as10%s')
        # create a mapping of id -> 10- & 21- quantities
        prod_forecast_qtys = self._get_forecast_quantities(cr, uid, [])
        # loop 1: update all the independent data
        for inv_rec in nvty:
            fis_sales_rec = cnvz.get(inv_rec[F135.sales_category])
            values = self._get_fis_values(inv_rec, fis_sales_rec)
            key = values['xml_id']
            item, _10_day, _21_day = prod_forecast_qtys.get(key) or Forecast()
            values['fis_qty_produced'] = 0
            values['fis_qty_consumed'] = 0
            values['fis_qty_purchased'] = 0
            values['fis_qty_sold'] = 0
            values['fis_qty_available'] = values['fis_qty_on_hand']
            values['fis_10_day_produced'] = _10_day.produced
            values['fis_10_day_consumed'] = _10_day.consumed
            values['fis_10_day_purchased'] = _10_day.purchased
            values['fis_10_day_sold'] = _10_day.sold
            values['fis_10_day_available'] = values['fis_qty_on_hand'] + sum(_10_day)
            values['fis_21_day_produced'] = _21_day.produced
            values['fis_21_day_consumed'] = _21_day.consumed
            values['fis_21_day_purchased'] = _21_day.purchased
            values['fis_21_day_sold'] = _21_day.sold
            values['fis_21_day_available'] = values['fis_qty_on_hand'] + sum(_21_day)
            if key.startswith('90000'):
                values['categ_id'] = cleaning_cat
                values['sale_ok'] = False
                del values['avail']
            else:
                try:
                    values['categ_id'] = cat_codes[values['categ_id']]
                except KeyError:
                    _logger.warning("Unable to add/update product %s because of missing category %r" % (key, values['categ_id']))
                    continue
                try:
                    values['avail'] = avail_codes[values['avail']]
                except KeyError:
                    _logger.warning("Unable to add/update product %s because of missing location %r" % (key, values['avail']))
                    continue
            if key in synced_prods:
                prod_rec = synced_prods[key]
                prod_items.write(cr, uid, prod_rec['id'], values)
            elif key in unsynced_prods:
                prod_rec = unsynced_prods[key]
                prod_items.write(cr, uid, prod_rec.id, values)
            else:
                id = prod_items.create(cr, uid, values)
                values['trademark_state'] = 'dead'
                prod_rec = prod_items.browse(cr, uid, [id])[0]
                synced_prods[key] = prod_rec
        # loop 2: update the dependent data
        for inv_rec in nvty:
            values = {}
            key = inv_rec[F135.item_code]
            values['fis_qty_makeable'] = recipe.make_on_hand(inv_rec[F135.item_code])
            if key in synced_prods:
                prod_rec = synced_prods[key]
                prod_items.write(cr, uid, prod_rec['id'], values)
            elif key in unsynced_prods:
                prod_rec = unsynced_prods[key]
                prod_items.write(cr, uid, prod_rec.id, values)
        # and we're done
        _logger.info(self._name + " done!")
        return True

    def _get_fis_values(self, fis_nvty_rec, sales_category_rec):
        values = {}
        values['xml_id'] = values['default_code'] = fis_nvty_rec[F135.item_code]
        name = NameCase(fis_nvty_rec[F135.name].strip())
        name = re.sub('sunridge', 'SunRidge', name, flags=re.I)
        values['name'] = name
        values['module'] = 'F135'
        categ_id = fis_nvty_rec[F135.sales_category].strip()
        if len(categ_id) == 2 and categ_id[0] in 'OISG':
            categ_id = {'O':'0', 'I':'1', 'S':'5', 'G':'6'}[categ_id[0]] + categ_id[1]
        values['categ_id'] = categ_id
        values['ean13'] = sanitize_ean13(fis_nvty_rec[F135.ean13])
        values['active'] = 1
        values['sale_ok'] = 1
        values['list_price'] = fis_nvty_rec[F135.wholesale]
        values['avail'] = fis_nvty_rec[F135.available].upper()
        values['fis_location'] = fis_nvty_rec[F135.storage_location]
        sl = fis_nvty_rec[F135.shelf_life]
        values['warranty'] = sl = float(fis_nvty_rec[F135.shelf_life] or 0.0)
        if not sl and sales_category_rec:
            values['warranty'] = float(sales_category_rec[F11.shelf_life] or 0.0)
        values['fis_qty_on_hand'] = fis_nvty_rec[F135.on_hand]
        values['trademark'] = fis_nvty_rec[F135.trademark_expiry_year].strip() or False
        if not values['trademark']:
            values['trademark_state'] = ''

        shipped_as = fis_nvty_rec[F135.ship_size].strip()
        if shipped_as.lower() in ('each','1 each','1/each'):
            shipped_as = '1 each'
        elif shipped_as:
            first, last = [], []
            letters = False
            for char in shipped_as:
                if letters or char.isalpha():
                    last.append(char)
                    letters = True
                else:
                    first.append(char)
            if last == 'z':
                last = 'oz'
            shipped_as = ''.join(first).strip() + ' ' + ''.join(last).strip()
        values['shipped_as'] = shipped_as
        return values

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

    def fis_updates(self, cr, uid, *args):
        _logger.info("fis_integration.production_line.auto-update starting...")
        module = 'F341'
        avail_codes = self.get_xml_id_map(cr, uid, module=module)
        cnvz = fisData(341, keymatch='f10%s')
        for avail_rec in cnvz:
            result = {}
            result['xml_id'] = key = avail_rec[F341.code].upper()
            result['module'] = module
            result['desc'] = re.sub('sunridge', 'SunRidge', avail_rec[F341.desc].title(), flags=re.I)
            if key in avail_codes:
                self.write(cr, uid, avail_codes[key], result)
            else:
                new_id = self.create(cr, uid, result)
                avail_codes[key] = new_id
        _logger.info(self._name + " done!")
        return True


class product_traffic(osv.Model):
    _name = 'fis_integration.product_traffic'
    _description = 'low product'
    _order = 'date desc'
    _inherit = ['mail.thread']
    _mirrors = {'product_id': ['description', 'categ_id']}

    def _check_already_open(self, cr, uid, ids):
        products = set()
        for rec in self.browse(cr, SUPERUSER_ID, [None]):
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

