from gsheetInterface import GSheetBackendInterface
from coreLogic import CoreLogic

def main():
    sheetId = input()
    verbose = True

    gsheetIntf = GSheetBackendInterface( sheetId, verbose )
    coreLogic = CoreLogic( gsheetIntf, verbose )
    gsheetIntf.authenticate()

    data = [
        [ 'Craft Cafe', '40', '5/10/2022', 'Retail', 'ws', '"V60", finally' ],
        [ 'Safeway', '20.12', '6/10/2022', 'Grocery', '', '' ]
    ]
    dataRange = 'BrainstormingTheDefaultValues!A:F'
    sheetName = 'BrainstormingTheDefaultValues'
    valueRange = 'A:F'
    coreLogic.addTransactions( data, sheetName, valueRange )
    # _ = gsheetIntf.append( dataRange, data )

    readRange1 = 'BrainstormingTheDefaultValues!H3:I13'
    readRange2 = 'BrainstormingTheDefaultValues!H16:I22'
    res = gsheetIntf.batchRead( [ readRange1, readRange2 ] )
    for i, vals in enumerate( res ):
        for val in vals[ 'values' ]:
            print( *val )

    # newTabId = 1
    newTabName = "December22January23"
    # sheetDefaultVals = [
    #     [ "Transactio Name", "Transaction Amount", "Transaction Date",
    #       "Transaction Category", "Budget Specifiers", "Transaction Note",
    #       "", "Aggregate", "", "", "FM Ceil", "Income", "Rents", "Spend" ],
    #     [ "" for _ in range( 10 ) ] + [ "1500", "", "1625", "=SUM(M2,K2,I20)" ],
    #     [ "" for _ in range( 7 ) ] + [ "Grocery",
    #                                    "=SUMIF($D$2:$D$200, H3, $B$2:$B$200)",
    #                                    "", "", "", "1550", "" ],
    #     [ "" for _ in range( 7 ) ] + [ "Bills",
    #                                    "=SUMIF($D$2:$D$200, H4, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Eating Out",
    #                                    "=SUMIF($D$2:$D$200, H5, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Retail",
    #                                    "=SUMIF($D$2:$D$200, H6, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Vices",
    #                                    "=SUMIF($D$2:$D$200, H7, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Health",
    #                                    "=SUMIF($D$2:$D$200, H8, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Subscriptions",
    #                                    "=SUMIF($D$2:$D$200, H9, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Transit",
    #                                    "=SUMIF($D$2:$D$200, H10, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Other",
    #                                    "=SUMIF($D$2:$D$200, H11, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Entertainment",
    #                                    "=SUMIF($D$2:$D$200, H12, $B$2:$B$200)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "Total",
    #                                    "=SUM(I2:I12)" ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 14 ) ],
    #     [ "" for _ in range( 14 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "fm + fmrent",
    #                                    '=SUMIF(E2:E200, "fm",B2:B200)+M3' ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "fm",
    #                                    '=I16-M3' ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "spend - fm",
    #                                    '=I13-I17' ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "ws",
    #                                    '=SUMIF(E2:E200, "ws",B2:B200)' ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "spend - fm - ws",
    #                                    '=I18-I19' ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "extra",
    #                                    '=SUMIF(E2:E200, "extra",B2:B200)' ] + \
    #                                  [ "" for _ in range( 5 ) ],
    #     [ "" for _ in range( 7 ) ] + [ "spend - fm - ws - extra",
    #                                    '=I20-I21' ] + \
    #                                  [ "" for _ in range( 5 ) ]
    # ]
    # gsheetIntf.createSheetTab( newTabId, newTabName )
    # gsheetIntf.append( f"{newTabName}!A1:N22", sheetDefaultVals )
    coreLogic.createNewMonthSheet( newTabName )

if __name__ == '__main__':
    main()
