from flask import Flask
from celery import Celery
from .config import Config


def make_celery(app, config):
    celery = Celery(app.import_name,
                    broker=config['broker_url'],
                    include=['tasks'])
    celery.conf.update(app.config)
    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


config = Config().get_section_config('celery')

flask_app = Flask(__name__)

for key, value in config.items():
    flask_app.config[key.upper()] = value

celery = make_celery(flask_app, config)
