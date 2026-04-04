from __future__ import annotations

from sqlmodel import Session, select

from app.models import Candidate, Experience, Skill


def seed_resume_if_empty(session: Session) -> Candidate:
    existing = session.exec(select(Candidate)).first()
    if existing:
        return existing

    candidate = Candidate(
        full_name="Bikramjit Ganguly",
        phone="408-242-8992",
        email="gangulybikramjit@hotmail.com",
        linkedin_url="https://www.linkedin.com/in/bganguly/",
        github_url="https://github.com/bganguly",
        work_authorization="US Citizen",
        location="San Jose, CA 95129",
        summary=(
            "Senior Full-Stack Engineer with 20+ years in IT and 17+ years in API-driven web "
            "platforms, distributed systems, and cloud/serverless architecture."
        ),
    )
    session.add(candidate)
    session.commit()
    session.refresh(candidate)

    experience_rows = [
        Experience(
            candidate_id=candidate.id,
            company="College Board",
            role="Senior Full-Stack Engineer (Contract)",
            start_period="Jul 2022",
            end_period="Present",
            highlights="React + TypeScript SPAs and Node/Python/Java serverless APIs on AWS.",
        ),
        Experience(
            candidate_id=candidate.id,
            company="Ayla Networks",
            role="Dev Manager",
            start_period="Mar 2017",
            end_period="Feb 2022",
            highlights="Led 7 engineers across React/Angular/Spring/Python/GraphQL and ETL.",
        ),
        Experience(
            candidate_id=candidate.id,
            company="Intuit Inc",
            role="Senior Software Engineer",
            start_period="Sep 2014",
            end_period="Dec 2016",
            highlights="Angular app leadership with integration work in Java/Spring.",
        ),
    ]

    skill_rows = [
        Skill(candidate_id=candidate.id, name="React", category="frontend"),
        Skill(candidate_id=candidate.id, name="TypeScript", category="frontend"),
        Skill(candidate_id=candidate.id, name="Node.js", category="backend"),
        Skill(candidate_id=candidate.id, name="FastAPI", category="backend"),
        Skill(candidate_id=candidate.id, name="Python", category="backend"),
        Skill(candidate_id=candidate.id, name="AWS Lambda", category="cloud"),
        Skill(candidate_id=candidate.id, name="DynamoDB", category="database"),
        Skill(candidate_id=candidate.id, name="PostgreSQL", category="database"),
    ]

    session.add_all(experience_rows + skill_rows)
    session.commit()
    session.refresh(candidate)
    return candidate
