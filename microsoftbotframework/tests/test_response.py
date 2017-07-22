from unittest import TestCase
from ..response import Response
import os
from ..cache import JsonCache
from ..state import JsonState


class ResponseTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def _clear_environ():
        os.environ = {}

    def test_valid_arguments(self):
        self._clear_environ()
        response = Response(config_location='microsoftbotframework/tests/test_files/test_all_args.yaml')

        self.assertEqual(response.auth, True)
        self.assertEqual(response.app_client_id, 'asdf')
        self.assertEqual(response.app_client_secret, 'fdsa')
        self.assertEqual(response.http_proxy, 'http://proxy:81')
        self.assertEqual(response.https_proxy, 'https://proxy:81')
        self.assertEqual(response.cache_token, True)
        self.assertEqual(type(response.cache), type(JsonCache()))
        self.assertEqual(type(response.state), type(JsonState()))
        self.assertEqual(response.data, {})
        self.assertEqual(response.headers, None)
        self.assertEqual(response.token, None)

        self.data = {}
        self.headers = None
        self.token = None

    def test_incorrect_argument(self):
        with self.assertRaises(Exception):
            Response(bad_argument=None)

    def test_auth_disable_no_id(self):
        # If app_client_id or app_client_id is not set, disable auth
        self._clear_environ()
        response = Response(config_location='microsoftbotframework/tests/test_files/test_auth_disable.yaml')
        self.assertEqual(response.app_client_secret, None)
        self.assertEqual(response.auth, False)

    def test_auth_disable_no_secret(self):
        # If app_client_id or app_client_id is not set, disable auth
        self._clear_environ()
        response = Response(config_location='microsoftbotframework/tests/test_files/test_auth_disable.yaml')
        self.assertEqual(response.app_client_id, None)
        self.assertEqual(response.auth, False)

    def test_auth_enable(self):
        # If app_client_id or app_client_id is not set, disable auth
        response = Response(app_client_id='123456', app_client_secret='654321',
                            config_location='microsoftbotframework/tests/test_files/test_auth_disable.yaml')
        self.assertEqual(response.app_client_id, '123456')
        self.assertEqual(response.app_client_secret, '654321')
        self.assertEqual(response.auth, True)

    def test_cache_default(self):
        self._clear_environ()
        response = Response(app_client_id='123456', app_client_secret='654321',
                            config_location='microsoftbotframework/tests/test_files/test_auth_disable.yaml')
        self.assertEqual(type(response.cache), type(JsonCache()))
        self.assertEqual(response.cache_token, True)

    def test_cache_disable_2(self):
        self._clear_environ()
        response = Response(app_client_id='123456', app_client_secret='654321',
                            config_location='microsoftbotframework/tests/test_files/test_auth_disable.yaml',
                            cache=False)
        self.assertEqual(response.cache, None)
        self.assertEqual(response.cache_token, False)

    def test_cache_enable(self):
        self._clear_environ()
        response = Response(app_client_id='123456', app_client_secret='654321',
                            config_location='microsoftbotframework/tests/test_files/test_auth_disable.yaml',
                            cache='JsonCache')
        self.assertEqual(type(response.cache), type(JsonCache()))
        self.assertEqual(response.cache_token, True)

    def test_state_disable(self):
        self._clear_environ()
        response = Response(state=False)
        self.assertEqual(response.state, None)

    def test_state_enable(self):
        self._clear_environ()
        response = Response(state='JsonState')
        self.assertEqual(type(response.state), type(JsonState()))

    def test_state_enable_object(self):
        self._clear_environ()
        response = Response(state=JsonState())
        self.assertEqual(type(response.state), type(JsonState()))

    def test_state_default(self):
        self._clear_environ()
        response = Response()
        self.assertEqual(response.cache, None)

    def test_urljoin(self):
        self.assertEqual(Response.urljoin('https://asdf.com', 'something'), 'https://asdf.com/something')
        self.assertEqual(Response.urljoin('https://asdf.com', '/something'), 'https://asdf.com/something')
        self.assertEqual(Response.urljoin('https://asdf.com/', 'something'), 'https://asdf.com/something')
        self.assertEqual(Response.urljoin('https://asdf.com/', '/something'), 'https://asdf.com/something')
