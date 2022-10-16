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
        self.topLevelChoices.append("Show Current Month")
        self.topLevelChoices.append("New Month")
        self.topLevelChoices.append("Change Current Month")
        self.topLevelChoices.append("Migrate Old Sheets")
        self.topLevelChoices.append("Exit")
        self.exitMessage = "Thank you for using the Financial Tracking App"
        self.topLevelQ = "topLevelQ"
        self.specificCliFunctionMap = {
            self.topLevelChoices[ 0 ]: self.addTransactions,
            self.topLevelChoices[ 1 ]: self.seeSummary,
            self.topLevelChoices[ 2 ]: self.showCurrentMonth,
            self.topLevelChoices[ 3 ]: self.newMonth,
            self.topLevelChoices[ 4 ]: self.changeCurrentMonth,
            self.topLevelChoices[ 5 ]: self.migrateOldSheets,
            self.topLevelChoices[ 6 ]: self.exitCli
        }
        self.currentMonth = self.coreLogic.getTabs()[ 0 ]

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

    def showCurrentMonth( self ):
        print( self.currentMonth )
        return False

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
            sanitizedTx = [ t.strip() for t in tx.split( "," ) ]
            self.coreLogic.addTransactions(
                [ sanitizedTx ], self.currentMonth,
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
                pendingTransactions.append(
                        [ t.strip() for t in tx.split( "," ) ] )

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

        if self.verbose:
            pprint( summary )

        categorySummary = [ [ "Category", "Total" ] ]
        aggregateSummary = [ [ "Budget", "Total" ] ]

        for line in summary[ 0 ] :
            categorySummary.append( [ line[ 0 ], line[ 1 ] ] )
        for line in summary[ 1 ]:
            aggregateSummary.append( [ line[ 0 ], line[ 1 ] ] )

        print( tabulate( categorySummary, headers="firstrow" ) )
        print()
        print( tabulate( aggregateSummary, headers="firstrow" ) )

        # Should the Cli exit after this?
        return False

    def validateNewMonthTab( self, newMonthTab ):
        tabs = self.coreLogic.getTabs()
        return newMonthTab not in tabs

    def newMonth( self ):
        if self.verbose:
            print( "Got to New Month" )

        newMonthTLQ = "newMonthTLQ"
        newMonthTLM = "Adding a new tab in google sheets for the new month."
        newMonthTLC = [ "Provide New Month", "Cancel" ]

        tlQuestions = [
            inquirer.List( newMonthTLQ, message=newMonthTLM,
                           choices=newMonthTLC )
        ]
        tlAnswers = inquirer.prompt( tlQuestions )

        if self.verbose:
            pprint( tlAnswers )

        if tlAnswers[ newMonthTLQ ] == newMonthTLC[ 1 ]:
            return False

        newMonthBLQ = "newMonthBLQ"
        newMonthBLM = "Provide a name for the new month sheet. " + \
                "If it's not new, the operation will do nothing"
        
        blQuestions = [
            inquirer.Text( newMonthBLQ, message=newMonthBLM )
        ]
        blAnswers = inquirer.prompt( blQuestions )
        
        if self.verbose:
            pprint( blAnswers )

        newMonthTab = blAnswers[ newMonthBLQ ]
        if self.validateNewMonthTab( newMonthTab ):
            self.coreLogic.createNewMonthSheet( newMonthTab )
            self.currentMonth = newMonthTab

        # Should the Cli exit after this?
        return False

    def changeCurrentMonth( self ):
        if self.verbose:
            print( "Got to Change Current Month" )

        changeMonthTLQ = "changeMonthTLQ"
        changeMonthTLM = "Change the month that the transactions will count against " + \
                "and the summary will be shown off."
        changeMonthTLC = [ "Cancel" ] + self.coreLogic.getTabs()

        tlQuestions = [
            inquirer.List( changeMonthTLQ, message=changeMonthTLM,
                           choices=changeMonthTLC )
        ]
        tlAnswers = inquirer.prompt( tlQuestions )

        if self.verbose:
            pprint( tlAnswers )

        if tlAnswers[ changeMonthTLQ ] == changeMonthTLC[ 0 ]:
            return False

        self.currentMonth = tlAnswers[ changeMonthTLQ ]
        
        # Should the Cli exit after this?
        return False

    def migrateOldSheets( self ):
        if self.verbose:
            print( "Got to Migrate Old Sheets" )
        
        migrateTLQ = "migrateTLQ"
        migrateTLM = "Will migrate all the old tabs saved as CSVs over to google " + \
                "sheets as described in CoreLogic's migrateOldSheets method"
        migrateTLC = [ "Provide path to folder with old sheets", "Cancel" ]

        tlQuestions = [
            inquirer.List( migrateTLQ, message=migrateTLM, choices=migrateTLC ) ]
        tlAnswers = inquirer.prompt( tlQuestions )

        if self.verbose:
            pprint( tlAnswers )

        if tlAnswers[ migrateTLQ ] == migrateTLC[ 1 ]:
            return False

        migrateBLQ = "migrateBLQ"
        migrateBLM = "Provide a path to the folder contaning all the CSVs. " + \
                "If it does not exist, the operation will do nothing."
        blQuestions = [
            inquirer.Path( migrateBLQ, message=migrateBLM, exists=True,
                           path_type=inquirer.Path.DIRECTORY,
                           normalize_to_absolute_path=True )
        ]
        blAnswers = inquirer.prompt( blQuestions )

        if self.verbose:
            pprint( blAnswers )

        self.coreLogic.migrateOldSheets( blAnswers[ migrateBLQ ] )

        # Should the Cli exit after this?
        return False

    def exitCli( self ):
        return True
