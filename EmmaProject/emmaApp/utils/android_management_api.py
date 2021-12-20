import json
from urllib.parse import urlencode

from google.protobuf import service
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
CALLBACK_URL = 'https://storage.googleapis.com/android-management-quick-start/enterprise_signup_callback.html'

androidmanagement = None
signup_url = None


def authenticate_google_user():
    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
    credentials = flow.run_local_server()
    # Create the API client.
    global androidmanagement
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    print('\nAuthentication succeeded.')


def create_enterprise():
    if androidmanagement is None:
        authenticate_google_user()

    global signup_url
    signup_url = androidmanagement.signupUrls().create(
        projectId=cloud_project_id,
        callbackUrl=CALLBACK_URL
    ).execute()

    print('Please visit this URL to create an enterprise:', signup_url['url'])
    return signup_url['url']


def enter_enterprise_token(token):
    global enterprise
    enterprise = androidmanagement.enterprises().create(
        projectId=cloud_project_id,
        signupUrlName=signup_url['name'],
        enterpriseToken=token,
        body={}
    ).execute()
    enterprise_name = enterprise['name']
    print('\nYour enterprise name is', enterprise_name)
    return enterprise_name



def enroll_device():
    # Run the OAuth flow.
    # Generate a signup URL where the enterprise admin can signup with a Gmail account.
    signup_url = androidmanagement.signupUrls().create(
        projectId=cloud_project_id,
        callbackUrl=CALLBACK_URL
    ).execute()
    print('Please visit this URL to create an enterprise:', signup_url['url'])
    enterprise_token = input('Enter the code: ')
    # Complete the creation of the enterprise and retrieve the enterprise name.
    enterprise = androidmanagement.enterprises().create(
        projectId=cloud_project_id,
        signupUrlName=signup_url['name'],
        enterpriseToken=enterprise_token,
        body={}
    ).execute()
    enterprise_name = enterprise['name']
    # EAJmqckxDX-PV1eJGZUS5SYmrHcB1O-stL5DbRbcwYl3PyTV_YHPDSPjScQKNav2i747XJSZSGAf5ukOM4vfUtTadFXigwBMIlvee4YkpVGzw_UBwcBtwisw
    print('\nYour enterprise name is', enterprise_name)
    # Paste the enterprise name here.
    # enterprise_name = 'enterprises/LC03hr5qbt'
    enterprise_name = 'enterprises/LC03hr5qbt'
    policy_name = enterprise_name + '/policies/policy1'
    policy_json = '''
{
    "applications": [
        {
            "packageName": "com.google.samples.apps.iosched",
            "installType": "FORCE_INSTALLED"
        }
    ],
    "debuggingFeaturesAllowed": true
}
'''
    androidmanagement.enterprises().policies().patch(
        name=policy_name,
        body=json.loads(policy_json)
    ).execute()
    enrollment_token = androidmanagement.enterprises().enrollmentTokens().create(
        parent=enterprise_name,
        body={"policyName": policy_name}
    ).execute()
    image = {
        'cht': 'qr',
        'chs': '500x500',
        'chl': enrollment_token['qrCode']
    }
    qrcode_url = 'https://chart.googleapis.com/chart?' + urlencode(image)
    print('Please visit this URL to scan the QR code:', qrcode_url)
    enrollment_link = 'https://enterprise.google.com/android/enroll?et=' + enrollment_token['value']
    print('Please open this link on your device:', enrollment_link)
    return qrcode_url
