"""
Assignment 1.2: Rule-Based Environmental Reasoner Implementation
Architecture: Simple Reflex Agent with Condition-Action Rules (Unit-1)
"""

import time
import random
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union


class TelemetryPacket:
    """Represents a structured environmental telemetry sensory frame."""
    def __init__(
        self,
        timestamp: str,
        student_id: Union[str, int] = "STU-101",
        skill_name: str = "Python",
        current_skill_proficiency: int = 2,
        study_hours_past_week: float = 12.0,
        milestone_velocity: float = 1.0,
        burnout_index: float = 30.0,
        market_demand_surge: bool = False,
        market_demand_index: float = 0.70,
        daily_study_hours: float = 2.0,
        weekly_hours: float = 12.0,
        days_to_deadline: int = 30,
        exam_proximity_days: int = 30,
        study_streak_days: int = 3,
        inactive_days: int = 0
    ):
        self.timestamp = timestamp
        self.student_id = str(student_id)
        self.skill_name = skill_name
        self.current_skill_proficiency = current_skill_proficiency
        self.study_hours_past_week = study_hours_past_week
        self.milestone_velocity = milestone_velocity
        self.burnout_index = burnout_index
        self.market_demand_surge = market_demand_surge
        self.market_demand_index = market_demand_index if market_demand_index != 0.70 else (0.92 if market_demand_surge else 0.70)
        self.daily_study_hours = daily_study_hours
        self.weekly_hours = weekly_hours or study_hours_past_week
        self.days_to_deadline = min(days_to_deadline, exam_proximity_days)
        self.exam_proximity_days = self.days_to_deadline
        self.study_streak_days = study_streak_days
        self.inactive_days = inactive_days

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "student_id": self.student_id,
            "skill_name": self.skill_name,
            "current_skill_proficiency": self.current_skill_proficiency,
            "study_hours_past_week": self.study_hours_past_week,
            "milestone_velocity": self.milestone_velocity,
            "burnout_index": self.burnout_index,
            "market_demand_surge": self.market_demand_surge,
            "market_demand_index": self.market_demand_index,
            "daily_study_hours": self.daily_study_hours,
            "weekly_hours": self.weekly_hours,
            "days_to_deadline": self.days_to_deadline,
            "exam_proximity_days": self.exam_proximity_days,
            "study_streak_days": self.study_streak_days,
            "inactive_days": self.inactive_days
        }


class TriggeredActionRecord:
    """Convenience wrapper for triggered action events."""
    def __init__(self, rule_id: str, rule_name: str, action_type: str, message: str, payload: Dict[str, Any], timestamp: str):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.action_type = action_type
        self.message = message
        self.payload = payload
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "action_type": self.action_type,
            "message": self.message,
            "payload": self.payload,
            "timestamp": self.timestamp
        }

    def __getitem__(self, item):
        return self.to_dict()[item]


class ConditionActionRule:
    """Represents an explicit Condition-Action production rule."""
    def __init__(self, rule_id: str, condition_desc: str, predicate, action, priority: int = 1):
        self.rule_id = rule_id
        self.condition_desc = condition_desc
        self.predicate = predicate
        self.action = action
        self.priority = priority

    @property
    def description(self) -> str:
        return self.condition_desc

    def evaluate(self, percept: Dict[str, Any]) -> bool:
        return self.predicate(percept)

    def execute(self, percept: Dict[str, Any]) -> Dict[str, Any]:
        return self.action(percept)


class ReflexEnvironmentalReasoner:
    """
    Simple Reflex Agent implementing Condition-Action rules
    over an environmental sensory data stream feed.
    """

    def __init__(self):
        self.rules: List[ConditionActionRule] = []
        self._init_rules()
        self.execution_log: List[Dict[str, Any]] = []

    def _init_rules(self):
        # Rule 1: High Industry Market Demand Surge
        self.rules.append(ConditionActionRule(
            rule_id="RULE_01_MARKET_DEMAND_SURGE",
            condition_desc="Industry market demand >= 0.85 OR market surge detected",
            predicate=lambda p: p.get("market_demand_index", 0.0) >= 0.85 or p.get("market_demand_surge", False),
            action=lambda p: {
                "action": "TRIGGER_URGENT_SKILL_PRIORITIZATION",
                "severity": "HIGH",
                "message": f"Market demand surge detected for '{p.get('skill_name', 'Target Skill')}' ({p.get('market_demand_index', 0.9)*100:.0f}% demand). Escalating roadmap priority to High.",
                "action_payload": {"recommendation": "Escalate priority of core framework milestones", "skill": p.get("skill_name"), "new_priority": "High"}
            },
            priority=10
        ))

        # Rule 2: Study Deficit with Approaching Exam/Deadline
        self.rules.append(ConditionActionRule(
            rule_id="RULE_02_SCHEDULE_COMPRESSION",
            condition_desc="Daily study hours < 2.0 AND days until target deadline < 14",
            predicate=lambda p: (p.get("daily_study_hours", 0.0) < 2.0 or p.get("study_hours_past_week", 0.0) < 10.0) and p.get("days_to_deadline", 999) < 14,
            action=lambda p: {
                "action": "TRIGGER_SCHEDULE_COMPRESSION",
                "severity": "CRITICAL",
                "message": f"Low study velocity logged with only {p.get('days_to_deadline')} days to deadline. Rebalancing weekly schedule.",
                "action_payload": {"recommendation": "Compress milestones, remove non-essential electives", "intervention": "Compress milestones & alert student"}
            },
            priority=9
        ))

        # Rule 3: Burnout / Fatigue Risk Mitigation
        self.rules.append(ConditionActionRule(
            rule_id="RULE_03_BURNOUT_GUARD",
            condition_desc="Burnout index > 75.0 AND weekly study hours > 25.0",
            predicate=lambda p: p.get("burnout_index", 0.0) > 75.0 and (p.get("weekly_hours", 0.0) > 25.0 or p.get("study_hours_past_week", 0.0) > 25.0),
            action=lambda p: {
                "action": "TRIGGER_REST_PACING_INTERVENTION",
                "severity": "MEDIUM",
                "message": f"Fatigue telemetry reached {p.get('burnout_index'):.1f}/100. Injecting recovery pacing buffer.",
                "action_payload": {"recommendation": "Schedule 2-day recovery rest buffer", "pacing_buffer_days": 2}
            },
            priority=8
        ))

        # Rule 4: Learning Acceleration on High Streak
        self.rules.append(ConditionActionRule(
            rule_id="RULE_04_MILESTONE_ACCELERATION",
            condition_desc="Study streak >= 7 days OR velocity >= 1.5",
            predicate=lambda p: p.get("study_streak_days", 0) >= 7 or p.get("milestone_velocity", 1.0) >= 1.5,
            action=lambda p: {
                "action": "TRIGGER_ADVANCED_PORTFOLIO_UNLOCK",
                "severity": "LOW",
                "message": f"High velocity detected (velocity {p.get('milestone_velocity')}). Unlocking advanced portfolio capstone challenge.",
                "action_payload": {"recommendation": "Fast-track student to capstone portfolio challenge", "unlock_advanced_project": True}
            },
            priority=7
        ))

        # Rule 5: Dormant Inactivity Alert
        self.rules.append(ConditionActionRule(
            rule_id="RULE_05_INACTIVITY_NUDGE",
            condition_desc="Inactivity gap >= 3 days",
            predicate=lambda p: p.get("inactive_days", 0) >= 3,
            action=lambda p: {
                "action": "TRIGGER_REENGAGEMENT_NUDGE",
                "severity": "MEDIUM",
                "message": f"Student inactive for {p.get('inactive_days')} consecutive days. Emitting automated micro-learning prompt.",
                "action_payload": {"recommendation": "Send 15-minute micro-learning recap prompt", "dispatch_micro_task": True}
            },
            priority=6
        ))

    def evaluate_packet(self, packet: Union[TelemetryPacket, Dict[str, Any]]) -> Optional[TriggeredActionRecord]:
        """Evaluates a sensory packet against prioritized rules, returning the highest priority triggered rule."""
        p_dict = packet.to_dict() if isinstance(packet, TelemetryPacket) else packet
        sorted_rules = sorted(self.rules, key=lambda r: r.priority, reverse=True)

        for rule in sorted_rules:
            if rule.evaluate(p_dict):
                res = rule.execute(p_dict)
                record = TriggeredActionRecord(
                    rule_id=rule.rule_id,
                    rule_name=rule.rule_id,
                    action_type=res["severity"],
                    message=res["message"],
                    payload=res["action_payload"],
                    timestamp=p_dict.get("timestamp", datetime.now(timezone.utc).isoformat())
                )
                self.execution_log.append(record.to_dict())
                return record
        return None

    def process_telemetry(self, raw_telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compatibility method for evaluating all matching rules for a single packet."""
        p_dict = raw_telemetry.to_dict() if isinstance(raw_telemetry, TelemetryPacket) else raw_telemetry
        triggered_actions = []
        sorted_rules = sorted(self.rules, key=lambda r: r.priority, reverse=True)

        for rule in sorted_rules:
            if rule.evaluate(p_dict):
                action_result = rule.execute(p_dict)
                event_record = {
                    "rule_id": rule.rule_id,
                    "condition": rule.condition_desc,
                    "action": action_result["action"],
                    "severity": action_result["severity"],
                    "message": action_result["message"],
                    "action_payload": action_result.get("action_payload", {}),
                    "timestamp": p_dict.get("timestamp", datetime.now(timezone.utc).isoformat()),
                    "telemetry_snapshot": p_dict
                }
                triggered_actions.append(event_record)
                self.execution_log.append(event_record)

        if not triggered_actions:
            passive_record = {
                "rule_id": "RULE_DEFAULT_STEADY_STATE",
                "condition": "Environmental parameters within nominal operating bounds",
                "action": "MAINTAIN_NOMINAL_CADENCE",
                "severity": "NORMAL",
                "message": "All sensory parameters nominal. Continuing active milestone tracking.",
                "timestamp": p_dict.get("timestamp", datetime.now(timezone.utc).isoformat()),
                "telemetry_snapshot": p_dict
            }
            triggered_actions.append(passive_record)
            self.execution_log.append(passive_record)

        return triggered_actions

    def process_stream(self, packets: List[Union[TelemetryPacket, Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Processes a sequence of telemetry packets."""
        results = []
        for pkt in packets:
            actions = self.process_telemetry(pkt)
            results.extend(actions)
        return results

    @staticmethod
    def generate_mock_stream(count: int = 5) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in generate_synthetic_telemetry_stream(count)]


def generate_synthetic_telemetry_stream(count: int = 5) -> List[TelemetryPacket]:
    """Generates synthetic telemetry packets demonstrating various environmental conditions."""
    scenarios = [
        # 1. Normal state
        {"hours": 12.0, "burnout": 25.0, "surge": False, "days": 35, "vel": 1.0, "streak": 4, "inactive": 0},
        # 2. Market surge
        {"hours": 14.0, "burnout": 30.0, "surge": True, "days": 30, "vel": 1.1, "streak": 5, "inactive": 0},
        # 3. High burnout
        {"hours": 32.0, "burnout": 88.0, "surge": False, "days": 25, "vel": 1.2, "streak": 6, "inactive": 0},
        # 4. Schedule deficit & exam approaching
        {"hours": 4.0, "burnout": 40.0, "surge": False, "days": 7, "vel": 0.4, "streak": 1, "inactive": 2},
        # 5. Inactivity nudge
        {"hours": 0.0, "burnout": 20.0, "surge": False, "days": 40, "vel": 0.0, "streak": 0, "inactive": 4},
        # 6. High streak velocity
        {"hours": 20.0, "burnout": 35.0, "surge": False, "days": 28, "vel": 1.8, "streak": 9, "inactive": 0},
    ]

    packets = []
    now = datetime.now(timezone.utc)
    for i in range(count):
        s = scenarios[i % len(scenarios)]
        pkt = TelemetryPacket(
            timestamp=now.isoformat(),
            student_id=f"STU-{100 + (i % 3) + 1}",
            skill_name="Full Stack Python & AI",
            current_skill_proficiency=2,
            study_hours_past_week=s["hours"],
            milestone_velocity=s["vel"],
            burnout_index=s["burnout"],
            market_demand_surge=s["surge"],
            daily_study_hours=round(s["hours"] / 7.0, 1),
            weekly_hours=s["hours"],
            days_to_deadline=s["days"],
            exam_proximity_days=s["days"],
            study_streak_days=s["streak"],
            inactive_days=s["inactive"]
        )
        packets.append(pkt)
    return packets
