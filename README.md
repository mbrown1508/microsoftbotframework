# Microsoft Bot Framework
Microsoft Bot Framework is a wrapper for the Microsoft Bot API by Microsoft. It uses Flask to recieve the post messages from microsoft and Celery to complete Async tasks.

The goal was to create a really simple to use library to enable you to interface with the microsoft bot framework.

## To run this app using the local simulator

Download and run the simulator from: https://docs.botframework.com/en-us/tools/bot-framework-emulator/

Install the library and run main.py

```
pip install microsoftbotframework
python main.py
```
By default the app runs at http://localhost:5000/api/messages.

Enter this address in the *Enter your endpoint URL* header of the emulator.

Start chatting! The frameowrk by default will act like a parrot and repeat everything you type.

## To run this app using the online bot framework
Install package using pip. We need to use the master branch of PyJwt as it has methods we need to use to verify the jwt token signature.
```sh
pip install microsoftbotframework
```
Create a Microsoft Chatbot | https://dev.botframework.com/bots. Generate 'Microsoft App ID' and 'Microsoft App Secret'. You will need to pass this to the response object (overview below) or you can set it as a global var (recommended) as below.
```
export APP_CLIENT_ID=<Microsoft App ID>
export APP_CLIENT_SECRET=<Microsoft App Secret>
```
or place them in the config.yaml file
```
other:
    app_client_id: <Microsoft App ID>
    app_client_secret: <Microsoft App Secret>
```


## Basic usage
```Python
# Create the MsBot object
bot = MsBot()
# Add processes (methods) to be executed when a message is recieved.
bot.add_process(echo_response)
# Start the webserver
bot.run()
```
This will start a server running on localhost, port 5000.
## Process Definition
Every time a message is recieved all of the methods passed to the chatbot via the MsBot.add_process() method will be called.
#### Base Definition
Every function is passed the message from Microsoft when it is called.
```python
def BaseTask(message):
    pass
```
#### Example Definition
This will echo back all messages recieved. See details on the Response object below.
```python
def RespondToConversation(message):
    if message["type"]=="message":
        response = Response(message)
        message_response = message["text"]
        response.reply_to_activity(message_response)
```
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
#### Enable Cryptography
This is a optional requriement as it can be hard to install the crpytography library
```sh
pip install git+git://github.com/jpadilla/pyjwt@master
pip isntall cryptography
```
