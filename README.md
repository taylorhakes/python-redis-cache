# python-redis-cache
Simple redis cache for Python functions

### Requirements
- Redis 5
- Python 3.6

## How to install
```
pip install python-redis-cache
```

## How to use
```python
from redis import StrictRedis
from redis_cache import RedisCache

redis_client = StrictRedis(host="redis", decode_responses=True)
cache = RedisCache(redis_client=client)


@cache.cache()
def my_func(arg1, arg2):
    # Some expensive operation
    return 5


# Invalidate a single value
my_func.invalidate(1, 2)

# Invalidate all values for function
my_func.invalidate_all()
```

## Limitations
Arguments and return types must be JSON serializable by default. You can override the serializer, but be careful with using Pickle. Make sure you understand the security risks. Pickle should not be used with untrusted values.

## API
```
RedisCache(redis_client, prefix="rc", serializer=dumps, deserializer=loads)

RedisCache.cache(ttl=None, limit=None, namespace=None)
```

- prefix - The string to prefix the redis keys with
- serializer/deserializer - functions to convert arguments and return value to a string (user JSON by default)
- ttl - The time in seconds to cache the return value
- namespace - The string namespace of the cache. This is useful for allowing multiple functions to use the same cache. By default its `f'{function.__module__}.{function.__file__}'`
