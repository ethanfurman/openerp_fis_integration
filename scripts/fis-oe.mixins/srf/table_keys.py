
table_keys = {
          8: (  8, 'CNVZD0', br'D010(.)'),                        # customer terms
         11: ( 11, 'CNVZas', br'as10(..)'),                       # product category
         27: ( 27, 'CNVZSV', br'SV10(..)'),                       # carrier
         33: ( 33, 'CSMS', br'10(......) '),                      # customer
         34: ( 34, 'CSMSS', br'10(......)1...'),                  # customer ship-to
         35: ( 35, 'RDER2', br'10(......)..0001'),                # open order header ship-to
         36: ( 36, 'RDERH', br'10(......)..0000'),                # open order header master
         37: ( 37, 'RDERD', br'10(......)..1'),                   # open order header detail
         47: ( 47, 'CNVZZ', br'Z(...)'),                          # sales rep
         74: ( 74, 'EMP1', br'10(.....)'),                        # employee
         65: ( 65, 'VNMS', br'10(......)'),                       # purchasers
         97: ( 97, 'CNVZaa', br'aa10(.)'),                        # product location
        135: (135, 'NVTY', br'(......)101000    101\*\*'),        # products
        163: (163, 'POSM', br'10(......)'),                       # vendors
        192: (192, 'CNVZO1', br'O110(......)'),                   # transmitter number
        257: (257, 'CNVZK', br'K(....)'),                         # sales rep
        262: (262, 'ARCI', br'10(......)......'),                 # customer product list
        320: (320, 'IFMS', br'10(..........).....0'),             # product formula
        322: (322, 'IFDT', br'10(..........).....0...'),          # product ingredients
        328: (328, 'IFPP0', br'10(......)000010000'),             # production order formula
        329: (329, 'IFPP1', br'10(......)000011...'),             # production order ingredients
        341: (341, 'CNVZf', br'f10(..)'),                         # production lines

        'arci'  : (262, 'ARCI', br'10(......)......'),            # customer product list
        'cnvzaa': ( 97, 'CNVZaa', br'aa10(.)'),                   # product location
        'cnvzas': ( 11, 'CNVZas', br'as10(..)'),                  # product category
        'cnvzd0': (  8, 'CNVZD0', br'D010(.)'),                   # customer terms
        'cnvzf' : (341, 'CNVZf', br'f10(..)'),                    # production lines
        'cnvzo1': (192, 'CNVZO1', br'O110(......)'),              # transmitter number
        'cnvzsv': ( 27, 'CNVZSV', br'SV10(..)'),                  # carrier
        'cnvzk' : (257, 'CNVZK', br'K(....)'),                    # sales rep
        'cnvzz' : ( 47, 'CNVZZ', br'Z(...)'),                     # sales rep
        'csms'  : ( 33, 'CSMS', br'10(......) '),                 # customer
        'csmss' : ( 34, 'CSMSS', br'10(......)1...'),             # customer ship-to
        'emp1'  : ( 74, 'EMP1', br'10(.....)'),                   # employee
        'ifms'  : (320, 'IFMS', br'10(..........).....0'),        # product formula
        'ifdt'  : (322, 'IFDT', br'10(..........).....0...'),     # product ingredients
        'ifpp0' : (328, 'IFPP0', br'10(......)000010000'),        # production order formula
        'ifpp1' : (329, 'IFPP1', br'10(......)000011...'),        # production order ingredients
        'nvty'  : (135, 'NVTY', br'(......)101000    101\*\*'),   # products
        'posm'  : (163, 'POSM', br'10(......)'),                  # vendors
        'rderd' : ( 37, 'RDERD', br'10(......)..1'),              # open order header detail
        'rderh' : ( 36, 'RDERH', br'10(......)..0000'),           # open order header
        'rder2' : ( 35, 'RDER2', br'10(......)..0001'),           # open order header ship-to
        'vnms'  : ( 65, 'VNMS', br'10(......)'),                  # purchasers
        }

