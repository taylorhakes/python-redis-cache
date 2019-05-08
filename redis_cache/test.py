from fakeredis import FakeStrictRedis
from redis_cache import RedisCache
from mock import patch


def test_basic_check():
    client = FakeStrictRedis()
    cache = RedisCache(redis_client=client)

    @cache.cache()
    def add(arg1, arg2):
        return arg1 + arg2

    result = add(3, 4)    
    assert result == 7

    with patch.object(client, 'get', wraps=client.get) as mock_get:
        with patch.object(client, 'set', wraps=client.set) as mock_set:
            result = add(3, 4)
            mock_get.assert_called_once_with('rc.redis_cache.test.add=nI4VRRx5stV01jmBXxCk0g==')
            mock_set.assert_not_called()
    assert result == 7

    result = add(5, 5)
    assert result == 10

def test_ttl():
    client = FakeStrictRedis()
    cache = RedisCache(redis_client=client)

    @cache.cache(ttl=100)
    def add(arg1, arg2):
        return arg1 + arg2

    result = add(3, 4)    
    assert result == 7

    result = add(3, 4)    
    assert result == 7

def test_limit():
    client = FakeStrictRedis()
    cache = RedisCache(redis_client=client)

    @cache.cache(limit=1)
    def add(arg1, arg2):
        return arg1 + arg2

    result = add(3, 4)    
    assert result == 7

    with patch.object(client, 'zpopmin', wraps=client.set) as mock_zpopmin:
        mock_zpopmin.return_value = [('rc.redis_cache.test.add=nI4VRRx5stV01jmBXxCk0g==', 1)]
        result = add(5, 5)
        mock_zpopmin.assert_called_once_with('rc.redis_cache.test.add.keys', 1)
        assert client.zcount('rc.redis_cache.test.add.keys', '-inf', '+inf') == 1

    assert result == 10
