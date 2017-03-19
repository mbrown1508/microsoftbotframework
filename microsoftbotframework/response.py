from .utils import get_config
from urllib.parse import urljoin
import requests
import datetime


class Response:
    def __init__(self, message=None, auth=None, app_client_id=None, app_client_secret=None):
        self.auth = get_config(auth, 'AUTH', 'True')
        self.app_client_id = get_config(app_client_id, 'APP_CLIENT_ID', None)
        self.app_client_secret = get_config(app_client_secret, 'APP_CLIENT_SECRET', None)

        if self.app_client_id is None:
            print('The \'APP_CLIENT_ID\' has not been set. Disabling authentication.')
            self.auth = 'False'
        elif self.app_client_secret is None:
            print('The \'APP_CLIENT_SECRET\' has not been set. Disabling authentication.')
            self.auth = 'False'

        self.data = {} if message is None else message
        self.headers = None

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise KeyError(key)

    def __setitem__(self, key, val):
        self.data[key] = val

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def __delitem__(self, key):
        self.data.pop(key, None)

    def __contains__(self, key):
        return True if key in self.data else False

    def authenticate(self):
        response_auth_url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
        data = {"grant_type": "client_credentials",
                "client_id": self.app_client_id,
                "client_secret": self.app_client_secret,
                "scope": "https://api.botframework.com/.default"
               }
        response = requests.post(response_auth_url, data)
        response_data = response.json()

        self.headers = {"Authorization": "{} {}".format(response_data["token_type"], response_data["access_token"])}

    def reply_to_activity(self, message, reply_to_id=None, from_info=None,
                          recipient=None, message_type=None, conversation=None):

        if self.auth == 'True':
            self.authenticate()

        conversation_id = self['conversation']["id"] if conversation is None else conversation['id']
        reply_to_id = self['id'] if reply_to_id is None else reply_to_id

        response_url = urljoin(self["serviceUrl"], "/v3/conversations/{}/activities".format(conversation_id, reply_to_id))

        response_json = {
            "from": self["recipient"] if from_info is None else from_info,
            "type": 'message' if message_type is None else message_type,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
            "conversation": self['conversation'] if conversation is None else conversation,
            "recipient": self["from"] if recipient is None else recipient,
            "text": message,
            "replyToId": reply_to_id
        }

        requests.post(response_url, json=response_json, headers=self.headers)