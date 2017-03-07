from flask import Flask
from celery import Celery
from microsoftbotframework.helpers import ConfigSectionMap

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'],
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
config = ConfigSectionMap('CELERY')
flask_app.config.update(
    CELERY_BROKER_URL=config['celery_broker_url'],
    CELERY_RESULT_BACKEND=config['celery_result_backend']
)
config = None

celery = make_celery(flask_app)