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
                    ('labeltime_url', 'LabelTime via http://labeltime:9000/Lbls'),
                    ('labeltime_mnt', 'LabelTime via /home/openerp/mnt/newlabeltimexpvm/xfer/LabelDirectory/'),
                    ('lumiere_mnt', 'Lumiere via /mnt/smb/lumiere-e-labels/'),
		    ('cache_mnt', 'cache only (11.16:/PNG_labels)'),
                ),
                sort_order='definition',
                string='Product Label Source',
                ),
            }
