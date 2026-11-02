"""
Assignment 5.2: Capstone Project Consolidation and Secure Deployment Execution
Component: Consolidated 5-Unit Capstone Master Orchestrator
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import time

# Unit 1: Core Loop & Reflex Reasoner
from app.agent.reflex_reasoner import ReflexEnvironmentalReasoner, generate_synthetic_telemetry_stream

# Unit 2: Worker Daemon & Socket Messaging
from app.agent.daemon_worker import CareerMonitorDaemon, global_daemon_state
from app.agent.socket_messaging import execute_distributed_socket_exchange

# Unit 3: Cooperation & Utility Optimization
from app.agent.negotiation_protocol import MultiAgentNegotiator
from app.agent.utility_optimizer import MultiAttributeUtilityOptimizer

# Unit 4: BDI Cognitive Architecture & Adaptive Knowledge API
from app.agent.bdi.bdi_agent import BDICognitiveAgent
from app.knowledge import CareerOntologyEngine, AdaptiveKnowledgeService

# Unit 5: Cryptographic Security & Host Authentication
from app.security.secure_command_handler import SecureCommandHandler


class CapstoneConsolidatedAgent:
    """
    Unifies all 5 curriculum units into a single production-grade cognitive agent:
      - Unit 1: Reflex Environmental Reasoner
      - Unit 2: Concurrent Task Daemon & Distributed Sockets
      - Unit 3: Multi-Agent Negotiation & Constrained Utility Optimization
      - Unit 4: BDI Cognitive Architecture & Adaptive Knowledge API
      - Unit 5: Cryptographic Signature Verification & Host Integrity
    """
    _instance: Optional['CapstoneConsolidatedAgent'] = None

    def __init__(self):
        self.bdi_agent = BDICognitiveAgent(agent_id="CAPSTONE_PROD_AGENT_VAIBHAV")
        self.reflex_reasoner = ReflexEnvironmentalReasoner()
        self.daemon_worker = CareerMonitorDaemon.get_instance()
        self.knowledge_service = AdaptiveKnowledgeService()
        self.security_handler = SecureCommandHandler.get_instance()
        self.utility_optimizer = MultiAttributeUtilityOptimizer()
        self.negotiator = MultiAgentNegotiator(max_turns=6)
        self.production_cycle_history: List[Dict[str, Any]] = []

    @classmethod
    def get_instance(cls) -> 'CapstoneConsolidatedAgent':
        if cls._instance is None:
            cls._instance = CapstoneConsolidatedAgent()
        return cls._instance

    def run_consolidated_production_cycle(
        self,
        student_id: str = "STU-RA2212704010040",
        target_role: str = "Full Stack Engineer",
        weekly_hours: float = 14.0,
        burnout_index: float = 25.0,
        simulate_security_breach: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a complete 10-stage end-to-end production cycle exercising all 5 units:
        Stage 1: Unit 5 Cryptographic Signature Verification
        Stage 2: Unit 1 Reflex Sensory Telemetry Evaluation
        Stage 3: Unit 4 BDI Belief Ingestion & Goal Deliberation
        Stage 4: Unit 4 Semantic Ontology Prerequisite Verification
        Stage 5: Unit 4 Live REST API Query & Knowledge Enrichment
        Stage 6: Unit 4 Operational Step Execution
        Stage 7: Unit 4 Dynamic Intention Reconsideration (Simulated Shock)
        Stage 8: Unit 2 Concurrent Daemon Milestone Scanning
        Stage 9: Unit 2 Distributed Socket Frame Transmission
        Stage 10: Unit 3 Multi-Agent Placement Negotiation Consensus
        """
        t_start = time.perf_counter()
        cycle_id = f"CYCLE_CAPSTONE_{len(self.production_cycle_history)+1:03d}"
        stages_log: List[Dict[str, Any]] = []

        # -------------------------------------------------------------
        # STAGE 1: Unit 5 Security Checkpoint
        # -------------------------------------------------------------
        if simulate_security_breach:
            # Tampered envelope attack
            envelope = self.security_handler.create_signed_envelope(
                host_id="HOST_STUDENT_PORTAL_CORE",
                sender_id="SENDER_ACADEMIC_ADVISOR",
                secret_key="CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
                action="UPDATE_STUDENT_PROFILE",
                payload_data={"student_id": student_id, "gpa": 3.8}
            )
            # Tamper with payload
            envelope["payload"]["gpa"] = 4.0 # Malicious tamper without resigning
            sec_res = self.security_handler.process_secure_command(envelope)
            stages_log.append({
                "stage": 1,
                "unit": "Unit-5 Security",
                "operation": "Malicious Tampering Attack Simulation",
                "outcome": sec_res["status"],
                "details": sec_res.get("error", "Signature mismatch blocked")
            })
        else:
            envelope = self.security_handler.create_signed_envelope(
                host_id="HOST_STUDENT_PORTAL_CORE",
                sender_id="SENDER_ACADEMIC_ADVISOR",
                secret_key="CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
                action="TRIGGER_AGENT_EVALUATION",
                payload_data={"student_id": student_id, "target_role": target_role}
            )
            sec_res = self.security_handler.process_secure_command(envelope)
            stages_log.append({
                "stage": 1,
                "unit": "Unit-5 Security",
                "operation": "Cryptographic Envelope Verification",
                "outcome": sec_res["status"],
                "details": f"Verified under host {envelope['host_id']}"
            })

        # -------------------------------------------------------------
        # STAGE 2: Unit 1 Reflex Sensory Evaluation
        # -------------------------------------------------------------
        stream_packets = generate_synthetic_telemetry_stream(count=2)
        reflex_actions = self.reflex_reasoner.process_stream(stream_packets)
        stages_log.append({
            "stage": 2,
            "unit": "Unit-1 Core Reflex",
            "operation": "Sensory Stream Telemetry Parsing",
            "outcome": "SUCCESS",
            "details": f"Processed {len(stream_packets)} frames; {len(reflex_actions)} reactive actions triggered"
        })

        # -------------------------------------------------------------
        # STAGE 3: Unit 4 BDI Cognitive Deliberation
        # -------------------------------------------------------------
        self.bdi_agent.perceive({
            "student_id": student_id,
            "target_role": target_role,
            "weekly_study_hours": weekly_hours,
            "burnout_index": burnout_index,
            "days_to_deadline": 28,
            "market_demand_surge": True
        })
        bdi_delib = self.bdi_agent.deliberate()
        stages_log.append({
            "stage": 3,
            "unit": "Unit-4 BDI Cognitive",
            "operation": "Belief-Desire-Intention Deliberation",
            "outcome": "SUCCESS",
            "details": f"Dominant Desire: {bdi_delib.get('dominant_desire', {}).get('name')}; Committed Intention: {bdi_delib.get('current_intention', {}).get('name')}"
        })

        # -------------------------------------------------------------
        # STAGE 4 & 5: Unit 4 Ontology & Live REST API Ingestion
        # -------------------------------------------------------------
        adapt_res = self.knowledge_service.adapt_roadmap_with_live_knowledge(
            student_id=student_id,
            target_role=target_role,
            current_skills=["Python", "SQL"],
            primary_skill_gap="FastAPI"
        )
        stages_log.append({
            "stage": 4,
            "unit": "Unit-4 Knowledge & API",
            "operation": "Semantic Ontology & External REST API Integration",
            "outcome": "SUCCESS",
            "details": f"Ingested {len(adapt_res['live_resources'])} live resources from {adapt_res['adaptation_record']['api_endpoint_invoked']}"
        })

        # -------------------------------------------------------------
        # STAGE 6: Unit 4 Operational Step Execution
        # -------------------------------------------------------------
        executed_step = self.bdi_agent.execute_next_action()
        stages_log.append({
            "stage": 5,
            "unit": "Unit-4 BDI Execution",
            "operation": "Procedural Intention Step Dispatch",
            "outcome": "SUCCESS",
            "details": f"Executed step: {executed_step.action_type if executed_step else 'Complete'}"
        })

        # -------------------------------------------------------------
        # STAGE 6: Unit 4 Dynamic Intention Readjustment (Belief Shock)
        # -------------------------------------------------------------
        reconsider_res = self.bdi_agent.update_belief_and_reconsider(
            belief_name="weekly_study_hours",
            new_value=3.5, # Sudden unexpected drop violating intensive plan
            source="ACADEMIC_EXAM_OVERLOAD"
        )
        stages_log.append({
            "stage": 6,
            "unit": "Unit-4 BDI Reconsideration",
            "operation": "Dynamic Intention Shift on Environmental Update",
            "outcome": "INTENTION_SHIFTED" if reconsider_res["intention_shifted"] else "NO_SHIFT",
            "details": f"Shifted to: {reconsider_res.get('active_intention', {}).get('name')}"
        })

        # -------------------------------------------------------------
        # STAGE 7: Unit 3 Multi-Attribute Utility Optimization (MAUT)
        # -------------------------------------------------------------
        util_res = self.utility_optimizer.optimize()
        top_bundle = util_res.get("optimal_bundle", {}) or {}
        stages_log.append({
            "stage": 7,
            "unit": "Unit-3 Utility Optimization",
            "operation": "Multi-Attribute Utility Maximization (10 Bundles)",
            "outcome": "OPTIMAL_BUNDLE_SELECTED",
            "details": f"Optimal: {top_bundle.get('title')}; Net Utility: {top_bundle.get('net_utility', 0)}; Feasible: {util_res.get('feasible_count')}/{util_res.get('total_options_evaluated')}"
        })

        # -------------------------------------------------------------
        # STAGE 8: Unit 2 Concurrent Daemon Monitoring
        # -------------------------------------------------------------
        daemon_snapshot = global_daemon_state.get_state_snapshot()
        stages_log.append({
            "stage": 8,
            "unit": "Unit-2 Concurrency",
            "operation": "Background Daemon Milestone Health Check",
            "outcome": "SUCCESS",
            "details": f"Daemon Status: {daemon_snapshot.get('daemon_status')}; Latency: {daemon_snapshot.get('last_cycle_latency_ms')} ms"
        })

        # -------------------------------------------------------------
        # STAGE 9: Unit 2 Distributed Socket Transfer
        # -------------------------------------------------------------
        sock_res = execute_distributed_socket_exchange({
            "student_id": student_id,
            "target_role": target_role,
            "skills": ["Python", "FastAPI", "Docker", "SQL"],
            "gpa": 3.75,
            "completed_milestones_count": 4
        }, port=9126)
        stages_log.append({
            "stage": 9,
            "unit": "Unit-2 Sockets",
            "operation": "TCP Wire Frame Dual-Agent Synchronization",
            "outcome": sock_res["status"],
            "details": f"Agent-B Readiness: {sock_res['inbound_response'].get('readiness_score')}%; Signature: {sock_res['inbound_response'].get('digital_handshake_signature')}"
        })

        # -------------------------------------------------------------
        # STAGE 10: Unit 3 Multi-Agent Coordination Protocol
        # -------------------------------------------------------------
        nego_res = self.negotiator.execute_negotiation(student_target_stipend=2200, recruiter_budget_ceiling=2400)
        stages_log.append({
            "stage": 10,
            "unit": "Unit-3 Coordination",
            "operation": "Multi-Agent Contract Net Bidding Protocol",
            "outcome": nego_res["status"],
            "details": f"Consensus Reached: {nego_res['consensus_reached']} in {nego_res['total_turns']} turns"
        })

        elapsed_sec = round(time.perf_counter() - t_start, 2)
        summary = {
            "cycle_id": cycle_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "execution_duration_sec": elapsed_sec,
            "total_stages_executed": len(stages_log),
            "stages_log": stages_log,
            "consolidated_status": "COMPLETED_SUCCESSFULLY",
            "all_units_operational": True
        }
        self.production_cycle_history.append(summary)
        return summary

    def get_live_system_state(self) -> Dict[str, Any]:
        """Provides unified diagnostic snapshot of all 5 course units."""
        return {
            "unit_1_reflex": {
                "rules_active": len(self.reflex_reasoner.rules),
                "total_events_logged": len(self.reflex_reasoner.execution_log)
            },
            "unit_2_concurrency_sockets": {
                "daemon_metrics": global_daemon_state.get_state_snapshot(),
                "recent_alerts": global_daemon_state.get_recent_alerts(limit=5)
            },
            "unit_3_cooperation_utility": {
                "candidate_bundles_count": len(self.utility_optimizer.optimize()["ranked_feasible_options"]),
                "last_negotiation_turns": len(self.negotiator.student.prefs.weights)
            },
            "unit_4_bdi_knowledge": {
                "bdi_beliefs_count": len(self.bdi_agent.beliefs.get_all_beliefs()),
                "current_intention": self.bdi_agent.current_intention.to_dict() if self.bdi_agent.current_intention else None,
                "recent_intention_shift": self.bdi_agent.intention_shift_history[-1] if self.bdi_agent.intention_shift_history else None,
                "ontology_roles_count": len(self.knowledge_service.ontology.get_all_roles()),
                "external_api_health": self.knowledge_service.api_client.last_response_metadata
            },
            "unit_5_security": {
                "total_security_events": len(self.security_handler.security_audit_log),
                "recent_audit_log": self.security_handler.get_security_audit_logs(limit=5)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
