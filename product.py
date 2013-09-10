from osv import osv, fields
from urllib import urlopen
from openerp.addons.product.product import sanitize_ean13
from fnx.BBxXlate.fisData import fisData
from fnx.utils import NameCase
from fnx import xid, check_company_settings
from openerp import tools

import time
import logging

_logger = logging.getLogger(__name__)

CONFIG_ERROR = "Cannot sync products until  Settings --> Configuration --> FIS Integration --> %s  has been specified." 

OWN_STOCK = 12  # Physical Locations / Your Company / Stock

# Sales Category codes
class F11(object):
    code = 'An$(5,2)'
    desc = 'Cn$'
    shelf_life = 'FN'
F11 = F11()

class product_category(osv.Model):
    "makes external_id visible and searchable"
    _name = 'product.category'
    _inherit = 'product.category'
    _order = 'xml_id'

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('product_category_integration','FIS Product Category', CONFIG_ERROR),
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg=('product_category_integration','FIS Product Category', CONFIG_ERROR),
            string="External ID",
            type='char',
            method=False,
            fnct_search=lambda s, c, u, m, n, d, context=None:
                            xid.search_xml_id(s, c, u, m, n, d, ('product_category_integration','Product Category Integration',CONFIG_ERROR), context=context),
            ),
        }

    def fis_updates(self, cr, uid, *args):
        _logger.info("product.category.fis_updates starting...")
        settings = check_company_settings(self, cr, uid, ('product_integration', 'Product Module', CONFIG_ERROR))
        context = {'module': settings['product_integration']}
        category_ids = self.search(cr, uid, [(1,'=',1)])
        category_recs = self.browse(cr, uid, category_ids)
        category_codes = dict([(r['xml_id'], dict(name=r['name'], id=r['id'], parent_id=r['parent_id'])) for r in category_recs])
        cnvz = fisData(11, keymatch='as10%s')
        for i in (1, 2):
            for category_rec in cnvz:
                result = {}
                result['xml_id'] = key = category_rec[F11.code].strip()
                if len(key) != i:
                    continue
                name = category_rec[F11.desc].title()
                if len(key) == 1:
                    name = key + ' - ' + name.strip('- ')
                result['name'] = name
                if key in category_codes:
                    result['parent_id'] = category_codes[key]['parent_id']['id']
                    self.write(cr, uid, category_codes[key]['id'], result, context=context)
                else:
                    if len(key) == 1:
                        result['parent_id'] = 2
                    else:
                        try:
                            result['parent_id'] = category_codes[key[:1]]['id']
                        except KeyError:
                            result['parent_id'] = category_codes['9']['id']
                    new_id = self.create(cr, uid, result, context=context)
                    category_codes[key] = dict(name=result['name'], id=new_id, parent_id=result['parent_id'])
        _logger.info(self._name +  " done!")
        return True
product_category()

# Inventory Availablility Code
class F97(object):
    code = 'An$(5,1)'
    desc = 'Bn$'
F97 = F97()

class product_available_at(osv.Model):
    "tracks availablility options for products"
    _name = 'product.available_at'
    _description = 'Product Location'


    _columns = {
        'name' : fields.char('Availability', size=50),
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('product_location_integration','FIS Product Location', CONFIG_ERROR),
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg=('product_location_integration','FIS Product Location', CONFIG_ERROR),
            string="External ID",
            type='char',
            method=False,
            fnct_search=lambda s, c, u, m, n, d, context=None:
                            xid.search_xml_id(s, c, u, m, n, d, ('product_location_integration','Product Location Integration',CONFIG_ERROR), context=context),
            ),
        'product_ids' : fields.one2many(
            'product.product',
            'avail',
            'Products',
            ),
        }
    
    def fis_updates(self, cr, uid, *args):
        _logger.info("product.available_at.auto-update starting...")
        settings = check_company_settings(self, cr, uid, ('product_integration', 'Product Module', CONFIG_ERROR))
        context = {'module': settings['product_integration']}
        avail_ids = self.search(cr, uid, [(1,'=',1)])
        avail_recs = self.browse(cr, uid, avail_ids)
        avail_codes = dict([(r['xml_id'], r['id']) for r in avail_recs])
        cnvz = fisData(97, keymatch='aa10%s')
        for avail_rec in cnvz:
            result = {}
            result['xml_id'] = key = avail_rec[F97.code].upper()
            result['name'] = avail_rec[F97.desc].title()
            if key in avail_codes:
                self.write(cr, uid, avail_codes[key], result, context=context)
            else:
                self.create(cr, uid, result, context=context)
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

# Products
class F135(object):
    item_code = 'An$(1,6)'
    available = 'Bn$(1,1)'
    sales_category = 'Bn$(3,2)'
    shelf_life = 'Bn$(69,2)'
    name = 'Cn$(1,40)'
    ship_size = 'Cn$(41,8)'
    manager = 'Dn$(5,1)'
    ean13 = 'Dn$(6,12)'
    storage_location = 'Dn$(18,6)'
    on_hand = 'I(6)'
    on_order = 'I(7)'
    committed = 'I(8)'
    wholesale = 'I(23)'
F135 = F135()

class product_product(osv.Model):
    'Adds Available column and shipped_as columns'
    _name = 'product.product'
    _inherit = 'product.product'

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        settings = check_company_settings(self, cr, uid, ('product_integration', 'Product Module', CONFIG_ERROR))
        if context is None:
            context = {}
        module = settings['product_integration']
        imd = self.pool.get('ir.model.data')
        nvty = fisData(135, keymatch='%s101000    101**')
        records = self.browse(cr, uid, ids, context=context)
        values = {}
        for rec in records:
            current = values[rec.id] = {}
            try:
                imd_rec = imd.get_object_from_module_model_resid(cr, uid, module, self._name, rec.id, context=context)
            except ValueError:
                continue
            fis_rec = nvty[rec['xml_id']]
            current['qty_available'] = qoh = fis_rec[F135.on_hand]
            current['incoming_qty'] = inc = fis_rec[F135.committed]
            current['outgoing_qty'] = out = fis_rec[F135.on_order]
            current['virtual_available'] = qoh + inc - out
        return values

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('product_integration','Product Module',CONFIG_ERROR),
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg=('product_integration','Product Module',CONFIG_ERROR),
            string="External ID",
            type='char',
            method=False,
            fnct_search=lambda s, c, u, m, n, d, context=None:
                            xid.search_xml_id(s, c, u, m, n, d, ('product_integration','Product Integration',CONFIG_ERROR), context=context),
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
        settings = check_company_settings(self, cr, uid, ('product_integration', 'Product Module', CONFIG_ERROR))
        if context is None:
            context = {}
        context['module'] = settings['product_integration']
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
            fis_nvty_rec = nvty[rec['xml_id']]
            fis_sales_rec = cnvz[fis_nvty_rec[F135.sales_category]]
            values = self._get_fis_values(fis_nvty_rec, fis_sales_rec)
            cat_ids = prod_cat.search(cr, uid, [('xml_id','=',values['categ_id'])])
            if not cat_ids:
                raise ValueError("unable to locate category code %s" % values['categ_id'])
            elif len(cat_ids) > 1:
                import pdb; pdb.set_trace()
                raise ValueError("too many matches for category code %s" % values['categ_id'])
            values['categ_id'] = prod_cat.browse(cr, uid, cat_ids)[0]['id']
            avail_ids = prod_avail.search(cr, uid, [('xml_id','=',values['avail'])])
            if not avail_ids:
                raise ValueError("unable to locate availability code %s" % values['avail'])
            elif len(avail_ids) > 1:
                raise ValueError("too many matches for availability code %s" % values['avail'])
            values['avail'] = prod_avail.browse(cr, uid, avail_ids)[0]['id']
            #warranty = values.pop('warranty')
            #tmpl_rec = rec.product_tmpl_id
            print values['warranty']
            self.write(cr, uid, rec['id'], values, context=context)
            #prod_template.write(cr, uid, [tmpl_rec.id], {'warranty':warranty}, context=context)
        return True

    def fis_updates(self, cr, uid, *args):
        """
        scans FIS product table and either updates product info or
        adds new products to table
        """
        # get the tables we'll need
        _logger.info("product.product.fis_updates starting...")
        time.sleep(300)
        settings = check_company_settings(self, cr, uid, ('product_integration', 'Product Module', CONFIG_ERROR))
        context = {'module': settings['product_integration']}
        imd = self.pool.get('ir.model.data')
        prod_cat = self.pool.get('product.category')
        prod_avail = self.pool.get('product.available_at')
        prod_items = self
        # create a mapping of id -> res_id for available_at (location)
        avail_ids = prod_avail.search(cr, uid, [(1,'=',1)])
        avail_recs = prod_avail.browse(cr, uid, avail_ids)
        avail_codes = dict([(r['xml_id'], r['id']) for r in avail_recs])
        # create a mapping of id -> res_id for categories
        cat_ids = prod_cat.search(cr, uid, [(1,'=',1)])
        cat_recs = prod_cat.browse(cr, uid, cat_ids)
        cat_codes = dict([(r['xml_id'], r['id']) for r in cat_recs])
        # create a mapping of id -> res_id for product items
        prod_ids = prod_items.search(cr, uid, [(1,'=',1)])
        prod_recs = prod_items.browse(cr, uid, prod_ids)
        synced_prods = {}
        unsynced_prods = {}
        for rec in prod_recs:
            if rec['xml_id']:
                synced_prods[rec['xml_id']] = rec
            elif rec['default_code']:
                unsynced_prods[rec['default_code']] = rec
        #products = dict([(r['xml_id'], r) for r in prod_recs])
        nvty = fisData(135, keymatch='%s101000    101**')
        for inv_rec in nvty:
            values = self._get_fis_values(inv_rec)
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
                prod_items.write(cr, uid, prod_rec['id'], values, context=context)
            elif key in unsynced_prods:
                prod_rec = unsynced_prods[key]
                prod_items.write(cr, uid, prod_rec['id'], values, context=context)
            else:
                id = prod_items.create(cr, uid, values, context=context)
                prod_rec = prod_items.browse(cr, uid, [id], context=context)[0]
                synced_prods[key] = prod_rec
        _logger.info(self._name + " done!")
        return True
    
    def _get_fis_values(self, fis_nvty_rec, sales_category_rec):
        values = {}
        values['xml_id'] = values['default_code'] = fis_nvty_rec[F135.item_code]
        values['name'] = NameCase(fis_nvty_rec[F135.name].strip())
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
        if not sl:
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

    def _change_product_qty(self, cr, uid, rec, new_qty, context=None):
        """ Changes the Product Quantity by making a Physical Inventory."""

        if context is None:
            context = {}

        rec_id = rec.id
        context['active_id'] = rec_id

        inventry_obj = self.pool.get('stock.inventory')
        inventry_line_obj = self.pool.get('stock.inventory.line')
        prod_obj_pool = self.pool.get('product.product')

        res_original = rec

        inventory_id = inventry_obj.create(cr , uid, {'name': 'INV: %s' % tools.ustr(res_original.name)}, context=context)
        line_data ={
            'inventory_id' : inventory_id,
            'product_qty' : new_qty,
            'location_id' : OWN_STOCK,
            'product_id' : rec_id,
            'product_uom' : res_original.uom_id.id,
            'prod_lot_id' : '',
        }
        inventry_line_obj.create(cr , uid, line_data, context=context)

        inventry_obj.action_confirm(cr, uid, [inventory_id], context=context)
        inventry_obj.action_done(cr, uid, [inventory_id], context=context)
        return {}

        if context is None:
            context = {}
        cpq = self.pool.get('stock.change.product.qty')
        sl = self.pool.get('stock.location')
        loc_id = sl.browse(cr, uid, [OWN_STOCK], context=context)[0]
        cpq.create(cr, uid,
                {'product_id': rec.id, 'new_quantity': new_qty, 'prodlot_id': '', 'location_id': loc_id.id},
                context=context)
        context['active_id'] = rec.id
        cpq.change_product_qty(cr, uid, [rec.id], context=context)
product_product()
