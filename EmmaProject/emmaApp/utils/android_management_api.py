import json
from urllib.parse import urlencode

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
enterprise = None
enterprise_name = None


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
    global enterprise_name
    enterprise_name = enterprise['name']
    print('\nYour enterprise name is', enterprise_name)
    return enterprise_name


def create_policy(policy_name, policy_options):
    policy_full_name = get_enterprise_name() + '/policies/' + policy_name
    print(policy_options)
    print(policy_options)
    print(policy_full_name)
    androidmanagement.enterprises().policies().patch(
        name=policy_full_name,
        body=policy_options
    ).execute()
    return policy_full_name


def create_default_policy():
    # enterprise_name = 'enterprises/LC03hr5qbt'
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
    return policy_name


def enroll_device(enterprise_name, policy_name):
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


def get_policy_name():
    policy_name = enterprise_name + '/policies/policy1'
    return policy_name


def get_enterprise_name():
    enterprise_list = androidmanagement.enterprises().list(
        projectId=cloud_project_id
    ).execute()

    print(enterprise_list)
    enterprises_name = enterprise_list['enterprises'][0]['name']
    enterprise_display_name = enterprise_list['enterprises'][0]['enterpriseDisplayName']
    print(enterprises_name)
    print(enterprise_display_name)
    global enterprise_name
    enterprise_name = enterprises_name

    return enterprises_name


def get_devices():
    print(enterprise_name)
    devices = androidmanagement.enterprises().devices().list(
        parent=get_enterprise_name()
    ).execute()

    if devices:
        return devices['devices']
    else:
        return None


def delete_device(device_id):
    print(device_id)
    androidmanagement.enterprises().devices().delete(
        name=str(device_id)
    ).execute()
