# Configuration
There are 3 ways to configure your application.
* config.yaml
* environment variable
* object arguments

## config.yaml
By default each of the objects will look for a config.yaml file in the current working directory of the application. If you don't want to have config.yaml in the working directory you can set CONFIG_LOCATION as an environment variable.
```
CONFIG_LOCATION="/home/user/configstore/config.yaml"
```
You can also passing config_location as a argument to any of the objects. 
```python
ReplyToActivity(config_location="/home/user/configstore/config.yaml")
```

To configure celery and redis (flask comming soon) you can set config in the file as follows.
```
celery:
    result_backend: redis://localhost:6379
    broker_url: redis://localhost:6379
    broker_pool_limit: None
redis:
    connections: 5
```

All other config mentioned in the library will be placed under the other heading.
```
other:
    app_client_id: sdjhdasgaerbwret
    app_client_secret: eahsadtkyrkryjsnb
```

## Environment Vars
Environment vars can be used for any configuration options. For app specific variables use the full uppercase name of the variable.
```
APP_CLIENT_ID="sdjhdasgaerbwret"
APP_CLIENT_SECRET="eahsadtkyrkryjsnb"
```
To set celery or redis configuration prefix the variable with CELERY_ or REDIS_
```
CELERY_RESULT_BACKEND="redis://localhost:6379"
CELERY_BROKER_URL="redis://localhost:6379"
CELERY_BROKER_POOL_LIMIT="None"
REDIS_CONNECTIONS="5"
```

## Arguments
All config can be passed via arguments
```python
ReplyToActivity(app_client_id='sdjhdasgaerbwret',
                app_client_secret='eahsadtkyrkryjsnb')
```

