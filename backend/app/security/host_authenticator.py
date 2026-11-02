"""
Assignment 5.1: Agent Authentication and Host Integrity Verification
Component: Trusted Host Registry, Replay Protection, and Authentication Logic
"""

import time
import secrets
from typing import Dict, Any, Tuple, Optional, Set
from datetime import datetime, timezone

from app.security.signature_verification import CryptographicSignatureManager


class HostAuthenticator:
    """
    Validates host provenance, enforces trusted-sender access control lists (ACL),
    and prevents replay attacks using a sliding nonce cache and timestamp expiration.
    """
    DEFAULT_TIMESTAMP_TOLERANCE_SEC = 300.0  # 5-minute validity window

    def __init__(self, timestamp_tolerance_sec: float = DEFAULT_TIMESTAMP_TOLERANCE_SEC):
        self.tolerance = timestamp_tolerance_sec
        self._nonce_cache: Set[str] = set()
        self._trusted_hosts: Dict[str, Dict[str, Any]] = {}
        self._init_trusted_hosts()

    def _init_trusted_hosts(self):
        """Initializes baseline trusted host registry with specific authorization scopes."""
        self.register_trusted_host(
            host_id="HOST_STUDENT_PORTAL_CORE",
            sender_id="SENDER_ACADEMIC_ADVISOR",
            secret_key="CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
            allowed_actions=["UPDATE_STUDENT_PROFILE", "TRIGGER_AGENT_EVALUATION", "ADAPT_ROADMAP_MILESTONES"]
        )
        self.register_trusted_host(
            host_id="HOST_PLACEMENT_INTELLIGENCE_NODE",
            sender_id="SENDER_PLACEMENT_OFFICER",
            secret_key="CAREERAI_SEC_KEY_PLACEMENT_NODE_4119",
            allowed_actions=["VERIFY_PLACEMENT_READINESS", "DISPATCH_INTERVIEW_HANDSHAKE"]
        )

    def register_trusted_host(self, host_id: str, sender_id: str, secret_key: str, allowed_actions: list):
        self._trusted_hosts[host_id] = {
            "sender_id": sender_id,
            "secret_key": secret_key,
            "allowed_actions": allowed_actions,
            "registered_at": datetime.now(timezone.utc).isoformat()
        }

    def get_trusted_hosts(self) -> Dict[str, Dict[str, Any]]:
        """Returns registered trusted hosts with sensitive keys masked."""
        safe_hosts = {}
        for hid, info in self._trusted_hosts.items():
            safe_hosts[hid] = {
                "sender_id": info["sender_id"],
                "allowed_actions": info["allowed_actions"],
                "registered_at": info["registered_at"],
                "secret_key_preview": info["secret_key"][:8] + "..." + info["secret_key"][-4:]
            }
        return safe_hosts

    def authenticate_and_verify_envelope(self, envelope: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Comprehensive 5-Point Security Validation Checkpoint:
          1. Schema Completeness: Must contain host_id, sender_id, timestamp, nonce, action, payload, signature.
          2. Host Authentication: Host must be present in trusted host registry.
          3. Timestamp Freshness: Prevents delayed or expired messages.
          4. Replay Protection: Prevents duplicate command execution by verifying nonce uniqueness.
          5. Cryptographic Signature: Verifies payload has not been tampered with.
          6. Action Authorization: Sender must have permission for requested action.
        """
        # 1. Schema check
        required_fields = ["host_id", "sender_id", "timestamp", "nonce", "action", "payload", "signature"]
        missing = [f for f in required_fields if f not in envelope]
        if missing:
            return False, f"Malformed envelope: missing required security fields {missing}", {"code": "ERR_SCHEMA_INCOMPLETE"}

        host_id = envelope["host_id"]
        sender_id = envelope["sender_id"]
        req_timestamp = envelope["timestamp"]
        nonce = envelope["nonce"]
        action = envelope["action"]
        signature = envelope["signature"]

        # 2. Host Authentication
        host_record = self._trusted_hosts.get(host_id)
        if not host_record:
            return False, f"Host Authentication Failed: Host '{host_id}' is untrusted or unverified", {"code": "ERR_UNTRUSTED_HOST"}

        if host_record["sender_id"] != sender_id:
            return False, f"Sender Identity Mismatch: Sender '{sender_id}' not authorized on host '{host_id}'", {"code": "ERR_SENDER_MISMATCH"}

        # 3. Timestamp Freshness Check
        try:
            now_ts = time.time()
            # Accept ISO string or float unix epoch
            if isinstance(req_timestamp, (int, float)):
                ts_val = float(req_timestamp)
            else:
                dt = datetime.fromisoformat(req_timestamp.replace("Z", "+00:00"))
                ts_val = dt.timestamp()
            
            clock_skew = abs(now_ts - ts_val)
            if clock_skew > self.tolerance:
                return False, f"Timestamp Expired / Clock Skew Exceeded: message age {clock_skew:.1f}s exceeds tolerance {self.tolerance}s", {"code": "ERR_TIMESTAMP_EXPIRED"}
        except Exception as e:
            return False, f"Invalid timestamp format: {str(e)}", {"code": "ERR_TIMESTAMP_MALFORMED"}

        # 4. Replay Protection via Nonce Cache
        if nonce in self._nonce_cache:
            return False, f"Replay Attack Detected: Nonce '{nonce}' has already been processed and revoked", {"code": "ERR_REPLAY_DETECTED"}

        # 5. Cryptographic Signature Verification
        secret_key = host_record["secret_key"]
        is_valid_sig, sig_msg = CryptographicSignatureManager.verify_hmac_signature(envelope, signature, secret_key)
        if not is_valid_sig:
            return False, f"Cryptographic Verification Failed: {sig_msg}", {"code": "ERR_SIGNATURE_TAMPERED"}

        # 6. Action Authorization ACL
        if action not in host_record["allowed_actions"]:
            return False, f"Authorization Refused: Sender '{sender_id}' lacks permission for action '{action}'", {"code": "ERR_UNAUTHORIZED_ACTION"}

        # Register nonce to prevent future replay
        self._nonce_cache.add(nonce)

        return True, "Security Checkpoints Passed: Host authenticated, signature verified, replay-safe", {
            "code": "SUCCESS_AUTHENTICATED",
            "host_id": host_id,
            "sender_id": sender_id,
            "action": action
        }
