"""
Assignment 4.1: Belief-Desire-Intention (BDI) Cognitive Architecture
Component: Plan Selector & Goal-to-Intention Deliberative Recipe Library
"""

from typing import Optional, List, Dict, Any
from app.agent.bdi.beliefs import BeliefBase
from app.agent.bdi.desires import Desire
from app.agent.bdi.intentions import Intention, ActionStep


class PlanSelector:
    """
    Deliberates and selects an executable Intention pipeline
    given a target Desire and the agent's active Beliefs.
    """

    @staticmethod
    def select_plan(desire: Desire, beliefs: BeliefBase) -> Intention:
        hours = float(beliefs.get_value("weekly_study_hours", 10.0))
        burnout = float(beliefs.get_value("burnout_index", 25.0))
        market_surge = bool(beliefs.get_value("market_demand_surge", False))

        # Scenario 1: Burnout or Severe Time Deficit -> Reduced Load Plan
        if desire.desire_id == "DESIRE_PREVENT_BURNOUT" or hours < 5.0 or burnout >= 75.0:
            return PlanSelector._create_reduced_load_recovery_plan(desire.desire_id, hours, burnout)

        # Scenario 2: Market Demand Surge -> Accelerated Capstone Plan
        if desire.desire_id == "DESIRE_CAPSTONE_ACCELERATION" or (market_surge and hours >= 12.0):
            return PlanSelector._create_accelerated_capstone_plan(desire.desire_id, hours)

        # Scenario 3: Schedule Compression -> Urgent Rebalancing Plan
        if desire.desire_id == "DESIRE_COMPRESS_CRITICAL_SCHEDULE":
            return PlanSelector._create_urgent_compression_plan(desire.desire_id)

        # Scenario 4: Standard Skill Gaps -> High vs Moderate Pacing
        if hours >= 12.0 and burnout < 60.0:
            return PlanSelector._create_intensive_deep_dive_plan(desire.desire_id, hours)
        else:
            return PlanSelector._create_balanced_modular_plan(desire.desire_id, hours)

    @staticmethod
    def _create_intensive_deep_dive_plan(desire_id: str, hours: float) -> Intention:
        steps = [
            ActionStep(
                step_id="STEP_INT_01",
                action_type="DEEP_DIVE_SYLLABUS",
                target="Core Algorithms & Architectures",
                parameters={"daily_hours_allocated": round(hours / 5.0, 1), "depth_level": "ADVANCED"}
            ),
            ActionStep(
                step_id="STEP_INT_02",
                action_type="ALGORITHM_SPRINT",
                target="Distributed Systems Coding Lab",
                parameters={"timed_challenge": True, "deliverable_code": True}
            ),
            ActionStep(
                step_id="STEP_INT_03",
                action_type="CAPSTONE_DEPLOYMENT",
                target="Production Portfolio Project",
                parameters={"deploy_target": "AWS / Docker", "public_url": True}
            )
        ]
        return Intention(
            intention_id="INTENTION_INTENSIVE_MASTERY",
            desire_id=desire_id,
            name="Intensive Full-Stack Deep Dive Plan",
            description=f"High-velocity 3-stage mastery commitment capitalizing on high weekly availability ({hours}h/wk)",
            plan_steps=steps,
            preconditions={"min_weekly_study_hours": 10.0, "max_burnout_index": 65.0},
            precondition_evaluator=lambda b: float(b.get_value("weekly_study_hours", 0.0)) >= 10.0 and float(b.get_value("burnout_index", 0.0)) <= 65.0,
            selection_rationale=f"Selected due to high available study bandwidth ({hours}h/week) and safe fatigue telemetry"
        )

    @staticmethod
    def _create_balanced_modular_plan(desire_id: str, hours: float) -> Intention:
        steps = [
            ActionStep(
                step_id="STEP_BAL_01",
                action_type="MODULAR_STUDY_BLOCK",
                target="Foundational Competencies",
                parameters={"pace": "MODERATE", "sessions_per_week": 4}
            ),
            ActionStep(
                step_id="STEP_BAL_02",
                action_type="GUIDED_PRACTICE",
                target="Hands-On Framework Exercises",
                parameters={"scaffolded_hints": True}
            ),
            ActionStep(
                step_id="STEP_BAL_03",
                action_type="MILESTONE_CHECKPOINT",
                target="Core Milestone Submission",
                parameters={"peer_review": False}
            )
        ]
        return Intention(
            intention_id="INTENTION_BALANCED_MODULAR",
            desire_id=desire_id,
            name="Balanced Modular Progression Plan",
            description=f"Sustainable steady-state roadmap tracking with moderate weekly commitment ({hours}h/wk)",
            plan_steps=steps,
            preconditions={"min_weekly_study_hours": 5.0, "max_burnout_index": 75.0},
            precondition_evaluator=lambda b: float(b.get_value("weekly_study_hours", 0.0)) >= 5.0 and float(b.get_value("burnout_index", 0.0)) <= 75.0,
            selection_rationale=f"Selected for moderate weekly availability ({hours}h/week)"
        )

    @staticmethod
    def _create_reduced_load_recovery_plan(desire_id: str, hours: float, burnout: float) -> Intention:
        steps = [
            ActionStep(
                step_id="STEP_REC_01",
                action_type="DISPATCH_REST_BUFFER",
                target="Cognitive Workload Recovery",
                parameters={"buffer_duration_days": 3, "freeze_deadlines": True}
            ),
            ActionStep(
                step_id="STEP_REC_02",
                action_type="PRUNE_ELECTIVES",
                target="Roadmap Milestones",
                parameters={"remove_optional_tasks": True, "protect_completed_milestones": True}
            ),
            ActionStep(
                step_id="STEP_REC_03",
                action_type="MICRO_RECAP",
                target="Conceptual Retention Quiz",
                parameters={"duration_minutes": 15, "low_cognitive_load": True}
            )
        ]
        return Intention(
            intention_id="INTENTION_REDUCED_LOAD_RECOVERY",
            desire_id=desire_id,
            name="Reduced-Load Recovery & Pacing Plan",
            description=f"Defensive intervention plan triggered by constrained study time ({hours}h/wk) or elevated fatigue ({burnout}/100)",
            plan_steps=steps,
            preconditions={}, # Always viable
            selection_rationale=f"Critical intervention selected: study time dropped to {hours}h/wk or burnout reached {burnout}/100"
        )

    @staticmethod
    def _create_accelerated_capstone_plan(desire_id: str, hours: float) -> Intention:
        steps = [
            ActionStep(
                step_id="STEP_SURGE_01",
                action_type="FAST_TRACK_SURGE_SKILLS",
                target="High-Demand Framework Milestones",
                parameters={"escalate_priority": "CRITICAL"}
            ),
            ActionStep(
                step_id="STEP_SURGE_02",
                action_type="API_PROJECT_SYNC",
                target="Live Open-Source Repositories",
                parameters={"query_external_api": True}
            ),
            ActionStep(
                step_id="STEP_SURGE_03",
                action_type="CAPSTONE_ACCELERATION",
                target="Portfolio Finalization",
                parameters={"target_placement_tier": "GOLD"}
            )
        ]
        return Intention(
            intention_id="INTENTION_ACCELERATED_CAPSTONE",
            desire_id=desire_id,
            name="Accelerated Market-Surge Capstone Plan",
            description="Aggressive sprint capturing hiring market demand spikes",
            plan_steps=steps,
            preconditions={"min_weekly_study_hours": 10.0, "max_burnout_index": 70.0},
            precondition_evaluator=lambda b: float(b.get_value("weekly_study_hours", 0.0)) >= 10.0 and float(b.get_value("burnout_index", 0.0)) <= 70.0,
            selection_rationale="Selected due to confirmed industry market hiring surge"
        )

    @staticmethod
    def _create_urgent_compression_plan(desire_id: str) -> Intention:
        steps = [
            ActionStep(
                step_id="STEP_COMP_01",
                action_type="SCHEDULE_COMPRESSION",
                target="Roadmap Phases",
                parameters={"compress_timeline_days": 10}
            ),
            ActionStep(
                step_id="STEP_COMP_02",
                action_type="PRIORITIZE_CORE_REQUIREMENTS",
                target="Essential Milestones Only",
                parameters={"defer_secondary": True}
            )
        ]
        return Intention(
            intention_id="INTENTION_URGENT_COMPRESSION",
            desire_id=desire_id,
            name="Urgent Milestone Schedule Compression Plan",
            description="Pacing compression plan recovering overdue deadlines",
            plan_steps=steps,
            preconditions={},
            selection_rationale="Triggered by approaching deadline with insufficient pacing velocity"
        )
