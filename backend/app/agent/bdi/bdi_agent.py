"""
Assignment 4.1: Belief-Desire-Intention (BDI) Cognitive Architecture
Component: BDI Cognitive Agent State Machine & Dynamic Reconsideration Engine
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json

from app.agent.bdi.beliefs import BeliefBase
from app.agent.bdi.desires import DesireManager, Desire
from app.agent.bdi.intentions import Intention, ActionStep
from app.agent.bdi.plan_selector import PlanSelector


class BDICognitiveAgent:
    """
    Cognitive-layer agent state machine tracking Beliefs, Desires, and Intentions.
    Implements the classical Rao & Georgeff BDI interpreter loop with dynamic
    plan reconsideration when environmental beliefs change mid-execution.
    """
    def __init__(self, agent_id: str = "BDI_CAREER_AGENT_01", initial_student_state: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.beliefs = BeliefBase()
        self.beliefs.initialize_from_student_state(initial_student_state or {
            "id": "STU-RA2212704010040",
            "target_role": "Full Stack Engineer",
            "weekly_hours": 14.0,
            "gpa": 3.75,
            "burnout_index": 20.0,
            "market_demand_surge": False,
            "days_to_deadline": 45
        })
        self.desires = DesireManager()
        self.current_intention: Optional[Intention] = None
        self.intention_shift_history: List[Dict[str, Any]] = []
        self.cycle_count = 0
        self.execution_audit_log: List[Dict[str, Any]] = []

    def perceive(self, sensory_packet: Dict[str, Any]):
        """Ingests environmental percepts and revises internal beliefs."""
        for key, val in sensory_packet.items():
            self.beliefs.set_belief(key, val, source="SENSORY_PERCEPT")

    def deliberate(self) -> Dict[str, Any]:
        """
        Cognitive deliberation cycle:
        1. Evaluate active desires against belief state.
        2. Select dominant desire.
        3. Bind or maintain committed procedural intention.
        """
        self.cycle_count += 1
        dominant_desire = self.desires.select_dominant_desire(self.beliefs)

        # If no intention committed, or previous intention finished, select plan
        if self.current_intention is None or self.current_intention.status in ("COMPLETED", "ABORTED"):
            if dominant_desire:
                self.current_intention = PlanSelector.select_plan(dominant_desire, self.beliefs)
                self.current_intention.status = "EXECUTING"

        return self.get_cognitive_state()

    def execute_next_action(self) -> Optional[ActionStep]:
        """Executes the next step in the currently committed intention."""
        if not self.current_intention or self.current_intention.status != "EXECUTING":
            return None

        current_step = self.current_intention.get_current_step()
        if not current_step:
            return None

        # Execute simulated operational step
        result = {
            "status": "SUCCESS",
            "action": current_step.action_type,
            "target": current_step.target,
            "cycle": self.cycle_count,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.execution_audit_log.append(result)

        # Advance pointer
        self.current_intention.advance_step(result_payload=result)
        return current_step

    def update_belief_and_reconsider(
        self,
        belief_name: str,
        new_value: Any,
        source: str = "UNEXPECTED_ENVIRONMENTAL_UPDATE"
    ) -> Dict[str, Any]:
        """
        Core Dynamic Plan Readjustment Routine:
        Updates a belief mid-execution, evaluates current intention viability,
        and triggers an intention shift if preconditions or dominant desires shift.
        """
        old_belief = self.beliefs.get_value(belief_name)
        self.beliefs.set_belief(belief_name, new_value, source=source)

        old_intention = self.current_intention
        intention_shifted = False
        shift_record = None

        if old_intention and old_intention.status == "EXECUTING":
            is_still_viable = old_intention.is_viable(self.beliefs)
            
            # Check if a critical higher-priority desire was triggered
            dominant_desire = self.desires.select_dominant_desire(self.beliefs)
            desire_conflict = dominant_desire and dominant_desire.desire_id != old_intention.desire_id

            if (not is_still_viable) or desire_conflict:
                reconsideration_reason = (
                    f"Precondition Violated: '{belief_name}' shifted from {old_belief} to {new_value}"
                    if not is_still_viable
                    else f"Dominant Goal Shift: New priority desire '{dominant_desire.name}' superseded previous plan"
                )

                # Abort old intention
                old_intention.abort(reason=reconsideration_reason)

                # Re-deliberate new intention
                new_intention = PlanSelector.select_plan(dominant_desire or self.desires.get_desire(old_intention.desire_id), self.beliefs)
                new_intention.status = "EXECUTING"
                self.current_intention = new_intention
                intention_shifted = True

                shift_record = {
                    "shift_id": f"SHIFT_{len(self.intention_shift_history)+1:03d}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "triggering_belief": {
                        "name": belief_name,
                        "old_value": old_belief,
                        "new_value": new_value,
                        "source": source
                    },
                    "previous_intention": {
                        "id": old_intention.intention_id,
                        "name": old_intention.name,
                        "steps_completed": old_intention.current_step_index,
                        "status": old_intention.status
                    },
                    "new_intention": {
                        "id": new_intention.intention_id,
                        "name": new_intention.name,
                        "total_steps": len(new_intention.plan_steps),
                        "rationale": new_intention.selection_rationale
                    },
                    "reconsideration_reason": reconsideration_reason
                }
                self.intention_shift_history.append(shift_record)

        return {
            "status": "RECONSIDERATION_COMPLETE",
            "intention_shifted": intention_shifted,
            "shift_details": shift_record,
            "active_intention": self.current_intention.to_dict() if self.current_intention else None
        }

    def get_cognitive_state(self) -> Dict[str, Any]:
        """Exports a full cognitive snapshot across Beliefs, Desires, and Intentions."""
        dominant_desire = self.desires.select_dominant_desire(self.beliefs)
        return {
            "agent_id": self.agent_id,
            "cycle_count": self.cycle_count,
            "beliefs": self.beliefs.get_all_beliefs(),
            "dominant_desire": dominant_desire.to_dict() if dominant_desire else None,
            "all_desires": self.desires.get_all_desires(),
            "current_intention": self.current_intention.to_dict() if self.current_intention else None,
            "intention_shifts_count": len(self.intention_shift_history),
            "recent_intention_shift": self.intention_shift_history[-1] if self.intention_shift_history else None,
            "audit_log_entries": len(self.execution_audit_log),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
