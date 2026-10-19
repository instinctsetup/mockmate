import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from app import oa


def test_bank_nonempty_and_sourced():
    qs = oa.list_questions()
    assert len(qs) >= 10
    for q in qs:
        assert q["url"].startswith("https://")
        assert q["model_written"] is True
        assert "solution" not in q  # list view hides solutions


def test_detail_has_labeled_solution():
    q = oa.get_question("two-sum")
    assert q and q["solution"]
    assert q["model_written"] is True


def test_company_filter():
    rz = oa.for_company("razorpay")
    assert rz and all("razorpay" in [c.lower() for c in q["companies"]] for q in rz)


def test_topic_filter():
    dp = oa.list_questions(topic="dp")
    assert dp and all("dp" in q["topics"] for q in dp)
