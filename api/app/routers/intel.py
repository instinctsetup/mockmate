from fastapi import APIRouter, Query
from ..intel import get_provider

router = APIRouter()


@router.get("/intel/search")
def search(q: str = Query(..., min_length=2), limit: int = 10):
    provider = get_provider()
    items = provider.search(q, limit)
    return {
        "provider": provider.name,
        "results": [vars(i) for i in items],
        "note": "model-written answers are labeled model_written=true; "
                "every item carries a source URL.",
    }
