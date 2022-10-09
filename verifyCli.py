import cliImpl
from gsheetInterface import GSheetBackendInterface, TestBackendInterface
from coreLogic import CoreLogic, TestCoreLogic

def main():
    verbose = True
    sheetId = "dummySheetId"
    gsheetIntf = TestBackendInterface( sheetId, verbose )
    coreLogic = TestCoreLogic( gsheetIntf, verbose )
    cli = cliImpl.CommandLineInterface( coreLogic, True )
    cli.cliLoop()

if __name__ == "__main__":
    main()
