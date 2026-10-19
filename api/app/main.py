from fastapi import FastAPI
from .routers import intel

app = FastAPI(title="mockmate API")
app.include_router(intel.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"ok": True}
