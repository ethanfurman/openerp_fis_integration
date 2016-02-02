from collections import defaultdict
from fis_integration.fis_schema import *
from fnx.BBxXlate.fisData import fisData
from fnx.address import NameCase
from fnx.oe import dynamic_page_stub, static_page_stub
from fnx.xid import xmlid
from openerp import tools
from openerp.addons.product.product import sanitize_ean13
from osv.osv import except_osv as ERPError
from osv import osv, fields
from urllib import urlopen
from scripts import recipe
import logging
import time

_logger = logging.getLogger(__name__)

OWN_STOCK = 12  # Physical Locations / Your Company / Stock

LabelLinks = (
    "Plone/LabelDirectory/%s/%sB.bmp",
    "Plone/LabelDirectory/%s/%sNI.bmp",
    "Plone/LabelDirectory/%s/%sMK.bmp",
    )

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
        'xml_id': fields.function(
            xmlid.get_xml_ids,
            arg=('F11',),
            string="FIS ID",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xmlid.get_xml_ids,
            arg=('F11',),
            string="FIS Module",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            ),
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
        category_ids = self.search(cr, uid, [('module','=',module)])
        category_recs = self.browse(cr, uid, category_ids)
        category_codes = dict([(('F11', r.xml_id), dict(name=r.name, id=r.id, parent_id=r.parent_id)) for r in category_recs])
        cnvz = fisData(11, keymatch='as10%s')
        for i in (1, 2):
            for category_rec in cnvz:
                result = {}
                result['xml_id'] = key = category_rec[F11.code].strip()
                result['module'] = 'F11'
                module_key = 'F11', key
                if len(key) != i:
                    continue
                name = category_rec[F11.desc].title()
                if len(key) == 1:
                    name = key + ' - ' + name.strip('- ')
                result['name'] = name
                if module_key in category_codes:
                    result['parent_id'] = category_codes[module_key]['parent_id']['id']
                    self.write(cr, uid, category_codes[module_key]['id'], result)
                else:
                    if len(key) == 1:
                        result['parent_id'] = 2
                    else:
                        try:
                            result['parent_id'] = category_codes[module_key[1][:1]]['id']
                        except KeyError:
                            result['parent_id'] = category_codes['F11','9']['id']
                    new_id = self.create(cr, uid, result)
                    category_codes[module_key] = dict(name=result['name'], id=new_id, parent_id=result['parent_id'])
        _logger.info(self._name +  " done!")
        return True


class product_available_at(xmlid, osv.Model):
    "tracks availablility options for products"
    _name = 'product.available_at'
    _description = 'Product Location'

    _columns = {
        'name' : fields.char('Availability', size=50),
        'xml_id': fields.function(
            xmlid.get_xml_ids,
            arg=('F97',),
            string="FIS ID",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xmlid.get_xml_ids,
            arg=('F97',),
            string="FIS Module",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            ),
        'product_ids' : fields.one2many(
            'product.product',
            'avail',
            'Products',
            ),
        }

    def fis_updates(self, cr, uid, *args):
        _logger.info("product.available_at.auto-update starting...")
        module = 'F97'
        avail_ids = self.search(cr, uid, [('module','=',module)])
        avail_recs = self.browse(cr, uid, avail_ids)
        avail_codes = dict([(r.xml_id, r.id) for r in avail_recs])
        cnvz = fisData(97, keymatch='aa10%s')
        for avail_rec in cnvz:
            result = {}
            result['xml_id'] = key = avail_rec[F97.code].upper()
            result['module'] = module
            result['name'] = avail_rec[F97.desc].title()
            module_key = module, key
            if key in avail_codes:
                self.write(cr, uid, avail_codes[key], result)
            else:
                new_id = self.create(cr, uid, result)
                avail_codes[key] = new_id
        _logger.info(self._name + " done!")
        return True



# may add this back later...
#class product_shipping_size(osv.Model):
#    "tracks the shipping size options for products"
#    _name = 'product.shipping_size'
#
#    _columns = {
#        'name' : fields.char('Shipped as', size=50),
#        'product_ids' : fields.one2many(
#            'product.product',
#            'shipped_as',
#            'Products',
#            ),
#        }
#product_available_at()

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
        xml_ids = [v for (k, v) in
                self.get_xml_ids(
                    cr, uid, ids, field_name,
                    arg=('F135', ),
                    ).items()
                ]
        result = {}
        htmlContentList = [ ]
        for id, d in zip(ids, xml_ids):  # there should only be one...
            xml_id = d['xml_id']
            htmlContentList.append('''<img src="%s" width=55%% align="left"/>''' % (LabelLinks[0] % (xml_id, xml_id)))
            htmlContentList.append('''<img src="%s" width=35%% align="right"/><br>''' % (LabelLinks[1] % (xml_id, xml_id)))
            htmlContentList.append('''<br><img src="%s" width=100%% /><br>''' % (LabelLinks[2] % (xml_id, xml_id)))
            result[id] = static_page_stub % "".join(htmlContentList)
        return result

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        model = self._name
        module = 'F135'
        imd = self.pool.get('ir.model.data')
        nvty = fisData(135, keymatch='%s101000    101**')
        records = self.browse(cr, uid, ids, context=context)
        values = {}
        for rec in records:
            current = values[rec.id] = {}
            current['qty_available'] = qoh = rec['st_qty_available']
            current['incoming_qty'] = inc = rec['st_incoming_qty']
            current['outgoing_qty'] = out = rec['st_outgoing_qty']
            current['virtual_available'] = qoh + inc - out
        return values

    def _product_available_inv(self, cr, uid, id, field_name, field_value, misc=None, context=None):
        field_name = 'st_' + field_name
        return self.write(cr, uid, id, {field_name: field_value}, context=context)

    _columns = {
        'xml_id': fields.function(
            xmlid.get_xml_ids,
            arg=('F135', ),
            string="FIS ID",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xmlid.get_xml_ids,
            arg=('F135',),
            string="FIS Module",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            ),
        'shipped_as': fields.char('Shipped as', size=50),
        'avail': fields.many2one(
            'product.available_at',
            'Availability',
            ),
        'spcl_ship_instr': fields.text('Special Shipping Instructions'),
        'fis_location': fields.char('Location', size=6),
        'qty_available': fields.function(
            _product_available,
            fnct_inv=_product_available_inv,
            multi='qty_available',
            type='float', digits=(16,3), string='Quantity On Hand',
            store=True,
            help="Current quantity of products according to FIS",
            ),
        'virtual_available': fields.function(
            _product_available,
            multi='qty_available',
            type='float', digits=(16,3), string='Forecasted 10-day Quantity',
            store=True,
            help="Forecast quantity (computed as Quantity On Hand - Outgoing + Incoming)",
            ),
        'incoming_qty': fields.function(
            _product_available,
            fnct_inv=_product_available_inv,
            multi='qty_available',
            type='float', digits=(16,3), string='Incoming',
            store=True,
            help="Quantity of product that are planned to arrive according to FIS.",
            ),
        'outgoing_qty': fields.function(
            _product_available,
            fnct_inv=_product_available_inv,
            multi='qty_available',
            type='float', digits=(16,3), string='Outgoing',
            store=True,
            help="Quantity of product that are planned to be shipped/used according to FIS.",
            ),
        'st_makeable_qty': fields.float(
            digits=[16,3], string='Immediately Producible',
            help='Quantity that could be immediately produced.',
            oldname='makeable_qty',
            ),
        'st_incoming_qty': fields.float(
            digits=(16,3), string='non-FIS Incoming',
            help="Quantity of product that are planned to arrive.",
            oldname='nf_incoming_qty',
            ),
        'st_outgoing_qty': fields.float(
            digits=(16,3), string='non-FIS Outgoing',
            help="Quantity of product that are planned to leave.",
            oldname='nf_outgoing_qty',
            ),
        'st_qty_available': fields.float(
            digits=(16,3), string='non-FIS Quantity On Hand',
            help="Current (actual) quantity of product.",
            oldname='nf_qty_available',
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
        'cost_customer': fields.function(
            lambda *a: {},
            string="Customer to check costs for",
            type='many2one',
            method=False,
            readonly=True,
            ),
        'label_text': fields.text('Label Text'),
        'docs': fields.html('Documents'),
        }

    def button_fis_refresh(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        product_module = 'F135'
        category_module = 'F11'
        location_module = 'F97'
        prod_avail = self.pool.get('product.available_at')
        prod_cat = self.pool.get('product.category')
        prod_template = self.pool.get('product.template')
        #avail_ids = prod_avail_at.search(cr, uid, [(1,'=',1)])
        #avail_recs = prod_avail_at.browse(cr, uid, avail_ids, context=context)
        #avail_codes = {}
            #avail_codes[rec['xml_id']] = rec['id']
        cnvz = fisData(11, keymatch='as10%s')
        nvty = fisData(135, keymatch='%s101000    101**')
        records = self.browse(cr, uid, ids, context=context)
        for rec in records:
            if rec.module != 'F135':
                continue
            fis_nvty_rec = nvty.get(rec['xml_id'])
            if fis_nvty_rec is None:
                continue
            fis_sales_rec = cnvz[fis_nvty_rec[F135.sales_category]]
            values = self._get_fis_values(fis_nvty_rec, fis_sales_rec)
            cat_ids = prod_cat.search(cr, uid, [('module','=',category_module),('xml_id','=',values['categ_id'])])
            if not cat_ids:
                raise ValueError("unable to locate category code %s" % values['categ_id'])
            elif len(cat_ids) > 1:
                raise ValueError("too many matches for category code %s" % values['categ_id'])
            values['categ_id'] = prod_cat.browse(cr, uid, cat_ids)[0]['id']
            avail_ids = prod_avail.search(cr, uid, [('module','=',location_module),('xml_id','=',values['avail'])])
            if not avail_ids:
                raise ValueError("unable to locate availability code %s" % values['avail'])
            elif len(avail_ids) > 1:
                raise ValueError("too many matches for availability code %s" % values['avail'])
            values['avail'] = prod_avail.browse(cr, uid, avail_ids)[0]['id']
            self.write(cr, uid, rec['id'], values, context=context)
        return True

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
        # create a mapping of id -> res_id for available_at (location)
        avail_ids = prod_avail.search(cr, uid, [('module','=',location_module)])
        avail_recs = prod_avail.browse(cr, uid, avail_ids)
        avail_codes = dict([(r['xml_id'], r['id']) for r in avail_recs])
        # create a mapping of id -> res_id for categories
        cat_ids = prod_cat.search(cr, uid, [('module','=',category_module)])
        cat_recs = prod_cat.browse(cr, uid, cat_ids)
        cat_codes = dict([(r.xml_id, r.id) for r in cat_recs])
        #import pdb; pdb.set_trace()
        # create a mapping of id -> res_id for product items
        prod_ids = prod_items.search(cr, uid, [('module','=',product_module)])
        prod_recs = prod_items.browse(cr, uid, prod_ids)
        synced_prods = {}
        unsynced_prods = {}
        for rec in prod_recs:
            if rec.xml_id:
                synced_prods[rec.xml_id] = rec
            elif rec.default_code:
                unsynced_prods[rec.default_code] = rec
        #products = dict([(r['xml_id'], r) for r in prod_recs])
        nvty = fisData(135, keymatch='%s101000    101**')
        cnvz = fisData(11, keymatch='as10%s')
        for inv_rec in nvty:
            fis_sales_rec = cnvz.get(inv_rec[F135.sales_category])
            values = self._get_fis_values(inv_rec, fis_sales_rec)
            key = values['xml_id']
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
                prod_items.write(cr, uid, prod_rec.id, values, context=context)
            else:
                id = prod_items.create(cr, uid, values)
                prod_rec = prod_items.browse(cr, uid, [id])[0]
                synced_prods[key] = prod_rec
        _logger.info(self._name + " done!")
        return True

    def _get_fis_values(self, fis_nvty_rec, sales_category_rec):
        values = {}
        values['xml_id'] = values['default_code'] = fis_nvty_rec[F135.item_code]
        values['name'] = NameCase(fis_nvty_rec[F135.name].strip())
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
        #values['product_manager'] = fis_nvty_rec[F135.manager]

        # these are no longer looked up everytime
        #
        values['st_qty_available'] = qoh = fis_nvty_rec[F135.on_hand]
        values['st_incoming_qty'] = inc = fis_nvty_rec[F135.on_order]
        values['st_outgoing_qty'] = out = fis_nvty_rec[F135.committed]
        values['st_makeable_qty'] = recipe.make_on_hand(fis_nvty_rec[F135.item_code])

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
        'xml_id': fields.function(
            xmlid.get_xml_ids,
            arg=('F341', ),
            string="FIS ID",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xmlid.get_xml_ids,
            arg=('F341',),
            string="FIS Module",
            type='char',
            method=True,
            fnct_search=xmlid.search_xml_id,
            multi='external',
            ),
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
        avail_ids = self.search(cr, uid, [('module','=',module)])
        avail_recs = self.browse(cr, uid, avail_ids)
        avail_codes = dict([(r.xml_id, r.id) for r in avail_recs])
        cnvz = fisData(341, keymatch='f10%s')
        for avail_rec in cnvz:
            result = {}
            result['xml_id'] = key = avail_rec[F341.code].upper()
            result['module'] = module
            result['desc'] = avail_rec[F341.desc].title()
            module_key = module, key
            if key in avail_codes:
                self.write(cr, uid, avail_codes[key], result)
            else:
                new_id = self.create(cr, uid, result)
                avail_codes[key] = new_id
        _logger.info(self._name + " done!")
        return True
