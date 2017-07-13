from unittest import TestCase
from ..config import Config
from ..state import JsonState, MongodbState
from pymongo import MongoClient
import os

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
        try:
            os.remove(os.getcwd() + '/testjsonstate.json')
        except OSError:
            pass

        self.state = JsonState(filename='testjsonstate.json')

    def tearDown(self):
        os.remove(os.getcwd() + '/testjsonstate.json')

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


class MongodbStateTestCase(JsonStateTestCase):
    def setUp(self):
        self.config = Config(os.getcwd() + '/microsoftbotframework/tests/test_files/mongodb_test_config.yaml')
        self._delete_collection()
        self.state = MongodbState(self.config, collection='testmongodbstate')

    def tearDown(self):
        # remove any name or age values
        self._delete_collection()

    def _delete_collection(self):
        # remove collection
        mongodb_uri = self.config.get_config(None, 'URI', root='mongodb')
        mongodb_database = self.config.get_config(None, 'DATABASE', root='mongodb')
        mongodb_collection = self.config.get_config('testmongodbstate', 'COLLECTION', root='mongodb')

        client = MongoClient(mongodb_uri)
        db = client[mongodb_database]
        collection = db[mongodb_collection]

        collection.drop()
