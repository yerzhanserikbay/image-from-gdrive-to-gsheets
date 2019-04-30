from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import gdrive

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1SJqPnKEnHTpG4YZlrxKIB5d7vXwSXIBbJJhcnzqGoYA'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-gsheet.pickle'):
        with open('token-gsheet.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials-gsheet.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token-gsheet.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    # sheet = service.spreadsheets()
    # result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
    #                             range=RANGE_NAME).execute()
    # values = result.get('values', [])


    RANGE_IMAGE_NAME = ''
    RANGE_IMAGE_ID = ''

    all_files = gdrive.getFiles()
    l = len(all_files)

    image_index = []
    image_name = []
    image_id = []

    for i in all_files:
        image_index.append([str(i[0])])
        image_name.append([str(i[1]).split(".")[0]])
        image_id.append([f"=IMAGE(\"https://drive.google.com/us?id={i[2]}\", 1)"])


    RANGE_IMAGE_INDEX = f'A2:{l+1}'
    RANGE_IMAGE_NAME = f'B2:{l+1}'
    RANGE_IMAGE_ID = f'C2:{l+1}'


    data = [
        {
            'range': RANGE_IMAGE_INDEX,
            'values': image_index
        },
        {
            'range': RANGE_IMAGE_ID,
            'values': image_name
        },
        {
            'range': RANGE_IMAGE_NAME,
            'values': image_id
        }
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))



if __name__ == '__main__':
    main()