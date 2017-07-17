# Cache
There are currently 2 cache adapters available in the library:
* JsonCache
* RedisCache

## Installation
#####JsonCache
JsonCache requires write privileges to the working directory or the configured directory.

#####RedisCache 
RedisCache requires a working redis data store. See the following url for a good guide on installing. https://www.linode.com/docs/databases/redis/deploy-redis-on-ubuntu-or-debian. If using Heroku you can also the resources to add "Heroku Redis :: Redis, Hobby Dev".

In addition the redis library is required. It can be installed with the following command.

```text
pip install redis
```

## Using Caching
The 2 main objects that use caching are the MsBot object which caches the certificates and the ConversationOperation objects who cache the auth token.

By default JsonCache is enabled. This is to reduce the amount of calls to the authorization and certificate endpoints. It is recomended that you don't use JsonCache in production.

They can be set inline using strings as follows.
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

#####config.yaml (Redis Only)
```yaml
other:
    cache: RedisCache   # cache to use
redis:
    uri: redis://localhost:6379
```

#####inline arguments
```python
bot = MsBot(state=RedisCache(config))

bot = MsBot(state=JsonCache('cache.json'))
```

#####environment variables (Redis Only)
```sh
# in linux
export CACHE=JsonCache
export REDIS_URI=redis://localhost:6379
```



