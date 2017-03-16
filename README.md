# Microsoft Bot Framework
Microsoft Bot Framework is a wrapper for the Microsoft Bot API by Microsoft. It uses Flask to recieve the post messages from microsoft and Celery to complete Async tasks.

The goal was to create a really simple to use library to enable you to interface with the microsoft bot framework.

## To run this app
Create a Microsoft Chatbot | https://dev.botframework.com/bots. Generate <Microsoft App ID> and <Microsoft App Secret> then add them to the evironment vars.
```
export APP_CLIENT_ID=<Microsoft App ID>
export APP_CLIENT_SECRET=<Microsoft App Secret>
```
Also set the environment (PROD or DEV)
```
export ENVIRONMENT=PROD
```
Install required packages using pip
```sh
pip install requirements.txt
```
To start the server run python main.py
##### Configure Async Tasks
Add the broker-url and result-backend uri to the environment vars
```
export CELERY_BROKER_URL=redis://localhost:6379
export CELERY_RESULT_BACKEND=redis://localhost:6379
```
To use celery install and configure celery and its backend and run
```sh
celery -A microsoftbotframework.runcelery.celery worker --loglevel=info
```
    
## Configure
Every time a message is recieved all of the methods passed to the chatbot via the MsBot.add_process() method will be called.
#### Base Definition
Every function is passed the message from Microsoft when it is called.
```python
def BaseTask(message):
    pass
```
#### Example Definition
This will echo back all messages recieved.
```python
def RespondToConversation(message):
    if message["type"]=="message":
        response = Response(message)
        message_response = message["text"]
        response.reply_to_activity(message_response)
```
#### Async Definition
This method will be executed asynchronously. Several Celery decorators are available, check the documentation.
```python
@celery.task()
def AsyncTask(message):
    sleep(10)
```
