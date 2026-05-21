#!/usr/bin/python3.5
import sys
sys.path.insert(0, '/usr/local/bin/fis-oe3')

from antipathy import Path
import dbf
from epithets import *
from fis_oe.sql import Table as SQLTable, SQL, ConnectionError
try:
    from MySQLdb import _mysql
except ImportError:
    _mysql = None
import logging
from scription import *

## globals

load_primary_data = SQL("""
        SELECT xml_id, name, fis_web_parent, fis_web_active, fis_web_ingredients,
               fis_web_ingredients2, fis_web_allergens, fis_web_shared_equipment, fis_web_warnings
        FROM product.product
        WHERE fis_web_active=True
        """)

mysql_ingred = (
        "UPDATE `sunridge_shop`.`wp__postmeta` "
        "SET `meta_value` = '%s' "
        "WHERE meta_key='attr_ingredients' and `post_id` = '%s';" 
            )

mysql_allergen = (
        "UPDATE `sunridge_shop`.`wp__postmeta` "
        "SET `meta_value` = '%s' "
        "WHERE meta_key='attr_allergens' and `post_id` = '%s';"
        )

mysql_shared = (
        "UPDATE `sunridge_shop`.`wp__postmeta` "
        "SET `meta_value` = '%s' "
        "WHERE meta_key='attr_shared' and `post_id` = '%s';"
        )

mysql_warning = (
        "UPDATE `sunridge_shop`.`wp__postmeta` "
        "SET `meta_value` = '%s' "
        "WHERE meta_key='attr_warnings' and `post_id` = '%s';"
        )

working_table = Path('/var/web-ingredients/web_products.dbf')
log_file = Path('/var/web-ingredients/web-ingredients.log')
corrections_file = Path('/var/web-ingredients/words.txt')

logger = logging.getLogger('web-ingredients')
logging.basicConfig(filename=log_file, level=logging.INFO)
logger.info(str(dbf.DateTime))

## Commands

@Command(
        items=('items to update [default=all]', MULTI),
        dry_run=('show updates, but do not do them', FLAG),
        )
def update(dry_run, *items):
    """
    update MySQL Shop database from OpenERP
    """
    global script_verbosity
    if dry_run:
        script_verbosity = 1
        v = 1
    else:
        db = _mysql.connect(host="72.32.164.247", user="sunridgeDB", passwd="us3l3ssr!s3S3t")
        v = 2

    extra = ''
    if items:
        extra = "and xml_id in [%s]" % ','.join(repr(i) for i in items)

    oe_q = """
            select 
                xml_id, 
                fis_web_parent,
                fis_web_ingredients2,
                fis_web_allergens,
                fis_web_shared_equipment,
                fis_web_warnings
            from product.product
            where fis_web_active=true %s
            """ % extra
    print('OpenERP:', oe_q, verbose=v)
    print(verbose=v)

    oe_data = list(SQL(oe_q))

    print('%d items retrieved' % len(oe_data))
    print(verbose=v)

    for fis_id,parent_id,ingredients,allergen,shared,warning in oe_data:
        #Update ingredient statement to web (replace w/ variables)
        ingred_q = mysql_ingred % (ingredients or '', int(parent_id))
        print('ingredients:', ingred_q, verbose=v)
        print(verbose=v)

        #Update allergen statement to web (replace w/ variables)
        allergen_q = mysql_allergen % (allergen or '', int(parent_id))
        print('allergen:', allergen_q, verbose=v)
        print(verbose=v)

        #Update shared equipment statement to web (replace w/ variables)
        shared_q = mysql_shared % (shared or '', int(parent_id))
        print('shared:', shared_q, verbose=v)
        print(verbose=v)

        #Update warnings to web (replace w/ variables)
        warning_q = mysql_warning % (warning or '', int(parent_id))
        print('warnings:', warning_q, verbose=v)
        print(verbose=v)

        if not dry_run:
            db.query(ingred_q)
            db.query(allergen_q)
            db.query(shared_q)
            db.query(warning_q)
            db.commit()
        print('Shop updated')


@Command(
        reset=('recreate dbf file', FLAG),
        )
def web_ingredients(reset):
    #
    # need buttons for:
    # - load data from OpenERP/Labeltime (fis_web_ingredients -> c_source)
    # - store data to OpenERP  (fis_web_ (ingredients2 | allergens | shared_equipment | warnings | parent) )
    # - store data to web store ( ^- all these )
    #   (should both store buttons just be one?)
    #
    # keep retrieved data in a .dbf file for easy reference
    #
    # `c_source`:       current LT data from `fis_web_ingredients` (no `2` suffix)
    # `c_*`:            current fields from LT data (modifiable)
    # `f_*`:            final fields saved to fis_web_* and web store
    # `f_source`:       LT data used for last save operation
    # `modified`:       text adjusted automatically

    correct_words = set((
            '', '&',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
            '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
            '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
            '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
            '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
            '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
            '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
            '80', '81', '82', '83', '84', '85', '86', '87', '88', '89',
            '90', '91', '92', '93', '94', '95', '96', '97', '98', '99',
            '100',
            'a', 'aa', 'acacia', 'acid', 'active', 'added', 'adzuki', 'allergenic',
            'almond', 'almonds', 'amaranth', 'and', 'and/or', 'anhydrous', 'animal',
            'aniseed', 'annatto', 'anthocyanin', 'apple', 'apples', 'apricot',
            'apricots', 'arabic', 'arborio', 'as', 'ascorbic', 'autolyzed', 'b12',
            'baby', 'baking', 'balls', 'banana', 'bananas', 'bar', 'barbeque', 'barley',
            'basil', 'basmati', 'bbq', 'bean', 'beans', 'bears', 'beet', 'beets',
            'berries', 'berry', 'beta', 'bicarbonate', 'bing', 'bites', 'black', 'blackberries',
            'blackcurrant', 'blanched', 'blend', 'blonde', 'blueberries', 'bran',
            'brazil', 'broccoli', 'brown', 'buckwheat', 'bulgur', 'butter', 'by', 'ca', 'cabbage', 'cacao',
            'cake', 'caking', 'calcium', 'california', 'cancer', 'cane', 'cannellini',
            'canola', 'caramel', 'caramels', 'carbonate', 'cardamom', 'carnauba',
            'carob', 'carotene', 'carrageenan', 'carrot', 'carrots', 'cashew',
            'cashews', 'cayenne', 'celery', 'center', 'centers', 'cereal',
            'certified', 'chai', 'cheddar', 'cheese', 'cherries', 'cherry', 'chews',
            'chia', 'chickpeas', 'chile', 'chiles', 'chili', 'chimayo', 'chipotle',
            'chips', 'chocolate', 'chopped', 'chunks', 'churro', 'cider', 'cinnamon',
            'citric', 'clove', 'cloves', 'clusters', 'coating', 'coatings', 'cocoa',
            'coconut', 'coffee', 'cold', 'cold-pressed', 'color', 'colored', 'colors',
            'concentrate', 'concentrated', 'condensed', 'contain', 'contains', 'cookie',
            'cookies', 'coriander', 'corn', 'cornstarch', 'cracked', 'crackers',
            'cranberries', 'cranberry', 'cream', 'crisp', 'crispy', 'crushed',
            'crystallized', 'crystals', 'culture', 'cultured', 'cultures', 'cumin',
            'cup', 'cups', 'currant', 'currants', 'curry', 'cut', 'dairy', 'dark',
            'date', 'dates', 'defatted', 'deglet', 'dehydrated', 'dextrin', 'dextrose',
            'diced', 'dietary', 'diglycerides', 'dioxide', 'distillate', 'distilled',
            'dragon', 'dried', 'drizzle', 'drops', 'dry', 'durum', 'e', 'egg', 'eggs',
            'elote', 'emmer', 'emulsifier', 'enriched', 'enzymes', 'equipment',
            'erythritol', 'espresso', 'evaporated', 'expeller', 'extract', 'extractive', 'extractives',
            'facility', 'fair', 'fancy', 'farro', 'fennel', 'fenugreek', 'ferrous',
            'fiber', 'fig', 'figs', 'filbert', 'filberts', 'filled', 'filling', 'flakes',
            'flame', 'flavor', 'flavors', 'flax', 'flour', 'folic', 'food', 'for',
            'fractionated', 'freeze', 'freshness', 'from', 'fruit', 'fuji', 'garbanzo',
            'garlic', 'ghost', 'ginger', 'glaze', 'glazed', 'glucose', 'glycerin',
            'glycerine', 'gmo', 'goji', 'golden', 'gov/food', 'grade', 'grain', 'grape',
            'granola', 'granulated', 'great', 'green', 'greens', 'groats', 'ground', 'gum', 'hard',
            'harm', 'hatch', 'hazelnut', 'hazelnuts', 'heavy', 'hemp', 'high', 'highly',
            'honey', 'horseradish', 'hot', 'hulled', 'hulls', 'husks', 'hydrochloride',
            'in', 'in-shell', 'including', 'ingredients', 'inulin', 'iron', 'is',
            'isolate', 'jalapeno', 'jasmine', 'jolly', 'juice', 'jumbo', 'kale', 'kernel',
            'keto', 'kidney', 'lactic', 'lactose', 'large', 'lecithin', 'lemon',
            'lentils', 'less', 'licorice', 'lima', 'lime', 'locust', 'long', 'maca',
            'macadamia', 'macadamias', 'made', 'maintain', 'malic', 'malt', 'malted',
            'maltodextrin', 'mango', 'manufactured', 'maple', 'marcona', 'may', 'meal',
            'medium', 'medjool', 'mesquite', 'mexican', 'milk', 'milkfat', 'milled',
            'millet', 'mini', 'mint', 'mission', 'mixed', 'modified', 'molasses', 'monk', 'mono',
            'mononitrate', 'multi', 'mung', 'mustard', 'natural', 'navy', 'nectarine',
            'nectarines', 'niacin', 'nibs', 'non', 'non-allergenic', 'nonfat', 'nongmo',
            'nonpareil', 'noor', 'northern', 'nuggets', 'nut', 'nutmeg', 'nuts', 'oat',
            'oats', 'of', 'oil', 'oils', 'oleic', 'on', 'onion', 'or', 'orange', 'oregano',
            'organic', 'other', 'p65warnings', 'palm', 'papaya', 'paprika', 'parboiled',
            'parsley', 'partially', 'pasteurized', 'pastry', 'pea', 'peach', 'peaches',
            'peanut', 'peanuts', 'pear', 'pearled', 'pears', 'peas', 'pecan', 'pecans',
            'pectin', 'pepper', 'peppermint', 'peppers', 'persimmon', 'persimmons', 'phosphate',
            'phosphates', 'picante', 'pieces', 'pine', 'pineapple', 'pineapples',
            'pinto', 'pistachio', 'pistachios', 'pits', 'pitted', 'plantain', 'plantains',
            'polenta', 'pomegranate', 'popcorn', 'poppy', 'potato', 'powder', 'powders', 'powdered', 'power',
            'premium', 'preservative', 'pressed', 'pretzel', 'pretzels', 'prevent',
            'produced', 'protein', 'prune', 'prunes', 'psyllium', 'pumpkin', 'pure',
            'puree', 'purple', 'pyridoxine', 'pyrophosphate', 'quick', 'quinoa', 'radish',
            'rainbow', 'raisins', 'raspberries', 'raspberry', 'raw', 'red', 'redskin',
            'reduced', 'refined', 'reproductive', 'responsibly', 'retention', 'riboflavin',
            'rice', 'roasted', 'rolled', 'rosemary', 'rye', 'safflower', 'salt', 'salted',
            'sauce', 'sea', 'seasoned', 'seasoning', 'seed', 'seeds', 'semisweet',
            'semolina', 'sesame', 'shared', 'shell', 'shelled', 'short', 'shortbread',
            'shoyu', 'shredded', 'silicon', 'skin', 'sliced', 'slices', 'slivered',
            'smoke', 'soda', 'sodium', 'soft', 'solids', 'sour', 'source', 'sourced',
            'soy', 'soybean', 'soybeans', 'spelt', 'spice', 'spiced', 'spices', 'spicy',
            'spinach', 'spirulina', 'split', 'spring', 'squash', 'starch', 'stars',
            'starter', 'steel', 'stevia', 'sticks', 'stone', 'strawberries', 'strawberry',
            'style', 'sucrose', 'sugar', 'sulfate', 'sulfite', 'sulfites', 'sulphite',
            'sulphites', 'sulphur', 'sultana', 'sunflower', 'sunny', 'supreme', 'sunflower', 'sushi',
            'sweet', 'sweetened', 'sweetener', 'syrup', 'tack', 'tamari', 'tapioca',
            'taro', 'tart', 'tartaric', 'tea', 'thamine', 'that', 'thews', 'thiamin', 'thiamine',
            'thick', 'thompson', 'tm', 'to', 'toasted', 'tocopherols', 'toffee', 'tomato',
            'tomatoes', 'torula', 'trade', 'treacle', 'tree', 'tricolor', 'triticale',
            'truffle', 'turbinado', 'turmeric', 'unbleached', 'unsalted', 'unsweetened',
            'usa', 'uses', 'vanilla', 'vegetable', 'vegetables', 'vinegar', 'vitamin',
            'walnut', 'walnuts', 'warning', 'wasabi', 'water', 'wax', 'wheat', 'whey',
            'white', 'whole', 'wild', 'winter', 'with', 'worms', 'www',
            'www.p65warnings.ca.gov/food', 'xanthan', 'yeast', 'yellow', 'yogurt',
            ))

    with open(corrections_file) as fh:
        for word in fh.read().split():
            if word:
                correct_words.add(word)

    class CommandButton(Frame):
        orient = VERTICAL
        border_style = SPACE

        def __init__(self):
            super().__init__()
            l = self.add_widget(Button('Load initial data', '#load', on_click=Signal('LoadInitial')))
            s = self.add_widget(Button('Save to OpenERP/Web Store', '#save', on_click=Signal('SaveAndPublish')))
            self.sizes = []
            self.layouts = [HORIZONTAL, VERTICAL]
            # first configuration: all on one "line"
            height = max(w.outer_size.height for w in (l, s))
            width = sum(w.outer_size.width for w in (l, s))
            self.sizes.append(Size(height, width))
            # second configuration: all in one column
            height = sum(w.outer_size.height for w in (l, s))
            width = max(w.outer_size.width for w in (l, s))
            self.sizes.append(Size(height, width))

    class Filter(RadioButtons):
        orient = VERTICAL
        border_style = SPACE
        choices = ( 'Source Changed', 'Source Empty', 'Fields Changed', 'AutoModified',
                    'Empty Equipment', 'Allergens', 'Warnings',
                    'Web Inactive', 'SRF Removed', 'Typos',
                    )
        size = 4, 75

    class Meta(Frame):
        border_style=SINGLE
        # css_id = '#meta'
        orient = VERTICAL
        size = 3, 100
        sticky = EW

        def __init__(self):
            super().__init__()
            self.add_widget(Label('FIS ID:                    '))
            self.add_widget(Label('Web parent:'))
            self.add_widget(Label('Web active:'))
            self.add_widget(Label('Name:'))
            self.add_widget(Label('Record:'))
            self.xml_id = ''
            self.product_name = ''
            self.web_parent = ''
            self.web_active = False
            self.total_records = 0
            self.current_recno = -1

        @property
        def current_record(self):
            return self._current_record

        @current_record.setter
        def current_record(self, rec):
            logger.debug('SETTING current record to %s(%r)', type(rec), rec)
            self._current_record = rec

        def paint(self, attr=A_NORMAL, cascade=True):
            super().paint(attr=attr, cascade=cascade)
            self.add_string(0, 12, self.xml_id)
            self.add_string(1, 12, self.web_parent)
            self.add_string(2, 12, str(self.web_active))
            self.add_string(0, 35, self.product_name)
            self.add_string(1, 35, '%s of %s' % (self.current_recno+1, self.total_records))
            self.refresh()


    class InitialData(TextBox):
        border_style = DOUBLE
        _focusable = False

        def _calc_best_fit(self, height, width):
            logger.debug('InitialData._calc_best_fit(%r, %r)', height, width)
            super()._calc_best_fit(min(16+self._dfy, height), width)


    class FixedData(TextBox):
        border_style = SINGLE

        def _calc_best_fit(self, height, width):
            logger.debug('FixedData._calc_best_fit(%r, %r)', height,width)
            w = self.parent.inner_size.width // 2 - self._dfx
            if 'ingredients' in self.css_id:
                self.inner_size = 23, w
            else:
                self.inner_size = 6, w
            super()._calc_best_fit(height, width)

        def paint(self, attr=A_NORMAL, cascade=True):
            super().paint(attr=attr, cascade=cascade)
            if self.read_only:
                return
            # underline unknown words
            y, x = 0, 0
            under = attr | A_UNDERLINE | curses.color_pair(1) | COLOR_RED
            while "checking words":
                ey, ex = self._word_end(y, x)
                if (ey, ex) == (y, x):
                    # nothing new found
                    break
                sy, sx = self._word_start(ey, ex)
                if (ey, ex) == (sy, sx):
                    # no words
                    break
                word = self.in_string(sy, sx, ex-sx)
                lword = word.strip(non_alpha).lower()
                if lword not in correct_words:
                    self.add_string(sy, sx, word, under)
                y, x = ey, ex + 1
            self.refresh()


    class MyApp(App):
        """
        Good stuff!
        """
        border_style = SINGLE
        current_index = None
        status = 2
        title = 'Web Data Updates'
        _rec_no = -1

        layout = [
                CommandButton, Filter, Meta,
                InitialData(id='initial', title='Initial Data'),
                FixedData(id='ingredients', title='LabelTime Ingredients'), FixedData(id='web_ingredients', title='Web Ingredients', read_only=True),
                FixedData(id='allergens', title='LabelTime Allergens'), FixedData(id='web_allergens', title='Web Allergens', read_only=True),
                FixedData(id='equipment', title='LabelTime Shared Equipment'), FixedData(id='web_equipment', title='Web Shared Equipment', read_only=True),
                FixedData(id='warnings', title='LabelTime Warnings'), FixedData(id='web_warnings', title='Web Warnings', read_only=True),
                ]

        def __init__(self):
            super().__init__()
            if working_table.exists() and not reset:
                logger.debug('using existing table %r', working_table)
                t = self.table = dbf.Table(working_table, dbf_type='clp', default_data_types='enhanced').open(dbf.READ_WRITE)
                sched.call_soon(self.load_next_record)
            else:
                logger.debug('creating %r', working_table)
                t = self.table = dbf.Table(
                        working_table,
                        [   'xml_id C(6)',
                            'name C(96)',
                            'parent_id C(12)',
                            'web_active L',
                            'c_source C(2048)',
                            'c_ingred C(2048)',
                            'c_allrgn C(512)',
                            'c_equip C(512)',
                            'c_warns C(512)',
                            'f_source C(2048)',
                            'f_ingred C(2048)',
                            'f_allrgn C(512)',
                            'f_equip C(512)',
                            'f_warns C(512)',
                            'modified L',
                            ],
                        dbf_type='clp',
                        default_data_types='enhanced',
                        ).open(dbf.READ_WRITE)
            self.meta = self.query_one(cls=Meta)
            self.meta.total_count = len(t)
            self.initial = self.query_one('#initial')
            #
            self.ingredients = self.query_one('#ingredients')
            self.allergens = self.query_one('#allergens')
            self.equipment = self.query_one('#equipment')
            self.warnings = self.query_one('#warnings')
            self.web_ingredients = self.query_one('#web_ingredients')
            self.web_allergens = self.query_one('#web_allergens')
            self.web_equipment = self.query_one('#web_equipment')
            self.web_warnings = self.query_one('#web_warnings')
            #
            def changed_field(rec):
                """
                Labeltime fields that are different from Web fields.
                """
                return (
                        rec.c_ingred != rec.f_ingred or rec.c_allrgn != rec.f_allrgn or
                        rec.c_equip != rec.f_equip or rec.c_warns != rec.f_warns
                        ) and rec.xml_id or dbf.DoNotIndex
            def changed_source(rec):
                """
                Labeltime data has changed.
                """
                return rec.c_source != rec.f_source and rec.xml_id or dbf.DoNotIndex
            def auto_changed(rec):                                                  
                """
                Fields automatically adjusted by program.
                """
                return rec.modified and rec.xml_id or dbf.DoNotIndex
            def source_empty(rec):
                """
                Labeltime source is empty.
                """
                return rec.c_source == '' and rec.xml_id or dbf.DoNotIndex
            def web_inactive(rec):
                """
                No longer web active.
                """
                return rec.web_active and rec.xml_id or dbf.DoNotIndex
            def allergens(rec):
                """
                Contains allergens.
                """
                return (rec.c_allrgn or rec.f_allrgn) and rec.xml_id or dbf.DoNotIndex
            def equipment(rec):
                """
                Empty shared equipment.
                """
                return (rec.c_equip and rec.f_equip) and dbf.DoNotIndex or rec.xml_id
            def warning(rec):
                """
                Has warnings.
                """
                return (rec.c_warns or rec.f_warns) and rec.xml_id or dbf.DoNotIndex
            def srf_removed(rec):
                """
                sunridgefarms.com removed.
                """
                return 'sunridge' in rec.c_source and rec.xml_id or dbf.DoNotIndex
            def typos(rec):
                """
                Misspelled words.
                """
                for w in get_words(rec.c_ingred, rec.c_allrgn, rec.c_equip, rec.c_warns):
                    if w not in correct_words:
                        return rec.xml_id
                else:
                    return dbf.DoNotIndex
            self.indices = {}
            self.indices['Fields Changed'] = dbf.Index(t, changed_field)
            self.indices['Source Changed'] = dbf.Index(t, changed_source)
            self.indices['AutoModified'] = dbf.Index(t, auto_changed)
            self.indices['Web Inactive'] = dbf.Index(t, web_inactive)
            self.indices['Allergens'] = dbf.Index(t, allergens)
            self.indices['Empty Equipment'] = dbf.Index(t, equipment)
            self.indices['Warnings'] = dbf.Index(t, warning)
            self.indices['SRF Removed'] = dbf.Index(t, srf_removed)
            self.indices['Typos'] = dbf.Index(t, typos)
            self.indices['Source Empty'] = dbf.Index(t, source_empty)
            self.indices[()] = self.primary_index = dbf.Index(t, lambda rec: rec.xml_id, doc='xml_id')
            self.current_index = self.primary_index
            self.meta.total_records = len(self.table)

        @on_key(KEY_CTRL_A, limit_scope=('#ingredients','#allergens','#equipment','#warnings'))
        def add_words(self):
            """
            ^A=Add words
            """
            record = self.current_index[self._rec_no]
            typos = self.indices['Typos']
            cid = sched.focus.css_id
            self.save_to_dbf()
            with open(corrections_file, 'a') as fh:
                if cid == '#ingredients':
                    for w in get_words(self.ingredients.value):
                        if w not in correct_words:
                            fh.write('%s\n' % w)
                            correct_words.add(w)
                elif cid == '#allergens':
                    for w in get_words(self.allergens.value):
                        if w not in correct_words:
                            fh.write('%s\n' % w)
                            correct_words.add(w)
                elif cid == '#equipment':
                    for w in get_words(self.equipment.value):
                        if w not in correct_words:
                            fh.write('%s\n' % w)
                            correct_words.add(w)
                elif cid == '#warnings':
                    for w in get_words(self.warnings.value):
                        if w not in correct_words:
                            fh.write('%s\n' % w)
                            correct_words.add(w)
                else:
                    raise ValueError('unknown id: %r' % cid)
            for rec in self.current_index:
                typos(rec)
            if record in typos:
                self.display_record(self._rec_no)
            else:
                self.display_record(None)
                self.meta.total_records = len(self.current_index)
                self._rec_no = -1
                self.load_next_record()

        def display_record(self, rec_no):
            if rec_no is None:
                rec_no = -1
                rec = self.table.create_template()
            else:
                rec = self.current_index[rec_no]
            #
            self.meta.xml_id = rec.xml_id
            self.meta.product_name = rec.name
            self.meta.web_parent = rec.parent_id
            self.meta.web_active = rec.web_active
            self.meta.current_recno = rec_no
            self.initial.value = '\n'.join(['', rec.c_source])
            self.ingredients.value = rec.c_ingred
            self.allergens.value = rec.c_allrgn
            self.equipment.value = rec.c_equip
            self.warnings.value = rec.c_warns
            self.web_ingredients.value = rec.f_ingred
            self.web_allergens.value = rec.f_allrgn
            self.web_equipment.value = rec.f_equip
            self.web_warnings.value = rec.f_warns
            for tb in (
                    self.ingredients, self.allergens, self.equipment, self.warnings,
                    self.web_ingredients, self.web_allergens, self.web_equipment, self.web_warnings,
                ):
                tb.border_style = SINGLE
            # highlight differences
            if rec.c_ingred != rec.f_ingred:
                self.ingredients.border_style = '*'
                self.web_ingredients.border_style = ' '
            if rec.c_allrgn != rec.f_allrgn:
                self.allergens.border_style = '*'
                self.web_allergens.border_style = ' '
            if rec.c_equip != rec.f_equip:
                self.equipment.border_style = '*'
                self.web_equipment.border_style = ' '
            if rec.c_warns != rec.f_warns:
                self.warnings.border_style = '*'
                self.web_warnings.border_style = ' '
            self.main.paint()
            self.main.refresh()

        def on_filter(self, msg):
            """
            Change to selected filter.
            """
            logger.debug('selected %r', msg)
            new_index = self.indices.get(msg.selected)
            if new_index is None:
                ProgramStatus('Unknown filter: %r' % (msg.selected, ))
                return
            self.current_index = new_index
            meta = self.meta
            meta.total_records = len(self.current_index)
            meta.current_recno = -1
            self._rec_no = -1
            self.display_record(None)
            self.load_next_record()

        async def on_load_initial(self):
            logger.debug('on_load_initial running')
            status = ProgramStatus('Loading records from OpenERP...', show_button=False)
            for rec in dbf.Process(self.table):
                rec.web_active = False
            try:
                q = load_primary_data.execute()
            except ConnectionError as e:
                status.dismiss()
                sched.call_soon(ProgramStatus, str(e))
                return
            for r in q:
                logger.debug('record: %r', r)
                self.save_to_dbf(self.parse_record(r))
                await switch()
            logger.debug('LINES')
            self.meta.total_records = len(self.table)
            logger.debug('len(self.table): %r', len(self.table))
            status.show_button()
            if self._rec_no == -1:
                self.load_next_record()

        def on_save_and_publish(self, xml_id=None):
            xml_ids = set()
            if _mysql is not None:
                db = _mysql.connect(host="72.32.164.247", user="sunridgeDB", passwd="us3l3ssr!s3S3t")
            # save all labeltime fields to their web* field equivalents
            for rec in dbf.Process(self.table):
                if xml_id is None or rec.xml_id == xml_id:
                    xml_ids.add(rec.xml_id)
                    rec.f_source = rec.c_source
                    rec.f_ingred = rec.c_ingred
                    rec.f_allrgn = rec.c_allrgn
                    rec.f_equip = rec.c_equip
                    rec.f_warns = rec.c_warns
            # then for each record, save to OpenERP and save to MySQL
            oe_table = SQLTable('product.product').table
            for d in oe_table.read(domain=[('xml_id','in',list(xml_ids))], fields=['id','xml_id']):
                xml_id = d['xml_id']
                rec ,= self.primary_index[xml_id,]
                values = {
                        'fis_web_ingredients2': rec.f_ingred,
                        'fis_web_allergens': rec.f_allrgn,
                        'fis_web_shared_equipment': rec.f_equip,
                        'fis_web_warnings': rec.f_warns,
                        }
                oe_table.write(d['id'], values)
                #
                if _mysql is not None:
                    db.query(mysql_ingred % (rec.f_ingred, int(rec.parent_id)))
                    db.query(mysql_allergen % (rec.f_allgrn, int(rec.parent_id)))
                    db.query(mysql_shared % (rec.f_equip, int(rec.parent_id)))
                    db.query(mysql_warning % (rec.f_warns, int(rec.parent_id)))
                    db.commit()

        @on_key(KEY_CTRL_L, limit_scope=('#ingredients','#allergens','#equipment','#warnings'))
        def load_from_labeltime(self):
            """
            ^L=Labeltime
            """
            # get current data from openerp
            for oe_rec in (SQL("""
                    SELECT fis_web_ingredients
                    FROM product.product
                    WHERE xml_id=%r
                    """ % self.meta.xml_id).execute()
                ):
                break
            # and parse
            self.initial.value = value = oe_rec.fis_web_ingredients or ''
            values = self.parse_source(value)
            cid = sched.focus.css_id
            if cid == '#ingredients':
                self.ingredients.value = values['c_ingred']
            elif cid == '#allergens':
                self.allergens.value = values['c_allrgn']
            elif cid == '#equipment':
                self.equipment.value = values['c_equip']
            elif cid == '#warnings':
                self.warnings.value = values['c_warns']
            else:
                raise ValueError('unknown id: %r' % cid)
            self.paint()
            self.save_to_dbf()

        @on_key(KEY_CTRL_W, limit_scope=('#ingredients','#allergens','#equipment','#warnings'))
        def load_from_web(self):
            """
            ^W=Web
            """
            cid = sched.focus.css_id
            wid = '#web_' + cid[1:]
            lt_frame = self.query_one(cid)
            web_frame = self.query_one(wid)
            lt_frame.value = web_frame.value
            lt_frame.border_style = lt_frame.__class__.border_style
            self.paint()
            self.save_to_dbf()

        @on_key(KEY_NPAGE)
        def load_next_record(self):
            """
            PgDn=Next
            """
            if self._rec_no != -1:
                self.save_to_dbf()
            self._rec_no += 1
            logger.debug('load_next_record: self._rec_no=%r, len(self.current_index)=%r', self._rec_no, len(self.current_index))
            if self._rec_no < len(self.current_index):
                self.display_record(self._rec_no)
            else:
                self._rec_no -= 1

        @on_key(KEY_PPAGE)
        def load_prev_record(self):
            """
            PgUp=Prev
            """
            if self._rec_no != -1:
                self.save_to_dbf()
            self._rec_no -= 1
            if self._rec_no >= 0:
                self.display_record(self._rec_no)
            else:
                self._rec_no = 0

        def parse_record(self, oe_rec):
            values = {
                    'xml_id': oe_rec.xml_id,
                    'name': oe_rec.name,
                    'parent_id': oe_rec.fis_web_parent,
                    'web_active': oe_rec.fis_web_active,
                    'c_source': oe_rec.fis_web_ingredients,
                    'c_ingred': '',
                    'c_allrgn': '',
                    'c_equip': '',
                    'c_warns': '',
                    'f_source': '',
                    'f_ingred': oe_rec.fis_web_ingredients2,
                    'f_allrgn': oe_rec.fis_web_allergens,
                    'f_equip': oe_rec.fis_web_shared_equipment,
                    'f_warns': oe_rec.fis_web_warnings,
                    'modified': False,
                    }
            if oe_rec.fis_web_ingredients:
                return self.parse_source(oe_rec.fis_web_ingredients, values)
            else:
                # empty source, copy web info to labeltime
                values['c_ingred'] = values['f_ingred']
                values['c_allrgn'] = values['f_allrgn']
                values['c_equip'] = values['f_equip']
                values['c_warns'] = values['f_warns']
                return values

        def parse_source(self, source, values=None):
            logging.error('parsing %r', source)
            if values is None:
                values = {
                        'c_ingred': '',
                        'c_allrgn': '',
                        'c_equip': '',
                        'c_warns': '',
                        }
            last = None
            for line in (source or '').split('\n'):
                line = ' '.join(line.split()).replace(
                        ',* ', '*, '
                        ).replace(
                        'Responsibly Source ', 'Responsibly Sourced '
                        ).replace(
                        ' on sahared ', ' on shared '
                        ).replace(
                        ' in shared ', ' on shared '
                        ).replace(
                        ' equpiment ', ' equipment '
                        ).replace(
                        ' and/ or ', ' and/or '
                        )
                lline = line.strip().lower()
                if not lline:
                    continue
                if 'sunridgefarms.com' in lline:
                    srf_index = lline.index('sunridgefarms.com')
                    line = line[:srf_index].strip()
                    lline = line.lower()
                if 'royal oaks' in lline:
                    ro_index = lline.index('royal oaks')
                    line = line[:ro_index].strip()
                    lline = line.lower()
                if 'net wt' in lline:
                    nw_index = lline.index('net wt')
                    line = line[:nw_index].strip()
                    lline = line.lower()
                if lline.startswith('ingredients:'):
                    values['c_ingred'] = line[12:].lstrip()
                    last = 'c_ingred'
                elif lline.startswith('contains:'):
                    values['c_allrgn'] = line
                    last = 'c_allrgn'
                else:
                    m_index = w_index = None
                    if 'manufactured on shared' in lline:
                        m_index = lline.index('manufactured')
                    if 'warning:' in lline:
                        w_index = lline.index('warning:')
                    if m_index is w_index is None:
                        # attach to last line
                        values[last] = '%s %s' % (values[last], line.strip())
                        values['modified'] = True
                    elif m_index is not None and w_index is None:
                        values['c_equip'] = line
                        last = 'c_equip'
                    elif w_index is not None and m_index is None:
                        values['c_warns'] = line
                        last = 'c_warns'
                    else:
                        if m_index < w_index:
                            values['c_equip'] = line[m_index:w_index]
                            values['c_warns'] = line[w_index:]
                            last = 'c_warns'
                        else:
                            values['c_equip'] = line[m_index:]
                            values['c_warns'] = line[w_index:m_index]
                            last = 'c_equip'
            # move foot notes to ingredients, and MAY CONTAIN to warnings
            for fld in ('c_allrgn', 'c_equip', 'c_warns'):
                if '*' in values[fld]:
                    values[fld], tmp = values[fld].split('*', 1)
                    values['c_ingred'] = '%s *%s' % (values['c_ingred'], tmp)
                    values['modified'] = True
                if '+' in values[fld]:
                    values[fld], tmp = values[fld].split('+', 1)
                    values['c_ingred'] = '%s +%s' % (values['c_ingred'], tmp)
                    values['modified'] = True
            for fld in ('c_ingred', 'c_allrgn', 'c_equip'):
                if 'MAY CONTAIN' in values[fld].upper():
                    idx = values[fld].upper().index('MAY CONTAIN')
                    values[fld], may_contain = values[fld][:idx].strip(), values[fld][idx:].upper()
                    values['c_warns'] = ('%s %s' % (values['c_warns'], may_contain)).strip()
                    values['modified'] = True
            return values

        @on_key(KEY_CTRL_S)
        def save_to_dbf(self, values=None, force_save=False):
            """
            ^S=Save
            """
            # called by parse_record with values, and by
            # load_(next|prev)_record with no values
            #
            # if values is None, get data from UI
            if values is None:
                # the load_*_record functions should always save
                force_save = True
                xml_id = self.meta.xml_id
                if not xml_id:
                    logger.debug('aborting save due to empty FIS ID')
                    return
                values = {}
                values['c_source'] = self.initial.value
                values['c_ingred'] = self.ingredients.value
                values['c_allrgn'] = self.allergens.value
                values['c_equip'] = self.equipment.value
                values['c_warns'] = self.warnings.value
            else:
                xml_id = values['xml_id']
            # find matching record, or create a new one
            try:
                rec ,= self.primary_index[xml_id]
            except dbf.NotFoundError:
                # should only happen when loading new data from OpenERP
                # meaning values should contain all data and all fields
                # should be saved
                rec = self.table.append(values)
            else:
                # previous record exists: only save f_* fields if they are empty,
                # and only save c_* fields (except c_source) if force_save is True
                if rec.f_ingred:
                    values.pop('f_ingred', None)
                if rec.f_allrgn:
                    values.pop('f_allrgn', None)
                if rec.f_equip:
                    values.pop('f_equip', None)
                if rec.f_warns:
                    values.pop('f_warns', None)
                if rec.c_source == rec.f_source and not force_save:
                    values.pop('c_ingred')
                    values.pop('c_allrgn')
                    values.pop('c_equip')
                    values.pop('c_warns')
                # at this point, at least c_source is getting saved
                dbf.write(rec, **values)

        @on_key(KEY_CTRL_U)
        def upload_record(self):
            """
            ^U=Upload
            """
            self.on_save_and_publish(xml_id=self.meta.xml_id)
            self.paint()


    app = MyApp()
    app.run()

## helpers

def get_words(*fields):
    words = set()
    for f in fields:
        for w in f.split():
            sub_words = [w.strip(non_alpha).lower()]
            for s in non_alpha:
                if s in sub_words[0]:
                    for w in sub_words.pop(0).split(s):
                        sub_words.append(w.strip(non_alpha).lower())
            else:
                for w in sub_words:
                    words.add(w)
    return words


Run()

