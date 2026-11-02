"""
========================================================================================
ASSIGNMENT 2.2: DISTRIBUTED AGENT MESSAGING USING SOCKETS/RPC COMMUNICATION
Course: Agent Technology (Unit-2)
Scenario: Distributed Dual-Agent State Serialization & Verification Mesh in CareerAI
========================================================================================
Description:
  This script demonstrates distributed agent communication across raw TCP sockets.
  Agent-A (Student Advisor) serializes local student state into structured JSON frames
  with length-prefixed transport and sends it to Agent-B (Placement Node).
  Agent-B ingests the packet, evaluates placement readiness, and replies with a
  signed verification payload.
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

from app.agent.socket_messaging import execute_distributed_socket_exchange


def main():
    print("=" * 78)
    print("  ASSIGNMENT 2.2: DISTRIBUTED AGENT TCP SOCKET MESSAGING DEMO")
    print("=" * 78)

    sample_student_profile = {
        "student_id": "STU-SOCKET-2026",
        "target_role": "Machine Learning Engineer",
        "skills": ["Python", "PyTorch", "FastAPI", "SQLAlchemy", "Docker"],
        "gpa": 3.82,
        "completed_milestones_count": 4,
        "notes": "Seeking autumn campus placements"
    }

    port = 9124  # Dedicated port for standalone demo
    print(f"\n[Environment Configuration] Target Socket Node: 127.0.0.1:{port}")
    print(f"[Outbound State Payload from Agent-A]:")
    print(json.dumps(sample_student_profile, indent=2))

    print("\n[Executing TCP Socket Exchange between Agent-A and Agent-B]...")
    result = execute_distributed_socket_exchange(sample_student_profile, port=port)

    print("\n" + "=" * 78)
    print("  DISTRIBUTED SOCKET AUDIT TRAIL LOG")
    print("=" * 78)
    for log_entry in result.get("audit_trail", []):
        print(f"  {log_entry}")

    print("\n" + "-" * 78)
    print("  INBOUND RESPONSE RECEIVED BY AGENT-A FROM AGENT-B")
    print("-" * 78)
    resp = result.get("inbound_response", {})
    print(f"  Responder Agent:       {resp.get('responder_agent')}")
    print(f"  Placement Eligibility: {resp.get('placement_eligibility')}")
    print(f"  Readiness Score:       {resp.get('readiness_score')}%")
    print(f"  Assigned Tier:         {resp.get('placement_tier')}")
    print(f"  Handshake Signature:   {resp.get('digital_handshake_signature')}")
    print(f"  Recommendations:       {', '.join(resp.get('recommendations', [])) or 'None (All criteria met)'}")
    print("-" * 78)
    print(f"Total Socket Round-Trip Latency: {result.get('round_trip_latency_ms')} ms")
    print("=" * 78)


if __name__ == "__main__":
    main()
