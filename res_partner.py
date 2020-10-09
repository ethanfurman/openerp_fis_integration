import logging
from collections import defaultdict
from itertools import groupby
from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.exceptions import ERPError
# from tools.misc import EnumNoAlias
from fnx_fs.fields import files
from VSS.address import normalize_address, Rise
from fnx.xid import xmlid

_logger = logging.getLogger(__name__)

ADDRESS_FIELDS = 'street', 'street2', 'city', 'state_id', 'zip', 'country_id'

class Specials(fields.SelectionEnum):
    _order_ = 'neither catalog specials both default'
    neither   = 'N', 'None'
    catalog   = 'C', 'Catalog'
    specials  = 'S', 'Specials Sheet'
    both      = 'B', 'Both'
    default   = 'D', 'Company'
    company   = default

class SpecialsType(fields.SelectionEnum):
    _order_ = 'soft hard'
    soft = 'Email'
    hard = 'Hardcopy'

class res_partner_keyword(osv.Model):
    """
    Provide keyword association for partner records.
    """
    _name = 'res.partner.keyword'

    _columns = {
        'name': fields.char('Keyword', size=32),
        'partner_ids': fields.many2many('res.partner', 'res_partner_partner_keyword', 'keyword_id', 'partner_id', 'Partners')
        }


class res_partner(xmlid, osv.Model):
    """
    Inherits partner and makes the external_id visible and modifiable
    """
    _name = 'res.partner'
    _inherit = ['res.partner', 'fnx_fs.fs', 'mail.thread']
    _mail_flat_thread = False

    _fnxfs_path = 'res_partner'
    _fnxfs_path_fields = ['xml_id', 'name']

    def _get_specials_type(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        children = self.browse(cr, uid, ids, context=context)
        children.sort(key=lambda r: r.parent_id.id)
        for parent, children in groupby(children, lambda c: c.parent_id):
            for child in children:
                if child.specials_notification == Specials.default:
                    res[child.id] = {}
                    for field in ('sn_catalog_type', 'sn_specials_type'):
                        if field in field_names:
                            res[child.id][field] = parent[field]
        return res

    def _get_child_ids(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        children_ids = []
        for partner in self.read(
                cr, uid, ids,
                fields=['is_company', 'child_ids', 'specials_notification', 'sn_catalog_type', 'sn_specials_type'],
                ):
            children_ids.extend(partner['child_ids'])
        return children_ids

    def _get_fis_address(self, cr, uid, ids, field_name, args, context=None):
        result = {}
        if not ids:
            return result
        datoms = self.browse(cr, uid, ids, context=context)
        for datom in datoms:
            name, street, street2 = datom.name, datom.street, datom.street2
            city, state_id, postal = datom.city, datom.state_id, datom.zip
            country_id = datom.country_id
            state = state_id and state_id.code or ''
            country = country_id and country_id.name or ''
            if country == 'United States':
                country = ''
            result[datom['id']] = '\n'.join([
                l
                for l in (
                    name or '',
                    street or '',
                    street2 or '',
                    ('%s %s' % (', '.join([f for f in (city, state) if f]), postal)).strip(),
                    country,
                    )
                if l.strip()
                ])
        return result

    def _get_transmitter_code_id(self, cr, uid, ids, field_name, args, context=None):
        # link records with FIS transmitter codes, if possible
        if isinstance(ids, (int, long)):
            ids = [ids]
        result = dict([(id, False) for id in ids])
        if not ids:
            return result
        xml_ids = dict([
            (r['id'], r['xml_id'])
            for r in self.read(
                    cr, uid,
                    [('id','in',ids),('xml_id','!=',False)],
                    fields=['id', 'xml_id'],
                    context=context,
                    )])
        ftc = self.pool.get('fis.transmitter_code')
        ftc_records = dict([
            (r['partner_xml_id'], r['id'])
            for r in ftc.read(
                    cr, SUPERUSER_ID,
                    [('partner_xml_id','in',xml_ids.values())],
                    context=context,
                    )])
        for id, xml_id in xml_ids.items():
            result[id] = ftc_records.get(xml_id, False)
        return result

    _columns = {
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'fis_valid': fields.boolean('Valid FIS code?'),
        'fis_active': fields.boolean('Active Partner?'),
        'name': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'street': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'street2': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'city': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'state_id': fields.many2one(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'zip': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'country_id':fields.many2one(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'email': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'phone': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'fax': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'mobile': fields.char(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'child_ids': fields.one2many(
            track_visibility='onchange',
            track_subtype='fis_integration.mt_fis_integration_contact'
            ),
        'specials_notification': fields.selection(
            Specials,
            string='Catelog Category',
            help='FIS Specials Notifications',
            oldname='special_notifications',
            ),
        'parent_specials_notification': fields.related(
            'parent_id', 'specials_notification',
            type='selection',
            selection=Specials,
            string='Company Catelog Category',
            help='FIS Specials Notifications',
            ),
        'sn_catalog_type': fields.function(
            _get_specials_type,
            fnct_inv=True,
            type='selection',
            selection=SpecialsType,
            string='Catalog',
            multi='specials',
            store={
                'res.partner': (_get_child_ids, ['specials_notification', 'sn_catalog_type', 'sn_specials_type'], 10),
                },
            ),
        'sn_specials_type': fields.function(
            _get_specials_type,
            fnct_inv=True,
            type='selection',
            selection=SpecialsType,
            string='Specials',
            multi='specials',
            store={
                'res.partner': (_get_child_ids, ['specials_notification', 'sn_catalog_type', 'sn_specials_type'], 10),
                },
            oldname='sn_special_type',
            ),
        'parent_name': fields.related('parent_id', 'name', type='char', string='Related'),
        'keyword_ids': fields.many2many(
            'res.partner.keyword',
            'res_partner_partner_keyword', 'partner_id', 'keyword_id',
            'Keywords',
            ),
        'fis_csms_terms': fields.many2one('fis.account.customer_terms', 'Terms'),
        'fis_credit_limit': fields.float('Credit Limit'),
        'fis_credit_current': fields.float('Current Balance'),
        'fis_credit_10_days': fields.float('10 Day Balance'),
        'fis_credit_20_days': fields.float('20 Day Balance'),
        'fis_credit_30_days': fields.float('30 Day Balance'),
        'fis_credit_total': fields.float('Total Balance'),
        'fis_price_list': fields.char('Price list code', size=1),
        'fis_portal_logins' : fields.one2many( 'res.users', 'fis_partner_id', string='FIS logins'),
        'fis_org_cert': fields.boolean(
            'Organic Cert?',
            ),
        'fis_org_cert_file': fields.boolean(
            'Organic Cert on file?',
            oldname='sp_org_cert_file',
            ),
        'fis_org_exp': fields.date(
            'Organic Cert expiration',
            oldname='sp_org_exp',
            ),
        'fis_non_gmo': fields.boolean(
            'Non-GMO vendor?',
            oldname='sp_non_gmo',
            ),
        'fis_gmo_exp': fields.date(
            'GMO expiration',
            oldname='sp_gmo_exp',
            ),
        'fis_kosher': fields.boolean(
            'Kosher?',
            oldname='sp_kosher',
            ),
        'fis_kosher_exp': fields.date(
            'Kosher expiration',
            oldname='sp_kosher_exp',
            ),
        'is_carrier': fields.boolean('Carrier', help='This partner is used for shipping.'),
        'warehouse_comment': fields.text('Warehouse Notes'),
        'fuel_surcharge': fields.boolean('Fuel surcharge'),
        'department': fields.char('Department', size=128),
        'email2': fields.char('Alt. Email', size=240),
        'facebook': fields.char('Facebook', size=240),
        'twitter': fields.char('Twitter', size=240),
        'is_bulk': fields.boolean('Bulk Sets', help='This partner has a bulk set installation.'),
        'bulk_img0': fields.binary('Bulk Image', help='Picture of bulk installation.', oldname='bulk_img'),
        'bulk_img1': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img2': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img3': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img4': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img5': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img6': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img7': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img8': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_img9': fields.binary('Bulk Image', help='Picture of bulk installation.'),
        'bulk_pdf': fields.binary(string='Bulk Contract', help='PDF of contract.'),
        'bulk_pdf_filename': fields.char('Bulk PDF Filename'),
        'fis_data_address': fields.function(
            _get_fis_address,
            type='text',
            string='FIS Name & Address',
            oldname='fis_data',
            store={
                'res.partner': (
                    lambda s, c, u, ids, ctx=None: ids,
                    ['name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id'],
                    10,
                    )},
            ),
        'fis_data_address_changed': fields.boolean('FIS data has changed', oldname='fis_data_changed'),
        'fis_updated_by_user': fields.char('Updated by user', size=12, oldname='updated_by_user'),
        # online order facilatation (attached to F33 and F34 records)
        'fis_transmitter_id': fields.many2one(
                'fis.transmitter_code',
                string='FIS Transmitter ID',
                oldname='fis_transmitter_code_id',
                ),
        'fis_transmitter_no': fields.related(
                'fis_transmitter_id', 'transmitter_no',
                string='Transmitter No',
                type='char',
                size=6,
                oldname='fis_transmitter_code',
                ),
        # shipping addresses
        'fis_ship_to_parent_id': fields.many2one('res.partner', 'Related Ship-To'),                       # F34
        'fis_ship_to_ids': fields.one2many('res.partner', 'fis_ship_to_parent_id', 'Ship-To Addresses'),  # F33
        'fis_ship_to_code': fields.char('Ship-To Code', size=7),                                          # F34
        # miscellany
        'fnxfs_files': files('general', string='Available Files'),
        'create_date': fields.datetime('Created', readonly=True),
        'create_uid': fields.many2one('res.users', string='Created by', readonly=True),
        'write_date': fields.datetime('Last changed', readonly=True),
        'write_uid': fields.many2one('res.users', string='Last changed by', readonly=True),
        }

    _defaults = {
        'specials_notification': Specials.neither,
        }

    def create(self, cr, uid, values, context=None):
        if 'code' in (values.get('zip', False) or ''):
            raise ERPError('data verification error', 'invalid zip code %r for record %r' % (values['zip'], values))
        if context is None:
            context = {}
        if 'child_ids' in values:
            for _, _, cvals in values['child_ids']:
                if cvals['specials_notification'] == Specials.company:
                    cvals['sn_catalog_type'] = values.get('sn_catalog_type', False)
                    cvals['sn_specials_type'] = values.get('sn_specials_type', False)
        new_id = super(res_partner, self).create(cr, uid, values, context=context)
        if values.get('user_id'):
            # salesperson has been given, assign them as a follower
            self.message_subscribe_users(cr, uid, [new_id], values['user_id'])
        return new_id

    def write(self, cr, uid, ids, values, context=None):
        if 'fis_transmitter_no' in values and not values['fis_transmitter_no']:
            raise ERPError('No', 'not authorized to remove the transmitter number')
        if 'code' in (values.get('zip', False) or ''):
            raise ERPError('data verification error', 'invalid zip code %r for ids %r' % (values['zip'], ids))
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        context = context.copy()
        updating_from_fis = context.pop('fis-updates', False)
        datas = self.read(
                cr, uid, ids,
                fields=['id', 'name', 'fis_updated_by_user', 'fis_data_address', 'is_company',
                        'specials_notification', 'sn_catalog_type', 'sn_specials_type', 'user_id',
                        ],
                context=context,
                )
        # datas is a list of dicts
        #
        # first check for changing sales person
        #
        if 'user_id' in values:
            new_rep = values['user_id']
            for data in datas:
                old_rep = data['user_id']
                if old_rep != new_rep:
                    # unfollow from old sales rep
                    if old_rep:
                        self.message_unsubscribe_users(cr, uid, data['id'], data['user_id'][0], context=context)
                    # and follow from new sales rep
                    if new_rep:
                        self.message_subscribe_users(cr, uid, data['id'], values['user_id'], context=context)
        #
        # then branch depending on source
        #
        if updating_from_fis:
            if any(f in values for f in ADDRESS_FIELDS+('specials_notifications','name')):
                # if any address fields set, data must be a dict
                #
                # save name/addr/cszc into fis_data_address field
                # if record has fis_updated_by_user set do not update name/addr/cszc
                #
                # save the records individually
                for data in datas:
                    piecemeal_values = values.copy()
                    updated_by_user = data['fis_updated_by_user'] or ''
                    if 'S' in updated_by_user:
                        piecemeal_values.pop('specials_notification', None)
                    if 'N' in updated_by_user:
                        piecemeal_values.pop('name', None)
                    if 'A' in updated_by_user:
                        piecemeal_values['fis_data_address_changed'] = True
                        for attr in ADDRESS_FIELDS:
                            piecemeal_values.pop(attr, None)
                    if not super(res_partner, self).write(cr, uid, data['id'], piecemeal_values, context=context):
                        return False
                return True
        else:
            if 'fis_updated_by_user' not in values:
                # we only care if a latched field is being updated
                check_fis = ''
                if 'name' in values:
                    check_fis += 'N'
                for field in ADDRESS_FIELDS:
                    if field in values:
                        check_fis += 'A'
                        break
                if 'specials_notification' in values:
                    check_fis += 'S'
                if check_fis:
                    # okay, we really only care if any the records to update are FIS records
                    if any(d['fis_data_address'] for d in datas):
                        for data in datas:
                            piecemeal_values = values.copy()
                            if data['fis_data_address']:
                                # definitely an FIS record
                                updated_by_user = data['fis_updated_by_user'] or ''
                                if 'N' in check_fis:
                                    updated_by_user += 'N'
                                if 'A' in check_fis:
                                    updated_by_user += 'A'
                                if 'S' in check_fis:
                                    updated_by_user += 'S'
                                piecemeal_values['fis_updated_by_user'] = ''.join(sorted(set(updated_by_user)))
                            if not super(res_partner, self).write(cr, uid, data['id'], piecemeal_values, context=context):
                                return False
                        return True
        return super(res_partner, self).write(cr, uid, ids, values, context=context)

    def fnxfs_folder_name(self, records):
        "return name of folder to hold related files"
        res = {}
        for record in records:
            res[record['id']] = record['xml_id'] or ("%s-%d" % (record['name'], record['id']))
        return res

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(res_partner, self).name_get(cr, uid, ids, context=context)
        show_fis = (context or {}).get('show_fis')
        if not show_fis:
            return res
        res = dict(res)
        new_res = []
        for data in self.read(cr, uid, ids, fields=['id', 'xml_id', 'module', 'user_ids'], context=context):
            id = data['id']
            xml_id = data['xml_id']
            module = data['module']
            user_ids = data['user_ids']
            name = res[id]
            if xml_id:
                if not user_ids or show_fis:
                    if module in ('F33', 'F65', 'F163'):
                        name = '[%s] %s' % (xml_id, name)
                    elif '_' in module:
                        name = '[%s] %s' % (module.split('_', 1)[1].upper(), name)
                    else:
                        name = '[%s] %s' % (module.upper(), name)
            new_res.append((id, name))
        return new_res

    def onchange_type(self, cr, uid, ids, is_company, notify, catalog, specials, context=None):
        res = super(res_partner, self).onchange_type(cr, uid, ids, is_company, context=context)
        if is_company and notify == Specials.company:
            # just promoted to company status, but currently set to follow old company's
            # notification policy
            value = res.setdefault('value', {})
            if catalog and specials:
                value['specials_notification'] = Specials.both
            elif catalog:
                value['specials_notification'] = Specials.catalog
            elif specials:
                value['specials_notification'] = Specials.special
            else:
                value['specials_notification'] = Specials.none
        return res

    def onchange_specials_notification(self, cr, uid, ids, notify, parent_id, context=None):
        res = {'value': {}, 'domain':{}}
        if notify == Specials.catalog:
            # remove specials
            res['value']['sn_specials_type'] = False
        elif notify == Specials.specials:
            # remove catalog
            res['value']['sn_catalog_type'] = False
        elif notify == Specials.company:
            # does this contact have a company?
            if not parent_id:
                res['warning'] = warning = {}
                warning['title'] = 'Invalid selection'
                warning['message'] = "Cannot choose 'Company'."
                res['value']['specials_notification'] = False
            # follow parent (or null parent)
            parent = self.browse(cr, uid, parent_id, context=context)
            res['value']['sn_specials_type'] = parent.sn_specials_type
            res['value']['sn_catalog_type'] = parent.sn_catalog_type
            if not parent_id:
                res['value']['specials_notification'] = Specials.neither
        return res


    def rp_remove_dups(self, cr, uid, *args):
        print("starting")
        ids = self.search(cr, uid, [])
        records = self.browse(cr, uid, ids)
        dup_lists = defaultdict(list)
        for i, rec in enumerate(records):
            if not i % 100:
                print("%d records sorted" % i)
            street, street2 = Rise(normalize_address(rec.street or ''), normalize_address(rec.street2 or ''))
            key = rec.supplier, rec.customer, rec.name, street, street2, rec.city, rec.state_id, rec.country_id, rec.zip
            if rec.supplier or rec.customer:
                dup_lists[key].append(rec)
        removed = 0
        print("checking %d possible groups..." % len(dup_lists))
        for i, batch in enumerate(dup_lists.values()):
            if not i % 100:
                print("%d processed" % i)
            to_kill = []
            to_save = []
            for rec in batch:
                if rec.xml_id and not to_save:
                    to_save.append(rec)
                else:
                    to_kill.append(rec)
            if not to_save:
                to_kill.pop()   # save one
            for rec in to_kill:
                self.unlink(cr, uid, [rec.id])
                removed += 1
        print("%d duplicates removed" % removed)
        return True

