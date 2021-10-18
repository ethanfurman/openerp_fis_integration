from openerp.osv import fields, osv
from openerp.tools import SUPERUSER_ID, self_ids, get_ids
from openerp.exceptions import ERPError

import re

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
            domain=[('fis_online_ordering_possible','=',True)],
            help="The ship-to partner to use for online orders",
            ),
        'fis_partner_online_ordering_enabled': fields.related(
            'fis_partner_id','fis_online_ordering_enabled',
            string='Partner Online Ordering enabled',
            type='boolean',
            ),
        'fis_ship_to_id': fields.many2one(
            'res.partner',
            string='FIS Ship-To',
            domain=[('fis_online_ordering_enabled','=',True)],
            ),
        'fis_order_code': fields.char(string='Ordering FIS ID', size=11, help="used by the order processing scripts", oldname='fis_partner_code'),
        'fis_product_cross_ref_code': fields.char('Online Order Code', size=6, help='usually the customer #'),
        'fis_transmitter_id': fields.many2one(
                'fis.transmitter_code',
                string='FIS Transmitter ID',
                relation='fis.transmitter_code',
                ),
        'fis_transmitter_no': fields.char('FIS Transmitter No', size=6),
        'fis_online_order_show_req_ship_date': fields.boolean('Show Requested Ship Date'),
        'fis_online_order_show_po_number': fields.boolean('Show PO Number'),
        'fis_salesperson_ids': fields.one2many(
            'fis.account.salesperson', 'user_id',
            "Salesperson Info",
            ),
        }


    def onchange_fis_partner(self, cr, uid, ids, partner_id, ship_to_id, transmitter_id, context=None):
        """
        fis_partner will always be an F33 customer record
        """
        res = {'domain': {}, 'value': {}}
        domain = res['domain']
        value = res['value']
        if not partner_id:
            value['fis_order_code'] = False
            value['fis_product_cross_ref_code'] = False
            domain['fis_transmitter_id'] = [('id','!=',0)]
            domain['fis_ship_to_id'] = [('is_company','=',False),('fis_online_ordering_enabled','=',True)]
            if transmitter_id:
                value['fis_transmitter_id'] = False
            if ship_to_id:
                value['fis_ship_to_id'] = False
        else:
            res_partner = self.pool.get('res.partner')
            partner = res_partner.browse(cr, SUPERUSER_ID, partner_id, context=context)
            if re.match('HE\d\d\d', partner.xml_id):
                crossref_code = 'HE447'
            else:
                crossref_code = '-all-'
            value['fis_product_cross_ref_code'] = crossref_code
            ship_tos = []
            ship_to_ids = []
            transmitter_ids = []
            for ship_to in (partner.fis_ship_to_ids or []):
                if ship_to.fis_transmitter_ids:
                    ship_tos.append(ship_to)
                    ship_to_ids.append(ship_to.id)
                    transmitter_ids.extend(get_ids(ship_to,'fis_transmitter_ids'))
            domain['fis_ship_to_id'] = [('id','in',ship_to_ids)]
            if len(ship_to_ids) == 1:
                value['fis_ship_to_id'] = ship_to_ids[0]
                value['fis_order_code'] = ship_tos[0].xml_id
            elif not ship_to_ids and partner.fis_online_ordering_enabled:
                value['fis_order_code'] = partner.xml_id
            domain['fis_transmitter_id'] = [('id','in',transmitter_ids)]
            if transmitter_id not in transmitter_ids:
                if len(transmitter_ids) == 1:
                    value['fis_transmitter_id'] = transmitter_ids[0]
                else:
                    value['fis_transmitter_id'] = False
        return res

    def onchange_fis_ship_to(self, cr, uid, ids, ship_to_id, partner_id, transmitter_id, context=None):
        """
        fis_ship_to will always be an F34 record
        """
        res = {'domain': {}, 'value': {}}
        domain = res['domain']
        value = res['value']
        res_partner = self.pool.get('res.partner')
        if not ship_to_id:
            if partner_id:
                # if partner has no ship-tos, then an empty ship-to is normal;
                # otherwise, zero out the partner and transmitter
                partner = res_partner.browse(cr, SUPERUSER_ID, partner_id, context=context)
                if not partner.fis_online_ordering_enabled:
                    value['fis_order_code'] = False
                    value['fis_partner_id'] = False
                    value['fis_partner_code'] = False
                    if transmitter_id:
                        value['fis_transmitter_code'] = False
        else:
            ship_to = res_partner.browse(cr, SUPERUSER_ID, ship_to_id, context=context)
            domain['fis_ship_to_id'] = [('id','in',get_ids(ship_to.fis_ship_to_parent_id,'fis_ship_to_ids'))]
            value['fis_order_code'] = ship_to.xml_id
            if partner_id != ship_to.fis_ship_to_parent_id.id:
                value['fis_partner_id'] = ship_to.fis_ship_to_parent_id.id
            transmitter_ids = get_ids(ship_to,'fis_transmitter_ids')
            if len(transmitter_ids) > 1:
                domain['fis_transmitter_id'] = [('id','in',transmitter_ids)]
            if transmitter_id not in transmitter_ids:
                value['fis_transmitter_id'] = transmitter_ids[0]
        return res

    def onchange_fis_transmitter(self, cr, uid, ids, transmitter_id, partner_id, ship_to_id, context=None):
        res = {'domain': {}, 'value': {}}
        domain = res['domain']
        value = res['value']
        if not transmitter_id:
                domain['fis_transmitter_id'] = [('id','!=',False)]
                domain['fis_ship_to_id'] = [('is_company','=',False),('fis_online_ordering_enabled','=',True)]
                if partner_id:
                    value['fis_partner_id'] = False
                if ship_to_id:
                    value['fis_ship_to_id'] = False
        else:
            transmitter_code = self.pool.get('fis.transmitter_code')
            transmitter = transmitter_code.browse(cr, uid, transmitter_id, context=context)
            ship_to = transmitter.ship_to_id
            value['fis_order_code'] = ship_to.xml_id or False
            if ship_to.module == 'F34':
                if ship_to.id != ship_to_id:
                    value['fis_ship_to_id'] = ship_to.id or False
                if ship_to.fis_ship_to_parent_id.id != partner_id:
                    value['fis_partner_id'] = ship_to.fis_ship_to_parent_id.id or False
                domain['fis_ship_to_id'] = [('id','=',get_ids(ship_to.fis_ship_to_parent_id,'fis_ship_to_ids'))]
            elif ship_to.module == 'F33':
                partner = ship_to
                if partner.id != partner_id:
                    value['fis_partner_id'] = partner.id or False
                    if ship_to_id:
                        value['fis_ship_to_id'] = False
                domain['fis_ship_to_id'] = [('id','=',False)]
        return res


    def onload_set_transmitter_domain(self, cr, uid, ids, transmitter_id, partner_id, ship_to_id, context=None):
        domain = {
                'fis_transmitter_id': [('id','!=',False)],
                'fis_partner_id': [('fis_valid','=',True),('is_company','=',True),('fis_online_ordering_possible','=',True)],
                'fis_ship_to_id': [('is_company','=',False),('fis_online_ordering_enabled','=',True)],
                }
        res = {'domain': domain}
        if partner_id:
            res_partner = self.pool.get('res.partner')
            partner = res_partner.browse(cr, SUPERUSER_ID, partner_id, context=context)
            ship_tos = []
            ship_to_ids = []
            transmitter_ids = []
            for ship_to in (partner.fis_ship_to_ids or []):
                if ship_to.fis_transmitter_ids:
                    ship_tos.append(ship_to)
                    ship_to_ids.append(ship_to.id)
                    transmitter_ids.extend(get_ids(ship_to,'fis_transmitter_ids'))
            domain['fis_ship_to_id'] = [('id','in',ship_to_ids)]
        if ship_to_id:
            res_partner = self.pool.get('res.partner')
            ship_to = res_partner.browse(cr, SUPERUSER_ID, ship_to_id, context=context)
            domain['fis_ship_to_id'] = [('id','in',get_ids(ship_to,'fis_ship_to_parent_id','fis_ship_to_ids'))]
            transmitter_ids = get_ids(ship_to,'fis_transmitter_ids')
            if len(transmitter_ids) > 1:
                domain['fis_transmitter_id'] = [('id','in',transmitter_ids)]
        if transmitter_id:
            transmitter_code = self.pool.get('fis.transmitter_code')
            transmitter = transmitter_code.browse(cr, uid, transmitter_id, context=context)
            ship_to = transmitter.ship_to_id
            if ship_to.module == 'F34':
                domain['fis_ship_to_id'] = [('id','in',get_ids(ship_to,'fis_ship_to_parent_id','fis_ship_to_ids'))]
            elif ship_to.module == 'F33':
                partner = ship_to
                domain['fis_ship_to_id'] = [('id','=',False)]
        return res

    def write(self, cr, uid, ids, values, context=None):
        return super(res_users, self).write(cr, uid, ids, values, context=context)

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
                fields=['transmitter_name','transmitter_no','ship_to_xml_id'],
                context=context,
                ):
            if rec['ship_to_xml_id'] and rec['transmitter_name']:
                text = '%s [%s] %s' % (rec['transmitter_no'], rec['ship_to_xml_id'], rec['transmitter_name'])
            elif rec['ship_to_xml_id']:
                text = '%s [%s]' % (rec['transmitter_no'], rec['ship_to_xml_id'])
            elif rec['transmitter_name']:
                text = '%s -- %s' % (rec['transmitter_no'], rec['transmitter_name'])
            else:
                text = rec['transmitter_no']
            res[rec['id']] = text
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
            ),
        'transmitter_name': fields.char("Transmitter Name", size=128),
        'transmitter_no': fields.char('Transmitter #', size=6),
        'ship_to_id': fields.many2one('res.partner', 'Associated partner/shipping address record'),
        'ship_to_xml_id': fields.char('Ship-to FIS ID', size=11, oldname='xml_id'),
        }

    _sql_constraints = [
            ('transmitter_unique', 'unique(transmitter_no)', 'transmitter code already exists'),
            ]

    def write(self, cr, uid, ids, values, context=None):
        if 'transmitter_no' in values and not values['transmitter_no']:
            raise ERPError('No', 'not authorized to remove the transmitter number')
        return super(transmitter, self).write(cr, uid, ids, values, context=context)
