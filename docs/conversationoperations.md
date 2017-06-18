# Conversation Operations
Once you recieve a message from the microsoft bot api you will want to respond using one of the following objects depending on what operation you want to perform.

* Create Conversation - Creates a new conversation.
* Send to Conversation - Sends an activity (message) to the end of the specified conversation.
* Reply to Activity - Sends an activity (message) to the specified conversation, as a reply to the specified activity.
* Get Conversation Members - Gets the members of the specified conversation.
* Get Activity Members - Gets the members of the specified activity within the specified conversation.
* Update Activity (Not Implemented) - Updates an existing activity.
* Delete Activity - Deletes an existing activity.
* Upload Attachment to Channel (Not Implemented) - Uploads an attachment directly into a channel's blob storage.

These operations come from https://docs.microsoft.com/en-us/bot-framework/rest-api/bot-framework-rest-connector-api-reference/ and more will be implemented in time.
 
Every Conversation Operation has a send() method that is called to send the message back to the Microsoft Bot API.


## Activity Object
All of the conversation operations extend the Activity object. The Activity object itself extends the Response Object. See http://microsoftbotframework.readthedocs.io/en/latest/response/ for more details on the arguments accepted.

The activity has all of the arguments listed here under Activity Object with the addition of the following arguments. https://docs.microsoft.com/en-us/bot-framework/rest-api/bot-framework-rest-connector-api-reference#activity-object . The only exception is the from argument which has been renamed to fromAccount due to reserved keywords.

* fill - You can pass the message object in the task declaration to fill and it will attempt to fill all of the fields it can. ie channelData which is the same in the response and the message you recieve.
* flip (default True) - If fill is not None then flip will swap the recipient and fromAccount variables which is useful when replying to activity or responding to a conversation.
  

## SendToConversation
This example:

* Prefills all fields possible by passing the message to the constructor.
* Sets the conversation id to jg3alifjua8sdljn9abiuao4ihbimroivb
* Sends the text 'How are you today?'

The send() method is called at the end to post the message to the service. 

```python
send_to_conversation = SendToConversation(fill=message,
                                          conversationId='jg3alifjua8sdljn9abiuao4ihbimroivb',
                                          text='How are you today?').send()
```

## ReplyToActivity
This example:

* Prefills all fields possible by passing the message to the constructor.
* Responds with the text 'I am good thanks.'

The send() method is called at the end to post the message to the service. 

```python
ReplyToActivity(fill=message,
                text='I am good thanks.').send()
```

## CreateConversation
The createConversation object has 4 additional arguments:

* isGroup - Flag to indicate whether or not this is a group conversation. Set to true if this is a group conversation; otherwise, false. The default is false. To start a group conversation, the channel must support group conversations. Defaults to False.
* bot - a json object with the id and name of the bot.
* members - Array of ChannelAccount objects that identify the members of the conversation. This list must contain a single user unless isGroup is set to true. This list may include other bots.
* topicName - Title of the conversation.

This example:

* Prefills the bot field using fill
* Sets a single member for the conversation.
* Sets the topicName and text for the first message to the conversation.

```python
response_info = CreateConversation(fill=message,
                                   members=[{"id": "l0skjasdkfjkjlshdyvoiunbqiewur"}],
                                   topicName='Starting a conversation',
                                   text='Lets have a conversation').send()
```

## DeleteActivity
Note: The delete activity doesn't seem to work on many platforms. I have been unable to test the functionality successfully.

This example:

* Replys to a activity and stores the response information which includes the activityId
* Prefills the DeleteActivity object
* Sets the activityId to delete

```python
response_info = ReplyToActivity(fill=message,
                                text='I am good thanks.').send()

DeleteActivity(fill=message,
               activityId=response_info.json()['id']).send()
```

## GetConversationMembers and GetActivityMembers
Both work much as described. The only fields required are conversationId and activityId accordingly.

```python
activity_members = GetActivityMembers(conversationId="asdfwetjerjbbvwre",
                                      activityId="asdkbuaeniouhrvqeoruih").send()
```