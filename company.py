from openerp.osv import fields, osv

class res_company(osv.Model):
    _inherit = "res.company"
    _columns = {
            'traffic_followers_ids': fields.many2many('res.users', 'fal_rescompany_rel', 'fal_tf_cid', 'fal_tf_uid', string='Traffic Report Auto-Followers'),
            'product_integration': fields.char('FIS Products', size=64, help="Module name used for product external ids."),
            'product_category_integration': fields.char('FIS Product Categories', size=64, help="Module name used for product category external ids."),
            'product_location_integration': fields.char('FIS Product Locations', size=64, help="Module name used for product location external ids."),
            'employee_integration': fields.char('FIS Employees', size=64, help='Module name used for employee external ids.'),
            'customer_integration': fields.char('FIS Customers', size=64, help='Module name used for customer external ids.'),
            'supplier_integration': fields.char('FIS Suppliers/Vendors', size=64, help='Module name used for supplier/vendor external ids.'),
            }
res_company()
