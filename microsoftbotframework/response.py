from .utils import get_config
from urllib.parse import urljoin
import requests
import datetime
import redis


class Response:
    def __init__(self, message=None, auth=None, app_client_id=None, app_client_secret=None,
                 redis_url_token_store=None):
        self.auth = get_config(auth, 'AUTH', 'True')
        self.app_client_id = get_config(app_client_id, 'APP_CLIENT_ID', None)
        self.app_client_secret = get_config(app_client_secret, 'APP_CLIENT_SECRET', None)
        self.redis_url_token_store = get_config(redis_url_token_store, 'REDIS_URL_TOKEN_STORE', None)

        if self.app_client_id is None:
            print('The \'APP_CLIENT_ID\' has not been set. Disabling authentication.')
            self.auth = 'False'
        elif self.app_client_secret is None:
            print('The \'APP_CLIENT_SECRET\' has not been set. Disabling authentication.')
            self.auth = 'False'

        self.cache_token = True
        if self.auth == 'True':
            if self.redis_url_token_store is None:
                print('The \'REDIS_URI_TOKEN_STORE\' has not been set. Disabling token caching.')
                self.cache_token = False

        self.data = {} if message is None else message
        self.headers = None
        self.token = None
        self.redis = None

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

    def get_remote_auth_token(self):
        response_auth_url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
        data = {"grant_type": "client_credentials",
                "client_id": self.app_client_id,
                "client_secret": self.app_client_secret,
                "scope": "https://api.botframework.com/.default"
               }
        response = requests.post(response_auth_url, data)
        response_data = response.json()

        if self.cache_token:
            self.store_auth_token(token_type=response_data["token_type"],
                                  access_token=response_data["access_token"],
                                  expires_in=response_data["expires_in"],
                                  )

        return {
            'token_type': response_data["token_type"],
            'access_token': response_data["access_token"]
        }

    def store_auth_token(self, token_type, access_token, expires_in):
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=(int(expires_in) - 60))
        expires_at_string = expires_at.strftime('%Y-%m-%dT%H:%M:%S')

        self.redis.set("token_type", token_type)
        self.redis.set("access_token", access_token)
        self.redis.set("token_expires_at", expires_at_string)

    @staticmethod
    def has_token_expired(expires_at):
        return datetime.datetime.utcnow() > datetime.datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S')

    def get_redis_auth_token(self):
        self.redis = redis.StrictRedis.from_url(self.redis_url_token_store)
        token_type = self.redis.get("token_type").decode('UTF-8')
        access_token = self.redis.get("access_token").decode('UTF-8')
        token_expires_at = self.redis.get("token_expires_at").decode('UTF-8')

        if token_type is None or access_token is None or token_expires_at is None or \
                self.has_token_expired(token_expires_at):
            return self.get_remote_auth_token()
        else:
            return {
                'token_type': token_type,
                'access_token': access_token
            }

    def set_header(self):
        if self.cache_token:
            token = self.get_redis_auth_token()
        else:
            token = self.get_remote_auth_token()

        self.headers = {"Authorization": "{} {}".format(token["token_type"], token["access_token"])}

    def reply_to_activity(self, message, reply_to_id=None, from_info=None,
                          recipient=None, message_type=None, conversation=None):

        if self.auth == 'True':
            self.set_header()

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