# Defining Tasks
Every time a message is recieved all of the methods passed to the chatbot via the MsBot.add_process() method will be called.

## Base Definition
Every function is passed the message from Microsoft when it is called.
```python
def BaseTask(message):
    pass
```
## Example Definition
This will echo back all messages recieved. For more information on ReplyToActivity see conversation operations.
```python
def echo_response(message):
    if message["type"] == "message":
        ReplyToActivity(fill=message,
                        text=message["text"]).send()
```
