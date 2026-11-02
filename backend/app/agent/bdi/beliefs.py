"""
Assignment 4.1: Belief-Desire-Intention (BDI) Cognitive Architecture
Component: Beliefs Representation & Knowledge Base State Repository
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Callable


@dataclass
class Belief:
    """
    Represents an explicit cognitive belief about the agent's internal state or external environment.
    Examples:
      - 'student_target_role': 'Data Scientist'
      - 'weekly_study_hours': 14.0
      - 'sql_proficiency': 2
      - 'burnout_index': 35.0
      - 'external_api_available': True
    """
    belief_id: str
    name: str
    value: Any
    source: str = "PERCEPT_INSPECTION"  # e.g., PERCEPT_INSPECTION, DATABASE, EXTERNAL_API, USER_INPUT
    confidence: float = 1.0            # 0.0 to 1.0 certainty
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "belief_id": self.belief_id,
            "name": self.name,
            "value": self.value,
            "source": self.source,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class BeliefBase:
    """
    The agent's knowledge base state repository tracking active beliefs.
    Provides reactive hooks and condition querying for cognitive deliberation.
    """
    def __init__(self):
        self._beliefs: Dict[str, Belief] = {}
        self._change_listeners: List[Callable[[Belief, Any], None]] = []

    def register_change_listener(self, listener: Callable[[Belief, Any], None]):
        """Adds a hook invoked whenever a belief is modified."""
        self._change_listeners.append(listener)

    def set_belief(self, name: str, value: Any, source: str = "INSPECTION", confidence: float = 1.0, metadata: Optional[Dict[str, Any]] = None) -> Belief:
        """Sets or updates a belief and notifies listeners if the value changed."""
        old_value = self._beliefs[name].value if name in self._beliefs else None
        belief_id = f"BELIEF_{name.upper()}"
        new_belief = Belief(
            belief_id=belief_id,
            name=name,
            value=value,
            source=source,
            confidence=confidence,
            metadata=metadata or {}
        )
        self._beliefs[name] = new_belief

        if old_value != value:
            for listener in self._change_listeners:
                listener(new_belief, old_value)

        return new_belief

    def get_belief(self, name: str) -> Optional[Belief]:
        return self._beliefs.get(name)

    def get_value(self, name: str, default: Any = None) -> Any:
        b = self._beliefs.get(name)
        return b.value if b else default

    def retract_belief(self, name: str) -> bool:
        if name in self._beliefs:
            del self._beliefs[name]
            return True
        return False

    def has_belief(self, name: str) -> bool:
        return name in self._beliefs

    def query(self, predicate: Callable[[Dict[str, Any]], bool]) -> bool:
        """Evaluates a logical predicate over current belief values."""
        snapshot = {k: v.value for k, v in self._beliefs.items()}
        return predicate(snapshot)

    def get_all_beliefs(self) -> Dict[str, Dict[str, Any]]:
        return {k: v.to_dict() for k, v in self._beliefs.items()}

    def initialize_from_student_state(self, student_dict: Dict[str, Any]):
        """Populates baseline beliefs from a CareerAI student profile."""
        self.set_belief("student_id", student_dict.get("id", "STU-001"), source="DATABASE")
        self.set_belief("target_role", student_dict.get("target_role", "Full Stack Engineer"), source="DATABASE")
        self.set_belief("weekly_study_hours", float(student_dict.get("weekly_hours", 10.0)), source="DATABASE")
        self.set_belief("gpa", float(student_dict.get("gpa", 3.5)), source="DATABASE")
        self.set_belief("burnout_index", float(student_dict.get("burnout_index", 25.0)), source="SENSORY_TELEMETRY")
        self.set_belief("market_demand_surge", bool(student_dict.get("market_demand_surge", False)), source="SENSORY_TELEMETRY")
        self.set_belief("days_to_deadline", int(student_dict.get("days_to_deadline", 30)), source="DATABASE")
        self.set_belief("external_api_healthy", True, source="SYSTEM_MONITOR")
