from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from requests.exceptions import ConnectionError, HTTPError, Timeout

from ..response import Response
import os
from ..cache import JsonCache
from ..state import JsonState


class ResponseTestCase(TestCase):
    def _mock_response(
            self,
            status_code=200,
            content=b'CONTENT',
            raise_for_status=None):
        """
        Build a mock for each response, include errors and content data
        """
        mock_resp = Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        mock_resp.status_code = status_code
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
            return mock_resp
        mock_resp.content = content
        mock_resp.iter_content = Mock()
        iter_result =  iter([bytes([b]) for b in content])
        mock_resp.iter_content.return_value = iter_result
        return mock_resp

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

    @patch('microsoftbotframework.response.requests.get')
    def test_request_raises_exceptions(self, mock_get):
        """
        This test ensures that the timeout_seconds is set correctly, and that requests exceptions are raised by
        the _request method
        """
        self._clear_environ()
        timeout_seconds = 2
        response = Response(config_location='microsoftbotframework/tests/test_files/test_auth_disable.yaml',
                            timeout_seconds=timeout_seconds)
        self.assertEqual(response.timeout_seconds, timeout_seconds)

        response_url = 'https://asdf.com/'
        methods = ['get', 'post', 'delete']

        for method in methods:
            # ConnectionError case
            mock_return_value = self._mock_response(status_code=None, raise_for_status=ConnectionError())
            mock_get.return_value = mock_return_value
            with self.assertRaises(ConnectionError):
                response._request(response_url, method, response_json=None)

            # HTTPError case
            mock_return_value = self._mock_response(status_code=404, raise_for_status=HTTPError())
            mock_get.return_value = mock_return_value
            with self.assertRaises(HTTPError):
                response._request(response_url, method, response_json=None)

            # Timeout case
            mock_return_value = self._mock_response(status_code=None, raise_for_status=Timeout())
            mock_get.return_value = mock_return_value
            with self.assertRaises(Timeout):
                response._request(response_url, method, response_json=None)
