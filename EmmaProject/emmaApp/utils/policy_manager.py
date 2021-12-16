import json

from emmaApp.utils.authentication_manager import androidmanagement

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
