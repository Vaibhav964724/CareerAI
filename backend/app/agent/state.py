from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    """Structured state of the CareerAI Agent across execution stages."""
    student_id: int
    cycle_trigger: str = "manual_evaluation"
    iteration_count: int = 0
    max_iterations: int = 5
    
    # Stage 1: Observed State
    student_profile: Dict[str, Any] = Field(default_factory=dict)
    active_roadmap: Optional[Dict[str, Any]] = None
    milestones: List[Dict[str, Any]] = Field(default_factory=list)
    recent_observations: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Stage 2: Reasoning Findings
    skill_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    detected_changes: List[str] = Field(default_factory=list)
    learning_delays: List[Dict[str, Any]] = Field(default_factory=list)
    has_hours_mismatch: bool = False
    has_role_mismatch: bool = False
    has_pending_milestones: bool = False
    all_milestones_completed: bool = False
    
    # Stage 3: Plan
    planned_actions: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Stage 4: Actions Executed
    actions_taken: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Stage 5: Verification Results
    verification_passed: bool = True
    verification_notes: List[str] = Field(default_factory=list)
    
    # Stage 6 & 7: Persistence & Report
    proposed_revisions: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    report_summary: str = ""
    cycle_status: str = "completed"
    mode: str = "rule-based"
