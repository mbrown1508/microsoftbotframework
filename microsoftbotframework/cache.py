from abc import ABCMeta, abstractmethod
import json
import os
try:
    import redis
except ImportError:
    pass
from .config import Config


def get_cache(cache, config=None):
    if isinstance(cache, str):
        if cache == 'JsonCache':
            return JsonCache()
        elif cache == 'RedisCache':
            if config is None:
                config = Config()
            return RedisCache(config)
        else:
            raise(Exception('Invalid string cache option specified.'))
    else:
        return cache


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


class JsonCache(Cache):
    def __init__(self, filename='cache.json', root_directory=None):
        if root_directory is not None:
            self.data_location = '{}/{}'.format(root_directory, filename)
        else:
            self.data_location = '{}/{}'.format(os.getcwd(), filename)

        # if the file doesn't exist create a empty file with a json object
        if not os.path.isfile(self.data_location):
            with open(self.data_location, 'w+') as data_file:
                data_file.write('{}')

    def get(self, key):
        with open(self.data_location) as data_file:
            data = json.load(data_file)
            if key in data:
                value = data[key]
            else:
                value = None

        return value

    def set(self, key, value):
        with open(self.data_location, 'r+') as data_file:
            data = json.load(data_file)

            data[key] = value

            data_file.seek(0)
            data_file.write(json.dumps(data))
            data_file.truncate()

        return True

    def delete(self, key):
        with open(self.data_location, 'r+') as data_file:
            data = json.load(data_file)

            if key not in data:
                return False

            data.pop(key, None)

            data_file.seek(0)
            data_file.write(json.dumps(data))
            data_file.truncate()

        return True


class RedisCache(Cache):
    # currently loading is only from config file
    def __init__(self, config):
        self.redis_uri = config.get_config(None, 'URI', root='redis')
        self.redis = None
        self.redis_config = config.get_section_config('redis')

    def get(self, key):
        self._connect()
        value = self.redis.get(key)
        if value is not None:
            value = value.decode('UTF-8')
        return value

    def set(self, key, value):
        self._connect()
        result = self.redis.set(key, value)

        if result > 0:
            return True
        else:
            return False

    def delete(self, key):
        self._connect()
        result = self.redis.delete(key)

        if result > 0:
            return True
        else:
            return False

    def _connect(self):
        if self.redis is None:
            self.redis = redis.StrictRedis.from_url(self.redis_uri)
            for name, value in self.redis_config.items():
                try:
                    self.redis.config_set(name, value)
                except:
                    pass
                    # log...

