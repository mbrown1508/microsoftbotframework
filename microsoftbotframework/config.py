import os
import yaml
import logging


class Config:
    def __init__(self):
        yaml_config = self.get_yaml_config()
        config = self.replace_missing_values_with_default(yaml_config)
        self.config = self.check_for_global_vars(config)
        self.parse_config_values()

    @staticmethod
    def get_yaml_config():
        try:
            with open('{}/config.yaml'.format(os.getcwd()), 'r') as stream:
                try:
                    return yaml.load(stream)
                except yaml.YAMLError:
                    return {'error': {}}
        except FileNotFoundError:
            return {'error': {}}

    @staticmethod
    def replace_missing_values_with_default(yaml_config):
        default_config =    {'other': {
                                'auth': True,
                                'verify_jwt_signature': True,
                                'app_client_id': None,
                                'app_client_secret': None,
                                'http_proxy': None,
                                'https_proxy': None,
                            }, 'celery': {
                                'broker_url': None,
                            }, 'flask': {
                                'host': '0.0.0.0',
                                'port': '5000',
                                'debug': False,
                            },
                                'redis': {
                                    'uri': None,
                            }}

        logger = logging.getLogger(__name__)

        for root, values in yaml_config.items():
            if root not in default_config:
                default_config[root] = {}
            for sub in values.keys():
                default_config[root][sub] = yaml_config[root][sub]
                logger.info('{}:{} loaded from yaml config'.format(root, sub))

        return default_config

    @staticmethod
    def check_for_global_vars(config):
        logger = logging.getLogger(__name__)

        for root, values in config.items():
            for sub in values.keys():
                if root == 'other':
                    env_key = sub.upper()
                else:
                    env_key = '{}_{}'.format(root, sub).upper()
                if env_key in os.environ:
                    config[root][sub] = os.environ[env_key]
                    logger.info('{}:{} loaded from global vars'.format(root, sub))
        return config

    def get_config(self, argument, config_name, root=None):
        # all config lives under the other section unless it is specific to
        # Flask, Celery or Redis
        if root is not None:
            config_section = self.config[root]
        else:
            config_section = self.config['other']

        # Check for argument - this simplifies the process of checking arguments
        if argument is not None:
            return argument
        else:
            if type(config_section[config_name.lower()]) is ValueError:
                raise config_section[config_name.lower()]
            else:
                return config_section[config_name.lower()]

    def get_section_config(self, section):
        return self.config[section]

    def parse_config_values(self):
        for root, values in self.config.items():
            for sub, value in values.items():
                if value == 'None':
                    self.config[root][sub] = None
                elif value == 'True':
                    self.config[root][sub] = True
                elif value == 'False':
                    self.config[root][sub] = False
                else:
                    try:
                        self.config[root][sub] = int(value)
                    except ValueError:
                        pass
                    except TypeError:
                        pass
