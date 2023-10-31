from fislib.schema import F135, F320, F322, F328, F329
from VSS.BBxXlate.fisData import fisData
from openerplib import AttrDict

def get_item_ingredients(item, rev='000', food_only=False):
    if not item:
        return []
    get_fis_data()
    #ensure item is 10 chars long
    item_ingredient, rev = '%-10s' % item, '%-3s' % rev
    item = item[:6]
    fulllist = [(rec[F322.ingr_code_batch_1], key, rec) for key, rec in IFDT.get_subset((item_ingredient, rev))]
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

def get_order_ingredients(order, food_only=False, include_null=True):
    get_fis_data()
    # get the order record from 328
    order, order_no = IFPP0[order], order
    item = order[F328.prod_no].strip()
    # then the ingredients
    fulllist = [(rec[F329.ingr_code_batch_1], key, rec) for key, rec in IFPP1.get_subset(order_no)]
    # import pdb; pdb.set_trace()
    foodlist = []
    # for i in sorted(ingredients, key=lambda r: r[F329.formula_line_no]):
    for ingredient, key, rec in fulllist:
        ingredient = ingredient[:6]
        if ingredient in ignored_ingredients:
            continue
        if rec[F329.qty_batch_1] or include_null:
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
    if not item:
        return AttrDict()
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
        rev = recipe[F320.rev_no]
        if NVTY.has_key(item):
            recipes.append((item, rev))
        elif print_missing:
            print('skipping recipe', item)
    return recipes

def get_ingredient_data(
        oid, item, qty=1, exdata=None, food_only=False, inventory=None,
        item_refs=None, level=None, use_production=False, include_null=True,
        ):
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
        if ifdt[F.qty_batch_1] or include_null:
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
        '910000', '910001', '910002', '910003', '910004', '910005', '910006',
        '910007', '910008',
        # misc
        '900110', '900111', '900112', '900113', '900115', '900200', '900205',
        '900210', '900215', '900230', '900235', '900291', '900448', '900485',
        '900700', '900715', '900900', '900910', '900915', '900917', '900918',
        '900920', '900921', '900922', '900930', '900932', '900935', '900940',
        '900950', '900951', '900952', '900954', '900960', '900962', '900965',
        '900970', '900975', '900980', '900983', '900985', '900986', '900995',
        '901000', '901005', '901006', '901008', '901009', '901010', '901011',
        '901012', '901013', '901014', '901019', '901021', '901023', '901028',
        '901031', '901040', '901041', '901042', '901043', '901044', '901045',
        '901046', '901050', '901065', '901091', '901093', '901095', '901097',
        '901098', '901100', '901101', '901102', '901105', '901107', '901111',
        '901112', '901113', '901117', '901128', '901130', '901131', '901132',
        '901133', '901134', '901135', '901200', '901210', '901245', '901265',
        '901279', '901285', '901286', '901288', '901291', '901292', '901293',
        '901295', '901298', '901302', '901315', '901327', '901329', '901331',
        '901338', '901340', '901352', '901370', '901372', '901375', '901380',
        '901400', '901401', '901403', '901404', '901406', '901407', '901409',
        '901425', '901451', '901465', '901467', '901468', '901469', '901500',
        '901502', '901505', '901507', '901510', '901520', '901521', '901522',
        '901523', '901524', '901525', '901530', '901531', '901532', '901533',
        '901570', '901571', '901572', '901630', '902002', '902003', '902004',
        '902005', '902006', '902007', '902008', '902022', '902025', '902027',
        '902071', '902073', '902076', '902078', '902101', '902105', '902120',
        '902125', '902126', '902127', '902128', '902130', '902134', '902136',
        '902140', '902143', '902150', '902152', '902280', '902281', '902282',
        '902283', '902288', '902495', '902498', '902499', '902500', '902501',
        '902502', '902503', '902663', '904108', '905001', '905005', '905008',
        '905010', '905015', '905016', '905685', '905700', '905703', '905728',
        '906017', '906050', '906063', '906212', '906220', '906223', '906225',
        '906704', '906705', '906706', '906707', '907134', '907135', '907149',
        '909450', '910103', '910109', '913810', '914108', '916105', '916107',
        '919163', '919164', '919165', '919180', '921112', '921113', '921115',
        '921117', '921120', '921121', '921122', '921123', '921124', '921125',
        '921126', '921127', '921128', '921129', '921130', '921132', '921133',
        '921138', '921211', '921212', '921300', '921308', '921310', '921312',
        '921313', '921314', '921315', '921320', '921322', '921325', '921330',
        '921335', '921336', '921337', '921338', '921340', '921342', '921345',
        '922162', '922166', '922167', '922600', '922601', '922602', '922603',
        '922604', '922605', '922606', '922607', '922608', '922609', '922610',
        '922611', '922612', '922613', '922614', '922615', '922616', '922617',
        '922618', '923610', '923613', '923614', '923615', '923616', '923617',
        '923618', '923619', '923621', '923622', '929340', '929450', '929550',
        '929551', '929552', '929553', '929610', '936148', '936149', '936150',
        '936151', '936152', '936153', '936154', '939105', '940105', '940200',
        '940201', '940202', '940205', '940210', '940215', '940220', '940225',
        '949448', '949495', '949555', '950800', '950808', '950815', '950817',
        '950820', '950830', '950831', '950832', '950834', '950837', '950925',
        '950926', '950927', '950929', '961005', '961007', '967005', '967052',
        '968103', '968107', '969025', '969027', '969031', '970000', '970150',
        '970220', '970221', '971050', '971051', '971052', '981040', '981095',
        '981097', '981112', '981312', '981400', '985002', '985003', '985103',
        '986063', '986064', '986065', '986066', '986067', '986700', '990103',
        '990605', '995000', '995100', '999016', '999017', '999018',
        # freight charges
        '967001', '967003', '967004', '993030', '993040', '996000', '996001',
        '996002', '996333', '996555', '997090',
        ])

