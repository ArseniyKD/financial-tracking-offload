import os.path
import sys
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class BaseBackendInterface( object ):
    def __init__( self ):
        pass

    def authenticate( self ):
        pass

    def makeService( self ):
        pass

    def append( self, valueRange, data ):
        pass

    def batchRead( self, readRanges ):
        pass

    def readSpreadsheetMetadata( self ):
        pass

    def createSheetTab( self, newTabIndex, newTabName ):
        pass

class TestBackendInterface( BaseBackendInterface ):
    # Mocks out the behavior of the regular gsheet interface for test purposes.
    # This class also keeps the expected interactions such as needing to do
    # auth before any op, and that the service creation happens on any first
    # op that needs it and fails if not authenticated yet.
    creds = False
    service = False

    def __init__( self, sheetId, verbose ):
        print( f"Mock: Constructor called with {sheetId}, {verbose}" )

    def authenticate( self ):
        print( "Mock: authentication requested." )
        self.creds = True

    def makeService( self ):
        if not self.creds:
            print( "Mock: Cannot make service, unauthenticated, bail" )
            sys.exit( 1 ) # See if this actually makes sense in test infra
        self.service = True

    def append( self, valueRange, data ):
        if not self.service:
            self.makeService()
        print( f"Mock: Append called with valueRange {valueRange} and data {data}" )
        return "mock"

    def batchRead( self, readRanges ):
        if not self.service:
            self.makeService()
        print( f"Mock: BatchRead called with readRanges {readRanges}" )
        retVal = [ { "values": [ [ "mock", "mock" ], [ "test", "test" ] ] },
                   { "values": [ [ "mock", "mock" ], [ "test", "test" ] ] } ]
        return retVal

    def readSpreadsheetMetadata( self ):
        if not self.service:
            self.makeService()
        print( "Mock: ReadSpreadsheetMetadata called" )
        retVal = [ { "properties" : { "title": "1" } },
                   { "properties" : { "title": "2" } } ]
        return retVal

    def createSheetTab( self, newTabIndex, newTabName ):
        if not self.service:
            self.makeService()
        print( f"Mock: CreateSheetTab called with index {newTabIndex}, name {newTabName}" )

class GSheetBackendInterface( BaseBackendInterface ):
    creds = None
    service = None
    sheetId = None
    verbose = False
    credentialScope = None

    def __init__( self, sheetId, verbose ):
        self.sheetId = sheetId
        self.verbose = verbose
        self.credentialScope = [ "https://www.googleapis.com/auth/spreadsheets" ]

    def authenticate( self ):
        if self.verbose:
            print( "Attempting to authenticate the user" )

        if self.creds:
            print( "WARN: Authentication called for the second time, returning" )
            return
        
        with open( '/usr/share/financialTracking/credentials.json' ) as source:
            info = json.load( source )

        self.creds = service_account.Credentials.from_service_account_info( info )
        return

    def makeService( self ):
        if self.verbose:
            print( "Attempting to create the API caller" )
        
        if not self.creds:
            print( "ERROR: Cannot make the service if unauthenticated, bail" )
            sys.exit( 1 )

        self.service = build('sheets', 'v4', credentials=self.creds)

    def append( self, valueRange, data ):
        if not self.service:
            self.makeService()

        try:
            body = {
                'values': data
            }
            req = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheetId, range=valueRange,
                valueInputOption="USER_ENTERED", body=body )
            res = req.execute()
            if self.verbose:
                print(f"{(res.get('updates').get('updatedCells'))} cells appended.")
            return res
        except HttpError as error:
            print(f"Append: An error occurred: {error}")
            return error

    def batchRead( self, readRanges ):
        if not self.service:
            self.makeService()

        try:
            result = self.service.spreadsheets().values().batchGet(
                    spreadsheetId=self.sheetId, ranges=readRanges ).execute()
            return result.get( 'valueRanges', [] )
        except HttpError as error:
            print(f"Append: An error occurred: {error}")
            return None
    
    def readSpreadsheetMetadata( self ):
        if not self.service:
            self.makeService()
        
        try:
            result = self.service.spreadsheets().get(
                    spreadsheetId=self.sheetId ).execute()
            return result.get( 'sheets', [] )
        except HttpError as error:
            print( f"readSpreadsheetMetadata: An error ocurred: {error}" )
            return None

    def createSheetTab( self, newTabIndex, newTabName ):
        if not self.service:
            self.makeService()

        request = [ {
            'addSheet' : {
                'properties' : {
                    'index': newTabIndex,
                    'title': newTabName,
                }
            }
            }
        ]
        body = {
            'requests' : request
        }
        try:
            self.service.spreadsheets().batchUpdate( spreadsheetId=self.sheetId,
                                                     body=body ).execute()
        except HttpError as error:
            print( f"failed creating a new sheet: {error}" )
            return
