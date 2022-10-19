# financial-tracking-offload
This is an app that allows me to interface with the Google Spreadsheet where I
keep all my financial transaction history and track my spending in. 

This is a simple command line utility that allows me to add new transactions to
the spreadsheet, and view spending summaries for the month. Additionally, it
allows me to create new sheets for new months and has a script to migrate my old
Excel spreadsheet to Google Sheets.

This README file will contain the information necessary to figure out how to
deploy this utility.

# "Deploying' the app
This app has a number of dependencies that need to be installed in order for the
utility to be installed. Check the `deps` file to see the list of dependencies
that need to be installed.

To get the app to work with google sheets, three files need to be present within
the file system (presumed to be a Linux file system because I am trying to
migrate away from any Windows device I have):
 1. `/usr/share/financialTracking/credentials.json`
 2. `/usr/share/financialTracking/staging`
 3. `/usr/share/financialTracking/prod`

The first file contains the service account credentials that are used to
communicate with the google sheets. You can follow the `Credentials` section of
the google sheet API quickstart tutorial and swap out the OAuth part with the
service account creds instead:
https://developers.google.com/sheets/api/quickstart/python

The second file contains the end of the URL for your "staging environment"
spreadsheet. This is where I manually test that my changes are sane and does not
contain any actually important / sensitive / real data. If you never run the app
with the `-s` flag, you can probably get away without setting the staging file,
but I would recommend using the staging environment to get used to what the app
does at first.

For example, if the URL for your "staging" spreadsheet is this:
`https://docs.google.com/spreadsheets/d/abcde12345/edit#gid=0`
Then the contents of the file would be:
`abcde12345`

The third file contains the end of the URL for your "production environment"
spreadsheet. Similar contents to what I just described for the staging file.

Now, one last tidbit of information that may be worth knowing: to give the 
service account access to your spreadsheet, copy the email generated within the
Google Cloud IAM for the service account and share the spreadsheet with that
email with editor access.

### Pls do not look through the older commits, they are a bit embarassing :(
