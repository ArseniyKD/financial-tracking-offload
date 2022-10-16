from gsheetInterface import GSheetBackendInterface, TestBackendInterface
from coreLogic import CoreLogic
from pprint import pprint

def main():
    sheetId = input()
    verbose = True

    oldSheetsDir = input()

    gsheetIntf = GSheetBackendInterface( sheetId, verbose )
    coreLogic = CoreLogic( gsheetIntf, verbose )
    gsheetIntf.authenticate()

    
    data = [
        [ 'Craft Cafe', '40', '5/10/2022', 'Retail', 'ws', '"V60" finally' ],
        [ 'Safeway', '20.12', '6/10/2022', 'Grocery', '', '' ]
    ]
    dataRange = 'BrainstormingTheDefaultValues!A:F'
    sheetName = 'BrainstormingTheDefaultValues'
    valueRange = 'A:F'
    """
    coreLogic.addTransactions( data, sheetName, valueRange )

    res = coreLogic.readSummaryInfo( sheetName )
    for val in res:
        print( *val )
    """
    tabs = coreLogic.getTabs()
    pprint( tabs )

    #newTabName = "January23February23"
    #coreLogic.createNewMonthSheet( newTabName )
    

    # coreLogic.migrateOldSheets( oldSheetsDir )

if __name__ == '__main__':
    main()
