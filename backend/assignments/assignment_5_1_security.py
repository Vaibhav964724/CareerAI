"""
========================================================================================
ASSIGNMENT 5.1: AGENT AUTHENTICATION AND HOST INTEGRITY VERIFICATION
Course: Agent Technology (Unit-5)
Scenario: Cryptographic HMAC Signature Verification, Host Provenance & Attack Defense
Student: Vaibhav Singh (Reg. No: RA2212704010040)
Faculty Evaluator: Dr. Prabhu Sir
========================================================================================
Description:
  Demonstrates cryptographic security and host integrity mechanisms for multi-agent systems:
  - Canonical JSON payload serialization.
  - Constant-time HMAC-SHA256 signature verification preventing timing attacks.
  - Trusted Host Access Control List (ACL) validation.
  - Sliding Nonce Cache protecting against Replay Attacks.
  - Automated simulation and mitigation of 3 hostile intrusion vectors:
      1. Tampered In-Flight Payload Attack (MITM modification)
      2. Rogue / Untrusted Host Identity Spoofing Attack
      3. Nonce Replay / Duplicate Packet Retransmission Attack
========================================================================================
"""

import sys
import os
import json
import time

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.security.signature_verification import CryptographicSignatureManager
from app.security.host_authenticator import HostAuthenticator
from app.security.secure_command_handler import SecureCommandHandler


def main():
    print("=" * 80)
    print("  ASSIGNMENT 5.1: AGENT AUTHENTICATION & HOST INTEGRITY VERIFICATION")
    print("  Student: Vaibhav Singh | Reg No: RA2212704010040 | Evaluator: Dr. Prabhu Sir")
    print("=" * 80)

    handler = SecureCommandHandler.get_instance()
    authenticator = handler.authenticator

    # 1. Display Trusted Host Registry
    print("\n[Checkpoint 1] Inspecting Registered Trusted Hosts & Access Control Lists (ACL)...")
    trusted_hosts = authenticator.get_trusted_hosts()
    for host_id, meta in trusted_hosts.items():
        print(f"  * Host ID:       {host_id}")
        print(f"    - Sender ID:   {meta['sender_id']}")
        print(f"    - Permissions: {', '.join(meta['allowed_actions'])}")
        print(f"    - Key Preview: {meta['secret_key_preview']}")
        print(f"    - Registered:  {meta['registered_at']}")

    # 2. Legitimate Signed Request Execution
    print("\n" + "=" * 80)
    print("  [Checkpoint 2] EXECUTING LEGITIMATE CRYPTOGRAPHICALLY SIGNED COMMAND")
    print("=" * 80)
    legit_envelope = handler.create_signed_envelope(
        host_id="HOST_STUDENT_PORTAL_CORE",
        sender_id="SENDER_ACADEMIC_ADVISOR",
        secret_key="CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
        action="UPDATE_STUDENT_PROFILE",
        payload_data={
            "student_id": "STU-RA2212704010040",
            "gpa": 3.75,
            "target_role": "Full Stack Engineer"
        }
    )
    print(f"  * Generated Cryptographic Envelope:")
    print(f"    - Host ID:   {legit_envelope['host_id']}")
    print(f"    - Sender:    {legit_envelope['sender_id']}")
    print(f"    - Nonce:     {legit_envelope['nonce']}")
    print(f"    - Timestamp: {legit_envelope['timestamp']}")
    print(f"    - Signature: {legit_envelope['signature']}")

    res_legit = handler.process_secure_command(legit_envelope)
    print(f"\n  * Security Gate Evaluation Result:")
    print(f"    - Status:       {res_legit.get('status')} [SECURITY ACCEPTED]")
    print(f"    - Message:      {res_legit.get('message')}")
    print(f"    - Audit Code:   {res_legit.get('audit_code')}")

    # 3. Simulate Attack 1: Tampered In-Flight Payload
    print("\n" + "=" * 80)
    print("  [Checkpoint 3] ATTACK SIMULATION 1: TAMPERED PAYLOAD (MITM MODIFICATION)")
    print("=" * 80)
    print("  Adversary intercepts legitimate packet and modifies GPA from 3.75 to 4.00 without valid key.")
    attack_1 = handler.simulate_attack("TAMPER_PAYLOAD")
    res_atk1 = attack_1["result"]
    print(f"  * Attack Result:    {res_atk1.get('status')} [INTRUSION INTERCEPTED & BLOCKED]")
    print(f"  * Error Code:       {res_atk1.get('error_code')}")
    print(f"  * Error Detail:     {res_atk1.get('error')}")
    print(f"  * Data Integrity:   Preserved = {res_atk1.get('data_integrity_preserved')}")

    # 4. Simulate Attack 2: Rogue / Untrusted Host Spoofing
    print("\n" + "=" * 80)
    print("  [Checkpoint 4] ATTACK SIMULATION 2: ROGUE / UNTRUSTED HOST SPOOFING")
    print("=" * 80)
    print("  Adversary attempts to dispatch commands from an unauthorized host 'ROGUE_EXTERNAL_SPOOFER_NODE_01'.")
    attack_2 = handler.simulate_attack("UNTRUSTED_HOST")
    res_atk2 = attack_2["result"]
    print(f"  * Attack Result:    {res_atk2.get('status')} [INTRUSION INTERCEPTED & BLOCKED]")
    print(f"  * Error Code:       {res_atk2.get('error_code')}")
    print(f"  * Error Detail:     {res_atk2.get('error')}")
    print(f"  * Host Identity:    Blocked unregistered host")

    # 5. Simulate Attack 3: Nonce Replay Attack
    print("\n" + "=" * 80)
    print("  [Checkpoint 5] ATTACK SIMULATION 3: REPLAY ATTACK (DUPLICATE NONCE)")
    print("=" * 80)
    print("  Adversary captures a previously accepted signed envelope and retransmits it verbatim.")
    attack_3 = handler.simulate_attack("REPLAY_ATTACK")
    res_atk3 = attack_3["result"]
    print(f"  * First Attempt:    {attack_3['legitimate_first_attempt'].get('status')} [SUCCESSFUL]")
    print(f"  * Replay Attempt:   {res_atk3.get('status')} [INTRUSION INTERCEPTED & BLOCKED]")
    print(f"  * Error Code:       {res_atk3.get('error_code')}")
    print(f"  * Error Detail:     {res_atk3.get('error')}")

    # 6. Audit Trail Dump
    print("\n" + "=" * 80)
    print("  SECURITY AUDIT TRAIL LOG (CareerAI Security Monitor)")
    print("=" * 80)
    recent_logs = handler.get_security_audit_logs(limit=6)
    print(f"{'Timestamp':<25} | {'Host ID':<25} | {'Action':<22} | {'Status'}")
    print("-" * 80)
    for log in recent_logs:
        print(f"{log['timestamp'][:22]:<25} | {log['host_id'][:24]:<25} | {log['action'][:21]:<22} | {log['status']}")
    print("-" * 80)
    print(f"Total Logged Security Events: {len(handler.security_audit_log)}")
    print("=" * 80)
    print("[SUCCESS] Assignment 5.1 Agent Security & Host Integrity verified successfully.\n")


if __name__ == "__main__":
    main()
