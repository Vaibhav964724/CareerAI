"""
Unit & Integration Tests for Agent Technology Academic Assignments (Units 1, 2, and 3)
Verifies:
  - 1.2: Condition-Action production rules in ReflexEnvironmentalReasoner
  - 2.1: Concurrent CareerMonitorDaemon thread execution & safety
  - 2.2: Distributed Agent Socket Serialization & Verification
  - 3.1: Multi-Agent Negotiation Protocol & Handshake Consensus
  - 3.2: Multi-Attribute Utility Optimization over 10 candidate bundles
"""

import pytest
import time
from app.agent.reflex_reasoner import (
    ReflexEnvironmentalReasoner,
    generate_synthetic_telemetry_stream,
    TelemetryPacket
)
from app.agent.daemon_worker import CareerMonitorDaemon, ConcurrentTelemetryState
from app.agent.socket_messaging import execute_distributed_socket_exchange, SocketAgentB_Server
from app.agent.negotiation_protocol import MultiAgentNegotiator, StudentAgent, RecruiterAgent
from app.agent.utility_optimizer import MultiAttributeUtilityOptimizer, CANDIDATE_BUNDLES


# ============================================================================
# Assignment 1.2: Reflex Reasoner Tests
# ============================================================================
def test_reflex_reasoner_rules_loading():
    reasoner = ReflexEnvironmentalReasoner()
    assert len(reasoner.rules) >= 5, "Reflex reasoner must have at least 5 Condition-Action rules loaded"
    rule_ids = [r.rule_id for r in reasoner.rules]
    assert "RULE_01_MARKET_DEMAND_SURGE" in rule_ids
    assert "RULE_02_SCHEDULE_COMPRESSION" in rule_ids
    assert "RULE_03_BURNOUT_GUARD" in rule_ids


def test_reflex_reasoner_market_surge_condition():
    reasoner = ReflexEnvironmentalReasoner()
    packet = TelemetryPacket(
        timestamp="2026-10-27T00:00:00Z",
        student_id="STU-TEST",
        skill_name="Python",
        market_demand_surge=True,
        market_demand_index=0.95
    )
    action = reasoner.evaluate_packet(packet)
    assert action is not None
    assert action.rule_name == "RULE_01_MARKET_DEMAND_SURGE"
    assert action.action_type == "HIGH"


def test_reflex_reasoner_burnout_condition():
    reasoner = ReflexEnvironmentalReasoner()
    packet = TelemetryPacket(
        timestamp="2026-10-27T00:00:00Z",
        student_id="STU-BURNOUT",
        burnout_index=85.0,
        weekly_hours=30.0
    )
    action = reasoner.evaluate_packet(packet)
    assert action is not None
    assert action.rule_name == "RULE_03_BURNOUT_GUARD"
    assert "pacing_buffer_days" in action.payload


# ============================================================================
# Assignment 2.1: Concurrent Daemon Worker Tests
# ============================================================================
def test_concurrent_telemetry_state_thread_safety():
    state = ConcurrentTelemetryState()
    assert state.get_state_snapshot()["daemon_status"] == "STOPPED"
    
    # Update metrics safely
    state.update_metrics(cycle_latency_ms=12.5, alerts=[{"test": "alert"}], milestone_count=5, overdue_count=1)
    snapshot = state.get_state_snapshot()
    assert snapshot["total_cycles_executed"] == 1
    assert snapshot["last_cycle_latency_ms"] == 12.5
    assert len(state.get_recent_alerts()) == 1


def test_daemon_worker_lifecycle():
    daemon = CareerMonitorDaemon(check_interval_seconds=0.1)
    assert not daemon.is_alive()
    
    daemon.start()
    assert daemon.is_alive()
    assert daemon.daemon is True
    
    time.sleep(0.3)
    snapshot = daemon.state.get_state_snapshot()
    assert snapshot["total_cycles_executed"] >= 1
    
    daemon.stop()
    daemon.join(timeout=1.0)
    assert not daemon.is_alive()


# ============================================================================
# Assignment 2.2: Distributed Socket Messaging Tests
# ============================================================================
def test_socket_agent_state_serialization_and_verification():
    test_profile = {
        "student_id": "STU-UNITTEST-01",
        "target_role": "Backend Engineer",
        "skills": ["Python", "SQL", "Docker", "FastAPI"],
        "gpa": 3.75,
        "completed_milestones_count": 3
    }
    
    result = execute_distributed_socket_exchange(test_profile, port=9125)
    assert result["status"] == "SUCCESS"
    assert "round_trip_latency_ms" in result
    assert result["inbound_response"]["placement_eligibility"] is True
    assert result["inbound_response"]["readiness_score"] > 60.0
    assert result["inbound_response"]["digital_handshake_signature"].startswith("SIG-AGENT-B-")


# ============================================================================
# Assignment 3.1: Multi-Agent Negotiation Protocol Tests
# ============================================================================
def test_multi_agent_negotiation_consensus():
    negotiator = MultiAgentNegotiator(max_turns=6)
    result = negotiator.execute_negotiation(
        student_target_stipend=2200,
        recruiter_budget_ceiling=2400
    )
    
    assert "consensus_reached" in result
    assert "timeline" in result
    assert len(result["timeline"]) > 0
    
    # Verify utility bounds
    for step in result["timeline"]:
        assert 0.0 <= step["student_utility"] <= 1.0
        assert 0.0 <= step["recruiter_utility"] <= 1.0
        
    if result["consensus_reached"]:
        assert result["handshake_signature"].startswith("AGREEMENT-SHA256-")
        assert result["final_agreement"]["stipend"] >= 800


# ============================================================================
# Assignment 3.2: Self-Interested Agent Utility Optimizer Tests
# ============================================================================
def test_candidate_bundles_count():
    assert len(CANDIDATE_BUNDLES) == 10, "Must have exactly 10 candidate bundles in catalog"


def test_utility_optimizer_evaluation_and_constraints():
    optimizer = MultiAttributeUtilityOptimizer(
        budget_limit_usd=160.0,
        time_limit_hours=18.0
    )
    result = optimizer.optimize()
    
    assert result["total_options_evaluated"] == 10
    assert result["feasible_count"] > 0
    assert result["infeasible_count"] > 0
    assert result["optimal_bundle"] is not None
    
    # Ensure optimal bundle satisfies hard constraints
    opt = result["optimal_bundle"]
    assert opt["cost_usd"] <= 160.0
    assert opt["hours_per_week"] <= 18.0
    assert opt["is_feasible"] is True
    assert opt["net_utility"] > 0.0
