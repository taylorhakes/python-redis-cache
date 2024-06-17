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
    return some_expensive_operation()

# Use the function
my_func(1, 2)

# Call it again with the same arguments and it will use cache
my_func(1, 2)

# Invalidate a single value
my_func.invalidate(1, 2)

# Invalidate all values for function
my_func.invalidate_all()
```

## API
```python
# Create the redis cache
cache = RedisCache(redis_client, prefix="rc", serializer=dumps, deserializer=loads, key_serializer=None, support_cluster=True, exception_handler=None)

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
- support_cluster - Set to False to disable the `{` prefix on the keys. This is NOT recommended. See below for more info.
- active - Optional flag to disable the caching completly for troubleshooting/lower environments


## Limitations and things to know
Arguments and return types must be JSON serializable by default. You can override the serializer, but be careful with using Pickle. Make sure you understand the security risks. Pickle should not be used with untrusted values.
https://security.stackexchange.com/questions/183966/safely-load-a-pickle-file
`decode_responses` parameter must be `False` in redis client if you use pickle.

- **ttl** - is based on the time from when it's first inserted in the cache, not based on the last access
- **limit** - The limit will revoke keys (once it hits the limit) based on FIFO, not based on LRU

### Redis key names
The key names by default are as follows:
```python
from base64 import b64encode

key = f"{{rc:{fn.__module__}.{fn.__qualname__}}}:{b64encode(function_args).decode('utf-8')}"
```
The cache key names start with `{`, which can be confusing, but is required for redis clusters to place the keys
in the correct slots.

**NOTE**: It is NOT recommended to use any of the options below. The key name generation by default handles all use cases.

#### Specifying `prefix` - The string to prefix the redis keys with
```python
cache = RedisCache(redis_client, prefix="custom_prefix")

# Changes keys to the following
key = f"{{custom_prefix:{fn.__module__}.{fn.__qualname__}}}:{b64encode(function_args).decode('utf-8')}"
```
#### Specifying `namespace` - The name of the cache function
```python
cache = RedisCache(redis_client)

@cache.cache(namespace="custom_func_name")
def my_func(arg1, arg2):
    pass

# Changes keys to the following
key = f"{{rc:custom_func_name}}:{b64encode(function_args).decode('utf-8')}"
```
#### Specifying `key_serializer` or `serializer` - The way function arguments are serialized
```python
def custom_key_serializer(fn_args):
    ## Do something with fn_args and return a string. For instance
    return my_custom_serializer(fn_args)

cache = RedisCache(redis_client, key_serializer=custom_key_serializer)

# Changes keys to the following
key = f"{{rc:{fn.__module__}.{fn.__qualname__}}}:{b64encode(custom_serialized_args).decode('utf-8')}"
```

#### Specifying `support_cluster=False`- This will disable the `{` prefix on the keys
This option is NOT recommended because this library will no longer work with redis clusters. Often times people/companies
will start not using cluster mode and then will migrate to using cluster. This option will make that migration require
a lot of work. If you know for sure you will never use a redis cluster, then you can enable this option. 
If you are unsure, don't use this option. There is not any benefit.
```python
cache = RedisCache(redis_client, support_cluster=False)

# Changes keys to the following
key = f"rc:{fn.__module__}.{fn.__qualname__}:{b64encode(custom_serialized_args).decode('utf-8')}"
```

### Instance/Class methods
To cache instance/class methods it may require a little refactoring. This is because the `self`/`cls` cannot be 
serialized to JSON without custom serializers. The best way to handle caching class methods is to make a 
more specific static method to cache (or global function). For instance:

Don't do this:
```python
class MyClass:
    @cache.cache()
    def my_func(self, arg1, arg2):
        return self.some_arg + arg1 + arg2
```

Do this instead:
```python
class MyClass:
    def my_func(self, arg1, arg2):
        return self.my_cached_method(self.some_arg, arg1, arg2)
    
    @cache.cache()
    @staticmethod
    def my_cached_method(some_arg, arg1, arg2):
        return some_arg + arg1 + arg2
```

If you aren't using `self`/`cls` in the method, you can use the `@staticmethod` decorator to make it a static method. 
If you must use `self`/`cls` in your cached method and can't use the options suggested above, you will need to create 
a custom JSON key serializer for the `self`/`cls` object or you can use the Pickle serializer (which isn't recommended).
