from __future__ import print_function
from flask import Flask, request
from flask_cors import CORS
import json
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging
import TextRank as eZ

app = Flask(__name__)
CORS(app)
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']
logging.basicConfig(level=logging.DEBUG)
# The ID of a document.
DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

@app.route('/ezRead/endpoint',methods=['POST'])
def ezEndpoint():
    print("Running Endpoint", file=sys.stderr)
    data = request.data
    dataJSON = json.loads(data)
    print(dataJSON, file=sys.stderr)
    ezLaunchDoc(dataJSON.get("selection", ""))
    return "Success"

    #ezLaunchDoc(json)

def ezLaunchDoc(selection):
    """Uses the Docs API.
        Makes a new document with a summery from POST request.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    # document = service.dtitle = 'My Document'
    summs = eZ.ezRank(selection)
    body = {
        'title' : "New Summary"
    }
    requests = [
        {
            'insertText':{
                'location':{
                    'index':1,

                },
                'text':"\n" + summs
            }
        }
    ]
    document = service.documents().create(body=body).execute()
    result = service.documents().batchUpdate(documentId=document.get("documentId"), body={'requests':requests}).execute()

if __name__ == '__main__':
    app.run(debug=True)
