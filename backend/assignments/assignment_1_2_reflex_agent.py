"""
========================================================================================
ASSIGNMENT 1.2: RULE-BASED ENVIRONMENTAL REASONER IMPLEMENTATION
Course: Agent Technology (Unit-1)
Scenario: Real-Time Environmental Telemetry Stream Reasoning in CareerAI
========================================================================================
Description:
  This script demonstrates a Simple Reflex Agent utilizing Condition-Action rules.
  It ingests a dynamic stream of environmental telemetry packets (student velocity,
  burnout score, and job market demand surges), evaluates prioritized rules,
  and fires immediate reactive adaptation logs.
========================================================================================
"""

import sys
import os
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

from app.agent.reflex_reasoner import (
    ReflexEnvironmentalReasoner,
    generate_synthetic_telemetry_stream,
    TelemetryPacket
)


def main():
    print("=" * 78)
    print("  ASSIGNMENT 1.2: SIMPLE REFLEX AGENT & ENVIRONMENTAL REASONER DEMO")
    print("=" * 78)

    reasoner = ReflexEnvironmentalReasoner()
    print(f"\n[Agent Initialization] Loaded {len(reasoner.rules)} Condition-Action Rules:")
    for rule in reasoner.rules:
        print(f"  * [Priority {rule.priority}] {rule.rule_id}: {rule.description}")

    print("\n[Sensory Stream Generator] Simulating 6 Real-Time Telemetry Packets...")
    packets = generate_synthetic_telemetry_stream(count=6)

    print("\n" + "-" * 78)
    print(f"{'Packet ID':<12} | {'Timestamp':<20} | {'Hours/Wk':<10} | {'Burnout':<8} | {'Market Surge'}")
    print("-" * 78)
    for i, p in enumerate(packets, 1):
        print(f"PKT-{i:03d}     | {p.timestamp[:19]:<20} | {p.study_hours_past_week:<10.1f} | {p.burnout_index:<8.1f} | {p.market_demand_surge}")
    print("-" * 78)

    print("\n[Agent Execution Loop] Processing Stream through Condition-Action Rules...")
    print("=" * 78)

    for i, packet in enumerate(packets, 1):
        print(f"\n>>> INGESTING SENSORY FRAME #{i} [Student: {packet.student_id}]")
        triggered_action = reasoner.evaluate_packet(packet)
        if triggered_action:
            print(f"    --> [CONDITION MATCHED]: {triggered_action.rule_name}")
            print(f"    --> [SEVERITY LEVEL]:   {triggered_action.action_type}")
            print(f"    --> [REACTIVE ACTION]:  {triggered_action.payload.get('recommendation')}")
        else:
            print("    --> [NO ACTION]: All sensory metrics within nominal tolerances.")
        time.sleep(0.08)

    print("\n" + "=" * 78)
    print(f"Execution Complete. Total Sensory Evaluations: {len(packets)} | Total Actions Fired: {len(reasoner.execution_log)}")
    print("=" * 78)


if __name__ == "__main__":
    main()
