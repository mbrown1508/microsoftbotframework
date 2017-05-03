##### Configure Async Tasks
Note: I have only successfully tested async tasks on Linux.

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
## The Response Object
The response object is created by passing it the message recieved and then calling Response.reply_to_activity(message).
```python
response = Response(message)
response.reply_to_activity('This is my response.')
```
You don't have to pass the message to the Response object but you will have to set all of the required vars before you respond to microsoft.

If you haven't added 'Microsoft App ID' and 'Microsoft App Secret' to the global vars you will have to pass them to the response as follows.
```python
response = Response(message, microsoft_app_id='Microsoft App ID', microsoft_app_secret='Microsoft App Secret')
response.reply_to_activity('This is my response.')
```
## Configuration
Additional configuration can be passed to celery and redis (flask comming soon) by setting them in the config.yaml as follows.
```
celery:
    result_backend: redis://localhost:6379
    broker_url: redis://localhost:6379
    broker_pool_limit: None
redis:

```
