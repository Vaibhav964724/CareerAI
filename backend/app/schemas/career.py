from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class RoleRequirementItem(BaseModel):
    skill_name: str
    target_proficiency: int = Field(default=3, ge=1, le=5)
    importance: str = "high" # critical, high, medium, low
    prerequisites: List[str] = Field(default_factory=list)
    example_activities: List[str] = Field(default_factory=list)
    suggested_projects: List[str] = Field(default_factory=list)

class CareerRoleBase(BaseModel):
    slug: str
    title: str
    description: str
    industry: str = "Technology"
    average_salary_range: Optional[str] = None
    job_outlook: Optional[str] = None

class CareerRoleResponse(CareerRoleBase):
    id: int
    skills: List[RoleRequirementItem] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class SkillGapItem(BaseModel):
    skill_name: str
    current_proficiency: int
    target_proficiency: int
    gap: int
    priority: str # High, Medium, Low
    importance: str # critical, high, medium
    reason: str
    recommended_activity: str
    suggested_project: Optional[str] = None
    prerequisites: List[str] = Field(default_factory=list)

class SkillGapAnalysisResponse(BaseModel):
    student_id: int
    target_role: str
    overall_match_percentage: float
    total_skills_evaluated: int
    matched_skills_count: int
    gaps_count: int
    gaps: List[SkillGapItem]
    summary: str

class RoleComparisonItem(BaseModel):
    skill_name: str
    current_role_proficiency: int
    new_role_proficiency: int
    student_proficiency: int
    status: str # "retained", "gap_increased", "new_requirement", "sufficient"

class RoleComparisonResponse(BaseModel):
    current_role: str
    new_role: str
    transferable_skills: List[str]
    new_skills_needed: List[str]
    comparison_table: List[RoleComparisonItem]
    transition_feasibility: str # "Smooth", "Moderate", "Challenging"
    estimated_additional_weeks: float
    recommendation: str
