import os.path
import sys

import defaultValues

class BaseCoreLogic( object ):
    def __init__( self ):
        pass

    def addTransactions( self, transactions, currentMonthTab, valueRange ):
        pass

    def migrateOldSheets( self, oldSheetsDir ):
        pass

    def createNewMonthSheet( self, newMonthTabName, populateDefault=True ):
        pass

    def readSummaryInfo( self, currentMonthTab ):
        pass

class TestCoreLogic( BaseCoreLogic ):
    backendInterface = None

    def __init__( self, backendIntf, verbose ):
        print( "Mock Core Logic: Constructor called" )

    def addTransactions( self, transactions, currentMonthTab, valueRange ):
        print( "Mock Core Logic: Add transaction called with these arguments" )
        print( f"\tTXs: {transactions}\n\tTab: {currentMonthTab}\n\tRange: {valueRange}" )

    def migrateOldSheets( self, oldSheetsDir ):
        print( f"Mock Core Logic: Sheet Migration called wtih {oldSheetsDir}" )

    def createNewMonthSheet( self, newMonthTabName, populateDefault=True ):
        print( f"Mock Core Logic: New Month Sheet called: {newMonthTabName} {populateDefault}" )

    def readSummaryInfo( self, currentMonthTab ):
        print( f"Mock Core Logic: Read Summary Info called: {currentMonthTab}" )
        return [ [ 'Grocery', '123.4', 'Bills', '200.52' ], [ [ 'fm', '300', 'total', '2000' ] ]

class CoreLogic( BaseCoreLogic ):
    # This is the actual core logic with all the APIs that are currently supported
    # The base class shows all the functions that exist, and the mock object
    # is used for test purposes.
    backendInterface = None
    verbose = False

    def __init__( self, backendIntf, verbose ):
        self.backendInterface = backendIntf
        # Do this just in case.
        self.backendInterface.authenticate()
        self.verbose = verbose

    def addTransactions( self, transactions, currentMonthTab, valueRange ):
        # This function takes in the list of transactions, the tab to which to
        # write, and the range to which to write to. The list of transactions is
        # a list of lists of strings. The strings themselves will not be validated,
        # but the list of transactions will be to make sure that all the
        # transactions are the same length and the transaction fits in the provided
        # range length.

        # First, get the width of the row from the value range for consistency
        # checks.
        rowLen = -1
        if valueRange != "":
            # Assumption: value ranges are in the form of Xx:Yy with X, Y as
            # alpha, and x, y as numeric and we never go into AA columns.
            start, end = valueRange.split( ":" )
            rowLen = ord( end[ 0 ] ) - ord( start[ 0 ] ) + 1
            if rowLen <= 0:
                print( "ERROR: the row length provided is 0 or less, bail" )
                sys.exit( 1 )

        rangeStr = f"{currentMonthTab}!{valueRange}"

        # Validate the transactions list
        transactionLen = -1
        for i, transaction in enumerate( transactions ):
            currTxLen = len( transaction )
            if transactionLen == -1:
                transactionLen = currTxLen
            if transactionLen != currTxLen:
                print( f"ERROR: the transaction in list of transactions with index {i} has a different size {currTxLen} to the other checked transactions {transactionLen}, bail" )
                print( f"TX: {transaction}" )
                print( f"Look at this: {transactions}" )
                sys.exit( 1 )
            if rowLen != -1 and rowLen != transactionLen:
                print( f"ERROR: the transaction with size {transactionLen} does not fit in value range {valueRange} of size {rowLen}, bail" )
                sys.exit( 1 )

        return self.backendInterface.append( rangeStr, transactions )

    def migrateOldSheets( self, oldSheetsDir ):
        # This method migrates all the sheets saved as csv files in the provided
        # directory. The expected layout of the files in the directory is as
        # follows:
        #    XX_{Month}{YY}{Month+1}{YY}.csv
        # XX is just an incremented two digit id for the csv as for the initial
        # deployment I had 19 months worth of financial data to migrate off of
        # excel.
        # I got the csvs by importing the excel spreadsheet into google sheets,
        # and then downloaded each individual tab one by one and renamed them to
        # be in the format I mentioned above.
        # ---
        # Anyway, onto the implementation of this method. Here are the steps:
        #    1. Get the files in the provided folder
        #    2. Sort the list of files
        #    3. Strip the XX and the ".csv", that will be the new sheet name.
        #    4. Read the file start to finish and populate the list of strings
        #       that is basically created by `.split( "," )`ing the read line.
        #    5. Take all the lists, create the new sheet, and append the lists
        #       to the new lists.
        #    6. Repeat steps [3, 5] until no more files are left.
        # At this point, all the sheets should be migrated safely.
        
        if not os.path.exists( oldSheetsDir ):
            print( f"ERROR: Provided path {oldSheetsDir} does not exist, bail." )
            sys.exit( 1 )

        filesInOldSheetsDir = sorted( os.listdir( oldSheetsDir ) )

        for file in filesInOldSheetsDir:
            newSheetName = file.split( "_" )[ 1 ].split( "." )[ 0 ]
            lines = None
            with open( f"{oldSheetsDir}/{file}", "r" ) as fp:
                lines = fp.readlines()
            dataToMigrate = []
            for line in lines:
                # Need to iterate over all the elements and strip them, as
                # otherwise the newlines at the end of the csv line (and other
                # erroneous characters) cause issues in the spreadsheet.
                dataToMigrate.append(
                    [ element.strip() for element in line.split( "," ) ] )
            self.createNewMonthSheet( newSheetName, populateDefault=False )

            # Need to get the range end, as the blind writing without a range
            # was causing the API to return a 400 due to incorrect range format.
            rangeEnd = chr( ord( 'A' ) + len( dataToMigrate[ 0 ] ) - 1 )
            self.addTransactions( dataToMigrate, newSheetName, f"A:{rangeEnd}" )

    def createNewMonthSheet( self, newMonthTabName, populateDefault=True ):
        self.backendInterface.createSheetTab( 0, newMonthTabName )
        if populateDefault:
            self.addTransactions( defaultValues.DEFAULT_NEW_MONTH_INFO,
                                  newMonthTabName, "A1:N22" )

    def readSummaryInfo( self, currentMonthTab ):
        readRanges = []
        readRanges.append( f"{currentMonthTab}!{defaultValues.DEFAULT_CATEGORY_SUMMARY_RANGE}" )
        readRanges.append( f"{currentMonthTab}!{defaultValues.DEFAULT_AGGREGATE_SUMMARY_RANGE}" )
        res = self.backendInterface.batchRead( readRanges )
        return [ vals[ 'values' ] for i, vals in enumerate( res ) ]
