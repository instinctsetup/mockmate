import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from app import db, cache


def test_graceful_fallback_without_services():
    # no DATABASE_URL/REDIS_URL in test env -> in-memory fallbacks
    assert db.using_postgres() is False
    assert cache.using_redis() is False
    sid = db.save_session("razorpay", "prep notes")
    assert any(s["id"] == sid for s in db.list_sessions())


def test_cache_roundtrip():
    cache.set_json("k1", {"a": 1}, ttl=60)
    assert cache.get_json("k1") == {"a": 1}
    assert cache.get_json("missing") is None
