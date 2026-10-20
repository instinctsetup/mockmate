import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)


def test_sessions_roundtrip():
    r = c.post("/api/sessions", json={"company": "razorpay", "notes": "x"})
    assert r.status_code == 200
    sid = r.json()["id"]
    r = c.get("/api/sessions")
    assert any(s["id"] == sid for s in r.json()["sessions"])


def test_oa_unknown_id_404():
    assert c.get("/api/oa/questions/does-not-exist").status_code == 404


def test_prep_endpoint():
    r = c.get("/api/prep/razorpay")
    assert r.status_code == 200
    body = r.json()
    assert body["oa_questions"] and body["note"]
