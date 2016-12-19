import enum

class FISenum(str, enum.Enum):
    pass

class F11(FISenum):
    "Sales Category codes"
    code = 'An$(5,2)'
    desc = 'Cn$'
    shelf_life = 'FN'

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
    'Customer Master'
    code =      'An$(3,6)'
    name =      'Bn$'
    addr1 =     'Cn$'
    addr2 =     'Dn$'
    addr3 =     'En$'
    postal =    'Ln$'
    salesrep =  'Gn$(4,3)'
    tele =      'Gn$(20,10)'
    contact =   'Kn$'

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
    home_dept         = 'Jn$(1,2)'       # HOME DEPARTMENT
    status_flag       = 'Kn$(1,1)'       # STATUS FLAG
    pay_type          = 'Kn$(2,1)'       # PAY TYPE
    marital_status    = 'Kn$(4,1)'       # MARITAL STATUS
    driver_license    = 'Kn$(26,10)'     # Driver's Lic #
    emergency_contact = 'Kn$(36,18)'     # Emerg Contact
    emergency_phone   = 'Kn$(54,10)'     # Emerg Phone
    exempt_fed        = 'X(0)'           # # EXEMPT-FED
    exempt_state      = 'X(1)'           # # EXEMPT-STATE
    hourly_rate       = 'R(0)'           # HOURLY RATE

class F97(FISenum):
    "Inventory Availablility Code"
    code = 'An$(5,1)'
    desc = 'Bn$'

class F135(FISenum):
    "Products"
    item_code = 'An$(1,6)'
    available = 'Bn$(1,1)'
    sales_category = 'Bn$(3,2)'
    shelf_life = 'Bn$(69,2)'
    trademark_expiry_year = 'Bn$(117,2)'
    name = 'Cn$(1,40)'
    ship_size = 'Cn$(41,8)'
    manager = 'Dn$(5,1)'
    ean13 = 'Dn$(6,12)'
    storage_location = 'Dn$(18,6)'
    on_hand = 'I(6)'
    committed = 'I(7)'
    on_order = 'I(8)'
    wholesale = 'I(23)'

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
