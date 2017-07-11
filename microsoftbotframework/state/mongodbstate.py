from .state import State
from pymongo import MongoClient


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
