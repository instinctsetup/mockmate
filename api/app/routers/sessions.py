from fastapi import APIRouter
from pydantic import BaseModel
from .. import db

router = APIRouter()


class SessionIn(BaseModel):
    company: str
    notes: str = ""


@router.post("/sessions")
def create_session(s: SessionIn):
    sid = db.save_session(s.company, s.notes)
    return {"id": sid, "postgres": db.using_postgres()}


@router.get("/sessions")
def sessions():
    return {"sessions": db.list_sessions(), "postgres": db.using_postgres()}
