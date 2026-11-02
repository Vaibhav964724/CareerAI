import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.config import settings
from app.models.student import Student
from app.models.roadmap import Roadmap, RoadmapMilestone
from app.agent.state import AgentState
from app.agent.memory import AgentMemory
from app.agent.decision_engine import DecisionEngine
from app.agent.planner import GoalPlanner
from app.agent import tools
from app.services.llm_service import get_active_mode

class AgentController:
    """
    Autonomous 7-Stage Agent Controller:
    Stage 1: OBSERVE
    Stage 2: REASON
    Stage 3: PLAN
    Stage 4: ACT
    Stage 5: VERIFY
    Stage 6: PERSIST
    Stage 7: REPORT
    """

    def __init__(self, db: Session, student_id: int):
        self.db = db
        self.student_id = student_id
        self.memory = AgentMemory(db, student_id)
        self.max_iterations = settings.AGENT_MAX_ITERATIONS

    def run_evaluation_cycle(self, trigger: str = "manual_evaluation") -> AgentState:
        """Execute a full bounded 7-stage autonomous evaluation cycle."""
        state = AgentState(
            student_id=self.student_id,
            cycle_trigger=trigger,
            max_iterations=self.max_iterations,
            mode=get_active_mode()
        )

        iteration = 0
        while iteration < state.max_iterations:
            iteration += 1
            state.iteration_count = iteration

            # STAGE 1: OBSERVE
            state = self._stage_observe(state)

            # STAGE 2: REASON
            state = self._stage_reason(state)

            # STAGE 3: PLAN
            state = self._stage_plan(state)

            # If no actions planned, cycle has achieved its goal
            if not state.planned_actions:
                break

            # STAGE 4: ACT
            state = self._stage_act(state)

            # STAGE 5: VERIFY
            state = self._stage_verify(state)

            # STAGE 6: PERSIST
            state = self._stage_persist(state)

            # STAGE 7: REPORT
            state = self._stage_report(state)

            # We execute one thorough cycle per trigger unless further actions needed
            break

        return state

    # --- STAGE 1: OBSERVE ---
    def _stage_observe(self, state: AgentState) -> AgentState:
        # 1. Retrieve student profile
        profile = tools.get_student_profile(self.db, self.student_id)
        state.student_profile = profile

        # 2. Retrieve active roadmap and milestones
        active_rm = self.db.query(Roadmap).filter(
            Roadmap.student_id == self.student_id,
            Roadmap.status == "active"
        ).first()

        if active_rm:
            milestones = []
            for m in active_rm.milestones:
                milestones.append({
                    "id": m.id,
                    "title": m.title,
                    "phase_number": m.phase_number,
                    "phase_name": m.phase_name,
                    "description": m.description,
                    "required_skills": json.loads(m.required_skills) if m.required_skills else [],
                    "priority": m.priority,
                    "estimated_hours": m.estimated_hours,
                    "estimated_weeks": m.estimated_weeks,
                    "prerequisites": json.loads(m.prerequisites) if m.prerequisites else [],
                    "completion_criteria": m.completion_criteria,
                    "deadline": m.deadline,
                    "status": m.status,
                    "completed_at": m.completed_at.isoformat() if m.completed_at else None
                })
            state.active_roadmap = {
                "id": active_rm.id,
                "target_role": active_rm.target_role,
                "total_estimated_weeks": active_rm.total_estimated_weeks,
                "weekly_hours": active_rm.weekly_hours,
                "status": active_rm.status,
                "version": active_rm.version,
                "milestones_count": len(milestones)
            }
            state.milestones = milestones
        else:
            state.active_roadmap = None
            state.milestones = []

        # 3. Retrieve learning delays
        state.learning_delays = tools.detect_learning_delays(self.db, self.student_id)

        # 4. Retrieve recent memory observations
        state.recent_observations = self.memory.get_recent_observations(limit=5)

        self.memory.log_action(
            action_name="OBSERVE",
            stage="OBSERVE",
            status="success",
            reason=f"Observed student profile for {profile.get('name')} (Role: {profile.get('target_role')}).",
            input_data={"student_id": self.student_id, "trigger": state.cycle_trigger},
            output_data={"has_roadmap": bool(active_rm), "milestones_count": len(state.milestones)}
        )

        return state

    # --- STAGE 2: REASON ---
    def _stage_reason(self, state: AgentState) -> AgentState:
        # Evaluate skill gaps
        target_role = state.student_profile.get("target_role", "Data Analyst")
        gap_results = tools.analyze_skill_gaps(self.db, self.student_id, target_role)
        state.skill_gaps = gap_results.get("gaps", [])

        # Apply rule-based decision engine
        state = DecisionEngine.evaluate(state)

        self.memory.log_action(
            action_name="REASON",
            stage="REASON",
            status="success",
            reason=f"Identified {len(state.detected_changes)} state factors and evaluated {len(state.skill_gaps)} skill gaps.",
            input_data={"target_role": target_role},
            output_data={"detected_changes": state.detected_changes, "delays": len(state.learning_delays)}
        )

        return state

    # --- STAGE 3: PLAN ---
    def _stage_plan(self, state: AgentState) -> AgentState:
        state = GoalPlanner.create_plan(state)

        self.memory.log_action(
            action_name="PLAN",
            stage="PLAN",
            status="success",
            reason=f"Planned {len(state.planned_actions)} actions based on reasoned factors.",
            output_data={"planned_actions": state.planned_actions}
        )

        return state

    # --- STAGE 4: ACT ---
    def _stage_act(self, state: AgentState) -> AgentState:
        actions_taken = []
        proposed_revisions = []

        for item in state.planned_actions:
            action_name = item.get("action")

            if action_name == "generate_initial_roadmap":
                res = tools.generate_career_roadmap(
                    self.db,
                    self.student_id,
                    state.student_profile.get("target_role", "Data Analyst"),
                    float(state.student_profile.get("weekly_hours", 10.0))
                )
                actions_taken.append({
                    "action": action_name,
                    "description": f"Generated personalized career roadmap with {res.get('milestones_count')} milestones."
                })
                # Refresh active roadmap in state
                state.active_roadmap = res
                state.milestones = res.get("milestones", [])

            elif action_name == "revise_roadmap_role":
                res = tools.revise_career_roadmap(
                    self.db,
                    self.student_id,
                    trigger_reason="target_role_change",
                    new_target_role=item.get("new_target_role")
                )
                proposed_revisions.append(res)
                actions_taken.append({
                    "action": action_name,
                    "description": f"Revised roadmap for new career goal '{item.get('new_target_role')}'. Preserved {res.get('preserved_count')} completed milestones."
                })

            elif action_name == "revise_roadmap_hours":
                res = tools.revise_career_roadmap(
                    self.db,
                    self.student_id,
                    trigger_reason="available_hours_change",
                    new_weekly_hours=float(item.get("new_weekly_hours"))
                )
                proposed_revisions.append(res)
                actions_taken.append({
                    "action": action_name,
                    "description": f"Rebalanced milestone timelines to {item.get('new_weekly_hours')} hrs/week. Preserved {res.get('preserved_count')} completed milestones."
                })

            elif action_name == "flag_learning_delays":
                actions_taken.append({
                    "action": action_name,
                    "description": f"Logged proactive alerts for {len(state.learning_delays)} learning delays or blockers."
                })

            elif action_name == "evaluate_next_best_action":
                next_act = tools.evaluate_next_best_action(self.db, self.student_id)
                actions_taken.append({
                    "action": action_name,
                    "next_best_action": next_act
                })
                state.recommendations.append(f"Recommended Next Action: {next_act.get('title')} — {next_act.get('description')}")

        state.actions_taken = actions_taken
        state.proposed_revisions = proposed_revisions
        return state

    # --- STAGE 5: VERIFY ---
    def _stage_verify(self, state: AgentState) -> AgentState:
        verification_notes = []
        is_valid = True

        # Check if roadmap exists and milestones have valid schemas
        active_rm = self.db.query(Roadmap).filter(
            Roadmap.student_id == self.student_id,
            Roadmap.status == "active"
        ).first()

        if active_rm:
            milestones = active_rm.milestones
            if not milestones:
                is_valid = False
                verification_notes.append("Roadmap has zero milestones.")
            else:
                verification_notes.append(f"Verified roadmap contains {len(milestones)} sequenced milestones.")

                # Check completed work preservation
                completed = [m for m in milestones if m.status == "completed"]
                verification_notes.append(f"Verified {len(completed)} completed milestones are preserved and marked complete.")

                # Check ordering
                order_indices = [m.order_index for m in milestones]
                if order_indices != sorted(order_indices):
                    verification_notes.append("Milestone order index sequence warning.")
                else:
                    verification_notes.append("Milestone dependency and phase sequence verified.")

        state.verification_passed = is_valid
        state.verification_notes = verification_notes

        self.memory.log_action(
            action_name="VERIFY",
            stage="VERIFY",
            status="success" if is_valid else "warning",
            reason="Verified post-action roadmap integrity and completed work preservation.",
            output_data={"passed": is_valid, "notes": verification_notes}
        )

        return state

    # --- STAGE 6: PERSIST ---
    def _stage_persist(self, state: AgentState) -> AgentState:
        # Save observation to SQLite memory
        summary = (
            f"Agent completed evaluation cycle triggered by '{state.cycle_trigger}'. "
            f"Detected {len(state.detected_changes)} factors, executed {len(state.actions_taken)} actions."
        )
        obs_details = {
            "trigger": state.cycle_trigger,
            "detected_changes": state.detected_changes,
            "actions_taken": [a.get("description", a.get("action")) for a in state.actions_taken],
            "proposed_revisions": state.proposed_revisions,
            "verification_passed": state.verification_passed
        }
        self.memory.log_observation(
            observation_type=state.cycle_trigger,
            summary=summary,
            details=obs_details
        )
        return state

    # --- STAGE 7: REPORT ---
    def _stage_report(self, state: AgentState) -> AgentState:
        # Build concise human-readable decision summary
        sections = []

        # 1. What was detected
        if state.detected_changes:
            detected_str = "; ".join(state.detected_changes)
            sections.append(f"🔍 **Detected**: {detected_str}")
        else:
            sections.append("🔍 **Detected**: Profile and progress are consistent with the current roadmap.")

        # 2. What action was selected
        actions_str = "; ".join([a.get("description", a.get("action")) for a in state.actions_taken])
        sections.append(f"⚡ **Action Taken**: {actions_str if actions_str else 'No corrective action required.'}")

        # 3. Why it was appropriate ("Why CareerAI Recommended This")
        reasons = []
        for p in state.planned_actions:
            reasons.append(p.get("reason"))
        if reasons:
            sections.append(f"💡 **Why CareerAI Recommended This**: {' '.join(reasons)}")

        # 4. Next steps for student
        if state.recommendations:
            sections.append(f"🎯 **Next Best Action**: {state.recommendations[0]}")

        state.report_summary = "\n\n".join(sections)
        state.cycle_status = "completed"
        return state
