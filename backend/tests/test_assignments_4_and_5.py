"""
Unit & Integration Tests for Agent Technology Assignments (Units 4 and 5)
Course: Agent Technology
Student: Vaibhav Singh (Reg. No: RA2212704010040)
Faculty Evaluator: Dr. Prabhu Sir

Verifies:
  - 4.1: BDI Cognitive Architecture (Beliefs, Desires, Intentions, and Dynamic Intention Shift)
  - 4.2: Structured Domain Ontology, External REST API Client & Adaptive Milestone Synthesis
  - 5.1: Agent Authentication, HMAC Signatures, Nonce Replay Defense, and Attack Mitigation
  - 5.2: Capstone Master Orchestration across all 5 Course Units
"""

import pytest
import time

# Assignment 4.1: BDI Cognitive Architecture
from app.agent.bdi.bdi_agent import BDICognitiveAgent
from app.agent.bdi.beliefs import BeliefBase
from app.agent.bdi.desires import DesireManager
from app.agent.bdi.intentions import Intention, ActionStep
from app.agent.bdi.plan_selector import PlanSelector

# Assignment 4.2: Knowledge Representation & Live API
from app.knowledge.ontology_engine import CareerOntologyEngine
from app.knowledge.external_api_client import ExternalCareerAPIClient, LiveKnowledgeResource
from app.knowledge.adaptive_knowledge_service import AdaptiveKnowledgeService

# Assignment 5.1: Security & Host Integrity
from app.security.signature_verification import CryptographicSignatureManager
from app.security.host_authenticator import HostAuthenticator
from app.security.secure_command_handler import SecureCommandHandler

# Assignment 5.2: Capstone Master Orchestration
from app.agent.capstone_orchestrator import CapstoneConsolidatedAgent


# ============================================================================
# Assignment 4.1: BDI Cognitive Architecture Tests
# ============================================================================
def test_bdi_beliefs_initialization_and_queries():
    beliefs = BeliefBase()
    beliefs.initialize_from_student_state({
        "id": "STU-RA2212704010040",
        "target_role": "Full Stack Engineer",
        "weekly_hours": 16.0,
        "gpa": 3.8,
        "burnout_index": 15.0
    })
    assert beliefs.get_value("student_id") == "STU-RA2212704010040"
    assert beliefs.get_value("target_role") == "Full Stack Engineer"
    assert beliefs.get_value("weekly_study_hours") == 16.0
    assert beliefs.get_value("burnout_index") == 15.0
    assert len(beliefs.get_all_beliefs()) >= 5


def test_bdi_desire_dominance_and_deliberation():
    agent = BDICognitiveAgent()
    state = agent.deliberate()
    assert state["dominant_desire"] is not None
    assert agent.current_intention is not None
    assert agent.current_intention.status == "EXECUTING"
    assert len(agent.current_intention.plan_steps) > 0


def test_bdi_procedural_intention_execution():
    agent = BDICognitiveAgent()
    agent.deliberate()
    initial_step_index = agent.current_intention.current_step_index
    assert initial_step_index == 0

    step = agent.execute_next_action()
    assert step is not None
    assert agent.current_intention.current_step_index == 1
    assert len(agent.execution_audit_log) == 1
    assert agent.execution_audit_log[0]["status"] == "SUCCESS"


def test_bdi_dynamic_intention_shift_on_belief_shock():
    agent = BDICognitiveAgent()
    agent.deliberate()
    old_intention_id = agent.current_intention.intention_id

    # Execute one step
    agent.execute_next_action()

    # Environmental shock: study hours drop from 14.0 to 4.0 (violating intensive plan precondition)
    reconsider = agent.update_belief_and_reconsider(
        belief_name="weekly_study_hours",
        new_value=4.0,
        source="UNEXPECTED_TIME_DROP"
    )

    assert reconsider["intention_shifted"] is True
    shift_details = reconsider["shift_details"]
    assert shift_details is not None
    assert shift_details["previous_intention"]["id"] == old_intention_id
    assert agent.current_intention.intention_id != old_intention_id
    assert agent.current_intention.status == "EXECUTING"
    assert len(agent.intention_shift_history) == 1


# ============================================================================
# Assignment 4.2: Knowledge Representation & Adaptive API Tests
# ============================================================================
def test_career_ontology_schema_and_prerequisites():
    ontology = CareerOntologyEngine.get_instance()
    roles = ontology.get_all_roles()
    assert len(roles) >= 4
    assert "Full Stack Engineer" in roles

    categories = ontology.get_all_categories()
    assert len(categories) >= 3

    # Check prerequisite tree: FastAPI requires Python and REST APIs
    prereq_fail = ontology.check_prerequisites_satisfied("FastAPI", ["Java", "C++"])
    assert prereq_fail["prerequisites_satisfied"] is False
    assert "Python" in prereq_fail["missing_prerequisites"]

    prereq_pass = ontology.check_prerequisites_satisfied("FastAPI", ["Python", "REST APIs"])
    assert prereq_pass["prerequisites_satisfied"] is True
    assert len(prereq_pass["missing_prerequisites"]) == 0


def test_external_api_client_and_resource_parsing():
    client = ExternalCareerAPIClient(timeout_sec=5.0)
    # Testing skill query with robust fallback / live handling
    resources = client.fetch_live_skill_resources("FastAPI", max_results=3)
    assert len(resources) >= 1
    top_resource = resources[0]
    assert isinstance(top_resource, LiveKnowledgeResource)
    assert top_resource.title != ""
    assert top_resource.stars_or_rating >= 0
    assert top_resource.source_url.startswith("http")
    assert top_resource.provenance.startswith("LIVE_GITHUB_API") or top_resource.provenance.startswith("CURATED_KNOWLEDGE_MAP")


def test_adaptive_knowledge_service_plan_synthesis():
    service = AdaptiveKnowledgeService()
    result = service.adapt_roadmap_with_live_knowledge(
        student_id="STU-RA2212704010040",
        target_role="Full Stack Engineer",
        current_skills=["Python", "HTML/CSS"],
        primary_skill_gap="FastAPI"
    )
    assert result["status"] == "ADAPTATION_COMPLETE"
    record = result["adaptation_record"]
    milestone = record["adapted_milestone"]
    assert milestone["skill"] == "FastAPI"
    assert milestone["adapted_difficulty"] in ("INTERMEDIATE", "ADVANCED")
    assert milestone["external_reference_url"] != ""


# ============================================================================
# Assignment 5.1: Security & Host Integrity Tests
# ============================================================================
def test_security_signature_generation_and_verification():
    handler = SecureCommandHandler.get_instance()
    envelope = handler.create_signed_envelope(
        host_id="HOST_STUDENT_PORTAL_CORE",
        sender_id="SENDER_ACADEMIC_ADVISOR",
        secret_key="CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
        action="UPDATE_STUDENT_PROFILE",
        payload_data={"student_id": "STU-RA2212704010040", "gpa": 3.75}
    )
    assert "signature" in envelope
    assert len(envelope["signature"]) == 64  # SHA256 hex digest length

    # Execute through security checkpoint
    res = handler.process_secure_command(envelope)
    assert res["status"] == "EXECUTED_SUCCESSFULLY"
    assert res["audit_code"] == "SUCCESS_AUTHENTICATED"


def test_security_tampered_payload_blocked():
    handler = SecureCommandHandler.get_instance()
    sim = handler.simulate_attack("TAMPER_PAYLOAD")
    result = sim["result"]
    assert result["status"] == "REJECTED"
    assert result["error_code"] == "ERR_SIGNATURE_TAMPERED"
    assert result["data_integrity_preserved"] is True


def test_security_untrusted_host_blocked():
    handler = SecureCommandHandler.get_instance()
    sim = handler.simulate_attack("UNTRUSTED_HOST")
    result = sim["result"]
    assert result["status"] == "REJECTED"
    assert result["error_code"] == "ERR_UNTRUSTED_HOST"


def test_security_replay_attack_nonce_blocked():
    handler = SecureCommandHandler.get_instance()
    sim = handler.simulate_attack("REPLAY_ATTACK")
    first_attempt = sim["legitimate_first_attempt"]
    replay_attempt = sim["replayed_second_attempt"]
    assert first_attempt["status"] == "EXECUTED_SUCCESSFULLY"
    assert replay_attempt["status"] == "REJECTED"
    assert replay_attempt["error_code"] == "ERR_REPLAY_DETECTED"


# ============================================================================
# Assignment 5.2: Capstone Master Orchestration Tests
# ============================================================================
def test_capstone_consolidated_10_stage_cycle():
    agent = CapstoneConsolidatedAgent.get_instance()
    cycle = agent.run_consolidated_production_cycle(
        student_id="STU-RA2212704010040",
        target_role="Full Stack Engineer",
        weekly_hours=14.0,
        burnout_index=20.0
    )
    assert cycle["consolidated_status"] == "COMPLETED_SUCCESSFULLY"
    assert cycle["all_units_operational"] is True
    assert cycle["total_stages_executed"] == 10
    stage_numbers = [s["stage"] for s in cycle["stages_log"]]
    assert stage_numbers == list(range(1, 11))


def test_capstone_diagnostic_state():
    agent = CapstoneConsolidatedAgent.get_instance()
    state = agent.get_live_system_state()
    assert "unit_1_reflex" in state
    assert "unit_2_concurrency_sockets" in state
    assert "unit_3_cooperation_utility" in state
    assert "unit_4_bdi_knowledge" in state
    assert "unit_5_security" in state
    assert state["unit_1_reflex"]["rules_active"] >= 5
    assert state["unit_4_bdi_knowledge"]["ontology_roles_count"] >= 4
