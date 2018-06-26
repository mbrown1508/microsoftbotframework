from unittest import TestCase
from ..config import Config
from ..activity import Activity
import os
from ..cache import JsonCache
from ..state import JsonState


class ResponseTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def _clear_environ():
        os.environ = {}

    @staticmethod
    def _get_full_arg_activity(fill=False, reply_to_activity=False, flip=False):
        return Activity(
            action=None,
            attachments=[{'url': 'http://attachment'}],          # Attachment[]
            attachmentLayout='basic',
            channelData={'SkypeData': {}},          # ChannelData object
            channelId='asdfqwer',
            conversation={'id': 'asdfqwer'},         # ConversationAccount object
            entities=[{'id': 'fdsa'}],             # mentioned entities ie Mention or Place objects
            fromAccount={'id': 'asdf'},          # ChannelAccount
            historyDisclosed=False,
            id='1234',                   # ActivityId - may not be required in response?
            inputHint='acceptingInput',            # (acceptingInput, expectingInput, ignoringInput)
            locale='english-Australia',               # <language>-<country>
            localTimestamp='345:3245:2345',
            membersAdded=[{'id': 'lkjh'}],         # This will be passed only in conversationUpdates
            membersRemoved=[{'id': 'hjkl'}],       # This will be passed only in conversationUpdates
            recipient={'id': 'rtyu'},            # ChannelAccount
            relatesTo='asdffghj',            # ConversationReferece - references a specific point in a convo
            replyToId='asdfghjr',            # Used to reply to a thread / specific activity.
            serviceUrl='https://asdfqwer',
            speak='Hello',                # Text to be spoken
            suggestedActions='bite',
            summary='short',              # A summary of information
            text='The text',                 # The text to be sent to a user
            textFormat='plain',           # [markdown, plain, xml]
            timestamp='123:3245,5435',            # UTC
            topicName='Topic!!',
            type='message',                 # [contactRelationUpdate, conversationUpdate, deleteUserData, message, ping, typing, endOfConversation]
            activityId='12345',
            conversationId='123456',
            isGroup=False,
            members=[{'id': 'zxcv'}],
            bot=False,
            fill=fill,
            reply_to_activity=reply_to_activity,
            flip=flip,
        )

    @staticmethod
    def _get_full_message():
        return {
            'action': None,
            'attachments': [{'url': 'http://attachment'}],          # Attachment[]
            'attachmentLayout': 'basic',
            'channelData': {'SkypeData': {}},          # ChannelData object
            'channelId': 'asdfqwer',
            'conversation': {'id': 'asdfqwer'},         # ConversationAccount object
            'entities': [{'id': 'fdsa'}],             # mentioned entities ie Mention or Place objects
            'fromAccount': {'id': 'asdf'},          # ChannelAccount
            'historyDisclosed': False,
            'id': '1234',                   # ActivityId - may not be required in response?
            'inputHint': 'acceptingInput',            # (acceptingInput, expectingInput, ignoringInput)
            'locale': 'english-Australia',               # <language>-<country>
            'localTimestamp': '345:3245:2345',
            'membersAdded': [{'id': 'lkjh'}],         # This will be passed only in conversationUpdates
            'membersRemoved': [{'id': 'hjkl'}],       # This will be passed only in conversationUpdates
            'recipient': {'id': 'rtyu'},            # ChannelAccount
            'relatesTo': 'asdffghj',            # ConversationReferece - references a specific point in a convo
            'replyToId': 'asdfghjr',            # Used to reply to a thread / specific activity.
            'serviceUrl': 'https://asdfqwer',
            'speak': 'Hello',                # Text to be spoken
            'suggestedActions': 'bite',
            'summary': 'short',              # A summary of information
            'text': 'The text',                 # The text to be sent to a user
            'textFormat': 'plain',           # [markdown, plain, xml]
            'timestamp': '123:3245,5435',            # UTC
            'topicName': 'Topic!!',
            'type': 'message',                 # [contactRelationUpdate, conversationUpdate, deleteUserData, message, ping, typing, endOfConversation]
        }

    def test_valid_arguments(self):
        self._clear_environ()
        activity = self._get_full_arg_activity()

        self.assertEqual(activity.action, None)
        self.assertEqual(activity.attachments, [{'url': 'http://attachment'}])
        self.assertEqual(activity.attachmentLayout, 'basic')
        self.assertEqual(activity.channelData, {'SkypeData': {}})
        self.assertEqual(activity.channelId, 'asdfqwer')
        self.assertEqual(activity.conversation, {'id': 'asdfqwer'})
        self.assertEqual(activity.entities, [{'id': 'fdsa'}])
        self.assertEqual(activity.fromAccount, {'id': 'asdf'})
        self.assertEqual(activity.historyDisclosed, False)
        self.assertEqual(activity.id, '1234')
        self.assertEqual(activity.inputHint, 'acceptingInput')
        self.assertEqual(activity.locale, 'english-Australia')
        self.assertEqual(activity.localTimestamp, '345:3245:2345')
        self.assertEqual(activity.membersAdded, [{'id': 'lkjh'}])
        self.assertEqual(activity.membersRemoved, [{'id': 'hjkl'}])
        self.assertEqual(activity.recipient, {'id': 'rtyu'})
        self.assertEqual(activity.relatesTo, 'asdffghj')
        self.assertEqual(activity.replyToId, 'asdfghjr')
        self.assertEqual(activity.serviceUrl, 'https://asdfqwer')
        self.assertEqual(activity.speak, 'Hello')
        self.assertEqual(activity.suggestedActions, 'bite')
        self.assertEqual(activity.summary, 'short')
        self.assertEqual(activity.text, 'The text')
        self.assertEqual(activity.textFormat, 'plain')
        self.assertEqual(activity.timestamp, '123:3245,5435')
        self.assertEqual(activity.topicName, 'Topic!!')
        self.assertEqual(activity.type, 'message')

        self.assertEqual(activity.activityId, '12345')
        self.assertEqual(activity.conversationId, '123456')
        self.assertEqual(activity.isGroup, False)
        self.assertEqual(activity.members, [{'id': 'zxcv'}])
        self.assertEqual(activity.bot, False)

    def test_fill(self):
        self._clear_environ()
        activity = Activity(fill=self._get_full_message())

        # removes fields that can't be returned
        # flips from / recipient
        # sets timestamp
        # activityId = id
        # conversationId = conversation['id']

        self.assertEqual(activity.action, None)
        self.assertEqual(activity.attachments, None)
        self.assertEqual(activity.attachmentLayout, 'basic')
        self.assertEqual(activity.channelData, {'SkypeData': {}})
        self.assertEqual(activity.channelId, 'asdfqwer')
        self.assertEqual(activity.conversation, {'id': 'asdfqwer'})
        self.assertEqual(activity.entities, None)
        self.assertEqual(activity.fromAccount, {'id': 'rtyu'})
        self.assertEqual(activity.historyDisclosed, False)
        self.assertEqual(activity.id, None)
        self.assertEqual(activity.inputHint, 'acceptingInput')
        self.assertEqual(activity.locale, 'english-Australia')
        self.assertEqual(activity.membersAdded, None)
        self.assertEqual(activity.membersRemoved, None)
        self.assertEqual(activity.recipient, {'id': 'asdf'})
        self.assertEqual(activity.relatesTo, 'asdffghj')
        self.assertEqual(activity.replyToId, 'asdfghjr')
        self.assertEqual(activity.serviceUrl, 'https://asdfqwer')
        self.assertEqual(activity.speak, 'Hello')
        self.assertEqual(activity.suggestedActions, 'bite')
        self.assertEqual(activity.summary, 'short')
        self.assertEqual(activity.text, None)
        self.assertEqual(activity.textFormat, 'plain')
        self.assertIsNotNone(activity.timestamp)
        self.assertEqual(activity.topicName, 'Topic!!')
        self.assertEqual(activity.type, 'message')

        self.assertEqual(activity.activityId, '1234')
        self.assertEqual(activity.conversationId, 'asdfqwer')
        self.assertEqual(activity.isGroup, False)
        self.assertEqual(activity.members, None)
        self.assertEqual(activity.bot, None)

    def test_fill_flip_false(self):
        self._clear_environ()
        activity = Activity(fill=self._get_full_message(), flip=False)

        # removes fields that can't be returned
        # flips from / recipient
        # sets timestamp
        # activityId = id
        # conversationId = conversation['id']

        self.assertEqual(activity.action, None)
        self.assertEqual(activity.attachments, None)
        self.assertEqual(activity.attachmentLayout, 'basic')
        self.assertEqual(activity.channelData, {'SkypeData': {}})
        self.assertEqual(activity.channelId, 'asdfqwer')
        self.assertEqual(activity.conversation, {'id': 'asdfqwer'})
        self.assertEqual(activity.entities, None)
        self.assertEqual(activity.fromAccount, {'id': 'asdf'})
        self.assertEqual(activity.historyDisclosed, False)
        self.assertEqual(activity.id, None)
        self.assertEqual(activity.inputHint, 'acceptingInput')
        self.assertEqual(activity.locale, 'english-Australia')
        self.assertEqual(activity.membersAdded, None)
        self.assertEqual(activity.membersRemoved, None)
        self.assertEqual(activity.recipient, {'id': 'rtyu'})
        self.assertEqual(activity.relatesTo, 'asdffghj')
        self.assertEqual(activity.replyToId, 'asdfghjr')
        self.assertEqual(activity.serviceUrl, 'https://asdfqwer')
        self.assertEqual(activity.speak, 'Hello')
        self.assertEqual(activity.suggestedActions, 'bite')
        self.assertEqual(activity.summary, 'short')
        self.assertEqual(activity.text, None)
        self.assertEqual(activity.textFormat, 'plain')
        self.assertIsNotNone(activity.timestamp)
        self.assertEqual(activity.topicName, 'Topic!!')
        self.assertEqual(activity.type, 'message')

        self.assertEqual(activity.activityId, '1234')
        self.assertEqual(activity.conversationId, 'asdfqwer')
        self.assertEqual(activity.isGroup, False)
        self.assertEqual(activity.members, None)
        self.assertEqual(activity.bot, None)

    def test_none(self):
        activity = Activity(
            action=None,
            attachments=None,          # Attachment[]
            attachmentLayout=None,
            channelData=None,          # ChannelData object
            channelId=None,
            conversation=None,         # ConversationAccount object
            fill=self._get_full_message()
        )

        self.assertEqual(activity.action, None)
        self.assertEqual(activity.attachments, None)
        self.assertEqual(activity.attachmentLayout, None)
        self.assertEqual(activity.channelData, None)
        self.assertEqual(activity.channelId, None)
        self.assertEqual(activity.conversation, None)

    def test_slack_channel_data(self):
        self._clear_environ()
        full_message = self._get_full_message()
        full_message['channelData'] = {'SlackMessage': {'from': 'Person', 'to': 'Someone'}}
        activity = Activity(fill=full_message)

        self.assertEqual(activity.action, None)
        self.assertEqual(activity.attachments, None)
        self.assertEqual(activity.attachmentLayout, 'basic')
        self.assertEqual(activity.channelData, None)
        self.assertEqual(activity.channelId, 'asdfqwer')
        self.assertEqual(activity.conversation, {'id': 'asdfqwer'})

    def test_reply_to_activity(self):
        self._clear_environ()
        activity = Activity(fill=self._get_full_message(), reply_to_activity=True)

        self.assertEqual(activity.channelId, 'asdfqwer')
        self.assertEqual(activity.conversation, {'id': 'asdfqwer'})
        self.assertEqual(activity.fromAccount, {'id': 'rtyu'})
        self.assertEqual(activity.id, None)
        self.assertEqual(activity.recipient, {'id': 'asdf'})
        self.assertEqual(activity.relatesTo, 'asdffghj')
        self.assertEqual(activity.text, None)
        self.assertEqual(activity.conversationId, 'asdfqwer')

        self.assertEqual(activity.replyToId, '1234')
        self.assertEqual(activity.activityId, '1234')

    def test_message_type_default(self):
        self._clear_environ()
        full_message = self._get_full_message()
        full_message['type'] = 'somethingElse'
        activity = Activity(fill=full_message)

        self.assertEqual(activity.type, 'message')

    def test_message_set_type(self):
        self._clear_environ()
        activity = Activity(fill=self._get_full_message(),
                            type='markdown')

        self.assertEqual(activity.type, 'markdown')

    def test_to_dict(self):
        expected_dict =  {'attachmentLayout': 'basic',
                          'channelData': {'SkypeData': {}},
                          'channelId': 'asdfqwer',
                          'conversation': {'id': 'asdfqwer'},
                          'from': {'id': 'rtyu'},
                          'historyDisclosed': False,
                          'inputHint': 'acceptingInput',
                          'locale': 'english-Australia',
                          'recipient': {'id': 'asdf'},
                          'relatesTo': 'asdffghj',
                          'replyToId': 'asdfghjr',
                          'serviceUrl': 'https://asdfqwer',
                          'speak': 'Hello',
                          'suggestedActions': 'bite',
                          'summary': 'short',
                          'text': 'Hey',
                          'textFormat': 'plain',
                          'timestamp': None,
                          'topicName': 'Topic!!',
                          'type': 'markdown'}

        self._clear_environ()
        activity = Activity(fill=self._get_full_message(),
                            type='markdown',
                            text='Hey')

        result_dict = activity.to_dict()
        result_dict['timestamp'] = None

        self.assertEqual(result_dict, expected_dict)

    def test_timestamp(self):
        self._clear_environ()
        activity = Activity()
        self.assertEqual(len(activity.timestamp), 27)
