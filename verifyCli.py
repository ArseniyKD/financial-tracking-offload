import cliImpl
from gsheetInterface import TestBackendInterface, GSheetBackendInterface
from coreLogic import TestCoreLogic, CoreLogic

def main():
    verbose = False
    sheetId = input()
    _ = input()
    gsheetIntf = GSheetBackendInterface( sheetId, verbose )
    coreLogic = CoreLogic( gsheetIntf, verbose )
    cli = cliImpl.CommandLineInterface( coreLogic, verbose )
    cli.cliLoop()

if __name__ == "__main__":
    main()
