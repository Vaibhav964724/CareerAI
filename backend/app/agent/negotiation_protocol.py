"""
Assignment 3.1: Multi-Agent Coordination Protocol Execution
Architecture: Multi-Agent Systems (MAS) Multi-Turn Contract Negotiation with Concession Curves (Unit-3)
Implements:
  - StudentAgent & RecruiterAgent independent decision models
  - Multi-attribute proposal/counter-proposal evaluation (stipend, hours, mentorship)
  - Time-dependent concession curve alpha(t) = P_min + (P_max - P_min) * (t / T_max)^k
  - Consensus handshake termination & formal contract signature
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
import hashlib


class AgentPreferences:
    """Encapsulates valuation parameters and reservation limits for an agent."""
    def __init__(
        self,
        name: str,
        role: str,
        stipend_range: Tuple[int, int],  # (min, max)
        hours_range: Tuple[int, int],    # (min, max)
        mentorship_range: Tuple[int, int],
        weights: Dict[str, float],      # stipend, hours, mentorship
        reservation_utility: float,      # minimum acceptable utility
        concession_power: float = 1.5    # k > 1 conceder, k < 1 boulware
    ):
        self.name = name
        self.role = role
        self.stipend_range = stipend_range
        self.hours_range = hours_range
        self.mentorship_range = mentorship_range
        self.weights = weights
        self.reservation_utility = reservation_utility
        self.concession_power = concession_power


class StudentAgent:
    """
    Self-interested agent representing the student.
    Prefers higher stipend, lower weekly work hours, and more mentorship sessions.
    """
    def __init__(self, prefs: Optional[AgentPreferences] = None):
        if prefs is None:
            self.prefs = AgentPreferences(
                name="StudentAgent:CareerGuidance",
                role="STUDENT",
                stipend_range=(800, 2500),
                hours_range=(10, 30),
                mentorship_range=(2, 8),
                weights={"stipend": 0.55, "hours": 0.25, "mentorship": 0.20},
                reservation_utility=0.52,
                concession_power=1.3  # Conceder pattern
            )
        else:
            self.prefs = prefs

    def calculate_utility(self, offer: Dict[str, Any]) -> float:
        """Normalized utility calculation for student."""
        s = offer["stipend"]
        h = offer["hours"]
        m = offer["mentorship"]

        s_min, s_max = self.prefs.stipend_range
        h_min, h_max = self.prefs.hours_range
        m_min, m_max = self.prefs.mentorship_range

        u_s = max(0.0, min(1.0, (s - s_min) / (s_max - s_min)))
        # Less hours is better for student
        u_h = max(0.0, min(1.0, (h_max - h) / (h_max - h_min)))
        # More mentorship is better for student
        u_m = max(0.0, min(1.0, (m - m_min) / (m_max - m_min)))

        w = self.prefs.weights
        total_utility = w["stipend"] * u_s + w["hours"] * u_h + w["mentorship"] * u_m
        return round(total_utility, 3)

    def generate_offer(self, turn: int, max_turns: int) -> Dict[str, Any]:
        """Generates proposal using concession curve alpha(t)."""
        fraction = turn / max_turns
        concession = fraction ** self.prefs.concession_power
        
        # At t=1, student asks for high stipend, low hours, high mentorship
        # Over time concessions lower stipend demand, accept slightly higher hours
        s_min, s_max = self.prefs.stipend_range
        stipend = int(s_max - (s_max - (s_min + 200)) * concession)

        h_min, h_max = self.prefs.hours_range
        hours = int(h_min + ((h_max - 5) - h_min) * concession)

        m_min, m_max = self.prefs.mentorship_range
        mentorship = int(m_max - (m_max - m_min) * concession * 0.7)

        return {
            "stipend": stipend,
            "hours": hours,
            "mentorship": max(2, mentorship),
            "proposer": self.prefs.name
        }


class RecruiterAgent:
    """
    Self-interested agent representing an employer or industry partner.
    Prefers lower stipend, higher weekly contribution hours, and fewer mentorship overheads.
    """
    def __init__(self, prefs: Optional[AgentPreferences] = None):
        if prefs is None:
            self.prefs = AgentPreferences(
                name="RecruiterAgent:TalentAcquisition",
                role="RECRUITER",
                stipend_range=(800, 2500),
                hours_range=(10, 30),
                mentorship_range=(2, 8),
                weights={"stipend": 0.50, "hours": 0.35, "mentorship": 0.15},
                reservation_utility=0.48,
                concession_power=1.1  # Boulware-leaning
            )
        else:
            self.prefs = prefs

    def calculate_utility(self, offer: Dict[str, Any]) -> float:
        """Normalized utility calculation for recruiter."""
        s = offer["stipend"]
        h = offer["hours"]
        m = offer["mentorship"]

        s_min, s_max = self.prefs.stipend_range
        h_min, h_max = self.prefs.hours_range
        m_min, m_max = self.prefs.mentorship_range

        # Lower stipend is better for recruiter
        u_s = max(0.0, min(1.0, (s_max - s) / (s_max - s_min)))
        # Higher hours is better for recruiter
        u_h = max(0.0, min(1.0, (h - h_min) / (h_max - h_min)))
        # Fewer mentorship sessions needed saves recruiter time
        u_m = max(0.0, min(1.0, (m_max - m) / (m_max - m_min)))

        w = self.prefs.weights
        total_utility = w["stipend"] * u_s + w["hours"] * u_h + w["mentorship"] * u_m
        return round(total_utility, 3)

    def generate_offer(self, turn: int, max_turns: int) -> Dict[str, Any]:
        """Generates counter-proposal using concession curve."""
        fraction = turn / max_turns
        concession = fraction ** self.prefs.concession_power

        # At t=1, recruiter offers low stipend, high hours, low mentorship
        s_min, s_max = self.prefs.stipend_range
        stipend = int(s_min + ((s_max - 300) - s_min) * concession)

        h_min, h_max = self.prefs.hours_range
        hours = int(h_max - (h_max - (h_min + 4)) * concession)

        m_min, m_max = self.prefs.mentorship_range
        mentorship = int(m_min + (m_max - m_min) * concession * 0.8)

        return {
            "stipend": stipend,
            "hours": hours,
            "mentorship": max(2, mentorship),
            "proposer": self.prefs.name
        }


class MultiAgentNegotiator:
    """
    Orchestrates the multi-turn negotiation protocol between StudentAgent and RecruiterAgent.
    Terminates when consensus is accepted or max turns is exhausted.
    """
    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        self.student = StudentAgent()
        self.recruiter = RecruiterAgent()

    def execute_negotiation(
        self,
        student_target_stipend: Optional[int] = None,
        recruiter_budget_ceiling: Optional[int] = None
    ) -> Dict[str, Any]:
        """Runs the turn-based Contract Net style negotiation loop."""
        if student_target_stipend:
            self.student.prefs.stipend_range = (800, max(student_target_stipend, 1500))
        if recruiter_budget_ceiling:
            self.recruiter.prefs.stipend_range = (800, recruiter_budget_ceiling)

        turns_history: List[Dict[str, Any]] = []
        is_consensus_reached = False
        final_agreement: Optional[Dict[str, Any]] = None
        handshake_signature: Optional[str] = None

        current_student_offer = None

        for turn in range(1, self.max_turns + 1):
            # Phase 1: Student generates proposal or evaluates Recruiter's previous offer
            student_offer = self.student.generate_offer(turn, self.max_turns)
            current_student_offer = student_offer
            
            # Recruiter evaluates Student offer
            recruiter_utility_for_student_offer = self.recruiter.calculate_utility(student_offer)
            student_utility_for_own_offer = self.student.calculate_utility(student_offer)

            turn_record = {
                "turn": turn,
                "proposer": "StudentAgent",
                "offer": student_offer,
                "student_utility": student_utility_for_own_offer,
                "recruiter_utility": recruiter_utility_for_student_offer,
                "action": "PROPOSED"
            }

            if recruiter_utility_for_student_offer >= self.recruiter.prefs.reservation_utility:
                # Recruiter accepts student proposal!
                turn_record["action"] = "ACCEPTED_BY_RECRUITER"
                turns_history.append(turn_record)
                is_consensus_reached = True
                final_agreement = student_offer
                break

            turn_record["action"] = "COUNTER_REQUIRED"
            turns_history.append(turn_record)

            # Phase 2: Recruiter counters
            recruiter_offer = self.recruiter.generate_offer(turn, self.max_turns)
            student_utility_for_recruiter_offer = self.student.calculate_utility(recruiter_offer)
            recruiter_utility_for_own_offer = self.recruiter.calculate_utility(recruiter_offer)

            counter_record = {
                "turn": turn,
                "proposer": "RecruiterAgent",
                "offer": recruiter_offer,
                "student_utility": student_utility_for_recruiter_offer,
                "recruiter_utility": recruiter_utility_for_own_offer,
                "action": "COUNTERED"
            }

            if student_utility_for_recruiter_offer >= self.student.prefs.reservation_utility:
                # Student accepts recruiter counter-proposal!
                counter_record["action"] = "ACCEPTED_BY_STUDENT"
                turns_history.append(counter_record)
                is_consensus_reached = True
                final_agreement = recruiter_offer
                break

            counter_record["action"] = "REJECTED_CONTINUE"
            turns_history.append(counter_record)

        if is_consensus_reached and final_agreement:
            raw_sig = f"{final_agreement['stipend']}-{final_agreement['hours']}-{final_agreement['mentorship']}"
            handshake_signature = "AGREEMENT-SHA256-" + hashlib.sha256(raw_sig.encode()).hexdigest()[:16].upper()
            status_text = "CONSENSUS_REACHED"
        else:
            status_text = "IMPASSE_REACHED"
            handshake_signature = None

        return {
            "status": status_text,
            "consensus_reached": is_consensus_reached,
            "total_turns": len(turns_history),
            "final_agreement": final_agreement,
            "handshake_signature": handshake_signature,
            "timeline": turns_history,
            "student_reservation_threshold": self.student.prefs.reservation_utility,
            "recruiter_reservation_threshold": self.recruiter.prefs.reservation_utility,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
