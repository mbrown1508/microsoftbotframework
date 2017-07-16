import os
import yaml
import logging


class Config:
    def __init__(self, config_location=None):
        self.logger = logging.getLogger(__name__)

        default_config = self._get_default_config()
        yaml_config = self._get_yaml_config(config_location)
        environment_vars = os.environ

        config = self._replace_with_yaml_config(default_config, yaml_config)
        self.config = self._replace_with_environment_vars(config, environment_vars)

        self._parse_config_values()

    @staticmethod
    def _get_default_config():
        return {'other': {
                    'auth': True,
                    'verify_jwt_signature': True,
                    'app_client_id': None,
                    'app_client_secret': None,
                    'http_proxy': None,
                    'https_proxy': None,
                    'cache': 'JsonCache',
                    'state': None,
                }, 'celery': {
                    'broker_url': None,
                }, 'flask': {
                    'host': '0.0.0.0',
                    'port': '5000',
                    'debug': False,
                }, 'redis': {
                    'uri': None,
                }, 'mongodb': {
                    'uri': None,
                    'database': 'microsoftbotframework',
                }}

    def _get_yaml_config(self, config_location):
        if config_location is not None:
            self.config_location = config_location
        else:
            self.config_location = '{}/config.yaml'.format(os.getcwd())

        try:
            with open(self.config_location, 'r') as stream:
                try:
                    yaml_config = yaml.load(stream)
                    for root, values in yaml_config.items():
                        try:
                            values.keys()
                        except:
                            raise (Exception('All config values have to be in a parent value. \
                                            Default values are [\'mongodb\', \'flask\', \'celery\', \'redis\', \'other\']'))
                    return yaml_config
                except yaml.YAMLError:
                    raise(Exception('There was a error parsing the config.yaml YAML file.'))
        except FileNotFoundError:
            self.logger.warning('There was no YAML file found. \
                                 If you have a config.yaml file make sure it is in the working directory and try again.')
            return {}

    def _replace_with_yaml_config(self, default_config, yaml_config):
        for root, values in yaml_config.items():
            if root not in default_config:
                default_config[root] = {}
            for sub in values.keys():
                default_config[root][sub] = yaml_config[root][sub]
                self.logger.info('{}:{} loaded from yaml config'.format(root, sub))

        return default_config

    def _replace_with_environment_vars(self, config, environment_vars):
        for root, values in config.items():
            for sub in values.keys():
                if root == 'other':
                    env_key = sub.upper()
                else:
                    env_key = '{}_{}'.format(root, sub).upper()
                if env_key in environment_vars:
                    config[root][sub] = environment_vars[env_key]
                    self.logger.info('{}:{} loaded from global vars'.format(root, sub))

        sutable_fields = ['OTHER', 'FLASK', 'CELERY', 'REDIS']
        for env_key in environment_vars:
            split_key = env_key.split('_')
            if split_key[0] in sutable_fields:
                if split_key[0].lower() not in config:
                    config[split_key[0].lower()] = {}

                config[split_key[0].lower()]['_'.join(split_key[1:]).lower()] = environment_vars[env_key]

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

    def _parse_config_values(self):
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
