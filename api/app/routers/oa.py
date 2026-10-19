from fastapi import APIRouter, HTTPException
from .. import oa

router = APIRouter()

COMPANY_TAG_NOTE = ("company tags are community-reported associations, not "
                    "verified claims; solutions are model-written and labeled")


@router.get("/oa/questions")
def questions(topic: str | None = None, difficulty: str | None = None, company: str | None = None):
    return {"questions": oa.list_questions(topic, difficulty, company), "note": COMPANY_TAG_NOTE}


@router.get("/oa/questions/{qid}")
def question(qid: str):
    q = oa.get_question(qid)
    if not q:
        raise HTTPException(404, "unknown question id")
    return {"question": q, "note": COMPANY_TAG_NOTE}
