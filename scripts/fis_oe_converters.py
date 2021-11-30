from __future__ import print_function

from aenum import Enum, NamedTuple
from dbf import Date, DateTime, Time
from fis_schema import F8, F11, F27, F33, F34, F47, F65, F74, F97, F135
from fis_schema import F163, F192, F257, F262, F320, F322, F328, F329, F341
from openerplib import local_to_utc
from openerplib import AttrDict, Many2One, XidRec, Phone
from recipe import ignored_ingredients
from scription import echo, error, print
from tools import Synchronize, SynchronizeAddress, XmlLink, ProductLabelDescription, odoo_erp, Odoo13, PsuedoFisTable
from VSS.address import NameCase, BsnsCase
    # from VSS.BBxXlate.fisData import fisData
from VSS.utils import fix_phone, fix_date
import math
import re
import tools

__all__ = [
        'ARCI',
        'CNVZaa', 'CNVZas', 'CNVZd0', 'CNVZf', 'CNVZO1', 'CNVZSV', 'CNVZ_Z_K',
        'CSMS', 'CSMSS',
        'EMP1',
        'IFMS', 'IFDT',
        'IFPP0', 'IFPP1',
        'NVTY',
        'POSM_VNMS',
        'get_customer_aging', 'get_product_descriptions', 'get_product_forecast',
        'CustomerAging', 'ForecastDetail', 'Forecast',
        'FIS_ID', 'FIS_MODULE',
        ]

if odoo_erp is Odoo13:
    FIS_ID = 'fis_id'
    FIS_MODULE = 'fis_module'
else:
    FIS_ID = 'xml_id'
    FIS_MODULE = 'module'
tools.FIS_ID = FIS_ID
tools.FIS_MODULE = FIS_MODULE

SALEABLE_CATEGORY_XML_ID = 'product_category_1'
INVALID_CATEGORY_XML_ID = 'fis_invalid_product_category'
ETC_CATEGORY_XML_ID = '9'

ONE_YEAR_AGO = Date.today().replace(delta_year=-1)

# For converters that treat 'quick' and 'full' diferently, there are two ways to calculate changes
# in 'quick' mode after using get_changed_fis_records() to isolate the potential changes:
#
# - convert the new records into OpenERP records and retrieve the existing OpenERP
#   records for comparison
#
# - partially convert the records (in case a full conversion is too messy), then complete
#   the conversion later when it is determined the records are actually needed
#

class ARCI(Synchronize):
    """
    customer product cross reference, 262  [CSMS, NVTY]
    """

    TN = 262
    FN = 'arci'
    F = 'F262'
    RE = r'10 HE447......'
    OE = (
            'fis_integration.customer_product_cross_reference',
            'fis.customer_product_xref',
            )[odoo_erp]
    IMD = 'customer_product_xref'
    OE_KEY = 'key'
    OE_KEY_MODULE = 'source','fis'
    OE_FIELDS = (
            'id','key','list_code','fis_code',
            'partner_id','fis_product_id','customer_product_code',
            'source',
            )
    FIS_SCHEMA = (
            F262.cust_item_id,
            )

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        cust_no = fis_rec[F262.cust_no]
        our_item_id = fis_rec[F262.our_item_id]
        key = '%s-%s' % (cust_no, our_item_id)
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        cust_item_id = fis_rec[F262.cust_item_id]
        #
        # fis record
        #
        item = AttrDict.fromkeys(self.OE_FIELDS, None)
        item.key = key
        item.list_code = cust_no
        item.fis_code = our_item_id
        item.fis_product_id = NVTY.Product(our_item_id)
        item.customer_product_code = cust_item_id or None
        module_field, module_value = self.OE_KEY_MODULE
        item[module_field] = module_value
        if cust_no == '-all-':
            item.partner_id = None
        else:
            item.partner_id = CSMS.Partner(cust_no)

        #
        return (XidRec.fromdict(item, imd), )

    def open_fis_tables(self):
        """
        combine FIS ARCI records HE447 with OpenERP inventory records containing Y and P availability codes
        """
        arci_table = self.get_fis_table(self.TN, rematch=self.RE)
        old_arci_table = self.get_fis_table(
                self.TN,
                rematch=self.RE,
                data_path=self.config.network.fis_data_local_old_path,
                )
        print('arci: %d\nold arci: %d' % (len(arci_table), len(old_arci_table)), verbose=2)
        #
        self.fis_table = PsuedoFisTable('combined arci/nvty table')
        self.old_fis_table = PsuedoFisTable('old combined arci/nvty table')
        for rec in arci_table.values():
            key = '%s-%s' % (rec[F262.cust_no], rec[F262.our_item_id])
            self.fis_table[key] = rec
        for rec in old_arci_table.values():
            key = '%s-%s' % (rec[F262.cust_no], rec[F262.our_item_id])
            self.old_fis_table[key] = rec
        # "new" inventory comes from F135
        # "old" inventory comes from old F135
        nvty_table = self.get_fis_table(NVTY.TN, rematch=NVTY.RE)
        old_nvty_table = self.get_fis_table(
                NVTY.TN,
                rematch=NVTY.RE,
                data_path=self.config.network.fis_data_local_old_path,
                )
        print('nvty: %d\nold nvty: %d' % (len(nvty_table), len(old_nvty_table)), verbose=2)
        cust_no = '-all-'
        for rec in nvty_table.values():
            if NVTY.in_catalog(rec):
                item_id = rec[F135.item_id]
                self.fis_table['%s-%s' % (cust_no, item_id)] = {
                        F262.company_id: '10',
                        F262.cust_no: cust_no,
                        F262.our_item_id: item_id,
                        F262.cust_item_id: item_id,
                        }
        for rec in old_nvty_table.values():
            if NVTY.in_catalog(rec):
                item_id = rec[F135.item_id]
                self.old_fis_table['%s-%s' % (cust_no, item_id)] = {
                        F262.company_id: '10',
                        F262.cust_no: cust_no,
                        F262.our_item_id: item_id,
                        F262.cust_item_id: item_id,
                        }


class CNVZaa(Synchronize):
    """
    product location, 97
    """

    TN = 97
    FN = 'cnvzaa'
    F = 'F097'
    OE = (
            'product.available_at',
            'product.availability',
            )[odoo_erp]
    IMD = 'product_availability'
    RE = r"aa10."
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F97'
    OE_FIELDS = (
            ('id', 'module', 'xml_id', 'name', 'available'),
            ('id', 'fis_module', 'fis_id', 'name', 'saleable'),
            )[odoo_erp]
    FIS_SCHEMA = (
            F97.desc, F97.availability,
            )
    #
    ProductLocation = XmlLink

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F97.availability_id].strip()
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        fis_module = ('module', 'fis_module')[odoo_erp]
        saleable = ('available', 'saleable')[odoo_erp]
        location = AttrDict.fromkeys(self.OE_FIELDS, None)
        location.name = re.sub('sunridge', 'SunRidge', fis_rec[F97.desc].title(), flags=re.I) or None
        location[FIS_ID] = key
        location[fis_module] = self.OE_KEY_MODULE
        avail = fis_rec[F97.availability].upper()
        if avail not in 'YN':
            avail = None
        location[saleable] = avail
        return (XidRec.fromdict(location, imd), )


class CNVZas(Synchronize):
    """
    product.category, 11
    """

    # product category, 11
    TN = 11
    FN = 'cnvzas'
    F = 'F011'
    OE = 'product.category'
    IMD = 'product_category'
    RE = r"as10.."
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F11'
    OE_FIELDS = ('id', FIS_MODULE, FIS_ID, 'name', 'parent_id', 'fis_shelf_life')
    FIS_SCHEMA = (
            F11.desc, F11.shelf_life,
            )
    #
    ProductCategory = XmlLink

    def __init__(self, *args, **kwds):
        super(CNVZas, self).__init__(*args, **kwds)
        self.SALEABLE_CATEGORY = self.ProductCategory(SALEABLE_CATEGORY_XML_ID)
        _, self.SALEABLE_CATEGORY.id = self.ir_model_data.get_object_reference('product', SALEABLE_CATEGORY_XML_ID)
        self.ETC_CATEGORY = self.ProductCategory(ETC_CATEGORY_XML_ID)
        # make sure the invalid category exists
        try:
            self.ir_model_data.get_object_reference('fis', INVALID_CATEGORY_XML_ID)
        except ValueError:
            self.ir_model_data.create({
                    'module': 'fis',
                    'name': INVALID_CATEGORY_XML_ID,
                    'model': 'product.category',
                    })

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F11.sales_category_id].strip()
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        category = AttrDict.fromkeys(self.OE_FIELDS, None)
        category[FIS_ID] = key
        category[FIS_MODULE] = self.OE_KEY_MODULE
        category.fis_shelf_life = fis_rec[F11.shelf_life]
        name = re.sub('sunridge', 'SunRidge', fis_rec[F11.desc].title(), flags=re.I)
        if len(key) == 1:
            name = key + ' - ' + name.strip('- ')
            category.parent_id = self.SALEABLE_CATEGORY
        else:
            parent_key = key[0]
            if parent_key.isdigit():
                parent_id = self.ProductCategory(parent_key)
            else:
                parent_id = self.ETC_CATEGORY
            category.parent_id = parent_id
        category.name = name or None
        return (XidRec.fromdict(category, imd), )


class CNVZd0(Synchronize):
    """
    customer terms, 8
    """
    TN = 8
    FN = 'cnvzd0'
    F = 'F008'
    RE = r"D010."
    OE = 'fis.account.customer_terms'
    IMD = 'account_customer_terms'
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F8'
    OE_FIELDS = ('id', FIS_MODULE, FIS_ID, 'description')
    FIS_SCHEMA = (
            F8.description,
            )
    #
    CustomerTerms = XmlLink

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F8.code]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        terms = AttrDict.fromkeys(self.OE_FIELDS, None)
        terms[FIS_ID] = key
        terms[FIS_MODULE] = self.OE_KEY_MODULE
        terms.description = ' / '.join([t.strip() for t in fis_rec[F8.description].split('/')]) or None
        return (XidRec.fromdict(terms, imd), )


class CNVZf(Synchronize):
    """
    production lines, 341
    """
    TN = 341
    FN = 'cnvzf'
    F = 'F341'
    OE = (
            'fis_integration.production_line',
            'fis.production.line',
            )[odoo_erp]
    IMD = 'production_line'
    RE = r"f10.."
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F341'
    OE_FIELDS = (
            ('id', 'xml_id', 'module', 'desc'),
            ('id', 'fis_id', 'fis_module', 'description'),
            )[odoo_erp]
    FIS_SCHEMA = (
            F341.desc,
            )
    #
    ProductionLine = XmlLink

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F341.prod_line_code]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        line = AttrDict.fromkeys(self.OE_FIELDS, None)
        desc = fis_rec[F341.desc] or None
        if desc:
            new_desc = []
            for word in desc.split():
                if word.upper() in ('KFK','USA','LLC'):
                    new_desc.append(word.upper())
                else:
                    new_desc.append(word.title())
            desc = ' '.join(new_desc)
        if odoo_erp:
            line.fis_module = self.OE_KEY_MODULE
            line.fis_id = key
            line.description = desc
        else:
            line.module = self.OE_KEY_MODULE
            line.xml_id = key
            line.desc = desc
        return (XidRec.fromdict(line, imd), )


class CNVZO1(Synchronize):
    """
    transmitter numbers, 192 [CSMSS]

    key field is the transmitter number
    ship_to will be empty if empty in FIS
    """
    TN = 192
    FN = 'cnvzo1'
    F = 'F192'
    OE = (
            'fis.transmitter_code',
            'fis.account.transmitter_code',
            )[odoo_erp]
    IMD = 'account_transmitter_code'
    #
    RE = r"O110......"
    OE_KEY = 'transmitter_no'
    OE_FIELDS = ('id', 'transmitter_no', 'transmitter_name', 'ship_to_xml_id', 'ship_to_id')
    #
    FIS_IGNORE_RECORD = lambda self, rec: not (
            rec[F192.transmitter_no].strip().isdigit()
            and rec[F192.status][0:1] == 'A'
            and rec[F192.cust_no].strip()
            )
    FIS_SCHEMA = (
            F192.transmitter_name, F192.cust_no, F192.ship_to_id, F192.status,
            )
    #
    TransmitterCode = XmlLink

    def __init__(self, oe, config, *args, **kwds):
        super(CNVZO1, self).__init__(oe, config, *args, **kwds)
        CSMS(oe, config, None, None).reify(fields=['xml_id','fis_online_ordering_possible','fis_online_ordering_enabled'])
        CSMSS(oe, config, None, None).reify(fields=['xml_id','fis_online_ordering_possible','fis_online_ordering_enabled'])

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F192.transmitter_no].strip()
        partner = fis_rec[F192.cust_no].strip() or ''
        ship_to = fis_rec[F192.ship_to_id].strip() or ''
        ship_to_xml_id = ('%s-%s' % (partner, ship_to)).strip('-')
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        tran_code = AttrDict.fromkeys(self.OE_FIELDS, None)
        tran_code.transmitter_no = key
        tran_code.transmitter_name = fis_rec[F192.transmitter_name].strip() or None
        tran_code.ship_to_xml_id = ship_to_xml_id
        tran_code.ship_to_id = CSMSS.ShipTo(ship_to_xml_id) or CSMSS.ShipTo(partner) or CSMS.Partner(partner) or None
        # echo('cnvzo1', tran_code)
        return (XidRec.fromdict(tran_code, imd), )

    def global_updates(self):
        """
        update CSMS and CSMSS records, fields fis_online_ordering_[possible|enabled]
        """
        F33_records = self.get_xid_records(
                self.erp,
                domain=[('module','=','fis'),('name','=like','F033_%_res_partner')],
                fields=['id','xml_id','fis_online_ordering_possible','fis_online_ordering_enabled'],
                context=self.context,
                )
        F34_records = self.get_xid_records(
                self.erp,
                domain=[('module','=','fis'),('name','=like','F034_%_res_partner')],
                fields=['id','xml_id','fis_online_ordering_enabled'],
                context=self.context,
                )
        F192_records = self.get_xid_records(
                self.erp,
                domain=[('module','=','fis'),('name','=like','F192_%_account_transmitter_code')],
                fields=['id','ship_to_xml_id','ship_to_id'],
                )
        oe_possible = []
        oe_impossible = []
        oe_enabled = []
        oe_disabled = []
        possibles = set()
        enabled = set()
        #
        for rec in F192_records:
            xml_id = rec.ship_to_xml_id.split('-')[0]
            possibles.add(xml_id)
            enabled.add(rec.ship_to_id)
        #
        for rec in F33_records:
            if rec.xml_id in possibles:
                if not rec.fis_online_ordering_possible:
                    oe_possible.append(rec.id)
            elif rec.fis_online_ordering_possible:
                oe_impossible.append(rec.id)
            if rec.id in enabled:
                if not rec.fis_online_ordering_enabled:
                    oe_enabled.append(rec.id)
            elif rec.fis_online_ordering_enabled:
                oe_disabled.append(rec.id)
        #
        for rec in F34_records:
            if rec.id in possibles:
                # ship-to records should alwasy have this off
                oe_impossible.append(rec.id)
            if rec.id in enabled:
                if not rec.fis_online_ordering_enabled:
                    oe_enabled.append(rec.id)
            elif rec.fis_online_ordering_enabled:
                oe_disabled.append(rec.id)
        #
        res_partner = self.erp.get_model('res.partner')
        if oe_possible:
            res_partner.write(oe_possible, {'fis_online_ordering_possible': True})
        if oe_impossible:
            res_partner.write(oe_impossible, {'fis_online_ordering_possible': False})
        if oe_enabled:
            res_partner.write(oe_enabled, {'fis_online_ordering_enabled': True})
        if oe_disabled:
            res_partner.write(oe_disabled, {'fis_online_ordering_enabled': False})


class CNVZSV(SynchronizeAddress):
    """
    shipping carriers, 27
    """
    TN = 27
    FN = 'cnvzsv'
    F = 'F027'
    OE = 'res.partner'
    IMD = 'res_partner'
    RE = r"SV10.."
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F27'
    OE_FIELDS = (
            'id', FIS_MODULE, FIS_ID, 'is_carrier', 'is_company', 'use_parent_address',
            'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id',
            'phone', 'fuel_surcharge', 'fis_updated_by_user',
            )
    FIS_SCHEMA = (
            F27.name, F27.tele, F27.fuel_surcharge,
            )

    def FIS_IGNORE_RECORD(self, fis_rec):
        return (
                fis_rec[F27.code] in ('', '99')
                or not self.process_name_address(F27, fis_rec)[0]
                )

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F27.code].strip()
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        names, address , do_not_use = self.process_name_address(F27, fis_rec)
        pname = names and names[0] or ''
        pname = re.sub('sunridge', 'SunRidge', BsnsCase(pname), flags=re.I)
        names[0:1] = [pname]
        name = ', '.join(names)
        dnu = ', '.join(do_not_use)
        name = ' / '.join([l for l in (name, dnu) if l])
        company = AttrDict.fromkeys(self.OE_FIELDS, None)
        company.name = name
        company.update(address)
        company[FIS_ID] = key
        company[FIS_MODULE] = self.OE_KEY_MODULE
        company.fis_updated_by_user = None
        company.is_company = True
        company.is_carrier = True
        company.use_parent_address = False
        if key == '99':
            company.name = '____________'
        company.phone = fix_phone(fis_rec[F27.tele].strip()) or None
        company.fuel_surcharge = fis_rec[F27.fuel_surcharge].upper() == 'Y'
        return (XidRec.fromdict(company, imd), )


class CNVZ_Z_K(Synchronize):
    """
    customer sales reps, 47; ordered by, 257
    """
    TN = 47
    TN_2ND = 257
    FN = 'cnvzz'
    FN_2ND = 'cnvzk'
    F = 'F047'
    OE = 'fis.account.salesperson'
    IMD = 'account_salesperson'
    RE = r"Z..."
    RE_2ND = r"K...."
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F47'
    OE_FIELDS = ('id', FIS_MODULE, FIS_ID, 'fis_name', 'user_id', 'ordered_by_no')
    FIS_SCHEMA = ()
    #
    SalesRep = XmlLink

    def __init__(self, *args, **kwds):
        super(CNVZ_Z_K, self).__init__(*args, **kwds)
        users = self.get_xid_records(
                self.erp,
                domain=[('module','=','fis'),('name','=like','F074_%_res_users')],
                fields=['id','login','name'],
                context=self.context,
                )
        self.users = {}
        for user in users:
            key = int(user._imd.name.split('_')[1])
            self.users[key] = user

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        sales_rec, orderedby_rec = fis_rec
        key = sales_rec[F47.salesperson_id]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        salesrep = AttrDict.fromkeys(self.OE_FIELDS, None)
        salesrep[FIS_ID] = key
        salesrep[FIS_MODULE] = self.OE_KEY_MODULE
        salesrep.ordered_by_no = orderedby_rec and orderedby_rec[F257.ordered_by_id] or None
        name = sales_rec[F47.salesperson_name]
        if '-' in name:
            name, unk = name.split('-')
            if not unk.isdigit():
                name = '%s [%s]' % (name, unk)
        salesrep.fis_name = name
        # try to find a match in res.users
        salesrep.user_id = self.users.get(sales_rec[F47.employee_no])
        if salesrep.user_id:
            salesrep.user_id = Many2One(salesrep.user_id.id, key, 'res.users')
        return (XidRec.fromdict(salesrep, imd), )

    def open_fis_tables(self):
        cnvzz_table = self.get_fis_table(self.TN, rematch=self.RE)
        cnvzk_table = self.get_fis_table(self.TN_2ND, rematch=self.RE_2ND)
        old_cnvzz_table = self.get_fis_table(
                self.TN,
                rematch=self.RE,
                data_path=self.config.network.fis_data_local_old_path,
                )
        old_cnvzk_table = self.get_fis_table(
                self.TN_2ND,
                rematch=self.RE_2ND,
                data_path=self.config.network.fis_data_local_old_path,
                )
        print('print is', print)
        print('cnvzz: %d\ncnvzk: %d\nold cnvzz: %d\nold cnvzk: %d' % (
                    len(cnvzz_table), len(cnvzk_table),
                    len(old_cnvzz_table), len(old_cnvzk_table),
                    ),
                verbose=2,
                )
        #
        self.fis_table = PsuedoFisTable('combined cnvzz/cnvzk table')
        self.old_fis_table = PsuedoFisTable('old combined cnvzz/cnvzk table')
        current_names = {}
        for rec in cnvzk_table.values():
            current_names[rec[F257.ordered_by_name].split('-')[0].upper()] = rec
        for rec in cnvzz_table.values():
            key = rec[F47.salesperson_id]
            name = rec[F47.salesperson_name].split('-')[0].upper()
            self.fis_table[key] = rec, current_names.get(name)
        old_names = {}
        for rec in old_cnvzk_table.values():
            old_names[rec[F257.ordered_by_name].split('-')[0].upper()] = rec
        for rec in old_cnvzz_table.values():
            key = rec[F47.salesperson_id]
            name = rec[F47.salesperson_name].split('-')[0].upper()
            self.old_fis_table[key] = rec, old_names.get(name)

    fis_quick_load = Synchronize.fis_long_load

class CSMS(SynchronizeAddress):
    """
    customers, 33  (CNVZ_Z_K, CNVZd0)
    """
    TN = 33
    FN = 'csms'
    F = 'F033'
    RE = r"10...... "
    OE = 'res.partner'
    IMD = 'res_partner'
    FIS_KEY = F33.code
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F33'
    OE_FIELDS_QUICK = (
            'id', FIS_MODULE, FIS_ID, 'fis_csms_terms', 'fis_price_list',
            'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id',
            'fis_valid', 'specials_notification', 'phone', 'is_company', 'customer',
            'fis_updated_by_user', 'active', 'use_parent_address', 'user_id',
            # 'fis_transmitter_id',
            )
    OE_FIELDS_LONG = OE_FIELDS_QUICK + (
            'fis_credit_current', 'fis_credit_limit', 'fis_credit_total',
            'fis_credit_10_days', 'fis_credit_20_days', 'fis_credit_30_days',
            )
    FIS_SCHEMA = (
            F33.name, F33.salesrep, F33.catalog_category, F33.this_year_sales,
            F33.last_year_sales, F33.tele, F33.contact,
            )
    FIELDS_CHECK_IGNORE = ('active', 'name')

    Partner = XmlLink

    def __init__(self, oe, config, *args, **kwds):
        super(CSMS, self).__init__(oe, config, *args, **kwds)
        CNVZ_Z_K(oe, config).reify(fields=['user_id'])

    def run(self, method):
        if method == 'full':
            print('getting aging data')
            aging = get_customer_aging('%s/customer_aging.txt' % self.config.network.fis_data_local_path)
        else:
            aging = None
        self.aging_data = aging
        super(CSMS, self).run(method)

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        #
        # creates an AttrDict with the following fields
        # - '(fis_)module', '(fis|xml)_id',
        # - 'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id',
        # - 'fis_valid', 'specials_notification', 'phone', 'is_company', 'customer',
        # - 'use_parent_address', 'active', 'fis_transmitter_id',
        #
        # fields coming from OpenERP that are missing/invalid on the FIS side
        # - 'id', 'fis_updated_by_user'
        # - address fields (for contact)
        #
        # fis records use the following fields to detect changes
        #
        # enum_schema=[
        #     F33.name, F33.salesrep, F33.catalog_category, F33.this_year_sales,
        #     F33.last_year_sales, F33.tele, F33.contact,
        #     ],
        # address_fields=[
        #     F33.addr1, F33.addr2, F33.addr3,
        #     ],
        #
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F33.code]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        names, address, do_not_use = self.process_name_address(F33, fis_rec)
        pname = names and names[0] or ''
        pname = re.sub('sunridge', 'SunRidge', BsnsCase(pname), flags=re.I) or ''
        if re.match('HE\d\d\d$', key) and pname.startswith('Heb '):
            pname = 'HEB ' + pname[4:]
        names[0:1] = [pname]
        name = ', '.join(names)
        dnu = ', '.join(do_not_use)
        name = ' / '.join([l for l in (name, dnu) if l])
        if not name:
            return ()
        company = AttrDict.fromkeys(self.OE_FIELDS, None)
        company.name = name
        company.update(address)
        company[FIS_MODULE] = self.OE_KEY_MODULE
        company[FIS_ID] = key
        company.fis_updated_by_user = None
        company.is_company = True
        company.customer = True
        company.use_parent_address = False
        # valid customer code? active account?
        company.fis_valid = len(key) == 5
        company.active = not bool(do_not_use)
        added = fis_rec[F33.date_added] or Date()
        if added:
            year, month, day = added[:2], int(added[2:4]), int(added[4:])
            if year.isdigit():
                year = 1900 + int(year)
            else:
                year = 1840 + int(year, 16)
            added = Date(year, month, day)
        if (
                fis_rec[F33.this_year_sales]
             or fis_rec[F33.last_year_sales]
             or added >= ONE_YEAR_AGO
            ):
            company.active = True
        else:
            # TODO check for open orders
            pass
        if fis_rec[F33.salesrep] == 'INA':
            company.active = False
        company.user_id = CNVZ_Z_K.SalesRep(fis_rec[F33.salesrep]).user_id
        notify_by = Specials.get_member(fis_rec[F33.catalog_category].upper(), Specials.neither)
        company.specials_notification = notify_by   #.value
        company.phone = fix_phone(fis_rec[F33.tele]) or None
        company.fis_csms_terms = CNVZd0.CustomerTerms(fis_rec[F33.payment_terms_id])
        company.fis_price_list = fis_rec[F33.price_list_id] or None
        if self.method == 'full':
            if key in self.aging_data:
                account = self.aging_data[key]
                company.fis_credit_limit = account.limit
                company.fis_credit_current = account.current
                company.fis_credit_10_days = account.d10
                company.fis_credit_20_days = account.d20
                company.fis_credit_30_days = account.d30
                company.fis_credit_total = account.total
            else:
                company.fis_credit_limit = 0
                company.fis_credit_current = 0
                company.fis_credit_10_days = 0
                company.fis_credit_20_days = 0
                company.fis_credit_30_days = 0
                company.fis_credit_total = 0
        # company.fis_transmitter_id = CNVZO1.TransmitterCode(key)
        company = XidRec.fromdict(company, imd)
        assert set(company._keys) == set(company._values.keys())
        contact = None
        if fis_rec[F33.contact] and fis_rec[F33.contact] != fis_rec[F33.name]:
            key = 'cntct_' + key
            imd = AttrDict(
                    id=0,
                    model=self.OE,
                    res_id=0,
                    module='fis',
                    name='F033_%s_res_partner' % (key),
                    )
            contact = AttrDict.fromkeys(self.OE_FIELDS, None)
            name = fis_rec[F33.contact]
            if name is not None and not (' ' not in name and '@' in name):
                name = NameCase(name)
            contact.name = name
            contact[FIS_MODULE] = 'F33'
            contact[FIS_ID] = key
            contact.fis_updated_by_user = None
            contact.is_company = False
            contact.customer = True
            contact.use_parent_address = False
            contact.street = company.street
            contact.street2 = company.street2
            contact.city = company.city
            contact.state_id = company.state_id
            contact.zip = company.zip
            contact.country_id = company.country_id
            contact.specials_notification = Specials.company
            contact.fis_valid = company.fis_valid
            contact.active = company.active
            contact.user_id = company.user_id
            if self.method == 'full':
                contact.fis_credit_limit = 0
                contact.fis_credit_current = 0
                contact.fis_credit_10_days = 0
                contact.fis_credit_20_days = 0
                contact.fis_credit_30_days = 0
                contact.fis_credit_total = 0
            contact = XidRec.fromdict(contact, imd)
            assert set(contact._keys) == set(contact._values.keys())
            return company, contact
        return (company, )

    def normalize_records(self, fis_rec, oe_rec):
        super(CSMS, self).normalize_records(fis_rec, oe_rec)
        fis_rec.fis_valid = oe_rec.fis_valid


class CSMSS(SynchronizeAddress):
    """
    ship-to addresses, 34  (CSMS)

    key field is the customer number plus a ship-to designation
    key field only has a ship-to if one is in FIS
    """
    TN = 34
    FN = 'csmss'
    F = 'F034'
    RE = r"10......1...."
    OE = 'res.partner'
    IMD = 'res_partner'
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F%s' % TN
    OE_FIELDS = (
            'id', FIS_MODULE, FIS_ID, 'phone',
            'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id',
            'customer', 'fis_ship_to_parent_id', 'use_parent_address', 'is_company',
            'fis_ship_to_code', 'active',
            # 'fis_transmitter_id',
            )
    FIS_SCHEMA = (
            F34.name, F34.addr1, F34.addr2, F34.addr3, F34.postal,
            F34.tele, F34.sales_contact,
            )
    FIS_IGNORE_RECORD = lambda self, rec: (
                not rec[F34.name]
                or re.search('.*additional.*ship.*to.*', rec[F34.name], re.I)
                or re.search('.*additional.*ship.*to.*', rec[F34.addr1], re.I)
                or re.search('.*additional.*ship.*to.*', rec[F34.addr2], re.I)
                or re.search('.*additional.*ship.*to.*', rec[F34.addr3], re.I)
                )

    ShipTo = XmlLink

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        "additional ship-to addresses"
        #
        # creates an XidRec with the following fields
        # - '(fis_)module', '(fis|xml)_id', 'active',
        # - 'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id',
        # - 'phone', 'is_company', 'customer','use_parent_address',
        # - 'fis_ship_to_code', 'fis_ship_to_parent_id', 'fis_transmitter_id',
        #
        # fields coming from OpenERP that are missing/invalid on the FIS side
        # - 'id',
        #
        # fis records use the following fields to detect changes
        #
        # enum_schema=[
        #     F34.name, F34.addr1, F34.addr2, F34.addr3, F34.postal, F34.tele, F34.sales_contact,
        #     ],
        # address_fields=[
        #     F34.addr1, F34.addr2, F34.addr3,
        #     ],
        #
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        parent_xml_id = fis_rec[F34.code]
        names, address, do_not_use = self.process_name_address(F34, fis_rec)
        ship_to_code = fis_rec[F34.ship_to_no].strip() or None
        # o1_key = ('%s-%s' % (fis_rec[F34.code], ship_to_code or '')).strip('-')
        key = ('%s-%s' % (parent_xml_id, ship_to_code or '')).strip('-')
        pname = names and names[0] or ''
        pname = re.sub('sunridge', 'SunRidge', BsnsCase(pname), flags=re.I) or ''
        if re.match('HE\d\d\d*$', key) and pname.startswith('Heb '):
            pname = 'HEB ' + pname[4:]
        names[0:1] = [pname]
        name = ', '.join(names)
        dnu = ', '.join(do_not_use)
        name = ' / '.join([l for l in (name, dnu) if l])
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        ship_to = AttrDict.fromkeys(self.OE_FIELDS, None)
        ship_to.name = name
        ship_to.update(address)
        ship_to[FIS_MODULE] = self.OE_KEY_MODULE
        ship_to[FIS_ID] = key
        ship_to.active = fis_rec[F34.salesrep_id] != 'INA'
        ship_to.fis_ship_to_code = ship_to_code
        ship_to.is_company = False
        ship_to.customer = False
        ship_to.use_parent_address = False
        ship_to.phone = fix_phone(fis_rec[F34.tele]) or None
        ship_to.fis_ship_to_parent_id = CSMS.Partner(parent_xml_id)
        # ship_to.fis_transmitter_id = CNVZO1.TransmitterCode(o1_key)
        return (XidRec.fromdict(ship_to, imd), )


class EMP1(SynchronizeAddress):
    """
    employees, 74
    """
    TN = 74
    FN = 'emp1'
    F = 'F074'
    OE = 'hr.employee'
    IMD = 'hr_employee'
    RE = r"10....."
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F74'
    OE_FIELDS = [
            'id', 'name', 'employment_type', 'ssnid', 'birthday',
            'hire_date', 'fire_date', 'active', 'status_flag', 'pension_plan',
            'pay_type', 'hourly_rate', 'last_raise', 'marital', 'gender', 'identification_id',
            'emergency_contact', 'emergency_number', 'state_exemptions', 'federal_exemptions',
            ]
    OE_FIELDS[1:1] = (
            ('module','xml_id','home_phone','home_street','home_street2','home_city','home_state_id','home_zip','home_country_id'),
            ('fis_module','fis_id','phone','street','street2','city','state_id','zip','country_id'),
            )[odoo_erp]
    FIS_SCHEMA = (
            F74.name, F74.ssn, F74.tele, F74.date_hired, F74.date_terminated,
            F74.birth_date, F74.last_raise, F74.status_flag, F74.pay_type,
            F74.marital_status, F74.pension_status, F74.gender, F74.emergency_contact,
            F74.emergency_phone, F74.exempt_fed, F74.exempt_state, F74.hourly_rate,
            )
    FIS_IGNORE_RECORD = lambda self, rec: int(rec[F74.emp_num]) >= 9000

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        emp_num = fis_rec[F74.emp_num].strip()
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(emp_num),
                )
        if odoo_erp:
            # odoo13
            kwds = {}
        else:
            kwds = {'home': True}
        names, address, do_not_use = self.process_name_address(F74, fis_rec, **kwds)
        pname = names and names[0] or ''
        pname = re.sub('sunridge', 'SunRidge', BsnsCase(pname), flags=re.I) or None
        names[0:1] = [pname]
        name = ', '.join(names)
        dnu = ', '.join(do_not_use)
        name = ' / '.join([l for l in (name, dnu) if l])
        if not name:
            return ()
        employee = AttrDict.fromkeys(self.OE_FIELDS, None)
        employee.name = name
        employee.update(address)
        employee[FIS_ID] = employee.identification_id = emp_num
        employee[FIS_MODULE] = self.OE_KEY_MODULE
        employee.employment_type = 'standard'
        if odoo_erp:
            employee.phone = fix_phone(fis_rec[F74.tele]) or None
        else:
            employee.home_phone = fix_phone(fis_rec[F74.tele]) or None
        ssn = fis_rec[F74.ssn]
        if len(ssn) == 9:
            ssn = '%s-%s-%s' % (ssn[:3], ssn[3:5], ssn[5:])
        employee.ssnid = ssn or None
        employee.hire_date = hired = fix_date(fis_rec[F74.date_hired]) or None
        employee.fire_date = fired = fix_date(fis_rec[F74.date_terminated]) or None
        employee.active = (not fired or hired > fired)
        # employee birth dates are stored extra weirdly: if the year is 99 or less
        #   then the it's 19xx, but if any hex digits are present then the year is
        #   1740 + xx
        text = fis_rec[F74.birth_date]
        emp_birthday = None
        if text:
            month, day, year = int(text[:2]), int(text[2:4]), text[4:]
            if year.isdigit():
                year = 1900 + int(year)
            else:
                year = 1740 + int(year, 16)
            emp_birthday = Date(year, month, day)
        employee.birthday = emp_birthday or None
        employee.status_flag = fis_rec[F74.status_flag] or None
        employee.pension_plan = fis_rec[F74.pension_status].upper() == 'Y'
        employee.pay_type = ('salary', 'hourly')[fis_rec[F74.pay_type].upper() == 'H']
        employee.hourly_rate = fis_rec[F74.hourly_rate]
        employee.last_raise = fix_date(fis_rec[F74.last_raise]) or None
        employee.marital = ('single', 'married')[fis_rec[F74.marital_status].upper() == 'M']
        employee.gender = ('male', 'female')[fis_rec[F74.gender].upper() == 'F']
        employee.emergency_contact = NameCase(fis_rec[F74.emergency_contact]) or None
        employee.emergency_number = fix_phone(fis_rec[F74.emergency_phone]) or None
        employee.federal_exemptions = int(fis_rec[F74.exempt_fed] or 0)
        employee.state_exemptions = int(fis_rec[F74.exempt_state] or 0)
        return (XidRec.fromdict(employee, imd), )


class IFMS(Synchronize):
    """
    product formula, 320
    """
    TN = 320
    FN = 'ifms'
    F = 'F320'
    RE = r'10(..........)..(...)0'
    OE = (
            'fnx.pd.product.formula',
            'fis.product.formula',
            )[odoo_erp]
    IMD = 'product_formula'
    OE_KEY = 'name'
    OE_FIELDS = ('id', 'name', 'formula', 'description', 'coating', 'allergens')
    FIS_SCHEMA = (
            F320.formula_id, F320.rev_no,
            F320.desc, F320.coating, F320.allergens,
            )
    FIS_IGNORE_RECORD = lambda self, rec: len(rec[F320.formula_id]) != 6
    #
    ProductFormula = XmlLink

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        "product formula"
        # convert the record into the following fields:
        #   formula, description, coating, allergens
        #
        # using:
        #   F320.formula, F320.rev_no, F320.desc, F320.coating, F320.allergens
        #
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F320.formula_id]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        formula = AttrDict().fromkeys(self.OE_FIELDS, None)
        formula.name = key
        formula.formula = '%s-%s' % (key, fis_rec[F320.rev_no])
        formula.description = fis_rec[F320.desc] or None
        formula.coating = fis_rec[F320.coating] or None
        formula.allergens = fis_rec[F320.allergens] or None
        return (XidRec.fromdict(formula, imd), )


class IFDT(Synchronize):
    """
    product ingredient, 322  (IFMS, NVTY)
    """
    TN = 322
    FN = 'ifdt'
    F = 'F322'
    RE = r'10(..........)..(...)0...'
    OE = (
            'fnx.pd.product.ingredient',
            'fis.product.formula.ingredient',
            )[odoo_erp]
    IMD = 'product_ingredient'
    OE_KEY = 'name'
    OE_FIELDS = ('id', 'name', 'sequence', 'formula_id', 'item_id', 'qty_needed', 'qty_desc')
    FIS_SCHEMA = (
            F322.formula_id, F322.rev_no, F322.desc_batch_1, F322.line_no,
            )
    FIS_IGNORE_RECORD = lambda self, rec: (
              not IFMS.ProductFormula('%s-%s' % (rec[F322.formula_id], rec[F322.rev_no]))
              or rec[F322.ingr_code_batch_1] in ignored_ingredients
              or rec[F322.qty_batch_1] <= 0
              or not NVTY.Product(rec[F322.ingr_code_batch_1])
              )

    def __init__(self, oe, config, *args, **kwds):
        super(IFDT, self).__init__(oe, config, *args, **kwds)
        #
        # load formulae from OE
        #
        IFMS(oe, config).reify()
        NVTY(oe, config).reify()

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        "product ingredient"
        # convert the record into the following fields:
        #   formula_id, item_id, qty_needed, qty_desc
        #
        # using:
        #   F322.formula_id, F322.rev_no,
        #   F322.ingr_code_batch_1, F322.qty_batch_1, F322.units_batch_1
        #
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        oe_key = '%s-%s' % (fis_rec[F322.formula_id], fis_rec[F322.rev_no])
        item = fis_rec[F322.ingr_code_batch_1]
        imd_name = '%s-%s' % (oe_key, fis_rec[F322.line_no])
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(imd_name),
                )
        ingredient = AttrDict().fromkeys(self.OE_FIELDS, None)
        ingredient.formula_id = IFMS.ProductFormula(oe_key)
        ingredient.item_id = NVTY.Product(item)
        ingredient.name = '%s:%s' % (oe_key, item)
        ingredient.sequence = int(fis_rec[F322.line_no] or 0)
        ingredient.qty_needed = fis_rec[F322.qty_batch_1]
        ingredient.qty_desc = fis_rec[F322.units_batch_1] or None
        return (XidRec.fromdict(ingredient, imd), )


class IFPP0(Synchronize):
    """
    production order, 328  (CNVZf, IFMS, NVTY)
    """
    TN = 328
    FN = 'ifpp0'
    F = 'F328'
    RE = r'10(......)000010000'
    OE = (
            'fnx.pd.order',
            'fis.production.order',
            )[odoo_erp]
    IMD = 'production_order'
    OE_KEY = 'order_no'
    OE_FIELDS = (
            'id', 'order_no', 'ordered_qty', 'completed_fis_qty', 'confirmed', 'item_id',
            'formula_code', 'line_id', 'schedule_date', 'finish_date',
            'line_id_set', 'schedule_date_set', 'state', 'coating', 'allergens',
            'batches',
            )
    OE_FIELDS += (('dept','department')[odoo_erp], )
    FIS_SCHEMA = (
            F328.order_no, F328.produced, F328.order_confirmed, F328.prod_no,
            F328.formula_id, F328.formula_rev, F328.dept_id, F328.prod_line,
            F328.prod_scheduled_date, F328.prod_date, F328.units_produced,
            F328.no_of_batches_a, F328.prod_qty
            )
    #
    ProductionOrder = XmlLink

    def __init__(self, oe, config, *args, **kwds):
        super(IFPP0, self).__init__(oe ,config, *args, **kwds)
        #
        # get current production lines from OE as there may be user
        # specified multi-lines
        #
        multiline_table = ('fnx.pd.multiline','fis.production.multiline')[odoo_erp]
        cnvzf_name = '%s_%%_%s' % (CNVZf.F, CNVZf.IMD)
        self.production_lines = dict(
                (r[FIS_ID], CNVZf.ProductionLine(r[FIS_ID], r.id))
                for r in self.get_xid_records(
                    self.erp,
                    domain=[('module','=','fis'),('name','=like',cnvzf_name)],
                    fields=['id', FIS_ID],
                    context=self.context,
                    ))
        multi_lines = dict(
                (r.key, r.line_ids)
                for r in self.get_records(
                    self.erp,
                    multiline_table,
                    fields=['key','line_ids'],
                    ))
        for key, lines in multi_lines.items():
            for i, line in enumerate(lines):
                lines[i] = CNVZf.ProductionLine(line.name, line.id)
            self.production_lines[key] = lines
        IFMS(oe, config).reify(['coating','allergens'])

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        "sales production order"
        # convert the record into the following fields:
        #   id, order_no, completed_fis_qty, confirmed, item_id,
        #   formula_code, dept, line_id,
        #   schedule_date, finish_date, completed_fis_qty,
        #
        # F328.order_no, F328.produced, F328.order_confirmed, F328.prod_no,
        # F328.formula_id, F328.formula_rev, F328.dept_id, F328.prod_line,
        # F328.prod_scheduled_date, F328.prod_date, F328.units_produced,
        #
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F328.order_no]
        item = fis_rec[F328.prod_no]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        order = AttrDict().fromkeys(self.OE_FIELDS, None)
        order.order_no = key
        order.item_id = NVTY.Product(item)
        order.completed_fis_qty = fis_rec[F328.units_produced]
        status = fis_rec[F328.produced]
        if status == 'Y':
            order.state = 'complete'
        elif status == 'X':
            order.state = 'cancelled'
        else:
            order.state = 'draft'
        order.confirmed = (None, 'fis')[fis_rec[F328.order_confirmed] == 'Y']
        formula = '%s-%s' % (fis_rec[F328.formula_id], fis_rec[F328.formula_rev])
        order.formula_code = ('[%s] %s' % (formula, fis_rec[F328.label_name])).replace('\x01','')
        dept = ('dept', 'department')[odoo_erp]
        order[dept] = fis_rec[F328.dept_id] or None
        line_id = fis_rec[F328.prod_line]
        if line_id and len(line_id) == 1:
            line_id = '0' + line_id
        order.line_id = self.production_lines.get(line_id)
        order.line_id_set = False
        sched_date = fix_date(fis_rec[F328.prod_scheduled_date], 'ymd') or None
        order.schedule_date = sched_date
        order.schedule_date_set = False
        order.ordered_qty = fis_rec[F328.prod_qty]
        fin_date = fix_date(fis_rec[F328.prod_date], 'mdy') or None
        if fin_date:
            fin_date = local_to_utc(DateTime.combine(fin_date, Time(17)))
        order.finish_date = fin_date
        order.completed_fis_qty = fis_rec[F328.units_produced] or 0
        formula = IFMS.ProductFormula(item)
        if formula:
            order.coating = formula.coating
            order.allergens = formula.allergens
        order.batches = numeric(fis_rec[F328.no_of_batches_a])
        #
        # do we need more than one order?
        #
        if not isinstance(order.line_id, list):
            return (XidRec.fromdict(order, imd), )
        #
        # yes we do
        #
        orders = []
        template = order
        total = len(template.line_id)
        for i, line in enumerate(template.line_id, start=1):
            key = '%s-%d_%d' % (template.order_no, i, total)
            imd = AttrDict(
                    id=0,
                    model=self.OE,
                    res_id=0,
                    module='fis',
                    name=self.calc_xid(key),
                    )
            order = AttrDict().fromkeys(self.OE_FIELDS, None)
            order.update(template)
            order.order_no = key
            order.line_id = line
            orders.append(XidRec.fromdict(order, imd))
        return tuple(orders)

    def normalize_records(self, fis_rec, oe_rec):
        super(IFPP0, self).normalize_records(fis_rec, oe_rec)
        #
        if fis_rec.state == 'draft':
            fis_rec.state = oe_rec.state
        # if oe_rec already has a finish date, remove it
        # TODO: figure out why a changed finish_date isn't updated on OpenERP
        if oe_rec.finish_date:
            fis_rec.finish_date = oe_rec.finish_date
        if oe_rec.line_id_set:
            fis_rec.line_id_set = True
            fis_rec.line_id = oe_rec.line_id
        if oe_rec.schedule_date_set:
            fis_rec.schedule_date_set = True
            fis_rec.schedule_date = oe_rec.schedule_date

class IFPP1(Synchronize):
    """
    production order ingredient, 329  (IFPP0, NVTY)
    """
    TN = 329
    FN = 'ifpp1'
    F = 'F329'
    RE = r"10(......)000011..."
    OE = (
            'fnx.pd.ingredient',
            'fis.production.ingredient',
            )[odoo_erp]
    IMD = 'production_ingredient'
    OE_KEY = 'name'
    OE_FIELDS = ('id', 'name', 'sequence', 'order_ids', 'item_id', 'qty_needed', 'qty_desc')
    FIS_SCHEMA = (
            F329.order_no, F329.ingr_code_batch_1, F329.units_batch_1, F329.qty_batch_1, F329.formula_line_no
            )
    def FIS_IGNORE_RECORD(self, rec):
        if rec[F329.item_type_batch_1] == 'M':
            return True
        elif rec[F329.ingr_code_batch_1] in ignored_ingredients:
            return True
        elif rec[F329.qty_batch_1] <= 0:
            return True
        order_no = rec[F329.order_no]
        if order_no not in self.oe_orders:
            return True
        return False

    def __init__(self, oe, config, *args, **kwds):
        super(IFPP1, self).__init__(oe, config, *args, **kwds)
        #
        # get all valid order numbers from OE, along with batch qty
        #
        ifpp0_name = '%s_%%_%s' % (IFPP0.F, IFPP0.IMD)
        orders = self.get_xid_records(
                self.erp,
                domain=[('module','=','fis'),('name','=like',ifpp0_name)],
                fields=['id','order_no','batches'],
                context=self.context,
                )
        self.oe_orders = {}
        # combine multiple steps under main order number, and convert order references
        # to Many2One
        for order in orders:
            self.oe_orders.setdefault(
                    order.order_no[:6], []
                    ).append(
                    IFPP0.ProductionOrder(order.order_no, order.id, batches=order.batches)
                    )

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        "order ingredient"
        # convert the record into the following fields:
        #   name, order_id, item_id, qty_needed, qty_desc
        #
        # multiply qty_needed by F328.no_of_batches_a
        #
        # using:
        #   F329.order_no, F329.ingr_code_batch_1, F329.qty_batch_1, F329.units_batch_1
        #
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        order = fis_rec[F329.order_no]
        item = fis_rec[F329.ingr_code_batch_1]
        key = '%s:%s' % (order, item)
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        ingredient = AttrDict().fromkeys(self.OE_FIELDS, None)
        ingredient.order_ids = self.oe_orders.get(fis_rec[F329.order_no])
        ingredient.item_id = NVTY.Product(fis_rec[F329.ingr_code_batch_1])
        ingredient.name = key
        ingredient.sequence = int(fis_rec[F329.formula_line_no] or 0)
        ingredient.qty_desc = fis_rec[F329.units_batch_1] or None
        production_order = ingredient.order_ids and ingredient.order_ids[0] or None
        if production_order:
            batches_needed = production_order.batches
        else:
            batches_needed = 0
        try:
            ingredient.qty_needed = fis_rec[F329.qty_batch_1] * batches_needed
        except:
            echo(order, item, key)
            echo(ingredient.order_ids)
            echo(ingredient.item_id)
            echo(production_order, production_order.batches)
            raise
        return (XidRec.fromdict(ingredient, imd), )

class NVTY(Synchronize):
    """
    products, 135  (CNVZas)
    """
    TN = 135
    FN = 'nvty'
    F = 'F135'
    RE = r'......101000    101\*\*'
    OE = 'product.product'
    IMD = 'product_product'
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F%s' % TN
    OE_FIELDS_QUICK = (
            'id', FIS_MODULE, FIS_ID, ('warranty','fis_shelf_life')[odoo_erp],
            'active', 'name', 'fis_name', 'fis_qty_on_hand', 'fis_availability_code',
            'sale_ok', 'trademarks', 'ean13', 'fis_location',
            'fis_shipping_size', 'categ_id', 'default_code', 'weight',
            'weight_net', 'list_price', 'lst_price', 'price',
            )
    OE_FIELDS_LONG = OE_FIELDS_QUICK + (
            'fis_qty_produced', 'fis_10_day_produced', 'fis_21_day_produced',
            'fis_qty_consumed', 'fis_10_day_consumed', 'fis_21_day_consumed',
            'fis_qty_purchased', 'fis_10_day_purchased', 'fis_21_day_purchased',
            'fis_qty_sold', 'fis_10_day_sold', 'fis_21_day_sold',
            'fis_qty_available', 'fis_10_day_available', 'fis_21_day_available',
            'fis_web_ingredients', 'fis_web_prep_instructions',
            )
    FIS_SCHEMA = (
            F135.item_id,
            F135.available_key, F135.sales_cat, F135.trademarkd,
            F135.catalog_location, F135.desc, F135.size, F135.upc_no, F135.primary_location,
            F135.supplier_id, F135.new_retail, F135.new_per_unit,
            F135.net_un_wt, F135.grs_un_wt,
            )
    FIELDS_CHECK_IGNORE = ('name', )
    #
    Product = XmlLink

    def FIS_IGNORE_RECORD(self, rec):
        return rec[F135.wrhse_no] != '1000'


    def __init__(self, *args, **kwds):
        super(NVTY, self).__init__(*args, **kwds)
        self.INVALID_CATEGORY = CNVZas.ProductCategory(INVALID_CATEGORY_XML_ID)
        _, self.INVALID_CATEGORY.id = self.ir_model_data.get_object_reference(
                'fis', INVALID_CATEGORY_XML_ID,
                )

    @staticmethod
    def in_catalog(rec):
        warehouse = rec[F135.wrhse_no]
        avail_code = rec[F135.available_key]
        location = rec[F135.catalog_location]
        return warehouse == '1000' and avail_code in 'YPW' and len(location) == 10

    def convert_fis_rec(self, fis_rec, use_ignore=False):
        # some fields come from non-FIS locations or are only updated once per
        # day -- those fields will not be evaluated here:
        # - name -> get_product_descriptions()
        # - fis_qty: _produced, _consumed, _purchased, _sold, _available
        # - fis_10_day: _produced, _consumed, _purchased, _sold, _available
        # - fis_21_day: _produced, _cosnumed, _purchased, _sold, _available
        if use_ignore and self.FIS_IGNORE_RECORD(fis_rec):
            return ()
        key = fis_rec[F135.item_id]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        item = AttrDict.fromkeys(self.OE_FIELDS, None)
        if odoo_erp:
            item.fis_id = key
            item.fis_module = self.OE_KEY_MODULE
            item.fis_shelf_life = float(fis_rec[F135.shelf_life_mos] or 0.0)
        else:
            item.xml_id = key
            item.module = self.OE_KEY_MODULE
            item.warranty = float(fis_rec[F135.shelf_life_mos] or 0.0)
        item.default_code = key
        name = NameCase(fis_rec[F135.desc].strip())
        name = re.sub('sunridge', 'SunRidge', name, flags=re.I) or None
        item.fis_name = name
        item.name = name
        item.active = True
        item.fis_availability_code = fis_rec[F135.available_key] or None
        # sale_ok actually tracks whether item is in the catalog with a Y, P, or W code
        item.sale_ok = self.in_catalog(fis_rec)
        item.trademarks = fis_rec[F135.trademarkd] or None
        item.ean13 = sanitize_ean13(fis_rec[F135.upc_no]) or None
        item.fis_location = fis_rec[F135.primary_location] or None
        item.fis_qty_on_hand = fis_rec[F135.qty_on_hand]
        item.weight = numeric(fis_rec[F135.grs_un_wt])
        item.weight_net = numeric(fis_rec[F135.net_un_wt])
        item.lst_price = numeric(fis_rec[F135.new_retail])      # "A" price
        item.list_price = numeric(fis_rec[F135.new_retail])     # to be consistent
        item.price = numeric(fis_rec[F135.new_per_unit])        # per unit price
        # 0,2,5,7,36,48,51,52,50,55,56,93,94,99,115,116
        shipping_size = fis_rec[F135.size].strip()
        if shipping_size.lower() in ('each','1 each','1/each'):
            shipping_size = '1 each'
        elif shipping_size:
            first, last = [], []
            letters = False
            for char in shipping_size:
                if char < ' ':
                    char = ' '
                if letters or char.isalpha():
                    last.append(char.lower())
                    letters = True
                else:
                    first.append(char)
            if last == ['z']:
                last.insert(0, 'o')
            shipping_size = ('%s %s' % (''.join(first).strip(), ''.join(last).strip())).strip()
        item.fis_shipping_size = shipping_size or None
        #
        category_code = fis_rec[F135.sales_cat].strip()
        if len(category_code) == 2 and category_code[0] in 'OIG':
            category_code = {'O':'0', 'I':'1', 'G':'6'}[category_code[0]] + category_code[1]
        item.categ_id = CNVZas.ProductCategory(category_code)
        #
        #
        return (XidRec.fromdict(item, imd), )

    def normalize_fis(self, method):
        super(NVTY, self).normalize_fis(method)
        if method == 'full':
            print('getting forecast data')
            forecast_data = get_product_forecast(self.config.network.fis_data_local_path/'product_forecast.txt')
        else:
            forecast_data = {}
        print('getting description data')
        description_data = get_product_descriptions(self.config.network.fis_data_local_path/'product_descriptions.txt')
        for (fis_module, fis_id), rec in self.fis_records.items():
            #
            desc = description_data.get(fis_id)
            rec.name = desc or rec.fis_name or None
            #
            if not rec.categ_id:
                rec.categ_id = self.INVALID_CATEGORY
            #
            if method == 'full':
                label_data = ProductLabelDescription(fis_id)
                rec.fis_web_ingredients = label_data.ingredients_text or None
                rec.fis_web_prep_instructions = label_data.recipe_text or None
                #
                forecast = forecast_data.get(fis_id)
                rec.fis_qty_produced = 0
                rec.fis_qty_consumed = 0
                rec.fis_qty_purchased = 0
                rec.fis_qty_sold = 0
                rec.fis_qty_available = 0
                rec.fis_10_day_produced = 0
                rec.fis_10_day_consumed = 0
                rec.fis_10_day_purchased = 0
                rec.fis_10_day_sold = 0
                rec.fis_10_day_available = 0
                rec.fis_21_day_produced = 0
                rec.fis_21_day_consumed = 0
                rec.fis_21_day_purchased = 0
                rec.fis_21_day_sold = 0
                rec.fis_21_day_available = 0
                if forecast is not None:
                    # the first four of the above values do not change
                    _, _10_day, _21_day = forecast
                    rec.fis_qty_available = rec.fis_qty_on_hand
                    rec.fis_10_day_produced = _10_day.produced
                    rec.fis_10_day_consumed = _10_day.consumed
                    rec.fis_10_day_purchased = _10_day.purchased
                    rec.fis_10_day_sold = _10_day.sold
                    rec.fis_10_day_available = rec.fis_qty_on_hand + sum(_10_day)
                    rec.fis_21_day_produced = _21_day.produced
                    rec.fis_21_day_consumed = _21_day.consumed
                    rec.fis_21_day_purchased = _21_day.purchased
                    rec.fis_21_day_sold = _21_day.sold
                    rec.fis_21_day_available = rec.fis_qty_on_hand + sum(_21_day)

    def normalize_records(self, fis_rec, oe_rec):
        super(NVTY, self).normalize_records(fis_rec, oe_rec)
        if fis_rec.name is None:
            fis_rec.name = oe_rec.name


class POSM_VNMS(SynchronizeAddress):
    """
    vendors & suppliers, 163 & 65
    """
    # VNMS_TN = 163
    # VNMS_FN = 'vnms'
    # VNMS_F = 'F163'
    # VNMS_OE = 'res.partner'
    # VNMS_IMD = VNMS_OE.replace('.','_')
    # suppliers/vendors, 65 & 163
    TN = 163
    TN_2ND = 65
    FN = 'posm'
    FN_2ND = 'vnms'
    F = 'F163'
    OE = 'res.partner'
    IMD = 'res_partner'
    RE = r"10(......)"
    OE_KEY = FIS_ID
    OE_KEY_MODULE = 'F163'
    OE_FIELDS = (
            'id', FIS_MODULE, FIS_ID, 'active', 'phone', 'fax',
            'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id',
            'fis_valid', 'is_company', 'customer', 'supplier',
            'fis_updated_by_user', 'use_parent_address',
            'fis_org_cert_file', 'fis_non_gmo', 'fis_kosher', 'fis_org_exp',
            'fis_gmo_exp', 'fis_kosher_exp',
            )
    FIS_SCHEMA = ()
    FIELDS_CHECK_IGNORE = ('active', 'name')

    def FIS_IGNORE_RECORD(self, rec):
        key = rec['An$(3,6)']
        name = rec['Bn$']
        address = (' '.join([rec[c] for c in ('Cn$','Dn$','En$')])).upper()
        return (
                not name
                or len(key) != 6 or not key.isdigit()
                or '**NO LONGER HERE**' in address
                or '**OLDER/N.L.H. EMPLOYEE**' in address
                or '**DISCO' in address
                )

    def convert_fis_rec(self, posm_vnms, use_ignore=True):
        #
        # creates a company AttrDict with the following fields
        # - '(fis_)module', '(fis|xml)_id', 'active',
        # - 'name', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id',
        # - 'fis_valid', 'phone', 'fax', 'is_company', 'customer', 'fis_org_cert_file',
        # - 'fis_non_gmo', 'fis_kosher', 'fis_org_exp', 'fis_gmo_exp', 'fis_kosher_exp',
        #
        # creates a contact AttrDict with the following fields
        # - 'module', 'xml_id', 'active', 'name', 'phone', 'fax',
        # - 'is_company', 'customer', 'supplier', 'fis_valid',
        #
        # fields coming from OpenERP that are missing/invalid on the FIS side
        # - 'id', 'fis_updated_by_user'
        # - address fields (for contact)
        #
        posm_rec, vnms_rec = posm_vnms
        if use_ignore and posm_rec and self.FIS_IGNORE_RECORD(posm_rec):
            posm_rec = None
        if use_ignore and vnms_rec and self.FIS_IGNORE_RECORD(vnms_rec):
            vnms_rec = None
        if posm_rec is vnms_rec is None:
            return ()
        if posm_rec is not None:
            contact_key = posm_rec[F163.vendor]
            if not contact_key:
                vnms_rec = None
        key = posm_rec and posm_rec[F163.code] or vnms_rec and vnms_rec[F65.code]
        imd = AttrDict(
                id=0,
                model=self.OE,
                res_id=0,
                module='fis',
                name=self.calc_xid(key),
                )
        company = AttrDict().fromkeys(self.OE_FIELDS, None)
        company[FIS_ID] = key
        company[FIS_MODULE] = self.OE_KEY_MODULE
        company.active = True
        company.fis_updated_by_user = ''
        company.is_company = True
        company.customer = False
        company.supplier = True
        company.use_parent_address = False
        company.fis_valid = len(key) == 6 and key.isdigit()
        if posm_rec is not None:
            names, address, do_not_use = self.process_name_address(F163, posm_rec)
            pname = names and names[0] or ''
            pname = re.sub('sunridge', 'SunRidge', BsnsCase(pname), flags=re.I)
            if re.match('HE\d\d\d$', key) and pname.startswith('Heb '):
                pname = 'HEB ' + pname[4:]
            names[0:1] = [pname]
            name = ', '.join(names)
            dnu = ', '.join(do_not_use)
            name = ' / '.join([l for l in (name, dnu) if l])
            # if not name:
            #     return ()
            company.name = name
            company.update(address)
            company.phone = Phone(posm_rec[F163.tele])
            company.fax = Phone(posm_rec[F163.fax])
            company.fis_org_cert_file = posm_rec[F163.org_cert_file].upper() in ('Y','O')
            company.fis_org_exp = fix_date(posm_rec[F163.cert_exp]) or None
            company.fis_non_gmo = posm_rec[F163.non_gmo].upper() == 'Y'
            company.fis_kosher = posm_rec[F163.kosher].upper() == 'Y'
            company.fis_gmo_exp = fix_date(posm_rec[F163.gmo_exp]) or None
            company.fis_kosher_exp = fix_date(posm_rec[F163.kosher_exp]) or None
        elif vnms_rec is not None:
            names, address, do_not_use = self.process_name_address(F65, vnms_rec)
            pname = names and names[0] or ''
            pname = re.sub('sunridge', 'SunRidge', BsnsCase(pname), flags=re.I)
            if re.match('HE\d\d\d$', key) and pname.startswith('Heb '):
                pname = 'HEB ' + pname[4:]
            names[0:1] = [pname]
            name = ', '.join(names)
            dnu = ', '.join(do_not_use)
            name = ' / '.join([l for l in (name, dnu) if l])
            # if not name:
            #     return ()
            company.name = name
            company.update(address)
            company.phone = Phone(vnms_rec[F65.tele])
            company.fax = Phone(vnms_rec[F65.fax])
            company.fis_org_cert_file = vnms_rec[F65.org_cert_file].upper() in ('Y','O')
            company.fis_org_exp = fix_date(vnms_rec[F65.cert_exp]) or None
            company.fis_non_gmo = False
            company.fis_kosher = False
            company.fis_gmo_exp = None
            company.fis_kosher_exp = None
        else:
            error("invalid POSM/VNMS fis_id: %r" % (key, ))
            return ()
        company = XidRec.fromdict(
                company,
                imd,
                types={
                    'fis_kosher': (bool, ),
                    'fis_non_gmo': (bool, ),
                    'fis_org_cert_file': (bool, ),
                    },
                )
        #
        def strip_ext(text):
            m = re.match('^(.*)[- ](x\d+)$', text, re.I)
            ext = ''
            if m:
                text, ext = m.groups()
            return text, ext.lower()
        #
        contact = None
        ext = ''
        if vnms_rec is not None and vnms_rec[F65.contact]:
            name, ext = strip_ext(NameCase(vnms_rec[F65.contact]))
            unk = name.split()[-1]
            if (    unk.lower()[0] == 'x' and unk[1:].isdigit()
                 or unk.lower()[:3] == 'ext' and unk[3:].isdigit()
                 ):
                ext = unk.lower()
                name = ' '.join(name.split()[:-1])
            name = name or None
            phone = Phone(vnms_rec[F65.tele], ext)
            fax = Phone(vnms_rec[F65.fax])
            if not name:
                # try to save any phone numbers from the contact
                if not company.phone.number:
                    company.phone = phone
                elif company.phone.base == phone.base and not company.phone.ext:
                    company.phone.ext = phone.ext
                phone = None
            if fax.base == company.fax.base:
                if fax.ext == company.fax.ext or fax.ext and not company.fax.ext:
                    company.fax.ext = fax.ext
                    fax = None
            if name or phone or fax:
                contact = AttrDict().fromkeys(self.OE_FIELDS, None)
                contact[FIS_MODULE] = 'F163'
                contact[FIS_ID] = 'cntct_' + key
                contact.fis_updated_by_user = ''
                contact.active = company.active
                contact.name = name or 'extra info'
                contact.fis_valid = company.fis_valid
                contact.is_company = False
                contact.customer = False
                contact.supplier = True
                contact.use_parent_address = False
                contact.street = company.street
                contact.street2 = company.street2
                contact.city = company.city
                contact.state_id = company.state_id
                contact.zip = company.zip
                contact.country_id = company.country_id
                contact.phone = Phone(vnms_rec[F65.tele], ext)
                contact.fax = Phone(vnms_rec[F65.fax])
                contact.fis_org_cert_file = False
                contact.fis_non_gmo = False
                contact.fis_kosher = False
                imd = AttrDict(
                        id=0,
                        model=self.OE,
                        res_id=0,
                        module='fis',
                        name=self.calc_xid(contact[FIS_ID]),
                        )
                contact = XidRec.fromdict(
                        contact,
                        imd,
                        types={
                            'fis_kosher': (bool, ),
                            'fis_non_gmo': (bool, ),
                            'fis_org_cert_file': (bool, ),
                            },
                        )
        if contact is not None:
            if not re.match('\w{2,}', name or ''):
                contact.active = False
            return company, contact
        else:
            return (company, )

    fis_quick_load = SynchronizeAddress.fis_long_load

    def open_fis_tables(self):
        posm_table = self.get_fis_table(self.TN, rematch=self.RE)
        vnms_table = self.get_fis_table(self.TN_2ND, rematch=self.RE)
        old_posm_table = self.get_fis_table(
                self.TN,
                rematch=self.RE,
                data_path=self.config.network.fis_data_local_old_path,
                )
        old_vnms_table = self.get_fis_table(
                self.TN_2ND,
                rematch=self.RE,
                data_path=self.config.network.fis_data_local_old_path,
                )
        print('posm: %d\nvnms: %d\nold posm: %d\nold vnms: %d' % (
                    len(posm_table), len(vnms_table),
                    len(old_posm_table), len(old_vnms_table),
                    ),
                verbose=2,
                )
        #
        self.fis_table = PsuedoFisTable('combined posm/vnms table')
        self.old_fis_table = PsuedoFisTable('old combined posm/vnms table')
        all_keys = list(posm_table.keys()) + list(vnms_table.keys())
        all_old_keys = list(old_posm_table.keys()) + list(old_vnms_table.keys())
        for key in all_keys:
            self.fis_table[key] = posm_table.get(key), vnms_table.get(key)
        for key in all_old_keys:
            self.old_fis_table[key] = old_posm_table.get(key), old_vnms_table.get(key)

def get_customer_aging(aging_file):
    aging_data = {}
    with open(aging_file) as af:
        lines = [line for line in af.read().split('\n') if line.strip()]
    try:
        for line in lines:
            # isolate FIS code
            key, rest = line.split(None, 1)
            # lines with filenames are invalid
            if key.endswith(':'):
                continue
            # isolate other info, ignoring company name
            limit, salesrep, total, d0, d10, d20, d30 = line.rsplit(None, 8)[-7:]
            aging_data[key] = CustomerAging(key, limit, d0, d10, d20, d30, total)
        return aging_data
    except Exception as exc:
        echo(exc, border='box')
        return {}

def get_product_descriptions(desc_file):
    descriptions = {}
    with open(desc_file) as f:
        lines = f.read().split('\n')
    for line in lines:
        match = re.match('(.{40})  \((\d{6})\)  (.*)$', line)
        if match:
            fis_desc, item_code, full_desc = match.groups()
            descriptions[item_code] = full_desc or fis_desc or None
    return descriptions

def get_product_forecast(pf_file):
    # parse the daily-updated file with the product forecasts
    forecast = {}
    with open(pf_file) as f:
        lines = f.read().split('\n')
    for i, line in enumerate(lines):
        if not line.strip() or '-' not in line:
            continue
        try:
            text = line.split(' - ')[1]
        except IndexError:
            continue
        if 'ERROR' in text:
            continue
        try:
            item_code, _10_day, _21_day = text.split(':')
        except ValueError:
            continue
        prod_in, purch, prod_out, sold = _10_day.split()[2:6]
        prod_in = float(prod_in)
        purch = float(purch)
        prod_out = -(float(prod_out))
        sold = -(float(sold))
        _10_day = ForecastDetail(prod_in, purch, prod_out, sold)
        prod_in, purch, prod_out, sold = _21_day.split()[2:6]
        prod_in = float(prod_in)
        purch = float(purch)
        prod_out = -(float(prod_out))
        sold = -(float(sold))
        _21_day = ForecastDetail(prod_in, purch, prod_out, sold)
        forecast[item_code] = Forecast(item_code, _10_day, _21_day)
    return forecast

_raise_lookup = object()
class Specials(str, Enum):
    _order_ = 'neither catalog specials both default'
    neither   = 'N'
    catalog   = 'C'
    specials  = 'S'
    both      = 'B'
    default   = 'D'
    company   = default
    @classmethod
    def get_member(cls, text, default=_raise_lookup):
        for member in cls:
            if member.value == text:
                return member
        else:
            if default is not _raise_lookup:
                return default
        raise LookupError('%r not found in %s' % (text, cls.__name__))


def is_contact(obj):
    "obj must be either a string or have an xml_id key"
    if not isinstance(obj, basestring):
        obj = obj.get(FIS_ID)
    return obj.startswith('cntct_')

def sanitize_ean13(ean13):
    """
    Creates and returns a valid ean13 from an invalid one
    """
    if not ean13:
        return "0000000000000"
    ean13 = re.sub("[A-Za-z]", "0", ean13);
    ean13 = re.sub("[^0-9]", "", ean13);
    ean13 = ean13[:13]
    if len(ean13) < 13:
        ean13 = ean13 + '0' * (13-len(ean13))
    return ean13[:-1] + str(ean_checksum(ean13))

def ean_checksum(eancode):
    """
    returns the checksum of an ean string of length 13, returns -1 if the string has the wrong length
    """
    if len(eancode) != 13:
        return -1
    oddsum=0
    evensum=0
    total=0
    eanvalue=eancode
    reversevalue = eanvalue[::-1]
    finalean=reversevalue[1:]
    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total=(oddsum * 3) + evensum
    check = int(10 - math.ceil(total % 10.0)) % 10
    return check

def numeric(number):
    if isinstance(number, (int, long, float)):
        return number
    try:
        return int(number)
    except ValueError:
        try:
            return float(number)
        except ValueError:
            pass
    return False

def get_updated_values(old_record, new_record):
    changes = AttrDict()
    for key in old_record:
        old_value = old_record[key]
        new_value = new_record[key]
        if (old_value or new_value) and old_value != new_value:
            changes[key] = new_value
    return changes

class CustomerAging(NamedTuple):
    _order_ = "xml_id limit current d10 d20 d30 total"
    xml_id = 'customer key'
    limit = 'credit limit'
    current = 'charges within 10 days'
    d10 = 'charges between 11 and 20 days old'
    d20 = 'charges between 21 and 30 days old'
    d30 = 'charges over 30 days old'
    total = 'total outstanding balance'

    def __new__(cls, *values):
        new_values = [values[0]]
        for value in values[1:]:
            value = value.replace(',','')
            if value[-1:] == '-':
                value = '-' + value[:-1]
            new_values.append(float(value))
        return NamedTuple.__new__(CustomerAging, *new_values)


class ForecastDetail(NamedTuple):
    produced = 0, None, 0.0
    purchased = 1, None, 0.0
    consumed = 2, None, 0.0
    sold = 3, None, 0.0


class Forecast(NamedTuple):
    item = 0, None, ''
    day_10 = 1, None, ForecastDetail()
    day_21 = 2, None, ForecastDetail()



