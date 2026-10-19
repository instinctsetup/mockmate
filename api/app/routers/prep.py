from fastapi import APIRouter
from ..intel import get_provider
from .. import oa

router = APIRouter()


@router.get("/prep/{company}")
def prep(company: str):
    provider = get_provider()
    intel = provider.search(f"{company} sde interview experience", 10)
    questions = oa.for_company(company)
    return {
        "company": company,
        "provider": provider.name,
        "intel": [vars(i) for i in intel],
        "oa_questions": questions,
        "note": ("intel items carry source URLs; company tags on questions are "
                 "community-reported; solutions are model-written and labeled"),
    }
