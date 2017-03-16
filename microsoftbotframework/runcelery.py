from flask import Flask
from celery import Celery
import os


def make_celery(app):
    celery = Celery(app.import_name, backend=os.environ['CELERY_RESULT_BACKEND'],
                    broker=os.environ['CELERY_BROKER_URL'],
                    include=['tasks'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL=os.environ['CELERY_BROKER_URL'],
    CELERY_RESULT_BACKEND=os.environ['CELERY_RESULT_BACKEND'],
    CELERY_REDIS_MAX_CONNECTIONS=15,
)

celery = make_celery(flask_app)
