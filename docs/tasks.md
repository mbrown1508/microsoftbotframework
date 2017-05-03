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
