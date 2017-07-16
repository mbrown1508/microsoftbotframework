import datetime
import json
import logging

import requests

from .cache import get_cache
from .state import get_state
from .config import Config

logger = logging.getLogger(__name__)


class Response:
    def __init__(self, **kwargs):
        config_location = kwargs.pop('config_location', None)
        config = Config(config_location)

        self.auth = config.get_config(kwargs.pop('auth', True), 'AUTH')
        self.app_client_id = config.get_config(kwargs.pop('app_client_id', None), 'APP_CLIENT_ID')
        self.app_client_secret = config.get_config(kwargs.pop('app_client_secret', None), 'APP_CLIENT_SECRET')
        self.http_proxy = config.get_config(kwargs.pop('http_proxy', None), 'HTTP_PROXY')
        self.https_proxy = config.get_config(kwargs.pop('https_proxy', None), 'HTTPS_PROXY')

        cache_arg = config.get_config(kwargs.pop('cache', None), 'cache')
        state_arg = config.get_config(kwargs.pop('state', None), 'state')

        if self.app_client_id is None:
            logger.info('The \'APP_CLIENT_ID\' has not been set. Disabling authentication.')
            self.auth = False
        elif self.app_client_secret is None:
            logger.info('The \'APP_CLIENT_SECRET\' has not been set. Disabling authentication.')
            self.auth = False

        self.cache_token = True
        if self.auth:
            if cache_arg is None or not cache_arg:
                logger.info('A cache object has not been set. Disabling token caching.')
                self.cache_token = False
                self.cache = None
            else:
                self.cache = get_cache(cache_arg, config)

        if state_arg is not None:
            self.state = get_state(state_arg, config)
        else:
            self.state = None

        self.data = {}
        self.headers = None
        self.token = None

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

        self.cache.set("token_type", token_type)
        self.cache.set("access_token", access_token)
        self.cache.set("token_expires_at", expires_at_string)

        logger.info('Auth token stored')

    @staticmethod
    def _has_token_expired(expires_at):
        return datetime.datetime.utcnow() > datetime.datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S')

    def _get_redis_auth_token(self):
        token_type = self.cache.get("token_type")
        access_token = self.cache.get("access_token")
        token_expires_at = self.cache.get("token_expires_at")

        if token_type is None or access_token is None or token_expires_at is None or \
                self._has_token_expired(token_expires_at):
            logger.info('Getting remote auth token')
            return self._get_remote_auth_token()
        else:
            logger.info('Got stored auth token')
            return {
                'token_type': token_type,
                'access_token': access_token
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

        if method == 'get':
            request_method = requests.get
        elif method == 'post':
            request_method = requests.post
        elif method == 'delete':
            request_method = requests.delete
        else:
            raise(Exception('{} is not a supported method'.format(method)))

        logger.info(str(method))
        logger.info('response_url: {}'.format(response_url))
        logger.info('response_headers: {}'.format(json.dumps(self.headers)))
        logger.info('response_json: {}'.format(json.dumps(response_json)))

        post_response = request_method(response_url, json=response_json, headers=self.headers)

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

    def save_response(self, type, conversation_id, response_json, url_parameters, response):
        if self.state is not None:
            self.state.save_activity({
                'type': type,
                'conversation_id': conversation_id,
                'activity': response_json,
                'url_parameters': url_parameters,
                'response': response,
            })
