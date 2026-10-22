import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import intel, oa, prep, sessions

app = FastAPI(title="mockmate API")
_origins = os.environ.get(
    "CORS_ORIGINS", "http://localhost:3100,http://127.0.0.1:3100"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins.split(",") if o.strip()],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(intel.router, prefix="/api")
app.include_router(oa.router, prefix="/api")
app.include_router(prep.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")


@app.get("/api/health")
def health():
    from . import db, cache
    return {"ok": True, "postgres": db.using_postgres(), "redis": cache.using_redis()}
