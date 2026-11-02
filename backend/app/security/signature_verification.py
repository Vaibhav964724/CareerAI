"""
Assignment 5.1: Agent Authentication and Host Integrity Verification
Component: Cryptographic Signature Generation and Verification Engine
"""

import hmac
import hashlib
import json
import time
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timezone


class CryptographicSignatureManager:
    """
    Manages cryptographic canonical serialization and HMAC-SHA256 / Ed25519 signature
    generation and verification to ensure agent payload authenticity and data integrity.
    """
    @staticmethod
    def canonicalize_payload(payload_dict: Dict[str, Any]) -> bytes:
        """
        Produces deterministic, sorted, canonical JSON byte representation.
        Excludes existing signature field if present.
        """
        filtered = {k: v for k, v in payload_dict.items() if k != "signature"}
        canonical_str = json.dumps(filtered, sort_keys=True, separators=(',', ':'))
        return canonical_str.encode("utf-8")

    @staticmethod
    def generate_hmac_signature(payload_dict: Dict[str, Any], secret_key: str) -> str:
        """Computes HMAC-SHA256 signature over canonical payload."""
        canonical_bytes = CryptographicSignatureManager.canonicalize_payload(payload_dict)
        key_bytes = secret_key.encode("utf-8")
        sig = hmac.new(key_bytes, canonical_bytes, hashlib.sha256).hexdigest()
        return sig

    @staticmethod
    def verify_hmac_signature(payload_dict: Dict[str, Any], signature: str, secret_key: str) -> Tuple[bool, str]:
        """
        Verifies HMAC-SHA256 signature using constant-time comparison (hmac.compare_digest)
        to prevent timing attacks.
        """
        if not signature:
            return False, "Missing cryptographic signature in request"
        expected_sig = CryptographicSignatureManager.generate_hmac_signature(payload_dict, secret_key)
        is_valid = hmac.compare_digest(expected_sig, signature)
        if not is_valid:
            return False, "Invalid cryptographic signature: payload content has been tampered or corrupted"
        return True, "Signature verified successfully"
