from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SkillAssessmentItem(BaseModel):
    skill_name: str
    proficiency: int = Field(default=0, ge=0, le=5) # 0 to 5 scale

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: Optional[str] = None
    degree: str = Field(..., min_length=2, max_length=100)
    branch: str = Field(..., min_length=2, max_length=100)
    year_of_study: int = Field(default=3, ge=1, le=5)
    gpa: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    interests: List[str] = Field(default_factory=list)
    existing_projects: List[str] = Field(default_factory=list)
    completed_certifications: List[str] = Field(default_factory=list)
    target_role: str = Field(..., min_length=2, max_length=100)
    preferred_industry: str = Field(default="Technology")
    weekly_hours: float = Field(default=10.0, gt=0, le=80)
    timeline_months: int = Field(default=6, ge=1, le=48)

class StudentCreate(StudentBase):
    skills: List[SkillAssessmentItem] = Field(default_factory=list)

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    year_of_study: Optional[int] = None
    gpa: Optional[float] = None
    interests: Optional[List[str]] = None
    existing_projects: Optional[List[str]] = None
    completed_certifications: Optional[List[str]] = None
    target_role: Optional[str] = None
    preferred_industry: Optional[str] = None
    weekly_hours: Optional[float] = None
    timeline_months: Optional[int] = None
    skills: Optional[List[SkillAssessmentItem]] = None

class StudentResponse(StudentBase):
    id: int
    skills: List[SkillAssessmentItem] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
