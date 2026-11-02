"""
API Routes for Agent Technology Academic Assignments (Units 1, 2, and 3)
Exposes endpoints to test and demonstrate:
  - Assignment 1.2: Rule-Based Reflex Reasoner & Telemetry Stream Engine
  - Assignment 2.1: Concurrent Background Task Daemon & Thread Metrics
  - Assignment 2.2: Distributed Agent Socket Messaging & Serialization
  - Assignment 3.1: Multi-Agent Coordination & Negotiation Protocol
  - Assignment 3.2: Self-Interested Agent Utility Optimizer (10 Resource Bundles)
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os

from app.agent.reflex_reasoner import (
    ReflexEnvironmentalReasoner,
    generate_synthetic_telemetry_stream,
    TelemetryPacket
)
from app.agent.daemon_worker import CareerMonitorDaemon, global_daemon_state
from app.agent.socket_messaging import execute_distributed_socket_exchange
from app.agent.negotiation_protocol import MultiAgentNegotiator
from app.agent.utility_optimizer import MultiAttributeUtilityOptimizer, CANDIDATE_BUNDLES

# Assignment 4.1: BDI Architecture
from app.agent.bdi.bdi_agent import BDICognitiveAgent

# Assignment 4.2: Knowledge Ontology & Live API
from app.knowledge.ontology_engine import CareerOntologyEngine
from app.knowledge.external_api_client import ExternalCareerAPIClient
from app.knowledge.adaptive_knowledge_service import AdaptiveKnowledgeService

# Assignment 5.1: Security & Host Authenticator
from app.security.signature_verification import CryptographicSignatureManager
from app.security.host_authenticator import HostAuthenticator
from app.security.secure_command_handler import SecureCommandHandler

# Assignment 5.2: Capstone Consolidation
from app.agent.capstone_orchestrator import CapstoneConsolidatedAgent

router = APIRouter(prefix="/assignments", tags=["Agent Technology Assignments"])

# Global daemon instance reference
_active_daemon_worker: Optional[CareerMonitorDaemon] = None

# Global BDI Cognitive Agent session reference
_active_bdi_agent: Optional[BDICognitiveAgent] = None

def get_bdi_agent() -> BDICognitiveAgent:
    global _active_bdi_agent
    if _active_bdi_agent is None:
        _active_bdi_agent = BDICognitiveAgent()
        _active_bdi_agent.deliberate()
    return _active_bdi_agent


# -------------------------------------------------------------
# Assignment 1.2: Reflex Reasoner
# -------------------------------------------------------------
class TelemetryStreamRequest(BaseModel):
    packet_count: int = Field(default=5, ge=1, le=20)
    custom_packets: Optional[List[Dict[str, Any]]] = None

@router.get("/1-2/sample-telemetry")
def get_sample_telemetry():
    """Generates synthetic telemetry packets for testing the reflex reasoner."""
    stream = generate_synthetic_telemetry_stream(count=5)
    return {
        "count": len(stream),
        "packets": [p.to_dict() for p in stream]
    }

@router.post("/1-2/reflex-stream")
def process_telemetry_stream(req: TelemetryStreamRequest):
    """Processes incoming telemetry packets through condition-action reflex rules."""
    reasoner = ReflexEnvironmentalReasoner()
    
    if req.custom_packets:
        packets = [
            TelemetryPacket(
                timestamp=p.get("timestamp", ""),
                student_id=p.get("student_id", "STU-DEMO"),
                study_hours_past_week=p.get("study_hours_past_week", 10.0),
                milestone_velocity=p.get("milestone_velocity", 1.0),
                burnout_index=p.get("burnout_index", 20.0),
                market_demand_surge=p.get("market_demand_surge", False),
                exam_proximity_days=p.get("exam_proximity_days", 30)
            )
            for p in req.custom_packets
        ]
    else:
        packets = generate_synthetic_telemetry_stream(count=req.packet_count)

    logs = reasoner.process_stream(packets)
    return {
        "status": "COMPLETED",
        "processed_packets_count": len(packets),
        "total_rules_evaluated_per_packet": len(reasoner.rules),
        "execution_logs": logs
    }


# -------------------------------------------------------------
# Assignment 2.1: Concurrent Background Task Daemon
# -------------------------------------------------------------
@router.get("/2-1/daemon-status")
def get_daemon_metrics():
    """Returns real-time thread latency, lock status, and alert count from the background daemon."""
    state = global_daemon_state.get_state_snapshot()
    alerts = global_daemon_state.get_recent_alerts(limit=10)
    return {
        "metrics": state,
        "recent_alerts": alerts
    }

class DaemonToggleRequest(BaseModel):
    action: str = Field(..., pattern="^(START|STOP)$")
    interval_seconds: float = Field(default=2.0, ge=0.5, le=30.0)

@router.post("/2-1/daemon-toggle")
def toggle_daemon_worker(req: DaemonToggleRequest):
    """Starts or stops the background worker thread safely."""
    global _active_daemon_worker
    
    if req.action == "START":
        if _active_daemon_worker is not None and _active_daemon_worker.is_alive():
            return {
                "message": "Daemon worker is already actively running.",
                "status": "ALREADY_RUNNING"
            }
        _active_daemon_worker = CareerMonitorDaemon(check_interval_seconds=req.interval_seconds)
        _active_daemon_worker.start()
        return {
            "message": f"Daemon worker started successfully with interval {req.interval_seconds}s.",
            "status": "STARTED"
        }
    else:
        if _active_daemon_worker is not None and _active_daemon_worker.is_alive():
            _active_daemon_worker.stop()
            _active_daemon_worker = None
            return {
                "message": "Daemon worker stopped gracefully.",
                "status": "STOPPED"
            }
        else:
            global_daemon_state.set_daemon_status("STOPPED")
            return {
                "message": "Daemon worker was not running.",
                "status": "STOPPED"
            }


# -------------------------------------------------------------
# Assignment 2.2: Distributed Socket Messaging
# -------------------------------------------------------------
class SocketTransferRequest(BaseModel):
    student_id: str = "STU-SOC-101"
    target_role: str = "Full Stack Engineer"
    skills: List[str] = ["Python", "FastAPI", "React", "Docker"]
    gpa: float = 3.6
    completed_milestones_count: int = 4
    port: int = 9123

@router.post("/2-2/socket-transfer")
def execute_socket_transfer(req: SocketTransferRequest):
    """Executes a local TCP socket exchange between Agent-A (Student Advisor) and Agent-B (Placement Node)."""
    payload = {
        "student_id": req.student_id,
        "target_role": req.target_role,
        "skills": req.skills,
        "gpa": req.gpa,
        "completed_milestones_count": req.completed_milestones_count
    }
    try:
        result = execute_distributed_socket_exchange(payload, port=req.port)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Socket transfer failed: {str(e)}")


# -------------------------------------------------------------
# Assignment 3.1: Multi-Agent Negotiation Protocol
# -------------------------------------------------------------
class NegotiationRequest(BaseModel):
    max_turns: int = Field(default=6, ge=2, le=12)
    student_target_stipend: Optional[int] = Field(default=2200, ge=800, le=4000)
    recruiter_budget_ceiling: Optional[int] = Field(default=2400, ge=1000, le=4000)

@router.post("/3-1/negotiate")
def execute_negotiation(req: NegotiationRequest):
    """Runs a multi-turn Contract Net style negotiation between StudentAgent and RecruiterAgent."""
    negotiator = MultiAgentNegotiator(max_turns=req.max_turns)
    result = negotiator.execute_negotiation(
        student_target_stipend=req.student_target_stipend,
        recruiter_budget_ceiling=req.recruiter_budget_ceiling
    )
    return result


# -------------------------------------------------------------
# Assignment 3.2: Self-Interested Agent Utility Optimization
# -------------------------------------------------------------
class OptimizationRequest(BaseModel):
    weight_skill: float = Field(default=0.40, ge=0.0, le=1.0)
    weight_relevance: float = Field(default=0.35, ge=0.0, le=1.0)
    weight_prestige: float = Field(default=0.25, ge=0.0, le=1.0)
    budget_limit_usd: float = Field(default=160.0, ge=10.0, le=500.0)
    time_limit_hours: float = Field(default=18.0, ge=2.0, le=40.0)

@router.post("/3-2/optimize")
def execute_utility_optimization(req: OptimizationRequest):
    """Evaluates 10 complex resource bundles using Multi-Attribute Utility Theory under budget & time constraints."""
    optimizer = MultiAttributeUtilityOptimizer(
        weight_skill=req.weight_skill,
        weight_relevance=req.weight_relevance,
        weight_prestige=req.weight_prestige,
        budget_limit_usd=req.budget_limit_usd,
        time_limit_hours=req.time_limit_hours
    )
    result = optimizer.optimize()
    return result

@router.get("/3-2/bundles")
def get_candidate_bundles():
    """Returns the catalog of 10 candidate resource bundles."""
    return {
        "count": len(CANDIDATE_BUNDLES),
        "bundles": CANDIDATE_BUNDLES
    }


# -------------------------------------------------------------
# Assignment 4.1: BDI Cognitive Architecture
# -------------------------------------------------------------
class BDIReconsiderRequest(BaseModel):
    belief_name: str = "weekly_study_hours"
    new_value: Any = 5.0
    source: str = "UNEXPECTED_ENVIRONMENTAL_UPDATE"

@router.get("/4-1/bdi-state")
def get_bdi_cognitive_state():
    """Returns current cognitive state across Beliefs, Desires, Intentions, and shift history."""
    agent = get_bdi_agent()
    return agent.get_cognitive_state()

@router.post("/4-1/bdi-step")
def execute_bdi_step():
    """Executes the next atomic action step in the committed intention."""
    agent = get_bdi_agent()
    executed_step = agent.execute_next_action()
    return {
        "executed_step": executed_step.to_dict() if executed_step else None,
        "active_intention": agent.current_intention.to_dict() if agent.current_intention else None,
        "is_completed": agent.current_intention.status == "COMPLETED" if agent.current_intention else False
    }

@router.post("/4-1/bdi-reconsider")
def trigger_bdi_reconsideration(req: BDIReconsiderRequest):
    """
    Simulates an environmental belief change mid-execution (e.g., student weekly study hours
    drop from 14.0 to 5.0, or stress level spikes to 85.0). The BDI agent re-evaluates desire
    dominance and triggers dynamic intention shift if preconditions are violated.
    """
    agent = get_bdi_agent()
    result = agent.update_belief_and_reconsider(
        belief_name=req.belief_name,
        new_value=req.new_value,
        source=req.source
    )
    return {
        "status": "SUCCESS",
        "reconsideration_result": result,
        "cognitive_state": agent.get_cognitive_state()
    }

@router.post("/4-1/bdi-reset")
def reset_bdi_agent():
    """Resets the BDI agent to its default initial state."""
    global _active_bdi_agent
    _active_bdi_agent = BDICognitiveAgent()
    _active_bdi_agent.deliberate()
    return {
        "status": "RESET_SUCCESSFUL",
        "state": _active_bdi_agent.get_cognitive_state()
    }


# -------------------------------------------------------------
# Assignment 4.2: Knowledge Representation and Adaptive API Integration
# -------------------------------------------------------------
class LiveResourceRequest(BaseModel):
    skill: str = "FastAPI"
    max_results: int = Field(default=3, ge=1, le=10)

class AdaptPlanRequest(BaseModel):
    student_id: str = "STU-RA2212704010040"
    target_role: str = "Full Stack Engineer"
    current_skills: List[str] = ["Python", "FastAPI"]
    primary_skill_gap: str = "Docker"

@router.get("/4-2/ontology")
def get_career_ontology():
    """Returns the formal career ontology roles, taxonomies, and prerequisite graphs."""
    engine = CareerOntologyEngine.get_instance()
    return {
        "roles": engine.get_all_roles(),
        "total_roles": len(engine.get_all_roles()),
        "categories": engine.get_all_categories(),
        "prerequisite_rules_count": len(engine.get_prerequisite_graph())
    }

@router.get("/4-2/prerequisites/{role_name}")
def get_role_prerequisites(role_name: str):
    """Returns required skills, prerequisite dependencies, and capstone archetype for a role."""
    engine = CareerOntologyEngine.get_instance()
    role_info = engine.get_role_requirements(role_name)
    if not role_info:
        raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found in career ontology.")
    return role_info

@router.post("/4-2/live-resources")
def fetch_live_skill_resources(req: LiveResourceRequest):
    """
    Connects to external REST API (GitHub Search API) with graceful fallback catalog
    to fetch real-time community repositories, ratings, and URLs.
    """
    client = ExternalCareerAPIClient()
    resources = client.fetch_live_skill_resources(req.skill, max_results=req.max_results)
    return {
        "skill": req.skill,
        "count": len(resources),
        "resources": [r.to_dict() for r in resources],
        "metadata": client.last_response_metadata
    }

@router.post("/4-2/adapt-plan")
def adapt_learning_plan_with_api(req: AdaptPlanRequest):
    """
    Dynamically adapts roadmap milestones by combining formal ontology prerequisites
    with live REST API project repository data.
    """
    service = AdaptiveKnowledgeService()
    result = service.adapt_roadmap_with_live_knowledge(
        student_id=req.student_id,
        target_role=req.target_role,
        current_skills=req.current_skills,
        primary_skill_gap=req.primary_skill_gap
    )
    return result


# -------------------------------------------------------------
# Assignment 5.1: Agent Authentication and Host Integrity Verification
# -------------------------------------------------------------
class CreateEnvelopeRequest(BaseModel):
    host_id: str = "HOST_STUDENT_PORTAL_CORE"
    sender_id: str = "SENDER_ACADEMIC_ADVISOR"
    secret_key: str = "CAREERAI_SEC_KEY_PROD_ADVISOR_9823"
    action: str = "UPDATE_STUDENT_PROFILE"
    payload_data: Dict[str, Any] = {"student_id": "STU-RA2212704010040", "gpa": 3.75}

class VerifyCommandRequest(BaseModel):
    envelope: Dict[str, Any]

class SimulateAttackRequest(BaseModel):
    attack_type: str = Field(default="TAMPER_PAYLOAD", pattern="^(TAMPER_PAYLOAD|UNTRUSTED_HOST|REPLAY_ATTACK)$")

@router.get("/5-1/trusted-hosts")
def get_trusted_hosts_registry():
    """Returns the registry of authenticated hosts and authorized actions."""
    handler = SecureCommandHandler.get_instance()
    return {
        "trusted_hosts": handler.authenticator.get_trusted_hosts()
    }

@router.post("/5-1/create-envelope")
def create_signed_security_envelope(req: CreateEnvelopeRequest):
    """Creates a canonical JSON cryptographically signed request envelope with HMAC-SHA256 signature and nonce."""
    handler = SecureCommandHandler.get_instance()
    envelope = handler.create_signed_envelope(
        host_id=req.host_id,
        sender_id=req.sender_id,
        secret_key=req.secret_key,
        action=req.action,
        payload_data=req.payload_data
    )
    return {
        "envelope": envelope,
        "signature_algorithm": "HMAC-SHA256",
        "digest": envelope["signature"]
    }

@router.post("/5-1/verify-command")
def verify_and_execute_secure_command(req: VerifyCommandRequest):
    """
    Passes incoming command envelope through the 5-point security checkpoint
    (schema, trusted host, timestamp skew, nonce cache replay check, HMAC signature).
    """
    handler = SecureCommandHandler.get_instance()
    result = handler.process_secure_command(req.envelope)
    return result

@router.post("/5-1/simulate-attack")
def simulate_security_attack(req: SimulateAttackRequest):
    """
    Simulates attacks (tampered payload, untrusted rogue host, or replay attack)
    and verifies that CareerAI security blocks the malicious attempt.
    """
    handler = SecureCommandHandler.get_instance()
    result = handler.simulate_attack(req.attack_type)
    return result

@router.get("/5-1/audit-logs")
def get_security_audit_logs():
    """Returns audit log of all security checkpoint decisions (ACCEPTED and BLOCKED)."""
    handler = SecureCommandHandler.get_instance()
    logs = handler.get_security_audit_logs(limit=25)
    return {
        "total_incidents": len(logs),
        "audit_logs": logs
    }


# -------------------------------------------------------------
# Assignment 5.2: Capstone Master Orchestration & State Dashboard
# -------------------------------------------------------------
class CapstoneCycleRequest(BaseModel):
    student_id: str = "STU-RA2212704010040"
    target_role: str = "Full Stack Engineer"
    weekly_hours: float = Field(default=14.0, ge=2.0, le=40.0)
    burnout_index: float = Field(default=25.0, ge=0.0, le=100.0)
    simulate_security_breach: bool = False

@router.get("/5-2/system-state")
def get_capstone_system_state():
    """Returns real-time integrated diagnostic snapshot across all 5 course units."""
    agent = CapstoneConsolidatedAgent.get_instance()
    return agent.get_live_system_state()

@router.post("/5-2/capstone-cycle")
def run_capstone_consolidated_cycle(req: CapstoneCycleRequest):
    """
    Executes a complete 10-stage consolidated production cycle across all 5 course units:
      Stage 1: Unit 5 Cryptographic Security & Host Integrity Check
      Stage 2: Unit 1 Reflex Environmental Perception
      Stage 3: Unit 4 Semantic Domain Ontology Validation
      Stage 4: Unit 4 Live REST API Repository Ingestion & Plan Adaptation
      Stage 5: Unit 4 BDI Cognitive Deliberation
      Stage 6: Unit 4 BDI Intention Step Execution
      Stage 7: Unit 3 Multi-Attribute Utility Optimization
      Stage 8: Unit 2 Background Task Daemon Health Check
      Stage 9: Unit 2 Distributed Socket Dual-Agent Transfer
      Stage 10: Unit 3 Multi-Agent Contract Net Negotiation Protocol
    """
    agent = CapstoneConsolidatedAgent.get_instance()
    result = agent.run_consolidated_production_cycle(
        student_id=req.student_id,
        target_role=req.target_role,
        weekly_hours=req.weekly_hours,
        burnout_index=req.burnout_index,
        simulate_security_breach=req.simulate_security_breach
    )
    return result
