from abc import ABCMeta, abstractmethod


class Cache(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass


