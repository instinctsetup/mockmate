from fastapi import FastAPI
from .routers import intel, oa, prep, sessions

app = FastAPI(title="mockmate API")
app.include_router(intel.router, prefix="/api")
app.include_router(oa.router, prefix="/api")
app.include_router(prep.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")


@app.get("/api/health")
def health():
    from . import db, cache
    return {"ok": True, "postgres": db.using_postgres(), "redis": cache.using_redis()}
