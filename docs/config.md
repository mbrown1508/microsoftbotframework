# The Config Object
Additional configuration can be passed to celery and redis (flask comming soon) by setting them in the config.yaml as follows.
```
celery:
    result_backend: redis://localhost:6379
    broker_url: redis://localhost:6379
    broker_pool_limit: None
redis:

```
