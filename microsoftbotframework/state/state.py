from abc import ABCMeta, abstractmethod


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


