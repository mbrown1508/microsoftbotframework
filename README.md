# Microsoft Bot Framework
Microsoft Bot Framework is a wrapper for the Microsoft Bot API by Microsoft. It uses Flask to recieve the post messages from Microsoft and Celery to complete Async tasks.

The goal was to create a really simple to use library to enable you to interface with the Microsoft bot framework.

Full Docs can be found here: http://microsoftbotframework.readthedocs.io/

## To run this app using the local simulator

Download and run the simulator from: https://docs.botframework.com/en-us/tools/bot-framework-emulator/

#### Install the library
```
pip install microsoftbotframework
```
#### Define a task
Create a file in the root directory called tasks.py. In the file define a task as follows.
More information on the ReplyToActivity object and others can be found at http://microsoftbotframework.readthedocs.io/en/latest/conversationoperations/
``` python
from microsoftbotframework import ReplyToActivity

def echo_response(message):
    if message["type"] == "message":
        ReplyToActivity(fill=message,
                        text=message["text"]).send()
```

#### Create the main file
``` python
from microsoftbotframework import MsBot
from tasks import *

bot = MsBot()
bot.add_process(echo_response)

if __name__ == '__main__':
    bot.run()
```

#### Run your app
```
python main.py
```

#### Connect to your bot
By default the app runs at http://localhost:5000/api/messages.

Enter this address in the *Enter your endpoint URL* header of the emulator.

Start chatting! If you followed the above instructions it should repeat back what you type in.

## To run this app using the online bot framework
In order to interact with the Microsoft bot framework you need to have a internet facing https endpoint with a valid certificate. This guide will show how to use gunicorn and heroku to host the application but you can easily use any wsgi hosting option as the MsBot object extends Flask.

#### Create a Microsoft Chatbot
Go to https://dev.botframework.com/bots. Register a bot and generate a 'Microsoft App ID' and 'Microsoft App Secret'. Don't worry about the messaging endpoint as we will create that soon. Create a config.yaml file in the root of your project and place the following information:
```yaml
other:
    app_client_id: <Microsoft App ID>
    app_client_secret: <Microsoft App Secret>
```
#### Publish to Heroku
Create a file called requirements.txt and add the following.
```
microsoftbotframework
gunicorn
```

Create a file called "Procfile" and add the following. We are going to use gunicorn as our web server. You can remove "--log-level INFO" or set it to a lower level for production.
```
web: gunicorn -b '0.0.0.0:'$PORT --log-level INFO main:bot
```

Create a file called runtime.txt and add the following.
```
python-3.6.0
```

If you haven't yet install git
``` sh
sudo apt-get install git
```

Signup for a Heroku account here: https://www.heroku.com/ and create a new app. Follow the instructions to Deploy using Heroku Git

Go back into the Microsoft MyBots tab and update the Messaging Endpoint to be the Domain found in the Heroku settings tab. Make sure you add "/api/messages" at the of the url.

Congratulations you should now be able to chat to your bot on Skype!

### Running this library's tests
1. Make sure that you have the required libraries installed from setup.py tests_require section with `pip install -e .[test]`
2. Make sure redis and mongodb are installed locally
3. Turn on redis: `redis-server`
4. Turn on mongobd: `mongod`
5. Open a terminal in the root of this directory
6. Run the tests with one of the below options
    - `nosetests` (requires step 1 libraries to be installed)
    - `python setup.py test` (doesn't require step 1 libraries to be installed)
