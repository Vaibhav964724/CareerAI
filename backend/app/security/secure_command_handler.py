"""
Assignment 5.1: Agent Authentication and Host Integrity Verification
Component: Secure Command Dispatcher & Tamper-Resistant Execution Handler
"""

import time
import secrets
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.security.signature_verification import CryptographicSignatureManager
from app.security.host_authenticator import HostAuthenticator


class SecureCommandHandler:
    """
    Enforces security checkpoints before protected state-mutating commands
    reach CareerAI core data models. Logs malicious attacks and blocked intrusions.
    """
    _instance: Optional['SecureCommandHandler'] = None

    def __init__(self):
        self.authenticator = HostAuthenticator()
        self.security_audit_log: List[Dict[str, Any]] = []

    @classmethod
    def get_instance(cls) -> 'SecureCommandHandler':
        if cls._instance is None:
            cls._instance = SecureCommandHandler()
        return cls._instance

    def create_signed_envelope(
        self,
        host_id: str,
        sender_id: str,
        secret_key: str,
        action: str,
        payload_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Utility helper generating a cryptographically signed request envelope."""
        envelope = {
            "host_id": host_id,
            "sender_id": sender_id,
            "timestamp": time.time(),
            "nonce": f"NONCE-{secrets.token_hex(8).upper()}",
            "action": action,
            "payload": payload_data
        }
        sig = CryptographicSignatureManager.generate_hmac_signature(envelope, secret_key)
        envelope["signature"] = sig
        return envelope

    def process_secure_command(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inspects incoming envelope, verifies cryptographic integrity and host credentials,
        and either executes the authorized action or blocks the request with an audit record.
        """
        is_authenticated, reason, audit_meta = self.authenticator.authenticate_and_verify_envelope(envelope)

        incident_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "host_id": envelope.get("host_id", "UNKNOWN"),
            "sender_id": envelope.get("sender_id", "UNKNOWN"),
            "action": envelope.get("action", "UNKNOWN"),
            "status": "ACCEPTED" if is_authenticated else "BLOCKED",
            "reason": reason,
            "error_code": audit_meta.get("code")
        }
        self.security_audit_log.append(incident_record)

        if not is_authenticated:
            return {
                "status": "REJECTED",
                "error": reason,
                "error_code": audit_meta.get("code"),
                "timestamp": incident_record["timestamp"],
                "data_integrity_preserved": True
            }

        # Simulated execution of protected action
        return {
            "status": "EXECUTED_SUCCESSFULLY",
            "message": f"Action '{envelope['action']}' executed under verified host '{envelope['host_id']}'",
            "audit_code": audit_meta.get("code"),
            "payload_echo": envelope.get("payload"),
            "timestamp": incident_record["timestamp"]
        }

    def get_security_audit_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        return list(self.security_audit_log[-limit:])

    def simulate_attack(self, attack_type: str) -> Dict[str, Any]:
        """
        Simulates one of three malicious intrusion vectors:
          1. TAMPER_PAYLOAD: Modifies the payload data after cryptographic signing.
          2. UNTRUSTED_HOST: Attempts unauthorized access from an unregistered host.
          3. REPLAY_ATTACK: Re-transmits an already-consumed nonce.
        """
        attack_type_upper = attack_type.upper().strip()

        if attack_type_upper == "TAMPER_PAYLOAD":
            # Generate valid envelope
            envelope = self.create_signed_envelope(
                host_id="HOST_STUDENT_PORTAL_CORE",
                sender_id="SENDER_ACADEMIC_ADVISOR",
                secret_key="CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
                action="UPDATE_STUDENT_PROFILE",
                payload_data={"student_id": "STU-RA2212704010040", "gpa": 3.5}
            )
            # Adversary tampers with the payload after signature creation
            envelope["payload"]["gpa"] = 4.0
            envelope["payload"]["tampered_by"] = "MALICIOUS_MITM_INTRUDER"
            result = self.process_secure_command(envelope)
            return {
                "attack_vector": "TAMPER_PAYLOAD",
                "attack_description": "Payload was modified in-transit after HMAC-SHA256 signature generation.",
                "tampered_envelope": envelope,
                "result": result
            }

        elif attack_type_upper == "UNTRUSTED_HOST":
            envelope = {
                "host_id": "ROGUE_EXTERNAL_SPOOFER_NODE_01",
                "sender_id": "SENDER_UNAUTHORIZED_HACKER",
                "timestamp": time.time(),
                "nonce": f"NONCE-{secrets.token_hex(8).upper()}",
                "action": "UPDATE_STUDENT_PROFILE",
                "payload": {"exploit": "DROP TABLE students;"},
                "signature": "DEADBEEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF01234567"
            }
            result = self.process_secure_command(envelope)
            return {
                "attack_vector": "UNTRUSTED_HOST",
                "attack_description": "Command originated from an unregistered and unauthorized host identity.",
                "tampered_envelope": envelope,
                "result": result
            }

        elif attack_type_upper == "REPLAY_ATTACK":
            envelope = self.create_signed_envelope(
                host_id="HOST_STUDENT_PORTAL_CORE",
                sender_id="SENDER_ACADEMIC_ADVISOR",
                secret_key="CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
                action="UPDATE_STUDENT_PROFILE",
                payload_data={"student_id": "STU-RA2212704010040", "audit_ping": True}
            )
            # First legitimate execution
            res_legit = self.process_secure_command(envelope)
            # Attacker intercepts and replays identical envelope with same nonce
            res_replay = self.process_secure_command(envelope)
            return {
                "attack_vector": "REPLAY_ATTACK",
                "attack_description": "Identical signed packet with already-consumed nonce was re-transmitted.",
                "legitimate_first_attempt": res_legit,
                "replayed_second_attempt": res_replay,
                "result": res_replay
            }

        else:
            return {
                "status": "ERROR",
                "message": f"Unknown attack type '{attack_type}'. Choose TAMPER_PAYLOAD, UNTRUSTED_HOST, or REPLAY_ATTACK."
            }
