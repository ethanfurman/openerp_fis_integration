import logging
from collections import defaultdict
from osv import osv, fields
from fnx.BBxXlate.fisData import fisData
from fnx.utils import cszk, fix_phone, fix_date, Rise, Sift, AddrCase, NameCase, BsnsCase, normalize_address
from fnx import xid, enum

_logger = logging.getLogger(__name__)

class FISenum(str, enum.Enum):
    pass

class F33(FISenum):
    'Customer Master'
    code =      'An$(3,6)'
    name =      'Bn$'
    addr1 =     'Cn$'
    addr2 =     'Dn$'
    addr3 =     'En$'
    postal =    'Ln$'
    tele =      'Gn$(20,10)'
    contact =   'Kn$'

class F65(FISenum):
    "Vendor Master"
    company_id =    'An$(1,2)'
    code =          'An$(3,6)'
    name =          'Bn$'
    addr1 =         'Cn$'
    addr2 =         'Dn$'
    addr3 =         'En$'
    tele =          'Gn$'
    org_cert =      'In$(5,1)'
    fax =           'In$(29,10)'
    contact =       'In$(39,15)'
    org_cert_file = 'In$(54,1)'
    cert_exp =      'In$(55,6)'

class F163(FISenum):
    "Supplier Master"
    company_id =    'An$(1,2)'
    code =          'An$(3,6)'
    name =          'Bn$'
    addr1 =         'Cn$'
    addr2 =         'Dn$'
    addr3 =         'En$'
    tele =          'Gn$'
    fax =           'Hn$'
    vendor =        'In$(10,6)'
    org_cert_file = 'Mn$(1,1)'
    non_gmo =       'Mn$(2,1)'
    kosher =        'Mn$(6,1)'
    cert_exp =      'Nn$(1,6)'
    gmo_exp =       'Nn$(7,6)'
    kosher_exp =    'Nn$(36,6)'

class res_partner(osv.Model):
    "Inherits partner and makes the external_id visible and modifiable"
    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
        'xml_id': fields.function(
            xid.get_xml_ids,
            arg=('F33', 'F65', 'F163', 'FIS_now', 'FIS_unfi'),
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg=('F33', 'F65', 'F163', 'FIS_now', 'FIS_unfi'),
            string="FIS ID",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
            ),
        'module': fields.function(
            xid.get_xml_ids,
            arg=('F33', 'F65', 'F163', 'FIS_now', 'FIS_unfi'),
            fnct_inv=xid.update_xml_id,
            fnct_inv_arg=('F33', 'F65', 'F163', 'FIS_now', 'FIS_unfi'),
            string="FIS Module",
            type='char',
            method=False,
            fnct_search=xid.search_xml_id,
            multi='external',
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
        state_table = self.pool.get('res.country.state')
        state_recs = state_table.browse(cr, uid, state_table.search(cr, uid, [(1,'=',1)]))
        state_recs = dict([(r.name, (r.id, r.code, r.country_id.id)) for r in state_recs])
        #state_recs = dict([(r['name'], (r['id'], r['code'], r['country_id.id'])) for r in state_recs])
        country_table = self.pool.get('res.country')
        country_recs = country_table.browse(cr, uid, country_table.search(cr, uid, []))
        country_recs_code = dict([(r.code, r.id) for r in country_recs])
        country_recs_name = dict([(r.name, r.id) for r in country_recs])
        supplier_recs = self.browse(cr, uid, self.search(cr, uid, [('module','=','F163')]))
        supplier_codes = dict([(r.xml_id, r.id) for r in supplier_recs])
        customer_recs = self.browse(cr, uid, self.search(cr, uid, [('module','=','F33')]))
        customer_codes = dict([(r.iml_id, r.id) for r in customer_recs])
        vnms = fisData(65, keymatch='10%s')
        posm = fisData(163, keymatch='10%s')
        csms = fisData(33, keymatch='10%s ')

        for sup_rec in posm:
            result = {}
            result['is_company'] = True
            result['supplier'] = True
            result['customer'] = False
            result['use_parent_address'] = False
            result['xml_id'] = key = sup_rec[F163.code]
            result['module'] = 'F163'
            result['name'] = BsnsCase(sup_rec[F163.name])
            addr1, addr2, addr3 = Sift(sup_rec[F163.addr1], sup_rec[F163.addr2], sup_rec[F163.addr3])
            addr2, city, state, postal, country = cszk(addr2, addr3)
            addr3 = ''
            if city and not (addr2 or state or postal or country):
                addr2, city = city, addr2
            addr1 = normalize_address(addr1)
            addr2 = normalize_address(addr2)
            addr1, addr2 = AddrCase(Rise(addr1, addr2))
            city = NameCase(city)
            state, country = NameCase(state), NameCase(country)
            result['street'] = addr1
            result['street2'] = addr2
            result['city'] = city
            result['zip'] = postal
            result['country_id'] = False
            result['state_id'] = False
            if state:
                result['state_id'] = state_recs[state][0]
                result['country_id'] = state_recs[state][2]
            elif country:
                country_id = country_recs_name.get(country, None)
                if country_id is None:
                    _logger.critical("Supplier %s has invalid country <%r>" % (key, country))
                else:
                    result['country_id'] = country_id
            result['sp_tele'] = fix_phone(sup_rec[F163.tele])
            result['sp_fax'] = fix_phone(sup_rec[F163.fax])
            result['sp_org_cert_file'] = sup_rec[F163.org_cert_file] in 'YO'
            result['sp_org_exp'] = fix_date(sup_rec[F163.cert_exp])
            result['sp_non_gmo'] = sup_rec[F163.non_gmo] in 'Y'
            result['sp_gmo_exp'] = fix_date(sup_rec[F163.gmo_exp])
            result['sp_kosher'] = sup_rec[F163.kosher] in 'Y'
            result['sp_kosher_exp'] = fix_date(sup_rec[F163.kosher_exp])
            ven_rec = vnms.get(sup_rec[F163.vendor])
            vendor_info = {}
            vendor_address_score = 0
            if ven_rec is None:
                result['vn_tele'] = ''
                result['vn_fax'] = ''
                result['vn_org_cert'] = ''
                result['vn_org_cert_file'] = ''
                result['vn_org_exp'] = None
            else:
                result['name'] = result['name'] or BsnsCase(ven_rec[F65.name])
                if not result['country_id']:
                    supplier_address_score = 0
                else:
                    supplier_address_score = sum([1 for datum in 
                        (result['street'], result['street2'], result['city'], result['zip'], result['state_id'], result['country_id'])
                        if datum])
                addr1, addr2, addr3 = Sift(sup_rec[F65.addr1], sup_rec[F65.addr2], sup_rec[F65.addr3])
                addr2, city, state, postal, country = cszk(addr2, addr3)
                addr3 = ''
                if city and not (addr2 or state or postal or country):
                    addr2, city = city, addr2
                addr1 = normalize_address(addr1)
                addr2 = normalize_address(addr2)
                addr1, addr2 = AddrCase(Rise(addr1, addr2))
                city = NameCase(city)
                state, country = NameCase(state), NameCase(country)
                vendor_info['street'] = addr1
                vendor_info['street2'] = addr2
                vendor_info['city'] = city
                vendor_info['zip'] = postal
                vendor_info['country_id'] = False
                vendor_info['state_id'] = False
                if state:
                    vendor_info['state_id'] = state_recs[state][0]
                    vendor_info['country_id'] = state_recs[state][2]
                elif country:
                    country_id = country_recs_name.get(country, None)
                    if country_id is None:
                        _logger.critical("Vendor %s has invalid country <%r>" % (key, country))
                    else:
                        vendor_info['country_id'] = country_id
                if vendor_info['country_id']:
                    vendor_address_score = sum([1 for datum in 
                        (result['street'], result['street2'], result['city'], result['zip'], result['state_id'], result['country_id'])
                        if datum])
                result['vn_tele'] = fix_phone(ven_rec[F65.tele])
                result['vn_fax'] = fix_phone(ven_rec[F65.fax])
                result['vn_org_cert'] = ven_rec[F65.org_cert] in 'Y'
                result['vn_org_cert_file'] = ven_rec[F65.org_cert_file] in 'Y'
                result['vn_org_exp'] = fix_date(ven_rec[F65.cert_exp])
            if vendor_address_score > supplier_address_score:
                result.update(vendor_info)
            if not result['name']:
                _logger.critical("Missing name for %s -- skipping" % (key, ))
                continue
            if key in supplier_codes:
                id = supplier_codes[key]
                self.write(cr, uid, id, result)
            else:
                new_id = self.create(cr, uid, result)
                supplier_codes[key] = new_id
            if ven_rec is not None:
                contact = ven_rec[F65.contact]
                if contact:
                    result = {}
                    result['name'] = NameCase(contact)
                    result['is_company'] = False
                    result['use_parent_address'] = True
                    result['xml_id'] = key = 'cntct_' + key
                    result['module'] = 'F163'
                    if key in supplier_codes:
                        id = supplier_codes[key]
                        self.write(cr, uid, id, result)
                    else:
                        new_id = self.create(cr, uid, result)
                        supplier_codes[key] = new_id

        for cus_rec in csms:
            result = {}
            result['is_company'] = True
            result['supplier'] = False
            result['customer'] = True
            result['use_parent_address'] = False
            result['xml_id'] = key = cus_rec[F33.code]
            result['module'] = 'F33'
            result['name'] = BsnsCase(cus_rec[F33.name])
            addr1, addr2, addr3 = Sift(cus_rec[F33.addr1], cus_rec[F33.addr2], cus_rec[F33.addr3])
            addr2, city, state, postal, country = cszk(addr2, addr3)
            addr3 = ''
            if city and not (addr2 or state or postal or country):
                addr2, city = city, addr2
            addr1 = normalize_address(addr1)
            addr2 = normalize_address(addr2)
            addr1, addr2 = AddrCase(Rise(addr1, addr2))
            city = NameCase(city)
            state, country = NameCase(state), NameCase(country)
            result['street'] = addr1
            result['street2'] = addr2
            result['city'] = city
            result['zip'] = postal
            result['country_id'] = False
            result['state_id'] = False
            if state:
                result['state_id'] = state_recs[state][0]
                result['country_id'] = state_recs[state][2]
            elif country:
                country_id = country_recs_name.get(country, None)
                if country_id is None:
                    _logger.critical("Customer %s has invalid country <%r>" % (key, country))
                    continue
                else:
                    result['country_id'] = country_id
            result['phone'] = fix_phone(cus_rec[F33.tele])
            if not result['name']:
                _logger.critical("Missing name for %s -- skipping" % (key, ))
                continue
            if key in customer_codes:
                id = customer_codes[key]
                self.write(cr, uid, id, result)
            else:
                new_id = self.create(cr, uid, result)
                customer_codes[key] = new_id
            if cus_rec[F33.contact]:
                contact = cus_rec[F33.contact]
                result = {}
                result['name'] = NameCase(contact)
                result['is_company'] = False
                result['use_parent_address'] = True
                result['xml_id'] = key = 'cntct_' + key
                result['module'] = 'F33'
                if key in customer_codes:
                    id = customer_codes[key]
                    self.write(cr, uid, id, result)
                else:
                    new_id = self.create(cr, uid, result)
                    customer_codes[key] = new_id


        _logger.info('res_partner.fis_updates done!')
        return True

    def rp_remove_dups(self, cr, uid, *args):
        print "starting"
        ids = self.search(cr, uid, [])
        records = self.browse(cr, uid, ids)
        dup_lists = defaultdict(list)
        for i, rec in enumerate(records):
            if not i % 100:
                print "%d records sorted" % i
            street, street2 = Rise(normalize_address(rec.street or ''), normalize_address(rec.street2 or ''))
            key = rec.supplier, rec.customer, rec.name, street, street2, rec.city, rec.state_id, rec.country_id, rec.zip
            if rec.supplier or rec.customer:
                dup_lists[key].append(rec)
        total_count = 0
        removed = 0
        print "checking %d possible groups..." % len(dup_lists)
        for i, batch in enumerate(dup_lists.values()):
            if not i % 100:
                print "%d processed" % i
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
        print "%d duplicates removed" % removed
        return True

res_partner()
