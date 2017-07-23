import datetime
from .response import Response


class Activity(Response):
    def __init__(self, **kwargs):
        self.defaults = {
            'action': None,
            'attachments': None,          # Attachment[]
            'attachmentLayout': None,
            'channelData': None,          # ChannelData object
            'channelId': None,
            'conversation': None,         # ConversationAccount object
            'entities': None,             # mentioned entities ie Mention or Place objects
            'fromAccount': None,          # ChannelAccount
            'historyDisclosed': None,
            'id': None,                   # ActivityId - may not be required in response?
            'inputHint': None,            # (acceptingInput, expectingInput, ignoringInput)
            'locale': None,               # <language>-<country>
            'localTimestamp': None,
            'membersAdded': None,         # This will be passed only in conversationUpdates
            'membersRemoved': None,       # This will be passed only in conversationUpdates
            'recipient': None,            # ChannelAccount
            'relatesTo': None,            # ConversationReferece - references a specific point in a convo
            'replyToId': None,            # Used to reply to a thread / specific activity.
            'serviceUrl': None,
            'speak': None,                # Text to be spoken
            'suggestedActions': None,
            'summary': None,              # A summary of information
            'text': None,                 # The text to be sent to a user
            'textFormat': None,           # [markdown, plain, xml]
            'timestamp': None,            # UTC
            'topicName': None,
            'type': 'message',                 # [contactRelationUpdate, conversationUpdate, deleteUserData, message, ping, typing, endOfConversation]
        }

        # Used to grab the activityId for responses
        self.activityId = None

        # Used in create Conversation - not is not required and will default to from
        self.isGroup = kwargs.pop('isGroup', False)
        self.members = kwargs.pop('members', None)
        self.bot = kwargs.pop('bot', None)

        for (prop, default) in self.defaults.items():
            prop_value = kwargs.pop(prop, '_notset')

            if prop_value is None:
                prop_value = '_None'
            elif prop_value == '_notset':
                prop_value = default

            setattr(self, prop, prop_value)

        fill = kwargs.pop('fill', None)
        reply_to_activity = kwargs.pop('reply_to_activity', None)
        if fill is not None and fill is not False:
            self.fill(fill, reply_to_activity)

        # Create timestamp
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")

        # A nicer way to set conversation = {"id": "asdfsdf"}
        self.conversationId = kwargs.pop('conversationId', None)
        if self.conversationId is not None and self.conversation is None:
            self.conversation = {"id": self.conversationId}

        if fill is not None and fill is not False and self.conversationId is None and 'id' in self.conversation:
            self.conversationId = self.conversation['id']
            
        # Set activityId if passed in args
        activityId_arg = kwargs.pop('activityId', None)
        if activityId_arg is not None:
            self.activityId = activityId_arg

        if activityId_arg is not None and self.id is None:
            self.id = self.activityId

        flip = kwargs.pop('flip', False if (fill is None or fill is False) else True)
        if flip:
            self.flip()

        self.cleanup_none()

        super(Activity, self).__init__(**kwargs)

    def cleanup_none(self):
        """
        Removes the temporary value set for None attributes.
        """
        for (prop, default) in self.defaults.items():
            if getattr(self, prop) == '_None':
                setattr(self, prop, None)

    def flip(self):
        recipient = self.recipient
        self.recipient = self.fromAccount
        self.fromAccount = recipient

    def fill(self, message, reply_to_activity=False):
        skip = ['timestamp', 'localTimestamp', 'entities', 'text', 'id', 'membersAdded', 'membersRemoved', 'attachments', 'channelData']
        for key, value in message.items():
            # in code from is called fromAccount, from is a reserved word (note from is still set)
            if key == 'from':
                if getattr(self, 'fromAccount') is None:
                    setattr(self, 'fromAccount', value)

            # set the activityId to id to make it easy to set in conversation operations.
            if key == 'id':
                if getattr(self, 'activityId') is None:
                    self.activityId = value

            # fill the remaining keys if they have not been set using defaults or arguments
            if key not in skip:
                if getattr(self, key, None) is None:
                    setattr(self, key, value)

            # We need to remove the slack channel data when posting back.
            if key == 'channelData':
                if getattr(self, 'channelData') is None:
                    if 'SlackMessage' in message['channelData']:
                        setattr(self, key, None)
                    else:
                        setattr(self, key, value)

        if reply_to_activity:
            self.replyToId = message['id']

    def to_dict(self):
        json = {}
        for key in self.defaults:
            attribute = getattr(self, key)
            if attribute is not None:
                if key == 'fromAccount':
                    json['from'] = attribute
                else:
                    json[key] = attribute
        return json
