import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from app.intel import get_provider


def test_fixture_default():
    p = get_provider()
    assert p.name == "fixture"


def test_fixture_results_have_sources():
    items = get_provider().search("razorpay sde interview")
    assert items
    for i in items:
        assert i.url.startswith("http")
        assert i.model_written is False


def test_api_roundtrip():
    from fastapi.testclient import TestClient
    from app.main import app
    c = TestClient(app)
    r = c.get("/api/health")
    assert r.status_code == 200 and r.json()["ok"]
    r = c.get("/api/intel/search", params={"q": "razorpay interview"})
    assert r.status_code == 200
    assert all(i["url"].startswith("http") for i in r.json()["results"])
