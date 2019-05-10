from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import glob
import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN = open('TOKEN.txt', 'r').readline()


def getFiles():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-gdrive.pickle'):
        with open('token-gdrive.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials-gdrive.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token-gdrive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API

    page_token = None

    items = service.files().list(q="{} in parents".format(TOKEN),
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)',
                                    pageSize=490,
                                    pageToken=page_token).execute()


    files_info_array = []

    remote_files_array = []

    if not items:
        print('No files found.')
    else:
        print('Files:')
        i = 1
        for item in items.get('files', []):
            # print(u'{0} - {1} ({2})'.format(i, item['name'], item['id']))
            files_info_array.append([i, item['name'], item['id']])
            # filesDict[str(item['name']).split(".")[0]] = "Null"
            remote_files_array.append(str(item['name']).split(".")[0])
            i += 1

    pprint.pprint(files_info_array)


    return files_info_array



    # Comparing

    local_files_array = []

    jpeg = glob.glob('/Users/ys/Documents/image/*.jpeg')
    jpg = glob.glob('/Users/ys/Documents/image/*.jpg')

    local_files_array.extend(jpg)
    local_files_array.extend(jpeg)

    print("remoteFilesArray count: ", len(remote_files_array))

    print("localFilesArray count: ", len(local_files_array))



    # Compare local files with on drive files
    def compare():
        files_dict = {}

        local_state = 'NULL'
        remote_state = 'NON NULL'


        if len(remote_files_array) < len(local_files_array):
            local_state = 'NULL'
            remote_state = 'NON NULL'

        elif len(remote_files_array) > len(local_files_array):
            local_state = 'NON NULL'
            remote_state = 'NULL'


        for i in local_files_array:
            name = i.split("/Users/ys/Documents/image/")[1].split(".")[0]
            files_dict[name] = local_state

        for i in remote_files_array:
            files_dict[i] = remote_state


        pprint.pprint(files_dict)

        null_files_array = []

        for k, v in files_dict.items():
            if v == "NULL":
                null_files_array.append(k)

        print("null_files_array count: ", len(null_files_array))
        print(null_files_array)
