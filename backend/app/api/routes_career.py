import json
from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.career import CareerRole
from app.schemas.career import (
    CareerRoleResponse,
    RoleRequirementItem,
    SkillGapAnalysisResponse,
    RoleComparisonResponse
)
from app.services.career_service import (
    get_all_roles,
    get_role_by_slug_or_title,
    calculate_skill_gaps,
    compare_roles
)

router = APIRouter(prefix="/careers", tags=["Careers"])

class SkillGapRequest(BaseModel):
    student_id: int
    target_role: str

class CompareRolesRequest(BaseModel):
    current_role: str
    new_role: str
    student_skills: Dict[str, int] = {}

def role_to_response(role: CareerRole) -> CareerRoleResponse:
    skills = []
    for r in role.requirements:
        skills.append(RoleRequirementItem(
            skill_name=r.skill_name,
            target_proficiency=r.target_proficiency,
            importance=r.importance,
            prerequisites=json.loads(r.prerequisites) if r.prerequisites else [],
            example_activities=json.loads(r.example_activities) if r.example_activities else [],
            suggested_projects=json.loads(r.suggested_projects) if r.suggested_projects else []
        ))
    return CareerRoleResponse(
        id=role.id,
        slug=role.slug,
        title=role.title,
        description=role.description,
        industry=role.industry,
        average_salary_range=role.average_salary_range,
        job_outlook=role.job_outlook,
        skills=skills
    )

@router.get("", response_model=List[CareerRoleResponse])
def list_career_roles(db: Session = Depends(get_db)):
    """List all available standardized career roles."""
    roles = get_all_roles(db)
    return [role_to_response(r) for r in roles]

@router.get("/{identifier}", response_model=CareerRoleResponse)
def get_career_role(identifier: str, db: Session = Depends(get_db)):
    """Get single career role by slug or title."""
    role = get_role_by_slug_or_title(db, identifier)
    if not role:
        raise HTTPException(status_code=404, detail=f"Career role '{identifier}' not found.")
    return role_to_response(role)

@router.post("/skill-gaps", response_model=SkillGapAnalysisResponse)
def analyze_gaps(payload: SkillGapRequest, db: Session = Depends(get_db)):
    """Calculate deterministic skill gap scores between student skills and role requirements."""
    try:
        return calculate_skill_gaps(db, payload.student_id, payload.target_role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compare", response_model=RoleComparisonResponse)
def compare_career_paths(payload: CompareRolesRequest, db: Session = Depends(get_db)):
    """Compare two career paths and evaluate transition feasibility."""
    try:
        return compare_roles(db, payload.current_role, payload.new_role, payload.student_skills)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
