import cliImpl
from gsheetInterface import TestBackendInterface
from coreLogic import TestCoreLogic

def main():
    verbose = True
    sheetId = "dummySheetId"
    gsheetIntf = TestBackendInterface( sheetId, verbose )
    coreLogic = TestCoreLogic( gsheetIntf, verbose )
    cli = cliImpl.CommandLineInterface( coreLogic, True )
    cli.cliLoop()

if __name__ == "__main__":
    main()
