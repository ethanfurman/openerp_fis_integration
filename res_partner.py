import logging
import re
from collections import defaultdict
from osv import osv, fields
# from tools.misc import EnumNoAlias
from fis_integration.fis_schema import F27, F33, F47, F65, F74, F163
from VSS.address import cszk, normalize_address, Rise, Sift, AddrCase, NameCase, BsnsCase
from VSS.BBxXlate.fisData import fisData
from VSS.utils import fix_phone, fix_date, var, Date
from fnx.xid import xmlid

_logger = logging.getLogger(__name__)

ADDRESS_FIELDS = 'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id'

class Specials(fields.SelectionEnum):
    catalog   = 'C', 'Catalog'
    specials  = 'S', 'Specials Sheet'
    both      = 'B', 'Both'


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
    _inherit = 'res.partner'

    _columns = {
        'xml_id': fields.char('FIS ID', size=16, readonly=True),
        'module': fields.char('FIS Module', size=16, readonly=True),
        'fis_valid': fields.boolean('Valid FIS code?'),
        'fis_active': fields.boolean('Active Partner?'),
        'special_notifications': fields.selection(Specials, 'Special Notifications'),
        'parent_name': fields.related('parent_id', 'name', type='char', string='Related'),
        'keyword_ids': fields.many2many(
            'res.partner.keyword',
            'res_partner_partner_keyword', 'partner_id', 'keyword_id',
            'Keywords',
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
        'fis_data': fields.text('FIS Name & Address'),
        'fis_data_changed': fields.boolean('FIS data has changed'),
        'updated_by_user': fields.boolean('Updated by user'),
        }

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        if 'xml_id' in values and 'module' in values and values['xml_id'] and values['module']:
            # we have an FIS record -- add appropriate fields
            # save name/addr/cszc into fis_data field
            state = self.pool.get('res.country.state').browse(cr, uid, values.get('state_id'), context=context)
            country = self.pool.get('res.country').browse(cr, uid, values.get('country_id'), context=context)
            values['fis_data'] = '\n'.join([
                    values['name'] or '',
                    values.get('street', ''),
                    values.get('street2', ''),
                    '%s, %s  %s' % (
                        values.get('city', ''),
                        state and state.name or '',
                        values.get('zip', ''),
                        ),
                    country and country.name or '',
                    ])
        return super(res_partner, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        if context is None:
            context = {}
        context = context.copy()
        updating_from_fis = context.pop('fis-updates', False)
        data = self.read(cr, uid, ids, fields=['id', 'updated_by_user', 'fis_data'], context=context)
        if updating_from_fis:
            # save name/addr/cszc into fis_data field
            # if record has updated_by_user set do not update name/addr/cszc
            # ids is a single integer
            state = self.pool.get('res.country.state').browse(cr, uid, values.get('state_id'), context=context)
            country = self.pool.get('res.country').browse(cr, uid, values.get('country_id'), context=context)
            values['fis_data'] = '\n'.join([
                    values['name'] or '',
                    values.get('street', ''),
                    values.get('street2', ''),
                    '%s, %s  %s' % (
                        values.get('city', ''),
                        state and state.name or '',
                        values.get('zip', ''),
                        ),
                    country and country.name or '',
                    ])
            if data['updated_by_user']:
                if data['fis_data'] and values['fis_data'] != data['fis_data']:
                    values['fis_data_changed'] = True
                for attr in ADDRESS_FIELDS:
                    values.pop(attr, None)
        else:
            # at this point data is either a dict or a list of dicts
            # we only care if an address field is being updated
            check_if_fis = False
            for field in ADDRESS_FIELDS:
                if field in values:
                    check_if_fis = True
                    break
            if check_if_fis:
                # an address field is being updated -- is the record(s) an FIS record?
                if isinstance(ids, (int, long)):
                    # only one record, data is a dict
                    if data['fis_data']:
                        data['updated_by_user'] = True
                else:
                    # list of dicts
                    fis_ids = []
                    ids = []
                    for d in data:
                        target = (ids, fis_ids)[bool(d['fis_data'])]
                        target.append(d['id'])
                    success = True
                    if ids:
                        # write non-fis records
                        success = super(res_partner, self).write(cr, uid, ids, values, context=context)
                    if fis_ids and success:
                        # update and write fis records
                        values['updated_by_user'] = True
                        success = super(res_partner, self).write(cr, uid, fis_ids, values, context=context)
                    return success
        return super(res_partner, self).write(cr, uid, ids, values, context=context)

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

    def fis_updates(self, cr, uid, partner=None, shipper=None, *args):
        context = {'hr_welcome': False}
        inactive_too = {'active_test': False}
        if partner is shipper is None:
            _logger.info("res_partner.fis_updates starting...")
            # reset valid fields to False
            # all_ids = self.search(cr, uid, [], context=inactive_too)
            # self.write(cr, uid, all_ids, {'fis_valid': False})
        else:
            _logger.info('res_partner.fis_updates: looking for %s' % (partner or shipper))
        if partner and shipper:
            raise ValueError('only one of <partner> or <shipper> may be specified (received %r and %r)' % (partner, shipper))
        context = {}
        state_table = self.pool.get('res.country.state')
        state_recs = state_table.browse(cr, uid, state_table.search(cr, uid, [(1,'=',1)]), context=context)
        state_recs = dict([(r.name, (r.id, r.code, r.country_id.id)) for r in state_recs])
        country_table = self.pool.get('res.country')
        country_recs = country_table.browse(cr, uid, country_table.search(cr, uid, []), context=context)
        country_recs_name = dict([(r.name, r.id) for r in country_recs])
        supplier_codes = self.get_xml_id_map(cr, uid, module='F163')
        customer_codes = self.get_xml_id_map(cr, uid, module='F33')
        carrier_codes = self.get_xml_id_map(cr, uid, module='F27')
        employee_codes = self.get_xml_id_map(cr, uid, module='F74')
        shipper_key = 'SV10%s'
        if shipper:
            shipper_key %= shipper
        carrier = fisData(27, keymatch=shipper_key)
        partner_key = '10%s'
        if partner:
            partner_key %= partner
        vnms = fisData(65, keymatch=partner_key)
        posm = fisData(163, keymatch=partner_key)
        csms = fisData(33, keymatch='%s ' % partner_key)
        emp1 = fisData(74, keymatch='10%s')
        today = Date.today()

        # first update the employees, then create a salesperson <-> code mapping
        hr_employee = self.pool.get('hr.employee')
        res_partner = self.pool.get('res.partner')
        res_users = self.pool.get('res.users')
        all_users = res_users.browse(cr, uid, context=inactive_too)
        hr_employees = dict([
            (e.identification_id, e)
            for e in hr_employee.browse(cr, uid, context=inactive_too)
            ])
        potential_sales_people = defaultdict(list)
        sales_people = {}
        for fis_emp_rec in emp1:
            result = {}
            result['name'] = emp_name = re.sub('sunridge', 'SunRidge', NameCase(fis_emp_rec[F74.name]), flags=re.I)
            result['identification_id'] = emp_num = fis_emp_rec[F74.emp_num].strip()
            try:
                if int(emp_num) >= 9000:
                    continue
            except (ValueError, TypeError):
                continue
            addr1, addr2, addr3 = Sift(fis_emp_rec[F74.addr1], fis_emp_rec[F74.addr2], fis_emp_rec[F74.addr3])
            addr2, city, state, postal, country = cszk(addr2, addr3)
            addr3 = ''
            if city and not (addr2 or state or postal or country):
                addr2, city = city, addr2
            addr1 = normalize_address(addr1)
            addr2 = normalize_address(addr2)
            addr1, addr2 = AddrCase(Rise(addr1, addr2))
            city = NameCase(city)
            state, country = NameCase(state), NameCase(country)
            result['home_street'] = addr1
            result['home_street2'] = addr2
            result['home_city'] = city
            result['home_zip'] = postal
            result['home_country_id'] = False
            result['home_state_id'] = False
            if state:
                result['home_state_id'] = state_recs[state][0]
                result['home_country_id'] = state_recs[state][2]
            elif country:
                country_id = country_recs_name.get(country, None)
                if country_id is None:
                    _logger.critical("Employee %s has invalid country <%r>" % (emp_num, country))
                else:
                    result['home_country_id'] = country_id
            result['home_phone'] = fix_phone(fis_emp_rec[F74.tele])
            # result['department']
            ssn = fis_emp_rec[F74.ssn]
            if len(ssn) == 9:
                ssn = '%s-%s-%s' % (ssn[:3], ssn[3:5], ssn[5:])
            result['ssnid'] = ssn
            result['hire_date'] = hired = fix_date(fis_emp_rec[F74.date_hired])
            result['fire_date'] = fired = fix_date(fis_emp_rec[F74.date_terminated])
            result['active'] = (not fired or hired > fired)
            result['birthday'] = birthday = fix_date(fis_emp_rec[F74.birth_date])
            # fix birthday
            if birthday > today:
                _logger.critical('Employee %s has bad birthdate on FIS' % (emp_num, ))
                result['birthday'] = birthday = birthday.replace(delta_year=-100)
            result['status_flag'] = fis_emp_rec[F74.status_flag]
            result['pay_type'] = ('salary', 'hourly')[fis_emp_rec[F74.pay_type].upper() == 'H']
            result['hourly_rate'] = fis_emp_rec[F74.hourly_rate]
            result['marital'] = ('single', 'married')[fis_emp_rec[F74.marital_status].upper() == 'M']
            result['gender'] = ('male', 'female')[fis_emp_rec[F74.gender].upper() == 'F']
            # fleet_hr has this
            result['driver_license_num'] = fis_emp_rec[F74.driver_license]
            result['emergency_contact'] = NameCase(fis_emp_rec[F74.emergency_contact])
            result['emergency_number'] = fix_phone(fis_emp_rec[F74.emergency_phone])
            result['federal_exemptions'] = int(fis_emp_rec[F74.exempt_fed] or 0)
            result['state_exemptions'] = int(fis_emp_rec[F74.exempt_state] or 0)
            he_employee = hr_employees.get(emp_num)
            if he_employee is None:
                hr_employee_id = hr_employee.create(cr, uid, result, context=context)
                hr_employees[emp_num] = he_employee = hr_employee.browse(cr, uid, hr_employee_id, context=context)
            else:
                hr_employee.write(cr, uid, he_employee.id, result, context=context)
            # when to create an employee partner record, and which one to use
            #   ep        up      create?     use?
            #  ---       ---      -------     ----
            #  yes       yes         no        up
            #  yes        no         no        ep
            #   no        no        yes       new
            #   no       yes         no        up
            rp_partner_id = employee_codes.get(emp_num)
            if rp_partner_id is None and not he_employee.partner_id:
                rp_partner_id = res_partner.create(
                        cr, uid,
                        {'name': emp_name, 'xml_id': emp_num, 'module': 'F74'},
                        context=context,
                        )
            rp_partner = res_partner.browse(cr, uid, rp_partner_id, context=inactive_too)
            if he_employee.partner_id and he_employee.partner_id != rp_partner:
                # two partner records exist -- deactivate the one not tied to a user account
                res_partner.write(cr, uid, he_employee.partner_id.id, {'active': False}, context=context)
            # and update partner record with link to employee record
            if he_employee.partner_id != rp_partner:
                values = {'partner_id': rp_partner_id, 'user_id': False}
                if rp_partner.user_ids:
                    values['user_id'] = rp_partner.user_ids[0].id
                hr_employee.write(cr, uid, he_employee.id, values, context=context)
            # housekeeping for salesperson mapping
            names = emp_name.lower().split()
            sales_user_id = rp_partner.user_ids and rp_partner.user_ids[0].id or False
            if sales_user_id:
                potential_sales_people[names[0]].append(sales_user_id)
                if len(names) > 1:
                    potential_sales_people[names[-1]].append(sales_user_id)
                    potential_sales_people[' '.join([names[0], names[-1]])].append(sales_user_id)

        # now the mapping
        cnvzz = fisData(47)
        failed_match = set()
        for rec in cnvzz:
            sales_id = rec[F47.salesperson_id].upper()
            sales_name = rec[F47.salesperson_name]
            company_id = rec[F47.company_id]
            if company_id != '10':
                _logger.warning('skipping %s (%s): not company id 10', sales_name, sales_id)
                continue

            if '-' in sales_name:
                sales_name, extra = sales_name.split('-')
                if not extra.strip().isdigit() and sales_id != 'BAD':
                    _logger.warning('skipping %s (%s): unknown format', sales_name, sales_id)
                    continue

            sales_full_name = sales_name.lower()
            names = sales_full_name.split()
            if len(names) > 1:
                sales_name = ' '.join([names[0], names[-1]])
            else:
                sales_name = sales_name.lower()
            if sales_name in failed_match:
                # this name already failed to match
                continue
            if var(potential_sales_people.get(sales_name)) is not None and len(var()) == 1:
                # full-name match
                sales_people[sales_id] = var()[0]
            # elif len(names) == 1:
            #     # if it didn't match before, it's not going to match now
            #     pass
            #     # potential_sales_people[sales_id] = None
            #     # failed_match.add(sales_name)
            elif var(potential_sales_people.get(names[-1])) and len(var()) == 1:
                # last name match
                sales_people[sales_id] = var()[0]
            elif var(potential_sales_people.get(names[0])) and len(var()) == 1:
                # first name match
                sales_people[sales_id] = var()[0]
            else:
                # no match at all
                # look for user matches and previously created dummy user accounts
                all_users = res_users.browse(cr, uid, context=inactive_too)
                all_users.sort(key=lambda r: not r.active)
                if len(names) > 1:
                    # try to match sales name with beginning of user name
                    # e.g. "billy bob" with "billy bob joe"
                    user = [u for u in all_users if u.name.lower().startswith(sales_name)]
                    if user:
                        if len(user) == 1:
                            sales_people[sales_id] = user[0].id
                            continue
                        else:
                            _logger.warning('unable to match %s (%s): too many possibles', sales_name, sales_id)
                            failed_match.add(sales_name)
                            continue

                    login = names[0][0] + names[1]
                else:
                    login = names[0]
                # try to match against login
                # e.g. "billy bob" with "bbob"
                for user in all_users:
                    if login == user.login:
                        sales_people[sales_id] = user.id
                        break
                else:
                    # if we make it this far, no matches -- so let's create a new (inactive)
                    # user so we can properly categorize customers
                    _logger.warning('unable to match %s: creating dummy user', sales_name)
                    id = res_users.create(
                            cr, uid,
                            {
                                'name': NameCase(sales_name),
                                'login': login,
                                'active': False,
                                },
                            context=context)
                    sales_people[sales_id] = id
                    all_users.append(res_users.browse(cr, uid, id, context=inactive_too))
                # continue
                # failed_match.add(sales_name)

        # the order of the remainder is unimportant
        context = {'fis-updates': True}
        for sup_rec in posm:
            result = {'active': True}
            result['is_company'] = True
            result['supplier'] = True
            result['use_parent_address'] = False
            result['xml_id'] = key = sup_rec[F163.code]
            result['module'] = 'F163'
            # valid supplier code? active account?
            result['fis_valid'] = fis_valid = len(key) == 6 and key.isdigit()
            result['name'] = re.sub('sunridge', 'SunRidge', BsnsCase(sup_rec[F163.name]), flags=re.I)
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
                result['name'] = result['name'] or re.sub('sunridge', 'SunRidge', BsnsCase(ven_rec[F65.name]), flags=re.I)
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
                _logger.critical("Missing name for vendor %s -- skipping" % (key, ))
                continue
            if key in supplier_codes:
                id = supplier_codes[key]
                # leave fis_valid alone
                del result['fis_valid']
                self.write(cr, uid, id, result, context=context)
            else:
                id = self.create(cr, uid, result, context=context)
                supplier_codes[key] = id
            if ven_rec is not None:
                ven_id = id
                contact = ven_rec[F65.contact]
                if contact:
                    result = {'fis_valid': fis_valid}
                    result['name'] = re.sub('sunridge', 'SunRidge', NameCase(contact), flags=re.I)
                    result['is_company'] = False
                    result['supplier'] = True
                    result['parent_id'] = ven_id
                    result['use_parent_address'] = True
                    result['xml_id'] = key = 'cntct_' + key
                    result['module'] = 'F163'
                    if key in supplier_codes:
                        id = supplier_codes[key]
                        # leave fis_valid alone
                        del result['fis_valid']
                        self.write(cr, uid, id, result, context=context)
                    else:
                        id = self.create(cr, uid, result, context=context)
                        supplier_codes[key] = id

        # 'fis_valid': fields.boolean('Valid FIS code?'),
        # 'fis_active': fields.boolean('Active Partner?'),
        # 'special_notifications': fields.char('Special Notifications', size=1),

        for cus_rec in csms:
            rep = cus_rec[F33.salesrep]
            rep = sales_people.get(rep, False)
            result = {'active': False}
            result['user_id'] = rep
            result['is_company'] = True
            result['customer'] = True
            result['use_parent_address'] = False
            result['xml_id'] = key = cus_rec[F33.code]
            result['module'] = 'F33'
            # valid customer code? active account?
            result['fis_valid'] = fis_valid = len(key) == 5
            if (
                    cus_rec[F33.this_year_sales]
                 or cus_rec[F33.last_year_sales]
                ):
                result['active'] = True
            else:
                # TODO check for open orders
                pass
            notify_by = Specials.get_member(cus_rec[F33.catalog_category].upper(), None)
            result['special_notifications'] = notify_by and notify_by.db or False
            result['name'] = re.sub('sunridge', 'SunRidge', BsnsCase(cus_rec[F33.name]), flags=re.I)
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
                _logger.critical("Missing name for customer %s -- skipping" % (key, ))
                continue
            if key in customer_codes:
                id = customer_codes[key]
                # leave fis_valid alone
                del result['fis_valid']
                self.write(cr, uid, id, result, context=context)
            else:
                id = self.create(cr, uid, result, context=context)
                customer_codes[key] = id
            if cus_rec[F33.contact]:
                cus_id = id
                contact = cus_rec[F33.contact]
                result = {
                        'fis_valid': fis_valid,
                        'special_notifications': result['special_notifications'],
                        }
                result['name'] = re.sub('sunridge', 'SunRidge', NameCase(contact), flags=re.I)
                result['is_company'] = False
                result['customer'] = True
                result['parent_id'] = cus_id
                result['use_parent_address'] = True
                result['xml_id'] = key = 'cntct_' + key
                result['module'] = 'F33'
                if key in customer_codes:
                    id = customer_codes[key]
                    # leave fis_valid alone
                    del result['fis_valid']
                    self.write(cr, uid, id, result, context=context)
                else:
                    id = self.create(cr, uid, result, context=context)
                    customer_codes[key] = id

        for sv_rec in carrier:
            result = {}
            result['is_company'] = True
            result['is_carrier'] = True
            result['use_parent_address'] = False
            result['xml_id'] = key = sv_rec[F27.code]
            result['module'] = 'F27'
            result['name'] = re.sub('sunridge', 'SunRidge', BsnsCase(sv_rec[F27.name]), flags=re.I)
            if key == '99':
                result['name'] = '____________'
            addr1, addr2, addr3 = Sift(sv_rec[F27.addr1], sv_rec[F27.addr2], sv_rec[F27.addr3])
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
                    _logger.critical("Carrier %s has invalid country <%r>" % (key, country))
                else:
                    result['country_id'] = country_id
            result['phone'] = fix_phone(sv_rec[F27.tele])
            result['fuel_surcharge'] = sv_rec[F27.fuel_surcharge]
            if key in carrier_codes:
                id = carrier_codes[key]
                self.write(cr, uid, id, result, context=context)
            else:
                id = self.create(cr, uid, result, context=context)
                carrier_codes[key] = id

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
