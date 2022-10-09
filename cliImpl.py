import os
import sys
from pprint import pprint
from tabulate import tabulate

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

    def __init__( self, coreLogic, verbose ):
        self.coreLogic = coreLogic
        self.verbose = verbose
        self.topLevelMessage = "Welcome to the Financial Tracking App!\nMain Menu"
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
            

    def cliLoop( self ):
        questions = [
            inquirer.List( "topLevelQ", message=self.topLevelMessage,
                           choices=self.topLevelChoices )
        ]
        while True:
            answers = inquirer.prompt( questions )
            if self.verbose:
                pprint( answers )
            if self.specificCliFunctionMap[ answers[ "topLevelQ" ] ]():
                break
        print( self.exitMessage )

    def addTransactions( self ):
        if self.verbose:
            print( "Got to add transactions" )
        # Should the Cli exit after this?
        return False

    def seeSummary( self ):
        if self.verbose:
            print( "Got to See Summary" )
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
