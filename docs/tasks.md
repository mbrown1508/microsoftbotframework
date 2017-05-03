# Defining Tasks
Every time a message is recieved all of the methods passed to the chatbot via the MsBot.add_process() method will be called.

## Base Definition
Every function is passed the message from Microsoft when it is called.
```python
def BaseTask(message):
    pass
```
## Example Definition
This will echo back all messages recieved. See details on the Response object below.
```python
def RespondToConversation(message):
    if message["type"]=="message":
        response = Response(message)
        response.reply_to_activity(message["text"])
```
