"""Cache: Redis when REDIS_URL is reachable, else an in-process dict."""
import os
import json
import time

_redis = None
_mem: dict[str, tuple[float, str]] = {}
TTL = 24 * 3600


def _client():
    global _redis
    if _redis is False:
        return None
    if _redis is not None:
        return _redis
    url = os.environ.get("REDIS_URL")
    if not url:
        _redis = False
        return None
    try:
        import redis
        r = redis.from_url(url, socket_connect_timeout=1)
        r.ping()
        _redis = r
        return r
    except Exception:
        _redis = False
        return None


def using_redis() -> bool:
    return _client() is not None


def get_json(key: str):
    r = _client()
    if r is not None:
        raw = r.get(key)
        return json.loads(raw) if raw else None
    ent = _mem.get(key)
    if ent and ent[0] > time.time():
        return json.loads(ent[1])
    return None


def set_json(key: str, value, ttl: int = TTL):
    raw = json.dumps(value)
    r = _client()
    if r is not None:
        r.setex(key, ttl, raw)
    else:
        _mem[key] = (time.time() + ttl, raw)
