from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AgentObservationResponse(BaseModel):
    id: int
    student_id: int
    observation_type: str
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AgentActionLogResponse(BaseModel):
    id: int
    student_id: int
    action_name: str
    stage: str
    status: str
    reason: Optional[str] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AgentEvaluationResponse(BaseModel):
    student_id: int
    cycle_status: str # "completed", "no_action_needed", "revisions_proposed"
    trigger: str
    detected_changes: List[str] = Field(default_factory=list)
    actions_taken: List[str] = Field(default_factory=list)
    proposed_revisions: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    report_summary: str
    mode: str # "rule-based" or "llm"

class NextBestActionResponse(BaseModel):
    student_id: int
    action_type: str # "start_milestone", "revise_roadmap", "resolve_blocker", "practice_project", "all_completed"
    title: str
    description: str
    reason: str
    priority: str # "high", "medium", "low"
    milestone_id: Optional[int] = None
    target_skill: Optional[str] = None

class AssistantQueryRequest(BaseModel):
    student_id: int
    message: str = Field(..., min_length=1, max_length=1000)

class AssistantQueryResponse(BaseModel):
    student_id: int
    reply: str
    mode: str # "rule-based" or "llm"
    relevant_context: Dict[str, Any] = Field(default_factory=dict)
    suggested_questions: List[str] = Field(default_factory=list)
