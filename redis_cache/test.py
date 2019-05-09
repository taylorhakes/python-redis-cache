from redis import StrictRedis
from redis_cache import RedisCache
from mock import patch
import pytest

client = StrictRedis(host='redis')

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
        mock_get.assert_called_once_with('rc:redis_cache.test.add_basic:nI4VRRx5stV01jmBXxCk0g==')
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

    with patch.object(cache, 'set_cache', wraps=cache.set_cache) as mock_set:
        result = add_limit(6, 5)
        assert result == 11
        assert client.zcount('rc:redis_cache.test.add_limit:keys', '-inf', '+inf') == 2
        mock_set.assert_not_called()

    with patch.object(cache, 'set_cache', wraps=cache.set_cache) as mock_set:
        result = add_limit(3, 4)    
        assert result == 7
        assert client.zcount('rc:redis_cache.test.add_limit:keys', '-inf', '+inf') == 2
        mock_set.assert_called()


