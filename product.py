from collections import defaultdict
from fis_integration.fis_schema import *
from fnx.BBxXlate.fisData import fisData
from fnx.address import NameCase
from openerp import tools
from openerp.addons.product.product import sanitize_ean13
from osv import osv, fields
from urllib import urlopen
import logging
import time

_logger = logging.getLogger(__name__)

OWN_STOCK = 12  # Physical Locations / Your Company / Stock

class product_category(xid.xmlid, osv.Model):
    "makes external_id visible and searchable"
    _name = 'product.category'
    _inherit = 'product.category'
    _order = 'xml_id'

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('F11',),
            string="FIS ID",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xid.get_xml_ids,
            arg=('F11',),
            string="FIS Module",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
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
product_category()

class product_available_at(xid.xmlid, osv.Model):
    "tracks availablility options for products"
    _name = 'product.available_at'
    _description = 'Product Location'

    _columns = {
        'name' : fields.char('Availability', size=50),
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('F97',),
            string="FIS ID",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xid.get_xml_ids,
            arg=('F97',),
            string="FIS Module",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
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
product_available_at()


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
product_template()

class product_product(xid.xmlid, osv.Model):
    'Adds Available column and shipped_as columns'
    _name = 'product.product'
    _inherit = 'product.product'

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        if context is None:
            context = {}
        model = self._name
        module = 'F135'
        imd = self.pool.get('ir.model.data')
        nvty = fisData(135, keymatch='%s101000    101**')
        records = self.browse(cr, uid, ids, context=context)
        values = {}
        for rec in records:
            current = values[rec.id] = {}
            try:
                imd_rec = imd.get_object_from_model_resid(cr, uid, model, rec.id, context=context)
                fis_rec = nvty[rec['xml_id']]
            except (ValueError, KeyError):
                values.update(super(product_product, self)._product_available(cr, uid, ids, field_names, arg, context))
            else:
                current['qty_available'] = qoh = fis_rec[F135.on_hand]
                current['incoming_qty'] = inc = fis_rec[F135.committed]
                current['outgoing_qty'] = out = fis_rec[F135.on_order]
                current['virtual_available'] = qoh + inc - out
        return values

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('F135', ),
            string="FIS ID",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xid.get_xml_ids,
            arg=('F135',),
            string="FIS Module",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
            ),
        'shipped_as': fields.char('Shipped as', size=50),
        'avail': fields.many2one(
            'product.available_at',
            'Availability',
            ),
        'spcl_ship_instr': fields.text('Special Shipping Instructions'),
        'fis_location': fields.char('Location', size=6),
        'qty_available': fields.function(_product_available, multi='qty_available',
            type='float', digits=(16,3), string='Quantity On Hand',
            help="Current quantity of products according to FIS",
            ),
        'virtual_available': fields.function(_product_available, multi='qty_available',
            type='float', digits=(16,3), string='Forecasted Quantity',
            help="Forecast quantity (computed as Quantity On Hand - Outgoing + Incoming)",
            ),
        'incoming_qty': fields.function(_product_available, multi='qty_available',
            type='float', digits=(16,3), string='Incoming',
            help="Quantity of products that are planned to arrive according to FIS.",
            ),
        'outgoing_qty': fields.function(_product_available, multi='qty_available',
            type='float', digits=(16,3), string='Outgoing',
            help="Quantity of products that are planned to leave according to FIS.",
            ),
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

product_product()

class production_line(xid.xmlid, osv.Model):
    "production line"
    _name = 'fis_integration.production_line'

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('F341', ),
            string="FIS ID",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
            select=True,
            ),
        'module': fields.function(
            xid.get_xml_ids,
            arg=('F341',),
            string="FIS Module",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
            ),
        'name': fields.char('Description', size=30),
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
            result['name'] = avail_rec[F341.desc].title()
            module_key = module, key
            if key in avail_codes:
                self.write(cr, uid, avail_codes[key], result)
            else:
                new_id = self.create(cr, uid, result)
                avail_codes[key] = new_id
        _logger.info(self._name + " done!")
        return True
production_line()
