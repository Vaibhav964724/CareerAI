"""
Assignment 4.1: Belief-Desire-Intention (BDI) Cognitive Architecture
Component: Intentions Representation & Action Execution Pipelines
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable
from app.agent.bdi.beliefs import BeliefBase


@dataclass
class ActionStep:
    """Represents a discrete, executable operational action step in a procedural plan."""
    step_id: str
    action_type: str        # e.g., 'SCHEDULE_MILESTONE', 'DISPATCH_PACING_BUFFER', 'FETCH_API_RESOURCES', 'AUDIT_PORTFOLIO'
    target: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING" # PENDING, EXECUTING, COMPLETED, SKIPPED, FAILED
    execution_result: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "action_type": self.action_type,
            "target": self.target,
            "parameters": self.parameters,
            "status": self.status,
            "execution_result": self.execution_result
        }


class Intention:
    """
    Represents an actively committed procedural plan of action steps
    chosen to achieve a specific dominant desire.
    Intentions persist across cycles until completed, impossible, or reconsidered.
    """
    def __init__(
        self,
        intention_id: str,
        desire_id: str,
        name: str,
        description: str,
        plan_steps: List[ActionStep],
        preconditions: Optional[Dict[str, Any]] = None,
        precondition_evaluator: Optional[Callable[[BeliefBase], bool]] = None,
        selection_rationale: str = ""
    ):
        self.intention_id = intention_id
        self.desire_id = desire_id
        self.name = name
        self.description = description
        self.plan_steps = plan_steps
        self.current_step_index = 0
        self.status = "READY" # READY, EXECUTING, COMPLETED, ABORTED, RECONSIDERING
        self.preconditions = preconditions or {}
        self.precondition_evaluator = precondition_evaluator
        self.selection_rationale = selection_rationale
        self.committed_at = datetime.now(timezone.utc).isoformat()
        self.completed_at: Optional[str] = None
        self.aborted_reason: Optional[str] = None

    def is_viable(self, beliefs: BeliefBase) -> bool:
        """
        Verifies whether current environmental beliefs still satisfy
        the operational preconditions required to execute this intention.
        """
        if self.precondition_evaluator:
            return self.precondition_evaluator(beliefs)
        
        # Simple threshold comparisons
        for key, required_val in self.preconditions.items():
            current_val = beliefs.get_value(key)
            if current_val is None:
                continue
            # If checking minimum hours
            if key == "min_weekly_study_hours" and float(current_val) < float(required_val):
                return False
            # If checking maximum burnout limit
            if key == "max_burnout_index" and float(current_val) > float(required_val):
                return False
        return True

    def get_current_step(self) -> Optional[ActionStep]:
        if 0 <= self.current_step_index < len(self.plan_steps):
            return self.plan_steps[self.current_step_index]
        return None

    def advance_step(self, result_payload: Optional[Dict[str, Any]] = None) -> Optional[ActionStep]:
        """Marks current step completed and advances pointer."""
        curr = self.get_current_step()
        if curr:
            curr.status = "COMPLETED"
            curr.execution_result = result_payload or {"status": "SUCCESS"}
            self.current_step_index += 1

        if self.current_step_index >= len(self.plan_steps):
            self.status = "COMPLETED"
            self.completed_at = datetime.now(timezone.utc).isoformat()
            return None

        self.status = "EXECUTING"
        return self.get_current_step()

    def abort(self, reason: str):
        """Aborts the intention when environmental beliefs violate viability."""
        self.status = "ABORTED"
        self.aborted_reason = reason
        curr = self.get_current_step()
        if curr and curr.status == "PENDING":
            curr.status = "SKIPPED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intention_id": self.intention_id,
            "desire_id": self.desire_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "current_step_index": self.current_step_index,
            "total_steps": len(self.plan_steps),
            "plan_steps": [s.to_dict() for s in self.plan_steps],
            "preconditions": self.preconditions,
            "selection_rationale": self.selection_rationale,
            "committed_at": self.committed_at,
            "completed_at": self.completed_at,
            "aborted_reason": self.aborted_reason
        }
