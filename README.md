[![CI](https://github.com/taylorhakes/python-redis-cache/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/taylorhakes/python-redis-cache/actions/workflows/tests.yml/badge.svg?branch=master)
[![pypi](https://img.shields.io/pypi/v/python-redis-cache.svg)](https://pypi.python.org/pypi/python-redis-cache)
[![license](https://img.shields.io/github/license/taylorhakes/python-redis-cache.svg)](https://github.com/taylorhakes/python-redis-cache/blob/master/LICENSE)

# python-redis-cache
Simple redis cache for Python functions

### Requirements
- Redis 5+
- Python 3.8+ (should work in Python 3.6+, but not tested)

## How to install
```
pip install python-redis-cache
```

## How to use
```python
from redis import StrictRedis
from redis_cache import RedisCache

client = StrictRedis(host="redis", decode_responses=True)
cache = RedisCache(redis_client=client)


@cache.cache()
def my_func(arg1, arg2):
    result = some_expensive_operation()
    return result

# Use the function
my_func(1, 2)

# Call it again with the same arguments and it will use cache
my_func(1, 2)

# Invalidate a single value
my_func.invalidate(1, 2)

# Invalidate all values for function
my_func.invalidate_all()
```

## Limitations and things to know
Arguments and return types must be JSON serializable by default. You can override the serializer, but be careful with using Pickle. Make sure you understand the security risks. Pickle should not be used with untrusted values.
https://security.stackexchange.com/questions/183966/safely-load-a-pickle-file
`decode_responses` parameter must be `False` in redis client if you use pickle.

- **ttl** - is based on the time from when it's first inserted in the cache, not based on the last access
- **limit** - The limit will revoke keys (once it hits the limit) based on FIFO, not based on LRU

## API
```python
# Create the redis cache
cache = RedisCache(redis_client, prefix="rc", serializer=dumps, deserializer=loads, key_serializer=None, exception_handler=None)

# Cache decorator to go on functions, see above
cache.cache(ttl=..., limit=..., namespace=...) -> Callable[[Callable], Callable]

# Get multiple values from the cache
cache.mget([{"fn": my_func, "args": [1,2], "kwargs": {}}, ...]) -> List[Any]

Redis

# Cached function API

# Returns a cached value, if it exists in cache. Saves value in cache if it doesn't exist
cached_func(*args, *kwargs)

# Invalidates a single value
cached_func.invalidate(*args, **kwargs)

# Invalidates all values for cached function
cached_func.invalidate_all()
```

- prefix - The string to prefix the redis keys with
- serializer/deserializer - functions to convert arguments and return value to a string (user JSON by default)
- ttl - The time in seconds to cache the return value
- namespace - The string namespace of the cache. This is useful for allowing multiple functions to use the same cache. By default its `f'{function.__module__}.{function.__file__}'`
- exception_handler - Function to handle Redis cache exceptions. This allows you to fall back to calling the original function or logging exceptions. Function has the following signature `exception_handler(exception: Exception, function: Callable, args: List, kwargs: Dict) -> Any`. If using this handler, reraise the exception in the handler to stop execution of the function. All return results will be used even if `None`. If handler not defined, it will raise the exception and not call the original function.
