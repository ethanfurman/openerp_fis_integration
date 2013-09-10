import logging
from osv import osv, fields
from fnx.BBxXlate.fisData import fisData
from fnx.utils import cszk, fix_phone, fix_date, Rise, Sift, AddrCase, NameCase, BsnsCase
from fnx import xid, check_company_settings

_logger = logging.getLogger(__name__)

CONFIG_ERROR = "Cannot sync products until  Settings --> Configuration --> FIS Integration --> %s  has been specified."

class F65(object):
    "Vendor Master"
    company_id = 'An$(1,2)'
    code = 'An$(3,6)'
    name = 'Bn$'
    addr1 = 'Cn$'
    addr2 = 'Dn$'
    addr3 = 'En$'
    tele = 'Gn$'
    org_cert = 'In$(5,1)'
    fax = 'In$(29,10)'
    contact = 'In$(39,15)'
    org_cert_file = 'In$(54,1)'
    cert_exp = 'In$(55,6)'
F65 = F65()

class F163(object):
    "Supplier Master"
    company_id = 'An$(1,2)'
    code = 'An$(3,6)'
    name = 'Bn$'
    addr1 = 'Cn$'
    addr2 = 'Dn$'
    addr3 = 'En$'
    tele = 'Gn$'
    fax = 'Hn$'
    vendor = 'In$(10,6)'
    org_cert_file = 'Mn$(1,1)'
    non_gmo = 'Mn$(2,1)'
    kosher = 'Mn$(6,1)'
    cert_exp = 'Nn$(1,6)'
    gmo_exp = 'Nn$(7,6)'
    kosher_exp = 'Nn$(36,6)'
F163 = F163()

class res_partner(osv.Model):
    "Inherits partner and makes the external_id visible and modifiable"
    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('supplier_integration', 'Supplier/Vendor Module', CONFIG_ERROR),
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg=('supplier_integration', 'Supplier/Vendor Module', CONFIG_ERROR),
            string="External ID",
            type='char',
            method=False,
            fnct_search=lambda s, c, u, m, n, d, context=None:
                            xid.search_xml_id(s, c, u, m, n, d, ('supplier_integration','Supplier/Vendor Integration',CONFIG_ERROR), context=context),
            ),
        'sp_tele': fields.char(
            'Telephone',
            size=20,
            ),
        'sp_fax': fields.char(
            'Fax',
            size=20,
            ),
        'sp_org_cert_file': fields.boolean(
            'Organic Cert on file?',
            ),
        'sp_org_exp': fields.date(
            'Cert expiration',
            ),
        'sp_non_gmo': fields.boolean(
            'Non-GMO vendor?',
            ),
        'sp_gmo_exp': fields.date(
            'GMO expiration',
            ),
        'sp_kosher': fields.boolean(
            'Kosher?',
            ),
        'sp_kosher_exp': fields.date(
            'Kosher expiration',
            ),
        'vn_tele': fields.char(
            'Telephone',
            size=20,
            ),
        'vn_fax': fields.char(
            'Fax',
            size=20,
            ),
        'vn_org_cert': fields.boolean(
            'Organic Cert?',
            ),
        'vn_org_cert_file': fields.boolean(
            'Organic Cert on file?',
            ),
        'vn_org_exp': fields.date(
            'Cert expiration',
            ),
        }

    def fis_updates(self, cr, uid, *args):
        _logger.info("res_partner.fis_updates starting...")
        settings = check_company_settings(self, cr, uid, ('supplier_integration', 'Supplier/Vendor Module', CONFIG_ERROR))
        context = {'module': settings['supplier_integration']}
        state_table = self.pool.get('res.country.state')
        state_recs = state_table.browse(cr, uid, state_table.search(cr, uid, [(1,'=',1)]))
        state_recs = dict([(r.name, (r.id, r.code, r.country_id.id)) for r in state_recs])
        #state_recs = dict([(r['name'], (r['id'], r['code'], r['country_id.id'])) for r in state_recs])
        country_table = self.pool.get('res.country')
        country_recs = country_table.browse(cr, uid, country_table.search(cr, uid, [(1,'=',1)]))
        country_recs_code = dict([(r['code'], r['id']) for r in country_recs])
        country_recs_name = dict([(r['name'], r['id']) for r in country_recs])
        supplier_recs = self.browse(cr, uid, self.search(cr, uid, [(1,'=',1)]))
        supplier_codes = dict([(r['xml_id'], r['id']) for r in supplier_recs])
        vnms = fisData(65, keymatch='10%s')
        posm = fisData(163, keymatch='10%s')

        for sup_rec in posm:
            result = {}
            result['is_company'] = True
            result['supplier'] = True
            result['customer'] = False
            result['use_parent_address'] = False
            result['xml_id'] = key = sup_rec[F163.code]
            result['name'] = BsnsCase(sup_rec[F163.name])
            addr1, addr2, addr3 = Sift(sup_rec[F163.addr1], sup_rec[F163.addr2], sup_rec[F163.addr3])
            addr2, city, state, postal, country = cszk(addr2, addr3)
            addr3 = ''
            if city and not (addr2 or state or postal or country):
                addr2, city = city, addr2
            addr1, addr2 = AddrCase(addr1, addr2)
            city = NameCase(city)
            state, country = NameCase(state), NameCase(country)
            result['street'] = addr1
            result['street2'] = addr2
            result['city'] = city
            result['zip'] = postal
            if state:
                result['state_id'] = state_recs[state][0]
                result['country_id'] = state_recs[state][2]
            elif country:
                country_id = country_recs_name.get(country, None)
                if country_id is None:
                    _logger.critical("Vendor %s has invalid country <%r> -- skipping" % (key, country))
                    continue
            result['sp_tele'] = fix_phone(sup_rec[F163.tele])
            result['sp_fax'] = fix_phone(sup_rec[F163.fax])
            result['sp_org_cert_file'] = sup_rec[F163.org_cert_file] in 'YO'
            result['sp_org_exp'] = fix_date(sup_rec[F163.cert_exp])
            result['sp_non_gmo'] = sup_rec[F163.non_gmo] in 'Y'
            result['sp_gmo_exp'] = fix_date(sup_rec[F163.gmo_exp])
            result['sp_kosher'] = sup_rec[F163.kosher] in 'Y'
            result['sp_kosher_exp'] = fix_date(sup_rec[F163.kosher_exp])
            ven_rec = vnms[sup_rec[F163.vendor]]
            if ven_rec is None:
                result['vn_tele'] = ''
                result['vn_fax'] = ''
                result['vn_org_cert'] = ''
                result['vn_org_cert_file'] = ''
                result['vn_org_exp'] = None
            else:
                result['vn_tele'] = fix_phone(ven_rec[F65.tele])
                result['vn_fax'] = fix_phone(ven_rec[F65.fax])
                result['vn_org_cert'] = ven_rec[F65.org_cert] in 'Y'
                result['vn_org_cert_file'] = ven_rec[F65.org_cert_file] in 'Y'
                result['vn_org_exp'] = fix_date(ven_rec[F65.cert_exp])
            if key in supplier_codes:
                id = supplier_codes[key]
                self.write(cr, uid, id, result, context=context)
            else:
                new_id = self.create(cr, uid, result, context=context)
            if ven_rec is not None:
                contact = ven_rec[F65.contact]
                if contact:
                    result = {}
                    result['name'] = NameCase(contact)
                    result['is_company'] = False
                    result['use_parent_address'] = True
                    result['xml_id'] = key = 'cntct_' + key
                    if key in supplier_codes:
                        id = supplier_codes[key]
                        self.write(cr, uid, id, result, context=context)
                    else:
                        self.create(cr, uid, result, context=context)

        _logger.info('res_partner.fis_updates done!')
        return True

res_partner()
