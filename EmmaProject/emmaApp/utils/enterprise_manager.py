from emmaApp.utils.authentication_manager import androidmanagement, cloud_project_id

CALLBACK_URL = 'https://storage.googleapis.com/android-management-quick-start/enterprise_signup_callback.html'

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

# Enterprise Name: enterprises/LC03hr5qbt

# Paste your enterprise name here.
# enterprise_name = 'enterprises/LC03hr5qbt'
