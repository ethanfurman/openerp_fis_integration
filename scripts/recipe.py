from enum import Enum
from VSS.BBxXlate.fisData import fisData
from openerplib import AttrDict

def get_item_ingredients(item, rev='000', food_only=False):
    get_fis_data()
    #ensure item is 10 chars long
    item_ingredient, rev = '%-10s' % item, '%-3s' % rev
    item = item[:6]
    fulllist = [(rec[F322.ingr_id_batch_1], key, rec) for key, rec in IFDT.get_subset((item_ingredient, rev))]
    foodlist = []
    try:
        depcode = IFMS[item_ingredient][F320.dept_id]
    except:
        depcode = ""
    if NVTY.has_key(item) and depcode != "98":  # check if depcode 98 and ignore the BOM if so
        for ingredient, key, rec in fulllist:
            ingredient = ingredient[:6]
            if ingredient in ignored_ingredients:
                continue
            if NVTY.has_key(ingredient):
                if item == ingredient:
                    foodlist.append((ingredient, key, rec, 1)) # the 1 means don't eplode (isself=1)
                    ingredient = "x" + ingredient
                elif not food_only or NVTY[ingredient][F135.net_un_wt] > 0:
                    # net_un_wt > 0 means it's an item that contributes wght (food ingredient?)
                    foodlist.append((ingredient, key, rec, 0))
    return foodlist

def get_order_ingredients(order, food_only=False):
    get_fis_data()
    # get the order record from 328
    order, order_no = IFPP0[order], order
    item = order[F328.prod_no].strip()
    # then the ingredients
    fulllist = [(rec[F329.ingr_id_batch_1], key, rec) for key, rec in IFPP1.get_subset(order_no)]
    # import pdb; pdb.set_trace()
    foodlist = []
    # for i in sorted(ingredients, key=lambda r: r[F329.formula_line_no]):
    for ingredient, key, rec in fulllist:
        ingredient = ingredient[:6]
        if ingredient in ignored_ingredients:
            continue
        if NVTY.has_key(ingredient):
            if item == ingredient:
                foodlist.append((ingredient, key, rec, 1)) # the 1 means don't eplode (isself=1)
                ingredient = "x" + ingredient # XXX this line should be above the previous one, or removed
            elif not food_only or NVTY[ingredient][F135.net_un_wt] > 0:
                # net_un_wt > 0 means it's an item that contributes wght (food ingredient?)
                foodlist.append((ingredient, key, rec, 0))
    return item, foodlist


def get_fis_data():
    global IFDT, NVTY, IFMS, IFDT1, IFDT1_REV, IFPP0, IFPP1
    IFDT = fisData('IFDT', subset="10%s  %s")               # 322
    NVTY = fisData('NVTY1', keymatch="%s101000    101**")   # 135
    IFMS = fisData('IFMS', keymatch="10%s      0000")       # 320
    IFDT1 = fisData('IFDT1', keymatch="10%s      000101")   # 323
    IFDT1_REV = fisData('IFDT1', keymatch="10%s  %s101")    # 323
    IFPP0 = fisData('IFPP0', keymatch="10%s000010000")      # 328
    IFPP1 = fisData('IFPP1', subset="10%s")                 # 329

def title(txt):
    txt = txt.strip().title()
    return txt.replace("Sunridge","SunRidge")

def item_detail(oid, item, qty, as_ingredient, inventory, item_refs):
    if item.startswith('x'):
        item_code = item[1:]
    else:
        item_code = item
    nvty = NVTY[item_code]
    yield_qty = 0.0
    desc="NVTY Record not found"
    um, umdesc = "xx", "xx"
    if nvty:
        desc = title(nvty[F135.desc])
        um, umdesc = nvty[F135.inv_units], nvty[F135.size]
        um = ' '.join(um.split())
        umdesc = ' '.join(umdesc.split())
        inventory[item_code] = AttrDict({
                'on_hand':  nvty[F135.qty_on_hand],
                'committed': nvty[F135.ic_units_committed],
                'on_order': nvty[F135.ic_units_on_order],
                'desc': desc,
                })
    if IFDT1.has_key(item_code):
        yield_qty = IFDT1[item_code]['Bn']
    oid = "%s-%s" % (oid, item)
    field = AttrDict({
        'id'        : oid,
        'desc'      : desc,                         # item description
        'um'        : "<%s %s>" % (umdesc, um),
        'unit_size' : um,
        'unit_wght' : umdesc,
        'qty'       : qty,                          # quantity needed for parent recipe
        'item'      : item_code,                    # item code
        'yield_qty' : yield_qty,                    # yield of sub-recipe
        })
    refs = item_refs.get(item_code)
    if refs is None:
        refs = AttrDict()
    refs[oid] = field
    item_refs[item_code] = refs
    return field

def get_items_with_recipes(print_missing=False):
    get_fis_data()
    recipes = []
    for recipe in IFMS:
        item = recipe[F320.formula_id].strip()
        rev = recipe[F320.rev_id]
        if NVTY.has_key(item):
            recipes.append((item, rev))
        elif print_missing:
            print('skipping recipe', item)
    return recipes

def get_ingredient_data(oid, item, qty=1, exdata=None, food_only=False, inventory=None, item_refs=None, level=None, use_production=False):
    # bom = bill of materials
    if inventory is None:
        inventory = AttrDict()
    if item_refs is None:
        item_refs = AttrDict()
    get_fis_data()
    if use_production:
        item, bom = get_order_ingredients(item)
        F = F329
    else:
        bom = get_item_ingredients(item, food_only=food_only)
        F = F322
    # import pdb; pdb.set_trace()
    datadict = item_detail(oid, item, qty, 0, inventory, item_refs)
    datadict.ingredients = AttrDict()
    for ingredient, ky, ifdt, isself in bom:
        datadict.ingredients["%s-%s" % (ky[-3:], ingredient)] = item_detail(
                oid=ky[-3:],
                item=ingredient,
                qty=ifdt[F.qty_batch_1],
                as_ingredient=True,
                inventory=inventory,
                item_refs=item_refs,
                )
        if not isself and get_item_ingredients(ingredient, food_only=food_only) and level not in (None, 0):
            if level is not None:
                level -= 1
            datadict.ingredients["%s-%s" % (ky[-3:], ingredient)] = get_ingredient_data(
                    oid=ky[-3:],
                    item=ingredient,
                    qty=ifdt[F.qty_batch_1],
                    food_only=food_only,
                    inventory=inventory,
                    item_refs=item_refs,
                    level=level,
                    use_production=use_production,
                    )
    if exdata is None:
        exdata = datadict
    return exdata

def make_on_hand(item, inventory_used=None):
    if inventory_used is None:
        inventory_used = AttrDict()
    recipe = get_ingredient_data(oid="", item=item, food_only=False, inventory=inventory_used)
    qtys = []
    for ingredient in recipe.ingredients.values():
        ingr_levels = inventory_used[ingredient.item]
        available = ingr_levels.on_hand - ingr_levels.committed
        if available < 0:
            return 0
        if ingredient.qty:
            qtys.append(available/ingredient.qty)
    if not qtys:
        return False
    buildable = min(qtys)
    return buildable * recipe.yield_qty


ignored_ingredients = set([
        # nutritional info
        '910000', '910001', '910002', '910003', '910004',
        '910005', '910006', '910007', '910008', 
        # freight charges
        '967001',
        ])

class F323(str, Enum):
    """
    IFDT1 - FORMULA DETAIL - PRODUCTION INFO
    """
    company_id     = 'An$(1,2)'      # Company Code
    formula_id     = 'An$(3,10)'     # Formula Code
                                     # (Open) An$(13,2)
    rev_id         = 'An$(15,3)'     # Revision Number
    key_type       = 'An$(18,1)'     # Key Group = "1"
    batch_id       = 'An$(19,2)'     # Batch Id
    desc           = 'Bn$'           # Description
    comments       = 'Cn$'           # Comments
    gross_weight   = 'An'            # Gross Weight (Lbs)
    yield_in_units = 'Bn'            # Yield In Units
    yield_pct      = 'Cn'            # Yield %
    labor_hours    = 'Dn'            # Labor Hours

class F322(str, Enum):
    """
    IFDT - FORMULA DETAIL - INGREDIENT DETAIL
    """
    company_id                = 'An$(1,2)'        # Company Code
    formula_id                = 'An$(3,10)'       # Formula Code
                                                  # (Open) An$(13,2)
    rev_id                    = 'An$(15,3)'       # Revision Number
    key_type                  = 'An$(18,1)'       # Key Group = "0"
    line_id                   = 'An$(19,3)'       # Line Number
    ingr_id_batch_1           = 'Bn$(1,8)'        # Ingredient Code - Batch 1
    ingr_id_batch_2           = 'Bn$(9,8)'        # Ingredient Code - Batch 2
    ingr_id_batch_3           = 'Bn$(17,8)'       # Ingredient Code - Batch 3
    ingr_id_batch_temp        = 'Bn$(25,8)'       # Ingredient Code - Batch Temp
    item_type_batch_1         = 'Cn$(1,1)'        # Item Type - Batch 1
    item_type_batch_2         = 'Cn$(2,1)'        # Item Type - Batch 2
    item_type_batch_3         = 'Cn$(3,1)'        # Item Type - Batch 3
    item_type_batch_temp      = 'Cn$(4,1)'        # Item Type - Batch Temp
    units_batch_1             = 'Dn$(1,2)'        # Units - Batch 1
    units_batch_2             = 'Dn$(3,2)'        # Units - Batch 2
    units_batch_3             = 'Dn$(5,2)'        # Units - Batch 3
    units_batch_temp          = 'Dn$(7,2)'        # Units - Batch Temp
                                                  # (open) En$
    desc_batch_1              = 'Fn$(1,48)'       # Desc - Batch 1
    desc_batch_2              = 'Fn$(49,48)'      # Desc - Batch 2
    desc_batch_3              = 'Fn$(97,40)'      # Desc - Batch 3
    desc_batch_temp           = 'Fn$(121,40)'     # Desc - Batch Temp
    lbl_claim_batch_1         = 'Gn$(1,8)'        # Lbl Claim - Batch 1
    lbl_claim_batch_2         = 'Gn$(9,8)'        # Lbl Claim - Batch 2
    lbl_claim_batch_3         = 'Gn$(17,8)'       # Lbl Claim - Batch 3
    lbl_claim_batch_temp      = 'Gn$(25,8)'       # Lbl Claim - Batch Temp
    pct_over_batch_1          = 'Hn$(1,2)'        # Pct Over - Batch 1
    pct_over_batch_2          = 'Hn$(3,2)'        # Pct Over - Batch 2
    pct_over_batch_3          = 'Hn$(5,2)'        # Pct Over - Batch 3
    pct_over_batch_temp       = 'Hn$(7,2)'        # Pct Over - Batch Temp
    pct_in_formula_batch_1    = 'A(1)'            # Pct In Formula - Batch 1
    pct_in_formula_batch_2    = 'A(2)'            # Pct In Formula - Batch 2
    pct_in_formula_batch_3    = 'A(3)'            # Pct In Formula - Batch 3
    pct_in_formula_batch_temp = 'A(4)'            # Pct In Formula - Batch Temp
    qty_batch_1               = 'B(1)'            # Qty - Batch 1
    qty_batch_2               = 'B(2)'            # Qty - Batch 2
    qty_batch_3               = 'B(3)'            # Qty - Batch 3
    qty_batch_temp            = 'B(4)'            # Qty - Batch Temp
                                                  # (open) C(1)
                                                  # (open) C(2)
                                                  # (open) C(3)
                                                  # (open) C(4)

class F329(str, Enum):
    """
    IFPP1 - SALES ORDER PRODUCTION PENDING - DETAIL
    """
    company_id             = 'An$(1,2)'      #   0: Company Code
    order_no               = 'An$(3,6)'      #   1: Order Number
    release_no             = 'An$(9,2)'      #   2: Release No
    sales_order_seq        = 'An$(11,3)'     #   3: Sales Order Seq
    key_type               = 'An$(14,1)'     #   4: Key Type = "1"
    formula_line_no        = 'An$(15,3)'     #   5: Formula Line No
    ingr_id_batch_1      = 'Bn$(1,8)'      #   6: Ingredient Code - Batch 1
    ingr_id_batch_2      = 'Bn$(9,8)'      #   7: Ingredient Code - Batch 2
    item_type_batch_1      = 'Cn$(1,1)'      #   8: Item Type - Batch 1
    item_type_batch_2      = 'Cn$(2,1)'      #   9: Item Type - Batch 2
                                             # (open) Cn$(3,2)
    units_batch_1          = 'Dn$(1,2)'      #  11: Units - Batch 1
    units_batch_2          = 'Dn$(3,2)'      #  12: Units - Batch 2
                                             # (open) Dn$(5,2)
                                             # (open) Dn$(7,2)
    desc                   = 'En$'           #  15: Description (Item Or Msg)
    label_claim            = 'Fn$'           #  16: Label Claim
    over                   = 'Gn$'           #  17: % Over
                                             # (open) Hn$
    pct_in_formula_batch_1 = 'A(1)'          #  19: Pct In Formula - Batch 1
    pct_in_formula_batch_2 = 'A(2)'          #  20: Pct In Formula - Batch 2
                                             # (open) A(3)
                                             # (open) A(4)
    qty_batch_1            = 'B(1)'          #  23: Quantity - Batch 1
    qty_batch_2            = 'B(2)'          #  24: Quantity - Batch 2
    qty_committed_batch_1  = 'B(3)'          #  25: Qty Committed - Batch 1
    qty_committed_batch_2  = 'B(4)'          #  26: Qty Committed - Batch 2
                                             # (open) C(1)
                                             # (open) C(2)
    wip_qty_batch_1        = 'C(3)'          #  29: WIP Qty - Batch 1
                                             # (open) C(4)



class F320(str, Enum):
    """
    IFMS - FORMULA MASTER FILE
    """
    company_id            = 'An$(1,2)'      # Company Code
    formula_id            = 'An$(3,10)'     # Formula Code
                                            # (Open) An$(13,2)
    rev_id                = 'An$(15,3)'     # Revision Number
    key_type              = 'An$(18,1)'     # Key Group = "0"
    desc                  = 'Bn$'           # Description
    coating               = 'Cn$'           # Project Number (mis-named)
    date_issued           = 'Dn$(1,6)'      # Date Issued
    date_revised          = 'Dn$(7,6)'      # Date Revised
    date_of_last_run      = 'Dn$(13,6)'     # Date Of Last Run
    date_put_on_hold      = 'Dn$(19,6)'     # Date Put On Hold
    date_written          = 'Dn$(25,6)'     # Date Written
    approved_by           = 'Dn$(31,3)'     # Approved By
    changed_by            = 'Dn$(34,3)'     # Changed By
    change_approved_by    = 'Dn$(37,3)'     # Change Approved By
    date_to_retest        = 'Dn$(40,3)'     # Date to Retest
    last_sales_ord        = 'En$(1,6)'      # Last Sales Ord. #
    last_customer         = 'En$(7,6)'      # Last Customer #
    dept_id               = 'En$(13,2)'     # Department Code
    color                 = 'En$(15,20)'    # Color
    formulated_by         = 'Fn$(1,3)'      # Formulated By
    formula_type          = 'Fn$(4,1)'      # Formula Type
    ok_to_use             = 'Fn$(5,1)'      # Ok To Use?
    hold_reason           = 'Fn$(6,2)'      # Hold Reason
    change_reason_id      = 'Fn$(8,2)'      # Change Reason Code
    test_w_milk           = 'Fn$(10,1)'     # Test W. Milk?
    tablet_type           = 'Fn$(11,3)'     # Tablet Type
    normal_prod_line      = 'Fn$(14,2)'     # Normal Production Line
    serving_size_units    = 'Fn$(16,2)'     # Serving Size Units
    bulk_item_id          = 'Fn$(18,6)'     # Bulk Item Code
                                            # (open) Fn$(24,2)
    prod_units            = 'Fn$(26,2)'     # Production Units
    allergens             = 'Fn$(28,8)'     # Alpha Sort Key (mis-named)
    std_batch_sizes       = 'Fn$(36,1)'     # Std Batch Sizes? (Y/N)
    tube_size             = 'Fn$(37,2)'     # Tube Size
                                            # (open) Fn$(39,2)
    label_name            = 'Gn$'           # Label Name
    reference_no          = 'Hn$'           # Reference No.
    previous_reference_no = 'In$'           # Previous Reference No.
    comment_line_1        = 'Jn$'           # Comment Line 1
    comment_line_2        = 'Kn$'           # Comment Line 2
    serving_size          = 'An'            # Serving Size
    expected_yield        = 'Bn'            # Expected Yield %
    hardness_range_low    = 'Cn'            # Hardness Range - Low
    hardness_range_high   = 'Dn'            # Hardness Range - High
    mos_shelf_life        = 'En'            # Mos Shelf Life
                                            # (open) Fn
    largest_batch_size    = 'Gn'            # Largest Batch Size
    weight_10             = 'Hn'            # Weight/10
                                            # (Open) In
                                            # (Open) Jn


class F135(str, Enum):
    """
    NVTY1 - INVENTORY MASTER (STATUS & DESCRIPTION)
    """
    item_id                  = 'An$(1,6)'         # Item Code
    company_id               = 'An$(7,2)'         # Company Code
    warehouse_id             = 'An$(9,4)'         # Warehouse Number
    company                  = 'An$(13,6)'        # 4 SPACES + COMPANY
    key_type                 = 'An$(19,3)'        # Key Type = '1**'
    available                = 'Bn$(1,1)'         # Available?
    contract_item            = 'Bn$(2,1)'         # Contract Item?
    sales_category           = 'Bn$(3,2)'         # Sales Category
    gl_category              = 'Bn$(5,1)'         # G/L Category
    warehouse_category       = 'Bn$(6,1)'         # Warehouse Category
    inv_units                = 'Bn$(7,2)'         # Inv Units
    pric_units               = 'Bn$(9,2)'         # Pric Units
    po_units                 = 'Bn$(11,2)'        # P/O Units
    rtl_units                = 'Bn$(13,2)'        # Rtl Units
    rabbi_flag               = 'Bn$(15,1)'        # Rabbi Flag
    mesg_cd_oper_inst        = 'Bn$(16,2)'        # MESG CD - OPER INST
    mesg_cd_ordr_prt         = 'Bn$(18,2)'        # MESG CD - ORDR PRT
    mesg_cd_po_prt           = 'Bn$(20,2)'        # MESG CD - PO PRT
    mesg_cd_inv_prt          = 'Bn$(22,2)'        # MESG CD - INV PRT
    fresh_froz_dry           = 'Bn$(24,1)'        # FRESH/FROZ/DRY
    lot_control              = 'Bn$(25,1)'        # Lot Control?
    catch_wgt                = 'Bn$(26,1)'        # CATCH WGT?
    substitutes              = 'Bn$(27,1)'        # SUBSTITUTES?
    other_packaging          = 'Bn$(28,1)'        # OTHER PACKAGING?
    abc_flag                 = 'Bn$(29,1)'        # ABC Flag
    whlsle_tax               = 'Bn$(30,1)'        # Whlsle Tax?
    catalog_section          = 'Bn$(31,4)'        # Catalog Section
    item_flag                = 'Bn$(35,1)'        # Item Flag
    supl_item                = 'Bn$(36,12)'       # Supl Item
    target_item              = 'Bn$(48,1)'        # Target Item(Y/N)
    pct_cost_to_whlse        = 'Bn$(49,6)'        # Pct Cost to Whlse
    pct_whlse_to_retail      = 'Bn$(55,6)'        # Pct Whlse to Retail
    whlse_rounding_method    = 'Bn$(61,1)'        # Whlse Rounding Method
    retail_rounding_method   = 'Bn$(62,1)'        # Retail Rounding Method
    ca_redemption_id         = 'Bn$(63,2)'        # CA Redemption Code
                                                  # (open) Bn$(65,4)
    discount_units           = 'Bn$(69,2)'        # Discount Units
    safety_stock             = 'Bn$(71,2)'        # Safety Stock (Wks)
    promo_cycle              = 'Bn$(73,2)'        # Promo Cycle (MM)
    manf_to_order            = 'Bn$(75,1)'        # Manf to Order?
    new_old_item_id          = 'Bn$(76,6)'        # New/Old Item Code
    split_case_id            = 'Bn$(82,1)'        # Split Case Code
    frt_units                = 'Bn$(83,2)'        # Frt Units
    po_un_wgt                = 'Bn$(85,10)'       # P/O Un Wgt
    formula_ingr             = 'Bn$(95,10)'       # Formula - Ingr
    formula_pkg              = 'Bn$(105,10)'      # Formula - Pkg
    non_gmo                  = 'Bn$(115,1)'       # Non-GMO?
    key_acct_item            = 'Bn$(116,1)'       # Key Acct Item?
    trademarkd               = 'Bn$(117,2)'       # TradeMarkd
    kosher_catg              = 'Bn$(119,1)'       # Kosher Catg
    catlog_loc               = 'Bn$(120,10)'      # Catlog Loc
    desc                     = 'Cn$(1,40)'        # Description
    size                     = 'Cn$(41,8)'        # Size
    retl_subpk               = 'Dn$(1,4)'         # Retl Subpk
    po_catg_id               = 'Dn$(5,1)'         # P/O Catg Code
    upc_id                   = 'Dn$(6,12)'        # UPC CODE
    prim_loc                 = 'Dn$(18,6)'        # Prim Loc
    primary_loc_ea           = 'Dn$(24,6)'        # Primary Loc - EA
    upstock_locs_1_8         = 'Dn$(30,48)'       # Upstock Locs 1-8 (6 chars ea)
    gl_account_sales         = 'En$'              # G/L Account - Sales
    dt_ava_dis               = 'Fn$(1,6)'         # Dt Ava/Dis
    date_last_sale           = 'Fn$(7,6)'         # Date Last Sale
    dt_lst_rcp               = 'Fn$(13,6)'        # Dt Lst Rcp
    date_added               = 'Fn$(19,6)'        # Date Added
    old_fob_eff_date         = 'Fn$(25,6)'        # Old FOB Eff  date
    old_fob_exp_date         = 'Fn$(31,6)'        # Old FOB Exp Date
    new_fob_eff_date         = 'Fn$(37,6)'        # New FOB Eff Date
    new_fob_exp_date         = 'Fn$(43,6)'        # New FOB Exp Date
    old_landed_cost_eff_date = 'Fn$(49,6)'        # Old Landed Cost Eff Date
    old_landed_cost_exp_date = 'Fn$(55,6)'        # Old Landed Cost Exp Date
    new_landed_eff_dt        = 'Fn$(61,6)'        # New Landed Eff Dt
    new_landed_cost_exp_date = 'Fn$(67,6)'        # New Landed Cost Exp Date
    date_last_new_cost       = 'Fn$(73,6)'        # Date Last New Cost
    date_last_cost_change    = 'Fn$(79,6)'        # Date Last Cost Change
    author_last_cost_change  = 'Fn$(85,6)'        # Author Last Cost Change
    dt_lst_cnt               = 'Fn$(91,6)'        # Dt Lst Cnt
    hold_date                = 'Fn$(97,6)'        # Hold Date
    old_each_price           = 'Fn$(105,10)'      # Old Each Price
    new_ea_prc               = 'Fn$(113,8)'       # New EA Prc
    first_rec_dt             = 'Fn$(121,6)'       # 1st Rec Dt
    first_sale_dt            = 'Fn$(127,6)'       # 1st Sale Dt
    supplier                 = 'Gn$(1,6)'         # Supplier
    each_pack_qty            = 'Gn$(7,6)'         # Each Pack Quantity
                                                  # (open) Gn$(13,6)
    count_supp               = 'Gn$(19,6)'        # Count Supp
    whsl_subpk               = 'Gn$(25,6)'        # Whsl Subpk
    un_pallet                = 'Gn$(31,6)'        # Un/Pallet
    usage_cd                 = 'Gn$(37,1)'        # Usage Cd
                                                  # (open) Gn$(38,10)
    phy_count                = 'Gn$(48,7)'        # Phy Count
    upstock_qty              = 'Gn$(55,7)'        # Upstock Qty
    loc_max                  = 'Gn$(62,6)'        # Loc Max
    case_dimn                = 'Gn$(68,10)'       # Case Dimn
    net_un_wt                = 'I(0)'             # Net Un Wt
    grs_un_wt                = 'I(1)'             # Grs Un Wt
    un_ic_un                 = 'I(2)'             # $ un/IC un
    sls_un_c                 = 'I(3)'             # # Sls UN /MC
    reorder_pt               = 'I(4)'             # Reorder Pt
    maximum_stock_level      = 'I(5)'             # MAXIMUM STOCK LEVEL
    qty_on_hand              = 'I(6)'             # Qty on Hand
    ic_units_committed       = 'I(7)'             # I/C Units Committed
    ic_units_on_order        = 'I(8)'             # I/C Units On Order
    average_cost             = 'I(9)'             # Average Cost
    last_fob_cost            = 'I(10)'            # Last FOB Cost
    unit_cube                = 'I(11)'            # Unit Cube
    qty_allocated            = 'I(12)'            # Quantity Allocated
    mtd_unit_sales           = 'I(13)'            # MTD Unit Sales
    ytd_unit_sales           = 'I(14)'            # YTD Unit Sales
    beginning_balance        = 'I(15)'            # Beginning Balance
    old_retail               = 'I(16)'            # Old Retail
    old_wholesale            = 'I(17)'            # Old Wholesale
    old_landed_cost          = 'I(18)'            # Old Landed Cost
    old_fob_cost             = 'I(19)'            # Old FOB Cost
    frght_hndlg              = 'I(20)'            # Frght/Hndlg
    disc_allow_amt           = 'I(21)'            # Disc/Allow Amt
    new_retail               = 'I(22)'            # New Retail
    new_whlsle               = 'I(23)'            # New Whlsle
    new_landed               = 'I(24)'            # New Landed
    new_fob_cost             = 'I(25)'            # New FOB Cost

class F328(str, Enum):
    """
    IFPP0 - SALES ORDER PRODUCTION PENDING - HEADER
    """
    company_id              = 'An$(1,2)'        #   0: Company Code
    order_no                = 'An$(3,6)'        #   1: Order Number
    release_no              = 'An$(9,2)'        #   2: Release No
    seq_no                  = 'An$(11,3)'       #   3: Sequence No
    record_type_0000        = 'An$(14,4)'       #   4: Record Type = '0000'
    batch_id_a              = 'Bn$(1,1)'        #   5: Batch Id - A
    formula_type            = 'Bn$(2,1)'        #   6: Formula Type (P/L/T/X/V/K)
    prod_order_printed      = 'Bn$(3,1)'        #   7: Prod Order Printed? (Y/N)
    packaging_order_printed = 'Bn$(4,1)'        #   8: Packaging Order Printed (Y/N)
    lot_nos_assigned        = 'Bn$(5,1)'        #   9: Lot Numbers Assigned (Y/N)
    batching_auto_manual    = 'Bn$(6,1)'        #  10: Batching Auto/Manual (A/M)
    recommit_necessary      = 'Bn$(7,1)'        #  11: Recommit Necessary (Y/N)
    produced                = 'Bn$(8,1)'        #  12: Produced (Y/N/P/X)
    type                    = 'Bn$(9,1)'        #  13: Type (S/M/X)
    spec_prod_changes       = 'Bn$(10,1)'       #  14: Spec Prod Changes (Y/N)
                                                # (open) Bn$(11,2)
    order_confirmed         = 'Bn$(13,1)'       #  16: Order Confirmed?
                                                # (open) Bn$(14,7)
    prod_no                 = 'Cn$(1,8)'        #  18: Product Number
    label                   = 'Cn$(9,6)'        #  19: Label
    pallets                 = 'Cn$(15,4)'       #  20: Pallets
    formula_id              = 'Cn$(19,10)'      #  21: Formula Code
    formula_rev             = 'Cn$(29,3)'       #  22: Formula Revision
    prod_color              = 'Cn$(32,18)'      #  23: Product Color
    tablet_type             = 'Cn$(50,3)'       #  24: Tablet Type
    hardness_range          = 'Cn$(53,8)'       #  25: Hardness Range
    thickness               = 'Cn$(61,13)'      #  26: Thickness
    label_claim             = 'Cn$(74,5)'       #  27: Label Claim
    current_status          = 'Cn$(79,2)'       #  28: Current Status
    requested_date          = 'Cn$(81,6)'       #  29: Requested Date
    addl_so_refs            = 'Cn$(87,24)'      #  30: Addl S/O Refs
    label_name              = 'Cn$(111,40)'     #  31: Label Name
    serving_size_units      = 'Cn$(151,2)'      #  32: Serving Size Units
    bult_item_units         = 'Cn$(153,2)'      #  33: Bult Item Units
    fingoods_units          = 'Cn$(155,2)'      #  34: Fin.Goods Units
    dept_id                 = 'Cn$(157,2)'      #  35: Department Code
    prod_line               = 'Cn$(159,2)'      #  36: Production Line
                                                # (open) Cn$(161,2)
    instruction_line_1      = 'Dn$'             #  38: Instruction Line 1
    instruction_line_2      = 'En$'             #  39: Instruction Line 2
    prod_scheduled_date     = 'Fn$(1,6)'        #  40: Production Scheduled Date
    date_lot_no_assgnd      = 'Fn$(7,6)'        #  41: Date Lot No Assgnd
    prod_date               = 'Fn$(13,6)'       #  42: Production Date
    scheduled_date          = 'Fn$(19,6)'       #  43: Scheduled Date
    warning_ids             = 'Gn$'             #  44: Warning Codes
    item_key                = 'Hn$'             #  45: Item Key (Inventory)
    lot_no_range_1          = 'In$'             #  46: Lot No Range 1
    lot_no_range_2          = 'Jn$'             #  47: Lot No Range 2
    lot_no_range_3          = 'Kn$'             #  48: Lot No Range 3
    lot_nos_produced        = 'Ln$'             #  49: Lot Nos Produced
    units_ordered           = 'An'              #  50: Units Ordered
    prod_qty                = 'Bn'              #  51: Production Qty
    no_of_batches_a         = 'Cn'              #  52: Number Of Batches - A
    no_of_batches_b         = 'Dn'              #  53: Number Of Batches - B
    batch_weight_a          = 'En'              #  54: Batch Weight - A
    batch_weight_b          = 'Fn'              #  55: Batch Weight - B
    batch_size              = 'Gn'              #  56: Batch Size (Units) - A
    batch_size              = 'Hn'              #  57: Batch Size (Units) - B
    weight_10               = 'In'              #  58: Weight/10
                                                # (open) Jn
    fg_qty_to_use           = 'Kn'              #  60: F.G. Qty To Use
    units_produced          = 'Ln'              #  61: Units Produced
    no_of_lots_produced     = 'Mn'              #  62: No Of Lots Produced
    qty_on_order            = 'Nn'              #  63: Qty On Order
