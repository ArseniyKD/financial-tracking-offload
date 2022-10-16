#!/usr/bin/python

import sys, os, getopt

from gsheetInterface import TestBackendInterface, GSheetBackendInterface
from cliImpl import CommandLineInterface
from coreLogic import TestCoreLogic, CoreLogic

helpStr = "Financial Tracking app usage:\n" + \
        "\t-h or --help:\tPrint the help string and exit\n" + \
        "\t-v or --verbose:\tSet the verbose flag to true\n" + \
        "\t-s or --staging:\tUse the staging google sheet.\n" + \
        "\t-b or --mockBackEnd:\tUse the mock back end.\n" + \
        "\t-c or --mockCoreLogic:\tUse the mock core logic.\n\n" + \
        "The expected file structure is to have the files for credentials, " + \
        "staging environment sheetId and production environment sheetid is as " + \
        "follows:\n" + \
        "\t/usr/share/financialTracking/credentials.json <- Service account creds\n" + \
        "\t/usr/share/financialTracking/staging <- File containing sheetId for staging environment\n" + \
        "\t/usr/share/financialTracking/prod <- File containing sheetId for production environment"

def main( argv ):
    shortOpt = "vshbc"
    longOpt = [ "verbose", "staging", "help", "mockBackEnd", "mockCoreLogic" ]
    try:
        opts, args = getopt.getopt( argv, shortOpt, longOpt )
    except getopt.GetoptError as err:
        print( f"Failed to get options: {err}" )
        print()
        print( helpStr )

    verbose = False
    mockCoreLogic = False
    mockBackend = False
    staging = False

    for opt, arg in opts:
        if opt in ( "-h", "--help" ):
            print( helpStr )
            sys.exit()
        elif opt in ( "-v", "--verbose" ):
            verbose = True
        elif opt in ( "-s", "--staging" ):
            staging = True
        elif opt in ( "-b", "--mockBackEnd" ):
            mockBackend = True
        elif opt in ( "-c", "--mockCoreLogic" ):
            mockCoreLogic = True

    sheetId = ""
    if staging:
        lines = None
        with open( "/usr/share/financialTracking/staging", "r" ) as fp:
            lines = fp.readlines()
        sheetId = lines[0].strip()
    else:
        lines = None
        with open( "/usr/share/financialTracking/prod", "r" ) as fp:
            lines = fp.readlines()
        sheetId = lines[0].strip()

    backend = None
    if mockBackend:
        backend = TestBackendInterface( sheetId, verbose )
    else:
        backend = GSheetBackendInterface( sheetId, verbose )

    coreLogic = None
    if mockCoreLogic:
        coreLogic = TestCoreLogic( backend, verbose )
    else:
        coreLogic = CoreLogic( backend, verbose )

    cli = CommandLineInterface( coreLogic, verbose )
    cli.cliLoop()


if __name__ == "__main__":
    main( sys.argv[ 1 : ] )
