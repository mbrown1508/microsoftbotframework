from .config import Config
import requests
import datetime
import redis
import logging
import json

logger = logging.getLogger(__name__)

class Response:
    def __init__(self, auth=None, app_client_id=None, app_client_secret=None,
                 redis_uri=None, http_proxy=None, https_proxy=None):
        config = Config()
        self.auth = config.get_config(auth, 'AUTH')
        self.app_client_id = config.get_config(app_client_id, 'APP_CLIENT_ID')
        self.app_client_secret = config.get_config(app_client_secret, 'APP_CLIENT_SECRET')
        self.redis_uri = config.get_config(redis_uri, 'URI', root='redis')
        self.http_proxy = config.get_config(http_proxy, 'HTTP_PROXY')
        self.https_proxy = config.get_config(https_proxy, 'HTTPS_PROXY')

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

        self.data = {}
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

    def _request(self, response_url, method, response_json=None):
        self._set_header()

        logger.info(str(method))
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

    @staticmethod
    def urljoin(url1, url2):
        url1_has_end_slash = url1[-1] == '/'
        url2_has_start_slash = url2[0] == '/'

        if url1_has_end_slash != url2_has_start_slash:
            return url1 + url2
        elif url1_has_end_slash and url1_has_end_slash:
            return url1 + url2[1:]
        else:
            return url1 + '/' + url2

    def reply_to_activity(self, activity):
        response_url = self.urljoin(activity.serviceUrl,
                                    "/v3/conversations/{}/activities/{}".format(
                                        activity.conversation['id'],
                                        activity.activityId))

        return self._request(response_url, requests.post, activity.to_dict())

    def send_to_conversation(self, activity):
        response_url = self.urljoin(activity.serviceUrl,
                                    "/v3/conversations/{}/activities".format(
                                        activity.conversation['id']))

        return self._request(response_url, requests.post, activity.to_dict())

    def delete_activity(self, activity):
        response_url = self.urljoin(activity.serviceUrl,
                                        "/v3/conversations/{}/activities/{}".format(
                                            activity.conversation['id'],
                                            activity.activityId))

        return self._request(response_url, requests.delete)

    def create_conversation(self, activity):
        # make sure that we remove and team or channel data from the request when working in teams.
        if activity.channelData is not None:
            activity.channelData = {"tenant": {"id": activity.channelData["tenant"]["id"]}}
        activity.channelId = None
        activity.conversation = None

        response_json = {
            'bot': activity.fromAccount if activity.bot is None else activity.bot,
            'isGroup': False if activity.isGroup is None else activity.isGroup,
            'members': [activity.recipient] if activity.members is None else activity.members,
            'activity': activity.to_dict(),
        }

        if len(response_json['members']) > 1:
            response_json['isGroup'] = True

        if activity.topicName is not None:
            response_json['topicName'] = activity.topicName

        response_url = self.urljoin(activity.serviceUrl, "/v3/conversations")

        return self._request(response_url, requests.post, response_json)