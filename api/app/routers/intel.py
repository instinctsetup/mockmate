from fastapi import APIRouter, Query
from ..intel import get_provider
from .. import cache

router = APIRouter()


@router.get("/intel/search")
def search(q: str = Query(..., min_length=2), limit: int = 10):
    key = f"intel:{q}:{limit}"
    hit = cache.get_json(key)
    if hit is not None:
        hit["cached"] = True
        return hit
    provider = get_provider()
    items = provider.search(q, limit)
    out = {
        "provider": provider.name,
        "results": [vars(i) for i in items],
        "note": "model-written answers are labeled model_written=true; "
                "every item carries a source URL.",
        "cached": False,
    }
    cache.set_json(key, out)
    return out
