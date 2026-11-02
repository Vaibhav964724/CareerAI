"""
========================================================================================
ASSIGNMENT 3.2: SELF-INTERESTED AGENT UTILITY OPTIMIZATION FOR RESOURCE ALLOCATION
Course: Agent Technology (Unit-3)
Scenario: Optimal Learning Bundle Allocation under Multi-Attribute Constraints in CareerAI
========================================================================================
Description:
  This script demonstrates Multi-Attribute Utility Theory (MAUT) optimization.
  An autonomous self-interested agent evaluates a complex catalog of 10 course/project
  bundles against student resource constraints (Budget <= $160, Weekly Time <= 18h).
  The agent calculates Gross Value, Cost Penalty, and Net Utility U(x) to mathematically
  select the global maximum feasible candidate.
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

from app.agent.utility_optimizer import MultiAttributeUtilityOptimizer, CANDIDATE_BUNDLES


def main():
    print("=" * 82)
    print("  ASSIGNMENT 3.2: SELF-INTERESTED AGENT UTILITY OPTIMIZATION (10 OPTIONS)")
    print("=" * 82)

    budget_limit = 160.0
    time_limit = 18.0
    optimizer = MultiAttributeUtilityOptimizer(
        weight_skill=0.40,
        weight_relevance=0.35,
        weight_prestige=0.25,
        cost_weight_price=0.45,
        cost_weight_time=0.40,
        cost_weight_difficulty=0.15,
        budget_limit_usd=budget_limit,
        time_limit_hours=time_limit
    )

    print("\n[Optimization Parameters & Weights]")
    print("  Utility Equation: U(x) = [0.40*Skill + 0.35*Relevance + 0.25*Prestige] - [0.45*CostNorm + 0.40*TimeNorm + 0.15*DiffNorm]")
    print(f"  Hard Constraints: Budget <= ${budget_limit:.2f} | Time <= {time_limit:.1f} hours/week")

    print("\n[Evaluating All 10 Candidate Resource Bundles]...")
    result = optimizer.optimize()

    print("\n" + "-" * 82)
    print(f"{'ID':<7} | {'Title':<32} | {'Cost':<6} | {'Hours':<6} | {'Gross':<6} | {'CostPen':<8} | {'Net U':<6} | {'Status'}")
    print("-" * 82)

    # Show ranked feasible first
    for b in result["ranked_feasible_options"]:
        is_opt = (b["id"] == result["optimal_bundle"]["id"])
        tag = "** OPTIMAL **" if is_opt else "FEASIBLE"
        print(f"{b['id']:<7} | {b['title'][:32]:<32} | ${b['cost_usd']:<5.0f} | {b['hours_per_week']:<4.0f}h | {b['gross_score']:<6.2f} | {b['cost_penalty']:<8.2f} | {b['net_utility']:<6.2f} | {tag}")

    # Show infeasible options with violation diagnostics
    for b in result["infeasible_options"]:
        violations = ", ".join(b["violations"])
        print(f"{b['id']:<7} | {b['title'][:32]:<32} | ${b['cost_usd']:<5.0f} | {b['hours_per_week']:<4.0f}h | {b['gross_score']:<6.2f} | {b['cost_penalty']:<8.2f} | {b['net_utility']:<6.2f} | REJECTED ({violations})")

    print("-" * 82)
    print(f"\nTotal Evaluated: {result['total_options_evaluated']} | Feasible: {result['feasible_count']} | Infeasible: {result['infeasible_count']}")

    opt = result["optimal_bundle"]
    if opt:
        print("\n" + "=" * 82)
        print("  GLOBAL MAXIMUM OPTIMAL BUNDLE SELECTED")
        print("=" * 82)
        print(f"  Bundle ID:       {opt['id']}")
        print(f"  Title:           {opt['title']}")
        print(f"  Provider:        {opt['provider']}")
        print(f"  Cost:            ${opt['cost_usd']:.2f}")
        print(f"  Time Commitment: {opt['hours_per_week']:.1f} hours/week")
        print(f"  Gross Score:     {opt['gross_score']}/100")
        print(f"  Cost Penalty:    {opt['cost_penalty']}/100")
        print(f"  Net Utility:     {opt['net_utility']:.2f} (Highest feasible payoff)")
        print("=" * 82)


if __name__ == "__main__":
    main()
