from .state import State
import os
import json


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

    def set_user_data_on_channel(self, key, value, channel_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_user_data_on_channel(channel_id, user_id)
        current_data[key] = value

        index_key = '{}-{}-{}'.format(channel_id, None, user_id)
        return self._set(index_key, current_data)

    def set_conversation_data_on_channel(self, key, value, channel_id=None, conversation_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_conversation_data_on_channel(channel_id, conversation_id)
        current_data[key] = value

        index_key = '{}-{}-{}'.format(channel_id, conversation_id, None)
        return self._set(index_key, current_data)

    def set_private_conversation_data_on_channel(self, key, value, channel_id=None, conversation_id=None, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_private_conversation_data_on_channel(channel_id, conversation_id, user_id)
        current_data[key] = value

        index_key = '{}-{}-{}'.format(channel_id, conversation_id, user_id)
        return self._set(index_key, current_data)

    def set_user_data(self, key, value, user_id=None, bot=False, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, bot)

        current_data = self.get_user_data(user_id)
        current_data[key] = value

        index_key = '{}-{}-{}'.format(None, None, user_id)
        return self._set(index_key, current_data)

    def set_channel_data(self, key, value, channel_id=None, fill=None):
        if fill is not None:
            channel_id, conversation_id, user_id = self._fill(fill, False)

        current_data = self.get_channel_data(channel_id)
        current_data[key] = value

        index_key = '{}-{}-{}'.format(channel_id, None, None)
        return self._set(index_key, current_data)

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
    def _fill(fill, bot):
        if fill is not None:
            user_id = fill['bot_id'] if bot else fill['user_id']
            return fill['channel'], fill['conversation'], user_id

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
