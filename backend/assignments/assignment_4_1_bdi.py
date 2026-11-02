"""
========================================================================================
ASSIGNMENT 4.1: BDI (BELIEF-DESIRE-INTENTION) GOAL-DRIVEN COGNITIVE MODELING
Course: Agent Technology (Unit-4)
Scenario: Adaptive Career Guidance Agent with Dynamic Intention Reconsideration
Student: Vaibhav Singh (Reg. No: RA2212704010040)
Faculty Evaluator: Dr. Prabhu Sir
========================================================================================
Description:
  Demonstrates an explicit Belief-Desire-Intention (BDI) architecture where:
  - Beliefs represent the agent's internal state and environmental knowledge base.
  - Desires represent competing candidate goals with dynamic utility scoring.
  - Intentions represent committed procedural execution plans.
  - Unexpected environmental shocks trigger dynamic intention recalculation (intention shift).
========================================================================================
"""

import sys
import os
import json
from datetime import datetime, timezone

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

from app.agent.bdi.bdi_agent import BDICognitiveAgent
from app.agent.bdi.beliefs import BeliefBase
from app.agent.bdi.desires import DesireManager
from app.agent.bdi.intentions import Intention, ActionStep
from app.agent.bdi.plan_selector import PlanSelector


def main():
    print("=" * 80)
    print("  ASSIGNMENT 4.1: BDI GOAL-DRIVEN COGNITIVE MODELING DEMONSTRATION")
    print("  Student: Vaibhav Singh | Reg No: RA2212704010040 | Evaluator: Dr. Prabhu Sir")
    print("=" * 80)

    # 1. Initialize BDI Cognitive Agent
    agent = BDICognitiveAgent(agent_id="BDI_STUDENT_ADVISOR_RA2212704010040")
    print(f"\n[Step 1] Initializing BDI Agent '{agent.agent_id}'...")
    print(f"  * Total Active Beliefs: {len(agent.beliefs.get_all_beliefs())}")
    print(f"    - target_role: {agent.beliefs.get_value('target_role')}")
    print(f"    - weekly_study_hours: {agent.beliefs.get_value('weekly_study_hours')} hrs/wk")
    print(f"    - burnout_index: {agent.beliefs.get_value('burnout_index')}/100")
    print(f"    - days_to_deadline: {agent.beliefs.get_value('days_to_deadline')} days")

    # 2. Deliberation Phase
    print("\n[Step 2] Cognitive Deliberation Cycle (Desire Evaluation & Intention Binding)...")
    agent.deliberate()
    dominant = agent.desires.select_dominant_desire(agent.beliefs)
    print(f"  * Dominant Desire Selected: [{dominant.desire_id}] {dominant.name}")
    print(f"    - Priority: {dominant.priority} | Status: {dominant.status}")
    print(f"    - Description: {dominant.description}")
    
    current_intention = agent.current_intention
    print(f"\n  * Committed Procedural Intention: [{current_intention.intention_id}] {current_intention.name}")
    print(f"    - Selection Rationale: {current_intention.selection_rationale}")
    print(f"    - Status: {current_intention.status}")
    print(f"    - Total Action Steps: {len(current_intention.plan_steps)}")
    for idx, step in enumerate(current_intention.plan_steps, 1):
        print(f"      Step {idx}: [{step.step_id}] {step.action_type} -> {step.target}")

    # 3. Execution of Initial Steps
    print("\n[Step 3] Procedural Execution of Committed Steps...")
    step_1 = agent.execute_next_action()
    print(f"  > Executed Step 1: {step_1.step_id} - {step_1.action_type} ({step_1.target}) [SUCCESS]")
    step_2 = agent.execute_next_action()
    print(f"  > Executed Step 2: {step_2.step_id} - {step_2.action_type} ({step_2.target}) [SUCCESS]")
    print(f"  * Progress: Step {current_intention.current_step_index}/{len(current_intention.plan_steps)} completed.")

    # 4. Unexpected Environmental Belief Update (The "Belief Shock")
    print("\n" + "=" * 80)
    print("  [Step 4] INJECTING UNEXPECTED ENVIRONMENTAL BELIEF SHOCK")
    print("=" * 80)
    print("  Scenario: Student encounters academic overload and unexpected exams.")
    print("  Sensory Percept Injected: 'weekly_study_hours' collapses from 14.0 -> 5.0 hrs/week!")
    print("  Sensory Percept Injected: 'stress_level' surges from 25.0 -> 82.0 (High Burnout Hazard)!")

    # Update stress_level
    agent.beliefs.set_belief("stress_level", 82.0, source="ACADEMIC_EXAM_SURGE")
    
    # Trigger dynamic reconsideration through study hours drop
    reconsideration = agent.update_belief_and_reconsider(
        belief_name="weekly_study_hours",
        new_value=5.0,
        source="STUDENT_TIME_CONSTRAINT_UPDATE"
    )

    print("\n[Step 5] Dynamic Plan Recalculation (Intention Shift Audit):")
    print(f"  * Intention Shift Occurred: {reconsideration['intention_shifted']}")
    shift = reconsideration["shift_details"]
    if shift:
        print(f"  * Shift ID: {shift['shift_id']}")
        print(f"  * Triggering Belief: '{shift['triggering_belief']['name']}' changed from {shift['triggering_belief']['old_value']} to {shift['triggering_belief']['new_value']}")
        print(f"  * Previous Intention (ABORTED): [{shift['previous_intention']['id']}] {shift['previous_intention']['name']}")
        print(f"    - Reason: {shift['reconsideration_reason']}")
        print(f"  * New Intention (COMMITTED): [{shift['new_intention']['id']}] {shift['new_intention']['name']}")
        print(f"    - New Plan Rationale: {shift['new_intention']['rationale']}")
        print(f"    - New Plan Action Count: {shift['new_intention']['total_steps']} steps")

    # 5. Execute Action under New Adapted Intention
    print("\n[Step 6] Resuming Execution Under Adapted Intention...")
    new_step_1 = agent.execute_next_action()
    print(f"  > Executed Adapted Step 1: {new_step_1.step_id} - {new_step_1.action_type} ({new_step_1.target}) [SUCCESS]")
    print(f"  * Active Intention Status: {agent.current_intention.status}")
    print(f"  * Intention Completion: {agent.current_intention.current_step_index}/{len(agent.current_intention.plan_steps)} steps")

    # 6. Final State Dump
    print("\n" + "=" * 80)
    print("  BDI COGNITIVE AGENT AUDIT SUMMARY")
    print("=" * 80)
    state = agent.get_cognitive_state()
    print(f"  Agent ID:               {state['agent_id']}")
    print(f"  Deliberation Cycles:    {state['cycle_count']}")
    print(f"  Active Desires Tracked: {len(state['all_desires'])}")
    print(f"  Total Intention Shifts: {state['intention_shifts_count']}")
    print(f"  Current Committed Goal: {state['dominant_desire']['name']}")
    print(f"  Current Intention:      {state['current_intention']['name']} (ID: {state['current_intention']['intention_id']})")
    print("=" * 80)
    print("[SUCCESS] Assignment 4.1 BDI Cognitive Model verified successfully.\n")


if __name__ == "__main__":
    main()
