from abc import ABCMeta, abstractmethod
try:
    from pymongo import MongoClient
except ImportError:
    pass
import json
import os


class State(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_user_data_on_channel(self, values, channel=None, user_id=None, bot=False, fill=None):
        pass

    @abstractmethod
    def set_conversation_data_on_channel(self, values, channel=None, conversation_id=None, bot=False, fill=None):
        pass

    @abstractmethod
    def set_private_conversation_data_on_channel(self, values, channel=None, user_id=None, conversation_id=None, bot=False, fill=None):
        pass

    def set_user_data(self, values, user_id=None, bot=False, fill=None):
        raise(Exception('This object does not have a set_user_data method'))

    def set_channel_data(self, values, channel_id=None, fill=None):
        raise(Exception('This object does not have a set_channel_data method'))

    @abstractmethod
    def get_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        pass

    @abstractmethod
    def get_conversation_data_on_channel(self, channel=None, conversation_id=None, bot=False, fill=None):
        pass

    @abstractmethod
    def get_private_conversation_data_on_channel(self, channel=None, user_id=None, conversation_id=None, bot=False, fill=None):
        pass

    def get_user_data(self, user_id=None, bot=False, fill=None):
        raise(Exception('This object does not have a get_user_data method'))

    def get_channel_data(self, channel_id=None, fill=None):
        raise(Exception('This object does not have a get_channel_data method'))

    def delete_user_data_on_channel(self, channel=None, user_id=None, bot=False, fill=None):
        raise (Exception('This object does not have a delete_user_data_on_channel method'))

    def delete_conversation_data_on_channel(self, channel=None, conversation_id=None, bot=False, fill=None):
        raise (Exception('This object does not have a delete_conversation_data_on_channel method'))

    def delete_private_conversation_data_on_channel(self, channel=None, user_id=None, conversation_id=None, bot=False, fill=None):
        raise (Exception('This object does not have a delete_private_conversation_data_on_channel method'))

    def delete_user_data(self, user_id=None, bot=False, fill=None):
        raise(Exception('This object does not have a delete_user_data method'))

    def delete_channel_data(self, channel_id=None, fill=None):
        raise(Exception('This object does not have a delete_channel_data method'))

    def delete_state_for_user(self, channel_id=None, user_id=None):
        raise (Exception('This object does not have a delete_state_for_user method'))

    @staticmethod
    def _fill(fill, bot):
        if fill is not None:
            user_id = fill['recipient']['id'] if bot else fill['fromAccount']['id']
            return fill['channelId'], fill['conversation']['id'], user_id


class MongodbState(State):
    # currently loading is only from config file
    def __init__(self, config):
        mongodb_uri = config.get_config(None, 'URI', root='mongodb')
        mongodb_database = config.get_config(None, 'DATABASE', root='mongodb')
        mongodb_collection = config.get_config(None, 'COLLECTION', root='mongodb')

        client = MongoClient(mongodb_uri)
        db = client[mongodb_database]
        self.collection = db[mongodb_collection]

    def set_user_data_on_channel(self, values, channel_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        index_key = '{}-{}-{}'.format(channel_id, None, user_id)
        result = self.collection.update_one({'_id': index_key}, {'$set': values}, upsert=True)
        return self._format_update_result(result)

    def set_conversation_data_on_channel(self, values, channel_id=None, conversation_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        index_key = '{}-{}-{}'.format(channel_id, conversation_id, None)
        result = self.collection.update_one({'_id': index_key}, {'$set': values}, upsert=True)
        return self._format_update_result(result)

    def set_private_conversation_data_on_channel(self, values, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        index_key = '{}-{}-{}'.format(channel_id, conversation_id, user_id)
        result = self.collection.update_one({'_id': index_key}, {'$set': values}, upsert=True)
        return self._format_update_result(result)

    def set_user_data(self, values, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        index_key = '{}-{}-{}'.format(None, None, user_id)
        result = self.collection.update_one({'_id': index_key}, {'$set': values}, upsert=True)
        return self._format_update_result(result)

    def set_channel_data(self, values, channel_id=None, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, False)

        index_key = '{}-{}-{}'.format(channel_id, None, None)
        result = self.collection.update_one({'_id': index_key}, {'$set': values}, upsert=True)
        return self._format_update_result(result)

    def get_user_data_on_channel(self, channel_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, None, user_id)
        return self._dict_if_none(self.collection.find_one({'_id': index_key}))

    def get_conversation_data_on_channel(self, channel_id=None, conversation_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, None)
        return self._dict_if_none(self.collection.find_one({'_id': index_key}))

    def get_private_conversation_data_on_channel(self, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, user_id)
        return self._dict_if_none(self.collection.find_one({'_id': index_key}))

    def get_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._dict_if_none(self.collection.find_one({'_id': index_key}))

    def get_channel_data(self, channel_id=None, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel_id, None, None)
        return self._dict_if_none(self.collection.find_one({'_id': index_key}))

    def delete_user_data_on_channel(self, channel_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, None, user_id)
        result = self.collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_conversation_data_on_channel(self, channel_id=None, conversation_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, None)
        result = self.collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_private_conversation_data_on_channel(self, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, user_id)
        result = self.collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        result = self.collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_channel_data(self, channel_id=None, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel_id, None, None)
        result = self.collection.delete_one({'_id': index_key})
        return self._format_delete_result(result)

    def delete_state_for_user(self, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        result1 = self._format_delete_result(self.collection.delete_one({'_id': '{}-{}-{}'.format(channel_id, conversation_id, user_id)}))
        result2 = self._format_delete_result(self.collection.delete_one({'_id': '{}-{}-{}'.format(channel_id, None, user_id)}))
        result3 = self._format_delete_result(self.collection.delete_one({'_id': '{}-{}-{}'.format(None, None, user_id)}))

        # or as sometimes there will be no data is parts, just tells if something was deleted
        return result1 or result2 or result3

    @staticmethod
    def _dict_if_none(value):
        return {} if value is None else value

    @staticmethod
    def _format_update_result(result):
        if result.acknowledged:
            if result.modified_count == 1 or result.upserted_id is not None:
                return True
        return False

    @staticmethod
    def _format_delete_result(result):
        if result.acknowledged:
            if result.deleted_count == 1:
                return True
        return False


class JsonState(State):
    def __init__(self, filename='state.json', root_directory=None):
        if root_directory is not None:
            self.data_location = '{}/{}'.format(root_directory, filename)
        else:
            self.data_location = '{}/{}'.format(os.getcwd(), filename)

        # if the file doesn't exist create a empty file with a json object
        if not os.path.isfile(self.data_location):
            with open(self.data_location, 'w+') as data_file:
                data_file.write('{}')

    def set_user_data_on_channel(self, values, channel_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_user_data_on_channel(channel_id, user_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel_id, None, user_id)
        return self._set(index_key, new_data)

    def set_conversation_data_on_channel(self, values, channel_id=None, conversation_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_conversation_data_on_channel(channel_id, conversation_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel_id, conversation_id, None)
        return self._set(index_key, new_data)

    def set_private_conversation_data_on_channel(self, values, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_private_conversation_data_on_channel(channel_id, conversation_id, user_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel_id, conversation_id, user_id)
        return self._set(index_key, new_data)

    def set_user_data(self, values, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_user_data(user_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._set(index_key, new_data)

    def set_channel_data(self, values, channel_id=None, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, False)

        current_data = self.get_channel_data(channel_id)
        new_data = self._set_values(current_data, values)

        index_key = '{}-{}-{}'.format(channel_id, None, None)
        return self._set(index_key, new_data)

    def get_user_data_on_channel(self, channel_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, None, user_id)
        return self._dict_if_none(self._get(index_key))

    def get_conversation_data_on_channel(self, channel_id=None, conversation_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, None)
        return self._dict_if_none(self._get(index_key))

    def get_private_conversation_data_on_channel(self, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, user_id)
        return self._dict_if_none(self._get(index_key))

    def get_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._dict_if_none(self._get(index_key))

    def get_channel_data(self, channel_id=None, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel_id, None, None)
        return self._dict_if_none(self._get(index_key))

    def delete_user_data_on_channel(self, channel_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, None, user_id)
        return self._delete(index_key)

    def delete_conversation_data_on_channel(self, channel_id=None, conversation_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, None)
        return self._delete(index_key)

    def delete_private_conversation_data_on_channel(self, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(channel_id, conversation_id, user_id)
        return self._delete(index_key)

    def delete_user_data(self, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._delete(index_key)

    def delete_channel_data(self, channel_id=None, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, False)
        index_key = '{}-{}-{}'.format(channel_id, None, None)
        return self._delete(index_key)

    def delete_state_for_user(self, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)
        result1 = self._delete('{}-{}-{}'.format(channel_id, conversation_id, user_id))
        result2 = self._delete('{}-{}-{}'.format(channel_id, None, user_id))
        result3 = self._delete('{}-{}-{}'.format(None, None, user_id))
        return result1 and result2 and result3

    @staticmethod
    def _set_values(current_data, values):
        new_data = dict(current_data)
        for key, value in values.items():
            if value is None:
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

        return True

    def _delete(self, key):
        with open(self.data_location, 'r+') as data_file:
            data = json.load(data_file)

            data.pop(key, None)

            data_file.seek(0)
            data_file.write(json.dumps(data))
            data_file.truncate()

        return True
