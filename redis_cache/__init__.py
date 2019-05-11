from functools import wraps
from hashlib import md5
from json import dumps, loads
from time import time
from base64 import b64encode


def get_cache_lua_fn(client):
    if not hasattr(client, '_lua_cache_fn'):
        client._lua_cache_fn = client.register_script("""
local ttl = tonumber(ARGV[2])
local value
if ttl > 0 then
  value = redis.call('SETEX', KEYS[1], ttl, ARGV[1])
else
  value = redis.call('SET', KEYS[1], ARGV[1])
end
local limit = tonumber(ARGV[3])
if limit > 0 then
  local time_parts = redis.call('TIME')
  local time = tonumber(time_parts[1] .. '.' .. time_parts[2])
  redis.call('ZADD', KEYS[2], time, KEYS[1])
  local count = tonumber(redis.call('ZCOUNT', KEYS[2], '-inf', '+inf'))
  local over = count - limit
  if over > 0 then
    local stale_keys_and_scores = redis.call('ZPOPMIN', KEYS[2], over)
    -- Remove the the scores and just leave the keys
    local stale_keys = {}
    for i = 1, #stale_keys_and_scores, 2 do
      stale_keys[#stale_keys+1] = stale_keys_and_scores[i]
    end
    redis.call('ZREM', KEYS[2], unpack(stale_keys))
    redis.call('DEL', unpack(stale_keys))
  end
end
return value
""")
    return client._lua_cache_fn

class RedisCache:
    def __init__(self, redis_client, prefix="rc", serializer=dumps, deserializer=loads):
        self.client = redis_client
        self.prefix = prefix
        self.serializer = serializer
        self.deserializer = deserializer

    def cache(self, ttl=0, limit=0, namespace=None):
        return CacheDecorator(
            redis_client=self.client,
            prefix=self.prefix,
            serializer=self.serializer,
            deserializer=self.deserializer,
            ttl=ttl,
            limit=limit,
            namespace=namespace
        )


class CacheDecorator:
    def __init__(self, redis_client, prefix="rc", serializer=dumps, deserializer=loads, ttl=0, limit=0, namespace=None):
        self.client = redis_client
        self.prefix = prefix
        self.serializer = serializer
        self.deserializer = deserializer
        self.ttl = ttl
        self.limit = limit
        self.namespace = namespace
        self.keys_key = None

    def get_key(self, args, kwargs):
        args_hash = str(b64encode(md5(self.serializer([args, kwargs]).encode('utf-8')).digest()), 'utf-8')
        return f'{self.prefix}:{self.namespace}:{args_hash}'

    def __call__(self, fn):
        self.namespace = self.namespace if self.namespace else f'{fn.__module__}.{fn.__name__}'
        self.keys_key = f'{self.prefix}:{self.namespace}:keys'

        @wraps(fn)
        def inner(*args, **kwargs):
            nonlocal self
            key = self.get_key(args, kwargs)
            result = self.client.get(key)
            if not result:
                result = fn(*args, **kwargs)
                result_json = self.serializer(result)
                get_cache_lua_fn(self.client)(keys=[key, self.keys_key], args=[result_json, self.ttl, self.limit])
            else:
                result = self.deserializer(result)
            return result

        inner.invalidate = self.invalidate
        inner.invalidate_all = self.invalidate_all
        return inner

    def invalidate(self, *args, **kwargs):
        key = self.get_key(args, kwargs)
        pipe = self.client.pipeline()
        pipe.delete(key)
        pipe.zrem(self.keys_key, key)
        pipe.execute()

    def invalidate_all(self, *args, **kwargs):
        all_keys = self.client.zrange(self.keys_key, 0, -1)
        self.client.delete(*all_keys, self.keys_key)
