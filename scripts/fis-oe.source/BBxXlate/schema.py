data = """
FCUBSQ   -DATA DICTIONARY HEADER RECORD MAINT. & I  ( 1 at start)
     1    FILE NAME                                8    A8$
     2    FRWD PNTR                                4    C8 ####
     3    MAX DSC LEN                              2    D8 ##
     4    NO FIELDS                                3    E8 ###
     5    NO COLUMNS                               2    F8 ##
     6    COL 1 POS.                               2    G8 ##
     7    COL 2 POS.                               2    H8 ##
     8    COL 3 POS.                               2    I8 ##
     9    COL 4 POS.                               2    J8 ##
    10    COL 1 LINE NO.                           2    K8 ##
    11    COL 2 LINE NO.                           2    L8 ##
    12    COL 3 LINE NO.                           2    M8 ##
    13    COL 4 LINE NO.                           2    N8 ##
    14    LEN COL 1                                2    O8 ##
    15    LEN COL 2                                2    P8 ##
    16    LEN COL 3                                2    Q8 ##
    17    LEN COL 4                                2    R8 ##
    18    CONTROL PROG.                            6    B8$
    19    EDIT PROG.                               6    C8$
    20    SCN HEADING                             50    D8$
    21    PASSWORD                                 3    E8$
    22    AUDIT IND                                1    F8$
    23    FILE TYPE                                1    N8$
    24    DATE OF LAST CHANGE                      8    T8$(1,8)
    25    ADD/CHG/DEL IND                          1    T8$(9,1)
    26    Access Priority                          2    T8$(10,1) ##
FCUBSQ   -DATA DICTIONARY HEADER RECORD MAINT. & I  ( 2 at start)
     1    FILE NO.                                 3    G8$ ###
     2    FRWD PNTR                                4    S8 ####
     3    BKWD PNTR                                4    T8 ####
     4    FIELD NAME                              30    H8$
     5    FLD LENGTH                               2    U8 ##
     6    KEY IND                                  1    I8$(1,1)
     7    FIELD TYPE                               1    I8$(2,1)
     8    PAD IND                                  1    I8$(3,1)
     9    PRESET IND                               1    I8$(4,1)
    10    SECURITY                                 1    I8$(5,1)
    11    PRECISION IND                            1    I8$(6,1)
    12    CRITICAL(DEL)                            1    I8$(7,1)
    13    EDITING?                                 1    I8$(8,1)
    14    SEP FIELD                                1    I8$(9,1)
    15    NAM/ADR/STD                              1    I8$(10,1)
    16    DATE OR TYPE IND                         1    I8$(11,1)
    17    AUDIT IND                                1    I8$(12,1)
    18    PRESET VALUE                            20    J8$
    19    DELETE VALUE                            10    K8$
    20    VARIABLE NAME                           10    L8$
    21    EDIT MASK                               14    M8$
    22    VLD VALUE(S)                            12    Q8$
    23    DOC CODE                                 6    O8$
    24    VAL TES IND                              1    P8$(1,1)
    25    EDIT FILE                                3    P8$(2,3)
    26    COLUMN #                                 2    C ##
    27    LINE NUMBER                              2    L ##
FCUASQA  -SELECTOR DICTIONARY HEADER RECORD MAINT.  ( 3 at start)
     1    SELECT NAME                              6    Cn$
     2    FRWD PNTR                                4    D0 ####
     3    DESC LENGTH                              2    E0 ##
     4    NO COLUMNS                               1    F0 #
     5    NO SELECTIONS                            2    G0 ##
FCUASQB  -CBS SELECTOR DICTIONARY DTL FILE  ( 4 at start)
     1    SELECT NAME                              6    Mn$
     2    FRWD PNTR                                4    N0 ####
     3    BKWD PNTR                                4    P0 ####
     4    MESSAGE NO.                              2    Q0 ##
     5    MSG PRFX/SUFX                            1    Rn$(1,1)
     6    PRINTER IND                              1    Rn$(2,1) #
     7    S.O.D. IND                               1    Rn$(3,1) #
     8    E.O.D. IND                               1    Rn$(4,1) #
     9    OPEN FILE ID                             1    Rn$(5,1)
    10    SELECT DESCR.                           40    Sn$
    11    MESSAGE P/S                             25    Tn$
    12    OPEN FILE 1:                             6    Un$(1,6)
    13              2:                             6    Un$(7,6)
    14              3:                             6    Un$(13,6)
    15              4:                             6    Un$(19,6)
    16              5:                             6    Un$(25,6)
    17              6:                             6    Un$(31,6)
    18              7:                             6    Un$(37,6)
    19              8:                             6    Un$(43,6)
    20    OPEN FILE 9:                             6    Un$(49,6)
    21             10:                             6    Un$(55,6)
    22             11:                             6    Un$(61,6)
    23             12:                             6    Un$(67,6)
    24             13:                             6    Un$(73,6)
    25             14:                             6    Un$(79,6)
    26             15:                             6    Un$(85,6)
    27             16:                             6    Un$(91,6)
    28    RUN PROGRAM                              6    Vn$
    29    SYS PARM CD                              1    Wn$(1,1)
    30    (open)                                   1    Wn$(2,1)
    31    (open)                                   1    Wn$(3,1)
    32    Jobstream Eligible                       1    Wn$(4,1)
    33    Non-Disp(X),Title(T)                     1    Wn$(5,1)
    34    Access Priority                          2    Wn$(6,2) ##
    35    (open)                                   1    Wn$(8,1)
    36    (open)                                   2    Wn$(9,2)
    37    Pass Paramater                           2    Gn$
    38    Report Program Name                      6    Jn$
    39    Sel Docum Code                           6    Yn$
    40    Password                                 3    Zn$
    41    Data Ent Ldmod                          18    An$
    42    Number of Pages                          4    Z0 ####
FCCNVZ** -COMPANY MASTER FILE  ( 5 at start)
     1    KEY                                      2    A0$(1,2)
     2    COMPANY CODE                             2    A0$(3,2)
     3    FILLER                                   3    A0$(5,3)
     4    PASSWORD                                 3    BN$
     5    COMPANY NAME                            40    CN$
     6    GENERAL LEDGER (1=Y,0=N)                 1    Dn$(1,1)
     7    CHECK RECONC (1=Y,0=N)                   1    Dn$(2,1)
     8    CASH(1) OR ACCRUAL(0) BASIS              1    Dn$(3.1)
     9    POST DIRECT TO G/L HIST(1=Y,0)           1    Dn$(4,1)
    10    POST TO G/L MONTHLY(1=Y,0=DLY)           1    Dn$(5,1)
    11    (open)                                   5    Dn$(6,5)
    12                                             1    EN$
    13    (open)                                   1    Fn$
    14    Number of Printers                       2    GN ##
    15    Printer 1 ID                             2    Hn$(1,2)
    16    Printer 1 Centering (4 or 2)             1    Hn$(3,1)
    17    Printer 2 ID                             2    In$(1,2)
    18    Printer 2 Centering (4 or 2)             1    In$(3,1)
    19    Printer 3 ID                             2    In$(4,2)
    20    Printer 3 Centering (4 or 2)             1    In$(6,1)
    21    Printer 4 ID                             2    In$(7,2)
    22    Printer 4 Centering                      1    In$(9,1)
    23    Printer 5 ID                             2    In$(10,2)
    24    Printer 5 Centering                      1    In$(12,1)
    25    Printer 6 ID                             2    In$(13,2)
    26    Printer 6 Centering                      1    In$(15,1)
    27    Printer 7 ID                             2    In$(16,2)
    28    Printer 7 Centering                      1    In$(18,1)
    29    Printer 8 ID                             2    In$(19,2)
    30    Printer 8 Centering                      1    In$(21,1)
    31    Printer 9 ID                             2    In$(22,2)
    32    (open)                                   1    In$(24,1)
    33    Export File Directory                   25    Jn$
    34    MUL TSK DSABLE                           1    KN$(1,1)
    35    (open)                                   5
FCCNVZF  -DATA FILE INFORMATION RECORDS  ( 6 at start)
     1    Key Group ='F'                           1    AN$(1,1)
     2    File Name                                8    An$(2,8)
     3    Key Size                                 2    BN ##
     4    Number of Records                        7    CN #######
     5    Record Size                              5    DN #####
     6    Disk Number                              1    EN #
     7    Starting Sector No                       5    FN #####
     8    File Description                        40    GN$
     9    Temporary or Permanent                   1    HN$
    10    Key Consists of                         50    IN$
    11    File Number                              3    JN ###
    12    Field No of Description                  2    Kn$(1,2)
    13    Start pos of CODE in key                 3    Kn$(3,3)
    14    End pos of CODE in key                   3    Kn$(6,3)
    15    (open)                                   2    Kn$(9,2)
    16    HTA of Q0$ string                       40    Ln$
    17    HTA of Q8$ string                       40    Mn$
    18    (open)                                   1    Nn$
FCCNVZ*G0-PERIOD-END CONTROL FILE  ( 7 at start)
     1    Key Type = '*G0'                         3    An$(1,3)
     2    Company Code                             2    An$(4,2)
     3    Curr Yr Income                          11    Bn ########.00
     4    Last Period Closed                       2    Cn ##
     5    Last Quarter Closed                      2    Dn ##
     6    Y/E Closing Flag                         1    En #
     7    Current Period                           2    Fn ##
     8    Trans Seq                                4    Nn ####
     9    Close Per 01                             6    C(1) ######
    10    Close Per 02                             6    C(2) ######
    11    Close Per 03                             6    C(3) ######
    12    Close Per 04                             6    C(4) ######
    13    Close Per 05                             6    C(5) ######
    14    Close Per 06                             6    C(6) ######
    15    Close Per 07                             6    C(7) ######
    16    Close Per 08                             6    C(8) ######
    17    Close Per 09                             6    C(9) ######
    18    Close Per 10                             6    C(10) ######
    19    Close Per 11                             6    C(11) ######
    20    Close Per 12                             6    C(12) ######
    21    Close Per 13                             6    C(13)
    22    Close Per 14                             6    C(14)
    23    Close Per 15                             6    C(15)
    24    Close Per 16                             6    C(16)
    25    Close Per 17                             6    C(17)
    26    Close Per 18                             6    C(18)
    27    Close Per 19                             6    C(19)
    28    Close Per 20                             6    C(20)
    29    Close Per 21                             6    C(21)
    30    Close Per 22                             6    C(22)
    31    Close Per 23                             6    C(23)
    32    Close Per 24                             6    C(24)
    33    (open)                                   1    Rn$
    34    (open)                                   1    Dn$
FCCNVZD0 -Customer Payment Terms Codes  ( 8 at start)
     1    Key Group = 'D0'                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Terms Code                               1    An$(5,1)
     4    Terms Description                       25    Bn$
     5    Discount: Number of Days                 3    An ###
     6    Discount: percentage                     4    Bn ##.0
     7    Ageing: Number of Days                   3    Cn ###
     8    Future Ageing (Y/N)                      1    Cn$
     9    Futures: No days til current             3    Dn ###
FCCNVZ^  -G/L INTERFACE RECORDS GENERAL FORMAT (^A  ( 9 at start)
     1    KEY TYPE = ^                             1    Zn$(1,1)
     2    CONTROL KEY                              1    Zn$(2,1)
     3    COMPANY CODE                             2    Zn$(3,2)
     4    NO. ENTRIES                              2    An ##
     5    JOURNAL NO.                              5    An$
     6    ACCOUNT 01                               6    Bn$
     7    ACCOUNT 02                               6    Cn$
     8    ACCOUNT 03                               6    Dn$
     9    ACCOUNT 04                               6    En$
    10    ACCOUNT 05                               6    Fn$
    11    ACCOUNT 06                               6    Gn$
    12    ACCOUNT 07                               6    Hn$
    13    ACCOUNT 08                               6    In$
    14    ACCOUNT 09                               6    Jn$
    15    ACCOUNT 10                               6    Kn$
    16    ACCOUNT 11                               6    Ln$
    17    ACCOUNT 12                               6    Mn$
    18    CR/DR MASK 1                             6    Nn$
    19    CR/DR MASK 2                             6    On$
FCCNVZ^A -G/L CONTROL RECORD - ACCOUNTS RECEIVABLE  ( 10 at start)
     1    Key Type = '^A'                          2    Zn$(1,2)
     2    COMPANY CODE                             2    Zn$(3,2)
     3    NO. ENTRIES                              2    An ##
     4    Journal No                               5    An$
     5    A/R Account                             11    Bn$
     6    A/R ACCT (NON-TRADE)                     4    Cn$
     7    SPLIT CASE CHARGES                      11    Dn$
     8    (OPEN)                                   4    En$
     9    Sales Tax Account                       11    Fn$
    10    Misc Charges Account                    11    Gn$
    11    Cash Account                            11    Hn$
    12    Discounts Taken Account                 11    In$
    13    Unapplied Cash Account                  11    Jn$
    14    Service Charges Account                 11    Kn$
    15    Promotion Allowance Account             11    Ln$
    16    Spoilage Allowance                      11    Mn$
FCCNVZas -SALES CATEGORY MASTER  ( 11 at start)
     1    KEY TYPE = as                            2    AN$(1,2)
     2    COMPANY                                  2    AN$(3,2)
     3    Sales Category Code                      2    An$(5,2)
     4    (open)                                   8    Bn$(8,1)
     5    Non Movement Rpt?                        1    Bn$(9,1)
     6    Allow Sales?                             1    Bn$(10,1)
     7    Physical I/C?                            1    Bn$(11,1)
     8    Valuation Report?                        1    Bn$(12,1)
     9    Description                             20    CN$
    10    Gross Margin Except % - Low              5    DN ##.00
    11    Gross Margin Except % - High             5    En ##.00
    12    MONTHS SHELF LIFE                        2    FN
FCOPERT  -Teminal Control Records  ( 12 at start)
     1    Key Group = 'T'                          1    An$(1,1)
     2    Terminal ID                              4    An$(2,4)
     3    Location / Description                  30    Bn$
     4    (open)                                   1    Cn$
     5    Batch Number                             4    Dn$ ####
     6    Initial Selector Number                  2    En$ ##
     7    Valid Selectors (Blank)=all             20    Fn$
FCCNVZ^O -G/L CONTROL RECORD - A/P PAYMENT DISTRIBUTION  ( 13 at start)
     1    KEY ="^O"                                2    Zn$(1,2)
     2    COMPANY CODE                             2    Zn$(3,2)
     3    NO. ENTRIES                              2    An ##
     4    JOURNAL NO.                              5    An$
     5    A/P ACCT - OTHER (DR)                   11    Bn$
     6    A/P ACCT - PURCH'S (DR)                 11    Cn$
     7    NET ACCT (CR)                           11    Dn$
     8    DISCOUNT ACCT (CR)                      11    En$
     9    DR/CR MASK 1                             8    Fn$
FCCNVZ^I0-G/L INTERFACE RECORD - INVENTORY  ( 14 at start)
     1    Key Type = "^I0"                         3    A$(1,3)
     2    Company Code                             2    A$(4,2)
     3    (open)                                   1    An #
     4    Journal Number                           5    An$
     5    Inventory Account                       11    Bn$
     6    Cost of Goods Account                   11    Cn$
     7    Physical Variance Account               11    Dn$
     8    A/P Suspense Account                    11    En$
     9    Freight Account                         11    Fn$
    10    Handling Account                        11    Gn$
    11    (open)                                   1    Hn$
    12    Whse Xfer Variance Account              11    In$
    13    Production Variance Account             11    Jn$
    14    Overlay Position of Whse                 2    Kn$ ##
    15    Whse Number of Chars                     2    Ln$ ##
    16    Overlay Pos of Sales Catg                2    Mn$ ##
    17    Sales Catg No of Chars                   2    Nn$ ##
FCCNVZ^N -G/L CONTROL RECORD - A/P PAYABLE DISTRIBUTION  ( 15 at start)
     1    KEY = "^N"                               2    Zn$(1,2)
     2    COMPANY CODE                             2    Zn$(3,2)
     3    NO. ENTRIES                              2    An ##
     4    JOURNAL NO.                              5    An$
     5    COST OF GOODS - PURCHASES (DR)          11    Bn$
     6    SALES TAX ACCT (CR)                     11    Cn$
     7    FREIGHT ACCT (CR)                       11    Dn$
     8    A/P - OTHER (CR)                        11    En$
     9    A/P - PURCHASES (CR)                    11    Fn$
    10    DR/CR MASK 1                             6    Gn$
FCCNVZaw -I/C WAREHOUSE CATEGORY MASTER MAINT. & INQUIRY  ( 16 at start)
     1    KEY TYPE = aw                            2    An$(1,2)
     2    COMPANY                                  2    An$(3,2)
     3    CODE                                     1    An$(5,1)
     4    (open)                                   1    Bn$
     5    DESCRIPTION                             20    Cn$
FCCNVZ8  -G/L INTERFACE - NCR INVOICING CONTROL RECORD  ( 17 at start)
     1    KEYTYPE = "^C"                           2    A$(1,2)
     2    COMPANY CODE                             2    A$(3,2)
     3    OPEN                                     1    An #
     4    JOURNAL NUMBER                           5    B$
     5    NET A/R (TRADE)                         11    C$
     6    NET A/R (NON-TRADE)                     11    D$
     7    GROSS A/R ACCOUNT                       11    E$
     8    TRADE DISCOUNT ACCOUNT                  11    F$
     9    CASH DISCOUNT ACCOUNT                   11    G$
    10    SALES TAX ACCOUNT                       11    H$
    11    COST OF SALES ACCOUNT (DEBIT)           11    I$
    12    INVENTORY ACCOUNT (CREDIT)              11    J$
    13    OPEN                                     1    K$
    14    OPEN                                     1    L$
FCCNVZ^B -G/L Interface Record - Invoicing  ( 18 at start)
     1    Key type = '^B'                          2    Zn$(1,2)
     2    Company Code                             2    Zn$(3,2)
     3    (open)                                   1    An #
     4    Journal Number                           5    An$
     5    Net A/R (trade)                         11    Bn$
     6    Net A/R (non-trade)                     11    Cn$
     7    Gross Sales                             11    Dn$
     8    Trade Discount Account                  11    En$
     9    Cash Discount Account                   11    Fn$
    10    Sales Tax Account                       11    Gn$
    11    Cost of Sales (DR)                      11    Hn$
    12    Inventory (CR)                          11    In$
    13    Azz Add-on Sales Acct                   11    Jn$
    14    Service Charges                         11    Kn$
    15    CRV Account (CR)                        11    Ln$
    16    Fuel Surcharge Acct                     11    Mn$
FCOPER   -Operator Codes Master File  ( 19 at start)
     1    Key Group = 'O'                          1    AN$(1,1)
     2    Operator Code                            3    AN$(2,3)
     3    Operator Name                           30    BN$
     4    Default Company Code                     2    Cn$(1,2)
     5    Installation Code                        1    Cn$(3,1)
     6    Access Priority                          2    Cn$(4,2) ##
     7    Message Flag                             1    Cn$(5,1)
     8    Initial Selector Number                  2    Dn$ ##
     9    Valid Selectors (Blank=all)             40    En$
    10    Message Name                             8    Fn$
    11    Message Group                            8    Gn$
    12    Linux user/email ID                     30
FCCNVZ"  -REPORT HEADING RECORD (GENERAL FORMAT)  ( 20 at start)
     1    Key Group = ' '                          1    AN$(1,1)
     2    Program Name                             6    AN$(2,6)
     3    Report Heading                          50    BN$
     4    Report Frequency                         1    DN$
     5    Files Used                              40    EN$
     6    Documentation Code                      12    CN$
     7    Report Width                             3    DN ###
     8    Number of Copies                         2    En ##
     9    Special Form (Y/N)                       1    Fn$(1,1)
    10    (open)                                   1    Fn$(2,1)
    11    Form Name                               12    Gn$
FCCNVZRB -Picking Exception Reason Codes  ( 21 at start)
     1    Key Type = 'RB'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Reason Code                              2    An$(5,2)
     4    Reason Description                      20    Bn$
FCCNVZM  -STANDARD MESSAGE MAINT & INQUIRY  ( 22 at start)
     1    Key Group = 'M'                          1    A7$(1,1)
     2    MESSAGE NO.                              2    A7$(2,2) ##
     3    Y/N INDICATOR                            1    B7$
     4    MESSAGE                                 60    C7$
     5    NEXT MSG NO.                             2    A7 ##
FCCNVZC  -COMPANY INFORMATION RECORDS  ( 23 at start)
     1    Key Group = 'C'                          1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Standard Warehouse                       4    Bn$(1,4)
     4    Inventory Costing Method                 1    Bn$(5,1) #
     5    INVENTORY COSTING - SALES                1    Bn$(6,1)
     6    (open)                                   1    Bn$(7,1)
     7    INVENTORY HISTORY (S/D/N=NO)             1    Bn$(8,1)
     8    (open)                                   2    Bn$(9,2)
     9    COMPANY NAME                            30    Cn$
    10    (open)                                   1    An
    11    (open)                                   1    Bn #
    12    NEXT INVOICE NO.                         6    Cn ######
    13    NEXT P/O NO.                             6    Dn ######
    14    Next A/R Adjustment No                   6    En ######
    15    Next A/P Adjustment No                   6    Fn ######
    16    NEXT CR MEMO NO.                         6    H8 ######
    17    NEXT DR MEMO NO.                         6    I8 ######
    18    NEXT STK REC NO.                         6    J8 ######
    19    (open)                                   1    K8
    20    (open)                                   1    L8
    21    (open)                                   1    M8
    22    (open)                                   1    N8 #
    23    Maximum A/P Check Amount                10    PN ##########
    24    NEXT I/C ADJ NO.                         6    Q8 ######
    25    (open)                                   1    RN #
FCCNVZK  -SALES CATEGORY BREAK DESCRIPTIONS  ( 24 at start)
     1    KEY TYPE = "K"                           1    AN$(1,1)
     2    COMPANY CODE                             2    AN$(2,2)
     3    HIGHEST ITEM NUMBER                      6    AN$(4,6)
     4    DESCRIPTION                             30    BN$
     5    CATEGORY CODE                            2    CN$
     6    OPEN                                     1    DN$
     7    OPEN                                     1    EN
FCCNVZX  -PRICING TYPE MAINT/INQUIRY  ( 25 at start)
     1    KEY GROUP = "X"                          1    A8$(1,1)
     2    COMPANY                                  2    A8$(2,2)
     3    PRICING TYPE                             2    AN$(4,2)
     4    DECSCRIPTION                            30    BN$
FCCNVZT  -TAXING AUTHORITY MASTER FILE MAINTENANCE  ( 26 at start)
     1    Key Type = 'T'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Tax Auth Code                            2    An$(4,2)
     4    Description                             30    Bn$
     5    (open)                                   1    Cn$
     6    (open)                                   1    Dn$
     7    Tax Percent                              5    En ##.00
     8    MTD - Taxable Sales                     10     #######.00
     9        - Non-Taxable Sales                 10     #######.00
    10        - Sales Tax Amount                  10     #######.00
    11    YTD - Taxable Sales                     11     ########.00
    12        - Non-Taxable Sales                 11     ########.00
    13        - Sales Tax Amount                  11     ########.00
FCCNVZSV -CARRIER (SHIP VIA) MASTER FILE MAINTENANCE/INQUIRY  ( 27 at start)
     1    Key Type = "SV"                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Carrier Code                             2    An$(5,2)
     4    Description/Name                        30    Bn$
     5    Address Line 1                          30    Cn$
     6    Address Line 2                          30    Dn$
     7    Address Line 3                          30    En$
     8    Telephone Number                        10    Fn$
     9    Fuel Surcharge? (Y/N)                    1    Gn$
FCCNVZU  -CUSTOMER TYPE MASTER FILE MAINTENANCE &   ( 28 at start)
     1    Key Type = 'U'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Customer Type                            2    An$(4,2)
     4    Description                             30    Bn$
     5    G/L Department                           3    Cn$
     6    Distributor? (Y/N)                       1    Dn$
FCCNVZ*G1-GENERAL LEDGER CONTROL RECORD  ( 29 at start)
     1    KEY GROUP = '*G1'                        3    An$(1,3)
     2    COMPANY CODE                             2    An$(4,2)
     3    CURRENT INCOME                          12    Bn #########.00
     4    CURR YR INC ACCT                         6    Rn$
     5    STATUS-TRIAL BALANCE                     1    Dn$(1,1)
     6          -DETAIL REPORT                     1    Dn$(2,1)
     7          -UPDATE                            1    Dn$(3,1)
     8          -INC STMT                          1    Dn$(4,1)
     9          -BAL SHEET                         1    Dn$(5,1)
    10          -BUDGET                            1    Dn$(6,1)
    11    FISCAL YEAR (YY)                         2    Dn$(7,2)
    12    ACCOUNT TYPE                             1    Dn$(9,1)
    13    (OPEN)                                   1    Dn$(10,1)
FCCNVZP2 -Quantity Discount Table  ( 30 at start)
     1    Key Type = "P2"                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Discount Table Code                      2    An$(5,2)
     4    Description                             30    Bn$
     5    Amt off,Pct,Net Price($,%,N)             1    Bn$(1,1)
     6    (open)                                   2    Bn$(2,4)
     7    Min Qty for Best Discount                5    M(1) ##.00
     8    Min Qty for 2nd Best Discount            5    M(2) #####
     9    Min Qty for 3rd Best Discount            5    M(3) #####
    10    Min Qty for 4th Best Discount            5    M(4) #####
    11    Min Qty for 5th Best Discount            5    M(5) #####
    12    Min Qty for 6th Best Discount            5    M(5)) #####
    13    Min Qty for 7th Best Discount            5    M(7) #####
    14    Min Qty for 8th Best Discount            5    M(8) #####
    15    Best Discount $/% Amt                    9    D(1) #####.00#
    16    2nd Best Dist $/% Amt                    9    D(2) ####.00##
    17    3rd Best Disc $/% Amt                    9    D(3) ####.00##
    18    4th Best Disc $/% Amt                    9    D(4) ####.00##
    19    5th Best Disc $/% Amt                    9    D(5) ####.00##
    20    6th Best Disc $/% Amt                    9    D(6) ####.00##
    21    7th Best Disc $/% Amt                    9    D(7) ####.00##
    22    8th Best Disc $/% Amt                    9    D(8) ####.00##
FCCNVZL  -MASTER FILE LINKAGES---ALA EZ  ( 31 at start)
     1    KEY GROUP = 'L'                          1    AN$(1,1)
     2    From File Number                         3    AN$(2,3)
     3    To File Number                           3    AN$(5,3)
     4    From File Name                           8    BN$
     5    To File Name                             8    CN$
     6    Key String for WP & ML                  40    DN$
     7    String Length                            2    EN ##
     8    Description                             40    FN$
     9    Verify String                           55    GN$
    10    Display Field NO                         2    HN ##
FCCNVZV  -CONSTRUCTED VARIABLES  ( 32 at start)
     1    KEY GROUP = 'V'                          1    AN$(1,1)
     2    FROM FILE #                              3    AN$(2,3)
     3    NAME                                     2    AN$(5,2)
     4    FROM FILE NAME                           6    BN$
     5    OPEN                                     1    CN$
     6    KEY STRG(VARS & LITS)                   40    DN$
     7    STRING LENGTH                            2    EN ##
     8    DESCRIPTION                             40    FN$
FCCSMS   -CUSTOMER MASTER FILE - BASIC RECORD  ( 33 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER NO.                             6    An$(3,6)
     3    RECORD TYPE                              1    An$(9,1)
     4    NAME                                    30    Bn$
     5    ADDR LINE 1                             30    Cn$
     6    ADDR LINE 2                             30    Dn$
     7    ADDR LINE 3                             30    En$
     8    ZIP CODE                                10    LN$
     9    Contract Prices?                         1    Fn$(1,1)
    10    Price List Code                          1    Fn$(2,1)
    11    SRP Code                                 1    Fn$(3,1)
    12    Credit Status                            1    Fn$(4,1)
    13    C/R TO OTH CUST?                         1    Fn$(5,1)
    14    STATEMENT IND                            1    Fn$(6,1)
    15    DELINQ'CY IND                            1    Fn$(7,1)
    16    Catalog Category                         1    Fn$(8,1)
    17    BACK ORD IND                             1    Fn$(9,1)
    18    Link to Ship-to                          1    Fn$(10,1)
    19    State Code                               2    Fn$(11,2)
    20    # Extra Labels                           1    Fn$(13,1) #
    21    P/A Eligible?                            1    Fn$(14,1)
    22    Rebate category code(sp=none)            1    Fn$(15,1)
    23    Price Chg Days Notice                    3    Fn$(16,3) ###
    24    BOL Required?                            1    Fn$(19,1)
    25    (open)                                   2    Fn$(19,2)
    26    INVOICE BALANCE                          9    Bn ######.00
    27    UNAPPLIED CASH BAL                       9    Cn ######.00
    28    CR MEMO BALANCE                          9    Dn ######.00
    29    DR MEMO BALANCE                          9    En ######.00
    30    CREDIT LIMIT                             6    Fn ######
    31    LARGST BALANCE                           6    Gn ######
    32    OUTSTAND ORDERS                          9    Hn ######.00
    33    M-T-D SALES                              6    In ######
    34    M-T-D COST                               6    Jn ######
    35    PREV MONTH A/R                           6    Kn ######
    36    Y-T-D SALES                             10    Ln #######.00
    37    Y-T-D COST                               7    Mn #######
    38    Y-T-D CREDITS                            7    Nn #######
    39    YTD Payments                             7    On #######
    40    Prev Year Sales                          8    Pn ########
    41    Taxing Authority Code                    2    Qn$
    42    Broker Code                              3    Gn$(1,3)
    43    Salesrep Code                            3    Gn$(4,3)
    44    Date Largest Balance                     6    Gn$(7,6)
    45    Date Last Payment                        6    Gn$(13,6)
    46    Payment terms code                       1    Gn$(19,1)
    47    Telephone Number                        10    Gn$(20,10)
    48    Service Charge Code                      1    Gn$(30,1)
    49    Date Added                               6    Gn$(31,6)
    50    Prod Sls Rpt?                            1    Gn$(37,1)
    51    Bulk Customer Type                       2    Gn$(38,2)
    52    Update S/A?                              1    GN$(40,1)
    53    Last PC Notice                           6    Gn$(41,6)
    54    Customer Type Code                       2    Hn$(1,2)
    55    Sales Class Code                         4    Hn$(3,4)
    56    Pricing Method                           2    Hn$(7,2)
    57    Reseller Number                         14    Hn$(9,14)
    58    Fuel Surcharge                           6    Hn$(23,6) ###.00
    59    Bulk Invc in LBS?                        1    Hn$(29,1)
    60    available                                1    Hn$(30,1)
    61    ExpireDt on Docs                         1    Hn$(31,1)
    62    Alpha Sort Key                           8    In$
    63    Accntg Comments                         40    Jn$
    64    Acctg Contact                           30    Kn$
    65    Total Number Invoices                    5    Qn #####
    66    Total Payment Days                       5    Rn #####
    67    Customer Rank                            3    Sn ###
FCCSMSS  -CUSTOMER MASTER FILE - ADDTN'L SHIP-TO'S  ( 34 at start)
     1    COMPANY                                  2    An$(1,2)
     2    CUSTOMER NUMBER                          6    An$(3,6)
     3    RECORD TYPE = "1"                        1    An$(9,1)
     4    SHIP TO NUMBER                           4    An$(10,4)
     5    SHIP TO NAME                            30    Bn$
     6    ADDRESS LINE 1                          30    Cn$
     7    ADDRESS LINE 2                          30    Dn$
     8    ADDRESS LINE 3                          30    En$
     9    ZIPCODE                                 10    Ln$
    10    (open) - do not use                      5    Fn$(1,5)
    11    MSI customer (Y/N)?                      1    Fn$(6,1)
    12    Price List Code                          1    Fn$(7,1)
    13    (open)                                   1    Fn$(8,1)
    14    ORD PRINT MSG                            2    FN$(9,2)
    15    INV PRINT MSG                            2    FN$(11,2)
    16    OPER MESSAGE                             2    FN$(13,2)
    17    CONTACT FREQUENCY                        1    Fn$(15,1)
    18    Pick Prior(1-9)                          1    Fn$(16,1)
    19    Day Contacted                            1    Fn$(17,1)
    20    Last Ord Dt                              6    Fn$(18,6)
    21    Last Inv Dt                              6    Fn$(24,6)
    22    Service Days                             5    Fn$(30,5)
    23    # Holiday Gifts                          1    Fn$(35,1) #
    24    Last Ord No                              6    Fn$(36,6)
    25    Last Inv No                              6    Fn$(42,6)
    26    Service Rep                              3    Fn$(48,3)
    27    WAREHOUSE                                4    Fn$(51,4)
    28    Salesrep Code                            3    Fn$(55,3)
    29    Route code                               3    Fn$(58,3)
    30    Stop Number                              3    Fn$(61,3) ###
    31    TAX AUTH                                 2    Fn$(64,2)
    32    Territory Code                           3    Fn$(66,3)
    33    SOURCE CODE                              2    Fn$(68,2)
    34    Velocity Rpt(Y/N)                        1    Fn$(71,1)
    35    Catalog Category                         1    Fn$(72,1)
    36    # Extra Labels                           1    Fn$(73,1) #
    37    Terms Code                               1    Fn$(74,1)
    38    BUILD-UP ITEMS?                          1    Fn$(75,1)
    39    DELIVERY DAYS                            3    FN$(76,3)
    40    Telephone No                            10    Fn$(79,10)
    41    Key Account Code                         6    Fn$(89,6)
    42    PPD/Collect (P/C)                        1    Fn$(95,1)
    43    S/A Category                             2    Fn$(96,2)
    44    Price Labels (Y/N)?                      1    Fn$(98,1)
    45    P/A Elg? (sp/N)                          1    Fn$(99,1)
    46    Price Labels Title 1                     6    Fn$(100,6)
    47    Price Labels Title 2                     6    Fn$(106,6)
    48    Order Days                               5    Fn$(112,5)
    49    Case Labels? (Y/N)                       1    Fn$(117,1)
    50    Contract Prices? (Y/N)                   1    Fn$(118,1)
    51    Carrier Code                             2    Fn$(119,2)
    52    Broker Code                              3    Fn$(121,3)
    53    TEMP A/R $                               8    Bn #####.00
    54    ORDER FREQUENCY                          2    Cn ##
    55    Min Order $ Amt                          6    Dn ######
    56    WEIGHT LAST ORDER                        7    En #######
    57    TTL ORDER WEIGHT                         8    Fn ########
    58    TOTAL # ORDERS                           3    Gn ###
    59    Off Inv Disc %                           6    Hn ##.00#
    60    Maximum Order Amount                     6    In ######
    61    Inv Svc Chg %                            5    Jn ###.0
    62    Spoilage Allowance                       5    Kn #.00#
    63    (open)                                   1    Ln #
    64    (open)                                   1    Mn #
    65    (open)                                   1    Nn #
    66    (open)                                   1    On #
    67    (open)                                   1    Pn #
    68    Sales Contact                           40    Qn$
    69    Delivery Instr.                         57    Gn$
    70    Fax Number                              10    Rn$(1,10)
    71    Bulk Cust Type                           2    Rn$(11,2)
    72    Route Code 2                             3    Rn$(13,3)
    73    Route Code 3                             3    Rn$(16,3)
    74    Route Code 4                             3    Rn$(19,3)
    75    Route Code 5                             3    Rn$(22,3)
    76    Stop Number 2                            3    Rn$(25,3) ###
    77    Stop Number 3                            3    Rn$(28,3) ###
    78    Stop Number 4                            3    Rn$(31,3) ###
    79    Stop Number 5                            3    Rn$(34,3) ###
    80    Prod Sls Rpt?                            1    Rn$(37,1)
FCRDER2  -OPEN ORDER HEADER PART II - SHIP-TO INFO  ( 35 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    ORDER NO.                                6    An$(3,6)
     3    RELEASE NO.                              2    An$(9,2)
     4    TYPE = "0001"                            4    An$(11,4)
     5    (OPEN)                                   1    An
     6    (OPEN)                                   1    Bn
     7    (OPEN)                                   1    Bn$
     8    (OPEN)                                   1    Cn$
     9    (OPEN)                                   1    Dn$
    10    (OPEN)                                   1    En$
    11    (OPEN)                                   1    Fn$
    12    SHIP-TO NAME                            30    Gn$
    13    ADDRESS 1                               30    Hn$
    14    ADDRESS 2                               30    In$
    15    ADDRESS 3                               30    Jn$
    16    (OPEN)                                   1    Kn$
    17    (OPEN)                                   1    Ln$
    18    (OPEN)                                   1    Mn$
    19    (OPEN)                                   1    Nn$
    20    (OPEN)                                   1    On$
    21    (OPEN)                                   1    Pn$
    22    (OPEN)                                   1    Qn$
    23    (OPEN)                                   1    Rn$
    24    (OPEN)                                   1    S(0)
    25    (OPEN)                                   1    S(1)
    26    (OPEN)                                   1    S(2)
    27    (OPEN)                                   1    S(3)
    28    (OPEN)                                   1    S(4)
    29    (OPEN)                                   1    S(5)
    30    (OPEN)                                   1    S(6)
    31    (OPEN)                                   1    S(7)
    32    (OPEN)                                   1    S(8)
    33    (OPEN)                                   1    S(9)
    34    (OPEN)                                   1    S(10)
    35    (OPEN)                                   1    Tn$
    36    (OPEN)                                   1    Un$
    37    (OPEN)                                   1    Vn$
    38    (OPEN)                                   1    Wn$
    39    (OPEN)                                   1    Xn$
    40    (OPEN)                                   1    Yn$
    41    (OPEN)                                   1    Zn$
FCRDERH  -OPEN ORDER HEADER MAINTENANCE & INQUIRY  ( 36 at start)
     1    Company Code                             2    AN$(1,2)
     2    Order No                                 6    An$(3,6)
     3    Release No                               2    AN$(9,2)
     4    TYPE = '0000'                            4    AN$(11,4)
     5    FWD PTR                                  5    AN #####
     6    INDEX                                    5    BN #####
     7    Customer No                              6    BN$
     8    Customer Name                           30    CN$
     9    Address 1                               30    DN$
    10    Address 2                               30    EN$
    11    Address 3                               30    FN$
    12    PICK START/END YYMMDDHHMM               20    GN$
    13    (OPEN)                                   1    HN$
    14    (OPEN)                                   1    IN$
    15    (OPEN)                                   1    JN$
    16    Booking Flag                             1    KN$(1,1)
    17    Confirmed Flag                           1    KN$(2,1)
    18    Ord Print Flag                           1    KN$(3,1)
    19    Invoice Flag                             1    KN$(4,1)
    20    CREDLIM FLAG                             1    KN$(5,1)
    21    Pick List Printed (Y/N)                  1    KN$(6,1)
    22    Customer Taxable Wholesale               1    Kn$(7,1)
    23    Add Back to Inventory                    1    Kn$(8,1)
    24    Hold Release Flag                        1    Kn$(9,1)
    25    Taxing Authority Code                    2    KN$(10,2)
    26    Ship-to Code                             4    Kn$(12,4)
    27    Sales Rep Code                           3    KN$(16,3)
    28    Order Source Code                        1    Kn$(19,1)
    29    Ppd/Collect                              1    Kn$(20,1)
    30    Terms Code                               1    KN$(21,1)
    31    ZIP CODE                                 9    KN$(22,9)
    32    Warehouse Code                           4    KN$(31,4)
    33    QTY EXCEEDED                             1    KN$(35,1)
    34    PRICING STATUS                           1    KN$(36,1)
    35    Entry Type                               1    KN$(37,1)
    36    Operator ID                              3    KN$(38,3)
    37    Route Code                               3    Kn$(41,3)
    38    Stop Code                                3    Kn$(44,3)
    39    Territory Code                           3    Kn$(47,3)
    40    Velocity Report (Y/N)                    1    Kn$(50,1)
    41    Pick Priority (1-9)                      1    Kn$(51,1)
    42    Cust Price Label Format                  1    Kn$(52,1)
    43    Released to Pick (Y/N/H) ?               1    Kn$(53,1)
    44    Pick Tags Printed (Y/N/P)                1    Kn$(54,1)
    45    Allocation Done (Y/H/P)                  1    Kn$(55,1)
    46    Price Tags Printed (Y/N/H)               1    Kn$(56,1)
    47    Price List & SRP List                    2    Kn$(57,2)
    48    Freight Zone for Pricing (0-9)           1    Kn$(59,1)
    49    Special Cust(CPP) Y/N                    1    Kn$(60,1)
    50    Editted (Y/N)                            1    Kn$(61,1)
    51    Linked (Y/N)                             1    Kn$(62,1)
    52    DM/CM Reason Code                        2    Kn$(63,2)
    53    OK to combine w/other orders             1    Kn$(65,1)
    54    Below Min Order (Y=Yes,sp=No)            1    Kn$(66,1)
    55    Promos elligible(sp=yes,N=No)            1    Kn$(67,1)
    56    (open)                                   2    Kn$(68,2)
    57    Update S/A?                              1    Kn$(70,1)
    58    Ordered By                               2    Kn$(71,2)
    59    Operator - Void                          3    Kn$(73,3)
    60    Carrier Code                             2    Kn$(76,2)
    61    (open)                                   3    Kn$(78,3)
    62    BOL Number                               6    Kn$(81,6)
    63    (open)                                   4    Kn$(87,4)
    64    Customer P.O. No.                       10    Ln$
    65    Order Date                               6    MN$(1,6)
    66    Ship Date                                6    MN$(7,6)
    67    Invoice Date                             6    MN$(13,6)
    68    Date Confirmed                           6    MN$(19,6)
    69    Date Wanted                              6    MN$(25,6)
    70    ORD PRT MSG                              2    MN$(31,2)
    71    INV PRT MSG                              2    MN$(33,2)
    72    Pricing 'as of' Date                     6    Mn$(35,6)
    73    Cust Price Label Titles                 12    Nn$
    74    Delivery Instructions                   60    ON$
    75    Phone Number                            10    Pn$
    76    Terms Description                       20    QN$
    77    Off Invoice Disc %                       6    RN$ ##.00#
    78    Number of Lines                          3    T(0) ###
    79    Tax Pct                                  5    T(1) ##.00
    80    Total Gross                             11    T(2) ########.00
    81    Total Discount                           9    T(3) ######.00
    82    Total Tax                                9    T(4) ######.00
    83    Total Misc Chgs                          9    T(5) ######.00
    84    Taxable Amt                              9    T(6) ######.00
    85    Net Order Amt                           11    T(7) ########.00
    86    Total Net Lbs                            9    T(8) ######.00
    87    Svc Chg Amt                              9    T(9) ######.00
    88    Total Cost                               9    T(10) ######.00
    89    Total Gross Lbs                          9    T(11) ####.00##
    90    Total Cases                             10    T(12) #######.00
    91    Total Eaches                             6    T(13) ######
    92    Spoilage Allowance                       9    T(14) #####.00#
    93    Fuel Surcharge                           9    T(15) ######.00
    94    CATEGORIES                               5    TN$
    95    Total Cube                              10    UN$ #######.00
    96    Invoice Number                           6    VN$
    97    E.O.S. Discount %                        5    Wn$
    98    EOE Transmission No                      6    Xn$(1,6)
    99    EOE Confirmation No                      6    Xn$(7,6)
   100    Date Transmitted                         6    Xn$(13,6)
   101    Time Transmitted                         4    Xn$(19,4)
   102    No of Price Labels Princed               6    Yn$(1,6) ######
   103    Charge for price labels                  8    Yn$(7,8) #####.00
   104    Invoice Svc Chg %                        5    ZN$ ###.0
FCRDERD  -OPEN ORDER DETAIL FILE MAINT. & INQUIRY  ( 37 at start)
     1    Company Code                             2    AN$(1,2)
     2    Order Number                             6    AN$(3,6)
     3    Release NO.                              2    AN$(9,2)
     4    KEY TYPE = '1'                           1    AN$(11,1)
     5    Line No.                                 3    AN$(12,3)
     6    Forward Ptr                              5    AN #####
     7    Backward Ptr                             5    BN #####
     8    Sales Unit                               2    BN$(1,2)
     9    Pricing Unit                             2    BN$(3,2)
    10    Wholesale Taxable (Y/N)                  1    BN$(5,1)
    11    Sales Category                           2    BN$(6,2)
    12    Retail Price List Code                   1    BN$(8,1)
    13    Wholesale Price List Code                1    BN$(9,1)
    14    Special Price? (Y/N)                     1    BN$(10,1)
    15    Line Item Terms Code                     1    BN$(11,1)
    16    Allocated (Y/N)                          1    Bn$(12,1)
    17    Split Case Code                          1    Bn$(13,1)
    18    SALES CD                                 1    BN$(14,1)
    19    Reason Code - Price Override             2    BN$(15,2)
    20    ADDS TO TOTAL WT                         1    BN$(17,1)
    21    Entry Type (I/A/M)                       1    BN$(18,1)
    22    CONTRACT?                                1    BN$(19,1)
    23    CATCH WEIGHT?                            1    BN$(20,1)
    24    Warehouse Code                           4    BN$(21,4)
    25    Pick Except Reason                       2    Bn$(25,2)
    26    Alloc Except Reason                      1    BN$(27,1)
    27    BOX/CASE (B/C/SP)                        1    BN$(28,1)
    28    FREIGHT CLASS                            1    BN$(29,1)
    29    Item Type                                1    BN$(30,1)
    30    WHSE Category                            1    BN$(31,1)
    31    G/L Category                             1    BN$(32,1)
    32    Inventory Units                          2    BN$(33,2)
    33    Initials for pick exceptions             3    Bn$(35,3)
    34    Retail Taxable (Y/N) ?                   1    Bn$(38,1)
    35    Quantity Exceeded (Y/sp) ?               1    Bn$(39,1)
    36    Invty Availability Code                  1    Bn$(40,1)
    37    CA Redemption Code                       1    Bn$(41,2)
    38    Reason Code - Credit Request             2    Bn$(42,2)
    39    Invoice Ref - Credit Request             8    Bn$(44,8)
    40    Commissionable (Y/N)                     1    Bn$(52,1)
    41    Update S/A (Y or sp=yes,N=no)            1    Bn$(53,1)
    42    Retail Price Overrive(V=yes)             1    Bn$(54,1)
    43    Cred Req Invoice Date                    6    Bn$(55,6)
    44    Cred Req Override(Y/sp)                  1    Bn$(61,1)
    45    Cred Req Disposition Code                2    Bn$(62,2)
    46    (open)                                   3    Bn$(64,3)
    47    Organic? (Y/N)                           1    Bn$(67,1)
    48    (open)                                  13    Bn$(68,13)
    49    Description                             48    Cn$
    50    Item Key                                21    DN$
    51    Item Code                                6    EN$
    52    UPC Code                                12    FN$
    53    ORD PRT MSG                              2    GN$(1,2)
    54    INV PRT MSG                              2    GN$(3,2)
    55    G/L ACCT #                              11    HN$
    56    LOT NUMBER                              36    IN$
    57    Location Codes                          12    Jn$
    58    Contract Number                         12    Kn$
    59    Original Alloc Quantity                  1    LN$
    60    (OPEN)                                   1    MN$
    61    (OPEN)                                   1    NN$
    62    Retail Sub-Pack                          6    ON$ ###.00
    63    PACK                                     4    PN$
    64    NET UNIT WEIGHT                          9    QN$
    65    (OPEN)                                   1    RN$
    66    Qty Ordered                             10    S(0) #######.00
    67    Qty Shipped                             10    S(1) #######.00
    68    P/A Per Unit                             9    S(2) ######.00
    69    QUANTITY INVOICED                       10    S(3) #######.00
    70    CATCH WGT OR UNIT CONV FACTOR           10    S(4) #####.00##
    71    Unit Price                              10    S(5) #####.00##
    72    GROSS UNIT WGT                           6    S(6) ###.00
    73    Extension                               10    S(7) #######.00
    74    DISCOUNT %                               5    S(8) ##.00
    75    TAX %                                    8    S(9) #####.00
    76    Unit Cost                                9    S(10) ####.00##
    77    Qty Committed Updated                    6    S(11) ######
    78    Qty on Hand Updated                      6    S(12) ######
    79    Sugggested Retail Price                  9    S(13) ######.00
    80    Total P/A %                              6    S(14) ###.00
    81    Quantity Allocated                       1    S(15) #
    82    Bill Back Pct                            6    Tn$
    83    P/A Percents                            16    Un$
    84    Invoice P/A Desc                         5    VN$
    85    Unit Cube                                6    WN$ ###.00
    86    (OPEN)                                   1    XN$
    87    Link to Header                           1    YN$
    88    OPEN                                     1    Z$
FCOEIV   -INVOICE OUT OF STOCK SORT FILE  ( 38 at start)
     1    Company Code                             2    An$(1,2)
     2    Invoice Date (YYMMDD)                    6    An$(3,6)
     3    Vendor Code                              6    An$(9,6)
     4    Item Description                        16    AN$(15,10)
     5    Item Code                               12    An$(25,12)
     6    Customer & Ship-to                      10    An$(37,10)
     7    Invoice Number & Release No.             8    An$(47,8)
     8    Reason Shorted (SpaceA=Alloc)            2    Bn$(1,2)
     9    Salesrep Code                            3    Bn$(3,3)
    10    Quantity Ordered                         6    Cn ###.00
    11    Quantity Shipped                         6    Dn ###.00
    12    Extension                                9    En ######.00
    13    (open)                                        Fn
FCCSXF   -CUSTOMER ALPHA SORT FILE  ( 39 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    SORT KEY                                 8    An$(3,8)
     3    CUSTOMER NUMBER                          6    An$(11,6)
FCCNVZo  -ALLOWANCE (ADD-ON'S) CODE CONTROL FILE M  ( 40 at start)
     1    KEY GROUP = "o"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    ADD-ON CODE                              2    An$(4,2)
     4    DESCRIPTION                             35    Bn$
     5    UNITS                                    2    Cn$(1,2)
     6    SUBJ TO BROKGE?                          1    Cn$(3,1)
     7    INCLUDE IN S/A                           1    Cn$(4,1)
     8    EXTENSION METHOD                         1    Cn$(5,1)
     9    SALES POST CODE                          1    Cn$(6,1)
    10    Percent or Amount (%,A)                  1    Cn$(6,1)
    11    (OPEN)                                   3    Cn$(8,3)
    12    Percentage or Amount                     9    Dn ####.00##
    13    UNIT COST                                9    En ####.00##
    14    G/L ACCOUNT                             11    Fn$
    15    DEFAULT QUANTITY                        12    Gn #########.00
    16    (OPEN)                                   1    Hn$
    17    (OPEN)                                   1    In$
FCICPC   -PRICE CHANGE TRANSACTION FILE  ( 41 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    ITEM CODE                               12    AN$(3,12)
     3    RECORD TYPE                              1    AN$(15,1)
     4    WHSE OR CUST                             6    AN$(16,6)
     5    AUTHORITY                                3    BN$(1,3)
     6    UNITS                                    2    BN$(4,2)
     7    EFFECTIVE DATE NEW PRICE                 8    BN$(6,8)
     8    OLD EFFECTIVE DATE                       8    BN$(14,8)
     9    ENTRY DATE                               8    BN$(22,8)
    10    ENTERED BY                               3    BN$(30,3)
    11    CHANGED (Y/N/A/D)                        1    BN$(33,1)
    12    PRICE TYPE                               1    BN$(34,1)
    13    (OPEN)                                   6    BN$(35,6)
    14    DESCRIPTION                             40    CN$
    15    OLD COST BASIS                           9    F(0) ####.00##
    16    OLD MKT VALUE                            9    F(1) ####.00##
    17    OLD PRICE A                              9    F(2) ####.00##
    18    OLD PRICE B                              9    F(3) ####.00##
    19    OLD PRICE C                              9    F(4) ####.00##
    20    OLD PRICE D                              9    F(5) ####.00##
    21    OLD PRICE E                              9    F(6) ####.00##
    22    OLD PRICE F                              9    F(7) ####.00##
    23    OLD PRICE G                              9    F(8) ####.00##
    24    OLD PRICE H                              9    F(9) ####.00##
    25    OLD P/A                                  7    F(10) ##.00##
    26    OLD 'PRICE TYPE' PERCENTAGE              5    F(11) ##.00
    27    NEW COST BASIS                           9    G(0) ####.00##
    28    NEW MKT VALUE                            9    G(1) ####.00##
    29    NEW PRICE A                              9    G(2) ####.00##
    30    NEW PRICE B                              9    G(3) ####.00##
    31    NEW PRICE C                              9    G(4) ####.00##
    32    NEW PRICE D                              9    G(5) ####.00##
    33    NEW PRICE E                              9    G(6) ####.00##
    34    NEW PRICE F                              9    G(7) ####.00##
    35    NEW PRICE G                              9    G(8) ####.00##
    36    NEW PRICE H                              9    G(9) ####.00##
    37    NEW P/A                                  7    G(10) ###.00#
    38    NEW 'PRICE TYPE' PERCENTAGE              6    G(11) ###.00
    39    PA CUST (EG,'AB')                        3    HN$
    40    START P.A.DATE (NEW)                     6    IN$
    41    END P.A. DATE (NEW)                      6    JN$
    42    MIN ORD WEIGHT                           7    KN ####.00
    43    MIN ORD QTY                              5    LN #####
    44    (open)                                   1    MN$
FCCNVZS  -SERVICE CHARGE PERIOD MASTER FILE  ( 42 at start)
     1    KEY TYPE = "SC"                          2    A$(1,2)
     2    COMPANY CODE                             2    A$(3,2)
     3    PERIOD CODE                              1    A$(4,1)
     4    open                                     1    B$
     5    NO. OF DAYS OLD                          3    A ###
     6    open                                     1    B #
FCSACM   -SALESMAN COMMISSION FILE  ( 43 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    SALESMAN NUMBER                          2    AN$(3,2)
     3    INVOICE NUMBER                           6    AN$(5,6)
     4    SPLIT COMMISSION (Y/N)                   1    BN$(1,1)
     5    MANUAL OVERRIDE (Y/N)                    1    BN$(2,1)
     6    --OPEN--                                 3    BN$(3,3)
     7    INVOICE DATE                             6    CN$
     8    INVOICE AMT.                             9    AN ######.00
     9    ELIGIBLE AMOUNT                          9    BN ######.00
    10    COMM %                                   6    CN ###.00
    11    COMM AMT                                 9    DN ######.00
    12    CUSTOMER CODE                            6    DN$
    13    --OPEN--                                 1    EN$
    14    ORDER NUMBER                             6    FN$
    15    --OPEN--                                 1    GN #
FCCNVZt  -FORM TYPE MASTER FILE  ( 44 at start)
     1    KEY TYPE = 't'                           1    AN$(1,1)
     2    FORM TYPE CODE                           2    AN$(2,2)
     3    FORM DESCRIPTION                        30    BN$
     4    LENGTH (INCHES)                          6    AN ##.00#
     5    WIDTH (INCHES)                           6    BN ##.00#
     6    # OF PARTS                               6    CN
     7    # OF FORMS-UP                            1    DN
     8    DIST. BETWEEN LABEL(INCH)                6    EN ##.00#
     9    STOCK NUMBER                            10    CN$
    10    OPEN                                     1    DN$
    11    OPEN                                     1
    12    OPEN                                     1    FN$
FCSADFC  -SALES ANALYSIS - CATEGORY RECORD  ( 45 at start)
     1    KEY TYPE - 'C'                           1    AN$(1,1)
     2    COMPANY                                  2    AN$(2,2)
     3    SALESMN                                  2    AN$(4,2)
     4    CATEGORY                                 1    AN$(6,1)
     5    UNITS-YTD                                8    D(0) ########
     6    -LST YTD                                 8    D(1) ########
     7    -CUR MTH                                 8    D(2) ########
     8    -PRV MTH                                 7    D(3) #######
     9    -PRV 2                                   7    D(4) #######
    10    -PRV 3                                   7    D(5) #######
    11    -PRV 4                                   7    D(6) #######
    12    -PRV 5                                   7    D(7) #######
    13    -PRV 6                                   7    D(8) #######
    14    -PRV 7                                   7    D(9) #######
    15    -PRV 8                                   7    D(10) #######
    16    -PRV 9                                   7    D(11) #######
    17    -PRV 10                                  7    D(12) #######
    18    -PRV 11                                  7    D(13) #######
    19    -PRV 12                                  7    D(14) #######
    20    -PRV 13                                  7    D(15) #######
    21                                             1    EN$
    22                                             1    FN$
    23    CWT - YTD                                8    E(0) ########
    24                                             8    E(1) ########
    25                                             8    E(2) ########
    26                                             7    E(3) #######
    27                                             7    E(4) #######
    28                                             7    E(5) #######
    29                                             7    E(6) #######
    30                                             7    E(7) #######
    31                                             7    E(8) #######
    32                                             7    E(9) #######
    33                                             7    E(10) #######
    34                                             7    E(11) #######
    35                                             7    E(12) #######
    36                                             7    E(13) #######
    37                                             7    E(14) #######
    38                                             7    E(15) #######
    39    SALES-YTD                                8    F(0) ########
    40                                             8    F(1) ########
    41                                             8    F(2) ########
    42                                             7    F(3) #######
    43                                             7    F(4) #######
    44                                             7    F(5) #######
    45                                             7    F(6) #######
    46                                             7    F(7) #######
    47                                             7    F(8) #######
    48                                             7    F(9) #######
    49                                             7    F(10) #######
    50                                             7    F(11) #######
    51                                             7    F(12) #######
    52                                             7    F(13) #######
    53                                             7    F(14) #######
    54                                             7    F(15) #######
    55    COST-YTD                                 8    G(0) ########
    56                                             8    G(1) ########
    57                                             8    G(2) ########
    58                                             7    G(3) #######
    59                                             7    G(4) #######
    60                                             7    G(5) #######
    61                                             7    G(6) #######
    62                                             7    G(7) #######
    63                                             7    G(8)  #######
    64                                             7    G(9) #######
    65                                             7    G(10) #######
    66                                             7    G(11) #######
    67                                             7    G(12) #######
    68                                             7    G(13) #######
    69                                             7    G(14) #######
    70                                             7    G(15) #######
FCCNVZCPO-P/O SYSTEM CONTROL RECORD  ( 46 at start)
     1    KEY TYPE = "CPO"                         3    An$(1,3)
     2    COMPANY CODE                             2    An$(4,2)
     3    I/C WAREHOUSE                            4    Bn$(1,4)
     4    DEL WAREHOUSE                            4    Bn$(5,4)
     5    DATE WANTED                              8    Cn$(1,8)
     6    CARRIER                                 20    Cn$(9,20)
     7    Item Key Type                            1    Dn$(1,1)
     8    Print P.O.s (Y/N)                        1    Dn$(2,1)
     9    Replace Costs (Y/N/A)                    1    Dn$(3,1)
    10    Auto Receipts (Y/N)                      1    Dn$(4,1)
    11    Standard Freight (Y/N)                   1    Dn$(5,1)
    12    Manf Out of Stock Code                   1    Dn$(6,1)
    13    Std P/O Type                             2    Dn$(7,2)
    14    Vendor Debit Msgs                       10    Dn$(9,10)
    15    Auto Gen Recomm P.O.s (Y/N)              1    Dn$(19,1)
    16    History Months                           2    Dn$(20,2) ##
    17    Exp Dt/Lot on PO?                        1    Dn$(22,1)
    18    (open)                                   6    Dn$(23,6)
    19    P/O Line Item Ctl                        8    En$
    20    P/O Print Messages                      40    Fn$
    21    ITEM CODE POSITION                       2    An ##
    22    ITEM CODE LENGTH                         2    Bn ##
    23    Item Receipts Hist Recs                  2    Cn ##
    24    Min Days for History                     3    Dn ###
FCCNVZZ  -CBS SALESMAN MASTER FILE  ( 47 at start)
     1    KEY TYPE = 'Z'                           1    AN$(1,1)
     2    SALESPERSON CODE                         3    An$(2,3)
     3    SALESPERSON NAME                        30    BN$
     4    Invoice Msg 1                           50    CN$
     5    Invoice Msg 2                           50    DN$
     6    Invoice Msg 3                           50    EN$
     7    COMMISSION PERIOD-TO-DATE                9    AN ######.00
     8    COMMISSION YEAR-TO-DATE                  9    BN ######.00
     9    COMM %                                   5    CN ##.00
    10    COMPANY CODE                             2    Fn$(1,2)
    11    PHONE NUMBER                            10    FN$(3,10)
    12    COMMISSIONABLE(Y/N)                      1    FN$(13,1)
    13    COMMISSION TYPE                          1    GN$
    14    SalesInq Access                          9    Hn$
FCRCKS   -CASH RECEIPTS CHECK FILE  ( 48 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER NUMBER                          6    An$(3,6)
     3    CHECK NUMBER                             5    An$(9,5)
     4    ABA NUMBER                              15    Bn$
     5    CHECK DATE                               6    Cn$
     6    CHECK AMOUNT                            12    Dn #########.00
     7    AMOUNT OF CHK APPLIED                   12    En #########.00
     8    Customer Name                           40    Fn$
FCDASL   -A/R XREF TO CUSTOMERS BY SALESPERSON  ( 49 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    SALESPERSON CODE                         3    An$(3,3)
     3    CUSTOMER NO.                             6    An$(6,6)
FCCNVZQ  -ORDER SOURCE CODES FILE MAINTENANCE & IN  ( 50 at start)
     1    Key Group = 'Q'                          1    An$(1,1)
     2    Order Source Code                        2    An$(2,2)
     3    Description                             20    Bn$
     4    Update Weekly Trend (Y/N) ?              1    Cn$(1,1)
     5    Update Monthly Trend                     1    Cn$(2,1)
     6    Update Sales Analysis (Y/N) ?            1    Cn$(3,1)
     7    (open)                                   7    Cn$(4,7)
FCCNVZD1 -Vendor Purchase Terms Codes  ( 51 at start)
     1    Key Group = 'D1'                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Purchase Terms Code                      1    An$(5,1)
     4    Terms Description                       25    Bn$
     5    Discount: Number of Days                 3    An ###
     6    Discount: percentage                     4    Bn ##.0
     7    Terms Ageing: Number of Days             3    Cn ###
     8    FUTURE AGING? (Y/N)                      1    Cn$
     9    # DAYS TILL CURRENT                      3    Dn ###
FCARTP   -TEMPORARY INVOICE LOAD SORT FILE  ( 52 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    CUSTOMER NO.                             6    AN$(3,6)
     3    INVOICE NO.                              6    AN$(9,6)
     4    TRANSACTION NO.                          6    AN$(15,6)
FCCRIR   -CASH RECEIPTS JOURNAL  ( 53 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER NO.                             6    An$(3,6)
     3    TRANSACTION NO.                          4    An$(9,4)
     4    Customer Name                           40    Bn$
     5    INVOICE NO.                              6    Cn$
     6    REASON OF TRANSACTION                    6    Dn$
     7    PAYMENT DATE                             6    En$
     8    PAYMENT                                 11    An ########.00
     9    NEW A/R BALANCE                         11    Bn ########.00
    10    OLD A/R BALANCE                         11    Cn ########.00
    11    PAYMENT DISCOUNT CREDIT                 11    Dn ########.00
    12    OTHER ALLOWANCES                        11    En ########.00
    13    A/R ACCOUNT # (CR A+D+E)                11    Fn$
    14    NET CASH ACCOUNT # (DR A)               11    Gn$
    15    DISCOUNT ACCOUNT # (DR D)               11    Hn$
    16    OTHER ACCOUNT # (DR E)                  11    In$
    17    RESERVED FOR EXPANSION                   1    Jn$
FCOPAR   -OPEN ACCOUNTS RECEIVABLE FILE MAINTENANC  ( 54 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER NO.                             6    An$(3,6)
     3    INVOICE NO.                              6    An$(9,6)
     4    TRANSACTION NO.                          6    An$(15,6)
     5    GROSS (INVTY SLS)                       11    An ########.00
     6    CASH DISCOUNT                           10    Bn #######.00
     7    OTHER CHARGES                           10    Cn #######.00
     8    FREIGHT AMOUNT                          10    Dn #######.00
     9    NET AMOUNT                              11    En ########.00
    10    TERMS CODE                              10    Bn$
    11    INVOICE DATE                             6    Cn$
    12    PAYMENT AMOUNT                          10    Fn #######.00
    13    PAYMENT DATE                             6    Dn$
    14    Discount Taken                          10    Gn #######.00
    15    Other Allowance Amount                  11    Hn ########.00
    16    Adjustment Code                          1    In #
    17    Total Debits                            11    Jn ########.00
    18    Total Credits                           11    Kn ########.00
    19    Company Code                             2    En$(1,2)
    20    Ship to Code                             4    En$(3,4)
    21    Customer P.O. Number                    10    Fn$
    22    Paid by Check Number                     5    Gn$
    23    G/L Account for A/R                     11    Hn$
    24    Terms Date                               6    In$(1,6)
    25    Date Posted                              6    In$(7,6)
    26    Order Date                               6    In$(13,6)
    27    Sales Rep(from conv)                     4    In$(19,4)
    28    Date Shipped                             6    In$(23,6)
    29    NO CHG,PICK,PRNT,CODE                    4    In$(29,4)
    30    Fin Charge(CR=yes,N=no)                  1    In$(33,1)
    31    Comment                                 10    In$(34,10)
FCAUTO   -AUTOMATIC CASH APPLICATION SORT FILE  ( 55 at start)
     1    INVOICE DATE                             6    An$(1,6)
     2    INVOICE NUMBER                           6    An$(7,6)
FCARBK   -ACCOUNTS RECEIVABLE BROKER STATEMENT FIL  ( 56 at start)
     1    Company Code                             2    An$(1,2)
     2    Broker Code                              3    An$(3,3)
     3    Customer Number                          6    An$(6,6)
     4    Invoice Number                           6    An$(12,6)
     5    Invoice Date                             6    Bn$(1,6)
     6    Statement Date                           6    Bn$(7,6)
     7    (open)                                  12    Bn$(13,12)
     8    Calc Type                                1    Cn$(1,1)
     9    When Paid                                1    Cn$(2,1)
    10    Multi-Vendor? (Y/N)                      1    Cn$(3,1)
    11    Printed? (Y/N)                           1    Cn$(4,1)
    12    (open)                                   1    Cn$(5,1)
    13    Pct Desc                                10    Dn$
    14    Invoice Amount                          12    B(0) #########.00
    15    Amount Subject                          12    B(1) #########.00
    16    Commission %                             5    B(2) ##.00
    17    Commission Amt                           8    B(3) #####.00
    18    (open)                                   8    B(4) #####.00
FCARHI   -Accounts Receivable History  ( 57 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER NO.                             6    An$(3,6)
     3    INVOICE NO.                              6    An$(9,6)
     4    TRANSACTION NO.                          6    An$(15,6)
     5    GROSS (INVTY SLS)                       11    An ########.00
     6    Cash Discount                           10    Bn ######.00#
     7    OTHER CHARGES                           10    Cn #######.00
     8    FREIGHT AMOUNT                           9    Dn ######.00
     9    NET AMOUNT                              11    En ########.00
    10    TERMS CODE                               1    Bn$
    11    INVOICE DATE                             6    Cn$
    12    PAYMENT AMOUNT                          11    Fn ########.00
    13    PAYMENT DATE                             6    Dn$
    14    Discount Taken                          10    Gn #######.00
    15    Other Allowance Amount                  11    Hn ########.00
    16    Adjustment Code                          1    In #
    17    Total Debits                            11    Jn ########.00
    18    Total Credits                           11    Kn ########.00
    19    Company Code                             2    En$(1,2)
    20    Ship-to Code                             4    An$(3,4)
    21    Customer P.O. Number                    10    Fn$
    22    Paid by Check Number                     5    Gn$
    23    G/L ACCT...NOT USED                      1    Hn$
    24    Terms Date                               6    In$(1,6)
    25    Date Posted                              6    In$(7,6)
    26    Order Date                               6    In$(13,6)
    27    Date Shipped                             6    In$(19,6)
    28    Comment                                 20    In$(25,20)
FCSVCG   -SERVICE CHARGE TRANSACTION  ( 58 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER NUMBER                          6    An$(3,6)
     3    S/C INVOICE NUMBER                       6    An$(9,6)
     4    SERVICE CHARGE AMOUNT                   10    An #######.00
     5    SERVICE CHARGE RATE                      4    Bn ##.0
     6    TRANSACTION CODE                         2    Cn$
     7    (open)                                   1    Dn$
     8    (OPEN)                                   1    En$
FCCNVZ6  -General Ledger Interface Record - Payroll  ( 59 at start)
     1    Key Type = '^S'                          2    Zn$(1,2)
     2    Company Code                             2    Zn$(3,2)
     3    (open)                                   1    An #
     4    Journal Number                           5    An$
     5    Fed W/H Payable (CR)                    11    Bn$
     6    F.I.C.A. Payable (CR)                   11    Cn$
     7    (open)                                   1    Dn$
     8    (open)                                   1    En$
     9    (open)                                   1    Fn$
    10    P/R Net Pay (CR)                        11    Gn$
    11    Worker's Comp (DR)                      11    Hn$
    12    Employer's F.I.C.A. (DR)                11    In$
    13    (open)                                   8    Jn$
    14    (open)                                   1    Kn$
FCCNVZB  -CUSTOMER BUILD-UP ITEMS  ( 60 at start)
     1    Key Type = "B"                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Fob Code                                 2    An$(4,2)
     4    Description                             20    Bn$
     5    Collect/Prepaid/Prepay & Add             1    Cn$
     6    (open)                                   1    Dn$
FCOEHI   -Invoice Detail History  ( 61 at start)
     1    Company Code                             2    An$(1,2)
     2    Customer Code                            6    An$(3,6)
     3    Ship-to Code                             4    An$(9,4)
     4    Invoice & Release Number                 8    An$(13,8)
     5    Item Code (spaces=header)                6    An$(21,6)
     6    Line Item                                3    An$(27,3) ###
     7    Units Ordered                            2    Bn$(1,2)
     8    P/A is Amount or Per unit(A/P)           1    Bn$(3,1)
     9    Invoice Date                             6    Bn$(4,6)
    10    Quantity Shipped                         4    Cn ####
    11    Wholesale Unit Price                     7    Dn ###.00#
    12    Promotion Amount                         7    En ###.00#
    13    Units Creditted to Date                  4    Fn ####
    14    Vendor Bill Back %                       6    Gn$ ###.00
    15    Qty Ordered                              5    Hn #####
FCCNVZI  -INVENTORY COMPANY CONTROL RECORD MAINTEN  ( 62 at start)
     1    KEY TYPE = I                             1    AN$(1,1)
     2    COMPANY CODE                             2    AN$(2,2)
     3    CURRENT PERIOD                           2    BN ##
     4    CLOSE - Period 01                        6    C(1) ######
     5          - Period 02                        6    C(2) ######
     6          - Period 03                        6    C(3) ######
     7          - Period 04                        6    C(4) ######
     8          - Period 05                        6    C(5) ######
     9          - Period 06                        6    C(6) ######
    10          - Period 07                        6    C(7) ######
    11          - Period 08                        6    C(8) ######
    12          - Period 09                        6    C(9) ######
    13          - Period 10                        6    C(10) ######
    14          - Period 11                        6    C(11) ######
    15          - Period 12                        6    C(12) ######
    16          - Period 13                        6    C(13) ######
    17    Weekly Trend Period End Date             6    DN ######
    18    Standard Warehouse                       4    En$(1,4)
    19    Stock Mvmt Rpt(D,S,X)                    1    En$(5,1)
    20    Report in CS(0) or EA(1)                 1    En$(6,1) #
    21    Last Catalog Date                        6    En$(7,6) ######
    22    Physical Tolerance $                     6    En$(13,6) ######
    23    Allow Dup Loctns? (Y/N)                  1    En$(19,1)
    24    ABC Catg - 'A' Pct                       2    En$(20,2) ##
    25             - 'B' Pct                       2    En$(22,2)
    26             - 'C' Pct                       2    En$(24,2) ##
    27    Max Number of Lots                       2    En$(26,2) ##
    28    Stock Mvmnt SEQ                          4    En$(28,4) ####
    29    Multiple Warehouses?                     1    En$(32,1)
    30    'Special' Location 1                     6    En$(33,6)
    31                       2                     6    En$(39,6)
    32                       3                     6    En$(45,6)
    33    Non-Stock Item Code                      6    En$(51,6)
    34    Last Bulletin Date                       6    En$(57,6)
    35    Next Pallet Tag No                       8    En$(63,8) ########
    36    Update G/L? (Y/N):                       1    En$(71,1)
    37    Stk Jrnl Update Passwd                   3    En$(72,3)
    38    (open)                                   4    En$(75,4)
    39    Number Months Movement                   2    En$(79,2) ##
FCAPST   -OPEN ACCOUNTS PAYABLE SORT FILE  ( 63 at start)
     1    DUE DATE                                 6    An$(1,6)
     2    COMPANY CODE                             2    An$(7,2)
     3    VENDOR NUMBER                            6    An$(9,6)
     4    VOUCHER NUMBER                           6    An$(15,6)
     5    TRANSACTION                              6    An$(21,6)
FCOPAF   -OPEN ACCOUNTS PAYABLE MASTER FILE MAINT.  ( 64 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    VENDOR NUMBER                            6    An$(3,6)
     3    VOUCHER NO.                              6    An$(9,6)
     4    TRANSACTION DATE                         6    An$(15,6)
     5    PAYEE NAME                              30    Bn$
     6    Date due                                 6    Cn$(1,6)
     7    Terms Date                               6    Cn$(7,6)
     8    P/O NUMBER                               6    Dn$
     9    GROSS AMOUNT                            10    An #######.00
    10    DISCOUNT AMOUNT                         10    Bn #######.00
    11    ENTRY DATE                               6    En$
    12    DEDUCTION                                7    Cn ####.00
    13    1099 AMOUNT                             11    Dn ###########
    14    DATE OF LAST PAYMENT                     6    Fn$
    15    PAYMENT CODE                             1    En #
    16    DATE OF LAST ADJUST                      6    Gn$
    17    VENDOR REF.NO.                          25    Hn$
    18    PPD FLAG                                 1    In$(1,1)
    19    (open)                                   3    In$(2,3)
    20    TERMS (PP/DDD)                           6    In$(5,6)
    21    G/L ACCOUNT                             11    In$(11,11)
    22    DATE ORDERED                             6    IN$(22,6) ######
    23    (OPEN)                                   1    JN$
    24    (OPEN)                                   1    KN$
    25    (OPEN)                                   1    LN$
FCVNMS   -VENDOR MASTER FILE MAINT & INQUIRY  ( 65 at start)
     1    Company Code                             2    An$(1,2)
     2    Vendor Number                            6    An$(3,6)
     3    Vendor Name                             35    Bn$
     4    Address Line 1                          35    Cn$
     5    Address Line 2                          35    Dn$
     6    Address Line 3                          35    En$
     7    Vendor Balance                          11    An ########.00
     8    Telephone Number                        10    Gn$
     9    Date Acct Opened                         6    Hn$
    10    Curr Yr Invoices                        11    Bn ########.00
    11    Curr Yr Disc Avail                      11    Cn ########.00
    12    Curr Yr Disc Taken                      11    Dn ########.00
    13    Prev Yr Invoices                        11    En ########.00
    14    Prev Yr Disc Avail.                     11    Fn ########.00
    15    Prev Yr Disc Taken                      11    Gn ########.00
    16    ANY CONTRACTS (Y/N)                      1    In$(1,1)
    17    1099 BOX NUMBER                          2    In$(2,2)
    18    TERMS (FOR P.O.)                         1    In$(4,1)
    19    Organic Cert? (Y/N)                      1    In$(5,1)
    20    BROKER CODE                              3    In$(6,3)
    21    G/L CATEG (0/1)                          1    In$(9,1)
    22    1099 ID NUMBER                          15    In$(10,15)
    23    Net Terms Days                           3    In$(25,3) ###
    24    Advertiser? (Y/N)                        1    In$(28,1)
    25    Fax Number                              10    In$(29,10) ##########
    26    Contact Name                            15    In$(39,15)
    27    Organic Cert on File?                    1    In$(54,1)
    28    Cert Exp Date                            6    In$(55,6)
    29    TERMS (PP/DDD)                           6    Jn$
    30    DATE LAST PURCHASE                       6    Kn$
    31    SORT KEY                                 8    Ln$
    32    1099 YTD BALANCE                        11    Hn ########.00
    33    Broker Telephone                        10    Mn$(1,10)
    34    Broker Fax Number                       10    Mn$(11,10)
    35    BROKER NAME                             42    Nn$
    36    Standard G/L Expense Account            11    On$
FCGLDA   -DAILY GENERAL LEDGER DISTRIBUTION FILE M  ( 66 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    G/L ACCOUNT NO.                         11    An$(3,11)
     3    VEND/CUST/ITEM                           6    An$(14,6)
     4    VOUCH/INV/WHSE                           6    An$(20,6)
     5    TRANSACTION DATE                         6    An$(26,6)
     6    DISTRIBUTION TYPE                        1    An$(32,1)
     7    VEND/CUST NAME                          30    Bn$
     8    REFERENCE/CHECK #                       25    Cn$
     9    DISTRIBUTION AMOUNT                     10    An #######.00
    10    # OF LINES                               5    Bn #####
    11    (OPEN)                                   1    Cn
    12    TRANSACTION DESCRIPTION                 30    Dn$
    13    REFER                                    4    En$
    14    PROJECT NUMBER                           3    Fn$
FCPYRH   -ACCOUNTS PAYABLE REGISTER MAINT & INQUIR  ( 67 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    Vendor Number                            6    An$(3,6)
     3    Voucher Number                           6    An$(9,6)
     4    INVOICE DATE                             6    An$(15,6)
     5    VENDOR NAME                             30    Bn$
     6    P/O NUMBER                               6    Cn$
     7    Invoice Due Date                         6    Dn$(1,6)
     8    Terms Date                               6    Dn$(7,6)
     9    GROSS AMOUNT                            11    A4 ########.00
    10    DISCOUNT                                 9    B4 ######.00
    11    DEDUCTIONS AMOUNT                        9    Cn ######.00
    12    1099 AMOUNT                             11    Dn ###########
    13    (open)                                   1    En #
    14    DATE ENTERED                             6    En$
    15    DISTRIBUTION UPDATE CODE                 1    Fn$
    16    VENDOR REF. NO.                         25    Gn$
    17    (OPEN)                                   1    Hn$
    18    (open)                                   1    In$
FCPYRD   -ACCOUNTS PAYABLE REGISTER (DETAIL) MAINT  ( 68 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    Vendor Number                            6    An$(3,6)
     3    Voucher Number                           6    An$(9,6)
     4    INVOICE DATE                             6    An$(15,6)
     5    SEQUENCE NO.                             3    An$(21,3)
     6    G/L ACCOUNT NO.                         11    Bn$
     7    AMOUNT                                  11    A5 ########.00
     8    COMPANY CODE                             2    Cn$
     9    REFER                                    4    Dn$
    10    PROJECT NUMBER                           3    En$
    11    APPLICATION DATE                         6    Fn$
    12    TRANSACTION DESCRIPTION                 30    Gn$
    13    (OPEN)                                   1    Hn$
FCVNCK   -ACCOUNTS PAYABLE CHECK FILE  ( 69 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    RECORD ID                                1    AN$(3,1)
     3    CHK/VNDR #                               6    AN$(4,6)
     4    VOUCHER NO.                              6    An$(10,6)
     5    INV. DATE                                6    An$(16,6)
     6    RCD COUNT                                2    An$(22,2)
     7    VND/PAYEE NAME                          35    CN$
     8    DATE DUE                                 6    DN$
     9    P/O #                                    9    EN$
    10    GROSS                                   10    AN #######.00
    11    DISCOUNT                                10    BN #######.00
    12    CHECK DATE                               6    FN$
    13    RCD CODE                                 1    CN #
    14    DEDUCTIONS AMOUNT                       10    Dn #######.00
    15    1099 AMOUNT                             10    En ##########
    16    G/L ACCOUNT NO.                         11    GN$
    17    VENDOR REF. NO.                         25    HN$
    18    VND NO-CHK ONLY                          6    IN$
    19    (open)                                   1    JN$
    20    (open)                                   3    Kn$(1,3)
    21    TERMS (00/000)                           6    KN$(4,6)
FCMCRG   -MONTHLY CHECK REGISTER MAINT & INQUIRY  ( 70 at start)
     1    COMPANY CODE                             2    A5$(1,2)
     2    CASH ACCT CODE                           1    A5$(3,1)
     3    CHECK NO.                                6    A5$(4,6)
     4    RECORD ID                                1    A5$(10,1)
     5    VENDOR NO.                               6    B5$
     6    (OPEN)                                   1    C5$
     7    (OPEN)                                   1    D5$
     8    (OPEN)                                   1    E5$ #
     9    VENDOR/PAYEE NAME                       30    F5$
    10    (OPEN)                                   1    G5$
    11    (OPEN)                                   1    H5$
    12    GROSS                                   10    A5 #######.00
    13    DISCOUNT                                10    B5 #######.00
    14    CHECK DATE                               6    I5$
    15    RECORD CODE                              1    J5$ #
    16    (OPEN)                                   1    K5$
    17    (OPEN)                                   1    L5$
    18    DEDUCTION AMOUNT                        11    C5
    19    1099 AMOUNT                             11    D5
    20    (OPEN)                                   1    E5
    21    (OPEN)                                   1    F5
FCAPAJH  -A/P ADJUSTMENTS HEADER  ( 71 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    VENDOR NO.                               6    AN$(3,6)
     3    VOUCHER NUMBER                           6    An$(9,6)
     4    MEMO NO.                                 6    An$(15,6)
     5    RECORD TYPE = '000'                      3    An$(21,3)
     6    VENDOR NAME                             30    BN$
     7    INVOICE DATE                             6    CN$
     8    MEMO DATE                                6    DN$
     9    GROSS AMOUNT OF INVOICE                 11    AN ########.00
    10    GROSS ADJUSTMENT AMOUNT                 11    BN ########.00
    11    DEDUCTION AMOUNT                        11    CN ########.00
    12    1099 AMOUNT                             11    DN ########.00
    13    DISCOUNT ADJUSTMENT                     11    EN ########.00
    14    ADJUSTED VENDOR BALANCE                 11    FN ########.00
    15    (open)                                   1    EN$
    16    (OPEN)                                   1    FN$
    17    (open)                                   1    Gn$
FCAPAJD  -ADJUSTMENT JOURNAL ENTRY (DISTRIBUTION D  ( 72 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    VENDOR NO.                               6    AN$(3,6)
     3    VOUCHER NUMBER                           6    An$(9,6)
     4    MEMO NO.                                 6    An$(15,6)
     5    RECORD TYPE = '1'                        1    An$(21,1)
     6    RECORD COUNT                             2    An$(22,2) ##
     7    G/L ACCOUNT NO.                         11    BN$
     8    (open)                                   1    CN$
     9    REFER                                    4    DN$
    10    DISTRIBUTION AMOUNT                     11    An ########.00
    11    (open)                                   1    Bn
    12    (open)                                   1    Cn
    13    (open)                                   1    Dn
    14    (open)                                   1    En
    15    (open)                                   1    Fn
    16    PROJECT NO                               3    EN$
    17    DESCRIPTION                             30    FN$
    18    (OPEN)                                   1    GN$
FCCNOF   -VENDOR CHECK NUMBERS (KEYS ONLY) MAINT &  ( 73 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    CHECK NO.                                6    AN$(3,6)
     3    VENDOR NUMBER                            6    AN$(9,6)
     4    VOUCHER NUMBER                           6    AN$(15,6)
     5    VOUCHER DATE                             6    AN$(21,6)
     6    RECORD COUNT                             2    AN$(27,2)
     7    RECORD TYPE                              1    AN$(29,1)
FCEMP1   -P/R EMPLOYEE MASTER BASIC RECORD MAINT/INQUIRY  ( 74 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    EMPLOYEE NO.                             5    An$(3,5)
     3    EMPLOYEE NAME                           25    Bn$
     4    ADDRESS 1                               25    Cn$
     5    ADDRESS 2                               25    Dn$
     6    ADDRESS 3                               25    En$
     7    SOC.SEC.NO.                              9    Fn$
     8    TELEPHONE NO.                           10    Gn$
     9    ALPHA SORT KEY                           8    Hn$
    10    DATE HIRED                               6    In$(1,6)
    11    DATE TERMINATED                          6    In$(7,6)
    12    ANNIVERS DATE                            6    In$(13,6)
    13    BIRTHDATE                                6    In$(19,6)
    14    LAST PERIOD WKD                          6    In$(25,6)
    15    Last Review                              6    In$(31,6)
    16    PENSION ELIGIBIL                         6    In$(37,6)
    17    Last Raise                               6    In$(43,6)
    18    Raise Amount                             8    In$(49,8) #####.00
    19    HOME DEPARTMENT                          2    Jn$(1,2)
    20    HOME COST CENTER                         3    Jn$(3,3)
    21    NORMAL SHIFT                             2    Jn$(6,2)
    22    CONTRACT NUMBER                          6    Jn$(8,6)
    23    STATUS FLAG                              1    Kn$(1,1)
    24    PAY TYPE                                 1    Kn$(2,1)
    25    PAY CYCLE                                1    Kn$(3,1)
    26    MARITAL STATUS                           1    Kn$(4,1)
    27    FICA EXEMPT                              1    Kn$(5,1)
    28    AG.WORKER                                1    Kn$(6,1)
    29    REASON TERMINATED                        1    Kn$(7,1)
    30    PENSION STATUS                           1    Kn$(8,1)
    31    STATE TAX ABBR                           2    Kn$(9,2)
    32    LOCAL TAX CODE                           2    Kn$(11,2)
    33    UNION CODE                               3    Kn$(13,3)
    34    WORKER'S COMP CODE                       5    Kn$(16,5)
    35    SEX CODE                                 1    Kn$(21,1)
    36    E.I.C. FLAG                              2    Kn$(22,2)
    37    SECURITY FLAG                            1    Kn$(24,2)
    38    HOLIDAY PAY? (Y/N)                       1    Kn$(25,1)
    39    Driver's Lic #                          10    Kn$(26,10)
    40    Emerg Contact                           18    Kn$(36,18)
    41    Emerg Phone                             10    Kn$(54,10)
    42    (open)                                   1
    43    # EXEMPT-FED                             2    X(0) ##
    44    # EXEMPT-STATE                           2    X(1) ##
    45    # EXEMPT-LOCAL                           2    X(2) ##
    46    HOURLY RATE                              7    R(0) ##.00##
    47    SALARY RATE                              8    R(1) #####.00
    48    QTD - GROSS                             10    Q(0) #######.00
    49    QTD - FED TAX                            9    Q(1) ######.00
    50    QTD - FICA                               8    Q(2) #####.00
    51    QTD - STE TAX                            9    Q(3) ######.00
    52    QTD - LOC TAX                            8    Q(4) #####.00
    53    QTD - SDI                                8    Q(5) #####.00
    54    QTD - SICK PAY                           8    Q(6) #####.00
    55    QTD - E.I.C.                             8    Q(7) #####.00
    56    QTD - NON TXBL                           8    Q(8) #####.00
    57    QTD - # WEEKS WRKD                       2    Q(9) ##
FCEMP2   -EMPLOYEE MASTER, DEDUCTION RECORD  ( 75 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    EMPLOYEE NO.                             5    An$(3,5)
     3    401K DED                                 9    A(1) ####.00##
     4    Donation DED                             9    A(2) ####.00##
     5    Med Exp Ded                              9    A(3) ####.00##
     6    Admin Fees Ded                           9    A(4) ####.00##
     7    ADVANCES                                 9    A(5) ####.00##
     8    HEALTH INS                               9    A(6) ####.00##
     9    Child Care                               9    A(7) ####.00##
    10    MISC DED 1                               9    A(8) ####.00##
    11    MISC DED 2                               9    A(9) ####.00##
    12    MISC DED 3                               9    A(10) ####.00##
    13    MISC DED 4                               9    A(11) ####.00##
    14    MISC DED 5                               9    A(12) ####.00##
    15    401K IND                                 4    Bn$(1,4)
    16    Donation IND                             4    Bn$(5,4)
    17    Med Exp Ind                              4    Bn$(9,4)
    18    Admin Fees Ind                           4    Bn$(13,4)
    19    ADVANCES IND                             4    Bn$(17,4)
    20    HEALTH IND                               4    Bn$(21,4)
    21    Child Care Ind                           4    Bn$(25,4)
    22    MISC 1 IND                               4    Bn$(29,4)
    23    MISC 2 IND                               4    Bn$(33,4)
    24    MISC 3 IND                               4    Bn$(37,4)
    25    MISC 4 IND                               4    Bn$(41,4)
    26    MISC 5 IND                               4    Bn$(45,4)
    27    401K BAL                                 8    B(1) #####.00
    28    Donation BAL                             9    B(2) ######.00
    29    Med Exp Bal                              9    B(3) ######.00
    30    Admin Fees Bal                           9    B(4) ######.00
    31    ADVANCE BAL                              9    B(5) ######.00
    32    HEALTH BAL                               9    B(6) ######.00
    33    Child Care Bal                           9    B(7) ######.00
    34    MISC 1 BAL                               9    B(8) ######.00
    35    MISC 2 BAL                               9    B(9) ######.00
    36    MISC 3 BAL                               9    B(10) ######.00
    37    MISC 4 BAL                               9    B(11) ######.00
    38    MISC 5 BAL                               9    B(12) ######.00
    39    FED TAX INCR                             7    An ####.00
    40    STE TAX INCR                             7    Bn ####.00
    41    LOC TAX INCR                             6    Cn ###.00
    42    SICK ACCR %                              7    Dn #.00###
    43    VAC ACCR %                               7    En #.00###
    44    FED INC FLG                              1    Cn$(1,1)
    45    STE INC FLG                              1    Cn$(2,1)
    46    LOC INC FLG                              1    Cn$(3,1)
    47    G/L SUB-ACCT.                            3    Cn$(4,3)
    48    Link to Master                           1    Cn$(7,1)
    49    (OPEN)                                   3    Cn$(8,3)
FCEMP3   -EMPLOYEE MASTER FILE, Y-T-D RECORD  ( 76 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    EMPLOYEE NO.                             5    An$(3,5)
     3    REG EARNINGS                             9    C(1) ######.00
     4    OT EARNINGS                              9    C(2) ######.00
     5    PREM EARNINGS                            9    C(3) ######.00
     6    SICK EARNINGS                            9    C(4) ######.00
     7    HOL EARNINGS                             9    C(5) ######.00
     8    VAC EARNINGS                             9    C(6) ######.00
     9    OTHER EARNINGS                           9    C(7) ######.00
    10    FUNERAL EARNINGS                         9    C(8) ######.00
    11    BONUS EARNINGS                           9    C(9) ######.00
    12    PER DIEM EARN                            9    C(10) ######.00
    13    EXPENSE ALLOW                            9    C(11) ######.00
    14    MISC (TXBL)                              9    C(12) ######.00
    15    MISC (NONTX)                             9    C(13) ######.00
    16    COMMISSION                               9    C(14) ######.00
    17    GROSS EARNINGS                          10    An #######.00
    18    NET EARNINGS                             9    Bn ######.00
    19    FED WAGE TAX                             9    D(1) ######.00
    20    F.I.C.A.                                 8    D(2) #####.00
    21    STE WAGE TAX                             9    D(3) ######.00
    22    LOC WAGE TAX                             8    D(4) #####.00
    23    S.D.I.                                   8    D(5) #####.00
    24    E.I.C.                                   8    D(6) #####.00
    25    # WEEKS WORKED                           2    D(7) ##
    26    401K                                     8    H(1) #####.00
    27    LIFE INSURANCE                           8    H(2) #####.00
    28    Medical Exp                              8    H(3) #####.00
    29    Admin Fees                               8    H(4) #####.00
    30    ADVANCES                                 8    H(5) #####.00
    31    HEALTH INS                               8    H(6) #####.00
    32    Child Care                               8    H(7) #####.00
    33    MISC DEDUCTNS                            8    H(8) #####.00
    34    REG HOURS                                8    I(1) #####.00
    35    OT HOURS                                 8    I(2) #####.00
    36    PREM HOURS                               8    I(3) #####.00
    37    SICK HOURS                               8    I(4) #####.00
    38    HOL HOURS                                8    I(5) #####.00
    39    VAC HOURS                                8    I(6) #####.00
    40    OTHER HOURS                              8    I(7) #####.00
    41    FUNERAL HOURS                            8    I(8) #####.00
    42    SICK LEAVE ACCR                          8    J(1) #####.00
    43    VAC HOURS ACCR                           8    J(2) #####.00
    44    LIFETIME HOURS                           7    J(3) ####.00
    45    LIFETIME DAYS                            8    J(4) #####.00
    46    ABSENTEE POINTS                          4    J(5) ####
    47    Link to Master                           1    J(6) #
FCEMP4   -EMPLOYEE PAYROLL HISTORY FILE MAINTENANC  ( 77 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    EMPLOYEE NO.                             5    An$(3,5)
     3    CHECK NO.                                6    An$(8,6)
     4    SEQUENCE NO.                             1    An$(14,1)
     5    (OPEN)                                   1    Bn$
     6    CHECK TYPE                               1    Cn$(1,1)
     7    PAY CYCLE                                1    Cn$(2,1)
     8    PAY PERIOD                               2    Cn$(3,2)
     9    BONUS TAX CYCLE                          1    Cn$(5,1)
    10    LOCAL TAX EXEMPT                         1    Cn$(6,1)
    11    MISC EARN CDE                            1    Cn$(7,1)
    12    CHECK SEQ NO.                            1    Cn$(8,1)
    13    DEDUCTIONS?                              1    Cn$(9,1)
    14    PAY TYPE                                 1    Cn$(10,1)
    15    RELATIVE CODE                            2    Cn$(11,2)
    16    MISC EARN TXB?                           1    Cn$(13,1)
    17    STATE CODE                               1    Cn$(14,2)
    18    PERIOD ENDING                            6    Dn$(1,6)
    19    CHECK DATE                               6    Dn$(7,6)
    20    401K DED                                 7    B(1) ####.00
    21    LIFE INS DED                             7    B(2) ####.00
    22    Medical Exp                              7    B(3) ####.00
    23    Admin Fees                               7    B(4) ####.00
    24    ADVANCES DED                             7    B(5) ####.00
    25    HEALTH INS DED                           7    B(6) ####.00
    26    Child Care                               7    B(7) ####.00
    27    MISC DED #1                              7    B(8) ####.00
    28    MISC DED #2                              7    B(9) ####.00
    29    MISC DED #3                              7    B(10) ####.00
    30    MISC DED #4                              7    B(11) ####.00
    31    MISC DED #5                              7    B(12) ####.00
    32    MSC DED CDS(1-5)                         5    En$
    33    REG EARNINGS                             8    F(1) #####.00
    34    OT EARNINGS                              8    F(2) #####.00
    35    PREM EARNINGS                            8    F(3) #####.00
    36    SICK EARNINGS                            8    F(4) #####.00
    37    HOL EARNINGS                             8    F(5) #####.00
    38    VAC EARNINGS                             8    F(6) #####.00
    39    OTHER EARNINGS                           8    F(7) #####.00
    40    FUNERAL EARNINGS                         8    F(8) #####.00
    41    BONUS EARNINGS                           8    F(9) #####.00
    42    PER DIEM EARNINGS                        8    F(10) #####.00
    43    EXP ALLOW                                8    F(11) #####.00
    44    MISC EARNINGS                            8    F(12) #####.00
    45    COMMISSION EARNINGS                      8    F(13) #####.00
    46    REG HOURS                                7    N(1) ####.00
    47    OT HOURS                                 7    N(2) ####.00
    48    PREM HOURS                               7    N(3) ####.00
    49    SICK HOURS                               7    N(4) ####.00
    50    HOL HOURS                                7    N(5) ####.00
    51    VAC HOURS                                7    N(6) ####.00
    52    OTHER HOURS                              7    N(7) ####.00
    53    FUNERAL HOURS                            7    N(8) ####.00
    54    TAX - FEDERAL                            8    M(1) #####.00
    55    TAX - FICA                               8    M(2) #####.00
    56    TAX - STATE                              8    M(3) #####.00
    57    TAX - LOCAL                              8    M(4) #####.00
    58    TAX - SDI                                8    M(5) #####.00
    59        - EIC                                8    M(6) #####.00
    60    FED TAX INCR                             7    An ####.00
    61    STE TAX INCR                             7    Bn ####.00
    62    LOC TAX INCR                             7    Cn ####.00
    63    GROSS EARNINGS                           9    Dn ######.00
    64    NET EARNINGS                             9    En ######.00
    65    SICK HRS ACCR                            7    Fn ####.00
    66    VACN HRS ACCR                            7    Gn ####.00
    67    TOTAL DAYS                               3    Hn ###
    68    ABSENTEE POINTS                          3    In ###
FCVNMD   -Vendor Monthly Detail File  ( 78 at start)
     1    Company Code                             2    An$(1,2)
     2    Vendor Code                              6    An$(3,6)
     3    Voucher Number                           6    An$(9,6)
     4    Transaction Date                         6    An$(15,6)
     5    Sequence Number                          2    An$(21,2)
     6    Trans Type...VPA=vchr,pymt,adj           1    Bn$
     7    (open)                                   1    Cn$
     8    (open)                                   1    Dn$
     9    Reference Number                        12    En$
    10    (open)                                   1    Fn$
    11    Voucher Amount                          10    An #######.00
    12    Discount Amount                         10    Bn #######.00
    13    Payment Amount                          10    Cn #######.00
    14    (open)                                   1    Dn
FCVNMB   -  ( 79 at start)
     1    Company Code                             2    An$(1,2)
     2    Vendor Code                              6    An$(3,6)
     3    (open)                                   1    Bn$(1,1)
     4    Beginning Yr Balance                     9    C(0) ######.00
     5    Beginning Month Balance                  9    C(1) ######.00
     6    Curr Month - Vouchers Amt                9    C(2) ######.00
     7    Curr Month - Net Adj Amt                 9    C(3) ######.00
     8    Curr Month - Payment Amt                 9    C(4) ######.00
     9    (open)                                   1    C(5) #
    10    Cur Mth - # of vouchers                  3    D(2) ###
    11    Cur Mth - # of Adjustments               3    D(3) ###
    12    Cur Mth - # of checks                    3    D(4) ###
    13    (open)                                        D(5)
FCVNMB   -  ( 80 at start)
     1    Company Code                             2    An$(1,2)
     2    Vendor Number                            6    An$(3,6)
     3    Vendor Name                             35    Bn$
     4    Address Line 1                          35    Cn$
     5    Address Line 2                          35    Dn$
     6    Address Line 3                          35    En$
     7    Vendor Balance                          11    An ########.00
     8    Telephone Number                        10    Gn$
     9    Date Acct Opened                         6    Hn$
    10    Curr Yr Invoices                        11    Bn ########.00
    11    Curr Yr Disc Avail                      11    Cn ########.00
    12    Curr Yr Disc Taken                      11    Dn ########.00
    13    Prev Yr Invoices                        11    En ########.00
    14    Prev Yr Disc Avail.                     11    Fn ########.00
    15    Prev Yr Disc Taken                      11    Gn ########.00
    16    ANY CONTRACTS (Y/N)                      1    In$(1,1)
    17    F.O.B.(FOR P.O.)                         2    In$(2,2)
    18    TERMS (FOR P.O.)                         1    In$(4,1)
    19    Organic Cert? (Y/N)                      1    In$(5,1)
    20    BROKER CODE                              3    In$(6,3)
    21    G/L CATEG (0/1)                          1    In$(9,1)
    22    1099 ID NUMBER                          15    In$(10,15)
    23    Net Terms Days                           3    In$(25,3) ###
    24    Advertiser? (Y/N)                        1    In$(28,1)
    25    Fax Number                              10    In$(29,10) ##########
    26    Contact Name                            15    In$(39,15)
    27    Organic Cert on File?                    1    In$(54,1)
    28    Cert Exp Date                            6    In$(55,6)
    29    TERMS (PP/DDD)                           6    Jn$
    30    DATE LAST PURCHASE                       6    Kn$
    31    SORT KEY                                 8    Ln$
    32    1099 YTD BALANCE                        11    Hn ########.00
    33    BROKER PHONE                            10    Mn$
    34    BROKER NAME                             42    Nn$
    35    Standard G/L Expense Account            11    On$
FCVNMB   -  ( 81 at start)
     1    TAXING AUTH.                             6    An$
     2    AGGR INC SW                              1    An #
     3    STD DED %                                5    Bn .00##
     4    MAX STD DED                              9    Cn ######.00
     5    EXEMPTION IND                            1    Dn #
     6    1ST EXEMP AMT                            7    E(1) ####.00
     7    2ND EXEMP AMT                            7    E(2) ####.00
     8    OTHR EXMPT AMT                           7    E(3) ####.00
     9    FIT DED SWITCH                           1    Fn #
    10    %,1ST BRACKET                            5    G(0,0) .00##
    11    BS TAX,1ST BKT                           7    G(0,1) ####.00
    12    UP/LIM,IST BKT                           6    G(0,2) ######
    13    %,2ND BRACKET                            5    G(1,0) .00##
    14    BS TAX,2ND BKT                           7    G(1,1) ####.00
    15    UP/LIM,2ND BKT                           6    G(1,2) ######
    16    %,3RD BRACKET                            5    G(2,0) .00##
    17    BS TAX,3RD BKT                           7    G(2,1) ####.00
    18    UP/LIM,3RD BKT                           6    G(2,2) ######
    19    %,4TH BRACKET                            5    G(3,0) .00##
    20    BS TAX,4TH BKT                           7    G(3,1) ####.00
    21    UP/LIM,4TH BKT                           6    G(3,2) ######
    22    %,5TH BRACKET                            5    G(4,0) .00##
    23    BS TAX,5TH BKT                           7    G(4,1) ####.00
    24    UP/LIM,5TH BKT                           6    G(4,2) ######
    25    %,6TH BRACKET                            5    G(5,0) .00##
    26    BS TAX,6TH BKT                           7    G(5,1) ####.00
    27    UP/LIM,6TH BKT                           6    G(5,2) ######
    28    %,7TH BRACKET                            5    G(6,0) .00##
    29    BS TAX,7TH BKT                           7    G(6,1) ####.00
    30    UP/LIM,7TH BKT                           6    G(6,2) ######
    31    %,8TH BRACKET                            5    G(7,0) .00##
    32    BS TAX,8TH BKT                           7    G(7,1) ####.00
    33    UP/LIM,8TH BKT                           6    G(7,2) ######
    34    %,9TH BRACKET                            5    G(8,0) .00##
    35    BS TAX,9TH BKT                           7    G(8,1) ####.00
    36    UP/LIM,9TH BKT                           6    G(8,2) ######
    37    LOC TAX IND                              1    Hn #
FCPWKF   -P/R Check File  ( 82 at start)
     1    CO/EMPL/SEQ                              8    An$
     2    CHECK NUMBER                             6    Bn$
     3    CHECK TYPE                               1    Cn$(1,1)
     4    PAY CYCLE                                1    Cn$(2,1)
     5    PAY PERIOD                               2    Cn$(3,2)
     6    BONUS TAX CYCLE                          1    Cn$(5,1)
     7    LOCAL TAX EXEMPT                         1    Cn$(6,1)
     8    MISC EARN CDE                            1    Cn$(7,1)
     9    UPDATE FLAG                              1    Cn$(8,1)
    10    DEDUCTIONS? (Y/N)                        1    Cn$(9,1)
    11    PAY TYPE                                 1    Cn$(10,1)
    12    RELATIVE CODE                            2    Cn$(11,2)
    13    MISC EARN TXBL?                          1    Cn$(13,1)
    14    STATE CODE                               2    Cn$(14,2)
    15    PERIOD ENDING                            6    Dn$(1,6)
    16    CHECK DATE                               6    Dn$(7,6)
    17    401K DED                                 7    B(1) ####.00
    18    Donation DED                             7    B(2) ####.00
    19    Medical Exp                              7    B(3) ####.00
    20    Admin Fees                               7    B(4) ####.00
    21    ADVANCES DED                             7    B(5) ####.00
    22    HEALTH INS DED                           7    B(6) ####.00
    23    Child Care Ded                           7    B(7) ####.00
    24    MISC DED #1                              7    B(8) ####.00
    25    MISC DED #2                              7    B(9) ####.00
    26    MISC DED #3                              7    B(10) ####.00
    27    MISC DED #4                              7    B(11) ####.00
    28    MISC DED #5                              7    B(12) ####.00
    29    MISC DED CODES                           5    En$
    30    REG EARNINGS                             8    F(1) #####.00
    31    OT EARNINGS                              8    F(2) #####.00
    32    PREM EARNINGS                            8    F(3) #####.00
    33    SICK EARNINGS                            8    F(4) #####.00
    34    HOL EARNINGS                             8    F(5) #####.00
    35    VAC EARNINGS                             8    F(6) #####.00
    36    OTHER EARNINGS                           8    F(7) #####.00
    37    FUNERAL EARNINGS                         8    F(8) #####.00
    38    BONUS EARNINGS                           8    F(9) #####.00
    39    PER DIEM EARNINGS                        8    F(10) #####.00
    40    EXP ALLOW                                8    F(11) #####.00
    41    MISC EARNINGS                            8    F(12) #####.00
    42    COMMISSION EARNINGS                      8    F(13) #####.00
    43    REG HOURS                                7    N(1) ####.00
    44    OT HOURS                                 7    N(2) ####.00
    45    PREM HOURS                               7    N(3) ####.00
    46    SICK HOURS                               7    N(4) ####.00
    47    HOL HOURS                                7    N(5) ####.00
    48    VAC HOURS                                7    N(6) ####.00
    49    OTHER HOURS                              7    N(7) ####.00
    50    FUNERAL HOURS                            7    N(8) ####.00
    51    TAX - FEDERAL                            8    M(1) #####.00
    52    TAX - FICA                               8    M(2) #####.00
    53    TAX - STATE                              8    M(3) #####.00
    54    TAX - LOCAL                              8    M(4) #####.00
    55    TAX - SDI                                8    M(5) #####.00
    56        - EIC                                8    M(6) #####.00
    57    FED TAX INCR                             7    An ####.00
    58    STE TAX INCR                             7    Bn ####.00
    59    LOC TAX INCR                             7    Cn ####.00
    60    GROSS EARNINGS                           9    Dn ######.00
    61    NET EARNINGS                             9    En ######.00
    62    SICK HRS ACCR                            7    Fn ####.00
    63    VACN HRS ACCR                            7    Gn ####.00
    64    TOTAL DAYS                               3    Hn ###
    65    ABSENTEE POINTS                          3    In ###
FCITTB   -PAYROLL INSURANCE TAX TABLES FILE MAINT & INQUIRY  ( 83 at start)
     1    TAXING AUTH.                             4    An$
     2    MAXIMUM FEDERAL TAX                      8    An ########
     3    MAXIMUM STATE TAX                        9    Bn ######.00
     4    STD RATE/STATE UNEMPLY                   5    Cn .00##
     5    STD RATE/FEDERAL UNEMPLY                 5    Dn .00##
     6    STATE NAME                              16    Bn$
     7    S.D.I. MAXIMUM                           5    En #####
     8    S.D.I. RATE                              5    Fn .00##
FCGLJE   -G/L JOURNAL ENTRY WORK FILE  ( 84 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    JOURNAL NO.                              5    An$(3,5)
     3    LINE NO.                                 3    An$(8,3)
     4    G/L ACCOUNT                             11    Bn$
     5    ENTRY DATE                               6    Cn$(1,6)
     6    G/L PERIOD                               4    Cn$(7,4)
     7    DESCRIPTION                             40    Dn$
     8    ENTRY AMOUNT                            12    An #########.00
     9    (OPEN)                                   1    Bn
    10    TRANSACTION DESCRIPTION                 30    En$
    11    REFER                                    4    Fn$
    12    PROJECT NUMBER                           3    Gn$
FCCNVZ<  -FORMULA REVISION REASON CODE MASTER FILE  ( 85 at start)
     1    KEY GROUP = "<"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    JOURNAL NO.                              5    An$(4,5)
     4    DESCRIPTION                             20    Bn$
FCGLWF2  -GENERAL LEDGER BUDGET REPORT WORK FILE  ( 86 at start)
     1    OPTION (SPACE,1-5)                       1    An$(1,1)
     2    LINE NUMBER                              4    An$(2,4)
     3    G/L ACCOUNT                             11    An$(6,11)
     4    DESCRIPTION                             45    Bn$
     5    REVERSE SIGNS?                           1    Cn$
     6    CURRENT MONTH (BUDGET)                  12    An #########.00
     7    CURRENT MONTH (ACTUAL)                  12    Bn #########.00
     8    YEAR-TO-DATE (BUDGET)                   12    Cn #########.00
     9    YEAR-TO-DATE (ACTUAL)                   12    Dn #########.00
    10    SUB TOTAL FLAG 01                        1    F(1)
    11    SUB TOTAL FLAG 02                        1    F(2)
    12    SUB TOTAL FLAG 03                        1    F(3)
    13    SUB TOTAL FLAG 04                        1    F(4)
    14    SUB TOTAL FLAG 05                        1    F(5)
    15    SUB TOTAL FLAG 06                        1    F(6)
    16    SUB TOTAL FLAG 07                        1    F(7)
    17    SUB TOTAL FLAG 08                        1    F(8)
    18    SUB TOTAL FLAG 09                        1    F(9)
    19    SUB TOTAL FLAG 10                        1    F(10)
    20    SUB TOTAL FLAG 11                        1    F(11)
    21    SUB TOTAL FLAG 12                        1    F(12)
FCGLMS   -GENERAL LEDGER MASTER  ( 87 at start)
     1    COMPANY                                  2    An$(1,2)
     2    ACCOUNT                                  4    An$(3,4)
     3    SUB-ACCT                                 2    An$(7,2)
     4    Department                               3    An$(9,3)
     5    (OPEN)                                   2    An$(12,2)
     6    INC STMT LINE NO.                        4    Bn$(1,4)
     7    (OPEN)                                   4    Bn$(5,4)
     8    BUDGET #                                 4    Bn$(9,4)
     9    BAL SHEET #                              4    Bn$(13,4)
    10    DESCR'TN                                40    Cn$
    11    A/L/R/E/C FLG                            1    Dn$
    12    CR/DR IND                                1    En$
    13    RATIO IND                                1    Fn$
    14    L/YR AMT                                13    An ##########.00
    15    L/YR M-1                                13    B(1) ##########.00
    16    L/YR M-2                                13    B(2) ##########.00
    17    L/YR M-3                                13    B(3) ##########.00
    18    L/YR M-4                                13    B(4) ##########.00
    19    L/YR M-5                                13    B(5) ##########.00
    20    L/YR M-6                                13    B(6) ##########.00
    21    L/YR M-7                                13    B(7) ##########.00
    22    L/YR M-8                                13    B(8) ##########.00
    23    L/YR M-9                                13    B(9) ##########.00
    24    L/YR M-10                               13    B(10) ##########.00
    25    L/YR M-11                               13    B(11) ##########.00
    26    L/YR M-12                               13    B(12) ##########.00
    27    C/YR M-1                                13    C(1) ##########.00
    28    C/YR M-2                                13    C(2) ##########.00
    29    C/YR M-3                                13    C(3) ##########.00
    30    C/YR M-4                                13    C(4) ##########.00
    31    C/YR M-5                                13    C(5) ##########.00
    32    C/YR M-6                                13    C(6) ##########.00
    33    C/YR M-7                                13    C(7) ##########.00
    34    C/YR M-8                                13    C(8) ##########.00
    35    C/YR M-9                                13    C(9) ##########.00
    36    C/YR M-10                               13    C(10) ##########.00
    37    C/YR M-11                               13    C(11) ##########.00
    38    C/YR M-12                               13    C(12) ##########.00
    39    BUDG M-1                                13    D(1) ##########.00
    40    BUDG M-2                                13    D(2) ##########.00
    41    BUDG M-3                                13    D(3) ##########.00
    42    BUDG M-4                                13    D(4) ##########.00
    43    BUDG M-5                                13    D(5) ##########.00
    44    BUDG M-6                                13    D(6) ##########.00
    45    BUDG M-7                                13    D(7) ##########.00
    46    BUDG M-8                                13    D(8) ##########.00
    47    BUDG M-9                                13    D(9) ##########.00
    48    BUDG M-10                               13    D(10) ##########.00
    49    BUDG M-11                               13    D(11) ##########.00
    50    BUDG M-12                               13    D(12) ##########.00
FCGLMT   -MONTHLY GENERAL LEDGER DISTRIBUTION FILE  ( 88 at start)
     1    DISTRIBUTION TYPE                        1    An$(1,1)
     2    COMPANY                                  2    An$(2,2)
     3    G/L ACCOUNT NO.                         11    An$(4,11)
     4    TRANSACTION DATE                         6    An$(15,6)
     5    VENDOR/CUSTOMER                          6    An$(21,6)
     6    VOUCHER/INVOICE                          6    An$(27,6)
     7    SEQUENCE #                               2    AN$(33,2)
     8    REFERENCE                               40    Bn$
     9    DISTRIBUTION AMOUNT                     12    An #########.00
    10    # LINE ITEMS                             6    Bn ######
    11    (OPEN)                                   1    Cn
    12    TRANSACTION DESCRIPTION                 30    Cn$
    13    REFER                                    4    Dn$
    14    PROJECT NUMBER                           3    En$
FCGLTR   -GENERAL LEDGER TRANSACTION FILE MAINTENA  ( 89 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    G/L PERIOD                               4    An$(3,4)
     3    G/L ACCOUNT                             11    An$(7,11)
     4    JOURNAL NO.                              5    An$(18,5)
     5    SEQUENCE NO.                             4    An$(23,4)
     6    DATE UPDATED                             6    Bn$(1,6)
     7    TRANSACTION DATE                         6    Bn$(7,6)
     8    REFERENCE                               40    Cn$
     9    TRANSACTION AMOUNT                      12    An #########.00
    10    # OF LINES                               6    Bn ######
    11    (OPEN)                                   1    Cn
    12    TRANSACTION DESCRIPTION                 30    Dn$
    13    REFER                                    4    En$
    14    PROJECT #                                3    Fn$
    15    TRANSACTION NUMBER                       6    GN$
    16    (OPEN)                                   1    HN$
    17    (OPEN)                                   1    IN$
FCGLIS   -G/L INCOME STATEMENT LINE HEADING FILE  ( 90 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    Statement Type                           1    An$(3,1)
     3    LINE NUMBER                              4    An$(4,4)
     4    LINE HEADING/DESCR                      45    Bn$
     5    TYPE OF LINE                             1    Cn$
     6    REVERSE SIGNS?                           1    Dn$
     7    THIS YR-CURR MO/QTR AMT                 14    An ###########.00
     8    LAST YR-CURR MO/QTR AMT                 14    Bn ###########.00
     9    THIS YR-YTD AMOUNT                      14    Cn ###########.00
    10    LAST YR-YTD AMOUNT                      14    Dn ###########.00
    11    LAST YR-TOT AMT                         14    EN ###########.00
    12    SUB-TOTAL FLAG 01                        1    E(1) #
    13    SUB-TOTAL FLAG 02                        1    E(2) #
    14    SUB-TOTAL FLAG 03                        1    E(3) #
    15    SUB-TOTAL FLAG 04                        1    E(4) #
    16    SUB-TOTAL FLAG 05                        1    E(5) #
    17    SUB-TOTAL FLAG 06                        1    E(6) #
    18    SUB-TOTAL FLAG 07                        1    E(7) #
    19    SUB-TOTAL FLAG 08                        1    E(8) #
    20    SUB-TOTAL FLAG 09                        1    E(9) #
    21    SUB-TOTAL FLAG 10                        1    E(10) #
    22    SUB-TOTAL FLAG 11                        1    E(11) #
    23    SUB-TOTAL FLAG 12                        1    E(12) #
FCUDED   -DATA ENTRY DICTIONARY MAINTENANCE & INQU  ( 91 at start)
     1    Screen Name                              6    A0$(1,6)
     2    Sequence Number                          2    A0$(7,2)
     3    Description column no                    2    A0 ##
     4    Description Line no                      2    B0 ##
     5    Field Description                       50    B0$
     6    Entry Column no                          2    C0 ##
     7    Entry Line no                            2    D0 ##
     8    Entry Length                             2    E0 ##
     9    Field Type                               1    C0$(1,1)
    10    Padding Indicator                        1    C0$(2,1)
    11    Precision Indicator                      1    C0$(3,1)
    12    Date Indicator                           1    D0$(1,1)
    13    File Number                              3    Dn$(2,3) ###
    14    (open)                                   1    En$
    15    Documentation Code                       6    Fn$
FCOPST   -OPERATOR STATISTICS FILE MAINTENANCE & I  ( 92 at start)
     1    OPERATOR CODE                            3    AN$(1,3)
     2    TERMINAL ID                              2    AN$(4,2)
     3    DATE                                     6    AN$(6,6)
     4    TIME                                     7    AN$(12,7)
     5    SELECT NO.                              12    AN$(19,12)
     6    START/END IND                            1    AN$(31,1)
     7    TERMINAL DATE                            8    AN$(32,8)
FCOPERL  -System Log-on Operator Codes  ( 93 at start)
     1    Key Group = 'L'                          1    An$(1,1)
     2    System Log-on Operator Code              9    An$(2,9)
     3    FIS Operator Code                        3    Bn$
     4    Allowable terminals (CR=all)            30    Cn$
FCUDEH   -Data Entry Screen Control Record  ( 94 at start)
     1    '**'                                     2    An$(1,2)
     2    Data Entry Screen Name                   4    An$(3,4)
     3    Display Window: Upper Left Row           3    Cn ###
     4    Display Window: Upper Left Col           3    Dn ###
     5    Display Window: Lower Right Rw           3    En ###
     6    Display Window: Lower right Cl           3    Fn ###
FCPINI   -  ( 95 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    FILLER                                   1    An$(3,1)
     3    COMPANY NAME                            30    Bn$
     4    ADDRESS 1                               30    Cn$
     5    ADDRESS 2                               30    Nn$
     6    FEDERAL TAX ID NO.                       9    En$
     7    STATE TAX ID NO.                         8    Fn$
     8    WEEKLY-PERIOD ENDING DATE                6    Pn$(1,6)
     9    WEEKLY-CHECK DATE                        6    Dn$(1,6)
    10    WEEKLY-PERIOD NUMBER                     2    P(1) ##
    11    WEEKLY-PERIOD HOURS                      6    H(1) ###.00
    12    BI-WKLY-PERIOD ENDING DATE               6    Pn$(7,6)
    13    BI-WKLY-CHECK DATE                       6    Dn$(7,6)
    14    BI-WKLY-PERIOD NUMBER                    2    P(2) ##
    15    BI-WKLY-PERIOD HOURS                     6    H(2) ###.00
    16    SEMI-MTHLY-PERIOD ENDING                 6    Pn$(13,6)
    17    SEMI-MTHLY-CHECK DATE                    6    Dn$(13,6)
    18    SEMI-MTHLY-PERIOD NUMBER                 2    P(3) ##
    19    SEMI-MTHLY-PERIOD HOURS                  6    H(3) ###.00
    20    MONTHLY-PERIOD ENDING                    6    Pn$(19,6)
    21    MONTHLY-CHECK DATE                       6    Dn$(19,6)
    22    MONTHLY-PERIOD NUMBER                    2    P(4) ##
    23    MONTHLY-PERIOD HOURS                     6    H(4) ###.00
    24    (OPEN)                                   1    An #
    25    (OPEN)                                   1    Bn #
    26    (OPEN)                                   1    Cn #
    27    (OPEN)                                   1    Dn #
    28    (OPEN)                                   1    En #
FCOEBK   -Broker Statement Detail File  ( 96 at start)
     1    Company Code                             2    An$(1,2)
     2    Invoice Number                           6    An$(3,6)
     3    Release No                               2    An$(9,2)
     4    Key Type = '1'                           1    An$(11,1)
     5    Line Item                                3    An$(12,3)
     6    Line Item Amount                        12    An #########.00
     7    Commission Pct                           6    Bn ##.00#
     8    Commission Amt                          10    Cn #######.00
FCCNVZaa -Inventory Availability Codes  ( 97 at start)
     1    Key Group = "aa"                         2    AN$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Availability Code                        1    An$(5,1)
     4    Description                             30    Bn$
     5    Count as Lost Sales (Y/N)                1    Cn$(1,1)
     6    Lost Sales Category                      1    Cn$(2,1)
     7    Availability(Y/N/D/H)                    1    Cn$(3,1)
     8    (open)                                   2    Cn$(4,2)
     9    Invoice Print Msg                       40    Dn$
FCGLXR   -GENERAL LEDGER JOURNAL TRANSACTION XREF   ( 98 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    G/L PERIOD                               4    An$(3,4)
     3    JOURNAL NO.                              5    An$(7,5)
     4    G/L ACCOUNT                             11    An$(12,11)
     5    SEQUENCE NO.                             4    An$(23,4)
FCCBSF   -FILE LAYOUT DOCUMENTATION MAINT. & INQUI  ( 99 at start)
     1    DOC CODE                                 6    A0$(1,6)
     2    DOC SUFFIX (01-99)                       2    A0$(7,8) ##
     3    DOCUMENTATION FLD(1)                    30    B0$
     4    DOCUMENTATION FLD(2)                    30    C0$
FCCNVZY0 -Route Code  ( 100 at start)
     1    Record Type = 'Y0"                       2    An$(1,2)
     2    COMPANY                                  2    An$(3,2)
     3    Route Code                               3    An$(6,3)
     4    (open)                                   4    BN$
     5    DESCRIPTION                             30    Cn$
     6    WAREHOUSE CODE (TRUCK INVENTY)           4    Dn$
     7    LAST PICK LIST PRINT DATE                6    En$ ######
     8    LAST PICK LIST PRINT TIME                5    Fn$ ##.00
FCWRK1   -CBS SORT WORK FILE  ( 101 at start)
     1    SORT KEY                                15    AN$
FCCNVZE  -PAYROLL EMPLOYER STATE TAX I.D. NUMBERS  ( 102 at start)
     1    Key Type = 'E'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    State Abbreviation                       2    An$(4,2)
     4    State Tax I.D. Number                    8    Bn$
     5    State Name                              16    Cn$
     6    G/L Acct: State Tax W/H (CR)            11    Dn$
     7     - SDI Withheld (CR)                    11    En$
     8     - Employee FICA Withheld (CR)          11    Fn$
     9     - SUTA Payable                         11    Gn$
    10     - FUTA Payable (CR)                    11    Hn$
    11    941-A Report Type(0=wks,1=hrs)           1    An #
FCIPCT   -Catalog Section Headings  ( 103 at start)
     1    Company Code                             2    An$(1,2)
     2    Type(Intro,Sectn,Brand-I/S/B)            1    An$(3,1)
     3    Section Code                             2    An$(4,2)
     4    Brand Code                               2    An$(6,2)
     5    Sequence Number                          2    An$(8,2) ##
     6    Text Line 1                             30    Bn$
     7    Text Line 2                             30    Cn$
     8    Text Line 3                             30    Dn$
     9    Text Line 4                             30    En$
    10    Text Line 5                             30    Fn$
    11    Text Line 6                             30    Gn$
    12    Text Line 7                             30    Hn$
    13    Text Line 8                             30    In$
    14    Text Line 9                             30    Jn$
    15    Text Line 10                            30    Kn$
FCCNVZY1 -Geogaphic Territory Code  ( 104 at start)
     1    Record Type = 'Y1"                       2    An$(1,2)
     2    COMPANY                                  2    An$(3,2)
     3    Territory Code                           3    An$(6,3)
     4    (open)                                   4    BN$
     5    DESCRIPTION                             30    Cn$
     6    (open)                                   1    Dn$
     7    (open)                                   1    En$
     8    (open)                                   1    Fn$
FCTTTL   -CBS AUDIT FILE MAINTENANCE & INQUIRY  ( 105 at start)
     1    FILE NO.                                 3    AN$(1,3)
     2    FIELD NO.                                2    AN$(4,2)
     3    OPERATOR CODE                            3    AN$(6,3)
     4    DATE (YYMMDD)                            6    AN$(9,6)
     5    TIME (HHMMSS)                            6    AN$(15,6)
     6    AUDITED RECORD KEY                      32    BN$
     7    OLD FIELD DATA                          40    CN$
     8    NEW FIELD DATA                          40    DN$
     9    TERMINAL NO.                             2    E1$
FCCNVZi  -Inventory Cycle Count Codes  ( 106 at start)
     1    Key Type = "i"                           1    An$(1,1)
     2    Company Code                             2    An$(1,1)
     3    Cycle Count Code                         1    An$(4,1)
     4    Description                             30    Bn$
     5    (open)                                   1    Cn$
     6    Days Between Counts                      3    An ###
     7    (open)                                   1    Bn #
FCLMOD   -CBS SELECTOR/DATA ENTRY LOAD MODULE WORK  ( 107 at start)
     1    KEY TYPE = ag                            2    AN$(1,2)
FCCNVZab -Brand Master  ( 108 at start)
     1    Key Type = 'ab'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Catalog Section Code                     4    An$(5,4)
     4    Description                             35    Bn$
     5    Flag from conversion (Y/space)           1    Cn$(1,1)
     6    (open)                                   4    Cn$(2,4)
FCCNVZac -Catalog Category Descriptions  ( 109 at start)
     1    Key Type = 'ac'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Catalog Category Code                    6    An$(5,6)
     4    Description                             40    Bn$
     5    (open)                                   4    Cn$
     6    Bulk Index? (Y/N)                        1    Dn$(1,1)
     7    Organic? (Y/N)                           1    Dn$(2,1)
     8    Include UPC codes                        1    Dn$(3,1)
     9    (open)                                   7    Dn$(4,7)
FCCNVZag -INVENTORY G/L CATEGORY MAINTENANCE & INQUIRY  ( 110 at start)
     1    KEY TYPE = ag                            2    AN$(1,2)
     2    COMPANY                                  2    AN$(3,2)
     3    CODE                                     1    AN$(5,1)
     4    STANDARD G/L SUBACCT                     4    BN$(1,4)
     5    (OPEN)                                   6    BN$(5,6)
     6    DESCRIPTION                             20    CN$
FCITTC   -California Personal Exemption Deductions  ( 111 at start)
     1    Taxing Authority                         4    An$(1,4)
     2    Pay Cycle Code (1-4)                     1    An$(5,1)
     3    Sequence (0-9)                           1    An$(6,1)
     4    (open)                                   1    Bn$
     5    (open)                                   1    Bn #
     6    Credit Amt for claim 0 on W4             6    C(0) ###.00
     7      --- Claim 1                            6    C(1) ###.00
     8      --- Claim 2                            6    C(2) ###.00
     9      --- Claim 3                            6    C(3) ###.00
    10      --- Claim 4                            6    C(4) ###.00
    11      --- Claim 5                            6    C(5) ###.00
    12      --- Claim 6                            6    C(6) ###.00
    13      --- Claim 7                            6    C(7) ###.00
    14      --- Claim 8                            6    C(8) ###.00
    15      --- Claim 9                            6    C(9) ###.00
    16      --- Claim 10                           6    C(10) ###.00
FCCNVZ9  -G/L CONTROL RECORD - INCOME STATEMENT  ( 112 at start)
     1    KEY = "^Y"                               2    Zn$(1,2)
     2    COMPANY CODE                             2    Zn$(3,2)
     3    INCOME STMT #                            1    Zn$(5,1)
     4    LINE NO - GROSS PROFIT                   4    Z0 ####
     5    LINE NO - TOTAL SALES                    4    Z1 ####
     6    LINE NO - TOTAL COST/GOODS               4    Z2 ####
     7    LINE NO - NET INCOME                     4    Z3 ####
     8    LINE NO - TOTAL EXPENSE                  4    Z4 ####
FCCSXFN  -Customers Requiring Price Change Notices  ( 113 at start)
     1    Key Type = 'N'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Customer Code                            6    An$(4,6)
     4    Ship-to Code                             4    An$(10,4)
     5    Group (2/4/8)                            1    An$(14,1)
     6    Email Address                           40
     7    Additional Price Lists                   6
     8    Addl Email 1                            40    Dn$
     9    Addl Email 2                            40    En$
    10    Addl Email 3                            40    Fn$
    11    Advance Notification Days                3
    12    Customer PCNs,All,FullP/L(CAF)           1
FCDEST   -DATA ENTRY SCREEN SORT FILE  ( 114 at start)
     1    DOC NO.                                 12    AN$
     2    DATE ENT ID.                             6    BN$
FCCORE   -CBS SYSTEM PARAMETER SAVE FILE  ( 115 at start)
     1    KEY                                      2    A$
     2    SYSTEM CONTROL DATA                     38    Z$
     3    EXECUTION SEQ. (SELECTOR NOS.)          99    X0$
     4    FILES TO OPEN                           30    U0$
     5    LEAD PROGRAM                             6    V0$
     6    SELECT IND                               5    R0$
     7    SEL DOC NO.                             12    D0$
     8    SEL LOAD MODULE                          6    M0$
     9    SELECTION MESSAGE NO.                    2    Q0
    10    MSG PRFX/SUFX TEXT                      25    T0$
FCGHcc   -GENERAL LEDGER HISTORY FILE MAINTENANCE  ( 116 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    G/L ACCOUNT                             11    An$(3,11)
     3    G/L PERIOD (YYMM)                        4    An$(14,4)
     4    JOURNAL NO.                              5    An$(18,5)
     5    TRANSACTION DATE                         6    An$(23,6)
     6    SEQ. NUMBER                              4    An$(29,4)
     7    ENTRY DATE                               6    Bn$(1,6)
     8    TRANSACTION DATE                         6    Bn$(7,6)
     9    DESCRIPTION                             40    Cn$
    10    DISTRIBUTION AMOUNT                     12    An #########.00
    11    (OPEN)                                   1    Bn
    12    TRANSACTION DESCRIPTION                 30    Dn$
    13    REFER                                    4    En$
    14    PROJECT NUMBER                           3    Fn$
    15    TRANSACTION NUMBER                       6    GN$
    16    (OPEN)                                   1    HN$
    17    (OPEN)                                   1    IN$
FCINVC   -Catalog List File  ( 117 at start)
     1    Company Code                             2    An$(1,2)
     2    Catlog List ID                           6    An$(3,6)
     3    Item Code                                6    An$(9,6)
FCICDT   -INVENTORY MONTH-TO-DATE HISTORY FILE MAINTENANCE  ( 118 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    I/C PERIOD                               4    An$(3,4)
     3    WAREHOUSE                                4    An$(7,4)
     4    ITEM CODE                                8    An$(11,8)
     5    (OPEN)                                   4    An$(19,4)
     6    LOT                                      8    An$(23,8)
     7    SEQUENCE NO.                             4    An$(31,4)
     8    I/C PERIOD ENDING                        6    Bn$(1,6)
     9    TRANSACTION DATE                         6    Bn$(7,6)
    10    TRANS TYPE                               1    Cn$(1,1)
    11    PRICE UNITS                              2    Cn$(2,2)
    12    SALES UNITS                              2    Cn$(4,2)
    13    CUSTOMER CODE                            6    Cn$(6,6)
    14    SHIP-TO                                  2    Cn$(12,2)
    15    SALESMAN CODE                            3    Cn$(14,3)
    16    BROKER CODE                              3    Cn$(17,3)
    17    TAXING AUTHORITY                         2    Cn$(20,2)
    18    DESTINATION                              3    Cn$(22,3)
    19    TERRITORY                                3    Cn$(25,3)
    20    SALES CLASS                              4    Cn$(28,4)
    21    CUSTOMER TYPE                            2    Cn$(32,2)
    22    SALES CATEGORY                           1    Cn$(34,1)
    23    WHSE CATEGORY                            1    Cn$(35,1)
    24    G/L CATEGORY                             1    Cn$(36,1)
    25    REASON TYPE                              1    Cn$(37,1)
    26    REASON CODE                              2    Cn$(38,2)
    27    REFERENCE                               20    Dn$
    28    QUANTITY (UNITS)                         6    Q(0) ######
    29    WEIGHT (LBS)                            10    Q(1) #######.00
    30    (OPEN)                                   1    Q(2) #
    31    UNIT COST                               10    Q(3) #####.00##
    32    (OPEN)                                   1    Q(4) #
FCCNVZ*G1-GENERAL LEDGER CONTROL RECORD  ( 119 at start)
     1    KEY GROUP = *G1                          3    An$(1,3)
     2    COMPANY CODE                             2    An$(4,2)
     3    CURRENT INCOME                          12    Bn #########.00
     4    CURR YR INC ACCT                         8    Rn$
     5    STATUS-TRIAL BALANCE                     1    Dn$(1,1)
     6          -DETAIL REPORT                     1    Dn$(2,1)
     7          -UPDATE                            1    Dn$(3,1)
     8          -INC STMT                          1    Dn$(4,1)
     9          -BAL SHEET                         1    Dn$(5,1)
    10          -BUDGET                            1    Dn$(6,1)
    11    FISCAL YEAR (YY)                         2    Dn$(7,2)
    12    ACCOUNT TYPE                             1    Dn$(9,1)
    13    LENGTH OF ACCT - ENTRY                   2    Dn$(10,2) ##
    14    LENGTH OF ACCT - DISPLAY                 2    Dn$(12,2) ##
    15    DECIMAL PLACES TO REPORT                 1    Dn$(14,1)
    16    REPORT IN                                1    Dn$(15,1)
FCPOBF   -Supplier Broker File  ( 120 at start)
     1    Company Code                             2    An$(1,2)
     2    Broker Code                              6    An$(3,6)
     3    Broker Name                             30    Bn$
     4    Broker Address 1                        30    Cn$
     5    Broker Address 2                        30    Dn$
     6    Broker Address 3                        30    En$
     7    Telephone Number                        10    Fn$
     8    Fax Number                              10    Gn$
     9    Email Address                           40    Hn$
    10    Contact Name                            30    In$
    11    Contact Telephone                       10    Jn$
    12    Contact Cell                            10    Kn$
    13    Contact Email                           40    Ln$
    14    Comment Line 1                          40    Mn$
    15    Comment Line 2                          40    Nn$
    16    Supplier Number                          6    Mn$
FCCNVZw  -WAREHOUSE MASTER MAINTENANCE & INQUIRY  ( 121 at start)
     1    KEY TYPE = "w"                           1    AN$(1,1)
     2    WAREHOUSE NUMBER                         4    AN$(2,4)
     3    G/L RESP. SUB ACCT                       2    BN$(1,2)
     4    Pick List Printer ID                     2    BN$(3,2)
     5    Company Code                             2    BN$(5,2)
     6    Active Warehouse (0=no, 1=yes)           1    BN$(7,1)
     7    ORDER SEQUENCE                           3    BN$(8,3) ###
     8    (open)                                   4    Bn$(11,4)
     9    Cost From W/H                            4    Bn$(15,4)
    10    Name                                    30    CN$
    11    (open)                                   1    DN$
    12    (open)                                   1    EN$
    13    (open)                                   1    FN$
    14    State Code                               2    GN$
    15    (open)                                   1    HN$
    16    NEXT HISTORY SEQ                         5    IN
    17    PRIORITY ORDER NUMBERS                  60    JN$
FCCNVZw  -WAREHOUSE MASTER MAINTENANCE & INQUIRY  ( 122 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER CODE                            6    An$(3,6)
     3    SHIP-TO CODE                             2    An$(9,2)
     4    ITEM CODE                                6    An$(11,6)
     5    NORMAL ORDER QTY                         4    An ####
FCCNVZw  -WAREHOUSE MASTER MAINTENANCE & INQUIRY  ( 123 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    KEY TYPE = "R"                           1    An$(3,1)
     3    ROUTE CODE                               2    An$(4,2)
     4    ITEM CODE                                6    An$(6,6)
     5    DAY                                      1    An$(12,1)
     6    QUANTITY                                 4    AN ####
FCCNVZw  -WAREHOUSE MASTER MAINTENANCE & INQUIRY  ( 124 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    KEY TYPE = "C"                           1    An$(3,1)
     3    CUSTOMER NUMBER                          6    An$(4,6)
     4    SHIP-TO CODE                             2    An$(10,2)
     5    ITEM CODE                                6    An$(12,6)
     6    REGULAR/BROKEN/CASE (SP,B,C)             1    An$(17,1)
     7    NORMAL ORDER QTY                         4    An ####
FCCNVZw  -WAREHOUSE MASTER MAINTENANCE & INQUIRY  ( 125 at start)
     1    ITEM NUMBER                              6    AN$
     2    LAST FOB COST                           10    Bn
     3    RCVNG COST                              10    Cn #####.00##
     4    AP Cost                                 10    Dn #####.00##
FCOEIFC  -OPEN ORDER CUSTOMER XREF BY CUSTOMER NO   ( 126 at start)
     1    KEY TYPE = "C"                           1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    CUSTOMER NUMBER                          6    An$(4,6)
     4    CUSTOMER ORDER NUMBER                   20    An$(10,20)
     5    ORDER NUMBER                             6    An$(30,6)
     6    RELEASE NUMBER                           2    An$(36,2)
FCOETC   -Case Picking Xref - Area,loc,route  ( 127 at start)
     1    Key Group = 'I'                          1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Pick Area (1-99)                         2    An$(4,2) ##
     4    Bin Location                             6    An$(5,6)
     5    Route Code                               3    An$(12,3)
     6    (open)                                  10    An$(15,10)
     7    Item Code                               12    An$(25,12)
     8    Order Number & Release NO.               8    An$(37,8)
     9    Order Line Number                        3    An$(45,3)
    10    Reverse Stop Number                      3    An$(48,3)
FCOEIFS  -ROUTE/REVERSE STOP XREF FILE  ( 128 at start)
     1    KEY TYPE = "S"                           1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    ROUTE CODE                               3    An$(4,2)
     4    REVERSE STOP                             3    An$(6,2)
     5    ORDER NUMBER                             8    An$(24,8)
FCOEIFE  -Inventory Order Exceptions  ( 130 at start)
     1    Key Group = 'E'                          1    An$(1,1)
     2    Company code                             2    An$(2,2)
     3    Item Code                               12    An$(4,12)
     4    Exception Reason                         1    An$(16,1)
     5    Order Number                             6    An$(17,6)
     6    Release Number                           3    An$(23,2)
     7    Line Number                              3    An$(25,3)
FCOETE   -Each Picking Xref - Route,area,cust,loc  ( 131 at start)
     1    Key Group = 'J'                          1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Route Code                               3    An$(4,3)
     4    Picking Area                             2    An$(7,2)
     5    Customer Code                            6    An$(9,6)
     6    Ship-to Code                             4    An$(15,4)
     7    Bin Location                             6    An$(19,6)
     8    Item Code                               12    An$(25,12)
     9    Order Number & Release NO.               8    An$(37,8)
    10    Order Line Number                        3    An$(45,3)
    11    Reverse Stop Number                      3    An$(48,3)
FCNVPA   -Inventory Promotion Allowances  ( 132 at start)
     1    Company Code                             2    An$(1,2)
     2    Key Type: C=Cust, V=Vendor               1    An$(3,1)
     3    Item Code                                6    An$(4,6)
     4    Specific Customer or Blank              10    An$(10,10)
     5    Expiration Date                          6    An$(20,6)
     6    Effective Date                           6    An$(26,6)
     7    Amount(A) or Percent(P)                  1    Bn$(1,1)
     8    Vendor Bill-back (Y/N)                   1    Bn$(2,1)
     9    Bill-Back Cost/Whlsle                    1    Bn$(3,1)
    10    Cust P/A Price/Cost                      1    Bn$(4,1)
    11    (open)                                   1    Bn$(5,1)
    12    Comment                                 12    Bn$(6,12)
    13    Date Entered                             6    Bn$(18,6)
    14    (open)                                   7    Bn$(24,7)
    15    (open)                                   1    Cn$
    16    Selected Price Lists (sp=all)           24    Dn$
    17    Reg Cust Amount or Percent               9    En ####.00##
    18    Spec Cust Amount or Percent              9    Fn ####.00##
    19    Vendor Amount or Percent                 9    Gn ####.00##
    20    Minimum Quantity                         5    Hn #####
FCCSXF   -CUSTOMER ALPHA SORT FILE  ( 133 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    NAME (SORT KEY)                          8    An$(3,8)
     3    CUSTOMER NUMBER                          6    An$(10,6)
FCNXRFw  -INVENTORY XREF - WAREHOUSE RECORD  ( 134 at start)
     1    Key Type = "w"                           1    An$(1,1)
     2    Warehouse Code                           4    An$(2,4)
     3    Item Code                                6    An$(6,6)
     4    Company Code                             2    An$(12,2)
     5    Spaces + Company                         6    An$(14,6)
FCNVTY1  -INVENTORY MASTER (STATUS & DESCRIPTION)  ( 135 at start)
     1    Item Code                                6    An$(1,6)
     2    Company Code                             2    An$(7,2)
     3    Warehouse Number                         4    An$(9,4)
     4    4 SPACES + COMPANY                       6    An$(13,6)
     5    Key Type = '1**'                         3    An$(19,3)
     6    Available?                               1    Bn$(1,1)
     7    Contract Item?                           1    Bn$(2,1)
     8    Sales Category                           2    Bn$(3,2)
     9    G/L Category                             1    Bn$(5,1)
    10    Warehouse Category                       1    Bn$(6,1)
    11    Inv Units                                2    Bn$(7,2)
    12    Pric Units                               2    Bn$(9,2)
    13    P/O Units                                2    Bn$(11,2)
    14    Rtl Units                                2    Bn$(13,2)
    15    Rabbi Flag                               1    Bn$(15,1)
    16    MESG CD - OPER INST                      2    Bn$(16,2)
    17    MESG CD - ORDR PRT                       2    Bn$(18,2)
    18    MESG CD - PO PRT                         2    Bn$(20,2)
    19    MESG CD - INV PRT                        2    Bn$(22,2)
    20    FRESH/FROZ/DRY                           1    Bn$(24,1)
    21    Lot Control?                             1    Bn$(25,1)
    22    CATCH WGT?                               1    Bn$(26,1)
    23    SUBSTITUTES?                             1    Bn$(27,1)
    24    OTHER PACKAGING?                         1    Bn$(28,1)
    25    ABC Flag                                 1    Bn$(29,1)
    26    Whlsle Tax?                              1    Bn$(30,1)
    27    Catalog Section                          4    Bn$(31,4)
    28    Item Flag                                1    Bn$(35,1)
    29    Supl Item                               12    Bn$(36,12)
    30    Target Item(Y/N)                         1    Bn$(48,1)
    31    Pct Cost to Whlse                        6    Bn$(49,6) ###.00
    32    Pct Whlse to Retail                      6    Bn$(55,6) ###.00
    33    Whlse Rounding Method                    1    Bn$(61,1)
    34    Retail Rounding Method                   1    Bn$(62,1)
    35    CA Redemption Code                       2    Bn$(63,2)
    36    (open)                                   4    Bn$(65,4)
    37    Discount Units                           2    Bn$(69,2)
    38    Safety Stock (Wks)                       2    Bn$(71,2) ##
    39    Promo Cycle (MM)                         2    Bn$(73,2)
    40    Manf to Order?                           1    Bn$(75,1)
    41    New/Old Item Code                        6    Bn$(76,6)
    42    Split Case Code                          1    Bn$(82,1)
    43    Frt Units                                2    Bn$(83,2)
    44    P/O Un Wgt                              10    Bn$(85,10) #######.00
    45    Formula - Ingr                          10    Bn$(95,10)
    46    Formula - Pkg                           10    Bn$(105,10
    47    Non-GMO?                                 1    Bn$(115,1)
    48    Key Acct Item?                           1    Bn$(116,1)
    49    TradeMarkd                               2    Bn$(117,2)
    50    Kosher Catg                              1    Bn$(119,1)
    51    Catlog Loc                              10    Bn$(120,10
    52    Description                             40    Cn$(1,40)
    53    Size                                     8    Cn$(41,8)
    54    Retl Subpk                               4    Dn$(1,4) ####
    55    P/O Catg Code                            1    Dn$(5,1)
    56    UPC CODE                                12    Dn$(6,12)
    57    Prim Loc                                 6    Dn$(18,6)
    58    Primary Loc - EA                         6    Dn$(24,6)
    59    Upstock Locs 1-8 (6 chars ea)           48    Dn$(30,48)
    60    G/L Account - Sales                     11    En$
    61    Dt Ava/Dis                               6    Fn$(1,6)
    62    Date Last Sale                           6    Fn$(7,6)
    63    Dt Lst Rcp                               6    Fn$(13,6)
    64    Date Added                               6    Fn$(19,6)
    65    Old FOB Eff  date                        6    Fn$(25,6)
    66    Old FOB Exp Date                         6    Fn$(31,6)
    67    New FOB Eff Date                         6    Fn$(37,6)
    68    New FOB Exp Date                         6    Fn$(43,6)
    69    Old Landed Cost Eff Date                 6    Fn$(49,6)
    70    Old Landed Cost Exp Date                 6    Fn$(55,6)
    71    New Landed Eff Dt                        6    Fn$(61,6)
    72    New Landed Cost Exp Date                 6    Fn$(67,6)
    73    Date Last New Cost                       6    Fn$(73,6)
    74    Date Last Cost Change                    6    Fn$(79,6)
    75    Author Last Cost Change                  6    Fn$(85,6)
    76    Dt Lst Cnt                               6    Fn$(91,6)
    77    Hold Date                                6    Fn$(97,6)
    78    Old Each Price                          10    Fn$(105,10 #######.00
    79    New EA Prc                               8    Fn$(113,8) #####.00
    80    1st Rec Dt                               6    Fn$(121,6)
    81    1st Sale Dt                              6    Fn$(127,6)
    82    Supplier                                 6    Gn$(1,6)
    83    Each Pack Quantity                       6    Gn$(7,6) ######
    84    (open)                                   6    Gn$(13,6)
    85    Count Supp                               6    Gn$(19,6)
    86    Whsl Subpk                               6    Gn$(25,6) ####.0
    87    Un/Pallet                                6    Gn$(31,6) ######
    88    Usage Cd                                 1    Gn$(37,1)
    89    (open)                                  10    Gn$(38,10)
    90    Phy Count                                7    Gn$(48,7) #######
    91    Upstock Qty                              7    Gn$(55,7) #######
    92    Loc Max                                  6    Gn$(62,6) ######
    93    Case Dimn                               15    Gn$(68,10)
    94    Net Un Wt                                9    Hn  I(0) ######.00
    95    Grs Un Wt                                9    In  I(1) ######.00
    96    $ un/IC un                               9    Jn  I(2) ####.00##
    97    # Sls UN /MC                             9    Kn  I(3)
    98    Reorder Pt                               7    Ln  I(4) #######
    99    MAXIMUM STOCK LEVEL                      8    Mn  I(5) ########
   100    Qty on Hand                             11    Nn  I(6) ########.00
   101    I/C Units Committed                      9    On  I(7) ######.00
   102    I/C Units On Order                       9    Pn  I(8) ######.00
   103    Average Cost                            10    Qn  I(9) #####.00##
   104    Last FOB Cost                           10    Rn  I(10) #####.00##
   105    Unit Cube                                7    Sn  I(11) ####.00
   106    Quantity Allocated                       9    I(12) #########
   107    MTD Unit Sales                           6    I(13) ######
   108    YTD Unit Sales                           6    I(14) ######
   109    Beginning Balance                        6    I(15) ######
   110    Old Retail                               7    I(16) ####.00
   111    Old Wholesale                            9    I(17) #####.00#
   112    Old Landed Cost                          9    I(18) #####.00#
   113    Old FOB Cost                             9    I(19) ####.00##
   114    Frght/Hndlg                              9    I(20) ####.00##
   115    Disc/Allow Amt                           9    I(21) ####.00##
   116    New Retail                               7    I(22) ####.00
   117    New Whlsle                               9    I(23) #####.00#
   118    New Landed                               9    I(24) ####.00##
   119    New FOB Cost                             9    I(25) ####.00##
FCNVTY2  -INVENTORY PRICING RECORD FILE MAINTENANC  ( 136 at start)
     1    PRODUCT NUMBER                           6    An$(1,6)
     2    COMPANY CODE                             2    An$(7,2)
     3    WAREHOUSE NUMBER                         4    An$(9,4)
     4    4 SPACES + CO. CODE                      6    An$(13,6)
     5    RECORD TYPE = 2**                        3    An$(19,3)
     6    LINE TERMS                               1    Bn$(1,1)
     7    (open)                                   1    Bn$(2,1)
     8    (open)                                   2    Bn$(3,2)
     9    (open)                                   2    Bn$(5,2)
    10    (open)                                   3    Bn$(7,3)
    11    SPEC CUST PRICES?                        1    Bn$(10,1)
    12    Old Price Eff Date                       6    Cn$(1,6)
    13       -Expir Date                           6    Cn$(7,6)
    14       -Authorization                        6    Cn$(13,6)
    15    Date Last Change                         6    Cn$(19,6)
    16    Date New Price Changed                   6    Cn$(25,6)
    17    New Price Eff Date                       6    Dn$(1,6)
    18       -Expir Date                           6    Dn$(7,6)
    19    Old Price A Method                       1    En$(1,1)
    20       -Basis                                1    En$(2,1)
    21       -Rounding                             1    En$(3,1)
    22    (open)                                   1    En$(4,1)
    23    Repeat for P/L B-X                      92    En$(5,92)
    24    New Price A Method                       1    Fn$(1,1)
    25       -Basis                                1    Fn$(2,1)
    26       -Rounding                             1    Fn$(3,1)
    27    (open)                                   1    Fn$(4,1)
    28    Repeat for P/L B-X                      92    Fn$(5,92)
    29    Old A Pct/Price                          7    P(1) ####.00
    30     - B                                     7    P(2) ####.00
    31     - C                                     7    P(3) ####.00
    32     - D                                     7    P(4) ####.00
    33     - E                                     7    P(5) ####.00
    34     - F                                     7    P(6) ####.00
    35     - G                                     7    P(7) ####.00
    36     - H                                     7    P(8) ####.00
    37     - I                                     7    P(9) ####.00
    38     - J                                     7    P(10) ####.00
    39     - K                                     7    P(11) ####.00
    40     - L                                     7    P(12) ####.00
    41     - M                                     7    P(13) ####.00
    42     - N                                     7    P(14) ####.00
    43     - O                                     7    P(15) ####.00
    44     - Q                                     7    P(16) ####.00
    45     - Q                                     7    P(17) ####.00
    46     - R                                     7    P(18) ####.00
    47     - S                                     7    P(19) ####.00
    48     - T                                     7    P(20) ####.00
    49     - U                                     7    P(21) ####.00
    50     - V                                     7    P(22) ####.00
    51     - W                                     7    P(23) ####.00
    52     - X                                     7    P(24) ####.00
    53    New A Pct/Price                          7    N(1) ####.00
    54     - B                                     7    N(2) ####.00
    55     - C                                     7    N(3) ####.00
    56     - D                                     7    N(4) ####.00
    57     - E                                     7    N(5) ####.00
    58     - F                                     7    N(6) ####.00
    59     - G                                     7    N(7) ####.00
    60     - H                                     7    N(8) ####.00
    61     - I                                     7    N(9) ####.00
    62     - J                                     7    N(10) ####.00
    63     - K                                     7    N(11) ####.00
    64     - L                                     7    N(12) ####.00
    65     - M                                     7    N(13) ####.00
    66     - N                                     7    N(14) ####.00
    67     - O                                     7    N(15) ####.00
    68     - P                                     7    N(16) ####.00
    69     - Q                                     7    N(17) ####.00
    70     - R                                     7    N(18) ####.00
    71     - S                                     7    N(19) ####.00
    72     - T                                     7    N(20) ####.00
    73     - U                                     7    N(21) ####.00
    74     - V                                     7    N(22) ####.00
    75     - W                                     7    N(23) ####.00
    76     - X                                     7    N(24) ####.00
FCNVPX   -SPECIAL CUSTOMER PRICES XREF BY ITEM  ( 137 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    PRODUCT NUMBER                          12    An$(3,12)
     3    CUSTOMER CODE                            6    An$(15,6)
FCNVPRCI -Customer Item Special Prices  ( 138 at start)
     1    Key Group = "CI"                         2    An$(1,2))
     2    Company Code                             2    An$(3,2)
     3    Customer Code                            6    An$(5,6)
     4    Ship-to                                  4    An$(11,4)
     5    Item Code                                6    An$(13,6)
     6    Warehouse Code                           4    An$(19,4)
     7    (open)                                  12    Bn$
     8    Old Price - Effective Date               6    Cn$(1,6)
     9    Expiration date                          6    Cn$(7,6)
    10     - Usage (WC,WE)                         2    Cn$(13,2)
    11     - Calculation Method                    1    Cn$(15,1)
    12     - Basis to Use (" ",A-X)                1    Cn$(16,1)
    13    (open)                                   1    Cn$(17,1)
    14     - Rounding Method                       1    Cn$(18,1)
    15     - Authorized by                         6    Cn$(19,6)
    16    (open)                                   1    Cn$(25,1)
    17     - Date Last Changed                     6    CN$(26,6)
    18    Date Last New Price Change               6    Cn$(32,4)
    19     - Price or Percent                      9    Dn ####.00##
    20    New Price - Effective Date               6    En$(1,6)
    21     - Expiration Date                       6    En$(7,6)
    22     - Usage (WC,WE)                         2    En$(13,2)
    23     - Calculation Method                    1    En$(15,1)
    24     - Basis to use (" ",A-X)                1    En$(16,1)
    25    (open)                                   1    En$(17,1)
    26     - Rounding Method                       1    En$(18,1)
    27     - Authorized by                         6    En$(19,6)
    28    (open)                                   1    Dn$(25,1)
    29     - Price or Percentage                   9    Fn ####.00##
    30    Old P/A Amt or Pct (A,P)                 1    Gn$(1,1)
    31     - Effective Date                        6    Gn$(2,6)
    32     - Expiration Date                       6    Gn$(8,6)
    33     - Date Last Changed                     6    Gn$(14,6)
    34     - Promotion Amt or Pct                  9    Hn ####.00##
    35    New P/A Amt or Pct (A,P)                 1    In$(1,1)
    36     - Effective Date                        6    In$(2,6)
    37     - Expiration Date                       6    In$(8,6)
    38     - Date Last Changed                     6    In$(14,6)
    39     - Promotion Amt or Pct                  9    Jn ######.00
    40    Old Min Order - Units                    6    Q(1) ######
    41                  - Amount                   6    Q(2) ######
    42                  - Lbs                      6    Q(3) ######
    43    New Min Order - Units                    6    Q(4) ######
    44                  - Amount                   6    Q(5) ######
    45                  - Lbs                      6    Q(6) ######
    46    (OPEN)                                   1    Q(7)
FCCNVZ:  -SELECTOR ACCESS CONTROL FILE  ( 139 at start)
     1    Key Type = ":"                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Selector Number                          2    An$(4,2)
     4    (open)                                   1    Bn$
     5    Operator Codes                          66    Cn$
     6    Terminal ID's                           30    Dn$
     7    Access Ctl Method                        1    En$
FCCSMSB  -CUSTOMER MASTER FILE - DEFAULT SHIP-TO  ( 140 at start)
     1    Company Code                             2    An$(1,2)
     2    Customer No                              6    An$(3,6)
     3    Record Type ='1    '                     5    An$(9,5)
     4    Ship To Name                            30    Bn$
     5    Addr Line 1                             30    Cn$
     6    Addr Line 2                             30    Dn$
     7    Addr Line 3                             30    En$
     8    Zip Code                                10    Ln$
     9    (open) - do not use                      5    Fn$(1,5)
    10    MSI customer (Y/N)                       1    Fn$(6,1)
    11    Price List Code                          1    Fn$(7,1)
    12    (open)                                   1    Fn$(8,1)
    13    ORD PRINT MSG                            2    FN$(9,2)
    14    INV PRINT MSG                            2    FN$(11,2)
    15    OPER MESSAGE                             2    FN$(13,2)
    16    CONTACT FREQUENCY                        1    Fn$(15,1)
    17    Pick Prior(1-9)                          1    Fn$(16,1)
    18    Day Contacted                            1    Fn$(17,1)
    19    Last Ord Dt                              6    Fn$(18,6)
    20    Last Inv Dt                              6    Fn$(24,6)
    21    Service Days                             5    Fn$(30,5)
    22    # Holiday Gifts                          1    Fn$(35,1) #
    23    Last Ord No                              6    Fn$(36,6)
    24    Last Inv No                              6    Fn$(42,6)
    25    Service Rep                              3    Fn$(48,3)
    26    WAREHOUSE                                4    Fn$(51,4)
    27    Salesrep Code                            3    Fn$(55,3)
    28    Route code                               3    Fn$(58,3)
    29    Stop Number                              3    Fn$(61,3) ###
    30    TAX AUTH                                 2    Fn$(64,2)
    31    Territory Code                           3    Fn$(66,3)
    32    SOURCE CODE                              2    Fn$(68,2)
    33    Velocity Rpt(Y/N)                        1    Fn$(71,1)
    34    Catalog Catg                             1    Fn$(72,1)
    35    # Extra Labels                           1    Fn$(73,1) #
    36    Terms Code                               1    Fn$(74,1)
    37    BUILD-UP ITEMS?                          1    Fn$(75,1)
    38    DELIVERY DAYS                            3    FN$(76,3)
    39    Telephone No                            10    FN$(79,10)
    40    Key Account Code                         6    Fn$(89,6)
    41    PPD/Collect (P/C)                        1    Fn$(95,1)
    42    S/A Category                             2    Fn$(96,2)
    43    Price Labels (Y/N)                       1    Fn$(98,1)
    44    P/A Elg? (sp/N)                          1    Fn$(99,1)
    45    Price Label Title - 1                    6    Fn$(100,6)
    46    Price Label Title - 2                    6    Fn$(106,6)
    47    Order Days                               5    Fn$(112,5)
    48    Case Labels?                             1    Fn$(117,1)
    49    Contract Prices?                         1    Fn$(118,1)
    50    Carrier Code                             2    Fn$(119,2)
    51    Broker Code                              3    Fn$(121,3)
    52    (open)                                   1    Fn$(124,1)
    53    TEMP A/R $                               8    Bn #####.00
    54    ORDER FREQUENCY                          2    Cn ##
    55    Min Order $ Amt                          6    Dn ######
    56    WEIGHT LAST ORDER                        7    En #######
    57    TTL ORDER WEIGHT                         8    Fn ########
    58    TOTAL # ORDERS                           3    Gn ###
    59    Off Inv Disc %                           6    Hn ##.00#
    60    Maximum order amount                     1    In #
    61    Inv Svc Chg %                            5    Jn ###.0
    62    Spoilage Allowance                       5    Kn #.00#
    63    (open)                                   1    Ln #
    64    (open)                                   1    Mn #
    65    (open)                                   1    Nn #
    66    (open)                                   1    On #
    67    (open)                                   1    Pn #
    68    Sales Contact                           40    Qn$
    69    Delivery Instr.                         57    Gn$
    70    Fax Number                              10    Rn$(1,10)
    71    Bulk Cust Type                           2    Rn$(11,2)
    72    Route Code 2                             3    Rn$(13,3)
    73    Route Code 3                             3    Rn$(16,3)
    74    Route Code 4                             3    Rn$(19,3)
    75    Route Code 5                             3    Rn$(22,3)
    76    Stop Number 2                            3    Rn$(25,3) ###
    77    Stop Number 3                            3    Rn$(28,3) ###
    78    Stop Number 4                            3    Rn$(31,3) ###
    79    Stop Number 5                            3    Rn$(34,3) ###
    80    Prod Sls Rpt?                            1    Rn$(37,1)
FCCNVZA  -A/R BALANCE FORWARD CONTROL FILE  ( 141 at start)
     1    KEY GROUP = "A"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    TRADE: BEG. BALNCE                      12    An A(1) #########.00
     4           INVOICES                         12    Bn  A(2) #########.00
     5           CASH                             12    Cn  A(3) #########.00
     6           SERV. CHGS                       12    Dn  A(4) #########.00
     7           DR/CR MEMOS                      12    En  A(5) #########.00
     8           ADJUSTMENTS                      12    Fn  A(6) #########.00
     9    NON-TRD: BEG. BAL                       12    Gn  A(7) #########.00
    10             INVOICES                       12    Hn  A(8)) #########.00
    11             CASH                           12    In  A(9) #########.00
    12             SERV CHGS                      12    Jn  A(10) #########.00
    13             CR/DR MEMOS                    12    Kn  A(11) #########.00
    14             ADJUSTMENTS                    12    Ln  A(12) #########.00
    15           DISC TAKEN                       12    Mn  A(13) #########.00
    16           OTH ALLOW                        12    Nn  A(14) #########.00
    17             DISC TAKEN                     12    On  A(15) #########.00
    18             OTH ALLOW                      12    Pn  A(15) #########.00
    19           DISC GIVEN                       12    Qn  A(17) #########.00
    20             DISC GIVEN                     12    Rn  A(18) #########.00
FCOETP   -Customer Price Labels Xref - cust,descr  ( 142 at start)
     1    Key Group = 'P'                          1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Route Code                               3    An$(4,3)
     4    Customer Code                            6    An$(7,6)
     5    Ship-to Code                             4    An$(13,4)
     6    Item Description                        20    An$(17,20)
     7    Order Number & Release NO.               8    An$(37,8)
     8    Order Line Number                        3    An$(45,3)
     9    Reverse Stop Number                      3    An$(48,3)
FCRCKSA  -A/R CASH RECEIPTS CONTROL RECORDS  ( 143 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    FILL WITH Z'S                           11    An$(3,11)
     3    CONTROL CODE                             1    Bn$
     4    RECEIPT DATE                             6    Cn$
     5    TOTAL RECEIPT AMOUNT                    12    Dn #########.00
     6    NOT USED                                 1    En #
     7    NOT USED                                 1    Dn$
FCCNTG   -TAG ACCOUNTING FILE  ( 144 at start)
     1    COMPANY CODE                             2    AN$(1,2)
     2    NUMBER TYPE                              1    AN$(3,1)
     3    LAST # IN SERIES                         6    AN$(4,6) ######
     4    FIRST # IN SERIES                        6    AN$(10,6) ######
FCNVPRCC -Customer Category Special Prices  ( 145 at start)
     1    Key Group = 'CC'                         2    An$(1,2))
     2    Company Code                             2    An$(3,2)
     3    Customer Code                            6    An$(5,6)
     4    Ship-to                                  4    An$(11,2)
     5    Product Category                         2    An$(13,2)
     6    (open)                                  12    Bn$
     7    Old Price - Effective Date               6    Cn$(1,6)
     8    Expiration date                          6    Cn$(7,6)
     9     - Usage (WC,WE)                         2    Cn$(13,2)
    10     - Calculation Method                    1    Cn$(15,1)
    11     - Basis to Use (" ",A-X)                1    Cn$(16,1)
    12    (open)                                   1    Cn$(17,1)
    13     - Rounding Method                       1    Cn$(18,1)
    14     - Authorized by                         6    Cn$(19,6)
    15    (open)                                   1    Cn$(25,1)
    16     - Date Last Changed                     6    CN$(26,6)
    17    Date Last New Price Changed              6    Dn$(32,6)
    18     - Price or Percent                      9    Dn ####.00##
    19    New Price - Effective Date               6    En$(1,6)
    20     - Expiration Date                       6    En$(7,6)
    21     - Usage (WC,WE)                         2    En$(13,2)
    22     - Calculation Method                    1    En$(15,1)
    23     - Basis to use (" ",A-X)                1    En$(16,1)
    24    (open)                                   1    En$(17,1)
    25     - Rounding Method                       1    En$(18,1)
    26     - Authorized by                         6    En$(19,6)
    27    (open)                                   1    Dn$(25,1)
    28     - Price or Percentage                   9    Fn ####.00##
    29    Old P/A Amt or Pct (A,P)                 1    Gn$(1,1)
    30     - Effective Date                        6    Gn$(2,6)
    31     - Expiration Date                       6    Gn$(8,6)
    32     - Date Last Changed                     6    Gn$(14,6)
    33     - Promotion Amt or Pct                  9    Hn ####.00##
    34    New P/A Amt or Pct (A,P)                 1    In$(1,1)
    35     - Effective Date                        6    In$(2,6)
    36     - Expiration Date                       6    In$(8,6)
    37     - Date Last Changed                     6    In$(14,6)
    38     - Promotion Amt or Pct                  9    Jn ######.00
    39    Old Min Order - Units                    6    Q(1) ######
    40                  - Amount                   6    Q(2) ######
    41                  - Lbs                      6    Q(3) ######
    42    New Min Order - Units                    6    Q(4) ######
    43                  - Amount                   6    Q(5) ######
    44                  - Lbs                      6    Q(6) ######
    45    (OPEN)                                   1    Q(7)
FCNVPRRI -Customer Special Retail Item Prices  ( 146 at start)
     1    Key Group ='RI'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Customer Code                            6    An$(5,6)
     4    Ship-to                                  4    An$(11,2)
     5    Item Code                                6    An$(13,6)
     6    Warehouse Code                           4    An$(19,4)
     7    (open)                                  12    Bn$
     8    Old Price - Effective Date               6    Cn$(1,6)
     9    Expiration date                          6    Cn$(7,6)
    10     - Usage (RE)                            2    Cn$(13,2)
    11     - Calculation Method                    1    Cn$(15,1)
    12     - Basis to Use (" ",A-X)                1    Cn$(16,1)
    13    (open)                                   1    Cn$(17,1)
    14     - Rounding Method                       1    Cn$(18,1)
    15     - Authorized by                         6    Cn$(19,6)
    16    (open)                                   1    Cn$(25,1)
    17     - Date Last Changed                     6    CN$(26,6)
    18    Date Last New Price Change               6    Cn$(32,6)
    19     - Price or Percent                      9    Dn ####.00##
    20    New Price - Effective Date               6    En$(1,6)
    21     - Expiration Date                       6    En$(7,6)
    22     - Usage (RE)                            2    En$(13,2)
    23     - Calculation Method                    1    En$(15,1)
    24     - Basis to use (" ",A-X)                1    En$(16,1)
    25    (open)                                   1    En$(17,1)
    26     - Rounding Method                       1    En$(18,1)
    27     - Authorized by                         6    En$(19,6)
    28    (open)                                   1    Dn$(25,1)
    29     - Price or Percentage                   9    Fn ####.00##
    30    Old P/A Amt or Pct (A,P)                 1    Gn$(1,1)
    31     - Effective Date                        6    Gn$(2,6)
    32     - Expiration Date                       6    Gn$(8,6)
    33     - Date Last Changed                     6    Gn$(14,6)
    34     - Promotion Amt or Pct                  9    Hn ####.00##
    35    New P/A Amt or Pct (A,P)                 1    In$(1,1)
    36     - Effective Date                        6    In$(2,6)
    37     - Expiration Date                       6    In$(8,6)
    38     - Date Last Changed                     6    In$(14,6)
    39     - Promotion Amt or Pct                  9    Jn ######.00
    40    Old Min Order - Units                    6    Q(1) ######
    41                  - Amount                   6    Q(2) ######
    42                  - Lbs                      6    Q(3) ######
    43    New Min Order - Units                    6    Q(4) ######
    44                  - Amount                   6    Q(5) ######
    45                  - Lbs                      6    Q(6) ######
    46    (OPEN)                                   1    Q(7)
FCNVPRRC -Customer Special Retail Category Prices  ( 147 at start)
     1    Key Group = 'RC'                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Customer Code                            6    An$(5,6)
     4    Ship-to                                  4    An$(11,2)
     5    Category Code                            2    An$(13,2)
     6    (open)                                   6
     7    (open)                                  12    Bn$
     8    Old Price - Effective Date               6    Cn$(1,6)
     9    Expiration date                          6    Cn$(7,6)
    10     - Usage (RE)                            2    Cn$(13,2)
    11     - Calculation Method                    1    Cn$(15,1)
    12     - Basis to Use (" ",A-X)                1    Cn$(16,1)
    13    (open)                                   1    Cn$(17,1)
    14     - Rounding Method                       1    Cn$(18,1)
    15     - Authorized by                         6    Cn$(19,6)
    16    (open)                                   1    Cn$(25,1)
    17     - Date Last Changed                     6    CN$(26,6)
    18    Date Last New Price Change               6    Cn$(32,6)
    19     - Price or Percent                      9    Dn ####.00##
    20    New Price - Effective Date               6    En$(1,6)
    21     - Expiration Date                       6    En$(7,6)
    22     - Usage (RE)                            2    En$(13,2)
    23     - Calculation Method                    1    En$(15,1)
    24     - Basis to use (" ",A-X)                1    En$(16,1)
    25    (open)                                   1    En$(17,1)
    26     - Rounding Method                       1    En$(18,1)
    27     - Authorized by                         6    En$(19,6)
    28    (open)                                   1    Dn$(25,1)
    29     - Price or Percentage                   9    Fn ####.00##
    30    Old P/A Amt or Pct (A,P)                 1    Gn$(1,1)
    31     - Effective Date                        6    Gn$(2,6)
    32     - Expiration Date                       6    Gn$(8,6)
    33     - Date Last Changed                     6    Gn$(14,6)
    34     - Promotion Amt or Pct                  9    Hn ####.00##
    35    New P/A Amt or Pct (A,P)                 1    In$(1,1)
    36     - Effective Date                        6    In$(2,6)
    37     - Expiration Date                       6    In$(8,6)
    38     - Date Last Changed                     6    In$(14,6)
    39     - Promotion Amt or Pct                  9    Jn ######.00
    40    Old Min Order - Units                    6    Q(1) ######
    41                  - Amount                   6    Q(2) ######
    42                  - Lbs                      6    Q(3) ######
    43    New Min Order - Units                    6    Q(4) ######
    44                  - Amount                   6    Q(5) ######
    45                  - Lbs                      6    Q(6) ######
    46    (OPEN)                                   1    Q(7)
FCCNVZp  -CUSTOMER/CATEGORY PRICING FILE  ( 148 at start)
     1    Key Type = 'p'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Customer Code                            6    An$(4,6)
     4    Product Sales Category                   2    An$(10,2)
     5    Price List Code to Use                   1    Bn$(1,1)
     6    Retail Price List Code to Use            1    Cn$
FCCNVZ$  -PAYROLL MISCELLANEOUS DEDUCTIONS CODE CONTROL FILE  ( 149 at start)
     1    Key Type = '$'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Deduction Code                           1    An$(4,1)
     4    Description                             25    Bn$
     5    G/L Account (CR)                        11    Cn$
     6    Abbreviated Description                  3    Dn$
     7    Abbreviated Heading                      6    En$
     8    Stop When Bal is Zero (Y/N)              1    Fn$
     9    Federal Tax?                             1    Gn$(1,1)
    10    State Tax?                               1    Gn$(2,1)
    11    Local Tax?                               1    Gn$(3,1)
    12    F.I.C.A.?                                1    Gn$(4,1)
    13    S.D.I.?                                  1    Gn$(5,1)
FCNVTY5  -INVENTORY - REC # 5 = LIFO/FIFO  ( 150 at start)
     1    Item Code                                6    An$(1,6)
     2    Company Code                             2    An$(7,2)
     3    Whse Code                                4    An$(9,4)
     4    Spaces + Co                              6    An$(13,6)
     5    Type = "5**"                             3    An$(19,3)
     6    Lot No  1                                8    Bn$(1,8)
     7    Lot No  2                                8    Bn$(9,8)
     8    Lot No  3                                8    Bn$(17,8)
     9    Lot No  4                                8    Bn$(25,8)
    10    Lot No  5                                8    Bn$(33,8)
    11    Lot No  6                                8    Bn$(41,8)
    12    Lot No  7                                8    Bn$(49,8)
    13    Lot No  8                                8    Bn$(57,8)
    14    Lot No  9                                8    Bn$(65,8)
    15    Lot No 10                                8    Bn$(73,8)
    16    Lot No 11                                8    Bn$(81,8)
    17    Lot No 12                                8    Bn$(89,8)
    18    Rec Date  1                              6    Cn$(1,6)
    19    Rec Date  2                              6    Cn$(7,6)
    20    Rec Date  3                              6    Cn$(13,6)
    21    Rec Date  4                              6    Cn$(19,6)
    22    Rec Date  5                              6    Cn$(25,6)
    23    Rec Date  6                              6    Cn$(31,6)
    24    Rec Date  7                              6    Cn$(37,6)
    25    Rec Date  8                              6    Cn$(43,6)
    26    Rec Date  9                              6    Cn$(49,6)
    27    Rec Date 10                              6    Cn$(55,6)
    28    Rec Date 11                              6    Cn$(61,6)
    29    Rec Date 12                              6    Cn$(67,6)
    30    Link to Master                           1    Dn$(1,1)
    31    Link to P/O                              1    Dn$(2,1)
    32    (open)                                   1    En$
    33    (open)                                   1    Fn$
    34    (open)                                   1    Gn$
    35    Quantity  1                              6    Q(0) ######
    36    Quantity  2                              6    Q(1)
    37    Quantity  3                              6    Q(2)
    38    Quantity  4                              6    Q(3)
    39    Quantity  5                              6    Q(4)
    40    Quantity  6                              6    Q(5)
    41    Quantity  7                              6    Q(6) ######
    42    Quantity  8                              6    Q(7) ######
    43    Quantity  9                              6    Q(8) ######
    44    Quantity 10                              6    Q(9) ######
    45    Quantity 11                              6    Q(10) ######
    46    Quantity 12                              6    Q(11) ######
    47    Cost  1                                  9    C(0) ####.00##
    48    Cost  2                                  9    C(1) ####.00##
    49    Cost  3                                  9    C(2) ####.00##
    50    Cost  4                                  9    C(3) ####.00##
    51    Cost  5                                  9    C(4) ####.00##
    52    Cost  6                                  9    C(5) ####.00##
    53    Cost  7                                  9    C(6) ####.00##
    54    Cost  8                                  9    C(7) ####.00##
    55    Cost  9                                  9    C(8) ####.00##
    56    Cost 10                                  9    C(9) ####.00##
    57    Cost 11                                  9    C(10) ####.00##
    58    Cost 12                                  9    C(11) ####.00##
    59    (open)                                   1    Tn$
    60    (open)                                   1    Un$
FCTKXF   -STOCK RECEIPTS, TRANSFERS & ADJUSTMENTS  ( 151 at start)
     1    Company Code                             2    An$(1,2)
     2    Warehouse Code                           4    An$(3,4)
     3    Item Code                                6    An$(7,6)
     4    Lot Number                               8    An$(12,8)
     5    Sequence Number                          3    An$(20,3)
     6    Trans Type                               1    Bn$(1,1)
     7    Reason Code                              2    Bn$(2,2)
     8    To/From Warehouse                        4    Bn$(4,4)
     9    To/From Lot Number                       8    Bn$(8,8)
    10    Quantity                                 9    Cn ######.00
    11    Unit Cost                                9    Dn ####.00##
    12    Receipt Date                             6    En$
    13    Reference                               14    Fn$
    14    PR Units/IC Units                        1    Gn #
    15    PACK QTY                                 6    Hn ######
    16    (open)                                   1    In #
    17    Initials (Adj)                           3    Jn$
FCGLWF   -GENERAL LEDGER INCOME STATEMENT WORK FIL  ( 152 at start)
     1    TYPE = 1 OR 2                            1    An$(1,1)
     2    LINE NUMBER                              4    An$(2,4)
     3    G/L ACCOUNT                             11    An$(6,11)
     4    DESCRIPTION                             45    Bn$
     5    REVERSE SIGNS?                           1    Cn$
     6    THIS YEAR-CURR MTH/QTR AMOUNT           14    An ###########.00
     7    LAST YEAR-CURR MTH/QTR AMOUNT           14    Bn ###########.00
     8    THIS YEAR-YTD AMOUNT                    14    Cn ###########.00
     9    LAST YEAR-YTD AMOUNT                    14    Dn ###########.00
    10    PREVIOUS YEAR AMOUNT                    14    En
FCGLJS   -GENERAL LEDGER BUDGET CONTROL FILE MAINT  ( 153 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    TYPE = BLANK                             1    An$(3,1)
     3    BUDGET LINE NO.                          4    An$(4,4)
     4    LINE HEADING/DESCR                      45    Bn$
     5    TYPE OF LINE                             1    Cn$
     6    REVERSE SIGNS?                           1    Dn$
     7    CURRENT PERIOD (BUDGET)                 12    An #########.00
     8    CURRENT PERIOD (ACTUAL)                 12    Bn #########.00
     9    YEAR-TO-DATE (BUDGET)                   12    Cn #########.00
    10    YEAR-TO-DATE (ACTUAL)                   12    Dn #########.00
    11    SUB-TOTAL FLAG 01                        1    E(1) #
    12    SUB-TOTAL FLAG 02                        1    E(2) #
    13    SUB-TOTAL FLAG 03                        1    E(3) #
    14    SUB-TOTAL FLAG 04                        1    E(4) #
    15    SUB-TOTAL FLAG 05                        1    E(5) #
    16    SUB-TOTAL FLAG 06                        1    E(6) #
    17    SUB-TOTAL FLAG 07                        1    E(7) #
    18    SUB-TOTAL FLAG 08                        1    E(8) #
    19    SUB-TOTAL FLAG 09                        1    E(9) #
    20    SUB-TOTAL FLAG 10                        1    E(10) #
    21    SUB-TOTAL FLAG 11                        1    E(11) #
    22    SUB-TOTAL FLAG 12                        1    E(12) #
FCCNVZt  -FORM TYPE MASTER FILE  ( 154 at start)
     1    KEY GROUP = "t"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    TERMINATION CODE                         1    An$(4,1)
     4    DESCRIPTION                             25    Bn$
FCARGL   -NON A/R CASH RECEIPTS WORK FILE MAINTENA  ( 155 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CUSTOMER NUMBER                          6    An$(3,6)
     3    CHECK NUMBER                             5    An$(9,5)
     4    SEQUENCE COUNTER                         2    An$(14,2)
     5    CUSTOMER NAME                           40    Bn$
     6    TRANSACTION DATE                         6    Cn$
     7    TRANSACTION AMOUNT                      12    An
     8    ACCOUNT NUMBER                          11    Dn$
FCCNVZ&  -PAYROLL MISCELLANEOUS EARNINGS CODE CONTROL FILE  ( 156 at start)
     1    Key Type = '&'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Earnings Code                            1    An$(4,1)
     4    Description                             25    Bn$
     5    G/L Account for Expense (DR)            11    Cn$
     6    Federal Taxable (Y/N)                    1    Dn$(1,1)
     7    State Taxable (Y/N)                      1    Dn$(2,1)
     8    Local Taxable (Y/N)                      1    Dn$(3,1)
     9    Count as FICA earnings (Y/N)             1    Dn$(4,1)
    10    Count as SDI earnings (Y/N)              1    Dn$(5,1)
FCCNVZCSA-Sales Analysis Control Record  ( 157 at start)
     1    Key Type = 'CSA'                         3    An$(1,3)
     2    Company Code                             2    An$(4,2)
     3    Calendar or Fiscal Periods-C/F           1    Bn$(1,1)
     4    Report Cwt,Lb,Li on Detail Rpt           1    Bn$(2,1)
     5    Report Units,$ on Summary Rpts           1    Bn$(3,1)
     6    S/A Update Status (0/1)                  1    Bn$(4,1)
     7    (open)                                   1    Bn$(5,1)
     8    Current period (PP)                      2    Cn ##
     9    Last S/A Update                          6    Dn$
FCOEDA   -Daily Invoicing Totals  ( 158 at start)
     1    Company Code                             2    An$(1,2)
     2    Date...Year,Mo,Day(YYYYMMDD)             8    An$(3,8)
     3    Trans Type...I=Invoice,C=CM              1    An$(11,1)
     4    Invoice Count                            4    D(0) ####
     5    Line Item Count                          4    D(1) ####
     6    Dollar Sales                             9    D(2) ######.00
     7    Dollar Cost                              9    D(3) ######.00
     8    Dollar Discounts/Promotions              9    D(4) ######.00
     9    (open)                                   1    D(5) #
    10    Total Net Pounds                         9    D(6) ######.00
    11    Total Gross Pounds                       9    D(7) ######.00
    12    Shorts - No of Customers                 4    D(8) ####
    13    Shorts - Line Items                      4    D(9) ####
    14    Shorts - Dollar Amount                   9    D(10) ######.00
    15    (open)                                   1    D(11) #
    16    (open)                                   1    D(12) #
    17    (open)                                   1    D(13)
FCOEVL   -VENDOR LOST SALES FILE  ( 159 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    SUPPLIER NUMBER                          6    An$(3,6)
     3    Curr Week - Demand                       5    C(1) #####
     4              - Demand $                     9    C(2) ######.00
     5              - Shipped                      5    C(3) #####
     6              - Shipped $                    9    C(4) ######.00
     7              - Vend Out                     5    C(5) #####
     8              - Vend Out $                   9    C(6) ######.00
     9    (open)                                   1    C(7)
    10    (open)                                   1    C(8)
    11    Last Week - Demand                       5    L(1) #####
    12              - Demand $                     9    L(2) ######.00
    13              - Shipped                      5    L(3) #####
    14              - Shipped $                    9    L(4) ######.00
    15              - Vend Out                     5    L(5) #####
    16              - Vend Out $                   9    L(6) ######.00
    17    (open)                                   1    L(7)
    18    (open)                                   1    L(8)
    19    M-T-D  - Demand                          5    M(1) #####
    20           - Demand $                        9    M(2) ######.00
    21           - Shipped                         5    M(3) #####
    22           - Shipped $                       9    M(4) ######.00
    23           - Vend Out                        5    M(4) #####
    24           - Vend Out $                      9    M(6) ######.00
    25    (open)                                   1    M(7)
    26    (open)                                   1    M(8)
    27    Y-T-D  - Demand                          5    Y(1) #####
    28           - Demand $                        9    Y(2) ######.00
    29           - Shipped                         5    Y(2) #####
    30           - Shipped $                       9    Y(4) ######.00
    31           - Vend Out                        5    Y(5) #####
    32           - Vend Out $                      9    Y(6) ######.00
FCCNVZc  -INVENTORY ITEM UNIT CONVERSION  ( 160 at start)
     1    Key Group = "c"                          1    A$(1,1)
     2    Purchasing Unit                          2    A$(2,2)
     3    Inventory Unit                           2    A$(4,2)
     4    FACTOR                                   4    Bn ####
     5    INC/DEC IND.                             1    C$
FCRCKX   -Cash Deposit Xref by Entry Sequence  ( 161 at start)
     1    Company code                             2    An$(1,2)
     2    Entry Sequence                           6    An$(3,6)
     3    Customer Code                            6    An$(9,6)
     4    Check Number                             5    An$(15,5)
FCSACA   -CA Redemption Sales Detail  ( 162 at start)
     1    Company Code                             2    An$(1,2)
     2    Period (YYMM)                            4    An$(3,4) ####
     3    CA Redemption Code                       2    An$(7,2)
     4    Item Code                                6    An$(9,6)
     5    Invoice Number                           6    An$(15,6)
     6    Invoice Line Number                      3    An$(21,3)
     7    Quantity Sold                            5    Bn #####
FCPOSM   -SUPPLIER MASTER FILE  ( 163 at start)
     1    Company Code                             2    An$(1,2)
     2    SUPPLIER NUMBER                          6    An$(3,6)
     3    Supplier Name                           35    Bn$
     4    Address 1                               35    Cn$
     5    Address 2                               35    Dn$
     6    Address 3                               35    En$
     7    (open)                                   9    An #########
     8    TELEPHONE NO.                           10    Gn$
     9    Fax Number                              10    Hn$
    10    Lead Time (Wks)                          3    Bn ###
    11    Min Weight (LBS)                         5    Cn #####
    12    Min Amount ($)                           5    Dn #####
    13    Min Units                                5    En #####
    14    Ord Freq (Wks)                           2    Fn ##
    15    Safety Stk (Wks)                         2    Gn ##
    16    CONTRACTS? (Y/N)                         1    In$(1,1)
    17    FOB CODE                                 2    In$(2,2)
    18    TERMS CODE                               1    In$(4,1)
    19    CARRIER CODE                             2    In$(5,2)
    20    P/A Date (O/S)                           1    In$(7,1)
    21    (open)                                   1    In$(8,1)
    22    Rec P/O's?                               1    In$(9,1)
    23    VENDOR NUMBER                            6    In$(10,6)
    24    (open)                                   5    In$(16,5)
    25    Purchasing Agent                         3    In$(21,3)
    26    Broker Code                              6    In$(24,6)
    27    Mfg UPC Code                             6    Jn$
    28    DATE LAST RECEIPT                        6    Kn$
    29    SORT KEY                                 8    Ln$
    30    (open)                                   1    Hn
    31    Org Cert on File?                        1    Mn$(1,1)
    32    Non-GMO Vendor?                          1    Mn$(2,1)
    33    Co-Ins on File?                          1    Mn$(3,1)
    34    Cont Ltr Grntee?                         1    Mn$(4,1)
    35    Ad Contract on File?                     1    Mn$(5,1)
    36    Kosher?                                  1    Mn$(6,1)
    37    (open)                                   3    Mn$(7,2)
    38    Cert Exp Date                            6    Nn$(1,6)
    39    GMO Exp Date                             6    Nn$(7,6)
    40    Co-Ins Exp Date                          6    Nn$(13,6)
    41    Grntee Exp Date                          6    Nn$(19,6)
    42    Contract Exp Date                        6    Nn$(25,6)
    43    Kosher Exp Date                          6    Nn$(36,6)
    44    Organic Certifier                       25    On$(1,25)
    45    Kosher Certifier                        25    On$(26,25)
    46    PICKUP - Name                           30    Pn$
    47           - Addr 1                         30    Qn$
    48           - Addr 2                         30    Rn$
    49           - Addr 3                         30    Sn$
    50           - Tele #                         10    Tn$
FCPOXX   -PURCHASE ORDER AUDIT FILE  ( 164 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    ITEM CODE                                8    An$(3,8)
     3    P/O NUMBER                               5    An$(16,5) #####
     4    P/O LINE NO                              3    An$(16,3) ###
     5    QTY ORDERED                              8    An #####.00
     6    QTY RECEIVED                             8    Bn #####.00
     7    QTY UPDATED                              8    Cn #####.00
FCPOPU   -PURCHASING UNITS CONVERSION FILE  ( 165 at start)
     1    Alternate Unit of Measure                2    AN$(1,2)
     2    Inventory Unit of Measure                2    AN$(3,2)
     3    Item Code (Spaces=ALL)                   8    An$(5,8)
     4    No Alt Units/Inv Unit                   10    AN #####.00##
     5    OPEN                                     1    BN
     6    OPEN                                     1    CN
     7    OPEN                                     1    BN$
FCICcc   -PHYSICAL INVENTORY COUNT FILE  ( 166 at start)
     1    Company Code                             2    An$(1,2)
     2    Warehouse Code                           4    An$(3,4)
     3    Location Code                            6    An$(7,6)
     4    Item Code                                6    An$(13,6)
     5    Units                                    2    Bn$(1,2)
     6    Supplier Code                            6    Bn$(3,6)
     7    Item Description                        40    Cn$(1,40)
     8    Size                                     8    Cn$(41,8)
     9    Book Quantity                           10    Dn ######.00#
    10    Count String                            50    En$
    11    Count in Units                          10    Fn ######.00#
    12    Unit Cost                                8    Gn ####.00#
    13    Computed Variance                       10    Hn ######.00#
    14    Total Count                             10    In ######.00#
    15    Quantity on Hand                        10    Jn ######.00#
    16    Pack Quantity                            6    Kn ######
    17    Expiration Date                          6    Ln$
FCICAI   -ADD ITEM ENTRY FILE  ( 167 at start)
     1    COMPANY                                  2    An$(1,2)
     2    WAREHOUSE                                4    An$(3,4)
     3    ITEM CODE                                6    An$(7,6)
     4    PROMOTION START DATE                     6    Bn$(1,6)
     5    PROMOTION END DATE                       6    Bn$(7,6)
     6    NEXT PROMOTION DATE                      6    Bn$(13,6)
     7    OPEN FIELD                               1    Cn$
     8    OPEN FILED                               1    Dn$
     9    PROMOTION AMOUNT                         6    An ###.00
FCICAS   -AD ITEM ENTRY SORT FILE  ( 168 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    WAREHOUSE CODE                           4    An$(3,4)
     3    PROMOTION END DATE                       6    An$(7,6)
     4    ITEM CODE                                6    An$(13,6)
     5    OPEN FIELD                               1    Bn$
     6    OPEN FIELD                               1    An #
FCPORN   -RESERVED PURCHASE ORDER NUMBER FILE  ( 169 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    P/O NUMBER                               5    An$(3,5) #####
     3    SUPPLIER NUMBER                          6    Bn$
     4    P/O PLACED BY/FOR                       20    Cn$
     5    P/O ISSUED TO                           20    Dn$
     6    COMMENTS                                20    En$
     7    DATE RESERVED                            6    Fn$(1,6)
     8    RESERVED BY                              3    Fn$(7,3)
FCCNVZCAR-A/R APPLICATION CONTROL RECORD  ( 170 at start)
     1    Key Group = 'CAR'                        3    An$(1,3)
     2    Company Code                             2    AN$(4,2)
     3    Company Name for A/R                    40    BN$
     4    A/R History (Y/N) ?                      1    CN$(1,1)
     5    Update G/L Monthly (Y/N=Daily)           1    Cn$(2,1)
     6    Post Directly to G/L Hist(Y/N)           1    Cn$(3,1)
     7    Salesrep(S) or Brokers(K)                1    Cn$(4,1)
     8    Deposit Register By Rep(Y/N)             1    Cn$(5,1)
     9    Age by Terms or Invc Date(T/I)           1    Cn$(6,1)
    10    Print Credit Statements (Y/N)?           1    Cn$(7,1)
    11    Print Zero Bal Statemts(Y/N)?            1    Cn$(8,1)
    12    Age Credit Memos(Date,Cur,Old)           1    Cn$(9,1)
    13    Temp Invc Reg by INVC,CUST-I/C           1    Cn$(10,1)
    14    Include Zero Bal on Aging(Y/N)           1    Cn$(11,1)
    15    Sep Stmts by Ship-to(Y/N)                1    Cn$(12,1)
    16    Allow Petty Cash Checks(Y/N)             1    Cn$(13,1)
    17    Deposit Seq by Cust/Entry(C/E)           1    Cn$(14,1)
    18    Current A/R Month                        2    Cn$(15,2) ##
    19    Last Month End                           6    Cn$(17,6)
    20    Days Late #1 - Regular Aging             3    DN$(1,3)
    21    Days Late #2 - Regular Aging             3    DN$(4,3)
    22    Days Late #3 - Regular Aging             3    DN$(7,3)
    23    Days Late for Finance Charges            3    EN ###
    24    Finance Charge Percentage                5    FN ##.00
    25    Gross Margin Mask                       10    GN$
    26    Minimum Finance Charge Amount            4    HN ##.0
    27    No. Days Late for Delinq Aging           3    In ###
    28    Days Late #1 - Delinquent Rpt            3    JN$(1,3)
    29    Days Late #2 - Delinquent Rpt            3    JN$(4,3)
    30    Days Late #3 - Delinquent Rpt            3    JN$(7,3)
    31    Terms Codes for CASH & COD               6    Kn$
    32    Number of Months of A/R Hist             5    Ln #####
FCCNVZCAP-AP APPLICATION CONTROL FILE  ( 171 at start)
     1    KEY TYPE = "CAP"                         3    An$(1,3)
     2    COMPANY CODE                             2    An$(4,2)
     3    OPEN PAYABLES (Y/N)                      1    Bn$(1,1)
     4    CHECK HISTORY (Y/N)                      1    Bn$(2,1)
     5    VOUCHER CONTROL (A=AUTO,V=VER)           1    Bn$(3,1)
     6    G/L UPDATED MONTHLY? (Y/N)               1    Bn$(4,1)
     7    POST TO G/L HISTORY? (Y/N)               1    Bn$(5,1)
     8    MULTIPLE CASH ACCTS? (Y/N)               1    Bn$(6,1)
     9    Date for G/L Posting                     1    Bn$(7,1)
    10    Reports by Invc/Terms dte(I/T)           1    Bn$(8,1)
    11    (open)                                   2    Bn$(9,2)
    12    CURRENT CASH ACCT CODE                   1    C$(1,1)
    13    (OPEN)                                   4    C$(2,4)
    14    (OPEN)                                   1    D$
    15    (OPEN)                                   1    E$
    16    No.Months of Voucher History             2    AN ##
    17    (OPEN)                                   1    BN
    18    (OPEN)                                   1    CN
FCCNVZCGL-G/L APPLICATION CONTROL RECORDD  ( 172 at start)
     1    KEY TYPE - 'CGL'                         3    An$(1,3)
     2    COMPANY CODE                             2    An$(4,2)
     3    G/L HISTORY (Y/N)                        1    Bn$(1,1)
     4    MULTIPLE INCOME STMT FORMATS?            1    Bn$(2,1)
     5    Full G/L Installed (Y/N)                 1    Bn$(3,1)
     6    (OPEN)                                   7    Bn$(4,7)
FCCNVZj  -STOCK ADJUSTMENT REASON CODE FILE  ( 173 at start)
     1    Key Type = "j"                           1    An$(1,1)
     2    Reason Code                              2    An$(2,2)
     3    Description                             15    BN$
     4    G/L Account                             11    Cn$ ###########
FCPOTR   -PURCHASE TREND FILE  ( 174 at start)
     1    ITEM CODE                                6    An$(1,6)
     2    COMPANY CODE                             2    An$(7,2)
     3    WAREHOUSE                                4    An$(9,4)
     4    4 SPACES + COMPANY                       6    An$(13,6)
     5    RECORD TYPE = "1**"                      3    An$(19,3)
     6    DATE LAST UPDATED                        6    Bn$(1,6)
     7    (open)                                   6    Bn$(7,6)
     8    RECEIPTS -   TOTAL                       6    A(0) ######
     9             - WEEK 01                       6    A(1) ######
    10             - WEEK 02                       6    A(2) ######
    11             - WEEK 03                       6    A(3) ######
    12             - WEEK 04                       6    A(4) ######
    13             - WEEK 05                       6    A(5) ######
    14             - WEEK 06                       6    A(6) ######
    15             - WEEK 07                       6    A(7) ######
    16             - WEEK 08                       6    A(8) ######
    17             - WEEK 09                       6    A(9) ######
    18             - WEEK 10                       6    A(10) ######
    19             - WEEK 11                       6    A(11)) ######
    20             - WEEK 12                       6    A(12) ######
    21             - WEEK 13                       6    A(13) ######
FCCNVZCOE-ORDER PROCESSING APPLICATION CONTROL REC  ( 175 at start)
     1    Key Group = "COE"                        3    An$(1,3)
     2    Company Code                             2    An$(4,2)
     3    Order No Req for DM/CM (Y/N)             1    Bn$(1,1)
     4    Invoice# Same as Order# (Y/N)            1    Bn$(2,1)
     5    Pick List Sequence                       1    Bn$(3,1)
     6    Invoice Sequence                         1    Bn$(4,1)
     7    Automatic Lot Assignment(Y/N)            1    Bn$(5,1)
     8    Automatic Selection of Shorts            1    Bn$(6,1)
     9    Print Shorts at End of Picklst           1    Bn$(7,1)
    10    Print Shorts at End of Invoice           1    Bn$(8,1)
    11    How to Print Promotions                  1    Bn$(9,1)
    12    Sales Tax Charged (Y/N)                  1    Bn$(10,1)
    13    Default Alloc Shortage Reason            1    Bn$(11,1)
    14    Backorders (Y/N) ?                       1    Bn$(12,1)
    15    Detail Pricing of Open Ord(YN)           1    Bn$(13,1)
    16    Print Case Labels (Y/N) ?                1    Bn$(14,1)
    17    Print Each Labels (Y/N) ?                1    Bn$(15,1)
    18    Print Price Stickers (Y/N) ?             1    Bn$(16,1)
    19    Week Starting Date (Mon)                 6    Bn$(17,6)
    20    Auto Daily S/A Update? (Y/N)             1    Bn$(23,1)
    21    Each Quantity Execption Limit            3    Cn ###
    22    Line Extension Limit-Dollars             5    Dn #####
    23    Credits: # days old allowed              3    En ###
    24    Num weeks of invoice history             2    Fn ##
    25    Case Quantity Exception-units            3    Gn ###
    26    Discount Item Code                       6    Hn$(1,6)
    27    Spoilage Item Code                       6    Hn$(7,6)
    28    Svc Chg Item Code                        6    Hn$(13,6)
FCCNVZH  -DIVISION CONTROL RECORDS  ( 176 at start)
     1    KEY GROUP = pv                           2    An$(1,2)
     2    COMPANY CODE                             2    An$(3,2)
     3    DIVISION CODE                            1    An$(5,1)
     4    DESCRIPTION                             30    Bn$
     5    (open)                                   6    Cn$
FCCNVZ/  -DEPARTMENT CONTROL RECORDS MAINTENANCE &  ( 177 at start)
     1    KEY GROUP = pd                           2    An$(1,2)
     2    COMPANY CODE                             2    An$(3,2)
     3    DEPARTMENT CODE                          3    An$(5,3)
     4    DESCRIPTION                             30    Bn$
     5    PAYROLL UNEMPL COMP ACCOUNT             11    Cn$
FCCNVZe  -COST CENTER CONTROL RECORDS MAINTENANCE & INQUIRY  ( 178 at start)
     1    Key Type = 'e'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Cost Center Code                         3    An$(4,3)
     4    Description                             25    Bn$
     5    G/L Accont for Expense (DR)             11    Cn$
FCCNVZn  -EMPLOYEE RELATIVE CODES MASTER FILE MAINTENANCE  ( 179 at start)
     1    KEY GROUP = "n"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    RELATIVE CODE                            2    An$(4,2)
     4    DESCRIPTION                             25    Bn$
     5    (OPEN)                                   1    Cn$
FCGLBS   -G/L BALANCE SHEET CONTROL FILE  ( 180 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    TYPE = BLANK                             1    An$(3,1)
     3    BALANCE SHEET LINE NO.                   4    An$(4,4)
     4    LINE HEADING/DESCR                      45    Bn$
     5    TYPE OF LINE                             1    Cn$
     6    REVERSE SIGNS?                           1    Dn$
     7    END OF CURRENT PERIOD                   14    An ###########.00
     8    END OF PRIOR PERIOD                     14    Bn ###########.00
     9    PRIOR YEAR END                          14    Cn ###########.00
    10    A-V-A-I-L-A-B-L-E                       14    Dn ##############
    11    (open)                                   1    En
    12    SUB-TOTAL FLAG 01                        1    E(1) #
    13    SUB-TOTAL FLAG 02                        1    E(2) #
    14    SUB-TOTAL FLAG 03                        1    E(3) #
    15    SUB-TOTAL FLAG 04                        1    E(4) #
    16    SUB-TOTAL FLAG 05                        1    E(5) #
    17    SUB-TOTAL FLAG 06                        1    E(6) #
    18    SUB-TOTAL FLAG 07                        1    E(7) #
    19    SUB-TOTAL FLAG 08                        1    E(8) #
    20    SUB-TOTAL FLAG 09                        1    E(9) #
    21    SUB-TOTAL FLAG 10                        1    E(10) #
    22    SUB-TOTAL FLAG 11                        1    E(11) #
    23    SUB-TOTAL FLAG 12                        1    E(12) #
FCGLWF1  -GENERAL LEDGER BALANCE SHEET WORK FILE  ( 181 at start)
     1    TYPE = BLANK                             1    An$(1,1)
     2    BALANCE SHEET LINE NUMBER                4    An$(2,4)
     3    G/L ACCOUNT                             11    An$(6,11)
     4    DESCRIPTION                             45    Bn$
     5    REVERSE SIGNS?                           1    Cn$
     6    CURRENT PERIOD AMOUNT                   14    An ###########.00
     7    PREVIOUS PERIOD AMOUNT                  14    Bn ###########.00
     8    PRIOR YEAR AMOUNT                       14    Cn ###########.00
FCPOHI   -P/O RECEIPTS HISTORY FILE  ( 182 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    ITEM CODE                                8    An$(3,8)
     3    WAREHOUSE                                4    An$(11,4)
     4    RECEIPT DATE                             6    An$(15,6)
     5    P/O NUMBER                               5    An$(21,5) #####
     6    LINE ITEM                                2    An$(26,2) ##
     7    ORDER DATE                               6    Bn$
     8    SUPPLIER CODE                            6    Cn$(1,6)
     9    UNIT OF MEASURE                          2    Cn$(7,2)
    10    Contract? (Y/N)                          1    Cn$(9,1)
    11    (open)                                  11    Cn$(10,11)
    12    SUPPLIER NAME                           30    Dn$
    13    QUANTITY RECEIVED                        8    An #####.00
    14    UNIT COST                                7    Bn ####.00
    15    QUANTITY ORDERED                         6    Cn ######
    16    (open)                                   1    Dn
FCPORF   -PURCHASE ORDER RECEIPTS FILE  ( 183 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    P/O NUMBER                               5    An$(3,5)
     3    RELEASE NO.                              2    An$(8,2)
     4    LINE NUMBER                              3    An$(11,3)
     5    ITEM CODE (KEY)                         21    Bn$
     6    ITEM DESCRIPTION                        40    Cn$
     7    UNIT OF MEASURE                          2    Dn$
     8    QTY ORDERED                              8    An #####.00
     9    COST PER UNIT                           10    Bn #####.00##
    10    (open)                                   1    Cn #
    11    QTY RECEIVED                             8    Dn #####.00
    12    RECEIVED PREVIOUS                        8    En #####.00
    13    P/O LINE NO.                             3    Fn ###
    14    REPLACE COSTS?                           1    En$(1,1)
    15    (open)                                   9    En$(2,9)
    16    LOT NUMBERS                             40    Fn$
    17    LOT QUANTITIES                          30    Gn$
    18    BIN NUMBER                               6    Hn$
    19    Date Received                            6    In$
    20    Additional Item Code                    12    Jn$
FCCNVZW  -I/C WAREHOUSE CATEGORY MASTER MAINT. & I  ( 184 at start)
     1    Key Type = 'W'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Worker's Compensation Code               5    An$(4,5)
     4    Description                             25    Bn$
     5    Abbreviated Descr for Headings          10    Cn$
     6    Factor to use (##.######)                9    An ##.00####
     7    G/L Account (CR)                        11    Dn$
     8    Wages,Hours,Days (W,H,D)                 1    En$
FCPOCT   -PURCHASE ORDER CONTRACT MASTER FILE  ( 185 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    SUPPLIER NUMBER                          6    An$(3,6)
     3    ITEM CODE                                8    An$(9,8)
     4    UNIT OF MEASURE                          2    Bn$(1,2)
     5    (open)                                   2    Bn$(3,2)
     6    (open)                                   1    Cn$
     7    ISSUE DATE                               6    Dn$(1,6)
     8    EXPIRE DATE                              6    Dn$(7,6)
     9    MESSAGE                                 30    En$
    10    FUTURE FOB COST                          7    An ###.00#
    11    FUTURE LANDED COST                       7    Bn ###.00#
    12    QTY RECEIVED                             7    Cn #######
    13    (open)                                   1    Dn #
    14    LAST P/O DATE                            6    MMDDYY
    15    LAST RECPT DATE                          6    Fn$(7,6)
    16    LAST P/O NUMBER                          5    Gn$(1,5)
    17    (open)                                   5    Gn$(6,5)
    18    (open)                                   1    Hn$
FCCNVZr  -CREDIT/DEBIT MEMO REASON CODE FILE MAINT  ( 186 at start)
     1    KEY GROUP = "r"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    SHIFT CODE                               2    An$(4,2)
     4    DESCRIPTION                             25    Bn$
     5    (OPEN)                                  10    Cn$
     6    STANDARD RATE                            8    An ###.00##
     7    SHIFT DIFFERENTIAL (PER HOUR)            8    Bn ###.00##
     8    (OPEN)                                   1    Cn #
     9    (OPEN)                                   1    Dn #
    10    (OPEN)                                   1    En #
FCCNVZ]  -A/R APPLICATION CONTROL RECORD  ( 187 at start)
     1    KEY GROUP = "]"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    UNION CONTRACT NUMBER                    6    An$(4,6)
     4    DESCRIPTION                             25    Bn$
     5    (OPEN)                                  10    Cn$
     6    UNION BENEFITS - LOW DAYS                7    An ####.00
     7                   - HIGH DAYS               7    Bn ####.00
     8    PENSION BENEFITS - LOW HOURS             7    Cn ####.00
     9                     - HIGH HOURS            7    Dn ####.00
    10    (OPEN)                                   1    En #
    11    (OPEN)                                   1    Fn #
FCICPD   -Customer Inventory Descr for Price Labls  ( 188 at start)
     1    Company Code                             2    An$(1,2)
     2    Inventory Item Code                      6    An$(3,6)
     3    Description Line 1                      17    Bn$
     4    Description Line 2                      17    Cn$
FCCNVZbc -Bulk Customer Type Codes  ( 189 at start)
     1    Key Type = 'bc'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Bulk Cust Type                           2    An$(5,2)
     4    Description                             30    Bn$
FCEOORH  -Electronic Order Header File  ( 190 at start)
     1    Company Code                             2    An$(1,2)
     2    Customer Number                          6    An$(3,6)
     3    Ship-to Code                             4    An$(9,4)
     4    Transmission Number                      6    An$(13,6) ######
     5    Key Type = '0000'                        4    An$(19,4) ####
     6    Confirmation Number                      6    Bn$(1,6) ######
     7    Date Received                            6    Bn$(7,6)
     8    Time Received (HHMM)                     4    Bn$(13,4) ####
     9    (open)                                   9    Bn$(17,9)
FCEOORD  -Electronic Order Detail File  ( 191 at start)
     1    Company Code                             2    An$(1,2)
     2    Customer Number                          6    An$(3,6)
     3    Ship-to Code                             2    An$(9,2)
     4    Transmission Number                      6    An$(10,6) ######
     5    Key Type = '1'                           1    An$(16,1)
     6    Sequence Number                          3    An$(17,3)
     7    Item Code or 'E'(unconverted)            6    Bn$
     8    Quantity Ordered                         9    Cn #########
     9    Unconverted Data                        36    Dn$
    10    (open)                                   1    En$
    11    (open)                                   1    Gn #
FCCNVZO1 -Transmitter Master File  ( 192 at start)
     1    Key Type = 'O1'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Transmitter Number                       6    An$(5,6)
     4    Transmitter  Name                       30    Bn$
     5    Status: A=Active, I=Inactive             1
     6    Date Last Transmission                   6    Cn$(2,6) ######
     7    Time Last Transmission                   4    Cn$(8,4) ####
     8    S/A Category                             2    Cn$(12,2)
     9    (open)                                   2    Cn$(14,2)
    10    Customer Number                          6    Dn$(1,6)
    11    Ship To Code                             4    Dn$(7,4)
    12    Transmission Format                     10    En$
    13    Phone Number                            16    Fn$
    14    Contact Person                          20    Gn$
    15    Sort Key                                 8    Hn
    16    EMAIL ADDRESS                           40    Jn$
    17    EMAIL ADDRESS                           40
    18    EMAIL ADDRESS                           40    In$
FCEODED  -Tranmission Format Masks  ( 193 at start)
     1    Key Type = 'D'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Transmitter Format                      10    An$(4,10)
     4    Sequence Number (00-99)                  2    An$(14,2) ##
     5    Description                             20    Bn$
     6    Mask                                    40    Cn$
     7    Data Representation                     40    Dn$
FCEODEH  -Transmitter Format Master  ( 194 at start)
     1    Key Type = 'H'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Transmitter Format                      10    An$(4,10)
     4    Description                             30    Bn$
FCCNVZO3 -Transmission Data Elements  ( 195 at start)
     1    Key Group = 'O3'                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Data Element Code                        1    An$(5,1)
     4    Description                             30    Bn$
     5    Minimum Length                           3    Cn ###
     6    Maximum Length                           3    Dn ###
     7    Output Rec(H=Hdr,D=Det,B=Both)           1    En$(1,1)
     8    Write Rec(P=prev,S=curr,N=new)           1    En$(2,1)
     9    Ending Output Position                   3    En$(3,3) ###
    10    R=Right Justify, L=Left Just.            1    En$(6,1)
    11    Field Type(C=cus,T=tran,H=bth)           1    En$(7,1)
    12    (open)                                   2    En$(12,2)
FCCNVZCEO-ELECTRONIC ORDER PROCESSING CONTROL RECORD  ( 196 at start)
     1    Key Group = 'CEO'                        3    An$(1,3)
     2    Company Code                             2    An$(4,2)
     3    Valid Separator Chars(&=space)           5    Bn$(1,5)
     4    Fill Character                           1    Bn$(6,1)
     5    Error Character                          1    Bn$(7,1)
     6    Number of Lines                          2    Bn$(8,2) ##
     7    Number or Days Trans to save             2    Bn$(10,2) ##
     8    Duplicate Trans (Hold,Pro,Ign)           1    Bn$(12,1)
     9    Process Automatic (Y/M=manual)           1    Bn$(13,1)
    10    Default Printer                          4    Bn$(14,4)
    11    (open)                                   2    Bn$(18,2)
    12    Next Transmision Number                  6    Cn ######
    13    Max No Char Errors for OK                4    Dn ####
    14    WINDOWS 1-4 STATUS (5*4BYTES)           20    En$
    15    Daily Cutoff Time (0000-2400)            4    Fn$(1,4) ####
    16    Last Transmission Date                   6    Fn$(5,6)
    17         - Time (HHMM)                       4    Fn$(11,4) ####
    18         - Line                              2    Fn$(15,2) ##
    19    (open)                                   4    Fn$(15,4)
    20    (open)                                   1    Gn #
    21    (open)                                   1    Hn #
FCCNVZO2 -EOP Application Control Record  ( 197 at start)
     1    Key Group = 'O2'                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Transmission Number                      6    An$(5,6) ######
     4    Confirmation Number                      6    Bn$(1,6) ######
     5    Transmitter Number                       6    Bn$(7,6) ######
     6    Date Received                            6    Bn$(13,6)
     7    Time Received                            4    Bn$(19,4) ####
     8    Received on Line Number                  2    Bn$(23,1) ##
     9    Receipt Status                           1    Bn$(25,1)
    10    Processing Status (RPXHE)                1    Bn$(26,1)
    11    Transmission NO of Last Good 1           6    Bn$(27,6) ######
    12    (open)                                  30    Bn$(33,30)
    13    Number or Records                        6    Cn ######
    14    Number of Characters in Error            4    Dn ####
    15    Number of Duplicate Records              5    En #####
    16    Number of Records to Ignore              6    Fn ######
    17    (open)                                   1    Gn #
    18    (open)                                   1    Hn #
FCEOTR   -Raw Received Electronic Orders  ( 198 at start)
     1    Company Code                             2    An$(1,2)
     2    Transmission Number                      6    An$(3,6)
     3    Sequence Number                          3    An$(9,3) ###
     4    Eight 12 Character Fields               96    Bn$(1,96)
     5    2nd Eight 12 Character fields           96    Bn$(97,96)
     6    3rd Eight 12 Character Fields           96    Bn$(192,96
     7    Last Four 12 Character Fields           48    Bn$(192,48
FCPWKG   -P/R Labor Distribution  ( 199 at start)
     1    CO. CODE                                 2    A$(1,2)
     2    EMPLOYEE NO.                             5    A$(3,5)
     3    SEQUENCE NO.                             1    A$(8,1)
     4    PAY TYPE                                 1    A$(9,1)
     5    DEPARTMENT                               2    A$(10,2)
     6    COST CENTER                              3    A$(12,3)
     7    SHIFT                                    2    A$(15,2)
     8    CONTRACT                                 6    A$(17,6)
     9    OPEN                                     5    B$
    10    G/L ACCOUNT                             11    C$
    11    RATE                                     7    An ##.00##
    12    HOURS                                    7    Bn ####.00
    13    EARNINGS                                 8    Cn #####.00
    14    OPEN                                     1    Dn #
FCCNVZQ  -ORDER SOURCE CODES FILE MAINTENANCE & IN  ( 200 at start)
     1    KEY GROUP = "Q"                          1    AN$(1,1)
     2    WAREHOUSE NUMBER                         4    AN$(3,4)
     3    DESCRIPTION                             30    BN$
     4    ADDRESS 1                               30    CN$
     5    ADDRESS 2                               30    DN$
     6    ADDRESS 3                               30    EN$
     7    TELEPHONE                               10    Fn$ ##########
     8    ZIP CODE                                 9    GN$
     9    DIRECT SHIP WHSE? (Y/N)                  1    Hn$(1,1)
    10    (open)                                   9    Hn$(2,9)
FCCNVZmE -ORDER ENTRY MESSAGE CODES  ( 201 at start)
     1    KEY TYPE='mE'                            2    AN$(1,2)
     2    COMPANY                                  2    AN$(3,2)
     3    MESSAGE CODE                             2    AN$(5,2)
     4    MESSAGE                                 64    BN$
FCCNVZap -Warehouse Picking Areas  ( 202 at start)
     1    Key Type = 'ap'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Case/Each Pick Areas (C/E) ?             1    An$(5,1)
     4    First Section-Start                      6    Bn$(1,6)
     5         -End                                6    Bn$(7,6)
     6    2nd Section - Start                      6    Bn$(13,6)
     7         -End                                6    Bn$(19,6)
     8    3rd Section - Start                      6    Bn$(25,6)
     9         -End                                6    Bn$(30,6)
    10    4th Section - Start                      6    Bn$(37,6)
    11         - End                               6    Bn$(42,6)
    12    5th Section - Start                      6    Bn$(49,6)
    13         - End                               6    Bn$(55,6)
    14    6th Section                              6    Bn$(61,6)
    15         - End                               6    Bn$(66,6)
    16    7th Section - Start                      6    Bn$(73,6)
    17         - End                               6    Bn$(79,6)
    18    8th Section - Start                      6    Bn$(85,6)
    19         - End                               6    Bn$(91,6)
    20    9th Section - Start                      6    Bn$(97,6)
    21         - End                               6    Bn$(103,6)
    22    10th Section - Start                     6    Bn$(109,6)
    23         - End                               6    Bn$(105,6)
FCOEOL   -Shipped Orders File  ( 203 at start)
     1    Company Code                             2    An$(1,2)
     2    Invoice Number                           6    An$(3,6)
     3    Customer Number                          6    Bn$(1,6)
     4    Ship to Code                             4    Bn$(7,4)
     5    P/O Number                              20    Cn$
     6    Order Date                               6    Dn$(1,6)
     7    Ship Date                                6    Dn$(7,6)
     8    (open)                                   1    En$
     9    Number of Lines                          3    An ###
    10    Net Weight                               9    Bn ######.00
    11    (open)                                   1    Cn #
    12    Net Invoice Amt                          9    Dn ######.00
    13    Sales Tax Pct                            5    En ##.00
    14    Sales Tax Amt                            6    Fn ###.00
    15    Taxable Amount                           8    Gn #####.00
FCCNVZmI -INVOICE PRINT MESSAGE CODES  ( 204 at start)
     1    Key Type = 'mI'                          2    AN$(1,2)
     2    Company Code                             2    AN$(3,2)
     3    Message Code                             2    AN$(5,2)
     4    Message Text                            48
FCICXF   -ITEM CODE CONVERSION FILE  ( 205 at start)
     1    File Name                                6    An$(1,6)
     2    Sequence                                 2    An$(7,2)
     3    Key Literal 1                            6    Bn$
     4    Key Literal 2                            6    Cn$
     5    Date Updated                             6    Dn$
     6    Time Updated                             6    En$ ###.00
     7    Key Literal 1 Pos                        2    An ##
     8    Key Literal 2 Pos                        2    Bn ##
     9    Field Number to Update                   3    Cn ###
    10    Position in Field                        3    Dn ###
    11    Field Number to Update                   3    En ###
    12    Position in Field                        3    Fn ###
    13    Total Records                            6    Gn ######
    14    Records Updated                          6    Hn ######
FCAPVH   -A/P VOUCHER HISTORY FILE  ( 206 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    VENDOR NUMBER                            6    An$(3,6)
     3    VOUCHER NUMBER                           6    An$(9,6)
     4    Sequence No                              2    An$(15,2) ##
     5    INVOICE DATE                             6    Bn$(1,6)
     6    CHECK DATE                               6    Bn$(7,6)
     7    CHECK NUMBER                             6    Cn$
     8    VENDOR REFERENCE NUMBER                 25    Dn$
     9    GROSS AMOUNT                             9    An ######.00
    10    DISCOUNT AMT                             9    Bn ######.00
    11    (open)                                   1    Cn
    12    (open)                                   1    Dn
    13    (open)                                   1    En
    14    P/O Number                               9    En$
FCCNVZrp -ORDER ENTRY CREDIT/DEBIT MEMO REASON CODES  ( 207 at start)
     1    Key Type = 'rp'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Reason Code                              2    An$(5,2)
     4    Description                             30    Bn$
     5    Restock charge applies(Y/N) ?            1    Cn$(1,1)
     6    Return to Stock (Y/N) ?                  1    Cn$(2,1)
     7    Bill-back to supplier (Y/N) ?            1    Cn$(3,1)
     8    (open)                                   7    Cn$(4,7)
     9    Restock Charge Percent (99.99)           5    Dn ##.00
    10    G/L Account                             11
FCIPEX   -Item Pricing Exception File  ( 208 at start)
     1    Item Code                                6    An$(1,6)
     2    Company Code                             2    An$(7,2)
     3    W/H Code                                 4    An$(9,4)
     4    Spaces+Co                                6    An$(13,6)
     5    Price List Code                          1    An$(19,1)
     6    (open)                                   1    An$(20,1)
     7    (open)                                   1    Bn$
     8    Old - Eff Date                           6    Cn$(1,6)
     9    Old - Exp Date                           6    Cn$(7,6)
    10    (open)                                  12    Cn$(13,12)
    11    New - Eff Date                           6    Dn$(1,6)
    12    New - Exp Date                           6    Dn$(7,6)
    13    (open)                                  12    Dn$(13,12)
    14    Old - Method                             1    En$(1,1)
    15    Old - Basis                              1    En$(2,1)
    16    Old - Rounding                           1    En$(3,1)
    17    (open)                                   1    En$(4,1)
    18    New - Method                             1    Fn$(1,1)
    19    New - Basis                              1    Fn$(2,1)
    20    New - Rounding                           1    Fn$(3,1)
    21    (open)                                   1    Fn$(4,1)
    22    Old Price/Pct                            8    P(1) #####.00
    23    New Price/Pct                            8    N(1) #####.00
FCCNVZP1 -Price List Master File  ( 209 at start)
     1    Key Group = 'P1"                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Price List Code                          1    An$(5,1)
     4    (open)                                   1    An$(6,1)
     5    Product Category(zz=all othr)            2    An$(7,2)
     6    Description                             30    Bn$
     7    Old Effective Date                       6    Cn$(1,6)
     8     - Expiration Date                       6    Cn$(7,6)
     9     - Usage (RC,RE,WC,WE)                   2    Cn$(13,2)
    10     - Calculation Method(MCPG)              1    Cn$(15,1)
    11     - Basis to use (" ",A-X)                1    Cn$(16,1)
    12    (open)                                   1    Cn$(17,1)
    13     - Rounding Method                       1    Cn$(18,1)
    14     - Each Price to use                     1    Cn$(19,1)
    15    (open)                                   1    Cn$(20,1)
    16     - Percentage                            5    Dn ##.00
    17    New Effective Date                       6    En$(1,6)
    18     - Expiration Date                       6    En$(7,6)
    19     - Usage                                 2    En$(13,2)
    20     - Calculation Method (MCPG)             1    En$(15,1)
    21     - Basis to use (" ",A-X)                1    En$(16,1)
    22    (open)                                   1    En$(17,1)
    23     - Rounding Method                       1    En$(18,1)
    24     - Each Price to use                     1    En$(19,1)
    25    (open)                                   1    En$(20,1)
    26     - Percentage to use                     5    Fn ##.00
    27    Date of Last Change                      6    Gn$(1,6)
    28    Authorized by                            6    Gn$(7,6)
    29    Date Last New Price Changd               6    Gn$(13,6)
    30    (open)                                   1    Hn #
    31    Catalog Description                     30    In$
FCCNVZ)  -PURCHASE ORDER PRINT MESSAGES  ( 210 at start)
     1    KEY GROUP = "mP"                         2    An$(1,2)
     2    COMPANY CODE                             2    An$(3,2)
     3    MESSAGE CODE                             2    An$(5,2)
     4    MESSAGE TEXT                            60    Bn$
FCCNVZ+  -A/R ADJUSTMENTS REASON CODES  ( 211 at start)
     1    Key Group = 'RA'                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Reason Code                              2    An$(5,2)
     4    Reason Description                      20    Bn$
     5    General Ledger Account                  11    Cn$
     6    (OPEN)                                   5    Dn$
FCCNVZP4 -Freight Upcharges for Pricing  ( 212 at start)
     1    Key Type = 'P4'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Zone Code (1-9)                          1    An$(5,1)
     4    Description                             30    Bn$
     5    (open)                                   2    Cn$
     6    Regular Customer per LB amount           7    Dn ###.00#
     7    Special Customer per LB amount           7    En ###.00#
FCCNVZP5 -Product Combination Specials  ( 213 at start)
     1    Key Type = 'P5'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Specials Category Code                   2    An$(5,2)
     4    Sequence Number                          2    An$(7,2) ##
     5    Description                             30    Bn$
     6    Discount Table to use                    2    Cn$(1,2)
     7    Count partial cases to qualify           1    Cn$(3,1)
     8    Do partial cases get discount            1    Cn$(4,1)
     9    Calculation Method                       1    Cn$(5,1)
    10    Basis to use (" ",0,1,A-X)               1    Cn$(6,1)
    11    (open)                                   1    Cn$(7,1)
    12    Rounding Method                          1    Cn$(8,1)
    13    Each Price to Use                        1    Cn$(10,1)
    14    Use Qty Ord/Ship (O/S)                   1    Cn$(11,1)
    15    (open)                                   4    Cn$(12,4)
    16    Price Lists is applies to               24    Dn$
    17    Effective Date                           6    En$(1,6)
    18    Expiration Date                          6    En$(7,6)
    19    Items included: Range 1                 12    Fn$(1,12)
    20    Items Included: Range 2                 12    Fn$(13,12)
    21    Items Included: Range 3                 12    Fn$(25,12)
    22    Items Included: Range 4                 12    Fn$(37,12)
    23    Items Included: Range 5                 12    Fn$(49,12)
    24    Items Included: Range 6                 12    Fn$(61,12)
    25    Items Included: Range 7                 12    Fn$(73,12)
    26    Items Included: Range 8                 12    Fn$(85,12)
    27    Customer Eligible 1                     10    Gn$(1,10)
    28    Customer Eligible 2                     10    Gn$(11,10)
    29    Customer Eligible 3                     10    Gn$(21,10)
    30    Customer Eligible 4                     10    Gn$(31,10)
    31    Customers Eligible 5&6                  20    Gn$(41,20)
FCIPXF   -Price Change Cross-reference  ( 214 at start)
     1    Company Code                             2    An$(1,2)
     2    Date of Change                           6    An$(3,6)
     3    Supplier Code                            6    An$(9,6)
     4    Item Code                               18    An$(15,18)
     5    Type of Change                           1    An$(33,1)
FCNXRF4  -Inventory XREF by Vendor  ( 215 at start)
     1    Key Group = '4'                          1    An$(1,1)
     2    Vendor Code                              6    An$(2,6)
     3    Item Code                               18    An$(8,18)
FCNXRF2  -Inventory Xref by Sales Category  ( 216 at start)
     1    Key Group = '2'                          1    An$(1,1)
     2    Sales Category                           2    An$(2,2)
     3    Item Key (1-18)                         18    An$(4,18)
FCNXRF3  -Inventory XREF by Name (First 20 Chars)  ( 217 at start)
     1    Key Group = '3'                          1    An$(1,1)
     2    Item Description (20 chars)             20    An$(2,20)
     3    Iventory key (1-18)                     18    An$(22,18)
FCPOSX   -SUPPLIER/ITEM XREF FILE  ( 218 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    SUPPLIER CODE                            6    An$(3,6)
     3    ITEM CODE                                8    An$(9,8)
     4    SUPPLIER ITEM CODE                      10    Bn$
     5    SUPPLIER ITEM DESC 1                    37    Cn$
     6    SUPPLIER ITEM DESC 2                    37    Dn$
     7    SUPPLIER ITEM DESC 3                    37    En$
     8    SUPPLIER ITEM DESC 4                    37    Fn$
     9    (open)                                   1    Gn$
    10    (open)                                   1    Hn$
FCPOHF   -PURCHASE ORDER HEADER FILE  ( 219 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    P/O NUMBER                               5    An$(3,5)
     3    RELEASE NUMBER                           2    An$(8,2)
     4    SUPPLIER NUMBER                          6    Bn$
     5    SUPPLIER NAME                           30    Cn$
     6    ADDR LINE 1                             30    Dn$
     7    ADDR LINE 2                             30    En$
     8    ADDR LINE 3                             30    Fn$
     9    ORDER PLACED BY/FOR                     20    Gn$
    10    ORDER ISSUED TO                         20    Hn$
    11    TERMS                                   20    In$
    12    F.O.B.                                  20    Jn$
    13    P/O REG FLAG                             1    Kn$(1,1)
    14    Vouchered (Y/N)                          1    Kn$(2,1)
    15    (open)                                   1    Kn$(3,1)
    16    PRINT FLAG                               1    Kn$(4,1)
    17    (open)                                   1    Kn$(5,1)
    18    Ammended P/O?                            1    Kn$(6,1)
    19    CONFIRMED FLAG                           1    Kn$(7,1)
    20    (open)                                   1    Kn$(8,1)
    21    P.O. RECVD COMPLETE?                     1    Kn$(9,1)
    22    TERMS CODE                               1    Kn$(10,1)
    23    TAXABLE?                                 1    Kn$(11,1)
    24    Carrier Code                             2    Kn$(12,2)
    25    Voucher Number                           6    Kn$(14,6)
    26    WAREHOUSE (I/C)                          4    Kn$(20,4)
    27    WAREHOUSE (DEL)                          4    Kn$(24,4)
    28    FOB CODE                                 2    Kn$(28,2)
    29    P/O Type                                 2    Kn$(30,2)
    30    Used                                     1    Kn$(32,1)
    31    Production Order?                        1    Kn$(33,1)
    32    (open)                                   7    Kn$(34,7)
    33    ORDER DATE                               6    On$(1,6)
    34    ETA DATE                                 6    On$(7,6)
    35    DATE WANTED                              8    Pn$(1,8)
    36    Date Ammended                            8    Pn$(9,8)
    37    CARRIER                                 20    Qn$
    38    LAST REC DATE                            6    Rn$ ######
    39    Discount Types                           3    Sn$(1,3)
    40    Freight Type                             1    Sn$(4,1)
    41    (open)                                   1    An #
    42    TOTAL UNITS                             10    Tn #######.00
    43    TOTAL WEIGHT                            10    Un #######.00
    44    TOTAL AMOUNT                            10    Vn #######.00
    45    Number of Lines                          3    Wn
    46    Operator Code                            3    Xn$
    47    Disc 1 - Rate/Amt                        8    TT(1) #####.00
    48    Disc 2 - Rate/Amt                        8    TT(2) #####.00
    49    Disc 3 - Rate/Amt                        8    TT(3) #####.00
    50    Freight Rate/Amt                         8    TT(4) ########
    51    Number of Pallets                        7    TT(5) ####.00
FCPODF   -PURCHASE ORDER DETAIL FILE  ( 220 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    P/O NUMBER                               5    An$(3,5)
     3    RELEASE NUMBER                           2    An$(8,2)
     4    LINE NO                                  3    An$(10,3) ###
     5    ITEM CODE (KEY)                         21    Bn$
     6    ITEM DESCRIPTION                        48    Cn$
     7    UNIT OF MEASURE                          2    Dn$
     8    ORDER QTY                                7    An #######
     9    NET UNIT COST                            9    Bn ####.00##
    10    QTY RECEIVED                             9    Cn ######.00
    11    Qty on order (I/C units)                 7    Dn #######
    12    Revised Cost                             8    En ####.00#
    13    LOT NUMBERS                             40    En$
    14    BIN NUMBERS                             30    Fn$
    15    WAREHOUSE CODE                           4    Gn$
    16    Unit Cost - FOB                          9    Fn ####.00##
    17    Freight Cost Per Unit                    8    Gn ###.00##
    18    Discount per unit                        8    Hn ###.00##
    19    DISCOUNT PERCENT                         6    In ###.00
    20    Wholesale Price                          7    Jn ####.00
    21    CONTRACT NUMBER                         10    Kn$(1,10)
    22    Freight Units                            2    Kn$(11,2)
    23    Discount Units                           2    Kn$(13,2)
    24    LINE ITEM TYPE (I/M)                     1    Kn$(15,1)
    25    Production Order No                      6    Kn$(16,6) ######
    26    Contract Item?                           1    Kn$(22,1)
    27    (open)                                   8    Kn$(23,9)
    28    Conv Factor (to P/O units)              10    Ln$ #####.00##
    29    Promo Exp Date                           6    Mn$(1,6)
    30    Promo Eff Date                           6    Mn$(7,6)
    31    (open)                                  12    Mn$(13,12)
FCNXRF1  -X-REFERENCE 1  ( 221 at start)
     1    Key Type = '1'                           1    AN$(1,1)
     2    Catalog Category                        10    An$(2,10)
     3    Item Description                        40    An$(12,40)
     4    Item Code                               12    An$(52,12)
FCCNVZ#  -PAYROLL STANDARD DEDUCTIONS CONTROL RECORDS  ( 222 at start)
     1    Key Type = '#'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Standard Deduction Code                  1    An$(4,1)
     4    Description                             25    Bn$
     5    G/L Account (CR)                        11    Cn$
     6    Abbreviated Description                  3    Dn$
     7    Abbreviated Heading                      6    En$
     8    Stop when balance is zero(Y/N)           1    Fn$
     9    Federal Tax?                             1    Gn$(1,1)
    10    State Tax?                               1    Gn$(2,1)
    11    Local Tax?                               1    Gn$(3,1)
    12    F.I.C.A.?                                1    Gn$(4,1)
    13    S.D.I.?                                  1    Gn$(5,1)
    14    W-2 FLAG                                 1    Gn$(6,1)
    15    Company Contribution %                   5    Hn ##.00
    16    Max % of Gross                           5    In ##.00
    17    Contract Number                          8    Jn$
FCCNVZq  -RECOMMENDED PURCHASING CATEGORY CODES  ( 223 at start)
     1    KEY TYPE = "q"                           1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    CATEGORY CODE                            1    An$(4,1)
     4    DESCRIPTION                             50    Bn$
     5    (open)                                   1    Cn$
     6    (open)                                   1    Dn$
     7    Number of Weeks                          2    A(1) ##
     8    Number of Weeks                          2    A(2) ##
     9    Number of Weeks                          2    A(3) ##
    10    Number of Weeks                          2    A(4) ##
    11    Number of Months                         2    A(5) ##
    12    Percentage                               3    B(1) ###
    13    Percentage                               3    B(2) ###
    14    Percentage                               3    B(3) ###
    15    Percentage                               3    B(4) ###
    16    Percentage                               3    B(5) ###
FCCNVZ%  -PAYROLL STANDARD EARNINGS CODES  ( 224 at start)
     1    Key Type = '%'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Standard Earnings Code                   1    An$(4,1)
     4    Description                             25    Bn$
     5    G/L Account for expense (DR)            11    Cn$
     6    Abbreviated Description                  3    Dn$
     7    Abbreviated Heading                      6    En$
FCCNVZb  -PAYROLL BONUS CYCLE DESCRIPTIONS CONTROL RECORDS  ( 225 at start)
     1    KEY GROUP = "b"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    CYCLE CODE                               1    An$(4,1)
     4    DESCRIPTION                             25    Bn$
FCCNVZu  -PAYROLL UNION CODES FILE MAINTENANCE & INQUIRY  ( 226 at start)
     1    KEY GROUP = "u"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    UNION CODE                               3    An$(4,3)
     4    UNION NAME                              25    Bn$
FCPOIX   -ITEM/PURCHASE ORDER XREF FILE  ( 227 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    ITEM CODE                                6    An$(3,6)
     3    WAREHOUSE CODE                           4    An$(9,4)
     4    P/O NUMBER                               5    An$(13,5) #####
     5    RELEASE NO                               2    An$(18,2) ##
     6    LINE NUMBER                              3    An$(20,3) ###
FCNXRF5  -X-REFERENCE 5  ( 228 at start)
     1    KEY TYPE = '5'                           1    AN$(1,1)
     2    LOCATION                                 6    An$(2,6)
     3    ITEM #                                  18    An$(8,18)
FCPRLD   -M-T-D LABOR DISTRIBUTION FILE MAINTENANC  ( 229 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    PAY CYCLE                                1    An$(3,1)
     3    (OPEN)                                   6    An$(4,6)
     4    DEPARTMENT                               2    An$(10,2)
     5    COST CENTER                              3    An$(12,3)
     6    PAY TYPE                                 1    An$(15,1)
     7    MONTH CODE                               4    An$(16,4)
     8    EARNINGS PERIOD 1                        9    E(1) ######.00
     9    EARNINGS PERIOD 2                        9    E(2) ######.00
    10    EARNINGS PERIOD 3                        9    E(3) ######.00
    11    EARNINGS PERIOD 4                        9    E(4) ######.00
    12    EARNINGS PERIOD 5                        9    E(5) ######.00
FCPRGL   -M-T-D G/L DISTRIBUTION FILE MAINTENANCE   ( 230 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    PAY CYCLE                                1    An$(3,1)
     3    G/L ACCOUNT                             11    An$(4,11)
     4    PAY TYPE                                 1    An$(15,1)
     5    MONTH CODE                               4    An$(16,4)
     6    AVAILABLE                                1    Bn$
     7    AVAILABLE                               10    Cn$
     8    DEBITS PERIOD 1                          9    E(0,1) ######.00
     9    DEBITS PERIOD 2                          9    E(0,2) ######.00
    10    DEBITS PERIOD 3                          9    E(0,3) ######.00
    11    DEBITS PERIOD 4                          9    E(0,4) ######.00
    12    DEBITS PERIOD 5                          9    E(0,5) ######.00
    13    CREDITS PERIOD 1                         9    E(1,1) ######.00
    14    CREDITS PERIOD 2                         9    E(1,2) ######.00
    15    CREDITS PERIOD 3                         9    E(1,3) ######.00
    16    CREDITS PERIOD 4                         9    E(1,4) ######.00
    17    CREDITS PERIOD 5                         9    E(1,5) ######.00
FCCNVZp  -CUSTOMER/CATEGORY PRICING FILE  ( 231 at start)
     1    Key Type = 'p'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Payroll Department Code                  2    An$(4,2)
     4    Description                             30    Bn$
     5    G/L Acct for Unempl Comp (DR)           11    Cn$
     6    Dept Manager Operator Code               3    D$
     7    Position of Dept in G/L Acct             2    An ##
     8    (open)                                   1    Bn #
FCPRWD   -W-2 FORM PRINTING FILE  ( 232 at start)
     1    Sequence                                 3    An$ ###
     2    W-2 Box Number                           2    Bn$ ##
     3    Description                             30    Cn$
     4    Horiz (X) Position                       3    An ###
     5    Vertical (Y) Position                    3    Bn ###
     6    Field to Print                           2    Cn ##
FCCNVZpa -Purchasing Agent Master File  ( 233 at start)
     1    Key Type = 'pa'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Purchasing Agent Code                    3    An$(5,3)
     4    Purchasing Agent Name                   30    Bn$
FCGLJX   -G/L PERMANENT JOURNAL ENTRIES FILE MAINT  ( 234 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    JOURNAL NO.                              5    An$(3,5)
     3    LINE NO.                                 3    An$(8,3)
     4    G/L ACCOUNT                             11    Bn$
     5    ENTRY DATE                               6    Cn$(1,6)
     6    G/L PERIOD                               4    Cn$(7,4)
     7    DESCRIPTION                             40    Dn$
     8    ENTRY AMOUNT                            12    An #########.00
     9    (OPEN)                                   1    Bn
    10    TRANSACTION DESCRIPTION                 30    En$
    11    ISSUE MONTH                              4    Fn$
    12    PROJECT NUMBER                           3    Gn$
FCNVTYP  -Inventory Purchasing Information  ( 235 at start)
     1    Product Number                           6    An$(1,6)
     2    Company Code                             2    An$(7,2)
     3    Warehouse Number                         4    An$(9,4)
     4    4 spaces + co number                     6    An$(13,6)
     5    Record Type                              3    An$(19,3)
     6    see file 235                             6    Bn$(1,6)
     7    Sale Units                               2    BN$(7,2)
     8    Pricing Units                            2    Bn$(9,2)
     9    Purchasing Units                         2    Bn$(11,2)
    10    see file 135                            36    Bn$(13,36)
    11    Pct cost to whlsl                        6    Bn$(49,6) ###.00
    12    Pct Whlsl to Retail                      6    Bn$(55,6) ###.00
    13    Wholesale Rounding Method                1    Bn$(61,1)
    14    Retail Rounding Method                   1    Bn$(62,1)
    15    (open)                                   6    Bn$(63,6)
    16    Discount Units                           2    Bn$(69,2)
    17    Safety Stock (Wks)                       2    Bn$(71,2) ##
    18    see file 135                             2    Bn$(73,2)
    19    Link to Master                           1    Bn$(75,1)
    20    Recom Order Categ                        1    Bn$(76,1)
    21    Cycle Count Category                     1    Bn$(77,1)
    22    (open)                                   3    Bn$(77,3)
    23    Item Description                        48    Cn$
    24    see file 135                            20    Dn$
    25    see file 135                            11    En$
    26    see file 135                            12    Fn$
    27    Date Last Receipt                        6    Fn$(13,6)
    28    see file 135                            30    Gn$
    29    see file 135                            10    I(0)
    30    see file 135                            10    I(1)
    31    PRIC PER I/C UNITS                      10    I(2)
    32    Conv Fctr-Buy/Price                     10    I(3) #####.00##
    33    see file 135                            10    I(4)
    34    see file 135                            10    I(5)
    35    see file 135                            10    I(6)
    36    see file 135                            10    I(7)
    37    see file 135                            10    I(8)
    38    Case Cost - AVG                          9    I(9) ####.00##
    39    Last FOB Cost                            9    I(10) ####.00##
    40    Case Cost - NET                          9    I(11) ####.00##
    41    see file 135                             1    I(12)
    42    see file 135                                  I(13)
    43    see file 235                             1    I(14)
    44    see file 135                                  I(15)
    45    see file 135                                  I(16)
    46    see file 135                                  I(17)
    47    see file 135                                  I(18)
    48    FOB Cost                                 9    I(19) ####.00##
FCCNVZpw -Product Warning Codes  ( 236 at start)
     1    Key Type = 'pw'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Trademark Flag                           2    An$(5,2)
     4    Description                             25    Bn$
     5    Warning Symbol                           1    Cn$
FCAPMTH  -OPEN ACCOUNTS PAYABLE MONTHLY FILE - HEA  ( 237 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    VENDOR NUMBER                            6    An$(3,6)
     3    VOUCHER NUMBER                           6    An$(9,6)
     4    RECORD TYPE IND.                         1    An$(15,1)
     5    SEQUENCE NUMBER                          2    An$(16,2)
     6    PAYEE NAME (VENDOR)                     30    Bn$
     7    DATE DUE                                 6    Cn$(1,6)
     8    VOUCHER DATE                             6    Cn$(7,6)
     9    Terms Date                               6    Cn$(13,6)
    10    P.O.NUMBER                               6    Dn$
    11    VENDOR REF NO.                          25    En$
    12    (OPEN)                                   1    Fn$
    13    ORIGINAL GROSS                          10    An #######.00
    14    ORIGINAL DISC.                          10    Bn #######.00
    15    BEGINNING MTH.BAL.                      10    Cn #######.00
    16    (OPEN)                                   1    Dn
FCAPMTD  -OPEN ACCOUNTS PAYABLE MONTHLY FILE - DET  ( 238 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    VENDOR NUMBER                            6    An$(3,6)
     3    VOUCHER NUMBER                           6    An$(9,6)
     4    RECORD TYPE IND.                         1    An$(15,1)
     5    SEQUENCE NUMBER                          2    An$(16,2)
     6    (OPEN)                                   1    Bn$
     7    DATE (PYMT OR ADJUST)                    6    Cn$(1,6)
     8    (OPEN)                                   6    Cn$(7,6)
     9    CHECK OR ADJ.NUMBER                      6    Dn$
    10    (OPEN)                                   1    En$
    11    (OPEN)                                   1    Fn$
    12    GROSS AMT.(PYMT/ADJ)                    10    An #######.00
    13    DISC.AMOUNT (PYMT/ADJ)                  10    Bn #######.00
    14    (OPEN)                                   1    Cn #
    15    (OPEN)                                   1    Dn #
FCCNVZkc -Kosher Categories  ( 239 at start)
     1    Key Type = "kc"                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Kosher Category                          1    An$(5,1)
     4    Category Description                    30    Bn$
FCORccC  -O/E EXCEPTIONS - CREDIT LIMIT EXCEEDED F  ( 240 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    KEY TYPE = "C"                           1    An$(3,1)
     3    CUSTOMER NO.                             6    An$(4,6)
     4    INVOICE NO.                              6    An$(10,6)
     5    ORDER KEY                               14    Bn$
     6    NET INVOICE                             11    An ########.00
     7    AMOUNT EXCEEDED                         11    Bn ########.00
FCORccD  -O/E EXCEPTIONS - DELINQUENT ACCOUNTS FIL  ( 241 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    KEY TYPE = "C"                           1    An$(3,1)
     3    CUSTOMER NO.                             6    An$(4,6)
     4    INVOICE NO.                              6    An$(10,6)
     5    ORDER KEY                               14    Bn$
     6    NET INVOICE                             11    An ########.00
     7    (OPEN)                                   1    Bn
FCCNVZic -Inventory Usage File  ( 242 at start)
     1    Key Type = 'ic'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Usage Code                               1    An$(5,1)
     4    Description                             40    Bn$
FCOEBL   -Bill of Lading Print File  ( 243 at start)
     1    Company Code                             2    An$(1,2)
     2    Bill of Lading No                        6    An$(3,6)
     3    Order Number(s)                         40    Bn$
     4    Customer Number                          6    Cn$
     5    BOL Print Date                           6    Dn$(1,6)
     6    Order Date                               6    Dn$(7,6)
     7    Ship Date                                6    Dn$(13,6)
     8    Pallet Count                             2    Dn$(19,2)
     9    Shipped                                  1    Dn$(21,1)
FCOEBL   -Bill of Lading Print File  ( 244 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    EMPLOYEE NO.                             5    An$(3,5)
     3    EMPLOYEE NAME                           25    Bn$
     4    ADDRESS 1                               25    Cn$
     5    ADDRESS 2                               25    Dn$
     6    ADDRESS 3                               25    En$
     7    SOC.SEC.NO.                              9    Fn$
     8    TELEPHONE NO.                           10    Gn$
     9    ALPHA SORT KEY                           8    Hn$
    10    DATE HIRED                               6    In$(1,6)
    11    DATE TERMINATED                          6    In$(7,6)
    12    ANNIVERS DATE                            6    In$(13,6)
    13    BIRTHDATE                                6    In$(19,6)
    14    LAST PERIOD WKD                          6    In$(25,6)
    15    Last Review                              6    In$(31,6)
    16    PENSION ELIGIBIL                         6    In$(37,6)
    17    Last Raise                               6    In$(43,6)
    18    Raise Amount                             8    In$(49,8) #####.00
    19    HOME DEPARTMENT                          2    Jn$(1,2)
    20    HOME COST CENTER                         3    Jn$(3,3)
    21    NORMAL SHIFT                             2    Jn$(6,2)
    22    CONTRACT NUMBER                          6    Jn$(8,6)
    23    STATUS FLAG                              1    Kn$(1,1)
    24    PAY TYPE                                 1    Kn$(2,1)
    25    PAY CYCLE                                1    Kn$(3,1)
    26    MARITAL STATUS                           1    Kn$(4,1)
    27    FICA EXEMPT                              1    Kn$(5,1)
    28    AG.WORKER                                1    Kn$(6,1)
    29    REASON TERMINATED                        1    Kn$(7,1)
    30    PENSION STATUS                           1    Kn$(8,1)
    31    STATE TAX ABBR                           2    Kn$(9,2)
    32    LOCAL TAX CODE                           2    Kn$(11,2)
    33    UNION CODE                               3    Kn$(13,3)
    34    WORKER'S COMP CODE                       5    Kn$(16,5)
    35    SEX CODE                                 1    Kn$(21,1)
    36    E.I.C. FLAG                              2    Kn$(22,2)
    37    SECURITY FLAG                            1    Kn$(24,2)
    38    HOLIDAY PAY? (Y/N)                       1    Kn$(25,1)
    39    Driver's Lic #                          10    Kn$(26,10)
    40    # EXEMPT-FED                             2    X(0) ##
    41    # EXEMPT-STATE                           2    X(1) ##
    42    # EXEMPT-LOCAL                           2    X(2) ##
    43    HOURLY RATE                              7    R(0) ##.00##
    44    SALARY RATE                              8    R(1) #####.00
    45    QTD - GROSS                             10    Q(0) #######.00
    46    QTD - FED TAX                            9    Q(1) ######.00
    47    QTD - FICA                               8    Q(2) #####.00
    48    QTD - STE TAX                            9    Q(3) ######.00
    49    QTD - LOC TAX                            8    Q(4) #####.00
    50    QTD - SDI                                8    Q(5) #####.00
    51    QTD - SICK PAY                           8    Q(6) #####.00
    52    QTD - E.I.C.                             8    Q(7) #####.00
    53    QTD - NON TXBL                           8    Q(8) #####.00
    54    QTD - # WEEKS WRKD                       2    Q(9) ##
FCOEBL   -Bill of Lading Print File  ( 245 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    EMPLOYEE NO.                             5    An$(3,5)
     3    REG EARNINGS                             9    C(1) ######.00
     4    OT EARNINGS                              9    C(2) ######.00
     5    PREM EARNINGS                            9    C(3) ######.00
     6    SICK EARNINGS                            9    C(4) ######.00
     7    HOL EARNINGS                             9    C(5) ######.00
     8    VAC EARNINGS                             9    C(6) ######.00
     9    OTHER EARNINGS                           9    C(7) ######.00
    10    FUNERAL EARNINGS                         9    C(8) ######.00
    11    BONUS EARNINGS                           9    C(9) ######.00
    12    PER DIEM EARN                            9    C(10) ######.00
    13    EXPENSE ALLOW                            9    C(11) ######.00
    14    MISC (TXBL)                              9    C(12) ######.00
    15    MISC (NONTX)                             9    C(13) ######.00
    16    COMMISSION                               9    C(14) ######.00
    17    GROSS EARNINGS                          10    An #######.00
    18    NET EARNINGS                             9    Bn ######.00
    19    FED WAGE TAX                             9    D(1) ######.00
    20    F.I.C.A.                                 8    D(2) #####.00
    21    STE WAGE TAX                             9    D(3) ######.00
    22    LOC WAGE TAX                             8    D(4) #####.00
    23    S.D.I.                                   8    D(5) #####.00
    24    E.I.C.                                   8    D(6) #####.00
    25    # WEEKS WORKED                           2    D(7) ##
    26    401K                                     8    H(1) #####.00
    27    LIFE INSURANCE                           8    H(2) #####.00
    28    Medical Exp                              8    H(3) #####.00
    29    Admin Fees                               8    H(4) #####.00
    30    ADVANCES                                 8    H(5) #####.00
    31    HEALTH INS                               8    H(6) #####.00
    32    Child Care                               8    H(7) #####.00
    33    MISC DEDUCTNS                            8    H(8) #####.00
    34    REG HOURS                                8    I(1) #####.00
    35    OT HOURS                                 8    I(2) #####.00
    36    PREM HOURS                               8    I(3) #####.00
    37    SICK HOURS                               8    I(4) #####.00
    38    HOL HOURS                                8    I(5) #####.00
    39    VAC HOURS                                8    I(6) #####.00
    40    OTHER HOURS                              8    I(7) #####.00
    41    FUNERAL HOURS                            8    I(8) #####.00
    42    SICK LEAVE ACCR                          8    J(1) #####.00
    43    VAC HOURS ACCR                           8    J(2) #####.00
    44    LIFETIME HOURS                           7    J(3) ####.00
    45    LIFETIME DAYS                            8    J(4) #####.00
    46    ABSENTEE POINTS                          4    J(5) ####
    47    Link to Master                           1    J(6) #
FCOEBP   -Broker Commission Pct File  ( 246 at start)
     1    Company Code                             2    An$(1,2)
     2    Broker Code                              3    An$(3,3)
     3    Sales Category                           2    An$(6,2)
     4    (open)                                   1    Bn$
     5    (open)                                   1    Cn$
     6    (open)                                   1    Dn$
     7    Comm Pct - Dist                          6    An ##.00#
     8    Comm Pct - Rtl                           6    Bn ##.00#
FCCNVZJ  -Broker Master File  ( 247 at start)
     1    Key Type = 'J'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Broker Code                              3    An$(4,3)
     4    Broker Name                             30    Bn$
     5    Address Line 1                          30    Cn$
     6    Address Line 2                          30    Dn$
     7    Address Line 3                          30    En$
     8    (open)                                   1    An #
     9    YTD Brokerage                            9    Bn ######.00
    10    % Brokerage                              5    Cn ##.00
    11    Broker Division                          2    Fn$(1,2)
    12    Telephone Number                        10    Fn$(3,10)
    13    Brok Eligible?                           1    Fn$(13,1)
    14    Calculation Type                         1    Fn$(14,1)
    15    When Paid                                1    Fn$(15,1)
    16    (open)                                   1    Gn$
    17    (open)                                   1    Hn$
    18    Vendor Code - 1                          6    In$(1,6)
    19                - 2                          6    In$(7,6)
    20                - 3                          6    In$(13,6)
    21                - 4                          6    In$(19,6)
    22    Vendor Pct  - 1                          6    V(0) ###.00
    23                - 2                          6    V(1) ###.00
    24                - 3                          6    V(2) ###.00
    25                - 4                          6    V(3) ###.00
FCCNVZv  -CA Redemption Codes  ( 248 at start)
     1    Key Type = 'v'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    CRV Code                                 2    An$(4,2)
     4    Description                             30    Bn$
     5    (open)                                   1    Cn$
     6    (open)                                   1    Dn$
     7    CRV Amt/Unit                             5    An #.00#
     8    (open)                                   1    Bn
     9    (open)                                   1    Cn
    10    (open)                                   1    Dn
FCPOHH   -Purchase Order History Header File  ( 249 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    P/O NUMBER                               5    An$(3,5)
     3    RELEASE NUMBER                           2    An$(8,2)
     4    SUPPLIER NUMBER                          6    Bn$
     5    SUPPLIER NAME                           30    Cn$
     6    ADDR LINE 1                             30    Dn$
     7    ADDR LINE 2                             30    En$
     8    ADDR LINE 3                             30    Fn$
     9    ORDER PLACED BY/FOR                     20    Gn$
    10    ORDER ISSUED TO                         20    Hn$
    11    TERMS                                   20    In$
    12    F.O.B.                                  20    Jn$
    13    P/O REG FLAG                             1    Kn$(1,1)
    14    Vouchered (Y/N)                          1    Kn$(2,1)
    15    (open)                                   1    Kn$(3,1)
    16    PRINT FLAG                               1    Kn$(4,1)
    17    (open)                                   1    Kn$(5,1)
    18    Ammended P/O?                            1    Kn$(6,1)
    19    CONFIRMED FLAG                           1    Kn$(7,1)
    20    (open)                                   1    Kn$(8,1)
    21    P.O. RECVD COMPLETE?                     1    Kn$(9,1)
    22    TERMS CODE                               1    Kn$(10,1)
    23    TAXABLE?                                 1    Kn$(11,1)
    24    Carrier Code                             2    Kn$(12,2)
    25    Voucher Number                           6    Kn$(14,6)
    26    WAREHOUSE (I/C)                          4    Kn$(20,4)
    27    WAREHOUSE (DEL)                          4    Kn$(24,4)
    28    FOB CODE                                 2    Kn$(28,2)
    29    P/O Type                                 2    Kn$(30,2)
    30    (open)                                   9    Kn$(32,9)
    31    ORDER DATE                               6    On$(1,6)
    32    ETA DATE                                 6    On$(7,6)
    33    DATE WANTED                              8    Pn$(1,8)
    34    Date Ammended                            8    Pn$(9,8)
    35    CARRIER                                 20    Qn$
    36    LAST REC DATE                            6    Rn$ ######
    37    Discount Types                           3    Sn$(1,3)
    38    Freight Type                             1    Sn$(4,1)
    39    (open)                                   1    An #
    40    TOTAL UNITS                             10    Tn #######.00
    41    TOTAL WEIGHT                            10    Un #######.00
    42    TOTAL AMOUNT                            10    Vn #######.00
    43    Number of Lines                          3    Wn
    44    Operator Code                            3    Xn$
    45    Disc 1 - Rate/Amt                        8    TT(1) #####.00
    46    Disc 2 - Rate/Amt                        8    TT(2) #####.00
    47    Disc 3 - Rate/Amt                        8    TT(3) #####.00
    48    Freight Rate/Amt                         8    TT(4) ########
FCPOHD   -Purchase Order History Detail File  ( 250 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    P/O NUMBER                               5    An$(3,5)
     3    RELEASE NUMBER                           2    An$(8,2)
     4    LINE NO                                  3    An$(10,3) ###
     5    ITEM CODE (KEY)                         21    Bn$
     6    ITEM DESCRIPTION                        48    Cn$
     7    UNIT OF MEASURE                          2    Dn$
     8    ORDER QTY                                7    An #######
     9    NET UNIT COST                            9    Bn ####.00##
    10    QTY RECEIVED                             7    Cn #######
    11    Qty on order (I/C units)                 7    Dn #######
    12    (open)                                   1    En #
    13    LOT NUMBERS                             40    En$
    14    BIN NUMBERS                             30    Fn$
    15    WAREHOUSE CODE                           4    Gn$
    16    Unit Cost - FOB                          9    Fn ####.00##
    17    Freight Cost Per Unit                    8    Gn ###.00##
    18    Discount per unit                        8    Hn ###.00##
    19    DISCOUNT PERCENT                         6    In ###.00
    20    Wholesale Price                          7    Jn ####.00
    21    CONTRACT NUMBER                         10    Kn$(1,10)
    22    Freight Units                            2    Kn$(11,2)
    23    Discount Units                           2    Kn$(13,2)
    24    LINE ITEM TYPE (I/M)                     1    Kn$(15,1)
    25    (open)                                   5    Kn$(16,5)
    26    Conv Factor (to P/O units)              10    Ln$ #####.00##
    27    Promo Exp Date                           6    Mn$(1,6)
    28    Promo Eff Date                           6    Mn$(7,6)
    29    (open)                                  12    Mn$(13,12)
FCPOHD   -Purchase Order History Detail File  ( 251 at start)
     1    Key Type = 'if'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Item Flag                                1    An$(5,1)
     4    Description                             40    Bn$
     5    Invoice Print Text                      50    Cn$
     6    Kosher? (Y/N)                            1    Dn$
     7    Catalog Symbol                           2    En$
     8    Organic? (Y/N)                           1    Fn$
FCARJH   -A/R ADJUSTMENTS HEADER FILE MAINTENANCE   ( 252 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    ADJUSTMENT NO.                           6    An$(3,6)
     3    CUSTOMER NO.                             6    Bn$
     4    TRANSACTION AMOUNT                      12    An #########.00
     5    OLD A/R BALANCE                         12    Bn #########.00
     6    NEW A/R BALANCE                         12    Cn #########.00
     7    REASON CODE                              2    Cn$
     8    REF/INVOICE NO.                          6    Dn$
     9    TRANSACTION DATE                         6    En$
    10    ADJUSTMENT REASON                       12    Fn$
    11    CUSTOMER NAME                           40    Gn$
    12    COMPANY CODE                             2    Hn$
    13    RESERVED FOR FUTURE                      1    In$
    14    RESERVED FOR FUTURE                      1    Jn$
    15    RESERVED FOR FUTURE                      1    Kn$
    16    RESERVED FOR FUTURE                      1    Ln$
FCARJD   -A/R ADJUSTMENTS DETAIL FILE MAINTENANCE   ( 253 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    ADJUSTMENT NO.                           6    An$(3,6)
     3    G/L ACCOUNT                             11    An$(9,11)
     4    DISTRIBUTION AMOUNT                     12    An #########.00
     5    G/L ACCOUNT (A/R)                       11    Bn$
     6    JV REF #                                 5    Cn$
     7    RESERVED FOR FUTURE                      1    Dn$
     8    RESERVED FOR FUTURE                      1    En$
     9    RESERVED FOR FUTURE                      1    Fn$
FCARJD   -A/R ADJUSTMENTS DETAIL FILE MAINTENANCE   ( 254 at start)
     1    KEY                                      2
     2    NUMERIC 1 (2)                            2     ##
     3    NUMERIC 2 (6)                            6     ######
     4    NUMERIC 3 (9)                            9     ######.00
FCPRGL0  -PAYROLL MONTHLY G/L DISTRIBUTION CONTROL  ( 255 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    MONTH (YYMM)                             4    An$(3,4)
     3    PERIOD ENDING - 1                        6    Bn$(1,6)
     4    PERIOD ENDING - 2                        6    Bn$(7,6)
     5    PERIOD ENDING - 3                        6    Bn$(13,6)
     6    PERIOD ENDING - 4                        6    Bn$(19,6)
     7    PERIOD ENDING - 5                        6    Bn$(25,6)
FCPRLD0  -PAYROLL MONTHLY LABOR DISTRIBUTION CONTR  ( 256 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    MONTH (YYMM)                             4    An$(3,4)
     3    PERIOD ENDING - 1                        6    Bn$(1,6)
     4    PERIOD ENDING - 2                        6    Bn$(7,6)
     5    PERIOD ENDING - 3                        6    Bn$(13,6)
     6    PERIOD ENDING - 4                        6    Bn$(19,6)
     7    PERIOD ENDING - 5                        6    Bn$(25,6)
FCCNVZk  -Ordered By Master File  ( 257 at start)
     1    Key Type = 'k'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Ordered By Code                          2    An$(4,2)
     4    Ordered by Name                         30    Bn$
     5    Rep FAX                                 10    Cn$
     6    Add'l FAX                               10
     7    Price Lists                             10    Dn$
     8    Email Address                           40
     9    Changes only or Full (C/F)               1
FCICTF   -Pallet Tag File  ( 258 at start)
     1    Company Code                             2    An$(1,2)
     2    Tag Number                               8    An$(3,8) ########
     3    Item Code                                6    Bn$
     4    Date Reference                           8    Cn$
     5    Location Code                            6    Dn$
     6    Reference Number                        25    En$
     7    Date Printed                             8    Fn$
     8    Time Printed                             7     ####.00
     9    Expiration Date                          8
    10    Upstock Location                         6
    11    Total Upstock Qty                        6     ######
    12    Warning Code                             1
    13    Quality Check?                           1
FCICTT   -  ( 259 at start)
     1    Company Code                             2
     2    Item Code                                6
     3    Tag Number                               8     ########
     4    Location Code                            6
     5    Sequence No                              3     ###
     6    Quantity                                 6     ######
     7    Date Updated                             8
     8    Time Updated                             7     ####.00
     9    LDT Reference                            8
FCCNVZ>  -CASH ACCOUNT MAINTENANCE  ( 260 at start)
     1    KEY TYPE =">"                            1    AN$(1,1)
     2    COMPANY CODE                             2    AN$(2,2)
     3    CASH ACCOUNT CODE                        1    AN$(4,1)
     4    G/L CASH ACCOUNT NUMBER                 11    BN$
     5    DESCRIPTION                             30    CN$
     6    (OPEN)                                   1    DN$
     7    (OPEN)                                   1    EN$
     8    NEXT AVAILABLE CHECK NO                  6    AN ######
     9    (OPEN)                                   1    BN #
    10    (OPEN)                                   1    CN #
FCARHF   -Customer Payment History  ( 261 at start)
     1    Company Code                             2    An$(1,2)
     2    Customer Number                          6    An$(3,6)
     3    Invs -  1                                3    Bn$(1,3) ###
     4    Invs -  2                                3     ###
     5    Invs -  3                                3     ###
     6    Invs -  4                                3     ###
     7    Invs -  5                                3     ###
     8    Invs -  6                                3     ###
     9    Invs -  7                                3     ###
    10    Invs -  8                                3     ###
    11    Invs -  9                                3     ###
    12    Invs - 10                                3     ###
    13    Invs - 11                                3     ###
    14    Invs - 12                                3     ###
    15    Invs 13-24                              36    Bn$(37,36)
    16    Days -  1                                4    Cn$(1,4) ####
    17    Days -  2                                4     ####
    18    Days -  3                                4     ####
    19    Days -  4                                4     ####
    20    Days -  5                                4     ####
    21    Days  - 6                                4     ####
    22    Days  - 7                                4     ####
    23    Days -  8                                4     ####
    24    Days -  9                                4     ####
    25    Days - 10                                4     ####
    26    Days - 11                                4     ####
    27    Days - 12                                4     ####
    28    Days - 13-24                            48    Cn$(49,48)
FCARCI   -Customer Item Code File  ( 262 at start)
     1    Company Code                             2    An$(1,2)
     2    Customer Number                          6    An$(3,6)
     3    Our Item Code                            6    An$(9,6)
     4    Customer Item Code                      10    Bn$
FCCNVZ\  -PAYROLL COMPANY CONTROL RECORD  ( 270 at start)
     1    KEY GROUP = "CPR"                        3    An$(1,3)
     2    COMPANY CODE                             2    An$(4,2)
     3    PAY CYCLE... INITIALZ                    1    Bn$(1,1)
     4         TIME SHEET ENTRY                    1    Bn$(2,1)
     5         GROSS TO NET                        1    Bn$(3,1)
     6         P/R REGISTER                        1    Bn$(4,1)
     7         CHECKS                              1    Bn$(5,1)
     8         LABOR DISTR                         1    Bn$(6,1)
     9         G/L DISTRIB                         1    Bn$(7,1)
    10         PENSION ELIG                        1    Bn$(8,1)
    11         DUES LISTING                        1    Bn$(9,1)
    12         FINAL REG/UPDATE                    1    Bn$(10,1)
    13    MONTH-END... ABSENTEE                    1    Cn$(1,1)
    14    MONTH-END... LABR DISTR                  1    Cn$(2,1)
    15         PENSION REPORT                      1    Cn$(3,1)
    16         INSURANCE                           1    Cn$(4,1)
    17         WORKER'S COMP                       1    Cn$(5,1)
    18         UNEMPLOY COMP                       1    Cn$(6,1)
    19         DUES LISTING                        1    Cn$(7,1)
    20         VAC/SICK LEAVE                      1    Cn$(8,1)
    21         G/L DISTR                           1    Cn$(9,1)
    22         UPDATE                              1    Cn$(10,1)
    23    QUARTER-END ... 941 FORMS                1    Dn$(1,1)
    24         WAGE & TAX REPORTS                  1    Dn$(2,1)
    25         UPDATE                              1    Dn$(3,1)
    26    YEAR-END ... MASTER LIST                 1    En$(1,1)
    27         W-2 FORMS                           1    En$(2,1)
    28         SENIORITY LIST                      1    En$(3,1)
    29         BIRTHDAY LIST                       1    En$(4,1)
    30         EMPLOYEE UPDATE                     1    En$(5,1)
    31         G/L UPDATE                          1    En$(6,1)
    32    CHECK RECON?                             1    Fn$(1,1)
    33    SICK PAY IN FICA?                        1    Fn$(2,1)
    34    (OPEN)                                   3    Fn$(3,3)
    35    CURRENT MONTH (YYMM)                     4    Gn$
    36    CURR WEEK 1                              6    H6$(1,6)
    37    CURR WEEK 2                              6    H6$(7,6)
    38    CURR WEEK 3                              6    H6$(13,6)
    39    CURR WEEK 4                              6    H6$(19,6)
    40    CURR WEEK 5                              6    H6$(25,6)
    41    NEXT AVAILABLE CHECK NUMBER              6    An ######
    42    (OPEN)                                   1    Bn #
    43    (OPEN)                                   1    Cn #
    44    (OPEN)                                   1    Dn #
    45    (OPEN)                                   1    En #
FCCNVZ]  -A/R APPLICATION CONTROL RECORD  ( 272 at start)
     1    KEY GROUP = "]"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    UNION CONTRACT NUMBER                    6    An$(4,6)
     4    DESCRIPTION                             25    Bn$
     5    (OPEN)                                  10    Cn$
     6    UNION BENEFITS - LOW DAYS                7    An ####.00
     7                   - HIGH DAYS               7    Bn ####.00
     8    PENSION BENEFITS - LOW HOURS             7    Cn ####.00
     9                     - HIGH HOURS            7    Dn ####.00
    10    (OPEN)                                   1    En #
    11    (OPEN)                                   1    Fn #
FCCNVZr  -CREDIT/DEBIT MEMO REASON CODE FILE MAINT  ( 273 at start)
     1    KEY GROUP = "r"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    SHIFT CODE                               2    An$(4,2)
     4    DESCRIPTION                             25    Bn$
     5    (OPEN)                                  10    Cn$
     6    STANDARD RATE                            8    An ###.00##
     7    SHIFT DIFFERENTIAL (PER HOUR)            8    Bn ###.00##
     8    (OPEN)                                   1    Cn #
     9    (OPEN)                                   1    Dn #
    10    (OPEN)                                   1    En #
FCSATI   -Customer/Item Weekly S/A Trend  ( 274 at start)
     1    Company Code                             2    A$(1,2)
     2    Key Type = 'T'                           1    An$(3,1)
     3    Customer Number                          6    An$(4,6)
     4    Ship to Code                             4    An$(10,4)
     5    Item Code                                6    An$(14,6)
     6    PERIOD 1 UNIT SALES                      6    A(0) ######
     7    PERIOD 2 UNIIT SALES                     6    A(1) ######
     8    PERIOD 3 UNIT SALES                      6    A(2) ######
     9    PERIOD 4 UNIT SALES                      6    A(3) ######
    10    PERIOD 5 UNIT SALES                      6    A(4) ######
    11    PERIOD 6 UNIT SALES                      6    A(5) ######
    12    PERIOD 7 UNIT SALES                      6    A(6) ######
    13    PERIOD 8 UNIT SALES                      6    A(7) ######
    14    PERIOD 9 UNIT SALES                      6    A(8) ######
    15    PERIOD 10 UNIT SALES                     6    A(9) ######
    16    PERIOD 11 UNIT SALES                     6    A(10) ######
    17    PERIOD 12 UNIT SALES                     6    A(11) ######
    18    PERIOD 13 UNIT SALES                     6    A(12) ######
FCJSIDH  -JOB-STREAM I.D.MASTER FILE - HEADER   ( 275 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    JOB-STREAM I.D.                          2    An$(3,2)
     3    STEP NO.(00)                             2    An$(5,2)
     4    (OPEN)                                   1    Bn$(1,1)
     5    NUMBER OF STEPS                          3    Bn$(2,3)
     6    (OPEN)                                   7    Bn$(5,6)
     7    JOB-STREAM DESCRIPTION                  20    Cn$
     8    (OPEN)                                   1    Dn$
     9    LAST RUN: DATE - SELECT STARTD           6    En$(1,6)
    10                   - RUN STARTED             6    En$(7,6)
    11                   - RUN COMPLETE            6    En$(13,6)
    12    LAST RUN: TIME - SELECT STARTD           5    Fn$(1,5)
    13                   - RUN STARTED             5    Fn$(6,5)
    14                   - RUN COMPLETE            5    Fn$(11,5)
FCJSIDD  -JOB-STREAM I.D. MASTER FILE - DETAIL REC  ( 276 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    JOB-STREAM I.D.                          2    An$(3,2)
     3    JOB-STREAM STEP NO.                      2    An$(5,2) ##
     4    STATUS                                   3    Bn$(1,3)
     5    FORMS I.D.                               2    Bn$(4,2)
     6    (OPEN)                                   5    Bn$(6,5)
     7    SELECTOR NO.                             2    Cn$(1,2)
     8    UASQ INDEX                               4    Cn$(3,4)
     9    RUN PROGRAM                              6    Dn$
    10    INTERRUPT INFO                          20    En$
    11    IOL PARMS AS NEEDED                      6    Fn$
FCNCdd   -NCR TRANSACTION FILE  ( 277 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    TRANS DATE (YYMMDD)                      6    An$(3,6)
     3    REGISTER NUMBER                          2    An$(9,2) ##
     4    TRANSACTION NUMBER                       6    An$(11,6) ######
     5    SEQUENCE NUMBER                          4    An$(17,4)
     6    RECORD TYPE                              2    Bn$(1,2)
     7    ITEM CODE                                6    Bn$(3,6)
     8    TAPE INDEX                               5    Bn$(9,5) #####
     9    TIME                                     4    Bn$(14,4) ####
    10    (open)                                   2    Bn$(18,2)
    11    CUSTOMER NUMBER                          6    Cn$(1,6)
    12    INVOICE NUMBER                           6    Cn$(7,6)
    13    QUANTITY                                 6    An ######
    14    UNIT PRICE                               9    Bn ######.00
    15    EXTENSION                                9    Cn ######.00
    16    (open)                                   1    Dn
    17    (open)                                   1    En
    18    (open)                                   1    Fn
    19    (open)                                   1    Gn
FCNCST   -  ( 278 at start)
     1    RECORD TYPE (16=CHG,0B=PYMT)             2    An$(1,2)
     2    REGISTER NUMBER                          2    An$(3,2)
     3    CUSTOMER NUMBER                          6    An$(5,6)
     4    INVOICE NUMBER                           6    An$(11,6)
     5    REGISTER                                 2    Bn$(1,2)
     6    TRANSACTION NUMBER                       6    Bn$(3,6)
     7    TRANSACTION SEQUENCE                     2    Bn$(9,4)
     8    AMOUNT                                   8    Cn #####.00
FCSATRW  -Weekly Item Sales Trend Analysis File  ( 279 at start)
     1    Company Code                             2    A$(1,2)
     2    Key Group = 'W'                          1    An$(3,1)
     3    (open)                                   1    An$(4,1)
     4    Item Code                                6    AN$(5,6)
     5    PERIOD 1 UNIT SALES                      6    A(0) ######
     6    PERIOD 2 UNIIT SALES                     6    A(1) ######
     7    PERIOD 3 UNIT SALES                      6    A(2) ######
     8    PERIOD 4 UNIT SALES                      6    A(3) ######
     9    PERIOD 5 UNIT SALES                      6    A(4) ######
    10    PERIOD 6 UNIT SALES                      6    A(5) ######
    11    PERIOD 7 UNIT SALES                      6    A(6) ######
    12    PERIOD 8 UNIT SALES                      6    A(7) ######
    13    PERIOD 9 UNIT SALES                      6    A(8) ######
    14    PERIOD 10 UNIT SALES                     6    A(9) ######
    15    PERIOD 11 UNIT SALES                     6    A(10) ######
    16    PERIOD 12 UNIT SALES                     6    A(11) ######
    17    PERIOD 13 UNIT SALES                     6    A(12) ######
FCSATRM  -Monthly Sales Trend File  ( 280 at start)
     1    Company Code                             2    A$(1,2)
     2    Key Group = 'M'                          1    An$(3,1)
     3    (open)                                   1    An$(4,1)
     4    Item Code                                6    A$(5,6)
     5    YEAR                                     2    A$(11,2)
     6    PERIOD 1 UNIT SALES                      6    A(0) ######
     7    PERIOD 2 UNIIT SALES                     6    A(1) ######
     8    PERIOD 3 UNIT SALES                      6    A(2) ######
     9    PERIOD 4 UNIT SALES                      6    A(3) ######
    10    PERIOD 5 UNIT SALES                      6    A(4) ######
    11    PERIOD 6 UNIT SALES                      6    A(5) ######
    12    PERIOD 7 UNIT SALES                      6    A(6) ######
    13    PERIOD 8 UNIT SALES                      6    A(7) ######
    14    PERIOD 9 UNIT SALES                      6    A(8) ######
    15    PERIOD 10 UNIT SALES                     6    A(9) ######
    16    PERIOD 11 UNIT SALES                     6    A(10) ######
    17    PERIOD 12 UNIT SALES                     6    A(11) ######
FCCNVZP3 -Split Case Charges  ( 281 at start)
     1    Key Group ="P3"                          2    An$(1,2)
     2    Company Code                             2    AN$(3,2)
     3    Split Case Code                          1    An$(5,1)
     4    Per Case,Unit,Line item(C,U,L)           1    Bn$(1,1)
     5    Amount (A) or Percent (P)                1    Bn$(2,1)
     6    (open)                                   1    Bn$(3,3)
     7    Actual Amount or Percent                 9    Cn ####.00##
FCSAVL   -Customer Velocity Detail File  ( 282 at start)
     1    Key Type = 'V'                           1    AN$(1,1)
     2    COMPANY                                  2    AN$(2,2)
     3    CUSTOMER                                 6    An$(3,6)
     4    SHIP TO                                  2    An$(9,2)
     5    Prod Category                            2    An$(11,2)
     6    Item Code                               12    An$(13,12)
     7    Units Week 1                             8    D(0) ########
     8    -Prv Week                                7    D(1) #######
     9    -PRV 2                                   7    D(4) #######
    10    -PRV 3                                   7    D(5) #######
    11    -PRV 4                                   7    D(6) #######
    12    -PRV 5                                   7    D(7) #######
    13    -PRV 6                                   7    D(8) #######
    14    -PRV 7                                   7    D(9) #######
    15    -PRV 8                                   7    D(10) #######
    16    -PRV 9                                   7    D(11) #######
    17    -PRV 10                                  7    D(12) #######
    18    -PRV 11                                  7    D(13) #######
    19    -PRV 12                                  7    D(14) #######
    20    -PRV 13                                  7    D(15) #######
    21    Sales Week 1                             8    F(2) ########
    22                                             7    F(3) #######
    23                                             7    F(4) #######
    24                                             7    F(5) #######
    25                                             7    F(6) #######
    26                                             7    F(7) #######
    27                                             7    F(8) #######
    28                                             7    F(9) #######
    29                                             7    F(10) #######
    30                                             7    F(11) #######
    31                                             7    F(12) #######
    32                                             7    F(13) #######
    33                                             7    F(14) #######
    34                                             7    F(15) #######
    35    Gr.M. Week 1                             8    G(2) ########
    36                                             7    G(3) #######
    37                                             7    G(4) #######
    38                                             7    G(5) #######
    39                                             7    G(6) #######
    40                                             7    G(7) #######
    41                                             7    G(8)  #######
    42                                             7    G(9) #######
    43                                             7    G(10) #######
    44                                             7    G(11) #######
    45                                             7    G(12) #######
    46                                             7    G(13) #######
    47                                             7    G(14) #######
    48                                             7    G(15) #######
FCSATRC  -Weekly Customer Sales Trend Analysis  ( 283 at start)
     1    Company Code                             2    A$(1,2)
     2    Key Group = 'W'                          1    An$(3,1)
     3    (open)                                   1    An$(4,1)
     4    Item Code                                6    AN$(5,6)
     5    PERIOD 1 UNIT SALES                      6    A(0) ######
     6    PERIOD 2 UNIIT SALES                     6    A(1) ######
     7    PERIOD 3 UNIT SALES                      6    A(2) ######
     8    PERIOD 4 UNIT SALES                      6    A(3) ######
     9    PERIOD 5 UNIT SALES                      6    A(4) ######
    10    PERIOD 6 UNIT SALES                      6    A(5) ######
    11    PERIOD 7 UNIT SALES                      6    A(6) ######
    12    PERIOD 8 UNIT SALES                      6    A(7) ######
    13    PERIOD 9 UNIT SALES                      6    A(8) ######
    14    PERIOD 10 UNIT SALES                     6    A(9) ######
    15    PERIOD 11 UNIT SALES                     6    A(10) ######
    16    PERIOD 12 UNIT SALES                     6    A(11) ######
    17    PERIOD 13 UNIT SALES                     6    A(12) ######
FCSATRD  -Monthly Customer Sales Trend  ( 284 at start)
     1    Company Code                             2    A$(1,2)
     2    Key Group = 'D '                         2    An$(3,2)
     3    Customer Code                            6    An$(5,6)
     4    Ship-to Code                             4    An$(11,4)
     5    Year (YY)                                2    An$(15,2)
     6    Period 1 Dollar Sales                    6    A(0) ######
     7        - Period 2                           6    A(1) ######
     8        - Period 3                           6    A(2) ######
     9        - Period 4                           6    A(3) ######
    10        - Period 5                           6    A(4) ######
    11        - Period 6                           6    A(5) ######
    12        - Period 7                           6    A(6) ######
    13        - Period 8                           6    A(7) ######
    14        - Period 9                           6    A(8) ######
    15        - Period 10                          6    A(9) ######
    16        - Period 11                          6    A(10) ######
    17        - Period 12                          6    A(11) ######
    18        - Period 13                          6    A(12) ######
FCSAHFP  -SALES ANALYSIS CUSTOMER-PROD CATEGORY  ( 285 at start)
     1    KEY TYPE = 'P'                           1    AN$(1,1)
     2    COMPANY CODE                             2    AN$(2,2)
     3    CUSTOMER NUMBER                          6    AN$(4,6)
     4    SHIP TO ID                               2    AN$(10,2)
     5    PRODUCT CATEORY                          2    An$(12,2)
     6    LAST ORDER DATE                          6    Bn$(1,6)
     7    (open)                                   1    Bn$(7,1)
     8    LARGEST QUANTITY                         7    CN #######
     9    TOTAL QUANTITY                           8    DN ########
    10    NUMBER OF ORDERS                         4    EN ####
    11    UNIT SALES - MTD                         7    Fn #######
    12    UNIT SALES - LAST MONTH                  7    Gn #######
    13    UNIT SALES - YTD                         8    Hn ########
    14    UNIT SALES - LAST YEAR                   8    In ########
FCCNVZr  -CREDIT/DEBIT MEMO REASON CODE FILE MAINT  ( 286 at start)
     1    KEY GROUP = "r"                          1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    SHIFT CODE                               2    An$(4,2)
     4    DESCRIPTION                             25    Bn$
     5    (OPEN)                                  10    Cn$
     6    STANDARD RATE                            8    An ###.00##
     7    SHIFT DIFFERENTIAL (PER HOUR)            8    Bn ###.00##
     8    (OPEN)                                   1    Cn #
     9    (OPEN)                                   1    Dn #
    10    (OPEN)                                   1    En #
FCSATC   -Customer/Invoice Weekly Trend  ( 287 at start)
     1    Company Code                             2    A$(1,2)
     2    Key Type = 'C'                           1    An$(3,1)
     3    Customer Number                          6    An$(4,6)
     4    Ship to Code                             4    An$(10,4)
     5    Period  1 Invoice Nos                   30    INV1$
     6    Period  2 Invoice Nos                   30    INV2$
     7    Period  3 Invoice Nos                   30    INV3$
     8    Period  4 Invoice Nos                   30    INV4$
     9    Period  5 Invoice Nos                   30    INV5$
    10    Period  6 Invoice Nos                   30    INV6$
    11    Period  7 Invoice Nos                   30    INV7$
    12    Period  8 Invoice Nos                   30    INV8$
    13    Period  9 Invoice Nos                   30    INV9$
    14    Period 10 Invoice Nos                   30    INV10$
    15    Period 11 Invoice Nos                   30    INV11$
    16    Period 12 Invoice Nos                   30    INV12$
    17    Period 13 Invoice Nos                   30    INV13$
FCSADE   -Target Item Sales Detail File  ( 288 at start)
     1    Company Code                             2    An$(1,2)
     2    Item Code                                6    An$(3,6)
     3    Customer Code                            6    An$(9,6)
     4    Ship-to Code                             4    An$(15,4)
     5    Invoice Date                             6    An$(19,6)
     6    Invoice Number                           6    An$(25,6)
     7    Release Number                           2    An$(31,2)
     8    Invoice Date                             6    Bn$(1,6)
     9    (open)                                   6    Bn$(7,6)
    10    Cases Sold                               4    Cn ####
    11    Eaches Sold                              6    Dn ######
    12    Sales Amount                             9    En ######.00
FCSADFR  -Sales Analysis - Route Record  ( 289 at start)
     1    KEY TYPE = 'R'                           1    AN$(1,1)
     2    COMPANY                                  2    AN$(2,2)
     3    Route                                    3    An$(4,3)
     4    CUST TYPE                                2    An$(6,2)
     5    UNITS-YTD                                7    D(0) #######
     6    -LST YTD                                 7    D(1) #######
     7    -CUR MTH                                 7    D(2) #######
     8    -PRV MTH                                 7    D(3) #######
     9    -PRV 2                                   7    D(4) #######
    10    -PRV 3                                   7    D(5) #######
    11    -PRV 4                                   7    D(6) #######
    12    -PRV 5                                   7    D(7) #######
    13    -PRV 6                                   7    D(8) #######
    14    -PRV 7                                   7    D(9) #######
    15    -PRV 8                                   7    D(10) #######
    16    -PRV 9                                   7    D(11) #######
    17    -PRV 10                                  7    D(12) #######
    18    -PRV 11                                  7    D(13) #######
    19    -PRV 12                                  7    D(14) #######
    20    -PRV 13                                  7    D(15) #######
    21                                             1    EN$
    22                                             1    FN$
    23    CWT - YTD                                8    E(0) ########
    24                                             8    E(1) ########
    25                                             8    E(2) ########
    26                                             7    E(3) #######
    27                                             7    E(4) #######
    28                                             7    E(5) #######
    29                                             7    E(6) #######
    30                                             7    E(7) #######
    31                                             7    E(8) #######
    32                                             7    E(9) #######
    33                                             7    E(10) #######
    34                                             7    E(11) #######
    35                                             7    E(12) #######
    36                                             7    E(13) #######
    37                                             7    E(14) #######
    38                                             7    E(15) #######
    39    SALES-YTD                                8    F(0) ########
    40                                             8    F(1) ########
    41                                             8    F(2) ########
    42                                             7    F(3) #######
    43                                             7    F(4) #######
    44                                             7    F(5) #######
    45                                             7    F(6) #######
    46                                             7    F(7) #######
    47                                             7    F(8) #######
    48                                             7    F(9) #######
    49                                             7    F(10) #######
    50                                             7    F(11) #######
    51                                             7    F(12) #######
    52                                             7    F(13) #######
    53                                             7    F(14) #######
    54                                             7    F(15) #######
    55    COST-YTD                                 8    G(0) ########
    56                                             8    G(1) ########
    57                                             8    G(2) ########
    58                                             7    G(3) #######
    59                                             7    G(4) #######
    60                                             7    G(5) #######
    61                                             7    G(6) #######
    62                                             7    G(7) #######
    63                                             7    G(8)  #######
    64                                             7    G(9) #######
    65                                             7    G(10) #######
    66                                             7    G(11) #######
    67                                             7    G(12) #######
    68                                             7    G(13) #######
    69                                             7    G(14) #######
    70                                             7    G(15) #######
FCSADFP  -SALES ANALYSIS - PRODUCT RECORD  ( 290 at start)
     1    KEY TYPE = 'P'                           1    AN$(1,1)
     2    COMPANY                                  2    AN$(2,2)
     3    SALESMAN                                 2    AN$(4,2)
     4    CATEGORY                                 1    AN$(6,1)
     5    ITEM                                    12    AN$(7,12)
     6    UNITS-YTD                                8    D(0) ########
     7    -LST YTD                                 8    D(1) ########
     8    -CUR MTH                                 8    D(2) ########
     9    -PRV MTH                                 7    D(3) #######
    10    -PRV 2                                   7    D(4) #######
    11    -PRV 3                                   7    D(5) #######
    12    -PRV 4                                   7    D(6) #######
    13    -PRV 5                                   7    D(7) #######
    14    -PRV 6                                   7    D(8) #######
    15    -PRV 7                                   7    D(9) #######
    16    -PRV 8                                   7    D(10) #######
    17    -PRV 9                                   7    D(11) #######
    18    -PRV 10                                  7    D(12) #######
    19    -PRV 11                                  7    D(13) #######
    20    -PRV 12                                  7    D(14) #######
    21    -PRV 13                                  7    D(15) #######
    22                                             1    EN$
    23                                             1    FN$
    24    CWT - YTD                                8    E(0) ########
    25                                             8    E(1) ########
    26                                             8    E(2) ########
    27                                             7    E(3) #######
    28                                             7    E(4) #######
    29                                             7    E(5) #######
    30                                             7    E(6) #######
    31                                             7    E(7) #######
    32                                             7    E(8) #######
    33                                             7    E(9) #######
    34                                             7    E(10) #######
    35                                             7    E(11) #######
    36                                             7    E(12) #######
    37                                             7    E(13) #######
    38                                             7    E(14) #######
    39                                             7    E(15) #######
    40    SALES-YTD                                8    F(0) ########
    41                                             8    F(1) ########
    42                                             8    F(2) ########
    43                                             7    F(3) #######
    44                                             7    F(4) #######
    45                                             7    F(5) #######
    46                                             7    F(6) #######
    47                                             7    F(7) #######
    48                                             7    F(8) #######
    49                                             7    F(9) #######
    50                                             7    F(10) #######
    51                                             7    F(11) #######
    52                                             7    F(12) #######
    53                                             7    F(13) #######
    54                                             7    F(14) #######
    55                                             7    F(15) #######
    56    COST-YTD                                 8    G(0) ########
    57                                             8    G(1) ########
    58                                             8    G(2) ########
    59                                             7    G(3) #######
    60                                             7    G(4) #######
    61                                             7    G(5) #######
    62                                             7    G(6) #######
    63                                             7    G(7) #######
    64                                             7    G(8)  #######
    65                                             7    G(9) #######
    66                                             7    G(10) #######
    67                                             7    G(11) #######
    68                                             7    G(12) #######
    69                                             7    G(13) #######
    70                                             7    G(14) #######
    71                                             7    G(15) #######
FCSADFS  -SALES ANALYSIS - CUSTOMER RECORD  ( 291 at start)
     1    KEY TYPE = 'S'                           1    AN$(1,1)
     2    COMPANY                                  2    AN$(2,2)
     3    SALESMAN                                 2    AN$(4,2)
     4    CUSTOMER                                 6    AN$(6,6)
     5    SHIP TO                                  2    AN$(12,2)
     6    UNITS-YTD                                8    D(0) ########
     7    -LST YTD                                 8    D(1) ########
     8    -CUR MTH                                 8    D(2) ########
     9    -PRV MTH                                 7    D(3) #######
    10    -PRV 2                                   7    D(4) #######
    11    -PRV 3                                   7    D(5) #######
    12    -PRV 4                                   7    D(6) #######
    13    -PRV 5                                   7    D(7) #######
    14    -PRV 6                                   7    D(8) #######
    15    -PRV 7                                   7    D(9) #######
    16    -PRV 8                                   7    D(10) #######
    17    -PRV 9                                   7    D(11) #######
    18    -PRV 10                                  7    D(12) #######
    19    -PRV 11                                  7    D(13) #######
    20    -PRV 12                                  7    D(14) #######
    21    -PRV 13                                  7    D(15) #######
    22                                             1    EN$
    23                                             1    FN$
    24    CWT - YTD                                8    E(0) ########
    25                                             8    E(1) ########
    26                                             8    E(2) ########
    27                                             7    E(3) #######
    28                                             7    E(4) #######
    29                                             7    E(5) #######
    30                                             7    E(6) #######
    31                                             7    E(7) #######
    32                                             7    E(8) #######
    33                                             7    E(9) #######
    34                                             7    E(10) #######
    35                                             7    E(11) #######
    36                                             7    E(12) #######
    37                                             7    E(13) #######
    38                                             7    E(14) #######
    39                                             7    E(15) #######
    40    SALES-YTD                                8    F(0) ########
    41                                             8    F(1) ########
    42                                             8    F(2) ########
    43                                             7    F(3) #######
    44                                             7    F(4) #######
    45                                             7    F(5) #######
    46                                             7    F(6) #######
    47                                             7    F(7) #######
    48                                             7    F(8) #######
    49                                             7    F(9) #######
    50                                             7    F(10) #######
    51                                             7    F(11) #######
    52                                             7    F(12) #######
    53                                             7    F(13) #######
    54                                             7    F(14) #######
    55                                             7    F(15) #######
    56    COST-YTD                                 8    G(0) ########
    57                                             8    G(1) ########
    58                                             8    G(2) ########
    59                                             7    G(3) #######
    60                                             7    G(4) #######
    61                                             7    G(5) #######
    62                                             7    G(6) #######
    63                                             7    G(7) #######
    64                                             7    G(8)  #######
    65                                             7    G(9) #######
    66                                             7    G(10) #######
    67                                             7    G(11) #######
    68                                             7    G(12) #######
    69                                             7    G(13) #######
    70                                             7    G(14) #######
    71                                             7    G(15) #######
FCSADFI  -SALES ANALYSIS - INDUSTRY RECORD  ( 292 at start)
     1    KEY TYPE = 'I'                           1    AN$(1,1)
     2    COMPANY                                  2    AN$(2,2)
     3    CUSTOMER TYPE                            2    AN$(4,2)
     4    UNITS-YTD                                8    D(0) ########
     5    -LST YTD                                 8    D(1) ########
     6    -CUR MTH                                 8    D(2) ########
     7    -PRV MTH                                 7    D(3) #######
     8    -PRV 2                                   7    D(4) #######
     9    -PRV 3                                   7    D(5) #######
    10    -PRV 4                                   7    D(6) #######
    11    -PRV 5                                   7    D(7) #######
    12    -PRV 6                                   7    D(8) #######
    13    -PRV 7                                   7    D(9) #######
    14    -PRV 8                                   7    D(10) #######
    15    -PRV 9                                   7    D(11) #######
    16    -PRV 10                                  7    D(12) #######
    17    -PRV 11                                  7    D(13) #######
    18    -PRV 12                                  7    D(14) #######
    19    -PRV 13                                  7    D(15) #######
    20                                             1    EN$
    21                                             1    FN$
    22    CWT - YTD                                8    E(0) ########
    23                                             8    E(1) ########
    24                                             8    E(2) ########
    25                                             7    E(3) #######
    26                                             7    E(4) #######
    27                                             7    E(5) #######
    28                                             7    E(6) #######
    29                                             7    E(7) #######
    30                                             7    E(8) #######
    31                                             7    E(9) #######
    32                                             7    E(10) #######
    33                                             7    E(11) #######
    34                                             7    E(12) #######
    35                                             7    E(13) #######
    36                                             7    E(14) #######
    37                                             7    E(15) #######
    38    SALES-YTD                                8    F(0) ########
    39                                             8    F(1) ########
    40                                             8    F(2) ########
    41                                             7    F(3) #######
    42                                             7    F(4) #######
    43                                             7    F(5) #######
    44                                             7    F(6) #######
    45                                             7    F(7) #######
    46                                             7    F(8) #######
    47                                             7    F(9) #######
    48                                             7    F(10) #######
    49                                             7    F(11) #######
    50                                             7    F(12) #######
    51                                             7    F(13) #######
    52                                             7    F(14) #######
    53                                             7    F(15) #######
    54    COST-YTD                                 8    G(0) ########
    55                                             8    G(1) ########
    56                                             8    G(2) ########
    57                                             7    G(3) #######
    58                                             7    G(4) #######
    59                                             7    G(5) #######
    60                                             7    G(6) #######
    61                                             7    G(7) #######
    62                                             7    G(8)  #######
    63                                             7    G(9) #######
    64                                             7    G(10) #######
    65                                             7    G(11) #######
    66                                             7    G(12) #######
    67                                             7    G(13) #######
    68                                             7    G(14) #######
    69                                             7    G(15) #######
FCSADFT  -SALES ANALYSIS - TERRITORY RECORD  ( 293 at start)
     1    KEY TYP=T                                1    AN$(1,1)
     2    COMPANY                                  2    AN$(2,2)
     3    TERRITORY                                3    An$(4,3)
     4    CUST TYPE                                2    An$(6,2)
     5    UNITS-YTD                                7    D(0) #######
     6    -LST YTD                                 7    D(1) #######
     7    -CUR MTH                                 7    D(2) #######
     8    -PRV MTH                                 7    D(3) #######
     9    -PRV 2                                   7    D(4) #######
    10    -PRV 3                                   7    D(5) #######
    11    -PRV 4                                   7    D(6) #######
    12    -PRV 5                                   7    D(7) #######
    13    -PRV 6                                   7    D(8) #######
    14    -PRV 7                                   7    D(9) #######
    15    -PRV 8                                   7    D(10) #######
    16    -PRV 9                                   7    D(11) #######
    17    -PRV 10                                  7    D(12) #######
    18    -PRV 11                                  7    D(13) #######
    19    -PRV 12                                  7    D(14) #######
    20    -PRV 13                                  7    D(15) #######
    21                                             1    EN$
    22                                             1    FN$
    23    CWT - YTD                                8    E(0) ########
    24                                             8    E(1) ########
    25                                             8    E(2) ########
    26                                             7    E(3) #######
    27                                             7    E(4) #######
    28                                             7    E(5) #######
    29                                             7    E(6) #######
    30                                             7    E(7) #######
    31                                             7    E(8) #######
    32                                             7    E(9) #######
    33                                             7    E(10) #######
    34                                             7    E(11) #######
    35                                             7    E(12) #######
    36                                             7    E(13) #######
    37                                             7    E(14) #######
    38                                             7    E(15) #######
    39    SALES-YTD                                8    F(0) ########
    40                                             8    F(1) ########
    41                                             8    F(2) ########
    42                                             7    F(3) #######
    43                                             7    F(4) #######
    44                                             7    F(5) #######
    45                                             7    F(6) #######
    46                                             7    F(7) #######
    47                                             7    F(8) #######
    48                                             7    F(9) #######
    49                                             7    F(10) #######
    50                                             7    F(11) #######
    51                                             7    F(12) #######
    52                                             7    F(13) #######
    53                                             7    F(14) #######
    54                                             7    F(15) #######
    55    COST-YTD                                 8    G(0) ########
    56                                             8    G(1) ########
    57                                             8    G(2) ########
    58                                             7    G(3) #######
    59                                             7    G(4) #######
    60                                             7    G(5) #######
    61                                             7    G(6) #######
    62                                             7    G(7) #######
    63                                             7    G(8)  #######
    64                                             7    G(9) #######
    65                                             7    G(10) #######
    66                                             7    G(11) #######
    67                                             7    G(12) #######
    68                                             7    G(13) #######
    69                                             7    G(14) #######
    70                                             7    G(15) #######
FCSADT   -SALES ANALYSIS DETAIL FILE MAINTENANCE & INQUIRY  ( 294 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    S/A PERIOD                               4    An$(3,4)
     3    INVOICE DATE                             6    An$(7,6)
     4    INVOICE NUMBER                           6    An$(13,6)
     5    Item Code                                6    An$(19,6)
     6    Invoice Line No                          3    An$(25,3)
     7    Sequence No                              3    An$(28,3)
     8    WAREHOUSE                                4    An$(31,4)
     9    S/A Period Ending Date                   6    Bn$(1,6)
    10    (open)                                   6    Bn$(7,6)
    11    Transaction type = '2'                   1    Cn$(1,1)
    12    Pricing Units                            2    Cn$(2,2)
    13    Sales Units                              2    Cn$(4,2)
    14    Customer Code                            6    Cn$(6,6)
    15    Price List Code                          1    Cn$(12,1)
    16    (open)                                   1    Cn$(13,1)
    17    Target Item(Y/N)                         1    Cn$(14,1)
    18    Order Type                               2    Cn$(15,2)
    19    Sales Rep Code                           3    Cn$(17,3)
    20    Taxing Authority                         2    Cn$(20,2)
    21    Velocity Report (Y/N)                    1    Cn$(22,1)
    22    CA Redemption Code                       2    Cn$(23,2)
    23    Route Code                               3    Cn$(25,3)
    24    Stop Code                                3    Cn$(28,3)
    25    Territory Code                           3    Cn$(31,3)
    26    Product Category                         2    Cn$(34,2)
    27    Warehouse Category                       1    Cn$(36,1)
    28    G/L CATEGORY                             1    Cn$(37,1)
    29    Ship-to Code                             4    Cn$(38,4)
    30    Supplier Code                            6    Cn$(42,6)
    31    Ordered By                               2    Cn$(48,2)
    32    (open)                                   1    Dn$
    33    Cases Shipped                            9    Q(0) #########
    34    LBS Shipped                              9    Q(1) ######.00
    35    Price Extension                         10    Q(2) #######.00
    36    Cost Extension                          10    Q(3) #######.00
    37    Eaches Shipped                           9    Q(4) #########
    38    Pack Quantity                            9    Q(5) ####.00##
    39    (open)                                   1    Q(11)
    40    Total Discount                           8    Q(6) ####.00#
    41    Retail Extension                         6    Q(7) ###.00
FCSAHFC  -SALES ANALYSIS CUSTOMER - PRODUCT RECORD  ( 295 at start)
     1    KEY TYPE = 'C'                           1    AN$(1,1)
     2    COMPANY CODE                             2    AN$(2,2)
     3    CUSTOMER NUMBER                          6    AN$(4,6)
     4    Ship-to ID                               4    An$(10,4)
     5    Product Code                             6    An$(14,6)
     6    Product key, pos 7,6 (co+whs)            6    An$(20,6)
     7    LAST ORDER DATE                          6    Bn$(1,6)
     8    (open)                                   1    Bn$(7,1)
     9    $ Sales Month-to-Date                    9    CN ######.00
    10    $ Sales Year-to-Date                     8    DN ########
    11    Dollar Sales Last Year Total             9    EN #########
    12    Unit Sales - Month-to-date               7    Fn #######
    13    Unit Sales - Last Month                  7    Gn #######
    14    Unit Sales - YTD                         8    Hn ########
    15    Unit Sales - Last Yr                     8    In ########
    16    Retail $ - Month-to-date                 9    Jn ######.00
    17    Retail $ - Year-to-date                  9    Kn ######.00
    18    Retail $ - Last Year Total               9    Ln ######.00
FCSAXFC  -CSADF XREF BY CUSTOMER TYPE  ( 296 at start)
     1    KEY TYPE = "C"                           1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    " " + CUSTOMER TYPE                      3    An$(4,3)
     4    PROD CAT(1)+ ITEM(12)+REP(3)            14    An$(7,14)
FCSAXFT  -CSADF XREF BY TERRITORY  ( 297 at start)
     1    KEY TYPE = "T"                           1    An$(1,1)
     2    COMPANY CODE                             2    An$(2,2)
     3    TERRITORY (ROUTE) CODE                   2    An$(4,2)
     4    PROD CAT(1)+ ITEM(12) +REP(3)           16    An$(7,16)
FCCNVZpw -Product Warning Codes  ( 298 at start)
     1    Key Type = 'pw'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Warning Code                             2    An$(5,2)
     4    Description                             25    Bn$
     5    Warning Symbol                           1    Cn$
FCCNVZh  -PRODUCT SHAPE CODES  ( 307 at start)
     1    Key Type = 'fx'                          2    An$(1,2)
     2    COMPANY CODE                             2    An$(3,2)
     3    REASON CODE                              2    An$(5,2) ##
     4    DESCRIPTION                             30    Bn$
     5    AUTO PURGE?                              1    Cn$(1,1)
     6    (open)                                   9    Cn$(2,9)
FCRDCH   -Production Transaction History  ( 308 at start)
     1    Company Number                           2    An$(1,2)
     2    Warehouse Code                           4    An$(3,4)
     3    Production Date                          6    An$(7,6)
     4    Reference Number                         5    An$(13,5)
     5    Sequence                                 3    An$(18,3) ###
     6    Rec Type = "H"                           1    Bn$(1,1)
     7    Generated/Manual (G/M)                   1    Bn$(2,1)
     8    Init Entry Complete? (Y/N)               1    Bn$(3,1)
     9    Department Code                          2    Bn$(4,2)
    10    (open)                                   5    Bn$(6,5)
    11    Problem Code 1                           2    Cn$(1,2)
    12    Problem Code 2                           2    Cn$(3,2)
    13    Formula Code                             6    Dn$(1,6)
    14    Formula Code                             4    Dn$(7,4)
    15    (open)                                   1    En
    16    (open)                                   1    Fn
    17    (open)                                   1    Gn #
    18    Order Number                             6    Hn$
    19    (open)                                   1    In$
    20    (open)                                   1    Jn$
    21    Total Produced Weight                    9    Kn ######.00
    22    Total Labor Hours                        3    Ln ###
    23    No Of Produced Lots                      2    Mn ##
    24    Number Of Items                          3    Nn ###
    25    Total Consumed Weight                    9    On ######.00
    26    Total Units Produced                     7    Pn #######
    27    Lot Numbers Produced                    24    Qn$
    28    (open)                                   1    R(1) #
    29    (open)                                   1    R(2) #
    30    (open)                                   1    R(3) #
    31    (open)                                   1    R(4) #
    32    (open)                                   1    R(5) #
    33    Prod Pending File Key                   17    Sn$
    34    (open)                                   1    Tn$
FCRDCH   -Production Transaction History  ( 309 at start)
     1    Company Code                             2    An$(1,2)
     2    Item Code                                6    An$(3,6)
     3    Production Date                          6    Bn$
     4    (open)                                   1    Cn$
     5    (open)                                   1    Dn$
     6    Qty on Hand                              8    Q(1) #####.00
     7    Reorder Qty                              8    Q(2) #####.00
     8    Qty in Production                        8    Q(3) #####.00
     9    Qty on Sales Orders                      8    Q(4) #####.00
    10    (open)                                   1    Q(5) #
    11    (open)                                   1    Q(6) #
    12    (open)                                   1    Q(7) #
    13    (open)                                   1    Q(8) #
    14    (open)                                   1    Q(9) #
    15    Suggested Qty                            8    Q(10) #####.00
FCRDCH   -Production Transaction History  ( 310 at start)
     1    Key Type = 'fm'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Model Code                               2    An$(5,2)
     4    Description                             30    Bn$
     5    Calculation Method                       1    Cn$(1,1)
     6    (open)                                   9    Cn$(2,9)
     7    (open)                                   1    Dn$
     8    Percent +/-                              6    An ###.00
     9    No of Prior Years                        2    Bn ##
    10    Source - Code 1                          1    En$(1,1)
    11           - Code 2                          1    En$(2,1)
    12           - Code 3                          1    En$(3,1)
    13    (open)                                   7    En$(4,7)
    14    Source - Pct 1                           6    P(1) ###.00
    15           - Pct 2                           6    P(2) ###.00
    16           - Pct 3                           6    P(3) ###.00
FCCNVZsp -Sales Price Category File  ( 311 at start)
     1    Key Type = 'sp'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Description                             30    Bn$
     4    Formula to Use                          20    Cn$
FCRDCH   -Production Transaction History  ( 312 at start)
     1    Company Number                           2    An$(1,2)
     2    Warehouse Code                           4    An$(3,4)
     3    Production Date                          6    An$(7,6)
     4    Reference Number                         5    An$(13,5)
     5    Sequence                                 3    An$(18,3) ###
     6    Trans Type (P/C/H=Header)                1    Bn$(1,1)
     7    Source(M-Manual,g-Gen In Prod)           1    Bn$(2,1)
     8    (open)                                   1    Bn$(3,1)
     9    (open)                                   2    Bn$(4,2)
    10    Units                                    2    Bn$(6,2)
    11    Lot Ctl Flag                             1    Bn$(8,1)
    12    Mult Lots? (Y/N)                         1    Bn$(9,1)
    13    Item Type                                1    Bn$(10,1)
    14    (open)                                  15    Bn$(11,15)
    15    Inventory Key                           21    Cn$
    16    Formula Code                             9    Dn$
    17    Production Qty                           9    En ######.00
    18    Quantity (I/C Units)                     9    Fn ######.00
    19    Unit Cost                                9    Gn ######.00
    20    Sales Order Num.                         6    Hn$
    21    Item Description                        40    In$
    22    Lot Number (Or 'Mult')                   8    Jn$
    23    Expected Yield %                         4    Kn ##.0
    24    Expected Cost                            9    Ln ######.00
    25    Previous Committed                       6    Mn ###.00
    26    Unit Weight                              9    Nn ######.00
    27    Expected Quantity                        9    On ######.00
    28    (open)                                   1    Pn #
    29    String Of Lot Numbrs                    40    Qn$
    30    Lot Qty 1                                5    R(1) #####
    31    Lot Qty 2                                5    R(2) #####
    32    Lot Qty 3                                5    R(3) #####
    33    Lot Qty 4                                5    R(4) #####
    34    Lot Qty 5                                5    R(5) #####
    35    Prod Pending Key                        17    Sn$
    36    (open)                                   1    Tn$
FCICFS   -Inventory Sales Forecast File  ( 313 at start)
     1    Company Code                             2    An$(1,2)
     2    Item Code                                6    An$(3,6)
     3    Prior Yr  - 1                            9     #########
     4             -  2                            9     #########
     5             -  3                            9     #########
     6             -  4                            9     #########
     7             -  5                            9     #########
     8             -  6                            9     #########
     9             -  7                            9     #########
    10             -  8                            9     #########
    11             -  9                            9     #########
    12             - 10                            9     #########
    13             - 11                            9     #########
    14             - 12                            9     #########
    15    Curr Yr -  1                             9     #########
    16            -  2                             9     #########
    17            -  3                             9     #########
    18            -  4                             9     #########
    19            -  5                             9     #########
    20            -  6                             9     #########
    21            -  7                             9     #########
    22            -  8                             9     #########
    23            -  9                             9     #########
    24            - 10                             9     #########
    25            - 11                             9     #########
    26            - 12                             9     #########
    27    Next Yr -  1                             9     #########
    28            -  2                             9     #########
    29            -  3                             9     #########
    30            -  4                             9     #########
    31            -  5                             9     #########
    32            -  6                             9     #########
    33            -  7                             9     #########
    34            -  8                             9     #########
    35            -  9                             9     #########
    36            - 10                             9     #########
    37            - 11                             9     #########
    38            - 12                             9     #########
FCPDCR   -Production Cost Recap File  ( 314 at start)
     1    Company Code                             2    An$(1,2)
     2    W/H Code                                 4    An$(3,4)
     3    Production Date                          6    An$(7,6)
     4    Reference Number                         5    An$(13,5)
     5    Produced Units                           7     #######
     6    Produced Weight                          9     #########
     7    Gross Cost                               9     ######.00
     8    Consumed Weight                          8     #####.00
     9    Labor Hours                              5     ##.00
    10    Labor Rate                               6     ###.00
    11    Fringe %                                 5     ##.00
    12    Last FOB Cost                            6     ###.00
    13    Produced Item Code                       6
FCIFMS   -FORMULA MASTER FILE  ( 320 at start)
     1    Company Code                             2    An$(1,2)
     2    Formula Code                            10    An$(3,10)
     3    (Open)                                   2    An$(13,2)
     4    Revision Number                          3    An$(15,3)
     5    Key Group = "0"                          1    An$(18,1)
     6    Description                             40    Bn$
     7    Project Number                           6    Cn$
     8    Date Issued                              6    Dn$(1,6)
     9    Date Revised                             6    Dn$(7,6)
    10    Date Of Last Run                         6    Dn$(13,6)
    11    Date Put On Hold                         6    Dn$(19,6)
    12    Date Written                             6    Dn$(25,6)
    13    Approved By                              3    Dn$(31,3)
    14    Changed By                               3    Dn$(34,3)
    15    Change Approved By                       3    Dn$(37,3)
    16    Date to Retest                           6    Dn$(40,3)
    17    Last Sales Ord. #                        6    En$(1,6)
    18    Last Customer #                          6    En$(7,6)
    19    Department Code                          2    En$(13,2)
    20    Color                                   20    En$(15,20)
    21    Formulated By                            3    Fn$(1,3)
    22    Formula Type                             1    Fn$(4,1)
    23    Ok To Use?                               1    Fn$(5,1)
    24    Hold Reason                              2    Fn$(6,2)
    25    Change Reason Code                       2    Fn$(8,2)
    26    Test W. Milk?                            1    Fn$(10,1)
    27    Tablet Type                              3    Fn$(11,3)
    28    Normal Production Line                   2    Fn$(14,2)
    29    Serving Size Units                       2    Fn$(16,2)
    30    Bulk Item Code                           6    Fn$(18,6)
    31    (open)                                   2    Fn$(24,2)
    32    Production Units                         2    Fn$(26,2)
    33    Alpha Sort Key                           8    Fn$(28,8)
    34    Std Batch Sizes? (Y/N)                   1    Fn$(36,1)
    35    Tube Size                                2    Fn$(37,2)
    36    (open)                                   2    Fn$(39,2)
    37    Label Name                              40    Gn$
    38    Reference No.                           12    Hn$
    39    Previous Reference No.                  12    In$
    40    Comment Line 1                          65    Jn$
    41    Comment Line 2                          65    Kn$
    42    Serving Size                             3    An ###
    43    Expected Yield %                         5    Bn ###.0
    44    Hardness Range - Low                     2    Cn ##
    45    Hardness Range - High                    2    Dn ##
    46    Mos Shelf Life                           3    En ###
    47    (open)                                   1    Fn
    48    Largest Batch Size                       6    Gn ######
    49    Weight/10                                5    Hn ##.00
    50    (Open)                                   1    In #
    51    (Open)                                   1    Jn #
FCIFMSH  -FORMULA MASTER - HISTORICAL  ( 321 at start)
     1    Company Code                             2    An$(1,2)
     2    Formula Code                            10    An$(3,10)
     3    (Open)                                   2    An$(13,2)
     4    Revision Number                          3    An$(15,3)
     5    Key Group = "1"                          1    An$(18,1)
     6    Current Warning Code 1                   2    Bn$(1,2)
     7    Current Warning Code 2                   2    Bn$(2,2)
     8    (Open)                                   6    Bn$(4,6)
     9    Date Of Last Run                         6    Cn$(1,6)
    10    (Open)                                   6    Cn$(7,6)
    11    Last Run - Sales Order No.               6    Dn$(1,6)
    12    Last Run - 1st Lot Number                8    Dn$(7,8)
    13    Last Run - Problem Code 1                2    Dn$(15,2)
    14    Last Run - Problem Code 2                2    Dn$(17,2)
    15    (Open)                                   2    Dn$(19,2)
    16    (Open)                                   1    En$
    17    (Open)                                   1    Fn$
    18    (Open)                                   1    Gn$
    19    (Open)                                   1    Hn$
    20    (Open)                                   1    In$
    21    (Open)                                   1    Jn$
    22    (Open)                                   1    Kn$
    23    Last Run - Total Lbs                     6    An ######
    24    Last Run - Total Batches                 3    Bn ###
    25    Last Run - Productn Time (Hrs)           5    Cn #####
    26    Last Run - Yield %                       4    Dn ##.0
    27    All Runs - No Runs                       4    En ####
    28    All Runs - Total Lots                    4    Fn ####
    29    Total Produced Wt                        6    Gn ######
    30    All Runs - Problems                      4    Hn ####
    31    All Runs - Yield %                       4    In ##.0
    32    Total Consumed Wt                        6    Jn ######
FCIFDT   -FORMULA DETAIL - INGREDIENT DETAIL  ( 322 at start)
     1    Company Code                             2    An$(1,2)
     2    Formula Code                            10    An$(3,10)
     3    (Open)                                   2    An$(13,2)
     4    Revision Number                          3    An$(15,3)
     5    Key Group = "0"                          1    An$(18,1)
     6    Line Number                              3    An$(19,3)
     7    Ingredient Code - Batch 1                8    Bn$(1,8)
     8    Ingredient Code - Batch 2                8    Bn$(9,8)
     9    Ingredient Code - Batch 3                8    Bn$(17,8)
    10    Ingredient Code - Batch Temp             8    Bn$(25,8)
    11    Item Type - Batch 1                      1    Cn$(1,1)
    12    Item Type - Batch 2                      1    Cn$(2,1)
    13    Item Type - Batch 3                      1    Cn$(3,1)
    14    Item Type - Batch Temp                   1    Cn$(4,1)
    15    Units - Batch 1                          2    Dn$(1,2)
    16    Units - Batch 2                          2    Dn$(3,2)
    17    Units - Batch 3                          2    Dn$(5,2)
    18    Units - Batch Temp                       2    Dn$(7,2)
    19    (open)                                   1    En$
    20    Desc - Batch 1                          48    Fn$(1,48)
    21    Desc - Batch 2                          48    Fn$(49,48)
    22    Desc - Batch 3                          48    Fn$(97,40)
    23    Desc - Batch Temp                       40    Fn$(121,40
    24    Lbl Claim - Batch 1                      8    Gn$(1,8)
    25    Lbl Claim - Batch 2                      8    Gn$(9,8)
    26    Lbl Claim - Batch 3                      8    Gn$(17,8)
    27    Lbl Claim - Batch Temp                   8    Gn$(25,8)
    28    Pct Over - Batch 1                       2    Hn$(1,2) ##
    29    Pct Over - Batch 2                       2    Hn$(3,2)
    30    Pct Over - Batch 3                       2    Hn$(5,2)
    31    Pct Over - Batch Temp                    2    Hn$(7,2)
    32    Pct In Formula - Batch 1                 8    A(1) ###.00##
    33    Pct In Formula - Batch 2                 8    A(2) ###.00##
    34    Pct In Formula - Batch 3                 8    A(3) ###.00##
    35    Pct In Formula - Batch Temp              8    A(4) ###.00##
    36    Qty - Batch 1                           11    B(1) #######.00#
    37    Qty - Batch 2                           11    B(2) #######.00#
    38    Qty - Batch 3                           11    B(3) #######.00#
    39    Qty - Batch Temp                        11    B(4) #######.00#
    40    (open)                                   1    C(1)
    41    (open)                                   1    C(2)
    42    (open)                                   1    C(3)
    43    (open)                                   1    C(4)
FCIFDT1  -FORMULA DETAIL - PRODUCTION INFO  ( 323 at start)
     1    Company Code                             2    An$(1,2)
     2    Formula Code                            10    An$(3,10)
     3    (Open)                                   2    An$(13,2)
     4    Revision Number                          3    An$(15,3)
     5    Key Group = "1"                          1    An$(18,1)
     6    Batch Id                                 2    An$(19,2)
     7    Description                             40    Bn$
     8    Comments                                10    Cn$
     9    (Open)                                   1    Dn$
    10    (Open)                                   1    En$
    11    (open)                                   1    Fn$
    12    (open)                                   1    Gn$
    13    (open)                                   1    Hn$
    14    Gross Weight (Lbs)                       8    An #####.00
    15    Yield In Units                           8    Bn #####.00
    16    Yield %                                  5    Cn ##.00
    17    Labor Hours                              7    Dn ####.00
    18    (Open)                                   1    En #
    19    (Open)                                   1    Fn #
    20    (Open)                                   1    Gn #
    21    (Open)                                   1    Hn #
    22    (Open)                                   1    In #
    23    (Open)                                   1    Jn #
    24    (Open)                                   1    Kn #
    25    (Open)                                   1    Ln #
    26    (Open)                                   1    Mn #
    27    (Open)                                   1    Nn #
    28    (Open)                                   1    On #
    29    (Open)                                   1    Pn #
FCIFTX   -FORMULA DETAIL - BATCHING DIRECTIONS  ( 324 at start)
     1    Company Code                             2    An$(1,2)
     2    Formula Code                            10    An$(3,10)
     3    (Open)                                   2    An$(13,2)
     4    Revision Number                          3    An$(15,3)
     5    Batch Id                                 2    An$(18,2)
     6    Line Number                              2    An$(20,2)
     7    Step                                     5    Bn$
     8    Text                                    50    Cn$
     9    Link To Formula Master                   1    Dn$
FCIFMFH  -MASTER FORMULA HEADER FILE  ( 325 at start)
     1    Company Code                             2    An$(1,2)
     2    Master Formula Code                      6    An$(3,6)
     3    Header Seq = "000"                       3    An$(9,3)
     4    Formula Description                     30    Bn$
     5    (open)                                   1    Cn$
     6    (open)                                   1    Dn$
     7    (open)                                   1    An #
     8    (open)                                   1    Bn #
FCIFMFD  -MASTER FORMULA DETAIL FILE  ( 326 at start)
     1    Company Code                             2    An$(1,2)
     2    Master Formula                           6    An$(3,6)
     3    Sequence                                 3    An$(9,3) ###
     4    Formula Code                            10    Bn$
     5    (open)                                   1    Cn$
     6    (open)                                   1    Dn$
     7    (open)                                   1    An #
     8    (open)                                   1    Bn #
FCIFIW   -INGREDIENT USAGE BY FORMULA XREF FILE  ( 327 at start)
     1    Company Code                             2    An$(1,2)
     2    Item Code                                8    An$(3,8)
     3    Formula Code                            10    An$(10,10)
     4    Revision Number                          3    An$(21,3)
     5    Batch Num (01,02,03,99)                  2    An$(24,2)
     6    Line Number                              3    An$(26,3)
FCIFPP0  -SALES ORDER PRODUCTION PENDING - HEADER  ( 328 at start)
     1    Company Code                             2    An$(1,2)
     2    Order Number                             6    An$(3,6)
     3    Release No                               2    An$(9,2) ##
     4    Sequence No                              3    An$(11,3)
     5    Record Type = '0000'                     4    An$(14,4)
     6    Batch Id - A                             1    Bn$(1,1)
     7    Formula Type (P/L/T/X/V/K)               1    Bn$(2,1)
     8    Prod Order Printed? (Y/N)                1    Bn$(3,1)
     9    Packaging Order Printed (Y/N)            1    Bn$(4,1)
    10    Lot Numbers Assigned (Y/N)               1    Bn$(5,1)
    11    Batching Auto/Manual (A/M)               1    Bn$(6,1)
    12    Recommit Necessary (Y/N)                 1    Bn$(7,1)
    13    Produced (Y/N/P/X)                       1    Bn$(8,1)
    14    Type (S/M/X)                             1    Bn$(9,1)
    15    Spec Prod Changes (Y/N)                  1    Bn$(10,1)
    16    (open)                                   2    Bn$(11,2)
    17    Order Confirmed?                         1    Bn$(13,1)
    18    (open)                                   7    Bn$(14,7)
    19    Product Number                           8    Cn$(1,8)
    20    Label                                    6    Cn$(9,6)
    21    Pallets                                  4    Cn$(15,4)
    22    Formula Code                            10    Cn$(19,10)
    23    Formula Revision                         3    Cn$(29,3)
    24    Product Color                           18    Cn$(32,18)
    25    Tablet Type                              3    Cn$(50,3)
    26    Hardness Range                           8    Cn$(53,8)
    27    Thickness                               13    Cn$(61,13)
    28    Label Claim                              5    Cn$(74,5)
    29    Current Status                           2    Cn$(79,2)
    30    Requested Date                           6    Cn$(81,6)
    31    Addl S/O Refs                           24    Cn$(87,24)
    32    Label Name                              40    Cn$(111,40
    33    Serving Size Units                       2    Cn$(151,2)
    34    Bult Item Units                          2    Cn$(153,2)
    35    Fin.Goods Units                          2    Cn$(155,2)
    36    Department Code                          2    Cn$(157,2)
    37    Production Line                          2    Cn$(159,2)
    38    (open)                                   2    Cn$(161,2)
    39    Instruction Line 1                      55    Dn$
    40    Instruction Line 2                      55    En$
    41    Production Scheduled Date                6    Fn$(1,6)
    42    Date Lot No Assgnd                       6    Fn$(7,6)
    43    Production Date                          6    Fn$(13,6)
    44    Scheduled Date                           6    Fn$(19,6)
    45    Warning Codes                            4    Gn$
    46    Item Key (Inventory)                    21    Hn$
    47    Lot No Range 1                          16    In$
    48    Lot No Range 2                          16    Jn$
    49    Lot No Range 3                          16    Kn$
    50    Lot Nos Produced                        16    Ln$
    51    Units Ordered                            6    An ######
    52    Production Qty                           7    Bn #######
    53    Number Of Batches - A                    2    Cn ##
    54    Number Of Batches - B                    2    Dn ##
    55    Batch Weight - A                         6    En ######
    56    Batch Weight - B                         6    Fn ######
    57    Batch Size (Units) - A                   7    Gn #######
    58    Batch Size (Units) - B                   7    Hn #######
    59    Weight/10                                5    In ##.00
    60    (open)                                   1    Jn #
    61    F.G. Qty To Use                          6    Kn ######
    62    Units Produced                           8    Ln ########
    63    No Of Lots Produced                      4    Mn ####
    64    Qty On Order                             8    Nn ########
FCIFPP1  -SALES ORDER PRODUCTION PENDING - DETAIL  ( 329 at start)
     1    Company Code                             2    An$(1,2)
     2    Order Number                             6    An$(3,6)
     3    Release No                               2    An$(9,2) ##
     4    Sales Order Seq                          3    An$(11,3) ###
     5    Key Type = "1"                           1    An$(14,1)
     6    Formula Line No                          3    An$(15,3)
     7    Ingredient Code - Batch 1                8    Bn$(1,8)
     8    Ingredient Code - Batch 2                8    Bn$(9,8)
     9    Item Type - Batch 1                      1    Cn$(1,1)
    10    Item Type - Batch 2                      1    Cn$(2,1)
    11    (open)                                   2    Cn$(3,2)
    12    Units - Batch 1                          2    Dn$(1,2)
    13    Units - Batch 2                          2    Dn$(3,2)
    14    (open)                                   2    Dn$(5,2)
    15    (open)                                   2    Dn$(7,2)
    16    Description (Item Or Msg)               48    En$
    17    Label Claim                              7    Fn$
    18    % Over                                   2    Gn$
    19    (open)                                   1    Hn$
    20    Pct In Formula - Batch 1                 8    A(1) ###.00##
    21    Pct In Formula - Batch 2                 8    A(2) ###.00##
    22    (open)                                   1    A(3) #
    23    (open)                                   1    A(4) #
    24    Quantity - Batch 1                      11    B(1)
    25    Quantity - Batch 2                      11    B(2) #######.00#
    26    Qty Committed - Batch 1                 10    B(3) ######.00#
    27    Qty Committed - Batch 2                 10    B(4) ######.00#
    28    (open)                                   1    C(1) #
    29    (open)                                   1    C(2)
    30    WIP Qty - Batch 1                       10    C(3) ######.00#
    31    (open)                                        C(4)
FCIFRM   -RAW MATERIAL COMMITTED FILE  ( 330 at start)
     1    Company Code                             2    An$(1,2)
     2    Item Code                                8    An$(3,8)
     3    W/H Code                                 4    An$(11,4)
     4    Sequence                                 3    An$(15,3) ###
     5    Sales Order Number                       6    Bn$
     6    Date Committed                           6    Cn$
     7    Time Committed                           7    Dn$ ##.00##
     8    Reference                                4    En$
     9    Qty Committed                            9    An ######.00
FCIFTF   -INVENTORY FORMULA TRANSACTION FILE  ( 331 at start)
     1    TERMINAL CODE                            2    An$(1,2)
     2    FORMULA CODE                             6    An$(3,6)
     3    REVISION NUMBER                          3    An$(9,3)
     4    BATCH I.D.                               2    An$(12,2)
     5    LINE NUMBER                              3    An$(14,3)
     6    TOTAL %                                  5    An ##.00
     7    PROTEIN                                  7    Bn ##.00##
     8    FAT                                      7    Cn ##.00##
     9    ASH                                      7    Dn ##.00##
    10    MOISTR                                   7    En ##.00##
    11    CARBOHY                                  7    Fn ##.00##
    12    ITEM CODE                                8    Bn$
FCIFWF   -INVENTORY FORMULA WORK FILE  ( 332 at start)
     1    TERMINAL CODE                            2    An$(1,2)
     2    FORMULA CODE                             6    An$(3,6)
     3    REVISION NUMBER                          3    An$(9,3)
     4    BATCH I.D.                               2    An$(12,2)
     5    NUTRIENT CODE                            3    An$(14,3)
     6    PCT IN PRODUCT                           8    An ###.00##
     7    100% USRDA                               8    Bn ####.00#
     8    UNITS                                    2    Bn$
     9    % RDA LABEL                              4    Cn ####
    10    SOURCE INGREDIENT                        6    Cn$
    11    PCT                                      3    Dn ###
    12    WEIGHT (MG)                              3    En ###
    13    TOTAL % ALL                              8    Fn ###.00##
FCIFCC   -FORMULA COMPANY CONTROL RECORD  ( 333 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    CONTROL TYPE                             2    An$(2,2)
     3    (OPEN)                                   1    Bn$
     4    FACTOR MILK ONLY                         3    F(0) ###
     5    FACTOR MILK AND/OR OTHER                 3    F(1) ###
     6    CALORIES (VIT.MIN.) TO                   3    F(2) ###
     7    FROM                                     3    F(3) ###
     8    ROUND TO                                 2    F(4) ##
     9    TO                                       3    F(5) ###
    10    FROM                                     3    F(6) ###
    11    ROUND TO                                 2    F(7) ##
    12    TO                                       3    F(8) ###
    13    FROM                                     3    F(9) ###
    14    ROUND TO                                 2    F(10) ##
    15    TO                                       3    F(11) ###
    16    FROM                                     3    F(12) ###
    17    ROUND TO                                 2    F(13) ##
    18    CALORIES (AMINO) TO                      3    F(14) ###
    19    FROM                                     3    F(15) ###
    20    ROUND TO                                 2    F(16) ##
FCIFCC   -FORMULA COMPANY CONTROL RECORD  ( 334 at start)
     1    TERMINAL CODE                            2    An$(1,2)
     2    FORMULA CODE                             6    An$(3,6)
     3    REVISION NUMBER                          3    An$(9,3)
     4    LINE NUMBER                              2    An$(12,2)
     5    NUTRIENT CODE                            3    Bn$(1,3)
     6    NUTRIENT DESCRIPTION                    21    Bn$(4,21)
     7    DESIRED CLAIM                            2    Bn ##
     8    INGREDIENT CODE                          8    Cn$(1,8)
     9    INGREDIENT DESCRIPTION                  21    Cn$(9,21)
    10    PCT TO SATISFY                           3    Cn ###
    11    AMT.PER SERVING(MGS)                     9    Dn #####.00#
FCPDST   -MAKE TO STOCK PRODUCTION FILE  ( 335 at start)
     1    Company Code                             2    A$(1,2)
     2    Production Order No                      6    A$(3,6) ######
     3    Release number                           2    A$(9,2) ##
     4    Sequence No                              3    An$(11,3) ###
     5    Item Code                                6    Bn$(1,6)
     6    Company Code                             2    Bn$(7,2)
     7    Warehouse Code                           4    Bn$(9,4)
     8    (open)                                   4    Bn$(13,4)
     9    Company Code                             2    Bn$(17,2)
    10    (open)                                   3    Bn$(19,3)
    11    Formula Code                            10    Cn$(1,10)
    12    Formula Revision                         3    Cn$(11,3) ###
    13    Productn Order Status                    1    Cn$(14,1)
    14    Prodctn Detail Status                    2    Cn$(15,2)
    15    Priority Code(00-99)                     2    Cn$(17,2)
    16    Production Line                          2    Cn$(17,2)
    17    ...reserved for prod line exp            2    Cn$(21,2)
    18    Source Code(sp=manual,F=4cast)           1    Cn$(23,1)
    19    Department Code                          2    Cn$(24,2)
    20    (open)                                   5    Cn$(26,5)
    21    Date Entered                             6    Dn$(1,6) ######
    22    Scheduled Start Date                     6    Dn$(7,6)
    23    Scheduled Finish Date                    6    Dn$(13,6)
    24    Date Last Changed                        6    Dn$(19,6)
    25    (open)                                  12    Dn$(25,12)
    26    Unit of Measure                          2    En$(1,2)
    27    Days in Production                       2    En$(3,2) ##
    28    (open)                                   6    En$(5,6)
    29    Comments                                 1    Fn$
    30    Production Qty                           8    An ########
    31    Number of Batches                        2    Bn ##
    32    Batch Size                               6    Cn ######
    33    Production Lbs                           6    Dn ######
FCPDLH   -PRODUCTION HISTORY BY LOT FILE  ( 336 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    LOT NUMBER                               8    An$(3,8)
     3    RAW MATERIAL CODE                        8    An$(11,8)
     4    RAW MATERIAL WHSE CODE                   4    An$(19,4)
     5    FINISHED GOOD CODE                       8    An$(23,8)
     6    FIN. ITEM WHSE                           4    An$(31,4)
     7    DATE                                     6    An$(35,6)
     8    SEQUENCE #                               3    An$(41,3)
     9    FORMULA CODE                            10    Bn$(1,10)
    10    FORMULA REVISION                         3    Bn$(11,3)
    11    UNITS                                    2    Bn$(14,2)
    12    (open)                                   9    Bn$(12,9)
    13    QUANTITY USED                           11    Cn ######.00##
    14    (open)                                  11    Dn
FCPDMP   -PRODUCTION ORDER MASTER  ( 337 at start)
     1    Company Code                             2    An$(1,2)
     2    Formula Code                             6    An$(3,6)
     3    (open)                                   6    An$(9,6)
     4    Revision Number                          3    An$(15,3)
     5    (open)                                   1    Bn$ #
     6    Number Of Production Units               7    Bn #######
FCCNVZh  -PRODUCT SHAPE CODES  ( 338 at start)
     1    Key Type = "h"                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Department Code                          2    An$(4,2)
     4    Description                             30    Bn$
     5    Update Usage? (Y/N)                      1    Cn$(1,1)
     6    (open)                                   4    Cn$(2,4)
     7    Labor Rate/Hour                          5    An ##.00
     8    Fringe Benefits %                        6    Bn ######
     9    # Employees                              5    Cn ###.0
    10    Fixed Overhead/Day                       8    Dn #####.00
    11    Var Overhead/Day                         8    En #####.00
    12    MTD - LBS Produced                       8    M(1) ########
    13        - Labor HRS                          7    M(2) ####.00
    14        - Labor COST                         8    M(3) #####.00
    15    (open)                                   1    M(4)
    16    (open)                                   1    M(5)
    17    YTD - LBS Produced                      10    Y(1)
    18        - Labor HRS                          8    Y(2) #####.00
    19        - Labor Cost                        10    Y(3) #######.00
    20    (open)                                   1    Y(4)
    21    (open)                                   1    Y(5)
FCCNVZ<  -FORMULA REVISION REASON CODE MASTER FILE  ( 339 at start)
     1    Key Group = "RF"                         2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Reason Code                              3    An$(5,3)
     4    Reason Description                      30    Bn$
     5    (open)                                   1    Cn$
     6    (open)                                   1    Dn$
FCCNVZ=  -SAFETY/HAZARD/WARNING CODE MASTER FILE  ( 340 at start)
     1    Key Type = 'RS'                          2    An$(1,2)
     2    Company Code                             2    An$(3,2)
     3    Warning Code                             2    An$(5,2)
     4    Description                             30    Bn$
     5    SHORT DESCRIPTION                       15    Cn$
     6    (OPEN)                                  10    Dn$
FCCNVZf  -PRODUCTION LINE MASTER FILE  ( 341 at start)
     1    KEY GROUP = "f"                          1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Production Line Code                     2    An$(4,2)
     4    Description                             30    Bn$
     5    Short Description                        6    Cn$
     6    Cost per Hour                            6    An ###.00
     7    Standard Performance per Hour            8    Bn #####.00
     8    Normal Hours per Day                     2    Gn ##
     9    Vendor Number                            6    Hn$
    10    (open)                                   1    In$
FCRDCTH  -PRODUCTION TRANSACTION HEADER  ( 342 at start)
     1    Company Number                           2    An$(1,2)
     2    Warehouse Code                           4    An$(3,4)
     3    Production Date                          6    An$(7,6)
     4    Reference Number                         5    An$(13,5)
     5    Sequence                                 3    An$(18,3) ###
     6    Rec Type = "H"                           1    Bn$(1,1)
     7    Generated/Manual (G/M)                   1    Bn$(2,1)
     8    Init Entry Complete? (Y/N)               1    Bn$(3,1)
     9    Department Code                          2    Bn$(4,2)
    10    (open)                                   5    Bn$(6,5)
    11    Problem Code 1                           2    Cn$(1,2)
    12    Problem Code 2                           2    Cn$(3,2)
    13    Formula Code                            10    Dn$
    14    (open)                                   1    En
    15    (open)                                   1    Fn
    16    (open)                                   1    Gn #
    17    Order Number                             6    Hn$
    18    (open)                                   1    In$
    19    (open)                                   1    Jn$
    20    Total Produced Weight                    9    Kn ######.00
    21    Total Labor Hours                        3    Ln ###
    22    No Of Produced Lots                      2    Mn ##
    23    Number Of Items                          3    Nn ###
    24    Total Consumed Weight                    9    On ######.00
    25    Total Units Produced                     7    Pn #######
    26    Lot Numbers Produced                    24    Qn$
    27    (open)                                   1    R(1) #
    28    (open)                                   1    R(2) #
    29    (open)                                   1    R(3) #
    30    (open)                                   1    R(4) #
    31    (open)                                   1    R(5) #
    32    Prod Pending File Key                   17    Sn$
    33    (open)                                   1    Tn$
FCRDCTD  -PRODUCTION TRANSACTION DETAILS  ( 343 at start)
     1    Company Number                           2    An$(1,2)
     2    Warehouse Code                           4    An$(3,4)
     3    Production Date                          6    An$(7,6)
     4    Reference Number                         5    An$(13,5)
     5    Sequence                                 3    An$(18,3) ###
     6    Trans Type (P/C/H=Header)                1    Bn$(1,1)
     7    Source(M-Manual,g-Gen In Prod)           1    Bn$(2,1)
     8    (open)                                   1    Bn$(3,1)
     9    (open)                                   2    Bn$(4,2)
    10    Units                                    2    Bn$(6,2)
    11    Lot Ctl Flag                             1    Bn$(8,1)
    12    Mult Lots? (Y/N)                         1    Bn$(9,1)
    13    Item Type                                1    Bn$(10,1)
    14    (open)                                  15    Bn$(11,15)
    15    Inventory Key                           21    Cn$
    16    Formula Code                             9    Dn$
    17    Production Qty                           9    En ######.00
    18    Quantity (I/C Units)                     9    Fn ######.00
    19    Unit Cost                                9    Gn ######.00
    20    Sales Order Num.                         6    Hn$
    21    Item Description                        40    In$
    22    Lot Number (Or 'Mult')                   8    Jn$
    23    Expected Yield %                         4    Kn ##.0
    24    Expected Cost                            9    Ln ######.00
    25    Previous Committed                       6    Mn ###.00
    26    Unit Weight                              9    Nn ######.00
    27    Expected Quantity                        9    On ######.00
    28    (open)                                   1    Pn #
    29    String Of Lot Numbrs                    40    Qn$
    30    Lot Qty 1                                5    R(1) #####
    31    Lot Qty 2                                5    R(2) #####
    32    Lot Qty 3                                5    R(3) #####
    33    Lot Qty 4                                5    R(4) #####
    34    Lot Qty 5                                5    R(5) #####
    35    Prod Pending Key                        17    Sn$
    36    (open)                                   1    Tn$
FCCNVZ'  -PRODUCTION SYSTEM CONTROL RECORD  ( 344 at start)
     1    Key Type = "C"                           1    An$(1,1)
     2    Application Code                         2    An$(2,2)
     3    Company Code                             2    An$(4,2)
     4    Check F.G. Stock?                        1    Bn$(1,1)
     5    (open)                                   9    Bn$(2,9)
     6    Formula Costing Flag                     1    Cn$(1,1)
     7    Desc Change Password                     3    Cn$(2,3)
     8    Formula Costing Price Lists              6    Cn$(5,6)
     9    WIP Warehouse                            4    Dn$
    10    Max Number of Batches                    4    An ####
    11    Cost Markup Pct                          6    Bn ###.00
    12    Open                                     1    Cn #
FCCNVZm  -WORK-IN-PROGRESS STATUS CODES  ( 345 at start)
     1    Key Type = "m"                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Status Code                              2    An$(4,2)
     4    Description                             30    Bn$
     5    (open)                                   1    Cn$
FCFPLB   -PACKAGE LABEL TEXT FILE  ( 346 at start)
     1    Company Code                             2    An$(1,2)
     2    Package Type (N)                         1    An$(3,1)
     3    Item Code                                6    An$(4,6)
     4    (open)                                   2    An$(10,2)
     5    (open)                                   4    An$(12,4)
     6    Countries of Origin 1                   45    Bn$
     7    Countries of Origin 2                   45    Cn$
     8    Countries of Origin 3                   45    Dn$
     9    Text Line 4                             45    En$
    10    Text Line 5                             45    Fn$
    11    Text Line 6                             45    Gn$
    12    Nutritional Label                       45    Hn$
    13    Serving Size                            10    In$
    14    Servings/Container                      20    Jn$
    15    Household Measure                       25    Kn$
    16    (open)                                  10    Ln$
FCIFMX   -FORMULA ALPHA XREF FILE  ( 347 at start)
     1    Company Code                             2    An$(1,2)
     2    Alpha Sort Key                           8    An$(3,8)
     3    Formula Code                            10    An$(11,10)
     4    (open)                                   2    An$(21,2)
     5    Formula Revision                         3    An$(23,3)
     6    (open)                                   1    An$(26,1)
FCICTRR  -Production Trend File  ( 348 at start)
     1    Key Type = 'R'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Department Code                          2    An$(4,2)
     4    Item Code                                6    An$(6,6)
     5    Year                                     2    An$(12,2)
     6    Production - Period 01                   9    A(1) ######.00
     7               - Period 02                   9    A(2) ######.00
     8               - Period 03                   9    A(3) ######.00
     9               - Period 04                   9    A(4) ######.00
    10               - Period 05                   9    A(5) ######.00
    11               - Period 06                   9    A(6) ######.00
    12               - Period 07                   9    A(7) ######.00
    13               - Period 08                   9    A(8) ######.00
    14               - Period 09                   9    A(9) ######.00
    15               - Period 10                   9    A(10) ######.00
    16               - Period 11                   9    A(11) ######.00
    17               - Period 12                   9    A(12) ######.00
FCICTRU  -INGREDIENT USAGE TREND FILE  ( 349 at start)
     1    Key Type = 'U'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Item Code                                6    An$(4,6)
     4    Year                                     2    An$(10,2)
     5    Usage - Period 01                        9    A(1) ######.00
     6          - Period 02                        9    A(2) ######.00
     7          - Period 03                        9    A(3) ######.00
     8          - Period 04                        9    A(4) ######.00
     9          - Period 05                        9    A(5) ######.00
    10          - Period 06                        9    A(6) ######.00
    11          - Period 07                        9    A(7) ######.00
    12          - Period 08                        9    A(8) ######.00
    13          - Period 09                        9    A(9) ######.00
    14          - Period 10                        9    A(10) ######.00
    15          - Period 11                        9    A(11) ######.00
    16          - Period 12                        9    A(12) ######.00
FCRDEH2  -Order History File Header Record 2  ( 350 at start)
     1    COMPANY CODE                             2    An$(1,2)
     2    ORDER NO.                                6    An$(3,6)
     3    RELEASE NO.                              2    An$(9,2)
     4    TYPE = "0001"                            4    An$(11,4)
     5    (OPEN)                                   1    An
     6    (OPEN)                                   1    Bn
     7    (OPEN)                                   1    Bn$
     8    (OPEN)                                   1    Cn$
     9    (OPEN)                                   1    Dn$
    10    (OPEN)                                   1    En$
    11    (OPEN)                                   1    Fn$
    12    SHIP-TO NAME                            30    Gn$
    13    ADDRESS 1                               30    Hn$
    14    ADDRESS 2                               30    In$
    15    ADDRESS 3                               30    Jn$
    16    (OPEN)                                   1    Kn$
    17    (OPEN)                                   1    Ln$
    18    (OPEN)                                   1    Mn$
    19    (OPEN)                                   1    Nn$
    20    (OPEN)                                   1    On$
    21    (OPEN)                                   1    Pn$
    22    (OPEN)                                   1    Qn$
    23    (OPEN)                                   1    Rn$
    24    (OPEN)                                   1    S(0)
    25    (OPEN)                                   1    S(1)
    26    (OPEN)                                   1    S(2)
    27    (OPEN)                                   1    S(3)
    28    (OPEN)                                   1    S(4)
    29    (OPEN)                                   1    S(5)
    30    (OPEN)                                   1    S(6)
    31    (OPEN)                                   1    S(7)
    32    (OPEN)                                   1    S(8)
    33    (OPEN)                                   1    S(9)
    34    (OPEN)                                   1    S(10)
    35    (OPEN)                                   1    Tn$
    36    (OPEN)                                   1    Un$
    37    (OPEN)                                   1    Vn$
    38    (OPEN)                                   1    Wn$
    39    (OPEN)                                   1    Xn$
    40    (OPEN)                                   1    Yn$
    41    (OPEN)                                   1    Zn$
FCPOBF   -Supplier Broker File  ( 351 at start)
     1    Company Code                             2    An$(1,2)
     2    Broker Code                              6    An$(3,6)
     3    Broker Name                             30    Bn$
     4    Broker Address 1                        30    Cn$
     5    Broker Address 2                        30    Dn$
     6    Broker Address 3                        30    En$
     7    Telephone Number                        10    Fn$
     8    Fax Number                              10    Gn$
     9    Email Address                           40    Hn$
    10    Contact Name                            30    In$
    11    Contact Telephone                       10    Jn$
    12    Contact Cell                            10    Kn$
    13    Contact Email                           40    Ln$
    14    Supplier Number                          6    Mn$
FCICTRA  -  ( 358 at start)
     1    Key Type = 'A'                           1    An$(1,1)
     2    Company Code                             2    An$(2,2)
     3    Item Code                                6    An$(4,6)
     4    Year                                     2    An$(10,2)
     5    Usage - Period 01                        9    A(1) ######.00
     6          - Period 02                        9    A(2) ######.00
     7          - Period 03                        9    A(3) ######.00
     8          - Period 04                        9    A(4) ######.00
     9          - Period 05                        9    A(5) ######.00
    10          - Period 06                        9    A(6) ######.00
    11          - Period 07                        9    A(7) ######.00
    12          - Period 08                        9    A(8) ######.00
    13          - Period 09                        9    A(9) ######.00
    14          - Period 10                        9    A(10) ######.00
    15          - Period 11                        9    A(11) ######.00
    16          - Period 12                        9    A(12) ######.00
FCICTRA  -  ( 359 at start)
     1    Company Code                             2    An$(2,2)
     2    Item Code                                6    An$(4,6)
     3    Year                                     2    An$(10,2)
     4    LBS - Per 01                             7    A(1) #######
     5        - Per 02                             7    A(2) #######
     6        - Per 03                             7    A(3) #######
     7        - Per 04                             7    A(4) #######
     8        - Per 05                             7    A(5) #######
     9        - Per 06                             7    A(6) #######
    10        - Per 07                             7    A(7) #######
    11        - Per 08                             7    A(8) #######
    12        - Per 09                             7    A(9) #######
    13        - Per 10                             7    A(10) #######
    14        - Per 11                             7    A(11) #######
    15        - Per 12                             7    A(12) #######
    16    HRS - Per 01                             6     ###.00
    17        - Per 02                             6     ###.00
    18        - Per 03                             6     ###.00
    19        - Per 04                             6     ###.00
    20        - Per 05                             6     ###.00
    21        - Per 06                             6     ###.00
    22        - Per 07                             6     ###.00
    23        - Per 08                             6     ###.00
    24        - Per 09                             6     ###.00
    25        - Per 10                             6     ###.00
    26        - Per 11                             6     ###.00
    27        - Per 12                             6     ###.00
    28    CST - Per 01                             8     ########
    29        - Per 02                             8     ########
    30        - Per 03                             8     ########
    31        - Per 04                             8     ########
    32        - Per 05                             8     ########
    33        - Per 06                             8     ########
    34        - Per 07                             8     ########
    35        - Per 08                             8     ########
    36        - Per 09                             8     ########
    37        - Per 10                             8     ########
    38        - Per 11                             8     ########
    39        - Per 12                             8     ########
FCRDEHH  -Order History Header File  ( 360 at start)
     1    Company Code                             2    AN$(1,2)
     2    Order No                                 6    An$(3,6)
     3    Release No                               2    AN$(9,2)
     4    TYPE = '0000'                            4    AN$(11,4)
     5    FWD PTR                                  5    AN #####
     6    INDEX                                    5    BN #####
     7    Customer No                              6    BN$
     8    Customer Name                           30    CN$
     9    Address 1                               30    DN$
    10    Address 2                               30    EN$
    11    Address 3                               30    FN$
    12    PICK START/END YYMMDDHHMM               20    GN$
    13    (OPEN)                                   1    HN$
    14    (OPEN)                                   1    IN$
    15    (OPEN)                                   1    JN$
    16    Booking Flag                             1    KN$(1,1)
    17    Confirmed Flag                           1    KN$(2,1)
    18    Ord Print Flag                           1    KN$(3,1)
    19    Invoice Flag                             1    KN$(4,1)
    20    CREDLIM FLAG                             1    KN$(5,1)
    21    Pick List Printed (Y/N)                  1    KN$(6,1)
    22    Customer Taxable Wholesale               1    Kn$(7,1)
    23    Add Back to Inventory                    1    Kn$(8,1)
    24    Hold Release Flag                        1    Kn$(9,1)
    25    Taxing Authority Code                    2    KN$(10,2)
    26    Ship-to Code                             4    Kn$(12,4)
    27    Sales Rep Code                           3    KN$(16,3)
    28    Order Source Code                        1    Kn$(19,1)
    29    Ppd/Collect                              1    Kn$(20,1)
    30    Terms Code                               1    KN$(21,1)
    31    ZIP CODE                                 9    KN$(22,9)
    32    Warehouse Code                           4    KN$(31,4)
    33    QTY EXCEEDED                             1    KN$(35,1)
    34    PRICING STATUS                           1    KN$(36,1)
    35    Entry Type                               1    KN$(37,1)
    36    Operator ID                              3    KN$(38,3)
    37    Route Code                               3    Kn$(41,3)
    38    Stop Code                                3    Kn$(44,3)
    39    Territory Code                           3    Kn$(47,3)
    40    Velocity Report (Y/N)                    1    Kn$(50,1)
    41    Pick Priority (1-9)                      1    Kn$(51,1)
    42    Cust Price Label Format                  1    Kn$(52,1)
    43    Released to Pick (Y/N/H) ?               1    Kn$(53,1)
    44    Pick Tags Printed (Y/N/P)                1    Kn$(54,1)
    45    Allocation Done (Y/H/P)                  1    Kn$(55,1)
    46    Price Tags Printed (Y/N/H)               1    Kn$(56,1)
    47    Price List & SRP List                    2    Kn$(57,2)
    48    Freight Zone for Pricing (0-9)           1    Kn$(59,1)
    49    Special Cust(CPP) Y/N                    1    Kn$(60,1)
    50    Editted (Y/N)                            1    Kn$(61,1)
    51    Linked (Y/N)                             1    Kn$(62,1)
    52    DM/CM Reason Code                        2    Kn$(63,2)
    53    OK to combine w/other orders             1    Kn$(65,1)
    54    Below Min Order (Y=Yes,sp=No)            1    Kn$(66,1)
    55    Promos elligible(sp=yes,N=No)            1    Kn$(67,1)
    56    (open)                                   2    Kn$(68,2)
    57    Update S/A?                              1    Kn$(70,1)
    58    Ordered By                               2    Kn$(71,2)
    59    Operator - Void                          3    Kn$(73,3)
    60    (open)                                   5    Kn$(76,5)
    61    (open)                                   3    Kn$(68,3)
    62    Customer P.O. No.                       10    Ln$
    63    Order Date                               6    MN$(1,6)
    64    Ship Date                                6    MN$(7,6)
    65    Invoice Date                             6    MN$(13,6)
    66    Date Confirmed                           6    MN$(19,6)
    67    Date Wanted                              6    MN$(25,6)
    68    ORD PRT MSG                              2    MN$(31,2)
    69    INV PRT MSG                              2    MN$(33,2)
    70    Pricing 'as of' Date                     6    Mn$(35,6)
    71    Cust Price Label Titles                 12    Nn$
    72    Delivery Instructions                   60    ON$
    73    Phone Number                            10    Pn$
    74    Terms Description                       20    QN$
    75    Off Invoice Disc %                       6    RN$ ###.00
    76    Number of Lines                          3    T(0) ###
    77    Tax Pct                                  5    T(1) ##.00
    78    Total Gross                             11    T(2) ########.00
    79    Total Discount                           9    T(3) ######.00
    80    Total Tax                                9    T(4) ######.00
    81    Total Misc Chgs                          9    T(5) ######.00
    82    Taxable Amt                              9    T(6) ######.00
    83    Net Order Amt                           11    T(7) ########.00
    84    Total Net Lbs                            9    T(8) ######.00
    85    Svc Chg Amt                              9    T(9) ######.00
    86    Total Cost                               9    T(10) ######.00
    87    Total Gross Lbs                          9    T(11) ####.00##
    88    Total Cases                             10    T(12) #######.00
    89    Total Eaches                             6    T(13) ######
    90    Spoilage                                 9    T(14) #####.00#
    91    Fuel Surcharge                           9    T(15) ######.00
    92    CATEGORIES                               5    TN$
    93    Total Cube                              10    UN$ #######.00
    94    Invoice Number                           6    VN$
    95    E.O.S. Discount %                        5    Wn$
    96    EOE Transmission No                      6    Xn$(1,6)
    97    EOE Confirmation No                      6    Xn$(7,6)
    98    Date Transmitted                         6    Xn$(13,6)
    99    Time Transmitted                         4    Xn$(19,4)
   100    No of Price Labels Princed               6    Yn$(1,6) ######
   101    Charge for price labels                  8    Yn$(7,8) #####.00
   102    Invoice Svc Chg %                        5    ZN$ ###.0
FCRDEHD  -Order History Detail File  ( 370 at start)
     1    Company Code                             2    AN$(1,2)
     2    Order Number                             6    AN$(3,6)
     3    Release NO.                              2    AN$(9,2)
     4    KEY TYPE = '1'                           1    AN$(11,1)
     5    Line No.                                 3    AN$(12,3)
     6    Forward Ptr                              5    AN #####
     7    Backward Ptr                             5    BN #####
     8    Sales Unit                               2    BN$(1,2)
     9    Pricing Unit                             2    BN$(3,2)
    10    Wholesale Taxable (Y/N)                  1    BN$(5,1)
    11    Sales Category                           2    BN$(6,2)
    12    Retail Price List Code                   1    BN$(8,1)
    13    Wholesale Price List Code                1    BN$(9,1)
    14    Special Price? (Y/N)                     1    BN$(10,1)
    15    Line Item Terms Code                     1    BN$(11,1)
    16    Allocated (Y/N)                          1    Bn$(12,1)
    17    Split Case Code                          1    Bn$(13,1)
    18    SALES CD                                 1    BN$(14,1)
    19    Reason Code - Price Override             2    BN$(15,2)
    20    ADDS TO TOTAL WT                         1    BN$(17,1)
    21    Entry Type (I/A/M)                       1    BN$(18,1)
    22    CONTRACT?                                1    BN$(19,1)
    23    CATCH WEIGHT?                            1    BN$(20,1)
    24    Warehouse Code                           4    BN$(21,4)
    25    Pick Except Reason                       2    Bn$(25,2)
    26    Alloc Except Reason                      1    BN$(27,1)
    27    BOX/CASE (B/C/SP)                        1    BN$(28,1)
    28    FREIGHT CLASS                            1    BN$(29,1)
    29    Item Type                                1    BN$(30,1)
    30    WHSE Category                            1    BN$(31,1)
    31    G/L Category                             1    BN$(32,1)
    32    Inventory Units                          2    BN$(33,2)
    33    Initials for pick exceptions             3    Bn$(35,3)
    34    Retail Taxable (Y/N) ?                   1    Bn$(38,1)
    35    Quantity Exceeded (Y/sp) ?               1    Bn$(39,1)
    36    Invty Availability Code                  1    Bn$(40,1)
    37    CA Redemption Code                       1    Bn$(41,2)
    38    Reason Code - Credit Request             2    Bn$(42,2)
    39    Invoice Ref - Credit Request             8    Bn$(44,8)
    40    Commissionable (Y/N)                     1    Bn$(52,1)
    41    Update S/A (Y or sp=yes,N=no)            1    Bn$(53,1)
    42    Retail Price Overrive(V=yes)             1    Bn$(54,1)
    43    Cred Req Invoice Date                    6    Bn$(55,6)
    44    Cred Req Override(Y/sp)                  1    Bn$(61,1)
    45    Cred Req Disposition Code                2    Bn$(62,2)
    46    (open)                                   3    Bn$(64,3)
    47    Organic? (Y/N)                           1    Bn$(67,1)
    48    (open)                                  13    Bn$(68,13)
    49    Description                             48    Cn$
    50    Item Key                                21    DN$
    51    Item Code                                6    EN$
    52    UPC Code                                10    FN$
    53    ORD PRT MSG                              2    GN$(1,2)
    54    INV PRT MSG                              2    GN$(3,2)
    55    G/L ACCT #                              11    HN$
    56    LOT NUMBER                               8    IN$
    57    Location Codes                          12    Jn$
    58    Contract Number                         12    Kn$
    59    Original Alloc Quantity                  1    LN$
    60    (OPEN)                                   1    MN$
    61    (OPEN)                                   1    NN$
    62    Retail Sub-Pack                          6    ON$ ###.00
    63    PACK                                     4    PN$
    64    NET UNIT WEIGHT                          9    QN$
    65    (OPEN)                                   1    RN$
    66    Qty Ordered                             10    S(0) #######.00
    67    Qty Shipped                             10    S(1) #######.00
    68    P/A Per Unit                             9    S(2) ######.00
    69    QUANTITY INVOICED                       10    S(3) #######.00
    70    CATCH WGT OR UNIT CONV FACTOR           10    S(4) #####.00##
    71    Unit Price                              10    S(5) #####.00##
    72    GROSS UNIT WGT                           6    S(6) ###.00
    73    Extension                               10    S(7) #######.00
    74    DISCOUNT %                               5    S(8) ##.00
    75    TAX %                                    8    S(9) #####.00
    76    Unit Cost                                9    S(10) ####.00##
    77    Quantity Committed Updated               6    S(11) ######
    78    Quantity on-hand Updated                 6    S(12) ######
    79    Sugggested Retail Price                  9    S(13) ######.00
    80    Total P/A %                              6    S(14) ###.00
    81    Quantity Allocated                       1    S(15) #
    82    Bill Back Pct                            6    Tn$
    83    P/A Percents                            16    Un$
    84    Invoice P/A Desc                         5    VN$
    85    Unit Cube                                6    WN$ ###.00
    86    (OPEN)                                   1    XN$
    87    (OPEN)                                   1    YN$
    88    OPEN                                     1    Z$
""".split("\n")
