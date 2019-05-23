from redis import StrictRedis
from redis_cache import RedisCache
from mock import patch
import pickle
import pytest
import base64
import zlib

client = StrictRedis(host='redis', decode_responses=True)
client_no_decode = StrictRedis(host='redis')

@pytest.fixture(scope="session", autouse=True)
def clear_redis(request):
    client.flushall()

def test_basic_check():
    cache = RedisCache(redis_client=client)

    @cache.cache()
    def add_basic(arg1, arg2):
        return arg1 + arg2

    result = add_basic(3, 4)    
    assert result == 7

    with patch.object(client, 'get', wraps=client.get) as mock_get:
        result = add_basic(3, 4)
        mock_get.assert_called_once_with('rc:redis_cache.test.add_basic:[[3, 4], {}]')
    assert result == 7

    result = add_basic(5, 5)
    assert result == 10

def test_ttl():
    cache = RedisCache(redis_client=client)

    @cache.cache(ttl=100)
    def add_ttl(arg1, arg2):
        return arg1 + arg2

    result = add_ttl(3, 4)    
    assert result == 7

    result = add_ttl(3, 4)    
    assert result == 7

def test_limit():
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=2)
    def add_limit(arg1, arg2):
        return arg1 + arg2

    result = add_limit(3, 4)    
    assert result == 7

    result = add_limit(5, 5)
    assert client.zcount('rc:redis_cache.test.add_limit:keys', '-inf', '+inf') == 2
    assert result == 10

    result = add_limit(6, 5)
    assert client.zcount('rc:redis_cache.test.add_limit:keys', '-inf', '+inf') == 2
    assert result == 11

    result = add_limit(6, 5)
    assert result == 11
    assert client.zrange('rc:redis_cache.test.add_limit:keys', 0, -1) == ['rc:redis_cache.test.add_limit:[[5, 5], {}]', 'rc:redis_cache.test.add_limit:[[6, 5], {}]']

    result = add_limit(3, 4)  
    assert result == 7
    assert client.zrange('rc:redis_cache.test.add_limit:keys', 0, -1) == ['rc:redis_cache.test.add_limit:[[6, 5], {}]', 'rc:redis_cache.test.add_limit:[[3, 4], {}]']

def test_invalidate_not_in_cache():
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=2)
    def add_invalidate_not_in_cache(arg1, arg2):
        return arg1 + arg2

    add_invalidate_not_in_cache(3, 4)
    add_invalidate_not_in_cache(4, 4)
    add_invalidate_not_in_cache.invalidate(5, 5)

    assert client.zrange('rc:redis_cache.test.add_invalidate_not_in_cache:keys', 0, -1) == ['rc:redis_cache.test.add_invalidate_not_in_cache:[[3, 4], {}]', 'rc:redis_cache.test.add_invalidate_not_in_cache:[[4, 4], {}]']
    assert client.get('rc:redis_cache.test.add_invalidate_not_in_cache:[[3, 4], {}]') == '7'
    assert client.get('rc:redis_cache.test.add_invalidate_not_in_cache:[[4, 4], {}]') == '8'
def test_invalidate_in_cache():
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=2)
    def add_invalidate_in_cache(arg1, arg2):
        return arg1 + arg2

    add_invalidate_in_cache(3, 4)
    add_invalidate_in_cache(4, 4)
    assert client.zrange('rc:redis_cache.test.add_invalidate_in_cache:keys', 0, -1) == ['rc:redis_cache.test.add_invalidate_in_cache:[[3, 4], {}]', 'rc:redis_cache.test.add_invalidate_in_cache:[[4, 4], {}]']


    add_invalidate_in_cache.invalidate(4, 4)

    assert client.zrange('rc:redis_cache.test.add_invalidate_in_cache:keys', 0, -1) == ['rc:redis_cache.test.add_invalidate_in_cache:[[3, 4], {}]']
    assert client.get('rc:redis_cache.test.add_invalidate_in_cache:[[3, 4], {}]') == '7'
    assert client.exists('rc:redis_cache.test.add_invalidate_in_cache:[[4, 4], {}]') == 0

def test_invalidate_all():
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=2)
    def add_invalidate_all(arg1, arg2):
        return arg1 + arg2

    add_invalidate_all(3, 4)
    add_invalidate_all(4, 4)
    assert client.zrange('rc:redis_cache.test.add_invalidate_all:keys', 0, -1) == ['rc:redis_cache.test.add_invalidate_all:[[3, 4], {}]', 'rc:redis_cache.test.add_invalidate_all:[[4, 4], {}]']
    add_invalidate_all.invalidate_all()
    # Check all the keys were removed
    assert client.zrange('rc:redis_cache.test.add_invalidate_all:keys', 0, -1) == []
    assert client.exists('rc:redis_cache.test.add_invalidate_all:[[3, 4], {}]', 'rc:redis_cache.test.add_invalidate_all:[[4, 4], {}]') == 0

class Result:
    def __init__(self, arg1, arg2):
        self.sum = arg1 + arg2

class Arg:
    def __init__(self, value):
        self.value = value


def test_custom_serializer():
    cache = RedisCache(redis_client=client_no_decode, serializer=pickle.dumps, deserializer=pickle.loads)

    @cache.cache()
    def add_custom_serializer(arg1, arg2):
        return Result(
            arg1.value,
            arg2.value
        )

    result = add_custom_serializer(Arg(2), Arg(3))    
    assert result.sum == 5

    with patch.object(client_no_decode, 'get', wraps=client_no_decode.get) as mock_get:
        result = add_custom_serializer(Arg(2), Arg(3))    
        assert result.sum == 5
        mock_get.assert_called_once_with('rc:redis_cache.test.add_custom_serializer:gANdcQAoY3JlZGlzX2NhY2hlLnRlc3QKQXJnCnEBKYFxAn1xA1gFAAAAdmFsdWVxBEsCc2JoASmBcQV9cQZoBEsDc2KGcQd9cQhlLg==')

    result = add_custom_serializer(Arg(5), Arg(5))
    assert result.sum == 10

def test_custom_serializer_with_compress():
    def dumps(value):
        return zlib.compress(pickle.dumps(value))

    def loads(value):
        return pickle.loads(zlib.decompress(value))

    cache = RedisCache(redis_client=client_no_decode, serializer=dumps, deserializer=loads)

    @cache.cache()
    def add_custom_serializer(arg1, arg2):
        return Result(
            arg1.value,
            arg2.value
        )

    result = add_custom_serializer(Arg(2), Arg(3))    
    assert result.sum == 5

    with patch.object(client_no_decode, 'get', wraps=client_no_decode.get) as mock_get:
        result = add_custom_serializer(Arg(2), Arg(3))    
        assert result.sum == 5
        mock_get.assert_called_once_with('rc:redis_cache.test.add_custom_serializer:eJxrYI4tZNBILkpNySyOT05MzkjVK0ktLuFyLErnKmTUbCxkqi1kjmBlYGAoS8wpTS1k8WYqTsoASbDWFrJlsHgzFye1FbLXFnKk6gEAgloWhw==')

    result = add_custom_serializer(Arg(5), Arg(5))
    assert result.sum == 10