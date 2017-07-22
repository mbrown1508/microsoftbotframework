from unittest import TestCase
from ..config import Config
from ..state import JsonState, MongodbState
from pymongo import MongoClient
import os
from random import choice

USER1 = '29:1SPw4GoUNGtDmuYex45S13g-1zgri1qp43uA345yjSFc'
USER2 = '29:1SPw4GoUNGtDmuYex45S13g-1zgri1qp43uA547yjSFc'
CHANNEL1 = 'skype'
CHANNEL2 = 'teams'
CONVERSATION1 = "29:123w4GoUNGtDmuYexhNS13g-1zgri1qp43uA3A0yjSFc"
CONVERSATION2 = "29:567w4GoUNGtDmuYexhNS13g-1zgri1qp43uA3A0yjSFc"

BOT = "28:5e21d7a8-d1b5-4534-a63d-f521712f5a64"

MESSAGE = {"text": "image", "type": "message", "timestamp": "2017-07-13T12:34:48.338Z", "id": "149993456252",
           "channelId": "skype", "serviceUrl": "https://smba.trafficmanager.net/apis/",
           "from": {"id": "29:1SPw4GoUNGtDmuYex45S13g-1zgri1qp43uA345yjSFc", "name": "Matthew Brown"},
           "conversation": {"id": "29:123w4GoUNGtDmuYexhNS13g-1zgri1qp43uA3A0yjSFc"},
           "recipient": {"id": "28:5e21d7a8-d1b5-4534-a63d-f521712f5a64", "name": "TestPythonBotFramework"},
           "entities": [{"locale": "en-US", "country": "AU", "platform": "Web", "type": "clientInfo"}],
           "channelData": {"text": "image"}}

NAME_VALUES1 = {'name': 'Sally'}
NAME_VALUES2 = {'name': 'Rachel'}
AGE_VALUES1 = {'age': 34}
AGE_VALUES2 = {'age': 24}
CAR_VALUES1 = {'car': 'truck'}
CAR_VALUES2 = {'car': 'train'}
MULTI_NAMES1 = {'car': 'truck', 'name': 'Sally'}
MULTI_NAMES2 = {'car': 'corolla', 'name': 'Sam'}
MULTI_AGES1 = {'age': 45, 'house_age': 73}
MULTI_AGES2 = {'age': 23, 'house_age': 45}
MULTI_CARS1 = {'car': 'truck', 'type': 'mack'}
MULTI_CARS2 = {'car': 'jeep', 'type': '4wd'}
DELETE_CAR = {'car': None}
DELETE_AGE = {'age': None}
DELETE_NAME = {'name': None}
DELETE_MULTI_NAMES = {'car': None, 'name': None}
DELETE_MULTI_AGES = {'age': None, 'house_age': None}
DELETE_MULTI_CARS = {'car': None, 'type': None}
DELETED_NAME1 = {'car': 'truck'}
DELETED_NAME2 = {'car': 'corolla'}
DELETED_CAR1 = {'type': 'mack'}
DELETED_CAR2 = {'type': '4wd'}
DELETED_AGE1 = {'house_age': 73}
DELETED_AGE2 = {'house_age': 45}


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


class JsonStateTestCase(TestCase):
    def setUp(self):
        self._remove_files()
        self.state = JsonState(state_file='teststate.json', conversation_file='testconversation.json')

    def tearDown(self):
        pass
        self._remove_files()

    def _remove_files(self):
        try:
            os.remove(os.getcwd() + '/teststate.json')
        except OSError:
            pass

        try:
            os.remove(os.getcwd() + '/testconversation.json')
        except OSError:
            pass

    def test_set_key_1(self):
        self.assertEqual(self.state.set_user_data_on_channel(NAME_VALUES1, channel=CHANNEL1, user_id=USER1),
                         NAME_VALUES1)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), NAME_VALUES1)

    def test_set_key_2(self):
        self.assertEqual(self.state.set_conversation_data_on_channel(NAME_VALUES2, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), NAME_VALUES2)
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            NAME_VALUES2)

    def test_set_key_3(self):
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(AGE_VALUES1, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), AGE_VALUES1)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         AGE_VALUES1)

    def test_set_key_4(self):
        self.assertEqual(self.state.set_user_data(AGE_VALUES2, user_id=USER1), AGE_VALUES2)
        self.assertEqual(self.state.get_user_data(user_id=USER1), AGE_VALUES2)

    def test_set_key_5(self):
        self.assertEqual(self.state.set_channel_data(CAR_VALUES1, channel=CHANNEL1), CAR_VALUES1)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), CAR_VALUES1)

    def test_update_key1(self):
        self.state.set_user_data_on_channel(NAME_VALUES1, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(NAME_VALUES2, channel=CHANNEL1, user_id=USER1),
                         NAME_VALUES2)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), NAME_VALUES2)

    def test_update_key2(self):
        self.state.set_conversation_data_on_channel(NAME_VALUES2, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(NAME_VALUES1, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), NAME_VALUES1)
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            NAME_VALUES1)

    def test_update_key3(self):
        self.state.set_private_conversation_data_on_channel(AGE_VALUES1, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(AGE_VALUES2, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), AGE_VALUES2)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         AGE_VALUES2)

    def test_update_key4(self):
        self.state.set_user_data(AGE_VALUES2, user_id=USER1)
        self.assertEqual(self.state.set_user_data(AGE_VALUES1, user_id=USER1), AGE_VALUES1)
        self.assertEqual(self.state.get_user_data(user_id=USER1), AGE_VALUES1)

    def test_update_key5(self):
        self.state.set_channel_data(CAR_VALUES1, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(CAR_VALUES2, channel=CHANNEL1), CAR_VALUES2)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), CAR_VALUES2)

    def test_set_additional_key1(self):
        self.state.set_user_data_on_channel(NAME_VALUES1, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(CAR_VALUES2, channel=CHANNEL1, user_id=USER1),
                         merge_two_dicts(NAME_VALUES1, CAR_VALUES2))
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1),
                         merge_two_dicts(NAME_VALUES1, CAR_VALUES2))

    def test_set_additional_key2(self):
        self.state.set_conversation_data_on_channel(NAME_VALUES2, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(CAR_VALUES2, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1),
                         merge_two_dicts(NAME_VALUES2, CAR_VALUES2))
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            merge_two_dicts(NAME_VALUES2, CAR_VALUES2))

    def test_set_additional_key3(self):
        self.state.set_private_conversation_data_on_channel(AGE_VALUES1, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(CAR_VALUES2, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1),
            merge_two_dicts(AGE_VALUES1, CAR_VALUES2))
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         merge_two_dicts(AGE_VALUES1, CAR_VALUES2))

    def test_set_additional_key4(self):
        self.state.set_user_data(AGE_VALUES2, user_id=USER1)
        self.assertEqual(self.state.set_user_data(CAR_VALUES2, user_id=USER1),
                         merge_two_dicts(AGE_VALUES2, CAR_VALUES2))
        self.assertEqual(self.state.get_user_data(user_id=USER1), merge_two_dicts(AGE_VALUES2, CAR_VALUES2))

    def test_set_additional_key5(self):
        self.state.set_channel_data(CAR_VALUES1, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(CAR_VALUES2, channel=CHANNEL1),
                         merge_two_dicts(CAR_VALUES1, CAR_VALUES2))
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), merge_two_dicts(CAR_VALUES1, CAR_VALUES2))

    def test_set_multi_key1(self):
        self.assertEqual(self.state.set_user_data_on_channel(MULTI_NAMES1, channel=CHANNEL1, user_id=USER1),
                         MULTI_NAMES1)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), MULTI_NAMES1)

    def test_set_multi_key2(self):
        self.assertEqual(self.state.set_conversation_data_on_channel(MULTI_NAMES2, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), MULTI_NAMES2)
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            MULTI_NAMES2)

    def test_set_multi_key3(self):
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(MULTI_AGES1, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), MULTI_AGES1)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         MULTI_AGES1)

    def test_set_multi_key4(self):
        self.assertEqual(self.state.set_user_data(MULTI_AGES2, user_id=USER1), MULTI_AGES2)
        self.assertEqual(self.state.get_user_data(user_id=USER1), MULTI_AGES2)

    def test_set_multi_key5(self):
        self.assertEqual(self.state.set_channel_data(MULTI_CARS1, channel=CHANNEL1), MULTI_CARS1)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), MULTI_CARS1)

    def test_update_multi_key1(self):
        self.state.set_user_data_on_channel(MULTI_NAMES1, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(MULTI_NAMES2, channel=CHANNEL1, user_id=USER1),
                         MULTI_NAMES2)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), MULTI_NAMES2)

    def test_update_multi_key2(self):
        self.state.set_conversation_data_on_channel(MULTI_NAMES2, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(MULTI_NAMES1, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), MULTI_NAMES1)
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            MULTI_NAMES1)

    def test_update_multi_key3(self):
        self.state.set_private_conversation_data_on_channel(MULTI_AGES1, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(MULTI_AGES2, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), MULTI_AGES2)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         MULTI_AGES2)

    def test_update_multi_key4(self):
        self.state.set_user_data(MULTI_AGES2, user_id=USER1)
        self.assertEqual(self.state.set_user_data(MULTI_AGES1, user_id=USER1), MULTI_AGES1)
        self.assertEqual(self.state.get_user_data(user_id=USER1), MULTI_AGES1)

    def test_update_multi_key5(self):
        self.state.set_channel_data(MULTI_CARS1, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(MULTI_CARS2, channel=CHANNEL1), MULTI_CARS2)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), MULTI_CARS2)

    def test_set_additional_multi_key1(self):
        self.state.set_user_data_on_channel(MULTI_NAMES1, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(MULTI_AGES1, channel=CHANNEL1, user_id=USER1),
                         merge_two_dicts(MULTI_NAMES1, MULTI_AGES1))
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1),
                         merge_two_dicts(MULTI_NAMES1, MULTI_AGES1))

    def test_set_additional_multi_key2(self):
        self.state.set_conversation_data_on_channel(MULTI_NAMES2, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(MULTI_AGES1, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1),
                         merge_two_dicts(MULTI_NAMES2, MULTI_AGES1))
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            merge_two_dicts(MULTI_NAMES2, MULTI_AGES1))

    def test_set_additional_multi_key3(self):
        self.state.set_private_conversation_data_on_channel(MULTI_AGES1, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(MULTI_CARS1, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1),
            merge_two_dicts(MULTI_AGES1, MULTI_CARS1))
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         merge_two_dicts(MULTI_AGES1, MULTI_CARS1))

    def test_set_additional_multi_key4(self):
        self.state.set_user_data(MULTI_AGES2, user_id=USER1)
        self.assertEqual(self.state.set_user_data(MULTI_CARS1, user_id=USER1),
                         merge_two_dicts(MULTI_AGES2, MULTI_CARS1))
        self.assertEqual(self.state.get_user_data(user_id=USER1), merge_two_dicts(MULTI_AGES2, MULTI_CARS1))

    def test_set_additional_multi_key5(self):
        self.state.set_channel_data(MULTI_CARS1, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(MULTI_NAMES1, channel=CHANNEL1),
                         merge_two_dicts(MULTI_CARS1, MULTI_NAMES1))
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), merge_two_dicts(MULTI_CARS1, MULTI_NAMES1))

    def test_get_none1(self):
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

    def test_get_none2(self):
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})

    def test_get_none3(self):
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

    def test_get_none4(self):
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

    def test_get_none5(self):
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_set_same_value1(self):
        self.state.set_user_data_on_channel(NAME_VALUES2, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(NAME_VALUES2, channel=CHANNEL1, user_id=USER1),
                         NAME_VALUES2)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), NAME_VALUES2)

    def test_set_same_value2(self):
        self.state.set_conversation_data_on_channel(NAME_VALUES1, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(NAME_VALUES1, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), NAME_VALUES1)
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            NAME_VALUES1)

    def test_set_same_value3(self):
        self.state.set_private_conversation_data_on_channel(AGE_VALUES2, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(AGE_VALUES2, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), AGE_VALUES2)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         AGE_VALUES2)

    def test_set_same_value4(self):
        self.state.set_user_data(AGE_VALUES1, user_id=USER1)
        self.assertEqual(self.state.set_user_data(AGE_VALUES1, user_id=USER1), AGE_VALUES1)
        self.assertEqual(self.state.get_user_data(user_id=USER1), AGE_VALUES1)

    def test_set_same_value5(self):
        self.state.set_channel_data(CAR_VALUES2, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(CAR_VALUES2, channel=CHANNEL1), CAR_VALUES2)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), CAR_VALUES2)

    def test_delete_key1(self):
        self.state.set_user_data_on_channel(NAME_VALUES2, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(DELETE_NAME, channel=CHANNEL1, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

    def test_delete_key2(self):
        self.state.set_conversation_data_on_channel(NAME_VALUES1, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(DELETE_NAME, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), {})
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})

    def test_delete_key3(self):
        self.state.set_private_conversation_data_on_channel(AGE_VALUES2, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(DELETE_AGE, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

    def test_delete_key4(self):
        self.state.set_user_data(AGE_VALUES1, user_id=USER1)
        self.assertEqual(self.state.set_user_data(DELETE_AGE, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

    def test_delete_key5(self):
        self.state.set_channel_data(CAR_VALUES2, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(DELETE_CAR, channel=CHANNEL1), {})
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_delete_some_key1(self):
        self.state.set_user_data_on_channel(MULTI_NAMES1, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(DELETE_NAME, channel=CHANNEL1, user_id=USER1),
                         DELETED_NAME1)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), DELETED_NAME1)

    def test_delete_some_key2(self):
        self.state.set_conversation_data_on_channel(MULTI_NAMES2, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(DELETE_NAME, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), DELETED_NAME2)
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
            DELETED_NAME2)

    def test_delete_some_key3(self):
        self.state.set_private_conversation_data_on_channel(MULTI_AGES1, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(DELETE_AGE, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), DELETED_AGE1)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         DELETED_AGE1)

    def test_delete_some_key4(self):
        self.state.set_user_data(MULTI_AGES2, user_id=USER1)
        self.assertEqual(self.state.set_user_data(DELETE_AGE, user_id=USER1), DELETED_AGE2)
        self.assertEqual(self.state.get_user_data(user_id=USER1), DELETED_AGE2)

    def test_delete_some_key5(self):
        self.state.set_channel_data(MULTI_CARS1, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(DELETE_CAR, channel=CHANNEL1), DELETED_CAR1)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), DELETED_CAR1)

    def test_delete_multi_key1(self):
        self.state.set_user_data_on_channel(MULTI_NAMES1, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.set_user_data_on_channel(DELETE_MULTI_NAMES, channel=CHANNEL1, user_id=USER1),
                         {})
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

    def test_delete_multi_key2(self):
        self.state.set_conversation_data_on_channel(MULTI_NAMES2, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(self.state.set_conversation_data_on_channel(DELETE_MULTI_NAMES, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), {})
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})

    def test_delete_multi_key3(self):
        self.state.set_private_conversation_data_on_channel(MULTI_AGES1, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(DELETE_MULTI_AGES, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

    def test_delete_multi_key4(self):
        self.state.set_user_data(MULTI_AGES2, user_id=USER1)
        self.assertEqual(self.state.set_user_data(DELETE_MULTI_AGES, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

    def test_delete_multi_key5(self):
        self.state.set_channel_data(MULTI_CARS1, channel=CHANNEL1)
        self.assertEqual(self.state.set_channel_data(DELETE_MULTI_CARS, channel=CHANNEL1), {})
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_delete_none1(self):
        self.assertEqual(self.state.set_user_data_on_channel(DELETE_MULTI_NAMES, channel=CHANNEL1, user_id=USER1),
                         {})
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

    def test_delete_none2(self):
        self.assertEqual(self.state.set_conversation_data_on_channel(DELETE_MULTI_NAMES, channel=CHANNEL1,
                                                                     conversation_id=CONVERSATION1), {})
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})

    def test_delete_none3(self):
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(DELETE_MULTI_AGES, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

    def test_delete_none4(self):
        self.assertEqual(self.state.set_user_data(DELETE_MULTI_AGES, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

    def test_delete_none5(self):
        self.assertEqual(self.state.set_channel_data(DELETE_MULTI_CARS, channel=CHANNEL1), {})
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_delete_set1(self):
        self.state.set_user_data_on_channel(NAME_VALUES2, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.delete_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

    def test_delete_set2(self):
        self.state.set_conversation_data_on_channel(NAME_VALUES1, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.delete_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})

    def test_delete_set3(self):
        self.state.set_private_conversation_data_on_channel(AGE_VALUES2, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(self.state.delete_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                                conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

    def test_delete_set4(self):
        self.state.set_user_data(AGE_VALUES1, user_id=USER1)
        self.assertEqual(self.state.delete_user_data(user_id=USER1), {})
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

    def test_delete_set5(self):
        self.state.set_channel_data(CAR_VALUES2, channel=CHANNEL1)
        self.assertEqual(self.state.delete_channel_data(channel=CHANNEL1), {})
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_delete_multi_set1(self):
        self.state.set_user_data_on_channel(MULTI_NAMES1, channel=CHANNEL1, user_id=USER1)
        self.assertEqual(self.state.delete_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

    def test_delete_multi_set2(self):
        self.state.set_conversation_data_on_channel(MULTI_NAMES2, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.assertEqual(
            self.state.delete_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})
        self.assertEqual(
            self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})

    def test_delete_multi_set3(self):
        self.state.set_private_conversation_data_on_channel(MULTI_AGES1, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.assertEqual(self.state.delete_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                                conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

    def test_delete_multi_set4(self):
        self.state.set_user_data(MULTI_AGES2, user_id=USER1)
        self.assertEqual(self.state.delete_user_data(user_id=USER1), {})
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

    def test_delete_multi_set5(self):
        self.state.set_channel_data(MULTI_CARS1, channel=CHANNEL1)
        self.assertEqual(self.state.delete_channel_data(channel=CHANNEL1), {})
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_all(self):
        self.assertEqual(self.state.set_user_data_on_channel(NAME_VALUES1, channel=CHANNEL1, user_id=USER1),
                         NAME_VALUES1)
        self.assertEqual(
            self.state.set_conversation_data_on_channel(NAME_VALUES2, channel=CHANNEL1, conversation_id=CONVERSATION1),
            NAME_VALUES2)
        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(AGE_VALUES1, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), AGE_VALUES1)
        self.assertEqual(self.state.set_user_data(AGE_VALUES2, user_id=USER1), AGE_VALUES2)
        self.assertEqual(self.state.set_channel_data(CAR_VALUES1, channel=CHANNEL1), CAR_VALUES1)

        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), NAME_VALUES1)
        self.assertEqual(self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
                         NAME_VALUES2)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         AGE_VALUES1)
        self.assertEqual(self.state.get_user_data(user_id=USER1), AGE_VALUES2)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), CAR_VALUES1)

        self.assertEqual(self.state.set_user_data_on_channel(DELETE_NAME, channel=CHANNEL1, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

        self.assertEqual(
            self.state.set_conversation_data_on_channel(DELETE_NAME, channel=CHANNEL1, conversation_id=CONVERSATION1),
            {})
        self.assertEqual(self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
                         {})

        self.assertEqual(
            self.state.set_private_conversation_data_on_channel(DELETE_AGE, channel=CHANNEL1, user_id=USER1,
                                                                conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

        self.assertEqual(self.state.set_user_data(DELETE_AGE, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

        self.assertEqual(self.state.set_channel_data(DELETE_CAR, channel=CHANNEL1), {})
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_all_delete(self):
        self.state.set_user_data_on_channel(NAME_VALUES2, channel=CHANNEL1, user_id=USER1)
        self.state.set_conversation_data_on_channel(NAME_VALUES1, channel=CHANNEL1, conversation_id=CONVERSATION1)
        self.state.set_private_conversation_data_on_channel(AGE_VALUES2, channel=CHANNEL1, user_id=USER1,
                                                            conversation_id=CONVERSATION1)
        self.state.set_user_data(AGE_VALUES1, user_id=USER1)
        self.state.set_channel_data(CAR_VALUES2, channel=CHANNEL1)

        self.assertEqual(self.state.delete_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), {})

        self.assertEqual(
            self.state.delete_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
                         {})

        self.assertEqual(self.state.delete_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                                conversation_id=CONVERSATION1), {})
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1), {})

        self.assertEqual(self.state.delete_user_data(user_id=USER1), {})
        self.assertEqual(self.state.get_user_data(user_id=USER1), {})

        self.assertEqual(self.state.delete_channel_data(channel=CHANNEL1), {})
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), {})

    def test_fill(self):
        self.assertEqual(self.state.set_user_data_on_channel(NAME_VALUES1, fill=MESSAGE), NAME_VALUES1)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=USER1), NAME_VALUES1)

        self.assertEqual(self.state.set_conversation_data_on_channel(NAME_VALUES2, fill=MESSAGE), NAME_VALUES2)
        self.assertEqual(self.state.get_conversation_data_on_channel(channel=CHANNEL1, conversation_id=CONVERSATION1),
                         NAME_VALUES2)

        self.assertEqual(self.state.set_private_conversation_data_on_channel(AGE_VALUES1, fill=MESSAGE), AGE_VALUES1)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=USER1,
                                                                             conversation_id=CONVERSATION1),
                         AGE_VALUES1)

        self.assertEqual(self.state.set_user_data(AGE_VALUES2, fill=MESSAGE), AGE_VALUES2)
        self.assertEqual(self.state.get_user_data(user_id=USER1), AGE_VALUES2)

        self.assertEqual(self.state.set_channel_data(CAR_VALUES1, fill=MESSAGE), CAR_VALUES1)
        self.assertEqual(self.state.get_channel_data(channel=CHANNEL1), CAR_VALUES1)

    def test_fill_bot(self):
        self.assertEqual(self.state.set_user_data_on_channel(NAME_VALUES1, fill=MESSAGE, bot=True), NAME_VALUES1)
        self.assertEqual(self.state.get_user_data_on_channel(channel=CHANNEL1, user_id=BOT), NAME_VALUES1)

        self.assertEqual(self.state.set_private_conversation_data_on_channel(AGE_VALUES1, fill=MESSAGE, bot=True),
                         AGE_VALUES1)
        self.assertEqual(self.state.get_private_conversation_data_on_channel(channel=CHANNEL1, user_id=BOT,
                                                                             conversation_id=CONVERSATION1),
                         AGE_VALUES1)

        self.assertEqual(self.state.set_user_data(AGE_VALUES2, fill=MESSAGE, bot=True), AGE_VALUES2)
        self.assertEqual(self.state.get_user_data(user_id=BOT), AGE_VALUES2)

    def _get_activity(self, id, conversation_id=None, type='ReplyToActivity', text=True):
        conversation_id = id if conversation_id is None else conversation_id
        activity = {
            'type': type,
            'conversation_id': '{}'.format(conversation_id),
            'activity': {'id': 'asdf', 'type': type},
            'url_parameters': {},
            'response': {'info': 'success'},
        }

        if type in ['received', 'ReplyToActivity', 'SendToConversation']:
            if text:
                activity['activity']['text'] = 'message text - {}'.format(id)
                if type == 'received':
                    activity['activity']['type'] = 'message'
            else:
                if type == 'received':
                    activity['activity']['type'] = choice(
                        ['contactRelationUpdate', 'conversationUpdate', 'deleteUserData', 'ping', 'typing',
                         'endOfConversation'])

        response_activity = activity.copy()
        response_activity['_id'] = id

        return activity, response_activity

    def test_add_conversation(self):
        activity, response_activity = self._get_activity(1)

        self.state.save_activity(activity)
        self.assertEqual(self.state.get_activities(), [response_activity])

    def test_add_multiple_conversations(self):
        response_activities = []
        for n in range(1, 15):
            activity, response_activity = self._get_activity(n)
            self.state.save_activity(activity)
            response_activities.append(response_activity)

        self.assertEqual(self.state.get_activities(), response_activities[-10:])
        self.assertEqual(len(self.state.get_activities()), 10)

    def test_add_multiple_conversations_with_argument(self):
        response_activities = []
        for n in range(1, 15):
            activity, response_activity = self._get_activity(n)
            self.state.save_activity(activity)
            response_activities.append(response_activity)

        self.assertEqual(self.state.get_activities(count=5), response_activities[-5:])
        self.assertEqual(len(self.state.get_activities(count=5)), 5)

        self.assertEqual(self.state.get_activities(count=15), response_activities[-15:])
        self.assertEqual(len(self.state.get_activities(count=-1)), 14)
        self.assertEqual(len(self.state.get_activities(count=100)), 14)

    def test_maximum_stored(self):
        for n in range(1, 60):
            activity, __ = self._get_activity(n)
            self.state.save_activity(activity)

        self.assertEqual(len(self.state.get_activities(count=-1)), 50)

    def test_get_conversation_id(self):
        response_activities = {}
        combined_response = []
        simple_combined_response = []
        multi = 0
        for conversation_id in ['conv1', 'conv2']:
            response_activities[conversation_id] = []
            for n in range(1, 4):
                n += multi * 3
                activity, response_activity = self._get_activity(n, conversation_id)
                self.state.save_activity(activity)
                response_activities[conversation_id].append(response_activity)
                combined_response.append(response_activity)
                simple_combined_response.append(response_activity['activity']['text'])
            multi += 1

        self.assertEqual(self.state.get_activities(), combined_response, combined_response)
        self.assertEqual(self.state.get_activities(simple=True), simple_combined_response)
        self.assertEqual(len(self.state.get_activities()), 6)

        self.assertEqual(self.state.get_activities(conversation_id='conv1'), response_activities['conv1'])
        self.assertEqual(self.state.get_activities(conversation_id='conv2'), response_activities['conv2'])

        self.assertEqual(len(self.state.get_activities(conversation_id='conv1')), 3)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv2')), 3)

    def test_get_conversation_id_limit(self):
        response_activities = {}
        simple_response_activities = {}
        combined_response = []
        simple_combined_response = []
        multi = 0
        for conversation_id in ['conv1', 'conv2']:
            response_activities[conversation_id] = []
            simple_response_activities[conversation_id] = []
            for n in range(1, 31):
                n += multi * 30
                activity, response_activity = self._get_activity(n, conversation_id)
                self.state.save_activity(activity)
                response_activities[conversation_id].append(response_activity)
                simple_response_activities[conversation_id].append(response_activity['activity']['text'])
                combined_response.append(response_activity)
                simple_combined_response.append(response_activity['activity']['text'])
            multi += 1

        self.assertEqual(self.state.get_activities(), combined_response[-10:])
        self.assertEqual(self.state.get_activities(simple=True), simple_combined_response[-10:])
        self.assertEqual(len(self.state.get_activities()), 10)

        self.assertEqual(self.state.get_activities(conversation_id='conv1'), response_activities['conv1'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv2'), response_activities['conv2'][-10:])

        self.assertEqual(self.state.get_activities(conversation_id='conv1', simple=True), simple_response_activities['conv1'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv2', simple=True), simple_response_activities['conv2'][-10:])

        self.assertEqual(len(self.state.get_activities(conversation_id='conv1')), 10)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv2')), 10)

    def test_get_conversation_id_alternate(self):
        response_activities = {}
        combined_response = []
        response_activities['conv1'] = []
        response_activities['conv2'] = []
        for n in range(1, 61, 2):
            multi = 0
            for conversation_id in ['conv1', 'conv2']:
                n += multi
                activity, response_activity = self._get_activity(n, conversation_id)
                self.state.save_activity(activity)
                response_activities[conversation_id].append(response_activity)
                combined_response.append(response_activity)
                multi += 1

        self.assertEqual(self.state.get_activities(), combined_response[-10:])
        self.assertEqual(len(self.state.get_activities()), 10)

        self.assertEqual(self.state.get_activities(conversation_id='conv1'), response_activities['conv1'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv2'), response_activities['conv2'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv3'), [])

        self.assertEqual(len(self.state.get_activities(conversation_id='conv1')), 10)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv2')), 10)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv3')), 0)

        # Test limits
        self.assertEqual(len(self.state.get_activities(count=50, conversation_id='conv2')), 25)
        self.assertEqual(len(self.state.get_activities(count=5, conversation_id='conv2')), 5)

    def test_get_conversation_id_different_types(self):

        values = ['received', 'ReplyToActivity', 'SendToConversation', 'DeleteActivity', 'CreateConversation', 'GetConversationMembers',
                  'GetActivityMembers']

        get_type = self._get_type(values)

        response_activities = {}
        simple_response_activities = {}

        combined_response = []
        simple_combined_response = []

        response_activities['conv1'] = []
        response_activities['conv2'] = []
        simple_response_activities['conv1'] = []
        simple_response_activities['conv2'] = []

        for n in range(1, 61, 2):
            multi = 0
            for conversation_id in ['conv1', 'conv2']:
                n += multi
                activity, response_activity = self._get_activity(n, conversation_id, type=next(get_type))
                self.state.save_activity(activity)

                response_activities[conversation_id].append(response_activity)
                if 'text' in response_activity['activity']:
                    simple_response_activities[conversation_id].append(response_activity['activity']['text'])

                combined_response.append(response_activity)
                if 'text' in response_activity['activity']:
                    simple_combined_response.append(response_activity['activity']['text'])

                multi += 1

        self.assertEqual(len(self.state.get_activities()), 10)
        self.assertEqual(len(self.state.get_activities(simple=True)), 10)

        self.assertEqual(self.state.get_activities(), combined_response[-10:])
        self.assertEqual(self.state.get_activities(simple=True), simple_combined_response[-10:])

        self.assertEqual(self.state.get_activities(conversation_id='conv1'), response_activities['conv1'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv2'), response_activities['conv2'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv3'), [])

        self.assertEqual(len(self.state.get_activities(conversation_id='conv1')), 10)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv2')), 10)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv3')), 0)

        self.assertEqual(len(self.state.get_activities(conversation_id='conv1', simple=True)), 10)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv2', simple=True)), 10)
        self.assertEqual(len(self.state.get_activities(conversation_id='conv3', simple=True)), 0)

        self.assertEqual(self.state.get_activities(conversation_id='conv1', simple=True), simple_response_activities['conv1'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv2', simple=True), simple_response_activities['conv2'][-10:])
        self.assertEqual(self.state.get_activities(conversation_id='conv3', simple=True), [])

        # Test limits
        self.assertEqual(len(self.state.get_activities(count=50, conversation_id='conv2')), 25)
        self.assertEqual(len(self.state.get_activities(count=5, conversation_id='conv2')), 5)

        print(simple_response_activities['conv2'])
        print(self.state.get_activities(count=50, conversation_id='conv2', simple=True))

        self.assertEqual(len(self.state.get_activities(count=50, conversation_id='conv2', simple=True)), 10)
        self.assertEqual(len(self.state.get_activities(count=5, conversation_id='conv2', simple=True)), 5)

    @staticmethod
    def _get_type(values):
        position = 0
        while True:
            actual_position = position % 7
            yield values[actual_position]
            position += 1

class MongodbStateTestCase(JsonStateTestCase):
    def setUp(self):
        self.config = Config(os.getcwd() + '/microsoftbotframework/tests/test_files/mongodb_test_config.yaml')
        self._drop_database()
        self.state = MongodbState(self.config, database='testmongodbstate')

    def tearDown(self):
        # remove any name or age values
        self._drop_database()

    def _drop_database(self):
        # remove collection
        mongodb_uri = self.config.get_config(None, 'URI', root='mongodb')
        client = MongoClient(mongodb_uri)
        client.drop_database('testmongodbstate')

    def test_get_next_id(self):
        self.assertEqual(self.state._get_last_id(), 0)

        for n in range(1, 6):
            self.assertEqual(self.state._get_next_id(), n)
            self.assertEqual(self.state._get_last_id(), n)
