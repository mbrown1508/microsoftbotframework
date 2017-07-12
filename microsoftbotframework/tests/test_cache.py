from unittest import TestCase
from microsoftbotframework import JsonCache, RedisCache, Config
import os


class JsonCacheTestCase(TestCase):
    def setUp(self):
        try:
            os.remove(os.getcwd() + '/testjsoncache.json')
        except OSError:
            pass

        self.cache = JsonCache(filename='testjsoncache.json')

    def tearDown(self):
        os.remove(os.getcwd() + '/testjsoncache.json')

    def test_set_new(self):
        self.assertEqual(self.cache.set('name', 'john'), True)

        self.assertEqual(self.cache.get('name'), 'john')

    def test_get_none(self):
        self.assertEqual(self.cache.get('name'), None)

    def test_set_update(self):
        self.cache.set('name', 'john')

        self.assertEqual(self.cache.set('age', '90'), True)

        self.assertEqual(self.cache.get('age'), '90')
        self.assertEqual(self.cache.get('name'), 'john')

    def test_set_different_value(self):
        self.cache.set('name', 'john')

        self.assertEqual(self.cache.set('name', 'sam'), True)

        self.assertEqual(self.cache.get('name'), 'sam')

    def test_set_same_value(self):
        self.cache.set('name', 'sam')

        self.assertEqual(self.cache.set('name', 'sam'), True)

        self.assertEqual(self.cache.get('name'), 'sam')

    def test_delete_value(self):
        self.cache.set('name', 'john')

        self.assertEqual(self.cache.delete('name'), True)

        self.assertEqual(self.cache.get('name'), None)

    def test_delete_none(self):
        self.assertEqual(self.cache.delete('name'), False)


class RedisCacheTestCase(JsonCacheTestCase):
    def setUp(self):
        config = Config(os.getcwd() + '/microsoftbotframework/tests/test_files/redis_test_config.yaml')
        self.cache = RedisCache(config)

        # remove any name or age values
        self.cache.delete('name')
        self.cache.delete('age')

    def tearDown(self):
        # remove any name or age values
        self.cache.delete('name')
        self.cache.delete('age')
