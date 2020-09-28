import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Reference: https://github.com/googleworkspace/python-samples/blob/master/slides/quickstart/quickstart.py
# Reference: https://github.com/googleworkspace/python-samples/blob/master/sheets/quickstart/quickstart.py   

TOKEN = "token"
PICKLE = "pickle"
CREDENTIALS = "credentials"
JSON = "json"

SLIDES = "slides"
SHEETS = "sheets"

SLIDES_VERSION = "v1"
SHEETS_VERSION = "v4"

SLIDES_SCOPES = ['https://www.googleapis.com/auth/presentations']
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class TriviaServices(object):
    def __init__(self):
        pass
    
    # main methods 
    def get_slides_service(self):
        return self.get_service_from_type(True) 
    
    def get_sheets_service(self):
        return self.get_service_from_type(False)

    def get_service_from_type(self, is_slides):
        suffix = self.get_suffix_fromType(is_slides)
        print(f"getting {suffix} service")
        pickle_filename, credentials_filename = self.get_pickle_and_credentials_filename_fromType(is_slides)
        service_name, version, scopes = self.get_serviceName_version_scopes_fromType(is_slides)
        service = self.get_service(pickle_filename, credentials_filename, service_name, version, scopes)
        print(f"done getting {suffix} service") 
        return service

    def get_service(self, pickle_filename, credentials_filename, service_name, version, scopes):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(pickle_filename):
            with open(pickle_filename, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_filename, scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(pickle_filename, 'wb') as token:
                pickle.dump(creds, token) 
        
        service = build(service_name, version, credentials=creds)
        return service

    # get helper methods 
    def get_serviceName_version_scopes_fromType(self, is_slides):        
        service_name = self.get_suffix_fromType(is_slides)
        version = SLIDES_VERSION if is_slides else SHEETS_VERSION
        scopes = SLIDES_SCOPES if is_slides else SHEETS_SCOPES
        return service_name, version, scopes

    def get_pickle_and_credentials_filename_fromType(self, is_slides):
        suffix = self.get_suffix_fromType(is_slides)
        pickle_filename = self.get_filename(TOKEN, suffix, PICKLE)
        credentials_filename = self.get_filename(CREDENTIALS, suffix, JSON)
        return pickle_filename, credentials_filename

    def get_filename(self, filename, suffix, ending):
        return f"{filename}_{suffix}.{ending}"
    
    def get_suffix_fromType(self, is_slides):
        return SLIDES if is_slides else SHEETS
        
