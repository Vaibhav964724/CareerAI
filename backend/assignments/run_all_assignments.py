"""
========================================================================================
CONSOLIDATED ACADEMIC ASSIGNMENTS RUNNER: AGENT TECHNOLOGY (UNITS 1, 2, 3, 4, AND 5)
Project: CareerAI - Autonomous & Persistent AI Career Guidance Agent
Student: Vaibhav Singh | Reg No: RA2212704010040 | Evaluator: Dr. Prabhu Sir
========================================================================================
This runner sequentially invokes and validates all nine curriculum assignments:
  1. Assignment 1.2: Rule-Based Environmental Reflex Reasoner
  2. Assignment 2.1: Concurrent Background Task Daemon & Thread Metrics
  3. Assignment 2.2: Distributed Agent TCP Socket Messaging & Serialization
  4. Assignment 3.1: Multi-Agent Coordination Protocol & Bidding Handshake
  5. Assignment 3.2: Self-Interested Agent Utility Optimization (10 Options)
  6. Assignment 4.1: Belief-Desire-Intention (BDI) Cognitive Modeling & Intention Shift
  7. Assignment 4.2: Knowledge Representation, Ontology & Real-Time REST API Ingestion
  8. Assignment 5.1: Cryptographic Authentication, HMAC Integrity & Attack Mitigation
  9. Assignment 5.2: Consolidated Capstone Pipeline Execution Across All 5 Units
========================================================================================
"""

import sys
import os
import subprocess
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    ("Assignment 1.2", "assignment_1_2_reflex_agent.py", "Rule-Based Environmental Reasoner (Unit-1)"),
    ("Assignment 2.1", "assignment_2_1_daemon_worker.py", "Concurrent Task Daemonization (Unit-2)"),
    ("Assignment 2.2", "assignment_2_2_socket_messaging.py", "Distributed Agent Sockets (Unit-2)"),
    ("Assignment 3.1", "assignment_3_1_negotiation.py", "Multi-Agent Coordination Protocol (Unit-3)"),
    ("Assignment 3.2", "assignment_3_2_utility_optimizer.py", "Self-Interested Utility Optimizer (Unit-3)"),
    ("Assignment 4.1", "assignment_4_1_bdi.py", "BDI Architecture & Dynamic Shift (Unit-4)"),
    ("Assignment 4.2", "assignment_4_2_knowledge_api.py", "Domain Ontology & Adaptive REST API (Unit-4)"),
    ("Assignment 5.1", "assignment_5_1_security.py", "Cryptographic Signatures & Attack Defense (Unit-5)"),
    ("Assignment 5.2", "assignment_5_2_capstone.py", "Consolidated Capstone Master Pipeline (Unit-5)")
]


def run_all():
    print("=" * 86)
    print("      CAREERAI - AGENT TECHNOLOGY CONSOLIDATED ASSIGNMENT SUITE EXECUTION")
    print("=" * 86)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Assignments to Execute: {len(SCRIPTS)}\n")

    passed_count = 0
    results_summary = []

    for name, script_name, description in SCRIPTS:
        script_path = os.path.join(CURRENT_DIR, script_name)
        print(f"\n{'#' * 86}")
        print(f"  RUNNING: {name} - {description}")
        print(f"{'#' * 86}\n")

        t_start = time.perf_counter()
        proc = subprocess.run([sys.executable, script_path], capture_output=False)
        elapsed = round((time.perf_counter() - t_start), 2)

        if proc.returncode == 0:
            print(f"\n>>> [STATUS: SUCCESS] {name} completed in {elapsed}s.")
            passed_count += 1
            results_summary.append((name, description, "PASS", f"{elapsed}s"))
        else:
            print(f"\n>>> [STATUS: FAILED] {name} exited with code {proc.returncode} in {elapsed}s.")
            results_summary.append((name, description, f"FAIL ({proc.returncode})", f"{elapsed}s"))

    print("\n\n" + "=" * 86)
    print("                     CONSOLIDATED EXECUTION SUMMARY REPORT")
    print("=" * 86)
    print(f"{'Assignment ID':<18} | {'Description':<42} | {'Status':<10} | {'Duration'}")
    print("-" * 86)
    for aid, desc, status, duration in results_summary:
        print(f"{aid:<18} | {desc:<42} | {status:<10} | {duration}")
    print("-" * 86)
    print(f"Final Score: {passed_count}/{len(SCRIPTS)} Assignments Executed Successfully.")
    print("=" * 86)


if __name__ == "__main__":
    run_all()
