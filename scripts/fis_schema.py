import aenum
from VSS.utils import LazyClassAttr

class FISenum(str, aenum.Enum):

    FIS_names = LazyClassAttr(set, name='FIS_names')

    def __init__(self, spec):
        if '(' in spec:
            fis_name, segment = spec.split('(', 1)
            segment = segment.strip(' )')
        else:
            fis_name = spec
            segment = None
        self.fis_name = fis_name
        self.segment = segment
        self.__class__.FIS_names.add(fis_name)

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self._name_)

class F8(FISenum):
    """
    CNVZD0 - Customer Payment Terms Codes
    """
    key_type                    = 'An$(1,2)'     #   0: Key Group = 'D0'
    company_id                  = 'An$(3,2)'     #   1: Company Code
    code                        = 'An$(5,1)'     #   2: Terms Code
    description                 = 'Bn$'          #   3: Terms Description

class F11(FISenum):
    """
    CNVZas - SALES CATEGORY MASTER
    """
    key_type                 = 'An$(1,2)'      #   0: KEY TYPE = as
    company                  = 'An$(3,2)'      #   1: COMPANY
    sales_category_id        = 'An$(5,2)'      #   2: Sales Category Code
    desc                     = 'Cn$'           #   8: Description
    shelf_life               = 'Fn'            #  11: MONTHS SHELF LIFE


class F27(FISenum):
    "Carrier (Ship Via) Master File (key starts with SV)"
    company_id = 'An$(3,2)'
    code = 'An$(5,2)'
    name = 'Bn$'
    addr1 = 'Cn$'
    addr2 = 'Dn$'
    addr3 = 'En$'
    tele = 'Fn$'
    fuel_surcharge = 'Gn$'

class F33(FISenum):
    """
    CSMS - CUSTOMER MASTER FILE - BASIC RECORD
    """
    company_id            = 'An$(1,2)'       # COMPANY CODE
    code                  = 'An$(3,6)'       # CUSTOMER NO.
    name                  = 'Bn$'            # NAME
    addr1                 = 'Cn$'            # ADDR LINE 1
    addr2                 = 'Dn$'            # ADDR LINE 2
    addr3                 = 'En$'            # ADDR LINE 3
    postal                = 'Ln$'            # ZIP CODE
    contract_prices       = 'Fn$(1,1)'       # Contract Prices?
    price_list_id         = 'Fn$(2,1)'       # Price List Code
    catalog_category      = 'Fn$(8,1)'       # Catalog Category
    back_ord_ind          = 'Fn$(9,1)'       # BACK ORD IND
    link_to_ship_to       = 'Fn$(10,1)'      # Link to Ship-to
    rebate_category_id    = 'Fn$(15,1)'      # Rebate category code(sp=none)
    price_chg_days_notice = 'Fn$(16,3)'      # Price Chg Days Notice
    bol_required          = 'Fn$(19,1)'      # BOL Required?
    outstand_orders       = 'Hn'             # OUTSTAND ORDERS
    this_year_sales       = 'Ln'             # M-T-D SALES
    last_year_sales       = 'Pn'             # Prev Year Sales
    broker_id             = 'Gn$(1,3)'       # Broker Code
    salesrep              = 'Gn$(4,3)'       # Salesrep Code
    payment_terms_id      = 'Gn$(19,1)'     # Payment Terms Code
    tele                  = 'Gn$(20,10)'     # Telephone Number
    bulk_cust_type        = 'Gn$(38,2)'      # Bulk Customer Type
    update_s_a            = 'Gn$(40,1)'      # Update S/A?
    cust_type_id          = 'Hn$(1,2)'       # Customer Type Code
    sales_class_id        = 'Hn$(3,4)'       # Sales Class Code
    pricing_method        = 'Hn$(7,2)'       # Pricing Method
    reseller_no           = 'Hn$(9,14)'      # Reseller Number
    fuel_surcharge        = 'Hn$(23,6)'      # Fuel Surcharge
    available             = 'Hn$(30,1)'      # available
    expiredt_on_docs      = 'Hn$(31,1)'      # ExpireDt on Docs
    alpha_sort_key        = 'In$'            # Alpha Sort Key
    comments              = 'Jn$'            # Accntg Comments
    contact               = 'Kn$'            # Acctg Contact

class F47(FISenum):
    "CNVZZ - CBS SALESMAN MASTER FILE"
    key_type                  = 'An$(1,1)'      # KEY TYPE = 'Z'
    salesperson_id            = 'An$(2,3)'      # SALESPERSON CODE
    salesperson_name          = 'Bn$'           # SALESPERSON NAME
    company_id                = 'Fn$(1,2)'      # COMPANY CODE
    phone_no                  = 'Fn$(3,10)'     # PHONE NUMBER
    salesinq_access           = 'Hn$'           # SalesInq Access

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
    gl_exp_acct =   'On$'

class F74(FISenum):
    "EMP1 - P/R EMPLOYEE MASTER BASIC RECORD MAINT/INQUIRY"
    company_id        = 'An$(1,2)'       # COMPANY CODE
    emp_num           = 'An$(3,5)'       # EMPLOYEE NO.
    name              = 'Bn$'            # EMPLOYEE NAME
    addr1             = 'Cn$'            # ADDRESS 1
    addr2             = 'Dn$'            # ADDRESS 2
    addr3             = 'En$'            # ADDRESS 3
    ssn               = 'Fn$'            # SOC.SEC.NO.
    tele              = 'Gn$'            # TELEPHONE NO.
    date_hired        = 'In$(1,6)'       # DATE HIRED
    date_terminated   = 'In$(7,6)'       # DATE TERMINATED
    birth_date        = 'In$(19,6)'      # BIRTHDATE
    last_raise        = 'In$(43,6)'      # Last Raise
    home_dept         = 'Jn$(1,2)'       # HOME DEPARTMENT
    status_flag       = 'Kn$(1,1)'       # STATUS FLAG
    pay_type          = 'Kn$(2,1)'       # PAY TYPE
    marital_status    = 'Kn$(4,1)'       # MARITAL STATUS
    pension_status    = 'Kn$(8,1)'       # PENSION STATUS
    gender            = 'Kn$(21,1)'      # GENDER
    driver_license    = 'Kn$(26,10)'     # Driver's Lic #
    emergency_contact = 'Kn$(36,18)'     # Emerg Contact
    emergency_phone   = 'Kn$(54,10)'     # Emerg Phone
    exempt_fed        = 'X(0)'           # # EXEMPT-FED
    exempt_state      = 'X(1)'           # # EXEMPT-STATE
    hourly_rate       = 'R(0)'           # HOURLY RATE

class F97(FISenum):
    """
    CNVZaa - Inventory Availability Codes
    """
    key_type            = 'An$(1,2)'     #   0: Key Group = "aa"
    company_id          = 'An$(3,2)'     #   1: Company Code
    availability_id     = 'An$(5,1)'     #   2: Availability Code
    desc                = 'Bn$'          #   3: Description
    count_as_lost_sales = 'Cn$(1,1)'     #   4: Count as Lost Sales (Y/N)
    lost_sales_category = 'Cn$(2,1)'     #   5: Lost Sales Category
    availability        = 'Cn$(3,1)'     #   6: Availability(Y/N/D/H)
                                         # (open) Cn$(4,2)
    inv_print_msg       = 'Dn$'          #   8: Invoice Print Msg



class F135(FISenum):
    """
    NVTY1 - INVENTORY MASTER (STATUS & DESCRIPTION)
    """
    item_id                  = 'An$(1,6)'        #   0: Item Code
    company_id               = 'An$(7,2)'        #   1: Company Code
    warehouse_no             = 'An$(9,4)'        #   2: Warehouse Number
    company                  = 'An$(13,6)'       #   3: 4 SPACES + COMPANY
    key_type                 = 'An$(19,3)'       #   4: Key Type = '1**'
    available_key            = 'Bn$(1,1)'        #   5: Available?
    sales_category           = 'Bn$(3,2)'        #   7: Sales Category
    trademarked              = 'Bn$(117,2)'      #  48: TradeMarkd
    kosher_category          = 'Bn$(119,1)'      #  49: Kosher Catg
    catlog_location          = 'Bn$(120,10)'     #  50: Catlog Loc
    description              = 'Cn$(1,40)'       #  51: Description
    size                     = 'Cn$(41,8)'       #  52: Size
    upc_no                   = 'Dn$(6,12)'       #  55: UPC CODE
    primary_location         = 'Dn$(18,6)'       #  56: Prim Loc
    supplier_id              = 'Gn$(1,6)'        #  81: Supplier
    new_retail               = 'I(22)'           # 115: New Retail
    new_whlolesale           = 'I(23)'           # 116: New Whlsle

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

class F341(FISenum):
    "Production Line Master"
    company_id =    'An$(2,2)'
    code =          'An$(4,2)'
    desc =          'Bn$'
    short_desc =    'Cn$'


def get_changed_records(old_records, new_records, enum_schema, address_fields, ignore=lambda r: False):
    # get changed records as list of
    # (old_record, new_record, [(enum_schema_member, old_value, new_value), (...), ...]) tuples
    try:
        if issubclass(enum_schema, aenum.Enum):
            enum = enum_schema
    except TypeError:
            enum = type(enum_schema[0])
    key_fields_name = list(enum)[0].fis_name
    key_fields = [m for m in enum if m.fis_name == key_fields_name]
    if address_fields is None:
        address_fields = ()
    enum_schema = [m for m in enum_schema if m not in address_fields]
    changes = []
    added = []
    deleted = []
    old_records_map = {}
    new_records_map = {}
    for rec in old_records:
        key = []
        for f in key_fields:
            key.append(rec[f])
        key = tuple(key)
        old_records_map[key] = rec
    for rec in new_records:
        key = []
        for f in key_fields:
            key.append(rec[f])
        key = tuple(key)
        new_records_map[key] = rec
    all_recs = set(new_records_map.keys() + old_records_map.keys())
    for key in all_recs:
        changed_values = []
        new_rec = new_records_map.get(key)
        old_rec = old_records_map.get(key)
        if new_rec == old_rec:
            continue
        if new_rec is None:
            deleted.append(old_rec)
            continue
        if old_rec is None:
            added.append(new_rec)
            continue
        if ignore(new_rec):
            continue
        for field in address_fields:
            if new_rec[field] != old_rec[field]:
                # add all the address fields and dump out of the loop
                for field in address_fields:
                    changed_values.append((field, old_rec[field], new_rec[field]))
                break
        for field in enum_schema:
            if new_rec[field] != old_rec[field]:
                changed_values.append((field, old_rec[field], new_rec[field]))
        if changed_values:
            changes.append((old_rec, new_rec, changed_values))
    return changes, added, deleted

