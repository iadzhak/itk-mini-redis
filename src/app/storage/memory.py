import time
from threading import Lock

from cachetools import LRUCache

from app.storage.base import BaseStorage

type _K = str
type _V = tuple[float, str]
_V_DEFAULT = 0, None


class MemoryStorage(BaseStorage):
    def __init__(self, cache: LRUCache[_K, _V], lock: Lock) -> None:
        self._cache = cache
        self._lock = lock

    def put(self, key: str, value: str, ttl_seconds: int = 0) -> None:
        if ttl_seconds > 0:
            expire = time.time() + ttl_seconds
        else:
            expire = 0
        with self._lock:
            self._cache[key] = expire, value

    def get(self, key: str) -> str | None:
        expire, value = self._cache.get(key, _V_DEFAULT)
        if expire == 0 or expire > time.time():
            return value
        self.delete(key)
        return None

    def delete(self, key: str) -> None:
        with self._lock:
            self._cache.pop(key)

    def list(self, prefix: str) -> list[tuple[str, str]]:
        with self._lock:
            items = list(self._cache.items())
        now = time.time()
        return [
            (k, v[1])
            for k, v in items
            if k.startswith(prefix) and (v[0] == 0 or v[0] > now)
        ]
