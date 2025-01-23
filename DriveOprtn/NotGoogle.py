import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    print(pickle_file)

    if os.path.exists(pickle_file):
        try:
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)
        except Exception as e:
            print("Failed to load credentials from file:", e)
            cred = None

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            try:
                cred.refresh(Request())
            except Exception as e:
                print("Failed to refresh token:", e)
                # Remove the invalid token file
                if os.path.exists(pickle_file):
                    os.remove(pickle_file)
                # Proceed to re-authenticate
                cred = None
        if not cred:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server(port=0)
                # Save the new credentials to a token file
                with open(pickle_file, 'wb') as token:
                    pickle.dump(cred, token)
            except Exception as e:
                print("Failed to create new credentials:", e)
                return None

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
