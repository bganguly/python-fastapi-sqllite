from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.db import get_session
from app.main import app


def test_seed_and_get_candidate() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_session

    with TestClient(app) as client:
        seed_response = client.post("/seed/resume")
        assert seed_response.status_code == 200
        candidate_id = seed_response.json()["candidate_id"]

        fetch_response = client.get(f"/candidates/{candidate_id}")
        assert fetch_response.status_code == 200
        payload = fetch_response.json()
        assert payload["full_name"] == "Bikramjit Ganguly"
        assert len(payload["experiences"]) >= 1
        assert len(payload["skills"]) >= 1

    app.dependency_overrides.clear()
