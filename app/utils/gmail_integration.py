import requests
import os
import datetime
import base64
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def search_emails(service, query):
    try:
        # Call the Gmail API
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_email_data(service, message_id):
    try:
        message = service.users().messages().get(userId='me', id=message_id).execute()
        payload = message['payload']
        headers = payload.get('headers', [])
        subject = None
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        parts = payload.get('parts', [])
        body = None
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
        return {'subject': subject, 'body': body}
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_todays_emails():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    today = datetime.date.today().strftime("%Y/%m/%d")
    query = f'after:{today} newsletter'
    messages = search_emails(service, query)
    emails = []
    if messages:
        for message in messages:
            email_data = get_email_data(service, message['id'])
            if email_data:
                emails.append(email_data)
    return emails

def load_clients_json():
    clients_path = os.getenv('CLIENTS_PATH_NAME')
    if clients_path and os.path.exists(clients_path):
        with open(clients_path, 'r') as file:
            return json.load(file)
    return None
