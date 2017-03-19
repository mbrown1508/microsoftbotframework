from configparser import ConfigParser
import os


# Used for everything but celery
def get_config(argument, environment_name, default):
    if argument is not None:
        return argument
    elif environment_name in os.environ:
        return os.environ[environment_name]
    else:
        if type(default) is ValueError:
            raise default
        else:
            return default


def config_section_map(section):
    config = ConfigParser()
    config.read('{}/config.ini'.format(os.getcwd()))
    if config.has_section(section):
        return {key: value for key, value in config[section].items()}
    else:
        return False


def get_celery_config():
    # Check for a config.ini
    if os.path.isfile('config.ini'):
        # check for a config.ini
        celery_config = config_section_map('CELERY')
        if celery_config and 'celery_broker_url' in celery_config and 'celery_result_backend' in celery_config:
            print('Celery using config.ini vars')
            return {
                'celery_broker_url': celery_config['celery_broker_url'],
                'celery_result_backend': celery_config['celery_result_backend']
            }
    # Check for a global vars
    if 'CELERY_BROKER_URL' in os.environ and 'CELERY_RESULT_BACKEND' in os.environ:
        print('Celery using global config vars')
        return {
            'celery_broker_url': os.environ['CELERY_BROKER_URL'],
            'celery_result_backend': os.environ['CELERY_RESULT_BACKEND']
        }
    # Load defaults
    print('Celery using default vars')
    return {
        'celery_broker_url': 'redis://localhost:6379',
        'celery_result_backend': 'redis://localhost:6379'
    }
