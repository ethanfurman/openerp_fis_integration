from fnx import enum

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
