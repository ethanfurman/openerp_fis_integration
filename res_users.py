from openerp.osv import fields, osv
from openerp.tools import SUPERUSER_ID, self_ids

class res_users(osv.Model):
    """ Update of res.users class
        - add link to the FIS partner account
    """
    _name = 'res.users'
    _inherit = ['res.users']

    _columns = {
        'fis_partner_id': fields.many2one(
            'res.partner',
            string='FIS Account',
            domain=[('customer','=',True),('is_company','=',True),('fis_valid','=',True)],
            ),
        'fis_partner_code': fields.related(
            'fis_partner_id','xml_id',
            type='char',
            size=6,
            string='Partner FIS ID',
            ),
        'fis_product_cross_ref_code': fields.char('Online Order Code', size=6, help='usually the customer #'),
        'fis_transmitter_id': fields.many2one('fis.transmitter_code', 'Transmitter #'),
        }


    def onchange_fis_partner(self, cr, uid, ids, fis_partner_id, context=None):
        res = {'domain': {}, 'value': {}}
        if not fis_partner_id:
            res['domain']['fis_transmitter_id'] = [('id','=',0)]
            res['value']['fis_transmitter_id'] = False
        else:
            res_partner = self.pool.get('res.partner')
            partner = res_partner.browse(cr, SUPERUSER_ID, fis_partner_id, context=context)
            res['domain']['fis_transmitter_id'] = [('partner_xml_id','=',partner.xml_id)]
            res['value']['fis_transmitter_id'] = False
        return res


    def onload_set_transmitter_domain(self, cr, uid, ids, fis_partner_id, context=None):
        res = {'domain': {}}
        if not fis_partner_id:
            res['domain']['fis_transmitter_id'] = [('id','=',0)]
        else:
            res_partner = self.pool.get('res.partner')
            partner = res_partner.browse(cr, SUPERUSER_ID, fis_partner_id, context=context)
            res['domain']['fis_transmitter_id'] = [('partner_xml_id','=',partner.xml_id)]
        return res


class transmitter(osv.Model):
    _name = 'fis.transmitter_code'

    def _calc_name(self, cr, uid, ids, field_name=None, arg=None, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}
        if not ids or field_name != 'name':
            return res
        for rec in self.read(
                cr, uid, ids,
                fields=['partner_xml_id','transmitter_name','transmitter_no','ship_to_code'],
                context=context,
                ):
            if rec['ship_to_code']:
                text = '%s [%s] %s' % (rec['transmitter_no'], rec['ship_to_code'], rec['transmitter_name'])
            else:
                text = '%s -- %s' % (rec['transmitter_no'], rec['transmitter_name'])
            res[rec['id']] = text
        return res

    _columns = {
        'name': fields.function(
            _calc_name,
            string='Transmitter Name',
            type='char',
            size=256,
            store={
                'fis.transmitter_code': (self_ids, [], 10),
                },
            ),
        'partner_xml_id': fields.char("Customer #", size=6, help="customer number in FIS"),
        'transmitter_name': fields.char("Transmitter Name", size=128),
        'transmitter_no': fields.char('Transmitter #', size=6),
        'ship_to_code': fields.char('Ship-to Code', size=4),
        }

    _sql_constraints = [
            ('transmitter_unique', 'unique(transmitter_no)', 'transmitter code already exists'),
            ]


