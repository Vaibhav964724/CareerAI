"""
Assignment 4.1: Belief-Desire-Intention (BDI) Cognitive Architecture
Component: Desires Representation & Goal-State Deliberation Logic
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from app.agent.bdi.beliefs import BeliefBase


@dataclass
class Desire:
    """
    Represents an agent's top-level strategic goal or desirable future world state.
    Examples:
      - 'DESIRE_RESOLVE_SKILL_DEFICIT'
      - 'DESIRE_MITIGATE_BURNOUT_RISK'
      - 'DESIRE_CAPSTONE_ACCELERATION'
      - 'DESIRE_REDUCE_STUDY_LOAD'
    """
    desire_id: str
    name: str
    description: str
    priority: int                                 # 1 (lowest) to 10 (highest)
    utility_weight: float = 1.0                   # Multiplier for deliberative ranking
    satisfaction_condition: Optional[Callable[[BeliefBase], bool]] = None
    trigger_condition: Optional[Callable[[BeliefBase], bool]] = None
    status: str = "ACTIVE"                        # ACTIVE, SATISFIED, SUSPENDED, DROPPED

    def is_triggered(self, beliefs: BeliefBase) -> bool:
        if self.trigger_condition:
            return self.trigger_condition(beliefs)
        return True

    def is_satisfied(self, beliefs: BeliefBase) -> bool:
        if self.satisfaction_condition:
            return self.satisfaction_condition(beliefs)
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "desire_id": self.desire_id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "utility_weight": self.utility_weight,
            "status": self.status
        }


class DesireManager:
    """
    Manages active candidate desires, evaluates environmental satisfaction conditions,
    and deliberates to select the dominant goal state.
    """
    def __init__(self):
        self._desires: Dict[str, Desire] = {}
        self._init_standard_careerai_desires()

    def _init_standard_careerai_desires(self):
        # 1. Burnout & Fatigue Mitigation (Highest Priority Safety Goal)
        self.add_desire(Desire(
            desire_id="DESIRE_PREVENT_BURNOUT",
            name="Prevent Student Cognitive Burnout",
            description="Ensure study workload remains within sustainable physiological limits",
            priority=10,
            utility_weight=2.0,
            trigger_condition=lambda b: float(b.get_value("burnout_index", 0.0)) >= 75.0 or float(b.get_value("weekly_study_hours", 10.0)) < 5.0,
            satisfaction_condition=lambda b: float(b.get_value("burnout_index", 0.0)) < 50.0 and float(b.get_value("weekly_study_hours", 10.0)) >= 5.0
        ))

        # 2. Urgent Milestone Deadline Pacing
        self.add_desire(Desire(
            desire_id="DESIRE_COMPRESS_CRITICAL_SCHEDULE",
            name="Recover Overdue Milestone Velocity",
            description="Rebalance milestone commitments when exams or placement deadlines approach",
            priority=9,
            utility_weight=1.8,
            trigger_condition=lambda b: int(b.get_value("days_to_deadline", 999)) < 14 and float(b.get_value("weekly_study_hours", 10.0)) < 10.0,
            satisfaction_condition=lambda b: int(b.get_value("days_to_deadline", 999)) >= 14 or float(b.get_value("weekly_study_hours", 10.0)) >= 12.0
        ))

        # 3. Market Demand Surge Skill Acquisition
        self.add_desire(Desire(
            desire_id="DESIRE_CAPSTONE_ACCELERATION",
            name="Fast-Track Industry Surge Competencies",
            description="Capitalize on hiring market spikes by accelerating high-demand competencies",
            priority=8,
            utility_weight=1.5,
            trigger_condition=lambda b: bool(b.get_value("market_demand_surge", False)) and float(b.get_value("burnout_index", 0.0)) < 65.0,
            satisfaction_condition=lambda b: not bool(b.get_value("market_demand_surge", False))
        ))

        # 4. Standard Skill Gap Resolution (Baseline Desired State)
        self.add_desire(Desire(
            desire_id="DESIRE_RESOLVE_SKILL_GAPS",
            name="Master Core Target Career Competencies",
            description="Systematically close skill gaps required for the student's selected target role",
            priority=7,
            utility_weight=1.2,
            trigger_condition=lambda b: True, # Always active as baseline goal
            satisfaction_condition=lambda b: int(b.get_value("unresolved_skill_gaps_count", 1)) == 0
        ))

    def add_desire(self, desire: Desire):
        self._desires[desire.desire_id] = desire

    def get_desire(self, desire_id: str) -> Optional[Desire]:
        return self._desires.get(desire_id)

    def deliberate_active_desires(self, beliefs: BeliefBase) -> List[Desire]:
        """
        Filters and ranks unsatisfied, triggered desires based on priority and utility.
        Returns ordered list from dominant to secondary desires.
        """
        active_candidates: List[Desire] = []
        for d in self._desires.values():
            if d.is_satisfied(beliefs):
                d.status = "SATISFIED"
                continue
            if d.is_triggered(beliefs):
                d.status = "ACTIVE"
                active_candidates.append(d)
            else:
                d.status = "SUSPENDED"

        # Sort descending by priority * utility_weight
        active_candidates.sort(key=lambda d: d.priority * d.utility_weight, reverse=True)
        return active_candidates

    def select_dominant_desire(self, beliefs: BeliefBase) -> Optional[Desire]:
        candidates = self.deliberate_active_desires(beliefs)
        return candidates[0] if candidates else None

    def get_all_desires(self) -> Dict[str, Dict[str, Any]]:
        return {k: v.to_dict() for k, v in self._desires.items()}
