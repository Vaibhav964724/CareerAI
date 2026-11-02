import json
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.agent_log import AgentObservation, AgentActionLog
from app.agent.controller import AgentController
from app.agent.tools import evaluate_next_best_action
from app.schemas.agent import (
    AgentEvaluationResponse,
    AgentObservationResponse,
    AgentActionLogResponse,
    NextBestActionResponse
)
from app.services.llm_service import get_active_mode

router = APIRouter(prefix="/agent", tags=["AI Agent"])

class EvaluationRequest(BaseModel):
    trigger: str = "manual_dashboard_evaluation"

@router.post("/evaluate/{student_id}", response_model=AgentEvaluationResponse)
def trigger_agent_evaluation(student_id: int, payload: EvaluationRequest = EvaluationRequest(), db: Session = Depends(get_db)):
    """
    Trigger the 7-stage autonomous agent cycle:
    OBSERVE -> REASON -> PLAN -> ACT -> VERIFY -> PERSIST -> REPORT
    """
    controller = AgentController(db, student_id)
    state = controller.run_evaluation_cycle(trigger=payload.trigger)

    return AgentEvaluationResponse(
        student_id=student_id,
        cycle_status=state.cycle_status,
        trigger=state.cycle_trigger,
        detected_changes=state.detected_changes,
        actions_taken=[a.get("description", a.get("action")) for a in state.actions_taken],
        proposed_revisions=state.proposed_revisions,
        recommendations=state.recommendations,
        report_summary=state.report_summary,
        mode=state.mode
    )

@router.get("/observations/{student_id}", response_model=List[AgentObservationResponse])
def get_observations(student_id: int, limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve chronological persistent observations recorded by the agent."""
    obs_list = db.query(AgentObservation).filter(
        AgentObservation.student_id == student_id
    ).order_by(AgentObservation.created_at.desc()).limit(limit).all()

    return [
        AgentObservationResponse(
            id=o.id,
            student_id=o.student_id,
            observation_type=o.observation_type,
            summary=o.summary,
            details=json.loads(o.details) if o.details else {},
            created_at=o.created_at
        )
        for o in obs_list
    ]

@router.get("/actions/{student_id}", response_model=List[AgentActionLogResponse])
def get_action_logs(student_id: int, limit: int = 25, db: Session = Depends(get_db)):
    """Retrieve execution action logs for verification and auditing."""
    logs = db.query(AgentActionLog).filter(
        AgentActionLog.student_id == student_id
    ).order_by(AgentActionLog.created_at.desc()).limit(limit).all()

    return [
        AgentActionLogResponse(
            id=l.id,
            student_id=l.student_id,
            action_name=l.action_name,
            stage=l.stage,
            status=l.status,
            reason=l.reason,
            input_data=json.loads(l.input_data) if l.input_data else {},
            output_data=json.loads(l.output_data) if l.output_data else {},
            created_at=l.created_at
        )
        for l in logs
    ]

@router.get("/next-action/{student_id}", response_model=NextBestActionResponse)
def get_next_action(student_id: int, db: Session = Depends(get_db)):
    """Evaluate and recommend the single next best action for the student."""
    res = evaluate_next_best_action(db, student_id)
    return NextBestActionResponse(**res)

@router.get("/mode")
def check_mode():
    """Check whether Claude LLM is active or Rule-Based Fallback is running."""
    active_mode = get_active_mode()
    return {
        "mode": active_mode,
        "is_llm_active": active_mode == "llm",
        "description": "Claude LLM Mode" if active_mode == "llm" else "Rule-Based Deterministic Fallback Mode (No API key needed)"
    }
