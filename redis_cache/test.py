from redis import StrictRedis
from redis_cache import RedisCache
from mock import patch
import pytest

client = StrictRedis(host='redis', decode_responses=True)

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

    result = add_limit(6, 5)
    assert result == 11
    assert client.zrange('rc:redis_cache.test.add_limit:keys', 0, -1) == ['rc:redis_cache.test.add_limit:xNLCe8YInyx9Ab+8SVpHPg==', 'rc:redis_cache.test.add_limit:tGuG3MhBSir5Nid98G4XAg==']

    result = add_limit(3, 4)  
    assert result == 7
    assert client.zrange('rc:redis_cache.test.add_limit:keys', 0, -1) == ['rc:redis_cache.test.add_limit:tGuG3MhBSir5Nid98G4XAg==', 'rc:redis_cache.test.add_limit:nI4VRRx5stV01jmBXxCk0g==']

def test_invalidate_not_in_cache():
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=2)
    def add_invalidate_not_in_cache(arg1, arg2):
        return arg1 + arg2

    add_invalidate_not_in_cache(3, 4)
    add_invalidate_not_in_cache(4, 4)
    add_invalidate_not_in_cache.invalidate(5, 5)

    assert client.zrange('rc:redis_cache.test.add_invalidate_not_in_cache:keys', 0, -1) == ['rc:redis_cache.test.add_invalidate_not_in_cache:nI4VRRx5stV01jmBXxCk0g==', 'rc:redis_cache.test.add_invalidate_not_in_cache:kqR3/pNVmT9wYGRqjLlq1w==']
    assert client.get('rc:redis_cache.test.add_invalidate_not_in_cache:nI4VRRx5stV01jmBXxCk0g==') == '7'
    assert client.get('rc:redis_cache.test.add_invalidate_not_in_cache:kqR3/pNVmT9wYGRqjLlq1w==') == '8'
def test_invalidate_in_cache():
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=2)
    def add_invalidate_in_cache(arg1, arg2):
        return arg1 + arg2

    add_invalidate_in_cache(3, 4)
    add_invalidate_in_cache(4, 4)
    add_invalidate_in_cache.invalidate(4, 4)

    assert client.zrange('rc:redis_cache.test.add_invalidate_in_cache:keys', 0, -1) == ['rc:redis_cache.test.add_invalidate_in_cache:nI4VRRx5stV01jmBXxCk0g==']
    assert client.get('rc:redis_cache.test.add_invalidate_in_cache:nI4VRRx5stV01jmBXxCk0g==') == '7'
    assert client.exists('rc:redis_cache.test.add_invalidate_in_cache:kqR3/pNVmT9wYGRqjLlq1w==') == 0

def test_invalidate_all():
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=2)
    def add_invalidate_all(arg1, arg2):
        return arg1 + arg2

    add_invalidate_all(3, 4)
    add_invalidate_all(4, 4)
    assert client.zrange('rc:redis_cache.test.add_invalidate_all:keys', 0, -1) == ['rc:redis_cache.test.add_invalidate_all:nI4VRRx5stV01jmBXxCk0g==', 'rc:redis_cache.test.add_invalidate_all:kqR3/pNVmT9wYGRqjLlq1w==']
    add_invalidate_all.invalidate_all()
    # Check all the keys were removed
    assert client.zrange('rc:redis_cache.test.add_invalidate_all:keys', 0, -1) == []
    assert client.exists('rc:redis_cache.test.add_invalidate_all:kqR3/pNVmT9wYGRqjLlq1w==', 'c:redis_cache.test.add_invalidate_all:nI4VRRx5stV01jmBXxCk0g==') == 0
    