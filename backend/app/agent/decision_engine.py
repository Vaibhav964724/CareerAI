from typing import Dict, Any, List, Tuple
from app.agent.state import AgentState

class DecisionEngine:
    """
    Deterministic rule-based reasoning engine.
    Evaluates state and determines whether revisions, alerts, or actions are needed.
    """

    @staticmethod
    def evaluate(state: AgentState) -> AgentState:
        """Analyze the observed state and populate reasoning findings."""
        profile = state.student_profile
        roadmap = state.active_roadmap
        milestones = state.milestones

        detected_changes: List[str] = []
        reasons: List[str] = []

        # Rule 1: No active roadmap exists
        if not roadmap:
            detected_changes.append("No active roadmap found for current profile.")
            state.has_pending_milestones = False
            state.all_milestones_completed = False

        else:
            # Rule 2: Weekly study hours changed
            student_hours = float(profile.get("weekly_hours", 10.0))
            roadmap_hours = float(roadmap.get("weekly_hours", 10.0))
            if abs(student_hours - roadmap_hours) > 0.01:
                state.has_hours_mismatch = True
                msg = f"Available study time changed from {roadmap_hours} hrs/week to {student_hours} hrs/week."
                detected_changes.append(msg)
                reasons.append(msg)

            # Rule 3: Target career role changed
            student_role = profile.get("target_role", "").strip().lower()
            roadmap_role = roadmap.get("target_role", "").strip().lower()
            if student_role and roadmap_role and student_role != roadmap_role:
                state.has_role_mismatch = True
                msg = f"Target career goal changed from '{roadmap.get('target_role')}' to '{profile.get('target_role')}'."
                detected_changes.append(msg)
                reasons.append(msg)

            # Rule 4: Milestone completion status check
            completed = [m for m in milestones if m.get("status") == "completed"]
            blocked = [m for m in milestones if m.get("status") == "blocked"]
            in_prog = [m for m in milestones if m.get("status") == "in_progress"]
            not_started = [m for m in milestones if m.get("status") == "not_started"]

            if blocked:
                detected_changes.append(f"{len(blocked)} milestone(s) are blocked by dependencies or conceptual hurdles.")

            if not_started or in_prog:
                state.has_pending_milestones = True
                state.all_milestones_completed = False
            elif milestones and len(completed) == len(milestones):
                state.all_milestones_completed = True
                state.has_pending_milestones = False
                detected_changes.append("All milestones in the active roadmap have been completed!")

        state.detected_changes = detected_changes
        return state
