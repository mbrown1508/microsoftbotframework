from abc import ABCMeta, abstractmethod
try:
    from pymongo import MongoClient, DESCENDING, ASCENDING
except ImportError:
    pass
import json
import os
from .config import Config


def get_state(state=None, config=None):
    if state is None and config is None:
        config = Config()

    if state is None:
        state = config.get_config(state, 'state')

    if isinstance(state, str):
        if state == 'JsonState':
            return JsonState()
        elif state == 'MongodbState':
            if config is None:
                config = Config()
            return MongodbState(config)
        else:
            raise(Exception('Invalid string state option specified.'))
    else:
        return state


class State(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_user_data_on_channel(self, values, channel=None, user_id=None, bot=False, fill=None):
        pass

    @abstractmethod
    def set_conversation_data_on_channel(self, values, channel=None, conversation_id=None, fill=None):
        pass

    @abstractmethod
    def set_private_conversation_data_on_channel(self, values, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        pass

    def set_user_data(self, values, user_id=None, bot=False, fill=None):
        raise(Exception('This object does not have a set_user_data method'))

    def set_channel_data(self, values, channel=None, fill=None):
        raise(Exception('This object does not have a set_channel_data method'))

    @abstractmethod
    def get_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        pass

    @abstractmethod
    def get_conversation_data_on_channel(self, channel=None, conversation_id=None, fill=None):
        pass

    @abstractmethod
    def get_private_conversation_data_on_channel(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        pass

    def get_user_data(self, user_id=None, bot=False, fill=None):
        raise(Exception('This object does not have a get_user_data method'))

    def get_channel_data(self, channel=None, fill=None):
        raise(Exception('This object does not have a get_channel_data method'))

    def delete_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        raise (Exception('This object does not have a delete_user_data_on_channel method'))

    def delete_conversation_data_on_channel(self, channel=None, conversation_id=None, fill=None):
        raise (Exception('This object does not have a delete_conversation_data_on_channel method'))

    def delete_private_conversation_data_on_channel(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        raise (Exception('This object does not have a delete_private_conversation_data_on_channel method'))

    def delete_user_data(self, user_id=None, bot=False, fill=None):
        raise(Exception('This object does not have a delete_user_data method'))

    def delete_channel_data(self, channel=None, fill=None):
        raise(Exception('This object does not have a delete_channel_data method'))

    def delete_state_for_user(self, channel=None, user_id=None):
        raise (Exception('This object does not have a delete_state_for_user method'))

    def save_activity(self, activity):
        raise(Exception('This object does not implement conversation tracking'))

    def get_activities(self, count=10):
        raise(Exception('This object does not implement conversation tracking'))

    @staticmethod
    def _fill(fill, bot):
        if fill is not None:
            user_id = fill['recipient']['id'] if bot else fill['from']['id']
            return fill['channelId'], fill['conversation']['id'], user_id

    @staticmethod
    def _simplify_response(value, simple):
        if not simple:
            return value
        else:
            if value['type'] in ['replyToActivity', 'SendToConversation', 'received']:
                return value['activity']['text']

    @staticmethod
    def _simplify_list(list, simple):
        if not simple:
            return list
        return_list = []
        for value in list:
            if value['type'] in ['replyToActivity', 'SendToConversation', 'received']:
                try:
                    return_list.append(value['activity']['text'])
                except:
                    # attachments fail here
                    pass
        return return_list


class MongodbState(State):
    # currently loading is only from config file
    def __init__(self, config, uri=None, database=None, conversation_limit=50):
        self.conversation_limit = conversation_limit

        mongodb_uri = config.get_config(uri, 'URI', root='mongodb')
        mongodb_database = config.get_config(database, 'DATABASE', root='mongodb')

        client = MongoClient(mongodb_uri)
        db = client[mongodb_database]
        self.state_collection = db['state']
        self.conversation_collection = db['conversation']
        self.counters_collection = db['counters']

        if self.counters_collection.find_one() is None:
            self._create_counter()

    def _set_keys(self, index_key, values):
        delete_keys = {}
        add_keys = {}
        for key, value in values.items():
            if value is None:
                delete_keys[key] = 1
            else:
                add_keys[key] = value

        if len(add_keys) > 0 and len(delete_keys) > 0:
            result = self.state_collection.find_one_and_update({'_id': index_key}, {'$set': add_keys, '$unset': delete_keys}, upsert=True, return_document=True)
        elif len(add_keys) > 0 and len(delete_keys) == 0:
            result = self.state_collection.find_one_and_update({'_id': index_key}, {'$set': add_keys}, upsert=True, return_document=True)
        elif len(add_keys) == 0 and len(delete_keys) > 0:
            result = self.state_collection.find_one_and_update({'_id': index_key}, {'$unset': delete_keys}, upsert=True, return_document=True)
        else:
            result = None
        return self._format_update_result(result)

    def set_user_data_on_channel(self, values, channel=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)

        index_key = '{}-{}-{}'.format(channel, None, user_id)
        return self._set_keys(index_key, values)

    def set_conversation_data_on_channel(self, values, channel=None, conversation_id=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)

        index_key = '{}-{}-{}'.format(channel, conversation_id, None)
        return self._set_keys(index_key, values)

    def set_private_conversation_data_on_channel(self, values, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)

        index_key = '{}-{}-{}'.format(channel, conversation_id, user_id)
        return self._set_keys(index_key, values)

    def set_user_data(self, values, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)

        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._set_keys(index_key, values)

    def set_channel_data(self, values, channel=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)

        index_key = '{}-{}-{}'.format(channel, None, None)
        return self._set_keys(index_key, values)

    def get_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, None, user_id)
        return self._dict_if_none(self.state_collection.find_one({'_id': index_key}))

    def get_conversation_data_on_channel(self, channel=None, conversation_id=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, conversation_id, None)
        return self._dict_if_none(self.state_collection.find_one({'_id': index_key}))

    def get_private_conversation_data_on_channel(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, conversation_id, user_id)
        return self._dict_if_none(self.state_collection.find_one({'_id': index_key}))

    def get_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._dict_if_none(self.state_collection.find_one({'_id': index_key}))

    def get_channel_data(self, channel=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, None, None)
        return self._dict_if_none(self.state_collection.find_one({'_id': index_key}))

    def delete_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, None, user_id)
        result = self.state_collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_conversation_data_on_channel(self, channel=None, conversation_id=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, conversation_id, None)
        result = self.state_collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_private_conversation_data_on_channel(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, conversation_id, user_id)
        result = self.state_collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        result = self.state_collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_channel_data(self, channel=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, None, None)
        result = self.state_collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_state_for_user(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)

        result1 = self._format_delete_result(self.state_collection.delete_one({'_id': '{}-{}-{}'.format(channel, conversation_id, user_id)}))
        result2 = self._format_delete_result(self.state_collection.delete_one({'_id': '{}-{}-{}'.format(channel, None, user_id)}))
        result3 = self._format_delete_result(self.state_collection.delete_one({'_id': '{}-{}-{}'.format(None, None, user_id)}))

        # or as sometimes there will be no data is parts, just tells if something was deleted
        return result1 or result2 or result3

    def save_activity(self, activity):
        activity['_id'] = self._get_next_id()
        self.conversation_collection.insert_one(activity)

        last_id = activity['_id'] - self.conversation_limit

        if last_id >= 0:
            self.conversation_collection.delete_one({'_id': last_id})

    def get_activities(self, count=10, conversation_id=None, simple=False):
        last_id = self._get_last_id()
        if count == -1:
            first_id = 0
        else:
            first_id = last_id - count
            if first_id < 0:
                first_id = 0

        if conversation_id is None:
            return self._simplify_list(list(self.conversation_collection.find({'_id': {'$gt': first_id, '$lte': last_id}}).sort("_id", ASCENDING)), simple)
        else:
            return self._simplify_list(list(self.conversation_collection.find({'conversation_id': conversation_id}).sort("_id", ASCENDING)), simple)[-count:]

    def _create_counter(self):
        self.counters_collection.insert_one({'_id': "conversation_id", 'seq': 0})

    def _get_next_id(self):
        response = self.counters_collection.find_one_and_update(
                {'_id': 'conversation_id'},
                {'$inc': {'seq': 1}},
                return_document=True,
            )
        return response['seq']

    def _get_last_id(self):
        response = self.counters_collection.find_one({'_id': 'conversation_id'})
        return response['seq']

    @staticmethod
    def _dict_if_none(value):
        if value is None:
            return {}
        else:
            value.pop('_id')
            return value

    @staticmethod
    def _format_update_result(result):
        if result is None:
            return {}
        else:
            result.pop('_id', None)
            return result

    @staticmethod
    def _format_delete_result(result):
        if result.acknowledged:
            if result.deleted_count == 1:
                return {}
        raise(Exception('Delete failed'))


class JsonState(State):
    def __init__(self, state_file='state.json', conversation_file='conversation.json', root_directory=None, conversation_limit=50):
        self.conversation_limit = conversation_limit

        if root_directory is not None:
            self.data_location = '{}/{}'.format(root_directory, state_file)
            self.conversation_location = '{}/{}'.format(root_directory, conversation_file)
        else:
            self.data_location = '{}/{}'.format(os.getcwd(), state_file)
            self.conversation_location = '{}/{}'.format(os.getcwd(), conversation_file)

        # if the file doesn't exist create a empty file with a json object
        if not os.path.isfile(self.data_location):
            with open(self.data_location, 'w+') as data_file:
                data_file.write('{}')

        if not os.path.isfile(self.conversation_location):
            with open(self.conversation_location, 'w+') as data_file:
                data_file.write(json.dumps({'_id': 0, 'activities': []}))

    def set_user_data_on_channel(self, values, channel=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_user_data_on_channel(channel, user_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel, None, user_id)
        return self._set(index_key, new_data)

    def set_conversation_data_on_channel(self, values, channel=None, conversation_id=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)

        current_data = self.get_conversation_data_on_channel(channel, conversation_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel, conversation_id, None)
        return self._set(index_key, new_data)

    def set_private_conversation_data_on_channel(self, values, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_private_conversation_data_on_channel(channel, conversation_id, user_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel, conversation_id, user_id)
        return self._set(index_key, new_data)

    def set_user_data(self, values, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_user_data(user_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._set(index_key, new_data)

    def set_channel_data(self, values, channel=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)

        current_data = self.get_channel_data(channel)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel, None, None)
        return self._set(index_key, new_data)

    def get_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, None, user_id)
        return self._dict_if_none(self._get(index_key))

    def get_conversation_data_on_channel(self, channel=None, conversation_id=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, conversation_id, None)
        return self._dict_if_none(self._get(index_key))

    def get_private_conversation_data_on_channel(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, conversation_id, user_id)
        return self._dict_if_none(self._get(index_key))

    def get_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._dict_if_none(self._get(index_key))

    def get_channel_data(self, channel=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, None, None)
        return self._dict_if_none(self._get(index_key))

    def delete_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, None, user_id)
        return self._delete(index_key)

    def delete_conversation_data_on_channel(self, channel=None, conversation_id=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, conversation_id, None)
        return self._delete(index_key)

    def delete_private_conversation_data_on_channel(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel, conversation_id, user_id)
        return self._delete(index_key)

    def delete_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._delete(index_key)

    def delete_channel_data(self, channel=None, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel, None, None)
        return self._delete(index_key)

    def delete_state_for_user(self, channel=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel, conversation_id, user_id = self._fill(fill, bot)
        result1 = self._delete('{}-{}-{}'.format(channel, conversation_id, user_id))
        result2 = self._delete('{}-{}-{}'.format(channel, None, user_id))
        result3 = self._delete('{}-{}-{}'.format(None, None, user_id))
        return result1 and result2 and result3

    def save_activity(self, activity):
        with open(self.conversation_location, 'r+') as data_file:
            data = json.load(data_file)

            data['_id'] += 1
            activity['_id'] = data['_id']

            data['activities'].append(activity)
            data['activities'] = data['activities'][-self.conversation_limit:]

            data_file.seek(0)
            data_file.write(json.dumps(data))
            data_file.truncate()
        return True

    def get_activities(self, count=10, conversation_id=None, simple=False):
        with open(self.conversation_location) as data_file:
            data = json.load(data_file)
            values = data['activities']

        return_values = []
        current_count = 0
        if conversation_id is not None:
            for activity in reversed(values):
                if activity['conversation_id'] == conversation_id:
                    return_values.append(self._simplify_response(activity, simple))
                    current_count += 1
                    if count != -1 and current_count == count:
                        return return_values[::-1]
            return return_values[::-1]
        else:
            if count == -1:
                return self._simplify_list(values, simple)
            else:
                return self._simplify_list(values, simple)[-count:]

    @staticmethod
    def _set_values(current_data, values):
        new_data = dict(current_data)
        for key, value in values.items():
            if value is None:
                if key in new_data:
                    new_data.pop(key)
            else:
                new_data[key] = value
        return new_data

    @staticmethod
    def _dict_if_none(value):
        return {} if value is None else value

    def _get(self, key):
        with open(self.data_location) as data_file:
            data = json.load(data_file)
            if key in data:
                value = data[key]
            else:
                value = None

        return value

    def _set(self, key, value):
        with open(self.data_location, 'r+') as data_file:
            data = json.load(data_file)

            data[key] = value

            data_file.seek(0)
            data_file.write(json.dumps(data))
            data_file.truncate()

        return data[key]

    def _delete(self, key):
        with open(self.data_location, 'r+') as data_file:
            data = json.load(data_file)

            if key in data:
                data.pop(key, None)

            data_file.seek(0)
            data_file.write(json.dumps(data))
            data_file.truncate()

        return {}
