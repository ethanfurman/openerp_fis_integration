from openerp.osv import fields, osv

class res_company(osv.Model):
    _inherit = "res.company"
    _columns = {
        'traffic_followers_ids': fields.many2many(
                'res.users',
                'fal_rescompany_rel', 'fal_tf_cid', 'fal_tf_uid',
                string='Traffic Report Auto-Followers',
                ),
        'product_label_source': fields.selection((
                ('labeltime_url', 'LabelTime via http'),
                ('labeltime_mnt', 'LabelTime via /mnt'),
                ('lumiere_mnt', 'Lumiere via /mnt'),
                ('cache_only', 'cache only'),
                ),
                sort_order='definition',
                string='Product Label Source',
                ),
            }
