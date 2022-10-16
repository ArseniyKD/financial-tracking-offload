import cliImpl
from gsheetInterface import TestBackendInterface, GSheetBackendInterface
from coreLogic import TestCoreLogic, CoreLogic

def main():
    verbose = True
    sheetId = input()
    _ = input()
    gsheetIntf = GSheetBackendInterface( sheetId, verbose )
    coreLogic = CoreLogic( gsheetIntf, verbose )
    cli = cliImpl.CommandLineInterface( coreLogic, True )
    cli.cliLoop()

if __name__ == "__main__":
    main()
