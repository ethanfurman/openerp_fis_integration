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
    bulk_cust_type             = 'Gn$(38,2)',   47     # Bulk Customer Type
    date_added                 = 'Gn$(31,6)',   48     # Date Customer Added
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


class F34(FISenum):
    """
    CSMSS - CUSTOMER MASTER FILE - ADDTN'L SHIP-TO'S
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id         = 'An$(1,2)',     0     # COMPANY
    code               = 'An$(3,6)',     1     # CUSTOMER NUMBER
    record_type_1      = 'An$(9,1)',     2     # RECORD TYPE = "1"
    ship_to_no         = 'An$(10,4)',    3     # SHIP TO NUMBER
    name               = 'Bn$',          4     # SHIP TO NAME
    addr1              = 'Cn$',          5     # ADDRESS LINE 1
    addr2              = 'Dn$',          6     # ADDRESS LINE 2
    addr3              = 'En$',          7     # ADDRESS LINE 3
    postal             = 'Ln$',          8     # ZIPCODE
                                               # (open) - do not use Fn$(1,5)
    msi_cust           = 'Fn$(6,1)',    10     # MSI customer (Y/N)?
    prc_list_id        = 'Fn$(7,1)',    11     # Price List Code
                                               # (open) Fn$(8,1)
    ord_print_msg      = 'Fn$(9,2)',    13     # ORD PRINT MSG
    inv_print_msg      = 'Fn$(11,2)',   14     # INV PRINT MSG
    oper_message       = 'Fn$(13,2)',   15     # OPER MESSAGE
    contact_frequency  = 'Fn$(15,1)',   16     # CONTACT FREQUENCY
    pick_prior         = 'Fn$(16,1)',   17     # Pick Prior(1-9)
    day_contacted      = 'Fn$(17,1)',   18     # Day Contacted
    last_ord_dt        = 'Fn$(18,6)',   19     # Last Ord Dt
    last_inv_dt        = 'Fn$(24,6)',   20     # Last Inv Dt
    service_days       = 'Fn$(30,5)',   21     # Service Days
    holiday_gifts      = 'Fn$(35,1)',   22     # # Holiday Gifts
    last_ord_no        = 'Fn$(36,6)',   23     # Last Ord No
    last_inv_no        = 'Fn$(42,6)',   24     # Last Inv No
    service_rep        = 'Fn$(48,3)',   25     # Service Rep
    wrhse              = 'Fn$(51,4)',   26     # WAREHOUSE
    salesrep_id        = 'Fn$(55,3)',   27     # Salesrep Code
    route_id           = 'Fn$(58,3)',   28     # Route code
    stop_no            = 'Fn$(61,3)',   29     # Stop Number
    tax_auth           = 'Fn$(64,2)',   30     # TAX AUTH
    territory_id       = 'Fn$(66,3)',   31     # Territory Code
    source_id          = 'Fn$(68,2)',   32     # SOURCE CODE
    velocity_rpt       = 'Fn$(71,1)',   33     # Velocity Rpt(Y/N)
    catalog_cat        = 'Fn$(72,1)',   34     # Catalog Category
    extra_labels       = 'Fn$(73,1)',   35     # # Extra Labels
    terms_id           = 'Fn$(74,1)',   36     # Terms Code
    build_up_items     = 'Fn$(75,1)',   37     # BUILD-UP ITEMS?
    delivery_days      = 'Fn$(76,3)',   38     # DELIVERY DAYS
    tele               = 'Fn$(79,10)',  39     # Telephone No
    key_acct_id        = 'Fn$(89,6)',   40     # Key Account Code
    ppd_collect        = 'Fn$(95,1)',   41     # PPD/Collect (P/C)
    sa_cat             = 'Fn$(96,2)',   42     # S/A Category
    prc_labels         = 'Fn$(98,1)',   43     # Price Labels (Y/N)?
    pa_elg             = 'Fn$(99,1)',   44     # P/A Elg? (sp/N)
    prc_labels_title_1 = 'Fn$(100,6)',  45     # Price Labels Title 1
    prc_labels_title_2 = 'Fn$(106,6)',  46     # Price Labels Title 2
    order_days         = 'Fn$(112,5)',  47     # Order Days
    case_labels        = 'Fn$(117,1)',  48     # Case Labels? (Y/N)
    contract_prices    = 'Fn$(118,1)',  49     # Contract Prices? (Y/N)
    carrier_id         = 'Fn$(119,2)',  50     # Carrier Code
    broker_id          = 'Fn$(121,3)',  51     # Broker Code
    temp_ar            = 'Bn',          52     # TEMP A/R $
    order_frequency    = 'Cn',          53     # ORDER FREQUENCY
    min_order_amt      = 'Dn',          54     # Min Order $ Amt
    weight_last_order  = 'En',          55     # WEIGHT LAST ORDER
    ttl_order_weight   = 'Fn',          56     # TTL ORDER WEIGHT
    total_orders       = 'Gn',          57     # TOTAL # ORDERS
    off_inv_disc       = 'Hn',          58     # Off Inv Disc %
    max_order_amt      = 'In',          59     # Maximum Order Amount
    inv_svc_chg        = 'Jn',          60     # Inv Svc Chg %
    spoilage_allwnc    = 'Kn',          61     # Spoilage Allowance
                                               # (open) Ln
                                               # (open) Mn
                                               # (open) Nn
                                               # (open) On
                                               # (open) Pn
    sales_contact      = 'Qn$',         67     # Sales Contact
    delivery_instr     = 'Gn$',         68     # Delivery Instr.
    fax_no             = 'Rn$(1,10)',   69     # Fax Number
    bulk_cust_type     = 'Rn$(11,2)',   70     # Bulk Cust Type
    route_code_2       = 'Rn$(13,3)',   71     # Route Code 2
    route_code_3       = 'Rn$(16,3)',   72     # Route Code 3
    route_code_4       = 'Rn$(19,3)',   73     # Route Code 4
    route_code_5       = 'Rn$(22,3)',   74     # Route Code 5
    stop_no_2          = 'Rn$(25,3)',   75     # Stop Number 2
    stop_no_3          = 'Rn$(28,3)',   76     # Stop Number 3
    stop_no_4          = 'Rn$(31,3)',   77     # Stop Number 4
    stop_no_5          = 'Rn$(34,3)',   78     # Stop Number 5
    prod_sls_rpt       = 'Rn$(37,1)',   79     # Prod Sls Rpt?


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
    an_index                     = 'Bn',          5     # INDEX
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
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    item_id                 = 'An$(1,6)',      0     # Item Code
    company_id              = 'An$(7,2)',      1     # Company Code
    wrhse_no                = 'An$(9,4)',      2     # Warehouse Number
    company                 = 'An$(13,6)',     3     # 4 SPACES + COMPANY
    key_type                = 'An$(19,3)',     4     # Key Type = '1**'
    available_key           = 'Bn$(1,1)',      5     # Available?
    contract_item           = 'Bn$(2,1)',      6     # Contract Item?
    sales_cat               = 'Bn$(3,2)',      7     # Sales Category
    gl_cat                  = 'Bn$(5,1)',      8     # G/L Category
    wrhse_cat               = 'Bn$(6,1)',      9     # Warehouse Category
    inv_units               = 'Bn$(7,2)',     10     # Inv Units
    pric_units              = 'Bn$(9,2)',     11     # Pric Units
    po_units                = 'Bn$(11,2)',    12     # P/O Units
    rtl_units               = 'Bn$(13,2)',    13     # Rtl Units
    rabbi_flag              = 'Bn$(15,1)',    14     # Rabbi Flag
    msg_cd_oper_inst        = 'Bn$(16,2)',    15     # MESG CD - OPER INST
    msg_cd_ordr_prt         = 'Bn$(18,2)',    16     # MESG CD - ORDR PRT
    msg_cd_po_prt           = 'Bn$(20,2)',    17     # MESG CD - PO PRT
    msg_cd_inv_prt          = 'Bn$(22,2)',    18     # MESG CD - INV PRT
    fresh_froz_dry          = 'Bn$(24,1)',    19     # FRESH/FROZ/DRY
    lot_control             = 'Bn$(25,1)',    20     # Lot Control?
    catch_wgt               = 'Bn$(26,1)',    21     # CATCH WGT?
    substitutes             = 'Bn$(27,1)',    22     # SUBSTITUTES?
    other_pkgg              = 'Bn$(28,1)',    23     # OTHER PACKAGING?
    abc_flag                = 'Bn$(29,1)',    24     # ABC Flag
    whlsl_tax               = 'Bn$(30,1)',    25     # Whlsle Tax?
    catalog_section         = 'Bn$(31,4)',    26     # Catalog Section
    item_flag               = 'Bn$(35,1)',    27     # Item Flag
    supl_item               = 'Bn$(36,12)',   28     # Supl Item
    target_item             = 'Bn$(48,1)',    29     # Target Item(Y/N)
    pct_cst_to_whlse        = 'Bn$(49,6)',    30     # Pct Cost to Whlse
    pct_whlse_to_retail     = 'Bn$(55,6)',    31     # Pct Whlse to Retail
    whlse_rndg_mthd         = 'Bn$(61,1)',    32     # Whlse Rounding Method
    retail_rndg_mthd        = 'Bn$(62,1)',    33     # Retail Rounding Method
    ca_rdmtn_id             = 'Bn$(63,2)',    34     # CA Redemption Code
                                                     # (open) Bn$(65,4)
    shelf_life_mos          = 'Bn$(69,2)',    36     # Discount Units (not really)
    safety_stk              = 'Bn$(71,2)',    37     # Safety Stock (Wks)
    promo_cycle             = 'Bn$(73,2)',    38     # Promo Cycle (MM)
    manf_to_order           = 'Bn$(75,1)',    39     # Manf to Order?
    new_old_item_id         = 'Bn$(76,6)',    40     # New/Old Item Code
    split_case_id           = 'Bn$(82,1)',    41     # Split Case Code
    frt_units               = 'Bn$(83,2)',    42     # Frt Units
    po_un_wgt               = 'Bn$(85,10)',   43     # P/O Un Wgt
    formula_ingr            = 'Bn$(95,10)',   44     # Formula - Ingr
    formula_pkg             = 'Bn$(105,10)',  45     # Formula - Pkg
    non_gmo                 = 'Bn$(115,1)',   46     # Non-GMO?
    key_acct_item           = 'Bn$(116,1)',   47     # Key Acct Item?
    trademarkd              = 'Bn$(117,2)',   48     # TradeMarkd
    kshr_catg               = 'Bn$(119,1)',   49     # Kosher Catg
    catalog_location        = 'Bn$(120,10)',  50     # Catlog Loc
    desc                    = 'Cn$(1,40)',    51     # Description
    size                    = 'Cn$(41,8)',    52     # Size
    retl_subpk              = 'Dn$(1,4)',     53     # Retl Subpk
    po_catg_id              = 'Dn$(5,1)',     54     # P/O Catg Code
    upc_no                  = 'Dn$(6,12)',    55     # UPC CODE
    primary_location        = 'Dn$(18,6)',    56     # Prim Loc
    primary_loc_ea          = 'Dn$(24,6)',    57     # Primary Loc - EA
    upstock_locs_1_8        = 'Dn$(30,48)',   58     # Upstock Locs 1-8 (6 chars ea)
    gl_acct_sales           = 'En$',          59     # G/L Account - Sales
    dt_ava_dis              = 'Fn$(1,6)',     60     # Dt Ava/Dis
    date_last_sale          = 'Fn$(7,6)',     61     # Date Last Sale
    dt_lst_rcp              = 'Fn$(13,6)',    62     # Dt Lst Rcp
    date_added              = 'Fn$(19,6)',    63     # Date Added
    old_fob_eff_date        = 'Fn$(25,6)',    64     # Old FOB Eff  date
    old_fob_exp_date        = 'Fn$(31,6)',    65     # Old FOB Exp Date
    new_fob_eff_date        = 'Fn$(37,6)',    66     # New FOB Eff Date
    new_fob_exp_date        = 'Fn$(43,6)',    67     # New FOB Exp Date
    old_landed_cst_eff_date = 'Fn$(49,6)',    68     # Old Landed Cost Eff Date
    old_landed_cst_exp_date = 'Fn$(55,6)',    69     # Old Landed Cost Exp Date
    new_landed_eff_dt       = 'Fn$(61,6)',    70     # New Landed Eff Dt
    new_landed_cst_exp_date = 'Fn$(67,6)',    71     # New Landed Cost Exp Date
    date_last_new_cst       = 'Fn$(73,6)',    72     # Date Last New Cost
    date_last_cst_change    = 'Fn$(79,6)',    73     # Date Last Cost Change
    author_last_cst_change  = 'Fn$(85,6)',    74     # Author Last Cost Change
    dt_lst_cnt              = 'Fn$(91,6)',    75     # Dt Lst Cnt
    hold_date               = 'Fn$(97,6)',    76     # Hold Date
    old_ea_prc              = 'Fn$(105,10)',  77     # Old Each Price
    new_ea_prc              = 'Fn$(113,8)',   78     # New EA Prc
    first_rec_dt            = 'Fn$(121,6)',   79     # 1st Rec Dt
    first_sale_dt           = 'Fn$(127,6)',   80     # 1st Sale Dt
    supplier_id             = 'Gn$(1,6)',     81     # Supplier
    ea_pack_qty             = 'Gn$(7,6)',     82     # Each Pack Quantity
                                                     # (open) Gn$(13,6)
    count_supp              = 'Gn$(19,6)',    84     # Count Supp
    whsl_subpk              = 'Gn$(25,6)',    85     # Whsl Subpk
    un_pallet               = 'Gn$(31,6)',    86     # Un/Pallet
    usage_cd                = 'Gn$(37,1)',    87     # Usage Cd
                                                     # (open) Gn$(38,10)
    phy_count               = 'Gn$(48,7)',    89     # Phy Count
    upstock_qty             = 'Gn$(55,7)',    90     # Upstock Qty
    loc_max                 = 'Gn$(62,6)',    91     # Loc Max
    case_dimn               = 'Gn$(68,10)',   92     # Case Dimn
    net_un_wt               = 'I(0)',         93     # Net Un Wt
    grs_un_wt               = 'I(1)',         94     # Grs Un Wt
    un_ic_un                = 'I(2)',         95     # $ un/IC un
    sls_un_c                = 'I(3)',         96     # # Sls UN /MC
    reorder_pt              = 'I(4)',         97     # Reorder Pt
    max_stk_lvl             = 'I(5)',         98     # MAXIMUM STOCK LEVEL
    qty_on_hand             = 'I(6)',         99     # Qty on Hand
    ic_units_committed      = 'I(7)',        100     # I/C Units Committed
    ic_units_on_order       = 'I(8)',        101     # I/C Units On Order
    avg_cst                 = 'I(9)',        102     # Average Cost
    last_fob_cst            = 'I(10)',       103     # Last FOB Cost
    unit_cube               = 'I(11)',       104     # Unit Cube
    qty_alctd               = 'I(12)',       105     # Quantity Allocated
    mtd_unit_sales          = 'I(13)',       106     # MTD Unit Sales
    ytd_unit_sales          = 'I(14)',       107     # YTD Unit Sales
    bgng_balance            = 'I(15)',       108     # Beginning Balance
    old_retail              = 'I(16)',       109     # Old Retail
    old_whlsl               = 'I(17)',       110     # Old Wholesale
    old_landed_cst          = 'I(18)',       111     # Old Landed Cost
    old_fob_cst             = 'I(19)',       112     # Old FOB Cost
    frght_hndlg             = 'I(20)',       113     # Frght/Hndlg
    disc_allow_amt          = 'I(21)',       114     # Disc/Allow Amt
    new_retail              = 'I(22)',       115     # New Retail
    new_whlsl               = 'I(23)',       116     # New Whlsle
    new_landed              = 'I(24)',       117     # New Landed
    new_fob_cst             = 'I(25)',       118     # New FOB Cost


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


class F192(FISenum):
    """
    CNVZO1 - Transmitter Master File
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    key_type                   = 'An$(1,2)',    0     # Key Type = 'O1'
    company_id                 = 'An$(3,2)',    1     # Company Code
    transmitter_no             = 'An$(5,6)',    2     # Transmitter Number
    transmitter_name           = 'Bn$',         3     # Transmitter  Name
    status                     = 'Cn$',         4     # Status: A=Active, I=Inactive
    date_last_transmission     = 'Cn$(2,6)',    5     # Date Last Transmission
    time_last_transmission     = 'Cn$(8,4)',    6     # Time Last Transmission
    sa_cat                     = 'Cn$(12,2)',   7     # S/A Category
                                                      # (open) Cn$(14,2)
    cust_no                    = 'Dn$(1,6)',    9     # Customer Number
    ship_to_id                 = 'Dn$(7,4)',   10     # Ship To Code
    transmission_format        = 'En$',        11     # Transmission Format
    phone_no                   = 'Fn$',        12     # Phone Number
    contact_person             = 'Gn$',        13     # Contact Person
    sort_key                   = 'Hn',         14     # Sort Key
    email_address1             = 'Jn$',        15     # EMAIL ADDRESS
    email_address2             = 'Kn$',        16     # EMAIL ADDRESS
    email_address3             = 'In$',        17     # EMAIL ADDRESS

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


class F262(FISenum):
    """
    ARCI - Customer Item Code File
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id   = 'An$(1,2)',   0     # Company Code
    cust_no      = 'An$(3,6)',   1     # Customer Number
    our_item_id  = 'An$(9,6)',   2     # Our Item Code
    cust_item_id = 'Bn$',        3     # Customer Item Code


class F320(FISenum):
    """
    IFMS - FORMULA MASTER FILE
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id            = 'An$(1,2)',     0     # Company Code
    formula_id            = 'An$(3,10)',    1     # Formula Code
                                                  # (Open) An$(13,2)
    rev_no                = 'An$(15,3)',    3     # Revision Number
    key_type              = 'An$(18,1)',    4     # Key Group = "0"
    desc                  = 'Bn$',          5     # Description
    coating               = 'Cn$',          6     # Project Number (not really)
    date_issued           = 'Dn$(1,6)',     7     # Date Issued
    date_revised          = 'Dn$(7,6)',     8     # Date Revised
    date_of_last_run      = 'Dn$(13,6)',    9     # Date Of Last Run
    date_put_on_hold      = 'Dn$(19,6)',   10     # Date Put On Hold
    date_written          = 'Dn$(25,6)',   11     # Date Written
    approved_by           = 'Dn$(31,3)',   12     # Approved By
    changed_by            = 'Dn$(34,3)',   13     # Changed By
    change_approved_by    = 'Dn$(37,3)',   14     # Change Approved By
    date_to_retest        = 'Dn$(40,3)',   15     # Date to Retest
    last_sales_ord        = 'En$(1,6)',    16     # Last Sales Ord. #
    last_cust             = 'En$(7,6)',    17     # Last Customer #
    dept_id               = 'En$(13,2)',   18     # Department Code
    color                 = 'En$(15,20)',  19     # Color
    formulated_by         = 'Fn$(1,3)',    20     # Formulated By
    formula_type          = 'Fn$(4,1)',    21     # Formula Type
    ok_to_use             = 'Fn$(5,1)',    22     # Ok To Use?
    hold_reason           = 'Fn$(6,2)',    23     # Hold Reason
    change_reason_id      = 'Fn$(8,2)',    24     # Change Reason Code
    test_w_milk           = 'Fn$(10,1)',   25     # Test W. Milk?
    tablet_type           = 'Fn$(11,3)',   26     # Tablet Type
    normal_prod_line      = 'Fn$(14,2)',   27     # Normal Production Line
    serving_size_units    = 'Fn$(16,2)',   28     # Serving Size Units
    bulk_item_id          = 'Fn$(18,6)',   29     # Bulk Item Code
                                                  # (open) Fn$(24,2)
    prod_units            = 'Fn$(26,2)',   31     # Production Units
    allergens             = 'Fn$(28,8)',   32     # Alpha Sort Key (not really)
    std_batch_sizes       = 'Fn$(36,1)',   33     # Std Batch Sizes? (Y/N)
    tube_size             = 'Fn$(37,2)',   34     # Tube Size
                                                  # (open) Fn$(39,2)
    label_name            = 'Gn$',         36     # Label Name
    reference_no          = 'Hn$',         37     # Reference No.
    previous_reference_no = 'In$',         38     # Previous Reference No.
    comment_line_1        = 'Jn$',         39     # Comment Line 1
    comment_line_2        = 'Kn$',         40     # Comment Line 2
    serving_size          = 'An',          41     # Serving Size
    expected_yield        = 'Bn',          42     # Expected Yield %
    hardness_range_low    = 'Cn',          43     # Hardness Range - Low
    hardness_range_high   = 'Dn',          44     # Hardness Range - High
    mos_shelf_life        = 'En',          45     # Mos Shelf Life
                                                  # (open) Fn
    largest_batch_size    = 'Gn',          47     # Largest Batch Size
    weight_10             = 'Hn',          48     # Weight/10
                                                  # (Open) In
                                                  # (Open) Jn
class F322(FISenum):
    """
    IFDT - FORMULA DETAIL - INGREDIENT DETAIL
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id                = 'An$(1,2)',      0     # Company Code
    formula_id                = 'An$(3,10)',     1     # Formula Code
                                                       # (Open) An$(13,2)
    rev_no                    = 'An$(15,3)',     3     # Revision Number
    key_type                  = 'An$(18,1)',     4     # Key Group = "0"
    line_no                   = 'An$(19,3)',     5     # Line Number
    ingr_code_batch_1         = 'Bn$(1,8)',      6     # Ingredient Code - Batch 1
    ingr_code_batch_2         = 'Bn$(9,8)',      7     # Ingredient Code - Batch 2
    ingr_code_batch_3         = 'Bn$(17,8)',     8     # Ingredient Code - Batch 3
    ingr_code_batch_temp      = 'Bn$(25,8)',     9     # Ingredient Code - Batch Temp
    item_type_batch_1         = 'Cn$(1,1)',     10     # Item Type - Batch 1
    item_type_batch_2         = 'Cn$(2,1)',     11     # Item Type - Batch 2
    item_type_batch_3         = 'Cn$(3,1)',     12     # Item Type - Batch 3
    item_type_batch_temp      = 'Cn$(4,1)',     13     # Item Type - Batch Temp
    units_batch_1             = 'Dn$(1,2)',     14     # Units - Batch 1
    units_batch_2             = 'Dn$(3,2)',     15     # Units - Batch 2
    units_batch_3             = 'Dn$(5,2)',     16     # Units - Batch 3
    units_batch_temp          = 'Dn$(7,2)',     17     # Units - Batch Temp
                                                       # (open) En$
    desc_batch_1              = 'Fn$(1,48)',    19     # Desc - Batch 1
    desc_batch_2              = 'Fn$(49,48)',   20     # Desc - Batch 2
    desc_batch_3              = 'Fn$(97,40)',   21     # Desc - Batch 3
    desc_batch_temp           = 'Fn$(121,40)',  22     # Desc - Batch Temp
    lbl_claim_batch_1         = 'Gn$(1,8)',     23     # Lbl Claim - Batch 1
    lbl_claim_batch_2         = 'Gn$(9,8)',     24     # Lbl Claim - Batch 2
    lbl_claim_batch_3         = 'Gn$(17,8)',    25     # Lbl Claim - Batch 3
    lbl_claim_batch_temp      = 'Gn$(25,8)',    26     # Lbl Claim - Batch Temp
    pct_over_batch_1          = 'Hn$(1,2)',     27     # Pct Over - Batch 1
    pct_over_batch_2          = 'Hn$(3,2)',     28     # Pct Over - Batch 2
    pct_over_batch_3          = 'Hn$(5,2)',     29     # Pct Over - Batch 3
    pct_over_batch_temp       = 'Hn$(7,2)',     30     # Pct Over - Batch Temp
    pct_in_formula_batch_1    = 'A(1)',         31     # Pct In Formula - Batch 1
    pct_in_formula_batch_2    = 'A(2)',         32     # Pct In Formula - Batch 2
    pct_in_formula_batch_3    = 'A(3)',         33     # Pct In Formula - Batch 3
    pct_in_formula_batch_temp = 'A(4)',         34     # Pct In Formula - Batch Temp
    qty_batch_1               = 'B(1)',         35     # Qty - Batch 1
    qty_batch_2               = 'B(2)',         36     # Qty - Batch 2
    qty_batch_3               = 'B(3)',         37     # Qty - Batch 3
    qty_batch_temp            = 'B(4)',         38     # Qty - Batch Temp
                                                       # (open) C(1)
                                                       # (open) C(2)
                                                       # (open) C(3)
                                                       # (open) C(4)


class F323(FISenum):
    """
    IFDT1 - FORMULA DETAIL - PRODUCTION INFO
    """
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id     = 'An$(1,2)',   0    # Company Code
    formula_id     = 'An$(3,10)',  1    # Formula Code
    rev_no         = 'An$(15,3)',  3    # Revision Number
    key_type       = 'An$(18,1)',  4    # Key Group = "1"
    batch_id       = 'An$(19,2)',  5    # Batch Id
    desc           = 'Bn$',        6    # Description
    comments       = 'Cn$',        7    # Comments
    gross_weight   = 'An',        13    # Gross Weight (Lbs)
    yield_in_units = 'Bn',        14    # Yield In Units
    yield_pct      = 'Cn',        15    # Yield %
    labor_hours    = 'Dn',        16    # Labor Hours

class F328(FISenum):
    """
    IFPP0 - SALES ORDER PRODUCTION PENDING - HEADER
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id           = 'An$(1,2)',      0     # Company Code
    order_no             = 'An$(3,6)',      1     # Order Number
    release_no           = 'An$(9,2)',      2     # Release No
    seq_no               = 'An$(11,3)',     3     # Sequence No
    record_type_0000     = 'An$(14,4)',     4     # Record Type = '0000'
    batch_id_a           = 'Bn$(1,1)',      5     # Batch Id - A
    formula_type         = 'Bn$(2,1)',      6     # Formula Type (P/L/T/X/V/K)
    prod_order_printed   = 'Bn$(3,1)',      7     # Prod Order Printed? (Y/N)
    pkgg_order_printed   = 'Bn$(4,1)',      8     # Packaging Order Printed (Y/N)
    lot_nos_assigned     = 'Bn$(5,1)',      9     # Lot Numbers Assigned (Y/N)
    batching_auto_manual = 'Bn$(6,1)',     10     # Batching Auto/Manual (A/M)
    recommit_necessary   = 'Bn$(7,1)',     11     # Recommit Necessary (Y/N)
    produced             = 'Bn$(8,1)',     12     # Produced (Y/N/P/X)
    type                 = 'Bn$(9,1)',     13     # Type (S/M/X)
    spec_prod_changes    = 'Bn$(10,1)',    14     # Spec Prod Changes (Y/N)
                                                  # (open) Bn$(11,2)
    order_confirmed      = 'Bn$(13,1)',    16     # Order Confirmed?
                                                  # (open) Bn$(14,7)
    prod_no              = 'Cn$(1,8)',     18     # Product Number
    label                = 'Cn$(9,6)',     19     # Label
    pallets              = 'Cn$(15,4)',    20     # Pallets
    formula_id           = 'Cn$(19,10)',   21     # Formula Code
    formula_rev          = 'Cn$(29,3)',    22     # Formula Revision
    prod_color           = 'Cn$(32,18)',   23     # Product Color
    tablet_type          = 'Cn$(50,3)',    24     # Tablet Type
    hardness_range       = 'Cn$(53,8)',    25     # Hardness Range
    thickness            = 'Cn$(61,13)',   26     # Thickness
    label_claim          = 'Cn$(74,5)',    27     # Label Claim
    current_status       = 'Cn$(79,2)',    28     # Current Status
    requested_date       = 'Cn$(81,6)',    29     # Requested Date
    addl_so_refs         = 'Cn$(87,24)',   30     # Addl S/O Refs
    label_name           = 'Cn$(111,40)',  31     # Label Name
    serving_size_units   = 'Cn$(151,2)',   32     # Serving Size Units
    bult_item_units      = 'Cn$(153,2)',   33     # Bult Item Units
    fingoods_units       = 'Cn$(155,2)',   34     # Fin.Goods Units
    dept_id              = 'Cn$(157,2)',   35     # Department Code
    prod_line            = 'Cn$(159,2)',   36     # Production Line
                                                  # (open) Cn$(161,2)
    instruction_line_1   = 'Dn$',          38     # Instruction Line 1
    instruction_line_2   = 'En$',          39     # Instruction Line 2
    prod_scheduled_date  = 'Fn$(1,6)',     40     # Production Scheduled Date
    date_lot_no_assgnd   = 'Fn$(7,6)',     41     # Date Lot No Assgnd
    prod_date            = 'Fn$(13,6)',    42     # Production Date
    scheduled_date       = 'Fn$(19,6)',    43     # Scheduled Date
    warning_codes        = 'Gn$',          44     # Warning Codes
    item_key             = 'Hn$',          45     # Item Key (Inventory)
    lot_no_range_1       = 'In$',          46     # Lot No Range 1
    lot_no_range_2       = 'Jn$',          47     # Lot No Range 2
    lot_no_range_3       = 'Kn$',          48     # Lot No Range 3
    lot_nos_produced     = 'Ln$',          49     # Lot Nos Produced
    units_ordered        = 'An',           50     # Units Ordered
    prod_qty             = 'Bn',           51     # Production Qty
    no_of_batches_a      = 'Cn',           52     # Number Of Batches - A
    no_of_batches_b      = 'Dn',           53     # Number Of Batches - B
    batch_weight_a       = 'En',           54     # Batch Weight - A
    batch_weight_b       = 'Fn',           55     # Batch Weight - B
    batch_size_a         = 'Gn',           56     # Batch Size (Units) - A
    batch_size_b         = 'Hn',           57     # Batch Size (Units) - B
    weight_10            = 'In',           58     # Weight/10
                                                  # (open) Jn
    fg_qty_to_use        = 'Kn',           60     # F.G. Qty To Use
    units_produced       = 'Ln',           61     # Units Produced
    no_of_lots_produced  = 'Mn',           62     # No Of Lots Produced
    qty_on_order         = 'Nn',           63     # Qty On Order


class F329(FISenum):
    """
    IFPP1 - SALES ORDER PRODUCTION PENDING - DETAIL
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    company_id             = 'An$(1,2)',    0     # Company Code
    order_no               = 'An$(3,6)',    1     # Order Number
    release_no             = 'An$(9,2)',    2     # Release No
    sales_order_seq        = 'An$(11,3)',   3     # Sales Order Seq
    key_type               = 'An$(14,1)',   4     # Key Type = "1"
    formula_line_no        = 'An$(15,3)',   5     # Formula Line No
    ingr_code_batch_1      = 'Bn$(1,8)',    6     # Ingredient Code - Batch 1
    ingr_code_batch_2      = 'Bn$(9,8)',    7     # Ingredient Code - Batch 2
    item_type_batch_1      = 'Cn$(1,1)',    8     # Item Type - Batch 1
    item_type_batch_2      = 'Cn$(2,1)',    9     # Item Type - Batch 2
                                                  # (open) Cn$(3,2)
    units_batch_1          = 'Dn$(1,2)',   11     # Units - Batch 1
    units_batch_2          = 'Dn$(3,2)',   12     # Units - Batch 2
                                                  # (open) Dn$(5,2)
                                                  # (open) Dn$(7,2)
    desc                   = 'En$',        15     # Description (Item Or Msg)
    label_claim            = 'Fn$',        16     # Label Claim
    over                   = 'Gn$',        17     # % Over
                                                  # (open) Hn$
    pct_in_formula_batch_1 = 'A(1)',       19     # Pct In Formula - Batch 1
    pct_in_formula_batch_2 = 'A(2)',       20     # Pct In Formula - Batch 2
                                                  # (open) A(3)
                                                  # (open) A(4)
    qty_batch_1            = 'B(1)',       23     # Quantity - Batch 1
    qty_batch_2            = 'B(2)',       24     # Quantity - Batch 2
    qty_committed_batch_1  = 'B(3)',       25     # Qty Committed - Batch 1
    qty_committed_batch_2  = 'B(4)',       26     # Qty Committed - Batch 2
                                                  # (open) C(1)
                                                  # (open) C(2)
    wip_qty_batch_1        = 'C(3)',       29     # WIP Qty - Batch 1
                                                  # (open) C(4)

class F341(FISenum):
    """
    CNVZf - PRODUCTION LINE MASTER FILE
    """
    #
    _init_ = "value sequence"
    _order_ = lambda m: m.sequence
    #
    key_type                      = 'An$(1,1)',   0     # KEY GROUP = "f"
    company_id                    = 'An$(2,2)',   1     # Company Code
    prod_line_code                = 'An$(4,2)',   2     # Production Line Code
    desc                          = 'Bn$',        3     # Description
    short_desc                    = 'Cn$',        4     # Short Description
    cst_per_hour                  = 'An',         5     # Cost per Hour
    standard_performance_per_hour = 'Bn',         6     # Standard Performance per Hour
    normal_hours_per_day          = 'Gn',         7     # Normal Hours per Day
    vendor_no                     = 'Hn$',        8     # Vendor Number
                                                        # (open) In$

