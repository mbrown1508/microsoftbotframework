from .config import Config
import requests
import datetime
import redis
import logging
import json


class Response:
    def __init__(self, message=None, auth=None, app_client_id=None, app_client_secret=None,
                 redis_uri=None, http_proxy=None, https_proxy=None):
        config = Config()
        self.auth = config.get_config(auth, 'AUTH')
        self.app_client_id = config.get_config(app_client_id, 'APP_CLIENT_ID')
        self.app_client_secret = config.get_config(app_client_secret, 'APP_CLIENT_SECRET')
        self.redis_uri = config.get_config(redis_uri, 'URI', root='redis')
        self.http_proxy = config.get_config(http_proxy, 'HTTP_PROXY')
        self.https_proxy = config.get_config(https_proxy, 'HTTPS_PROXY')

        logger = logging.getLogger(__name__)

        if self.app_client_id is None:
            logger.info('The \'APP_CLIENT_ID\' has not been set. Disabling authentication.')
            self.auth = False
        elif self.app_client_secret is None:
            logger.info('The \'APP_CLIENT_SECRET\' has not been set. Disabling authentication.')
            self.auth = False

        self.cache_token = True
        if self.auth:
            if self.redis_uri is None:
                logger.info('The \'REDIS_URI_TOKEN_STORE\' has not been set. Disabling token caching.')
                self.cache_token = False

        self.data = {} if message is None else message
        self.headers = None
        self.token = None
        self.redis = None
        self.redis_config = config.get_section_config('redis')

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

    def _get_remote_auth_token(self):
        response_auth_url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
        data = {"grant_type": "client_credentials",
                "client_id": self.app_client_id,
                "client_secret": self.app_client_secret,
                "scope": "https://api.botframework.com/.default"
                }
        response = requests.post(response_auth_url, data)
        response_data = response.json()

        if self.cache_token:
            self._store_auth_token(token_type=response_data["token_type"],
                                   access_token=response_data["access_token"],
                                   expires_in=response_data["expires_in"],
                                   )

        return {
            'token_type': response_data["token_type"],
            'access_token': response_data["access_token"]
        }

    def _store_auth_token(self, token_type, access_token, expires_in):
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=(int(expires_in) - 60))
        expires_at_string = expires_at.strftime('%Y-%m-%dT%H:%M:%S')

        self.redis.set("token_type", token_type)
        self.redis.set("access_token", access_token)
        self.redis.set("token_expires_at", expires_at_string)

        logger = logging.getLogger(__name__)
        logger.info('Auth token stored')

    @staticmethod
    def _has_token_expired(expires_at):
        return datetime.datetime.utcnow() > datetime.datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S')

    def _get_redis_auth_token(self):
        self.redis = redis.StrictRedis.from_url(self.redis_uri)
        for name, value in self.redis_config.items():
            if name != 'uri':
                self.redis.config_set(name, value)
        token_type = self.redis.get("token_type")
        access_token = self.redis.get("access_token")
        token_expires_at = self.redis.get("token_expires_at")

        logger = logging.getLogger(__name__)

        if token_type is None or access_token is None or token_expires_at is None or \
                self._has_token_expired(token_expires_at.decode('UTF-8')):
            logger.info('Getting remote auth token')
            return self._get_remote_auth_token()
        else:
            logger.info('Got stored auth token')
            return {
                'token_type': token_type.decode('UTF-8'),
                'access_token': access_token.decode('UTF-8')
            }

    def _set_header(self):
        if self.auth:
            if self.cache_token:
                token = self._get_redis_auth_token()
            else:
                token = self._get_remote_auth_token()

            self.headers = {"Authorization": "{} {}".format(token["token_type"], token["access_token"])}

    def _post_request(self, response_url, method, response_json=None):
        self._set_header()

        logger = logging.getLogger(__name__)
        logger.info('response_url: {}'.format(response_url))
        logger.info('response_headers: {}'.format(json.dumps(self.headers)))
        logger.info('response_json: {}'.format(json.dumps(response_json)))

        post_response = method(response_url, json=response_json, headers=self.headers)

        if post_response.status_code == 200 or post_response.status_code == 201:
            logger.info('Successfully posted to Microsoft Bot Connector. {}'.format(post_response.text))
        else:
            logger.error('Error posting to Microsoft Bot Connector. Status Code: {}, Text {}'
                         .format(post_response.status_code, post_response.text))

        return post_response

    def _preload_message_data(self, fields, additional_fields, override=None):
        response_json = {}
        additional_params = {}

        for field in fields:
            if field in ['from', 'recipient', 'replyToId', 'timestamp']:
                if field == 'from' and 'recipient' in self.data:
                    response_json['from'] = self.data['recipient']
                elif field == 'recipient' and 'from' in self.data:
                    response_json['recipient'] = self.data['from']
                elif field == 'replyToId' and 'id' in self.data:
                    response_json['replyToId'] = self.data['id']
                elif field == 'timestamp':
                    response_json["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")
            else:
                if field in self.data:
                    response_json[field] = self.data[field]

        if override is not None:
            for key, value in override.items():
                if key in response_json:
                    response_json[key] = value

        for field in additional_fields:

            if field in ['conversationId', 'activityId']:
                if field == 'conversationId' and 'conversation' in self.data:
                    if 'id' in self.data['conversation']:
                        additional_params['conversationId'] = self.data['conversation']['id']
                elif field == 'activityId' and 'id' in self.data:
                    additional_params['activityId'] = self.data['id']
            else:
                if field in self.data:
                    additional_params[field] = self.data[field]

        return response_json, additional_params

    def _reply_to_activity(self, message, override_response_json, conversation_id=None,
                          activity_id=None, service_url=None):
        response_json, additional_params = self._preload_message_data(
            fields=['from', 'type', 'timestamp', 'conversation', 'recipient', 'text',
                    'replyToId', 'serviceUrl', 'channelId', 'channelData', 'textFormat'],
            additional_fields=['conversationId', 'activityId', 'serviceUrl'],
            override=override_response_json,
        )
        response_json['text'] = message

        response_url = self.urljoin(additional_params['serviceUrl'] if service_url is None else service_url,
                               "/v3/conversations/{}/activities/{}".format(
            additional_params['conversationId'] if conversation_id is None else conversation_id,
            additional_params['activityId'] if activity_id is None else activity_id))

        return self._post_request(response_url, requests.post, response_json)

    def reply_to_activity(self, message, conversation_id=None,
                          activity_id=None, service_url=None, **override_response_json):
        return self._reply_to_activity(message, override_response_json, conversation_id,
                                       activity_id, service_url)

    def send_to_conversation(self, message, conversation_id=None,
                             service_url=None, **override_response_json):
        return self._reply_to_activity(message, override_response_json, conversation_id,
                                       '', service_url)

    def delete_activity(self, activity_id=None, conversation_id=None, service_url=None):
        response_json, additional_params = self._preload_message_data(
            fields=[],
            additional_fields=['conversationId', 'activityId', 'serviceUrl'],
        )

        response_url = self.urljoin(additional_params['serviceUrl'] if service_url is None else service_url,
                               "/v3/conversations/{}/activities/{}".format(
            additional_params['conversationId'] if conversation_id is None else conversation_id,
            additional_params['activityId'] if activity_id is None else activity_id))

        return self._post_request(response_url, requests.delete)

    def create_conversation(self, message, topic_name=None, service_url=None, **override_response_json):
        response_json, additional_params = self._preload_message_data(
            fields=['channelData'],
            additional_fields=['serviceUrl'],
            override=override_response_json,
        )
        response_json['bot'] = self['recipient']
        response_json['isGroup'] = True
        response_json['activity'] = {}
        response_json['members'] = []
        response_json['activity'] = {
            'type': "message",
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
            'serviceUrl': self['serviceUrl'],
            'channelId': self['channelId'],
            "from": self['recipient'],
            "text": message
        }
        if topic_name is not None:
            response_json['topicName'] = topic_name

        response_url = self.urljoin(additional_params['serviceUrl'] if service_url is None else service_url, "/v3/conversations")

        return self._post_request(response_url, requests.post, response_json)

    @staticmethod
    def urljoin(url1, url2):
        url1_has_end_slash = url1[-1] == '/'
        url2_has_start_slash = url2[0] == '/'

        print(url1_has_end_slash, url2_has_start_slash)

        if url1_has_end_slash != url2_has_start_slash:
            return url1 + url2
        elif url1_has_end_slash and url1_has_end_slash:
            return url1 + url2[1:]
        else:
            return url1 + '/' + url2

