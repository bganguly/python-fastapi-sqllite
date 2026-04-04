# Resume Profile API (FastAPI + SQLite)

A compact end-to-end FastAPI project with persistence, built to be implementable in a couple of hours.

## Quickstart

1. Check Python, create venv (if missing), and activate it

```bash
python3 --version
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python3 -m pip --version
```

2. Install dependencies
3. Run the API

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

## What this includes

- FastAPI service with OpenAPI docs
- SQLite persistence using SQLModel
- Relational entities: candidate, experiences, skills
- CRUD endpoints for candidate and nested resources
- Resume seed endpoint with your profile data preloaded
- One API test proving seed + read flow works

## Project layout

- app/main.py
- app/db.py
- app/models.py
- app/resume_seed.py
- app/routers/candidates.py
- tests/test_api.py

API docs:

- http://127.0.0.1:8000/docs

## Useful endpoints

- GET /health
- POST /seed/resume
- GET /candidates
- POST /candidates
- GET /candidates/{candidate_id}
- PATCH /candidates/{candidate_id}
- DELETE /candidates/{candidate_id}
- POST /candidates/{candidate_id}/experiences
- GET /candidates/{candidate_id}/experiences
- POST /candidates/{candidate_id}/skills
- GET /candidates/{candidate_id}/skills

## Run tests

```bash
python3 -m pytest -q
```

## Notes

- Default DB path: app.db in project root
- Set AUTO_SEED_ON_STARTUP=false to avoid automatic seed
