import os.path
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from os.path import abspath

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

g_path = abspath(__file__).split('\\')[:-1]
g_path = '/'.join(g_path)


def google_auth():
    creds = None
    if os.path.exists('views/token.json'):
        creds = Credentials.from_authorized_user_file(f'{g_path}/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(f'{g_path}/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(f'{g_path}/token.json', 'w') as token:
            token.write(creds.to_json())

    return creds
    '''service = build('sheets', 'v4', credentials=creds)
    return service'''

