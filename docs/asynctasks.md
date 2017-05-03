##### Configure Async Tasks
Note: Async tasks will not work on windows as

You will have to setup a celery backend, I personally use redis but rabbitmq should work as well. I good guide to setting up reddis on Ubuntu can be found here https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04.

Add the broker-url and result-backend uri to the environment vars. The default values are for a redis backend.
```
export CELERY_BROKER_URL=redis://localhost:6379
export CELERY_RESULT_BACKEND=redis://localhost:6379
```
or you can use a config.yaml file with the following information
```
celery:
    result_backend: redis://localhost:6379
    broker_url: redis://localhost:6379
```
to start celery run the following command.
```sh
celery -A microsoftbotframework.runcelery.celery worker --loglevel=info
```
#### Async Definition
This method will be executed asynchronously. Several Celery decorators are available, check the documentation.
```python
@celery.task()
def AsyncTask(message):
    sleep(10)
```
