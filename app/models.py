from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class CandidateBase(SQLModel):
    full_name: str
    phone: str
    email: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    work_authorization: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None


class Candidate(CandidateBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    experiences: List["Experience"] = Relationship(back_populates="candidate")
    skills: List["Skill"] = Relationship(back_populates="candidate")


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(SQLModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    work_authorization: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None


class CandidateRead(CandidateBase):
    id: int


class ExperienceBase(SQLModel):
    company: str
    role: str
    start_period: str
    end_period: str
    highlights: str


class Experience(ExperienceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="candidate.id", index=True)
    candidate: Optional[Candidate] = Relationship(back_populates="experiences")


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceRead(ExperienceBase):
    id: int
    candidate_id: int


class SkillBase(SQLModel):
    name: str
    category: Optional[str] = None


class Skill(SkillBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="candidate.id", index=True)
    candidate: Optional[Candidate] = Relationship(back_populates="skills")


class SkillCreate(SkillBase):
    pass


class SkillRead(SkillBase):
    id: int
    candidate_id: int


class CandidateDetails(CandidateRead):
    experiences: List[ExperienceRead] = Field(default_factory=list)
    skills: List[SkillRead] = Field(default_factory=list)
