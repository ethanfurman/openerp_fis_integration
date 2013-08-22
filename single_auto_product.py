from osv import osv, fields
from urllib import urlopen
import oe_xid as xid
from openerp.addons.product.product import sanitize_ean13
from VSS.BBxXlate.fisData import fisData
from VSS.utils import NameCase

class product_category(osv.Model):
    "makes external_id visible and searchable"
    _name = 'product.category'
    _inherit = 'product.category'
    _order = 'xml_id'

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg='product.category',
            string="External ID",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            ),
        }

product_category()

class product_available_at(osv.Model):
    "tracks availablility options for products"
    _name = 'product.available_at'
    _description = 'Product Location'

    _columns = {
        'name' : fields.char('Availability', size=50),
        'xml_id': fields.function(
            xid.get_xml_ids,
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg='product.available_at',
            string="External ID",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            ),
        'product_ids' : fields.one2many(
            'product.product',
            'avail',
            'Products',
            ),
        }
    
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

# Sales Category codes
class F11(object):
    code = 'An$(5,2)'
    desc = 'Cn$'
F11 = F11()

# Inventory Availablility Code
class F97(object):
    code = 'An$(5,1)'
    desc = 'Bn$'
F97 = F97()

# Products
class F135(object):
    item_code = 'An$(1,6)'
    avail = 'Bn$(1,1)'
    categ = 'Bn$(3,2)'
    name = 'Cn$(1,40)'
    ship_size = 'Cn$(41,8)'
    ean13 = 'Dn$(6,12)'
F135 = F135()

class product_product(osv.Model):
    'Adds Available column and shipped_as columns'
    _name = 'product.product'
    _inherit = 'product.product'

    _columns = {
        'shipped_as': fields.char('Shipped as', size=50),
        'avail': fields.many2one(
            'product.available_at',
            'Availability',
            ),
        }

    def FIS_updates(self, cr, uid, *args):
        """
        scans FIS availability, category, and product tables and either updates
        info or adds new items to the appropriate table
        """
        # get the tables we'll need
        print "\nchecking for category updates..."
        imd = self.pool.get('ir.model.data')
        prod_cat = self.pool.get('product.category')
        prod_avail = self.pool.get('product.available_at')
        prod_items = self

        import pdb; pdb.set_trace()

        cat_ids = prod_cat.search(cr, uid, [(1,'=',1)])
        cat_recs = prod_cat.browse(cr, uid, cat_ids)
        cat_codes = dict([(r['xml_id'], {'id':r['id'], 'parent_id':r['parent_id']}) for r in cat_recs])
        print cat_codes
        for rec in cat_recs:
            if rec['name'] == 'Saleable':
                cat_root = rec['id']
        cnvz = fisData(11, keymatch='as10%s')
        fis_categories = {}
        for rec in cnvz:
            result = {'parent_id':None}
            result['xml_id'] = key = rec[F11.code].strip()
            name = rec[F11.desc].title()
            if len(key) == 1:
                name = key + ' - ' + name.strip(' -')
                result['parent_id'] = cat_root
            result['name'] = name
            fis_categories[key] = result
        for key, settings in sorted(fis_categories.items()):
            print key, key in cat_codes
            if key in cat_codes:
                # make sure parent_id is correct
                settings['parent_id'] = cat_codes[key]['parent_id']
                settings['id'] = cat_codes[key]['id']
                print settings
                prod_cat.write(cr, uid, [key], settings)
            else:
                cat_codes[key] = {'id':None, 'parent_id':settings['parent_id']}
                if settings['parent_id'] is None:
                    try:
                        settings['parent_id'] = fis_categories[key[:1]]['id']
                    except KeyError:
                        settings['parent_id'] = fis_categories['9']['id']
                    cat_codes[key]['parent_id'] = settings['parent_id']
                new_id = prod_cat.create(cr, uid, settings)
                settings['id'] = cat_codes[key]['id'] = new_id
                print settings

        print "\nchecking for location updates..."
        avail_ids = prod_avail.search(cr, uid, [(1,'=',1)])
        avail_recs = prod_avail.browse(cr, uid, avail_ids)
        avail_codes = dict([(r['xml_id'], r['id']) for r in avail_recs])
        print avail_codes
        cnvz = fisData(97, keymatch='aa10%s')
        for rec in cnvz:
            print repr(rec)
            result = {}
            key = rec[F97.code].upper()
            result['name'] = rec[F97.desc].title()
            if key in avail_codes:
                result['xml_id'] = id = avail_codes[key]
                prod_avail.write(cr, uid, [id], result)
            else:
                new_id = prod_avail.create(cr, uid, result)
                avail_codes[key] = new_id

        print "checking for product updates..."
        # create a mapping of id -> res_id for product items
        prod_ids = prod_items.search(cr, uid, [(1,'=',1)])
        prod_recs = prod_items.browse(cr, uid, prod_ids)
        products = dict([(r['xml_id'], r) for r in prod_recs])
        nvty = fisData(135, keymatch='%s101000    101**')
        values = {}
        for inv_rec in nvty:
            values['xml_id'] = key = inv_rec[F135.item_code]         # external id
            values['code'] = key                                # internal reference
            values['name'] = inv_rec[F135.name].strip().title() # name_template
            shipped_as = inv_rec[F135.ship_size].strip()
            categ_id = inv_rec[F135.categ].strip()
            if len(categ_id) == 2 and categ_id[0] in 'OISG':
                categ_id = {'O':'0', 'I':'1', 'S':'5', 'G':'6'}[categ_id[0]] + categ_id[1]
            try:
                values['categ_id'] = cat_codes[categ_id]['id']
            except KeyError:
                print "Unable to add/update product %s because of missing category %r" % (key, categ_id)
                continue
            try:
                values['avail'] = avail_codes[inv_rec[F135.avail]]
            except KeyError:
                print "Unable to add/update product %s because of missing location %r" % (key, inv_rec[F135.avail])
                continue
            values['ean13'] = sanitize_ean13(inv_rec[F135.ean13])
            values['active'] = 1
            values['sale_ok'] = 1
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
                shipped_as = ' '.join(first).strip() + ' ' + ' '.join(last).strip()
            values['shipped_as'] = shipped_as
            if key in products:
                prod_rec = products[key]
                prod_items.write(cr, uid, [prod_rec['id']], values)
            else:
                new_id = prod_items.create(cr, uid, values)
                products[key] = new_id
        print "Done!\n"
        return True
product_product()
