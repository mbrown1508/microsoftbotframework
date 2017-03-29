from flask import Flask, request
from celery.local import PromiseProxy
from .config import Config
import requests
import json
from jwt.algorithms import RSAAlgorithm
import jwt


class MsBot:
    def __init__(self, host=None, port=None, debug=None, app_client_id=None):
        self.processes = []
        config = Config()
        self.host = config.get_config(host, 'HOST', root='flask')
        self.port = config.get_config(port, 'PORT', root='flask')
        self.debug = config.get_config(debug, 'DEBUG', root='flask')
        self.app_client_id = config.get_config(app_client_id, 'APP_CLIENT_ID')

        self.app = Flask(__name__)

        @self.app.route('/api/messages', methods=['POST'])
        def message_post():
            valid_token = self.verify_token(request)

            if valid_token:
                json_message = request.get_json()

                self.app.logger.info('message.headers: {}'.format(json.dumps({a:b for a, b in request.headers.itervalues()})))
                self.app.logger.info('message.body: {}'.format(json_message))

                for process in self.processes:
                    if isinstance(process, PromiseProxy):
                        self.app.logger.info('Processing task {} asynchronously.'.format(type(process).__name__))
                        process.delay(json_message)
                    elif callable(process):
                        self.app.logger.info('Processing task {} synchronously.'.format(process.__name__))
                        process(json_message)
                return "Success"

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def verify_token(self, request):
        authorization_header = request.headers['Authorization']
        token = authorization_header[7:]
        authorization_scheme = authorization_header[:6]
        token_headers = jwt.get_unverified_header(token)

        # Get valid signing keys
        openid_metadata_url = "https://login.botframework.com/v1/.well-known/openidconfiguration"
        openid_metadata = requests.get(openid_metadata_url)

        valid_signing_keys_url = openid_metadata.json()["jwks_uri"]
        valid_signing_keys = requests.get(valid_signing_keys_url)
        valid_signing_keys = valid_signing_keys.json()

        # 1. The token was sent in the HTTP Authorization header with 'Bearer' scheme
        if authorization_scheme != "Bearer":
            self.app.logger.warning('The token was not sent in the http authorisation header with the Bearer scheme.')
            return False

        # 2. The token is valid JSON that conforms to the JWT standard (see references)
        # 4. The token contains an audience claim with a value equivalent to your bot's Microsoft App ID.
        # 5. The token has not yet expired. Industry-standard clock-skew is 5 minutes.
        # 6. The token has a valid cryptographic signature with a key listed in the OpenId keys document retrieved in step 1, above.
        decoded_jwt = None
        for dict_key in valid_signing_keys['keys']:
            if dict_key['kid'] == token_headers['kid']:
                key = json.dumps(dict_key)

                algo = RSAAlgorithm('SHA256')
                public_key = algo.from_jwk(key)

                try:
                    decoded_jwt = jwt.decode(token, public_key, algorithms=['RS256'], audience=self.app_client_id)
                    self.app.logger.info(decoded_jwt)
                except jwt.exceptions.InvalidTokenError as e:
                    self.app.logger.warning('{}'.format(e))
                    return False

        if decoded_jwt is None:
            self.app.logger.warning('No valid certificate was found to verify JWT')
            return False

        # 3. The token contains an issuer claim with value of https://api.botframework.com
        if decoded_jwt['iss'] != 'https://api.botframework.com':
            self.app.logger.warning('The token issuer claim had the incorrect value of {}'.format(decoded_jwt['iss']))
            return False

        self.app.logger.info('Token was validated.')
        return decoded_jwt
