from typing import List, Dict, Any
from app.agent.state import AgentState

class GoalPlanner:
    """Selects target agent actions based on the current reasoned state."""

    @staticmethod
    def create_plan(state: AgentState) -> AgentState:
        planned_actions: List[Dict[str, Any]] = []

        # 1. If no roadmap, top priority is generating initial roadmap
        if not state.active_roadmap:
            planned_actions.append({
                "action": "generate_initial_roadmap",
                "priority": 1,
                "reason": "Student has saved a profile but does not have an active career roadmap."
            })
            state.planned_actions = planned_actions
            return state

        # 2. If career goal changed, prioritize role transition revision
        if state.has_role_mismatch:
            planned_actions.append({
                "action": "revise_roadmap_role",
                "priority": 1,
                "reason": f"Target career role changed to '{state.student_profile.get('target_role')}'. Update curriculum while preserving transferable completed work.",
                "new_target_role": state.student_profile.get("target_role")
            })

        # 3. If study hours changed, prioritize schedule duration revision
        if state.has_hours_mismatch:
            planned_actions.append({
                "action": "revise_roadmap_hours",
                "priority": 2,
                "reason": f"Available weekly study time changed to {state.student_profile.get('weekly_hours')} hrs/week. Rebalance milestone estimates.",
                "new_weekly_hours": state.student_profile.get("weekly_hours")
            })

        # 4. Check learning delays
        if state.learning_delays:
            planned_actions.append({
                "action": "flag_learning_delays",
                "priority": 3,
                "reason": f"Detected {len(state.learning_delays)} blocked or delayed milestone(s)."
            })

        # 5. Always evaluate next best action for student guidance
        planned_actions.append({
            "action": "evaluate_next_best_action",
            "priority": 4,
            "reason": "Determine the highest impact next learning activity for the student."
        })

        # Sort actions by priority
        planned_actions.sort(key=lambda x: x.get("priority", 10))
        state.planned_actions = planned_actions
        return state
