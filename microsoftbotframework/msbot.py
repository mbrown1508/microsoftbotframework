from flask import Flask, request
from celery.local import PromiseProxy
from .config import Config
import requests
import json
import redis
import datetime

try:
    from jwt.algorithms import RSAAlgorithm
    import jwt
except ImportError:
    pass

class MsBot:
    def __init__(self, host=None, port=None, debug=None, app_client_id=None, redis_uri=None, verify_jwt_signature=None):
        self.app = Flask(__name__)

        self.processes = []
        config = Config()
        self.host = config.get_config(host, 'HOST', root='flask')
        self.port = config.get_config(port, 'PORT', root='flask')
        self.debug = config.get_config(debug, 'DEBUG', root='flask')
        self.app_client_id = config.get_config(app_client_id, 'APP_CLIENT_ID')
        self.redis_uri = config.get_config(redis_uri, 'URI', root='redis')
        self.redis = None

        try:
            from jwt.algorithms import RSAAlgorithm
            import jwt
            self.verify_jwt_signature = config.get_config(verify_jwt_signature, 'VERIFY_JWT_SIGNATURE')
        except ImportError:
            self.verify_jwt_signature = False

        self.cache_certs = True
        if self.redis_uri is None:
            self.app.logger.info('The \'REDIS_URI\' has not been set. Disabling certificate caching.')
            self.cache_certs = False

        self.redis_config = config.get_section_config('redis')

        @self.app.route('/api/messages', methods=['POST'])
        def message_post():
            if self.verify_jwt_signature:
                valid_token = self._verify_token(request)
            else:
                valid_token = True

            if valid_token:
                json_message = request.get_json()

                json_headers = {}
                for key, value in request.headers:
                    json_headers[key] = value

                self.app.logger.info('message.headers: {}'.format(json.dumps(json_headers)))
                self.app.logger.info('message.body: {}'.format(json.dumps(json_message)))

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

    def _verify_token(self, request, forced_refresh=False):
        authorization_header = request.headers['Authorization']
        token = authorization_header[7:]
        authorization_scheme = authorization_header[:6]
        token_headers = jwt.get_unverified_header(token)

        # Get valid signing keys
        if self.cache_certs:
            valid_certificates = self._get_redis_certificates()
        else:
            valid_certificates = self._get_remote_certificates()

        # 1. The token was sent in the HTTP Authorization header with 'Bearer' scheme
        if authorization_scheme != "Bearer":
            self.app.logger.warning('The token was not sent in the http authorisation header with the Bearer scheme.')
            return False

        # 2. The token is valid JSON that conforms to the JWT standard (see references)
        # 4. The token contains an audience claim with a value equivalent to your bot's Microsoft App ID.
        # 5. The token has not yet expired. Industry-standard clock-skew is 5 minutes.
        # 6. The token has a valid cryptographic signature with a key listed in the OpenId keys document retrieved in step 1, above.
        decoded_jwt = None
        for dict_key in valid_certificates['keys']:
            if dict_key['kid'] == token_headers['kid']:
                key = json.dumps(dict_key)

                algo = RSAAlgorithm('SHA256')
                public_key = algo.from_jwk(key)

                try:
                    decoded_jwt = jwt.decode(token, public_key, algorithms=['RS256'], audience=self.app_client_id)
                except jwt.exceptions.InvalidTokenError as e:
                    self.app.logger.warning('{}'.format(e))
                    return False

        if decoded_jwt is None:
            if self.cache_certs and not forced_refresh:
                # Force cache refresh
                self.app.logger.warning('Forcing cache refresh as no valid certificate was found.')
                self._get_remote_certificates()
                return self._verify_token(request, forced_refresh=True)

            self.app.logger.warning('No valid certificate was found to verify JWT')
            return False

        # 3. The token contains an issuer claim with value of https://api.botframework.com
        if decoded_jwt['iss'] != 'https://api.botframework.com':
            self.app.logger.warning('The token issuer claim had the incorrect value of {}'.format(decoded_jwt['iss']))
            return False

        self.app.logger.info('Token was validated - {}'.format(json.dumps(decoded_jwt)))
        return decoded_jwt

    def _get_remote_certificates(self):
        openid_metadata_url = "https://login.botframework.com/v1/.well-known/openidconfiguration"
        openid_metadata = requests.get(openid_metadata_url)

        valid_signing_keys_url = openid_metadata.json()["jwks_uri"]
        valid_certificates = requests.get(valid_signing_keys_url)
        valid_certificates = valid_certificates.json()

        if self.cache_certs:
            self._store_certificates(valid_certificates)

        return valid_certificates

    def _store_certificates(self, valid_certificates):
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=5)
        expires_at_string = expires_at.strftime('%Y-%m-%dT%H:%M:%S')

        self.redis.set("valid_certificates", json.dumps(valid_certificates))
        self.redis.set("certificates_expire_at", expires_at_string)

        self.app.logger.info('Certificates stored')

    @staticmethod
    def _has_certificate_expired(expires_at):
        return datetime.datetime.utcnow() > datetime.datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S')

    def _get_redis_certificates(self):
        self.redis = redis.StrictRedis.from_url(self.redis_uri)
        for name, value in self.redis_config.items():
            if name != 'uri':
                self.redis.config_set(name, value)

        valid_certificates = self.redis.get("valid_certificates")
        certificates_expire_at = self.redis.get("certificates_expire_at")

        if valid_certificates is None or certificates_expire_at is None or \
                self._has_certificate_expired(certificates_expire_at.decode('UTF-8')):
            self.app.logger.info('Getting remote certificates')
            return self._get_remote_certificates()
        else:
            self.app.logger.info('Got stored certificates')
            return json.loads(valid_certificates.decode('UTF-8'))
