from functools import wraps
from hashlib import md5
from json import dumps, loads
from time import time
from base64 import b64encode


class RedisCache:
    def __init__(self, redis_client, prefix="rc", serializer=dumps, deserializer=loads):
        self.client = redis_client
        self.prefix = prefix
        self.serialzer = serializer
        self.deserializer = deserializer

    def cache(self, ttl=None, limit=None, namespace=None):
        def decorator(fn):
            nonlocal namespace
            nonlocal ttl
            nonlocal limit

            if not namespace:
                namespace = f'{fn.__module__}.{fn.__name__}'
        
            @wraps(fn)
            def inner(*args, **kwargs):
                args_hash = str(b64encode(md5(self.serialzer([args, kwargs]).encode('utf-8')).digest()), 'utf-8')
                key = f'{self.prefix}.{namespace}={args_hash}'
                print('key', key)
                result = self.client.get(key)
                if not result:
                    result = fn(*args, **kwargs)
                    result_json = self.serialzer(result)
                    pipe = self.client.pipeline()
                    if ttl:
                        pipe.setex(key, ttl, result_json)
                    else:
                        pipe.set(key, result_json)

                    keys_key = f'{self.prefix}.{namespace}.keys'
                    pipe.zadd(keys_key, {key: time()})
                    pipe.execute()

                    if limit:
                        result_count = self.client.zcount(keys_key, '-inf', '+inf')
                        over_limit = result_count - limit
                        if over_limit > 0:
                            stale_key_items = self.client.zpopmin(keys_key, over_limit)
                            stale_keys = (key for key, score in stale_key_items)
                            self.client.zrem(keys_key, *stale_keys)

                else:
                    result = self.deserializer(result)
                return result

            return inner
        return decorator



        
        