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
In order to interact with the Microsoft bot framework you need to have a internet facing https endpoint with a valid certificate. I personally use Heroku to host my bot as it is free and simple to use so I will show how I set it up there but you can host it anywhere as long as you meet the above criteria.

#### Create a Microsoft Chatbot
Go to https://dev.botframework.com/bots. Register a bot and generate a 'Microsoft App ID' and 'Microsoft App Secret'. Don't worry about the messaging endpoint as we will create that soon. Create a config.yaml file in the root of your project and place the following information:
```yaml
other:
    app_client_id: <Microsoft App ID>
    app_client_secret: <Microsoft App Secret>
```
#### Publish to Heroku
Create a file called "Procfile" and add the following.
```
web: python main.py
```

Create a file called requirements.txt and add the following.
```
microsoftbotframework
```

Create a file called runtime.txt and add the following.
```
python-3.6.0
```

Modify main.py to add set the port argument to the environment variable PORT.
``` python
from microsoftbotframework import MsBot
from tasks import *
import os

bot = MsBot(port=int(os.environ['PORT']))
bot.add_process(echo_response)
bot.run()
```

If you haven't yet install git
``` sh
sudo apt-get install git
```

Signup for a Heroku account here: https://www.heroku.com/ and create a new app. Follow the instructions to Deploy using Heroku Git

Go back into the Microsoft MyBots tab and update the Messaging Endpoint to be the Domain found in the Heroku settings tab. Make sure you add "/api/messages" at the of the url.

Congratulations you should now be able to chat to your bot on Skype!
