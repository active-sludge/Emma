from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


cloud_project_id = 'swe599-emma'

CLIENT_CONFIG = {
    'installed': {
        'client_id': '882252295571-uvkkfelq073vq73bbq9cmr0rn8bt80ee.apps.googleusercontent.com',
        'client_secret': 'S2QcoBe0jxNLUoqnpeksCLxI',
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://accounts.google.com/o/oauth2/token'
    }
}

SCOPES = ['https://www.googleapis.com/auth/androidmanagement']

# Run the OAuth flow.
flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
credentials = flow.run_console()

# Create the API client.
androidmanagement = build('androidmanagement', 'v1', credentials=credentials)

print('\nAuthentication succeeded.')


