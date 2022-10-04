import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def basicReadData( SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, SCOPES ):
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            print( *row )
    except HttpError as err:
        print(err)

def getCreds( scope ):
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scope)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def basicAppendWriter( sheetId, valueRange, data, service ):
    try:
        body = {
            'values': data
        }
        req = service.spreadsheets().values().append(
            spreadsheetId=sheetId, range=valueRange,
            valueInputOption="USER_ENTERED", body=body )
        print( req )
        res = req.execute()
        print(f"{(res.get('updates').get('updatedCells'))} cells appended.")
        return res
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def main():
    sheetId = input()
    sampleRange = "BrainstormingTheDefaultValues!A:F"
    scope = [ "https://www.googleapis.com/auth/spreadsheets" ]
    if False:
        # This is a basic check to ensure everything works. That code is mostly
        # copy pasted from the quickstart tutorial.
        basicReadData( sheetId, sampleRange, scope )

    # Next thing I want to test out is seeing how I can write to the
    # spreadsheet itself. However, I do need some extra infra for this now: I 
    # will pull creds generation logic from the sample example and just generate
    # creds once on startup.
    creds = getCreds( scope )
    service = build('sheets', 'v4', credentials=creds)
    data = [
        [ 'Craft Cafe', '40', '5/10/2022', 'Retail', 'ws', '"V60", finally' ],
        [ 'Safeway', '20.12', '6/10/2022', 'Groceries', '', '', '' ]
    ]
    dataRange = 'BrainstormingTheDefaultValues!A:F'
    res = basicAppendWriter( sheetId, dataRange, data, service )

if __name__ == '__main__':
    main()
