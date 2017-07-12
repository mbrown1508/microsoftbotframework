from .cache import Cache

try:
    import redis
except ImportError:
    pass


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

