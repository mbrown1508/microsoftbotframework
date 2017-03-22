from configparser import ConfigParser
import os
import yaml


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
                                'app_client_id': None,
                                'app_client_secret': None,
                            }, 'celery': {
                                'celery_broker_url': None,
                            }, 'flask': {
                                'host': '0.0.0.0',
                                'port': '5000',
                            },
                                'redis': {
                                    'uri': None,
                            }}

        for root, values in yaml_config.items():
            if root not in default_config:
                default_config[root] = {}
            for sub in values.keys():
                default_config[root][sub] = yaml_config[root][sub]

        return default_config

    @staticmethod
    def check_for_global_vars(config):
        for root, values in config.items():
            for sub in values.keys():
                if root == 'other':
                    env_key = sub.upper()
                else:
                    env_key = '{}_{}'.format(root, sub).upper()
                if env_key in os.environ:
                    config[root][sub] = os.environ[env_key]
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
