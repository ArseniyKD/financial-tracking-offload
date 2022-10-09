import os
import sys
from pprint import pprint
from tabulate import tabulate
import defaultValues

# No clue why this line is here, but adding it in case as it seems to be used
# in all the inquirer lib samples
sys.path.append( os.path.realpath( "." ) )
import inquirer # noqa

class CommandLineInterface( object ):
    coreLogic = None
    verbose = False

    topLevelMessage = ""
    topLevelChoices = []
    exitMessage = ""
    topLevelQ = ""
    specificCliFunctionMap = {}

    currentMonth = ""

    def __init__( self, coreLogic, verbose ):
        self.coreLogic = coreLogic
        self.verbose = verbose
        self.topLevelMessage = "Welcome to the Financial Tracking App! Main Menu"
        self.topLevelChoices.append("Add Transactions")
        self.topLevelChoices.append("See Summary")
        self.topLevelChoices.append("New Month")
        self.topLevelChoices.append("Change Current Month")
        self.topLevelChoices.append("Migrate Old Sheets")
        self.topLevelChoices.append("Exit")
        self.exitMessage = "Thank you for using the Financial Tracking App"
        self.topLevelQ = "topLevelQ"
        self.specificCliFunctionMap = {
            self.topLevelChoices[ 0 ]: self.addTransactions,
            self.topLevelChoices[ 1 ]: self.seeSummary,
            self.topLevelChoices[ 2 ]: self.newMonth,
            self.topLevelChoices[ 3 ]: self.changeCurrentMonth,
            self.topLevelChoices[ 4 ]: self.migrateOldSheets,
            self.topLevelChoices[ 5 ]: self.exitCli
        }
        self.currentMonth = "TestTab"

    def cliLoop( self ):
        questions = [
            inquirer.List( self.topLevelQ, message=self.topLevelMessage,
                           choices=self.topLevelChoices )
        ]
        while True:
            answers = inquirer.prompt( questions )
            if self.verbose:
                pprint( answers )
            if self.specificCliFunctionMap[ answers[ self.topLevelQ ] ]():
                break
        print( self.exitMessage )

    def transactionValidation( self, tx ):
        txList = tx.split( "," )
        if len( txList ) != 6:
            print( f"Transaction validation failed, {txList} is not of length 6" )
            return False
        if len( txList[ 0 ] ) == 0:
            print( f"Transaction validation failed for: {txList}, transaction name is empty" )
            return False
        if len( txList[ 1 ] ) == 0:
            print( f"Transaction validation failed for: {txList}, transaction amount is empty" )
            return False
        if len( txList[ 2 ] ) == 0:
            print( f"Transaction validation failed for: {txList}, transaction date is empty" )
            return False

        acceptedTransactionCategories = [
            "Grocery", "Bills", "Eating Out", "Retail", "Vices", "Health",
            "Subscriptions", "Transit", "Other", "Entertainment"
        ]
        acceptedBudgetSpecifiers = [ "fm", "ws", "extra", "" ]
        if txList[ 3 ].strip() not in acceptedTransactionCategories:
            print( f"Transaction Validation failed for: {txList}, transaction " + \
                    f"category {txList[3]} not in accepted transaction categories" )
            return False
        if txList[ 4 ].strip() not in acceptedBudgetSpecifiers:
            print( f"Transaction Validation failed for: {txList}, budget " + \
                    f"specifier {txList[4]} not in accepted transaction categories" )
            return False
        
        return True

    def printTransactionRequirements( self ):
        # Print the command usage:
        print( "Adding a transaction. Usage:" )
        print( "\tA comma separated list of six entries such as this: \"A,B,C,D,E,F\"" )
        print( "\t\tA: Transaction Name e.g.: Craft Cafe, not empty, no commas" )
        print( "\t\tB: Transaction Amount e.g.: 46.5, not empty, no commas" )
        print( "\t\tC: Transaction Date e.g.: 10/9/2022, not empty, no commas" )
        print( "\t\tD: Transaction Category e.g.: Retail, not empty, specific values" )
        print( "\t\tE: Budget Specifier e.g.: fm, may be empty, specific values" )
        print( "\t\tF: Transaction Note: e.g.: \"Finally got the V60\", may be empty, no commas" )
        print()
        print( "\tThe Category may be one of [ Grocery, Bills, Eating Out, " + \
                "Retail, Vices, Health, Subscriptions, Transit, Other, Entertainment ]" )
        print( "\tThe Budget Specifier may be one of [ fm, ws, extra ]" )
        print()
        print( "\tSample Final Transaction: Craft Cafe, 46.5, 10/9/2022, " + \
                "Retail, fm, Finally got the V60" )
        print()
        print( "Each transaction is verified individually, invalid transactions ignored" )

    def readOneTransaction( self ):
        singleTransactionTLQ = "oneTxTLQ"
        singleTransactionTLM = "Transaction:"
        questions = [
            inquirer.Text( singleTransactionTLQ, message=singleTransactionTLM )
        ]
        answers = inquirer.prompt( questions )
        if self.verbose:
            print( answers )
        return answers[ singleTransactionTLQ ]

    def addSingleTransaction( self ):
        if self.verbose:
            print( "Got to the Add Single Transaction submenu" )

        self.printTransactionRequirements()
        tx = self.readOneTransaction()
        if self.transactionValidation( tx ):
            self.coreLogic.addTransactions(
                [ tx.split( "," ) ], self.currentMonth,
                defaultValues.DEFAULT_TRANSACTION_RANGE )

    def batchTransactions( self ):
        if self.verbose:
            print( "Got to the batch transaction submenu" )
        
        self.printTransactionRequirements()
        
        batchTransactionsTLQ = "batchTLQ"
        batchTransactionsTLM = "Adding a batch of transactions. Options:"
        batchTransactionsTLC = [ "Add transaction to batch", "Done" ]

        questions = [
            inquirer.List( batchTransactionsTLQ, message=batchTransactionsTLM,
                           choices=batchTransactionsTLC )
        ]
        pendingTransactions = []
        while True:
            answers = inquirer.prompt( questions )
            if self.verbose:
                pprint( answers )
            if answers[ batchTransactionsTLQ ] == batchTransactionsTLC[ 1 ]:
                break
            tx = self.readOneTransaction()
            if self.transactionValidation( tx ):
                pendingTransactions.append( tx.split( "," ) )

        if pendingTransactions:
            if self.verbose:
                pprint( pendingTransactions )
            self.coreLogic.addTransactions(
                pendingTransactions, self.currentMonth,
                defaultValues.DEFAULT_TRANSACTION_RANGE )

    def addTransactions( self ):
        if self.verbose:
            print( "Got to add transactions" )

        addTransactionTLQ = "addTxTLQ"
        addTransactionTLM = "Add Transaction Functionality. Please select an option"
        addTransactionTLC = [ "Single Transaction", "Batch Transactions", "Back" ]
        questions = [
            inquirer.List( addTransactionTLQ, message=addTransactionTLM,
                           choices=addTransactionTLC )
        ]
        answers = inquirer.prompt( questions )
        if self.verbose:
            pprint( answers )
        if answers[ addTransactionTLQ ] == addTransactionTLC[ 0 ]:
            self.addSingleTransaction()
        if answers[ addTransactionTLQ ] == addTransactionTLC[ 1 ]:
            self.batchTransactions()
        # Should the Cli exit after this?
        return False

    def seeSummary( self ):
        if self.verbose:
            print( "Got to See Summary" )
        
        summary = self.coreLogic.readSummaryInfo( self.currentMonth )

        categorySummary = [ [ "Category", "Total" ] ]
        aggregateSummary = [ [ "Budget", "Total" ] ]

        for i in range( 0, len( summary[ 0 ] ), 2 ):
            categorySummary.append( [ summary[ 0 ][ i ], summary[ 0 ][ i + 1 ] ] )
        for i in range( 0, len( summary[ 1 ] ), 2 ):
            aggregateSummary.append( [ summary[ 1 ][ i ], summary[ 1 ][ i + 1 ] ] )

        print( tabulate( categorySummary, headers="firstrow" ) )
        print()
        print( tabulate( aggregateSummary, headers="firstrow" ) )

        # Should the Cli exit after this?
        return False

    def newMonth( self ):
        if self.verbose:
            print( "Got to New Month" )
        # Should the Cli exit after this?
        return False

    def changeCurrentMonth( self ):
        if self.verbose:
            print( "Got to Change Current Month" )
        # Should the Cli exit after this?
        return False

    def migrateOldSheets( self ):
        if self.verbose:
            print( "Got to Migrate Old Sheets" )
        # Should the Cli exit after this?
        return False

    def exitCli( self ):
        return True
