from openerp.osv import fields, osv
from openerp.tools import SUPERUSER_ID, self_ids

class res_users(osv.Model):
    """ Update of res.users class
        - add link to the FIS partner account
        - add link to the FIS transmitter accounts
    """
    _name = 'res.users'
    _inherit = ['res.users']

    _columns = {
        'fis_partner_id': fields.many2one(
            'res.partner',
            string='FIS Account',
            domain = [('fis_ship_to_code','!=',False),('module','in',['F33','F34'])],
            ),
        'fis_partner_code': fields.related(
            'fis_partner_id','xml_id',
            type='char',
            size=6,
            string='Partner FIS ID',
            ),
        'fis_product_cross_ref_code': fields.char('Online Order Code', size=6, help='usually the customer #'),
        'fis_transmitter_id': fields.related(
                'fis_partner_id', 'fis_transmitter_id',
                type='many2one',
                string='FIS Transmitter ID',
                relation='fis.transmitter_code',
                ),
        'fis_transmitter_no': fields.related(
            'fis_partner_id','fis_transmitter_id','transmitter_no',
                string='FIS Transmitter No',
                type='char',
                size=6,
                ),
        'fis_online_order_show_req_ship_date': fields.boolean('Show Requested Ship Date'),
        'fis_online_order_show_po_number': fields.boolean('Show PO Number'),
        }


    def onchange_fis_partner(self, cr, uid, ids, fis_partner_id, context=None):
        res = {'domain': {}, 'value': {}}
        if not fis_partner_id:
            res['domain']['fis_transmitter_id'] = [('id','=',0)]
            res['value']['fis_transmitter_id'] = False
        else:
            res_partner = self.pool.get('res.partner')
            fis_transmitter_code = self.pool.get('fis.transmitter_code')
            partner = res_partner.browse(cr, SUPERUSER_ID, fis_partner_id, context=context)
            if '-' not in partner.xml_id:
                xml_id, ship_to = partner.xml_id, ''
            else:
                xml_id, ship_to = partner.xml_id.split('-')
                if ship_to == 'default':
                    ship_to = ''
            transmitter_ids = fis_transmitter_code.search(
                    cr, SUPERUSER_ID,
                    [('partner_xml_id','=',xml_id),('ship_to_code','=',ship_to)],
                    )
            value = False
            if len(transmitter_ids) == 1:
                [value] = transmitter_ids
            res['domain']['fis_transmitter_id'] = [('partner_xml_id','=like',xml_id+'%')]
            res['value']['fis_transmitter_id'] = value
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

    def _calc_name(self, cr, uid, ids, field_names=None, arg=None, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}
        if not ids or 'name' not in field_names and 'xml_id' not in field_names:
            return res
        for rec in self.read(
                cr, uid, ids,
                fields=['partner_xml_id','transmitter_name','transmitter_no','ship_to_code'],
                context=context,
                ):
            if rec['ship_to_code'] and rec['transmitter_name']:
                name = '%s [%s] %s' % (rec['transmitter_no'], rec['ship_to_code'], rec['transmitter_name'])
                xml_id = '%s-%s' % (rec['partner_xml_id'], rec['ship_to_code'])
            elif rec['ship_to_code']:
                name = '%s [%s]' % (rec['transmitter_no'], rec['ship_to_code'])
                xml_id = '%s-%s' % (rec['partner_xml_id'], rec['ship_to_code'])
            elif rec['transmitter_name']:
                name = '%s -- %s' % (rec['transmitter_no'], rec['transmitter_name'])
                xml_id = '%s' % (rec['partner_xml_id'], )
            else:
                name = rec['transmitter_no']
            res[rec['id']] = {'name': name, 'xml_id': xml_id}
        return res

    _columns = {
        'name': fields.function(
            _calc_name,
            string='Transmitter No & Name',
            type='char',
            size=256,
            store={
                'fis.transmitter_code': (self_ids, [], 10),
                },
            multi='xml-name',
            ),
        'xml_id': fields.function(
            _calc_name,
            string='FIS ID',
            type='char',
            size=11,
            store={
                'fis.transmitter_code': (self_ids, [], 10),
                },
            multi='xml-name',
            ),
        'partner_xml_id': fields.char("Customer #", size=6, help="customer number in FIS"),
        'transmitter_name': fields.char("Transmitter Name", size=128),
        'transmitter_no': fields.char('Transmitter #', size=6),
        'ship_to_code': fields.char('Ship-to Code', size=7),
        }

    _sql_constraints = [
            ('transmitter_unique', 'unique(transmitter_no)', 'transmitter code already exists'),
            ]


