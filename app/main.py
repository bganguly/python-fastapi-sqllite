from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import Session

from app.config import auto_seed_enabled
from app.db import create_db_and_tables, engine, get_session
from app.resume_seed import seed_resume_if_empty
from app.routers.candidates import router as candidates_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    if auto_seed_enabled():
        with Session(engine) as session:
            seed_resume_if_empty(session)
    yield


app = FastAPI(title="Resume Profile API", version="1.0.0", lifespan=lifespan)
app.include_router(candidates_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/seed/resume")
def seed_resume(session: Session = Depends(get_session)) -> dict[str, int | str]:
    candidate = seed_resume_if_empty(session)
    return {"message": "resume seeded", "candidate_id": candidate.id}
