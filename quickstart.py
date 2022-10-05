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

    readRange1 = 'BrainstormingTheDefaultValues!H3:I13'
    readRange2 = 'BrainstormingTheDefaultValues!H16:I22'
    res = gsheetIntf.batchRead( [ readRange1, readRange2 ] )
    for i, vals in enumerate( res ):
        for val in vals[ 'values' ]:
            print( *val )

    newTabName = "December22January23"
    coreLogic.createNewMonthSheet( newTabName )

if __name__ == '__main__':
    main()
