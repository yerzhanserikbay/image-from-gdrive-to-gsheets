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

    results = service.files().list(
        pageSize=425, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

    # folder_id = '0B7URSlB1tD6YWFV4bGRXQWRmSk0'

    page_token = None

    response = service.files().list(q="'1cghx9fx2aWchKsaEQrupoXdCr7nJrXxb' in parents",
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)',
                                    pageSize=490,
                                    pageToken=page_token).execute()

    remoteFilesArray = []

    filesInfoArray = []

    if not items:
        print('No files found.')
    else:
        print('Files:')
        i = 1
        for item in response.get('files', []):
            # print(u'{0} - {1} ({2})'.format(i, item['name'], item['id']))
            filesInfoArray.append([i, item['name'], item['id']])
            # filesDict[str(item['name']).split(".")[0]] = "Null"
            remoteFilesArray.append(str(item['name']).split(".")[0])
            i += 1

    return filesInfoArray

    pprint.pprint(filesInfoArray)

    # Comparing

    localFilesArray = []

    jpeg = glob.glob('/Users/ys/Documents/image/*.jpeg')
    jpg = glob.glob('/Users/ys/Documents/image/*.jpg')

    localFilesArray.extend(jpg)
    localFilesArray.extend(jpeg)

    print("remoteFilesArray count: ", len(remoteFilesArray))

    print("localFilesArray count: ", len(localFilesArray))

    if len(remoteFilesArray) < len(localFilesArray):
        bigger = localFilesArray
        smaller = remoteFilesArray
    elif len(remoteFilesArray) > len(localFilesArray):
        bigger = remoteFilesArray
        smaller = localFilesArray

    def compare():
        filesDict = {}

        # for i in bigger:
        #     name = i.split("/Users/ys/Documents/image/")[1].split(".")[0]
        #     filesDict[name] = "NULL"
        #
        # for i in smaller:
        #     filesDict[i] = "NON NULL"

        for i in bigger:
            filesDict[i] = "NULL"

        for i in smaller:
            name = i.split("/Users/ys/Documents/image/")[1].split(".")[0]
            filesDict[name] = "NON NULL"

        # pprint.pprint(localFilesDict)

        nullFilesArray = []

        for k, v in filesDict.items():
            if v == "NULL":
                nullFilesArray.append(k)

        print("nullFilesArray count: ", len(nullFilesArray))
        print(nullFilesArray)
# if __name__ == '__main__':
#     getFiles()