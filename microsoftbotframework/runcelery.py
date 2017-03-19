from flask import Flask
from celery import Celery
from.utils import get_celery_config


def make_celery(app, celery_config):

    celery = Celery(app.import_name, backend=celery_config['celery_result_backend'],
                    broker=celery_config['celery_broker_url'],
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


celery_config = get_celery_config()

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL=celery_config['celery_broker_url'],
    CELERY_RESULT_BACKEND=celery_config['celery_result_backend'],
    CELERY_REDIS_MAX_CONNECTIONS=15,
)

celery = make_celery(flask_app, celery_config)
