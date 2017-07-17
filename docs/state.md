# State
There are currently 2 state adapters available in the library:
* JsonState
* MongodbState
* Microsoft Bot Framework API (comming soon)

## Installation
#####JsonState
JsonState requires write privileges to the working directory or the configured directory.

#####MongodbState 
MongodbState requires a working Mongodb Database. See the following url for a good guide on installing. https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/. If using Heroku you can also the resources to add "mLab MongoDB :: Mongodb, Sandbox".

In addition the pymongo library is required. It can be installed with the following command.

```text
pip install pymongo
```

## Conversation tracking
The MsBot and Response can be setup to save all incoming and outgoing conversations. By default this is disabled.

This can be configured in 4 ways.

#####Inline string arguments
```python
bot = MsBot(state='MongodbState')

activity_members = GetActivityMembers(conversationId="asdfwetjerjbbvwre",
                                      activityId="asdkbuaeniouhrvqeoruih",
                                      state="MongodbState").send()
```

#####Inline object arguments
```python
config = Config()
bot = MsBot(state=MongodbState(config))
```

This allows you to build your own State objects using the same API by extending the State Abstract Class

#####config.yaml
```yaml
other:
    state: JsonState   # state to use
    database: statedatabase     # defaults to microsoft bot framework
```

#####Environment variables
```sh
# in linux
export STATE=JsonState
```

##Get Conversation Tracking
You can get the saved conversation as follows.
* count is the number of records to return, default 10
* conversation_id will only get records regarding to that conversation, default all
* simple will respond with an array of the text strings from the activities rather than the whole activities.
```python
json_state = JsonState()
json_state.get_activities(self, count=10, conversation_id=None, simple=False)
```


## Configuring State Objects
objects can be configured in 3 ways
#####inline arguments
```python
bot = MsBot(state=RedisCache(config))

bot = MsBot(state=JsonCache('cache.json'))
```

#####config.yaml (Mongodb Only)
```yaml
mongodb:
    uri: mongodb://127.0.0.1:27017
```

#####environment variables (Mongodb Only)
```sh
# in linux
export MONGODB_URI=redis://localhost:6379
```

## State Objects
To access state create a state object as follows:
```python
mongodb_state = MongodbState(config=Config())
json_state = JsonState()
```

You can set, get and state against a few combinations of:
* channel
* conversation_id
* user_id

values should be a dictionary of values.

```python
json_state = JsonState()

values = {'name': 'Sam', 'age': 23}

json_state.set_user_data_on_channel(values, channel, user_id)
json_state.set_conversation_data_on_channel(values, channel, conversation_id)
json_state.set_private_conversation_data_on_channel(values, channel, conversation_id, user_id)
json_state.set_user_data(values, user_id)
json_state.set_channel_data(values, channel)

json_state.get_user_data_on_channel(channel, user_id)
json_state.get_conversation_data_on_channel(channel, conversation_id)
json_state.get_private_conversation_data_on_channel(channel, conversation_id, user_id)
json_state.get_user_data(user_id)
json_state.get_channel_data(channel)

json_state.delete_user_data_on_channel(channel, user_id)
json_state.delete_conversation_data_on_channel(channel, conversation_id)
json_state.delete_private_conversation_data_on_channel(channel, conversation_id, user_id)
json_state.delete_user_data(user_id)
json_state.delete_channel_data(channel)

# Deletes all state on a channel for a user
json_state.delete_state_for_user(channel, user_id)
```

All methods also have a fill argument which will autofill the 3 required fields if passed a message.
```python
json_state = JsonState()
json_state.set_user_data_on_channel(values, fill=message)
```

When using the fill method you can also pass bot=True to use the bots id as the user_id
```python
json_state = JsonState()
json_state.set_user_data_on_channel(values, fill=message, bot=True)
```
