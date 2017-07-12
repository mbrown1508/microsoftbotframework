# Cache
There are currently 2 cache adapters available in the library:
* JsonCache
* RedisCache

## Using Caching
The 2 main objects that use caching are the MsBot object which caches the certificates and the ConversationOperation objects who cache the auth token.

By default JsonCache is enabled. This is to reduce the amount of calls to the authorization and certificate endpoints. It is recomended that you don't use JsonCache in production.

They can be configured inline using strings as follows.
```python
bot = MsBot(cache='RedisCache')

activity_members = GetActivityMembers(conversationId="asdfwetjerjbbvwre",
                                      activityId="asdkbuaeniouhrvqeoruih",
                                      cache="RedisCache").send()
```

They can also be configured using objects.
```python
config = Config()
bot = MsBot(cache=RedisCache(config))
```

This allows you to build your own Cache objects using the same API by extending the Cache Abstract Class

While it is not recommended you can disable caching by setting cache to False
```python
bot = MsBot(cache=False)
```

## Configuring Cache Objects
You can configure the cache objects in 3 ways.

#####config.yaml
```yamlex
other:
    cache: RedisCache
redis:
    uri: redis://localhost:6379
json:
    cache_file: cache.json
    root_dir: /home/user
```

#####inline arguments
```python
bot = MsBot(cache=RedisCache(config))

bot = MsBot(cache=JsonCache('cache.json'))
```

#####environment variables
```sh
# in linux
export CACHE=RedisCache
export REDIS_URI=redis://localhost:6379
export JSON_ROOT_DIR=/home/user
```





