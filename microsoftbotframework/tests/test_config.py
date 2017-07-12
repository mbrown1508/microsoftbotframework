from unittest import TestCase
from microsoftbotframework import Config
import os

class ConfigTestCase(TestCase):
    def setUp(self):
        self.config = Config(os.getcwd() + '/microsoftbotframework/tests/test_files/good_config.yaml')

    # Test default
    def test_default_load(self):
        default_values = {'other': {'https_proxy': None, 'http_proxy': None, 'auth': True, 'verify_jwt_signature': True,
                                    'app_client_id': None, 'app_client_secret': None}, 'redis': {'uri': None},
                          'flask': {'host': '0.0.0.0', 'debug': False, 'port': '5000'}, 'celery': {'broker_url': None},
                          'mongodb': {'uri': None, 'database': 'microsoftbotframework', 'collection': 'state'}}
        self.assertEqual(self.config._get_default_config(), default_values)

    # Test yaml
    def test_yaml_load(self):
        yaml_config = self.config._get_yaml_config(os.getcwd() + '/microsoftbotframework/tests/test_files/good_config.yaml')
        self.assertEqual(yaml_config, {'other': {'app_client_id': '245gsh246hjb', 'app_client_secret': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_pool_limit': 'None'}})

    def test_bad_yaml_load(self):
        with self.assertRaises(Exception):
            self.config._get_yaml_config(os.getcwd() + '/microsoftbotframework/tests/test_files/bad_config.yaml')

    def test_missing_yaml(self):
        yaml_data = self.config._get_yaml_config(os.getcwd() + '/microsoftbotframework/tests/test_files/fjipowgnaoepirvniurv.yaml')
        self.assertEqual(yaml_data, {})

    def test_yaml_bad_formatting(self):
        with self.assertRaises(Exception):
            yaml_data = self.config._get_yaml_config(os.getcwd() + '/microsoftbotframework/tests/test_files/no_roots.yaml')

    # Test yaml merge
    def test_yaml_merge_same_values(self):
        default_values = {'other': {'https_proxy': None, 'http_proxy': None}, 'celery': {'broker_url': None}}
        yaml_config = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}}
        result = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}}

        self.assertEqual(self.config._replace_with_yaml_config(default_values, yaml_config), result)

    def test_yaml_merge_more_defaults(self):
        default_values = {'other': {'https_proxy': None, 'http_proxy': None}, 'celery': {'broker_url': None}, 'flask': {'port': 3000}}
        yaml_config = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}}
        result = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}, 'flask': {'port': 3000}}

        self.assertEqual(self.config._replace_with_yaml_config(default_values, yaml_config), result)

    def test_yaml_merge_additional_fields(self):
        default_values = {'other': {'https_proxy': None, 'http_proxy': None}, 'celery': {'broker_url': None}}
        yaml_config = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}, 'flask': {'port': 3000}}
        result = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}, 'flask': {'port': 3000}}

        self.assertEqual(self.config._replace_with_yaml_config(default_values, yaml_config), result)

    # Test env merge
    def test_env_merge_same_values(self):
        default_values = {'other': {'https_proxy': None, 'http_proxy': None}, 'celery': {'broker_url': None}}
        yaml_config = {'HTTPS_PROXY': '245gsh246hjb', 'HTTP_PROXY': '45hrtvb24hrtwhwrtb', 'CELERY_BROKER_URL': 'None'}
        result = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}}

        self.assertEqual(self.config._replace_with_environment_vars(default_values, yaml_config), result)

    def test_env_merge_more_defaults(self):
        default_values = {'other': {'https_proxy': None, 'http_proxy': None}, 'celery': {'broker_url': None}, 'flask': {'port': 3000}}
        yaml_config = {'HTTPS_PROXY': '245gsh246hjb', 'HTTP_PROXY': '45hrtvb24hrtwhwrtb', 'CELERY_BROKER_URL': 'None'}
        result = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}, 'flask': {'port': 3000}}

        self.assertEqual(self.config._replace_with_environment_vars(default_values, yaml_config), result)

    def test_env_merge_additional_fields(self):
        default_values = {'other': {'https_proxy': None, 'http_proxy': None}, 'celery': {'broker_url': None}}
        yaml_config = {'HTTPS_PROXY': '245gsh246hjb', 'HTTP_PROXY': '45hrtvb24hrtwhwrtb', 'CELERY_BROKER_URL': 'None', 'FLASK_PORT': 3000}
        result = {'other': {'https_proxy': '245gsh246hjb', 'http_proxy': '45hrtvb24hrtwhwrtb'}, 'celery': {'broker_url': 'None'}, 'flask': {'port': 3000}}

        self.assertEqual(self.config._replace_with_environment_vars(default_values, yaml_config), result)

    # Test parse
    def test_parse_config(self):
        config = {'other': {'https_proxy': 'True', 'http_proxy': 'False'},
                  'celery': {'broker_url': 'None'}, 'flask': {'port': '3000'}}
        result = {'other': {'https_proxy': True, 'http_proxy': False},
                  'celery': {'broker_url': None}, 'flask': {'port': 3000}}

        self.config.config = config
        self.config._parse_config_values()
        self.assertEqual(self.config.config, result)

    # Get Section Config
    def test_get_section_config(self):
        config = {'other': {'https_proxy': True, 'http_proxy': False},
                  'celery': {'broker_url': None}, 'flask': {'port': 3000}}
        result = {'https_proxy': True, 'http_proxy': False}

        self.config.config = config
        self.assertEqual(self.config.get_section_config('other'), result)

    # Get config
    def test_get_config_available(self):
        config = {'other': {'https_proxy': True, 'http_proxy': False},
                  'celery': {'broker_url': None}, 'flask': {'port': 3000}}
        result = True

        self.config.config = config
        self.assertEqual(self.config.get_config(None, 'https_proxy'), result)

    def test_get_config_unavailable(self):
        config = {'other': {'https_proxy': True, 'http_proxy': False},
                  'celery': {'broker_url': None}, 'flask': {'port': 3000}}
        result = None

        self.config.config = config

        with self.assertRaises(Exception):
            self.config.get_config(None, 'does_not_exist')

    def test_get_argument(self):
        config = {'other': {'https_proxy': True, 'http_proxy': False},
                  'celery': {'broker_url': None}, 'flask': {'port': 3000}}
        result = 'argument'

        self.config.config = config

        self.assertEqual(self.config.get_config('argument', 'https_proxy'), result)

    def test_get_config_different_root(self):
        config = {'other': {'https_proxy': True, 'http_proxy': False},
                  'celery': {'broker_url': None}, 'flask': {'port': 3000}}
        result = 3000

        self.config.config = config
        self.assertEqual(self.config.get_config(None, 'port', root='flask'), result)
