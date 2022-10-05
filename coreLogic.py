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
                sys.exit( 1 )
            if rowLen != -1 and rowLen != transactionLen:
                print( f"ERROR: the transaction with size {transactionLen} does not fit in value range {valueRange} of size {rowLen}, bail" )
                sys.exit( 1 )

        return self.backendInterface.append( rangeStr, transactions )

    def migrateOldSheets( self, oldSheetsDir ):
        # Not implemented yet.
        pass

    def createNewMonthSheet( self, newMonthTabName, populateDefault=True ):
        self.backendInterface.createSheetTab( 0, newMonthTabName )
        if populateDefault:
            self.addTransactions( defaultValues.DEFAULT_NEW_MONTH_INFO,
                                  newMonthTabName, "A1:N22" )

    def readSummaryInfo( self, currentMonthTab ):
        # Not implemented yet
        pass 
