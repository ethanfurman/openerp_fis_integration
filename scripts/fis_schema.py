from tools import FISenum

class F8(FISenum):
    """
    CNVZD0 - Customer Payment Terms Codes
    """
    key_type                    = 'An$(1,2)', 0     #   0: Key Group = 'D0'
    company_id                  = 'An$(3,2)', 1     #   1: Company Code
    code                        = 'An$(5,1)', 2     #   2: Terms Code
    description                 = 'Bn$',      3     #   3: Terms Description

class F11(FISenum):
    """
    CNVZas - SALES CATEGORY MASTER
    """
    key_type                 = 'An$(1,2)',  0      #   0: KEY TYPE = as
    company                  = 'An$(3,2)',  1      #   1: COMPANY
    sales_category_id        = 'An$(5,2)',  2      #   2: Sales Category Code
    desc                     = 'Cn$',       8      #   8: Description
    shelf_life               = 'Fn',       11      #  11: MONTHS SHELF LIFE


class F27(FISenum):
    """
    CNVZSV - CARRIER (SHIP VIA) MASTER FILE MAINTENANCE/INQUIRY
    """
    company_id     = 'An$(3,2)',   1     # Company Code
    code           = 'An$(5,2)',   2     # Carrier Code
    name           = 'Bn$',        3     # Description/Name
    addr1          = 'Cn$',        4     # Address Line 1
    addr2          = 'Dn$',        5     # Address Line 2
    addr3          = 'En$',        6     # Address Line 3
    tele           = 'Fn$',        7     # Telephone Number
    fuel_surcharge = 'Gn$',        8     # Fuel Surcharge? (Y/N)

class F33(FISenum):
    """
    CSMS - CUSTOMER MASTER FILE - BASIC RECORD
    """
    company_id                 = 'An$(1,2)',     0     # COMPANY CODE
    code                       = 'An$(3,6)',     1     # CUSTOMER NO.
    name                       = 'Bn$',          3     # NAME
    addr1                      = 'Cn$',          4     # ADDR LINE 1
    addr2                      = 'Dn$',          5     # ADDR LINE 2
    addr3                      = 'En$',          6     # ADDR LINE 3
    postal                     = 'Ln$',          7     # ZIP CODE
    contract_prices            = 'Fn$(1,1)',     8     # Contract Prices?
    price_list_id              = 'Fn$(2,1)',     9     # Price List Code
    catalog_category           = 'Fn$(8,1)',    15     # Catalog Category
    back_ord_ind               = 'Fn$(9,1)',    16     # BACK ORD IND
    link_to_ship_to            = 'Fn$(10,1)',   17     # Link to Ship-to
    rebate_category_id         = 'Fn$(15,1)',   21     # Rebate category code(sp=none)
    price_chg_days_notice      = 'Fn$(16,3)',   22     # Price Chg Days Notice
    bol_required               = 'Fn$(19,1)',   23     # BOL Required?
    outstand_orders            = 'Hn',          31     # OUTSTAND ORDERS
    this_year_sales            = 'Ln',          35     # Y-T-D SALES
    last_year_sales            = 'Pn',          39     # Prev Year Sales
    broker_id                  = 'Gn$(1,3)',    41     # Broker Code
    salesrep                   = 'Gn$(4,3)',    42     # Salesrep Code
    payment_terms_id           = 'Gn$(19,1)',   45     # Payment terms code
    tele                       = 'Gn$(20,10)',  46     # Telephone Number
    bulk_cust_type             = 'Gn$(38,2)',   50     # Bulk Customer Type
    update_s_a                 = 'Gn$(40,1)',   51     # Update S/A?
    cust_type_id               = 'Hn$(1,2)',    53     # Customer Type Code
    sales_class_id             = 'Hn$(3,4)',    54     # Sales Class Code
    pricing_method             = 'Hn$(7,2)',    55     # Pricing Method
    reseller_no                = 'Hn$(9,14)',   56     # Reseller Number
    fuel_surcharge             = 'Hn$(23,6)',   57     # Fuel Surcharge
    available                  = 'Hn$(30,1)',   59     # available
    expiredt_on_docs           = 'Hn$(31,1)',   60     # ExpireDt on Docs
    alpha_sort_key             = 'In$',         61     # Alpha Sort Key
    comments                   = 'Jn$',         62     # Accntg Comments
    contact                    = 'Kn$',         63     # Acctg Contact


class F35(FISenum):
    """
    RDER2 - OPEN ORDER HEADER PART II - SHIP-TO INFO
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id   = 'An$(1,2)',    0     # COMPANY CODE
    order_no     = 'An$(3,6)',    1     # ORDER NO.
    release_no   = 'An$(9,2)',    2     # RELEASE NO.
    type_0001    = 'An$(11,4)',   3     # TYPE = "0001"
    ship_to_name = 'Gn$',        11     # SHIP-TO NAME
    address_1    = 'Hn$',        12     # ADDRESS 1
    address_2    = 'In$',        13     # ADDRESS 2
    address_3    = 'Jn$',        14     # ADDRESS 3


class F36(FISenum):
    """
    RDERH - OPEN ORDER HEADER MAINTENANCE & INQUIRY
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id                   = 'An$(1,2)',    0     # Company Code
    order_no                     = 'An$(3,6)',    1     # Order No
    release_no                   = 'An$(9,2)',    2     # Release No
    type_0000                    = 'An$(11,4)',   3     # TYPE = '0000'
    fwd_ptr                      = 'An',          4     # FWD PTR
    index                        = 'Bn',          5     # INDEX
    cust_no                      = 'Bn$',         6     # Customer No
    cust_name                    = 'Cn$',         7     # Customer Name
    address_1                    = 'Dn$',         8     # Address 1
    address_2                    = 'En$',         9     # Address 2
    address_3                    = 'Fn$',        10     # Address 3
    pick_start_end_yymmddhhmm    = 'Gn$',        11     # PICK START/END YYMMDDHHMM
    booking_flag                 = 'Kn$(1,1)',   15     # Booking Flag
    confirmed_flag               = 'Kn$(2,1)',   16     # Confirmed Flag
    ord_print_flag               = 'Kn$(3,1)',   17     # Ord Print Flag
    inv_flag                     = 'Kn$(4,1)',   18     # Invoice Flag
    credlim_flag                 = 'Kn$(5,1)',   19     # CREDLIM FLAG
    pick_list_printed            = 'Kn$(6,1)',   20     # Pick List Printed (Y/N)
    cust_taxable_whlsl           = 'Kn$(7,1)',   21     # Customer Taxable Wholesale
    add_back_to_inventory        = 'Kn$(8,1)',   22     # Add Back to Inventory
    hold_release_flag            = 'Kn$(9,1)',   23     # Hold Release Flag
    taxing_auth_id               = 'Kn$(10,2)',  24     # Taxing Authority Code
    ship_to_id                   = 'Kn$(12,4)',  25     # Ship-to Code
    sales_rep_id                 = 'Kn$(16,3)',  26     # Sales Rep Code
    order_source_id              = 'Kn$(19,1)',  27     # Order Source Code
    ppd_collect                  = 'Kn$(20,1)',  28     # Ppd/Collect
    terms_id                     = 'Kn$(21,1)',  29     # Terms Code
    zip_id                       = 'Kn$(22,9)',  30     # ZIP CODE
    wrhse_id                     = 'Kn$(31,4)',  31     # Warehouse Code
    qty_exceeded                 = 'Kn$(35,1)',  32     # QTY EXCEEDED
    pricing_status               = 'Kn$(36,1)',  33     # PRICING STATUS
    entry_type                   = 'Kn$(37,1)',  34     # Entry Type
    operator_id                  = 'Kn$(38,3)',  35     # Operator ID
    route_id                     = 'Kn$(41,3)',  36     # Route Code
    stop_id                      = 'Kn$(44,3)',  37     # Stop Code
    territory_id                 = 'Kn$(47,3)',  38     # Territory Code
    velocity_report              = 'Kn$(50,1)',  39     # Velocity Report (Y/N)
    pick_priority                = 'Kn$(51,1)',  40     # Pick Priority (1-9)
    cust_prc_label_format        = 'Kn$(52,1)',  41     # Cust Price Label Format
    released_to_pick             = 'Kn$(53,1)',  42     # Released to Pick (Y/N/H) ?
    pick_tags_printed            = 'Kn$(54,1)',  43     # Pick Tags Printed (Y/N/P)
    allocation_done              = 'Kn$(55,1)',  44     # Allocation Done (Y/H/P)
    prc_tags_printed             = 'Kn$(56,1)',  45     # Price Tags Printed (Y/N/H)
    prc_list_srp_list            = 'Kn$(57,2)',  46     # Price List & SRP List
    freight_zone_for_pricing     = 'Kn$(59,1)',  47     # Freight Zone for Pricing (0-9)
    special_cust                 = 'Kn$(60,1)',  48     # Special Cust(CPP) Y/N
    editted                      = 'Kn$(61,1)',  49     # Editted (Y/N)
    linked                       = 'Kn$(62,1)',  50     # Linked (Y/N)
    dm_cm_reason_id              = 'Kn$(63,2)',  51     # DM/CM Reason Code
    ok_to_combine_w_other_orders = 'Kn$(65,1)',  52     # OK to combine w/other orders
    below_min_order              = 'Kn$(66,1)',  53     # Below Min Order (Y=Yes,sp=No)
    promos_elligible             = 'Kn$(67,1)',  54     # Promos elligible(sp=yes,N=No)
    update_s_a                   = 'Kn$(70,1)',  56     # Update S/A?
    ordered_by                   = 'Kn$(71,2)',  57     # Ordered By
    operator_void                = 'Kn$(73,3)',  58     # Operator - Void
    carrier_id                   = 'Kn$(76,2)',  59     # Carrier Code
    bol_no                       = 'Kn$(81,6)',  61     # BOL Number
    cust_po_no                   = 'Ln$',        63     # Customer P.O. No.
    order_date                   = 'Mn$(1,6)',   64     # Order Date
    ship_date                    = 'Mn$(7,6)',   65     # Ship Date
    inv_date                     = 'Mn$(13,6)',  66     # Invoice Date
    date_confirmed               = 'Mn$(19,6)',  67     # Date Confirmed
    date_wanted                  = 'Mn$(25,6)',  68     # Date Wanted
    ord_prt_msg                  = 'Mn$(31,2)',  69     # ORD PRT MSG
    inv_prt_msg                  = 'Mn$(33,2)',  70     # INV PRT MSG
    pricing_as_of_date           = 'Mn$(35,6)',  71     # Pricing 'as of' Date
    cust_prc_label_titles        = 'Nn$',        72     # Cust Price Label Titles
    delivery_instructions        = 'On$',        73     # Delivery Instructions
    phone_no                     = 'Pn$',        74     # Phone Number
    terms_desc                   = 'Qn$',        75     # Terms Description
    off_inv_disc                 = 'Rn$',        76     # Off Invoice Disc %
    no_of_lines                  = 'T(0)',       77     # Number of Lines
    tax_pct                      = 'T(1)',       78     # Tax Pct
    total_gross                  = 'T(2)',       79     # Total Gross
    total_disc                   = 'T(3)',       80     # Total Discount
    total_tax                    = 'T(4)',       81     # Total Tax
    total_misc_chgs              = 'T(5)',       82     # Total Misc Chgs
    taxable_amt                  = 'T(6)',       83     # Taxable Amt
    net_order_amt                = 'T(7)',       84     # Net Order Amt
    total_net_lbs                = 'T(8)',       85     # Total Net Lbs
    svc_chg_amt                  = 'T(9)',       86     # Svc Chg Amt
    total_cst                    = 'T(10)',      87     # Total Cost
    total_gross_lbs              = 'T(11)',      88     # Total Gross Lbs
    total_cases                  = 'T(12)',      89     # Total Cases
    total_eaches                 = 'T(13)',      90     # Total Eaches
    spoilage_allwnc              = 'T(14)',      91     # Spoilage Allowance
    fuel_surcharge               = 'T(15)',      92     # Fuel Surcharge
    categories                   = 'Tn$',        93     # CATEGORIES
    total_cube                   = 'Un$',        94     # Total Cube
    inv_no                       = 'Vn$',        95     # Invoice Number
    eos_disc                     = 'Wn$',        96     # E.O.S. Discount %
    eoe_transmission_no          = 'Xn$(1,6)',   97     # EOE Transmission No
    eoe_confirmation_no          = 'Xn$(7,6)',   98     # EOE Confirmation No
    date_transmitted             = 'Xn$(13,6)',  99     # Date Transmitted
    time_transmitted             = 'Xn$(19,4)', 100     # Time Transmitted
    no_of_prc_labels_princed     = 'Yn$(1,6)',  101     # No of Price Labels Princed
    charge_for_prc_labels        = 'Yn$(7,8)',  102     # Charge for price labels
    inv_svc_chg                  = 'Zn$',       103     # Invoice Svc Chg %


class F37(FISenum):
    """
    RDERD - OPEN ORDER DETAIL FILE MAINT. & INQUIRY
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id                    = 'An$(1,2)',     0     # Company Code
    order_no                      = 'An$(3,6)',     1     # Order Number
    release_no                    = 'An$(9,2)',     2     # Release NO.
    key_type                      = 'An$(11,1)',    3     # KEY TYPE = '1'
    line_no                       = 'An$(12,3)',    4     # Line No.
    forward_ptr                   = 'An',           5     # Forward Ptr
    backward_ptr                  = 'Bn',           6     # Backward Ptr
    sales_unit                    = 'Bn$(1,2)',     7     # Sales Unit
    pricing_unit                  = 'Bn$(3,2)',     8     # Pricing Unit
    whlsl_taxable                 = 'Bn$(5,1)',     9     # Wholesale Taxable (Y/N)
    sales_cat                     = 'Bn$(6,2)',    10     # Sales Category
    retail_prc_list_id            = 'Bn$(8,1)',    11     # Retail Price List Code
    whlsl_prc_list_id             = 'Bn$(9,1)',    12     # Wholesale Price List Code
    special_prc                   = 'Bn$(10,1)',   13     # Special Price? (Y/N)
    line_item_terms_id            = 'Bn$(11,1)',   14     # Line Item Terms Code
    alctd                         = 'Bn$(12,1)',   15     # Allocated (Y/N)
    split_case_id                 = 'Bn$(13,1)',   16     # Split Case Code
    sales_cd                      = 'Bn$(14,1)',   17     # SALES CD
    reason_code_prc_override      = 'Bn$(15,2)',   18     # Reason Code - Price Override
    adds_to_total_wt              = 'Bn$(17,1)',   19     # ADDS TO TOTAL WT
    entry_type                    = 'Bn$(18,1)',   20     # Entry Type (I/A/M)
    contract                      = 'Bn$(19,1)',   21     # CONTRACT?
    catch_weight                  = 'Bn$(20,1)',   22     # CATCH WEIGHT?
    wrhse_id                      = 'Bn$(21,4)',   23     # Warehouse Code
    pick_except_reason            = 'Bn$(25,2)',   24     # Pick Except Reason
    alloc_except_reason           = 'Bn$(27,1)',   25     # Alloc Except Reason
    box_case                      = 'Bn$(28,1)',   26     # BOX/CASE (B/C/SP)
    freight_class                 = 'Bn$(29,1)',   27     # FREIGHT CLASS
    item_type                     = 'Bn$(30,1)',   28     # Item Type
    whse_cat                      = 'Bn$(31,1)',   29     # WHSE Category
    gl_cat                        = 'Bn$(32,1)',   30     # G/L Category
    inventory_units               = 'Bn$(33,2)',   31     # Inventory Units
    initials_for_pick_exceptions  = 'Bn$(35,3)',   32     # Initials for pick exceptions
    retail_taxable                = 'Bn$(38,1)',   33     # Retail Taxable (Y/N) ?
    qty_exceeded                  = 'Bn$(39,1)',   34     # Quantity Exceeded (Y/sp) ?
    invty_availability_id         = 'Bn$(40,1)',   35     # Invty Availability Code
    ca_rdmtn_id                   = 'Bn$(41,2)',   36     # CA Redemption Code
    reason_code_cr_request        = 'Bn$(42,2)',   37     # Reason Code - Credit Request
    inv_ref_cr_request            = 'Bn$(44,8)',   38     # Invoice Ref - Credit Request
    commissionable                = 'Bn$(52,1)',   39     # Commissionable (Y/N)
    update_sa                     = 'Bn$(53,1)',   40     # Update S/A (Y or sp=yes,N=no)
    retail_prc_overrive           = 'Bn$(54,1)',   41     # Retail Price Overrive(V=yes)
    cred_req_inv_date             = 'Bn$(55,6)',   42     # Cred Req Invoice Date
    cred_req_override             = 'Bn$(61,1)',   43     # Cred Req Override(Y/sp)
    cred_req_disposition_id       = 'Bn$(62,2)',   44     # Cred Req Disposition Code
    organic                       = 'Bn$(67,1)',   46     # Organic? (Y/N)
    desc                          = 'Cn$',         48     # Description
    item_key                      = 'Dn$',         49     # Item Key
    item_id                       = 'En$',         50     # Item Code
    upc_id                        = 'Fn$',         51     # UPC Code
    ord_prt_msg                   = 'Gn$(1,2)',    52     # ORD PRT MSG
    inv_prt_msg                   = 'Gn$(3,2)',    53     # INV PRT MSG
    gl_acct                       = 'Hn$',         54     # G/L ACCT #
    lot_no                        = 'In$',         55     # LOT NUMBER
    location_ids                  = 'Jn$',         56     # Location Codes
    contract_no                   = 'Kn$',         57     # Contract Number
    original_alloc_qty            = 'Ln$',         58     # Original Alloc Quantity
    retail_sub_pack               = 'On$',         61     # Retail Sub-Pack
    pack                          = 'Pn$',         62     # PACK
    net_unit_weight               = 'Qn$',         63     # NET UNIT WEIGHT
    qty_ordered                   = 'S(0)',        65     # Qty Ordered
    qty_shipped                   = 'S(1)',        66     # Qty Shipped
    pa_per_unit                   = 'S(2)',        67     # P/A Per Unit
    qty_invoiced                  = 'S(3)',        68     # QUANTITY INVOICED
    catch_wgt_or_unit_conv_factor = 'S(4)',        69     # CATCH WGT OR UNIT CONV FACTOR
    unit_prc                      = 'S(5)',        70     # Unit Price
    gross_unit_wgt                = 'S(6)',        71     # GROSS UNIT WGT
    extension                     = 'S(7)',        72     # Extension
    disc                          = 'S(8)',        73     # DISCOUNT %
    tax                           = 'S(9)',        74     # TAX %
    unit_cst                      = 'S(10)',       75     # Unit Cost
    qty_committed_updated         = 'S(11)',       76     # Qty Committed Updated
    qty_on_hand_updated           = 'S(12)',       77     # Qty on Hand Updated
    sugggested_retail_prc         = 'S(13)',       78     # Sugggested Retail Price
    total_pa                      = 'S(14)',       79     # Total P/A %
    qty_alctd                     = 'S(15)',       80     # Quantity Allocated
    bill_back_pct                 = 'Tn$',         81     # Bill Back Pct
    pa_percents                   = 'Un$',         82     # P/A Percents
    inv_pa_desc                   = 'Vn$',         83     # Invoice P/A Desc
    unit_cube                     = 'Wn$',         84     # Unit Cube
    link_to_header                = 'Yn$',         86     # Link to Header


class F47(FISenum):
    """
    CNVZZ - CBS SALESMAN MASTER FILE
    """
    #
    key_type                  = 'An$(1,1)',    0     # KEY TYPE = 'Z'
    salesperson_id            = 'An$(2,3)',    1     # SALESPERSON CODE
    salesperson_name          = 'Bn$',         2     # SALESPERSON NAME
    company_id                = 'Fn$(1,2)',    9     # COMPANY CODE
    phone_no                  = 'Fn$(3,10)',  10     # PHONE NUMBER
    salesinq_access           = 'Hn$',        13     # SalesInq Access


class F65(FISenum):
    """
    VNMS - VENDOR MASTER FILE MAINT & INQUIRY
    """
    company_id               = 'An$(1,2)',     0     # Company Code
    code                     = 'An$(3,6)',     1     # Vendor Number
    name                     = 'Bn$',          2     # Vendor Name
    addr1                    = 'Cn$',          3     # Address Line 1
    addr2                    = 'Dn$',          4     # Address Line 2
    addr3                    = 'En$',          5     # Address Line 3
    tele                     = 'Gn$',          7     # Telephone Number
    org_cert                 = 'In$(5,1)',    18     # Organic Cert? (Y/N)
    fax                      = 'In$(29,10)',  24     # Fax Number
    contact                  = 'In$(39,15)',  25     # Contact Name
    org_cert_file            = 'In$(54,1)',   26     # Organic Cert on File?
    cert_exp                 = 'In$(55,6)',   27     # Cert Exp Date
    gl_exp_acct              = 'On$',         35     # Standard G/L Expense Account


class F74(FISenum):
    """
    EMP1 - P/R EMPLOYEE MASTER BASIC RECORD MAINT/INQUIRY
    """
    company_id           = 'An$(1,2)',     0     # COMPANY CODE
    emp_num              = 'An$(3,5)',     1     # EMPLOYEE NO.
    name                 = 'Bn$',          2     # EMPLOYEE NAME
    addr1                = 'Cn$',          3     # ADDRESS 1
    addr2                = 'Dn$',          4     # ADDRESS 2
    addr3                = 'En$',          5     # ADDRESS 3
    ssn                  = 'Fn$',          6     # SOC.SEC.NO.
    tele                 = 'Gn$',          7     # TELEPHONE NO.
    date_hired           = 'In$(1,6)',     9     # DATE HIRED
    date_terminated      = 'In$(7,6)',    10     # DATE TERMINATED
    birth_date           = 'In$(19,6)',   12     # BIRTHDATE
    last_raise           = 'In$(43,6)',   16     # Last Raise
    home_dept            = 'Jn$(1,2)',    18     # HOME DEPARTMENT
    status_flag          = 'Kn$(1,1)',    22     # STATUS FLAG
    pay_type             = 'Kn$(2,1)',    23     # PAY TYPE
    marital_status       = 'Kn$(4,1)',    25     # MARITAL STATUS
    pension_status       = 'Kn$(8,1)',    29     # PENSION STATUS
    gender               = 'Kn$(21,1)',   34     # SEX CODE
    driver_license       = 'Kn$(26,10)',  38     # Driver's Lic #
    emergency_contact    = 'Kn$(36,18)',  39     # Emerg Contact
    emergency_phone      = 'Kn$(54,10)',  40     # Emerg Phone
    exempt_fed           = 'X(0)',        41     # # EXEMPT-FED
    exempt_state         = 'X(1)',        42     # # EXEMPT-STATE
    hourly_rate          = 'R(0)',        44     # HOURLY RATE
    salary_rate          = 'R(1)',        45     # SALARY RATE

class F97(FISenum):
    """
    CNVZaa - Inventory Availability Codes
    """
    key_type            = 'An$(1,2)', 0     #   0: Key Group = "aa"
    company_id          = 'An$(3,2)', 1     #   1: Company Code
    availability_id     = 'An$(5,1)', 2     #   2: Availability Code
    desc                = 'Bn$',      3     #   3: Description
    count_as_lost_sales = 'Cn$(1,1)', 4     #   4: Count as Lost Sales (Y/N)
    lost_sales_category = 'Cn$(2,1)', 5     #   5: Lost Sales Category
    availability        = 'Cn$(3,1)', 6     #   6: Availability(Y/N/D/H)
                                            # (open) Cn$(4,2)
    inv_print_msg       = 'Dn$',      8     #   8: Invoice Print Msg



class F135(FISenum):
    """
    NVTY1 - INVENTORY MASTER (STATUS & DESCRIPTION)
    """
    item_id            = 'An$(1,6)',      0     #   0: Item Code
    company_id         = 'An$(7,2)',      1     #   1: Company Code
    warehouse_no       = 'An$(9,4)',      2     #   2: Warehouse Number
    company            = 'An$(13,6)',     3     #   3: 4 SPACES + COMPANY
    key_type           = 'An$(19,3)',     4     #   4: Key Type = '1**'
    available_key      = 'Bn$(1,1)',      5     #   5: Available?
    sales_category     = 'Bn$(3,2)',      7     #   7: Sales Category
    shelf_life_mos     = 'Bn$(69,2)',    36     #  36: Discount Units (not really)
    trademarked        = 'Bn$(117,2)',   48     #  48: TradeMarkd
    kosher_category    = 'Bn$(119,1)',   49     #  49: Kosher Catg
    catalog_location   = 'Bn$(120,10)',  50     #  50: Catlog Loc
    description        = 'Cn$(1,40)',    51     #  51: Description
    size               = 'Cn$(41,8)',    52     #  52: Size
    upc_no             = 'Dn$(6,12)',    55     #  55: UPC CODE
    primary_location   = 'Dn$(18,6)',    56     #  56: Prim Loc
    supplier_id        = 'Gn$(1,6)',     81     #  81: Supplier
    qty_on_hand        = 'I(6)',         99     #  99: Qty on Hand
    new_retail         = 'I(22)',       115     # 115: New Retail
    new_wholesale      = 'I(23)',       116     # 116: New Whlsle


class F163(FISenum):
    """
    POSM - SUPPLIER MASTER FILE
    """
    company_id       = 'An$(1,2)',     0     # Company Code
    code             = 'An$(3,6)',     1     # SUPPLIER NUMBER
    name             = 'Bn$',          2     # Supplier Name
    addr1            = 'Cn$',          3     # Address 1
    addr2            = 'Dn$',          4     # Address 2
    addr3            = 'En$',          5     # Address 3
    tele             = 'Gn$',          7     # TELEPHONE NO.
    fax              = 'Hn$',          8     # Fax Number
    vendor           = 'In$(10,6)',   22     # VENDOR NUMBER
    org_cert_file    = 'Mn$(1,1)',    30     # Org Cert on File?
    non_gmo          = 'Mn$(2,1)',    31     # Non-GMO Vendor?
    kosher           = 'Mn$(6,1)',    35     # Kosher?
    cert_exp         = 'Nn$(1,6)',    37     # Cert Exp Date
    gmo_exp          = 'Nn$(7,6)',    38     # GMO Exp Date
    kosher_exp       = 'Nn$(36,6)',   42     # Kosher Exp Date


class F219(FISenum):
    """
    POHF - PURCHASE ORDER HEADER FILE
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id          = 'An$(1,2)',    0     # COMPANY CODE
    po_no               = 'An$(3,5)',    1     # P/O NUMBER
    release_no          = 'An$(8,2)',    2     # RELEASE NUMBER
    supplier_no         = 'Bn$',         3     # SUPPLIER NUMBER
    supplier_name       = 'Cn$',         4     # SUPPLIER NAME
    addr_line_1         = 'Dn$',         5     # ADDR LINE 1
    addr_line_2         = 'En$',         6     # ADDR LINE 2
    addr_line_3         = 'Fn$',         7     # ADDR LINE 3
    order_placed_by_for = 'Gn$',         8     # ORDER PLACED BY/FOR
    order_issued_to     = 'Hn$',         9     # ORDER ISSUED TO
    terms               = 'In$',        10     # TERMS
    fob                 = 'Jn$',        11     # F.O.B.
    po_reg_flag         = 'Kn$(1,1)',   12     # P/O REG FLAG
    vouchered           = 'Kn$(2,1)',   13     # Vouchered (Y/N)
                                               # (open) Kn$(3,1)
    print_flag          = 'Kn$(4,1)',   15     # PRINT FLAG
                                               # (open) Kn$(5,1)
    ammended_p_o        = 'Kn$(6,1)',   17     # Ammended P/O?
    confirmed_flag      = 'Kn$(7,1)',   18     # CONFIRMED FLAG
                                               # (open) Kn$(8,1)
    po_recvd_complete   = 'Kn$(9,1)',   20     # P.O. RECVD COMPLETE?
    terms_id            = 'Kn$(10,1)',  21     # TERMS CODE
    taxable             = 'Kn$(11,1)',  22     # TAXABLE?
    carrier_id          = 'Kn$(12,2)',  23     # Carrier Code
    voucher_no          = 'Kn$(14,6)',  24     # Voucher Number
    wrhse               = 'Kn$(20,4)',  25     # WAREHOUSE (I/C)
    wrhse               = 'Kn$(24,4)',  26     # WAREHOUSE (DEL)
    fob_id              = 'Kn$(28,2)',  27     # FOB CODE
    po_type             = 'Kn$(30,2)',  28     # P/O Type
    used                = 'Kn$(32,1)',  29     # Used
    prod_order          = 'Kn$(33,1)',  30     # Production Order?
                                               # (open) Kn$(34,7)
    order_date          = 'On$(1,6)',   32     # ORDER DATE
    eta_date            = 'On$(7,6)',   33     # ETA DATE
    date_wanted         = 'Pn$(1,8)',   34     # DATE WANTED
    date_ammended       = 'Pn$(9,8)',   35     # Date Ammended
    carrier             = 'Qn$',        36     # CARRIER
    last_rec_date       = 'Rn$',        37     # LAST REC DATE
    disc_types          = 'Sn$(1,3)',   38     # Discount Types
    freight_type        = 'Sn$(4,1)',   39     # Freight Type
                                               # (open) An
    total_units         = 'Tn',         41     # TOTAL UNITS
    total_weight        = 'Un',         42     # TOTAL WEIGHT
    total_amt           = 'Vn',         43     # TOTAL AMOUNT
    no_of_lines         = 'Wn',         44     # Number of Lines
    operator_id         = 'Xn$',        45     # Operator Code
    disc_1_rate_amt     = 'Tt(1)',      46     # Disc 1 - Rate/Amt
    disc_2_rate_amt     = 'Tt(2)',      47     # Disc 2 - Rate/Amt
    disc_3_rate_amt     = 'Tt(3)',      48     # Disc 3 - Rate/Amt
    freight_rate_amt    = 'Tt(4)',      49     # Freight Rate/Amt
    no_of_pallets       = 'Tt(5)',      50     # Number of Pallets


class F220(FISenum):
    """
    PODF - PURCHASE ORDER DETAIL FILE
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id           = 'An$(1,2)',     0     # COMPANY CODE
    po_no                = 'An$(3,5)',     1     # P/O NUMBER
    release_no           = 'An$(8,2)',     2     # RELEASE NUMBER
    line_no              = 'An$(10,3)',    3     # LINE NO
    item_code            = 'Bn$',          4     # ITEM CODE (KEY)
    item_desc            = 'Cn$',          5     # ITEM DESCRIPTION
    unit_of_measure      = 'Dn$',          6     # UNIT OF MEASURE
    order_qty            = 'An',           7     # ORDER QTY
    net_unit_cst         = 'Bn',           8     # NET UNIT COST
    qty_received         = 'Cn',           9     # QTY RECEIVED
    qty_on_order         = 'Dn',          10     # Qty on order (I/C units)
    revised_cst          = 'En',          11     # Revised Cost
    lot_nos              = 'En$',         12     # LOT NUMBERS
    bin_nos              = 'Fn$',         13     # BIN NUMBERS
    wrhse_id             = 'Gn$',         14     # WAREHOUSE CODE
    unit_cst_fob         = 'Fn',          15     # Unit Cost - FOB
    freight_cst_per_unit = 'Gn',          16     # Freight Cost Per Unit
    disc_per_unit        = 'Hn',          17     # Discount per unit
    disc_percent         = 'In',          18     # DISCOUNT PERCENT
    whlsl_prc            = 'Jn',          19     # Wholesale Price
    contract_no          = 'Kn$(1,10)',   20     # CONTRACT NUMBER
    freight_units        = 'Kn$(11,2)',   21     # Freight Units
    disc_units           = 'Kn$(13,2)',   22     # Discount Units
    line_item_type       = 'Kn$(15,1)',   23     # LINE ITEM TYPE (I/M)
    prod_order_no        = 'Kn$(16,6)',   24     # Production Order No
    contract_item        = 'Kn$(22,1)',   25     # Contract Item?
    conv_factor          = 'Ln$',         27     # Conv Factor (to P/O units)
    promo_exp_date       = 'Mn$(1,6)',    28     # Promo Exp Date
    promo_eff_date       = 'Mn$(7,6)',    29     # Promo Eff Date


class F341(FISenum):
    """
    CNVZf - PRODUCTION LINE MASTER FILE
    """
    company_id            = 'An$(2,2)',   1     # Company Code
    code                  = 'An$(4,2)',   2     # Production Line Code
    desc                  = 'Bn$',        3     # Description
    short_desc            = 'Cn$',        4     # Short Description

