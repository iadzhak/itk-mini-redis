import time
from threading import Lock

import pytest
from cachetools import LRUCache

from app.storage.memory import _K, _V, MemoryStorage


class TestMemoryStorage:
    MAX_SIZE = 10

    def make_storage_and_cache(self) -> tuple[MemoryStorage, LRUCache[_K, _V]]:
        cache = LRUCache(self.MAX_SIZE)
        lock = Lock()
        return MemoryStorage(cache, lock), cache

    def test_put(self):
        storage, cache = self.make_storage_and_cache()
        key, value, ttl = 'key', 'value', 12
        storage.put(key, value, ttl)
        found = cache.get(key)
        assert found is not None
        f_ttl, f_v = found
        assert f_ttl > time.time()
        assert f_v == value

    def test_get_exist(self):
        storage, cache = self.make_storage_and_cache()
        key, value = 'key', 'value'
        cache[key] = 0, value
        found = storage.get(key)
        assert found is not None
        assert found == value

    def test_get_not_exist(self):
        storage, cache = self.make_storage_and_cache()
        key, value = 'key', 'value'
        cache[key] = 0, value
        key_2 = 'key_2'
        found = storage.get(key_2)
        assert found is None

    def test_get_expired(self):
        storage, cache = self.make_storage_and_cache()
        key, value, ttl = 'key', 'value', 1
        cache[key] = ttl, value
        time.sleep(ttl + 0.1)
        found = storage.get(key)
        assert found is None

    @pytest.mark.parametrize(
        'key1, key2, value1',
        (
            ('key1', 'key1', 'value'),
            ('key1', 'key2', 'value'),
        ),
        ids=['exist', 'not_exist'],
    )
    def test_delete(self, key1, key2, value1):
        storage, cache = self.make_storage_and_cache()
        key, value = 'key', 'value'
        cache[key] = 0, value
        storage.delete(key)
        assert key not in cache

    def test_list(self):
        storage, cache = self.make_storage_and_cache()
        items = [('pr:1', 'val1'), ('pr:2', 'val2'), ('xr:2', 'val2')]
        for key, value in items:
            cache[key] = 0, value
        found = storage.list('pr:')
        assert found is not None
        assert ('pr:1', 'val1') in found
        assert ('pr:2', 'val2') in found
        assert ('xr:2', 'val2') not in found
