from functools import wraps
from json import dumps, loads
from base64 import b64encode
from inspect import signature, Parameter

def compact_dump(value):
    return dumps(value, separators=(',', ':'), sort_keys=True)

def get_args(fn, args, kwargs):
    """
    This function parses the args and kwargs in the context of a function and creates unified
    dictionary of {<argument_name>: <value>}. This is useful
    because arguments can be passed as args or kwargs, and we want to make sure we cache
    them both the same. Otherwise there would be different caching for add(1, 2) and add(arg1=1, arg2=2)
    """
    arg_sig = signature(fn)
    standard_args = [param.name for param in arg_sig.parameters.values() if param.kind is param.POSITIONAL_OR_KEYWORD or param.kind is param.POSITIONAL_ONLY]
    allowed_kwargs = {param.name for param in arg_sig.parameters.values() if param.kind is param.POSITIONAL_OR_KEYWORD or param.kind is param.KEYWORD_ONLY}
    variable_args = [param.name for param in arg_sig.parameters.values() if param.kind is param.VAR_POSITIONAL]
    variable_kwargs = [param.name for param in arg_sig.parameters.values() if param.kind is param.VAR_KEYWORD]
    parsed_args = {}

    if standard_args or variable_args:
        for index, arg in enumerate(args):
            try:
                parsed_args[standard_args[index]] = arg
            except IndexError:
                # then fallback to using the positional varargs name
                if variable_args:
                    vargs_name = variable_args[0]
                    if vargs_name not in parsed_args:
                        parsed_args[vargs_name] = []

                    parsed_args[vargs_name].append(arg)


    if kwargs:
        for key, value in kwargs.items():
            if key in allowed_kwargs:
                parsed_args[key] = value
            elif variable_kwargs:
                vkwargs_name = variable_kwargs[0]
                if vkwargs_name not in parsed_args:
                    parsed_args[vkwargs_name] = {}
                parsed_args[vkwargs_name][key] = value

    for param in arg_sig.parameters.values():
        if param.name not in parsed_args and param.default is not Parameter.empty:
            parsed_args[param.name] = param.default

    return parsed_args


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


# Utility function to batch keys
def chunks(iterable, n):
    """Yield successive n-sized chunks from iterator."""
    _iterable = iter(iterable)
    while True:
        elements = []
        for _ in range(n):
            try:
                elements.append(next(_iterable))
            except StopIteration:
                break

        if not len(elements):
            break

        yield elements


class RedisCache:
    def __init__(self, redis_client, prefix="rc", serializer=compact_dump, deserializer=loads, key_serializer=None, support_cluster=True, exception_handler=None, active:bool=True):
        self.client = redis_client
        self.prefix = prefix
        self.serializer = serializer
        self.deserializer = deserializer
        self.key_serializer = key_serializer
        self.exception_handler = exception_handler
        self.support_cluster = support_cluster
        self.active = active

    def cache(self, ttl=0, limit=0, namespace=None, exception_handler=None):
        return CacheDecorator(
            redis_client=self.client,
            prefix=self.prefix,
            serializer=self.serializer,
            deserializer=self.deserializer,
            key_serializer=self.key_serializer,
            ttl=ttl,
            limit=limit,
            namespace=namespace,
            support_cluster=self.support_cluster,
            exception_handler=exception_handler or self.exception_handler,
            active=self.active
        )

    def mget(self, *fns_with_args):
        keys = []
        for fn_and_args in fns_with_args:
            fn = fn_and_args['fn']
            args = fn_and_args['args'] if 'args' in fn_and_args else []
            kwargs = fn_and_args['kwargs'] if 'kwargs' in fn_and_args else {}
            keys.append(fn.instance.get_key(args=args, kwargs=kwargs))

        results = self.client.mget(*keys)
        pipeline = self.client.pipeline()

        deserialized_results = []
        needs_pipeline = False
        for i, result in enumerate(results):
            if result is None:
                needs_pipeline = True

                fn_and_args = fns_with_args[i]
                fn = fn_and_args['fn']
                args = fn_and_args['args'] if 'args' in fn_and_args else []
                kwargs = fn_and_args['kwargs'] if 'kwargs' in fn_and_args else {}
                result = fn.instance.original_fn(*args, **kwargs)
                result_serialized = self.serializer(result)
                get_cache_lua_fn(self.client)(keys=[keys[i], fn.instance.keys_key], args=[result_serialized, fn.instance.ttl, fn.instance.limit], client=pipeline)
            else:
                result = self.deserializer(result)
            deserialized_results.append(result)

        if needs_pipeline:
            pipeline.execute()
        return deserialized_results

class CacheDecorator:
    def __init__(self, redis_client, prefix="rc", serializer=compact_dump, deserializer=loads, key_serializer=None, ttl=0, limit=0, namespace=None, support_cluster=True, exception_handler=None, active:bool=True):
        self.client = redis_client
        self.prefix = prefix
        self.serializer = serializer
        self.key_serializer = key_serializer
        self.deserializer = deserializer
        self.ttl = ttl
        self.limit = limit
        self.namespace = namespace
        self.exception_handler = exception_handler
        self.support_cluster = support_cluster
        self.keys_key = None
        self.original_fn = None
        self.active=active


    def get_full_prefix(self):
        if self.support_cluster:
            # Redis cluster requires keys operated in batch to be in the same key space. Redis cluster hashes the keys to
            # determine the key space. The braces specify which part of the key to hash (instead of the whole key).
            # See https://github.com/taylorhakes/python-redis-cache/issues/29  The `{prefix}:keys` and `{prefix}:args`
            # need to be in the same key space.
            return f'{{{self.prefix}:{self.namespace}}}'
        else:
            return f'{self.prefix}:{self.namespace}'

    def get_key(self, args, kwargs):
        normalized_args = get_args(self.original_fn, args, kwargs)

        if self.key_serializer:
            serialized_data = self.key_serializer(normalized_args)
        else:
            serialized_data = self.serializer(normalized_args)

        if isinstance(serialized_data, str):
            serialized_data = serialized_data.encode('utf-8')

        # Encode the value as base64 to avoid issues with {} and other special characters
        serialized_encoded_data = b64encode(serialized_data).decode('utf-8')

        return f'{self.get_full_prefix()}:{serialized_encoded_data}'

    def __call__(self, fn):
        self.namespace = self.namespace or f'{fn.__module__}.{fn.__qualname__}'
        self.keys_key = f'{self.get_full_prefix()}:keys'
        self.original_fn = fn

        @wraps(fn)
        def inner(*args, **kwargs):
            nonlocal self
            # Return the original function if we're not in active mode
            if not self.active:
                return fn(*args, **kwargs)
            key = self.get_key(args, kwargs)
            result = None

            exception_handled = False
            try:
                result = self.client.get(key)
            except Exception as e:
                if self.exception_handler:
                    # This allows people to handle failures in cache lookups
                    exception_handled = True
                    parsed_result = self.exception_handler(e, self.original_fn, args, kwargs)
            if result:
                parsed_result = self.deserializer(result)
            elif not exception_handled:
                parsed_result = fn(*args, **kwargs)
                result_serialized = self.serializer(parsed_result)
                get_cache_lua_fn(self.client)(keys=[key, self.keys_key], args=[result_serialized, self.ttl, self.limit])

            return parsed_result

        inner.invalidate = self.invalidate
        inner.invalidate_all = self.invalidate_all
        inner.get_full_prefix = self.get_full_prefix
        inner.instance = self
        return inner

    def invalidate(self, *args, **kwargs):
        key = self.get_key(args, kwargs)
        pipe = self.client.pipeline()
        pipe.delete(key)
        pipe.zrem(self.keys_key, key)
        pipe.execute()

    def invalidate_all(self, *args, **kwargs):
        chunks_gen = chunks(self.client.scan_iter(f'{self.get_full_prefix()}:*'), 500)
        for keys in chunks_gen:
            self.client.delete(*keys)
