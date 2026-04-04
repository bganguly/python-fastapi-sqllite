from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db import get_session
from app.models import (
    Candidate,
    CandidateCreate,
    CandidateDetails,
    CandidateRead,
    CandidateUpdate,
    Experience,
    ExperienceCreate,
    ExperienceRead,
    Skill,
    SkillCreate,
    SkillRead,
)

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("", response_model=CandidateRead, status_code=status.HTTP_201_CREATED)
def create_candidate(payload: CandidateCreate, session: Session = Depends(get_session)) -> Candidate:
    candidate = Candidate.model_validate(payload)
    session.add(candidate)
    session.commit()
    session.refresh(candidate)
    return candidate


@router.get("", response_model=list[CandidateRead])
def list_candidates(session: Session = Depends(get_session)) -> list[Candidate]:
    return list(session.exec(select(Candidate)).all())


@router.get("/{candidate_id}", response_model=CandidateDetails)
def get_candidate(candidate_id: int, session: Session = Depends(get_session)) -> CandidateDetails:
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    experiences = list(
        session.exec(select(Experience).where(
            Experience.candidate_id == candidate_id)).all()
    )
    skills = list(session.exec(select(Skill).where(
        Skill.candidate_id == candidate_id)).all())

    return CandidateDetails(
        **candidate.model_dump(),
        experiences=[ExperienceRead.model_validate(
            item) for item in experiences],
        skills=[SkillRead.model_validate(item) for item in skills],
    )


@router.patch("/{candidate_id}", response_model=CandidateRead)
def update_candidate(
    candidate_id: int, payload: CandidateUpdate, session: Session = Depends(get_session)
) -> Candidate:
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(candidate, field, value)

    session.add(candidate)
    session.commit()
    session.refresh(candidate)
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: int, session: Session = Depends(get_session)) -> Response:
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    experiences = list(
        session.exec(select(Experience).where(
            Experience.candidate_id == candidate_id)).all()
    )
    skills = list(session.exec(select(Skill).where(
        Skill.candidate_id == candidate_id)).all())
    for row in experiences + skills:
        session.delete(row)

    session.delete(candidate)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{candidate_id}/experiences", response_model=ExperienceRead, status_code=201)
def create_experience(
    candidate_id: int, payload: ExperienceCreate, session: Session = Depends(get_session)
) -> Experience:
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    experience = Experience(candidate_id=candidate_id, **payload.model_dump())
    session.add(experience)
    session.commit()
    session.refresh(experience)
    return experience


@router.get("/{candidate_id}/experiences", response_model=list[ExperienceRead])
def list_experiences(candidate_id: int, session: Session = Depends(get_session)) -> list[Experience]:
    return list(session.exec(select(Experience).where(Experience.candidate_id == candidate_id)).all())


@router.post("/{candidate_id}/skills", response_model=SkillRead, status_code=201)
def create_skill(candidate_id: int, payload: SkillCreate, session: Session = Depends(get_session)) -> Skill:
    candidate = session.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    skill = Skill(candidate_id=candidate_id, **payload.model_dump())
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.get("/{candidate_id}/skills", response_model=list[SkillRead])
def list_skills(candidate_id: int, session: Session = Depends(get_session)) -> list[Skill]:
    return list(session.exec(select(Skill).where(Skill.candidate_id == candidate_id)).all())
