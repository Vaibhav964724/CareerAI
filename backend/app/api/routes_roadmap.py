import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.roadmap import Roadmap, RoadmapMilestone, RoadmapRevisionHistory
from app.schemas.roadmap import (
    RoadmapResponse,
    RoadmapMilestoneResponse,
    MilestoneStatusUpdate,
    RoadmapRevisionResponse,
    LearningResourceItem,
    RecommendedProjectItem
)
from app.services.roadmap_service import generate_roadmap, revise_roadmap
from app.agent.tools import update_milestone_progress

router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])

class GenerateRoadmapRequest(BaseModel):
    student_id: int
    target_role: str
    weekly_hours: float = 10.0

def milestone_to_response(m: RoadmapMilestone) -> RoadmapMilestoneResponse:
    resources = [
        LearningResourceItem(**r)
        for r in (json.loads(m.learning_resources) if m.learning_resources else [])
    ]
    project = None
    if m.recommended_project:
        try:
            p_dict = json.loads(m.recommended_project)
            if p_dict and "title" in p_dict:
                project = RecommendedProjectItem(
                    title=p_dict.get("title", ""),
                    description=p_dict.get("description", ""),
                    deliverables=p_dict.get("deliverables", []),
                    verification_checklist=p_dict.get("verification_checklist", [])
                )
        except Exception:
            project = None

    return RoadmapMilestoneResponse(
        id=m.id,
        roadmap_id=m.roadmap_id,
        title=m.title,
        phase_number=m.phase_number,
        phase_name=m.phase_name,
        description=m.description,
        required_skills=json.loads(m.required_skills) if m.required_skills else [],
        priority=m.priority,
        estimated_hours=m.estimated_hours,
        estimated_weeks=m.estimated_weeks,
        prerequisites=json.loads(m.prerequisites) if m.prerequisites else [],
        learning_resources=resources,
        recommended_project=project,
        completion_criteria=m.completion_criteria,
        deadline=m.deadline,
        status=m.status,
        order_index=m.order_index,
        completed_at=m.completed_at
    )

def roadmap_to_response(rm: Roadmap) -> RoadmapResponse:
    milestone_resps = [milestone_to_response(m) for m in rm.milestones]
    completed_count = sum(1 for m in rm.milestones if m.status == "completed")
    total_count = len(rm.milestones)
    completion_pct = round((completed_count / total_count * 100), 1) if total_count > 0 else 0.0

    return RoadmapResponse(
        id=rm.id,
        student_id=rm.student_id,
        target_role=rm.target_role,
        total_estimated_weeks=rm.total_estimated_weeks,
        weekly_hours=rm.weekly_hours,
        status=rm.status,
        version=rm.version,
        milestones=milestone_resps,
        completed_milestones_count=completed_count,
        total_milestones_count=total_count,
        completion_percentage=completion_pct,
        created_at=rm.created_at,
        updated_at=rm.updated_at
    )

@router.post("/generate", response_model=RoadmapResponse, status_code=status.HTTP_201_CREATED)
def create_roadmap(payload: GenerateRoadmapRequest, db: Session = Depends(get_db)):
    """Generate a personalized phased career roadmap."""
    try:
        rm = generate_roadmap(db, payload.student_id, payload.target_role, payload.weekly_hours)
        return roadmap_to_response(rm)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/student/{student_id}", response_model=RoadmapResponse)
def get_active_roadmap(student_id: int, db: Session = Depends(get_db)):
    """Retrieve current active roadmap for a student."""
    rm = db.query(Roadmap).filter(
        Roadmap.student_id == student_id,
        Roadmap.status == "active"
    ).first()
    if not rm:
        raise HTTPException(status_code=404, detail="No active roadmap found for this student.")
    return roadmap_to_response(rm)

@router.patch("/milestones/{milestone_id}")
def update_status(milestone_id: int, payload: MilestoneStatusUpdate, db: Session = Depends(get_db)):
    """Update milestone progress status (not_started, in_progress, completed, blocked)."""
    try:
        return update_milestone_progress(db, milestone_id, payload.new_status, payload.notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/revisions/{student_id}", response_model=List[RoadmapRevisionResponse])
def get_revisions(student_id: int, db: Session = Depends(get_db)):
    """Retrieve full roadmap revision audit history for a student."""
    revisions = db.query(RoadmapRevisionHistory).filter(
        RoadmapRevisionHistory.student_id == student_id
    ).order_by(RoadmapRevisionHistory.created_at.desc()).all()

    return [
        RoadmapRevisionResponse(
            id=r.id,
            roadmap_id=r.roadmap_id,
            student_id=r.student_id,
            revision_trigger=r.revision_trigger,
            summary=r.summary,
            changes_applied=json.loads(r.changes_applied) if r.changes_applied else {},
            preserved_milestones_count=r.preserved_milestones_count,
            created_at=r.created_at
        )
        for r in revisions
    ]
