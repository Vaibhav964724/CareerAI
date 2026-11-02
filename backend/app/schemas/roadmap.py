from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class LearningResourceItem(BaseModel):
    name: str
    url: str
    type: str # documentation, course, interactive, tutorial
    provider: str

class RecommendedProjectItem(BaseModel):
    title: str
    description: str
    deliverables: List[str] = Field(default_factory=list)
    verification_checklist: List[str] = Field(default_factory=list)

class RoadmapMilestoneResponse(BaseModel):
    id: int
    roadmap_id: int
    title: str
    phase_number: int
    phase_name: str
    description: str
    required_skills: List[str] = Field(default_factory=list)
    priority: str # high, medium, low
    estimated_hours: float
    estimated_weeks: float
    prerequisites: List[str] = Field(default_factory=list)
    learning_resources: List[LearningResourceItem] = Field(default_factory=list)
    recommended_project: Optional[RecommendedProjectItem] = None
    completion_criteria: str
    deadline: Optional[str] = None
    status: str # not_started, in_progress, completed, blocked
    order_index: int
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MilestoneStatusUpdate(BaseModel):
    new_status: str = Field(..., pattern="^(not_started|in_progress|completed|blocked)$")
    notes: Optional[str] = None

class RoadmapResponse(BaseModel):
    id: int
    student_id: int
    target_role: str
    total_estimated_weeks: float
    weekly_hours: float
    status: str # active, archived, completed
    version: int
    milestones: List[RoadmapMilestoneResponse] = Field(default_factory=list)
    completed_milestones_count: int = 0
    total_milestones_count: int = 0
    completion_percentage: float = 0.0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RoadmapRevisionResponse(BaseModel):
    id: int
    roadmap_id: int
    student_id: int
    revision_trigger: str
    summary: str
    changes_applied: Dict[str, Any] = Field(default_factory=dict)
    preserved_milestones_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
