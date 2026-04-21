
from fastapi import FastAPI
from api.routes import jobs

app = FastAPI(title="Job Platform")

app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

@app.get("/health")
def health():
    return {"status": "ok"}