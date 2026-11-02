"""
========================================================================================
ASSIGNMENT 3.1: MULTI-AGENT COORDINATION PROTOCOL EXECUTION
Course: Agent Technology (Unit-3)
Scenario: Multi-Turn Capstone Internship Negotiation Protocol in CareerAI
========================================================================================
Description:
  This script demonstrates a multi-agent negotiation system with independent agents:
  StudentAgent (seeking higher stipend, lower weekly hours, high mentorship) and
  RecruiterAgent (seeking lower stipend, higher weekly hours, lower mentorship).
  Agents exchange proposals using time-dependent concession curves alpha(t) until
  reaching a consensus handshake or max turns.
========================================================================================
"""

import sys
import os

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

from app.agent.negotiation_protocol import MultiAgentNegotiator


def main():
    print("=" * 78)
    print("  ASSIGNMENT 3.1: MULTI-AGENT NEGOTIATION PROTOCOL & CONSENSUS HANDSHAKE")
    print("=" * 78)

    negotiator = MultiAgentNegotiator(max_turns=6)
    
    print("\n[Agent Preference Parameters]")
    print(f"  Student Agent:   Reservation Utility >= {negotiator.student.prefs.reservation_utility:.2f} | Concession Power k={negotiator.student.prefs.concession_power}")
    print(f"  Recruiter Agent: Reservation Utility >= {negotiator.recruiter.prefs.reservation_utility:.2f} | Concession Power k={negotiator.recruiter.prefs.concession_power}")
    print(f"  Target Terms:    Monthly Stipend ($), Weekly Hours (h), Mentorship Sessions/Mo (m)")

    print("\n[Executing Multi-Turn Negotiation Loop]...")
    result = negotiator.execute_negotiation(student_target_stipend=2300, recruiter_budget_ceiling=2500)

    print("\n" + "-" * 78)
    print(f"{'Turn':<6} | {'Proposer':<16} | {'Stipend':<10} | {'Hours':<8} | {'Mentor':<8} | {'U_Student':<10} | {'U_Recruiter':<10} | {'Action'}")
    print("-" * 78)

    for item in result["timeline"]:
        offer = item["offer"]
        print(f"Turn {item['turn']:<2} | {item['proposer']:<16} | ${offer['stipend']:<9} | {offer['hours']}h/wk   | {offer['mentorship']} ses/mo | {item['student_utility']:<10.3f} | {item['recruiter_utility']:<10.3f} | {item['action']}")

    print("-" * 78)
    print(f"\nFinal Status:        {result['status']}")
    print(f"Consensus Reached:   {result['consensus_reached']}")
    print(f"Total Turns Elapsed: {result['total_turns']}")

    if result["consensus_reached"]:
        ag = result["final_agreement"]
        print(f"\n[MUTUAL CONSENSUS AGREEMENT ACHIEVED]")
        print(f"  * Monthly Stipend:        ${ag['stipend']}")
        print(f"  * Weekly Workload:        {ag['hours']} hours/week")
        print(f"  * Mentorship Sessions:    {ag['mentorship']} sessions/month")
        print(f"  * Digital Handshake Sign: {result['handshake_signature']}")
    else:
        print("\n[NEGOTIATION IMPASSE] Reservation thresholds were not met within allotted turns.")

    print("=" * 78)


if __name__ == "__main__":
    main()
