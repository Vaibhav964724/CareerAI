"""
Assignment 3.2: Self-Interested Agent Utility Optimization for E-Commerce / Resource Allocation
Architecture: Multi-Attribute Utility Theory (MAUT) Constrained Optimization Engine (Unit-3)
Implements:
  - Multi-term mathematical utility scoring:
      U(x) = [w1*SkillGain + w2*CareerRelevance + w3*Prestige] - [c1*Cost + c2*Time + c3*Difficulty]
  - Evaluation of 10 complex learning/project bundles
  - Strict budget and weekly time constraint boundary checks
  - Global optimal selection and ranked feasible candidate list
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


# 10 Complex Candidate Resource Bundles
CANDIDATE_BUNDLES: List[Dict[str, Any]] = [
    {
        "id": "OPT-01",
        "title": "Full-Stack Cloud & DevOps Mastery Bundle",
        "provider": "CloudScale Academy",
        "cost_usd": 120.0,
        "hours_per_week": 14.0,
        "skill_gain": 92.0,           # 0 - 100
        "career_relevance": 95.0,     # 0 - 100
        "prestige_rating": 90.0,      # 0 - 100
        "difficulty_factor": 0.70     # 0.0 - 1.0
    },
    {
        "id": "OPT-02",
        "title": "Applied Machine Learning & Deep Learning Specialization",
        "provider": "NeuralTech Institute",
        "cost_usd": 150.0,
        "hours_per_week": 18.0,
        "skill_gain": 96.0,
        "career_relevance": 93.0,
        "prestige_rating": 96.0,
        "difficulty_factor": 0.85
    },
    {
        "id": "OPT-03",
        "title": "FastAPI Microservices & Distributed Backend Kit",
        "provider": "PyPro Lab",
        "cost_usd": 60.0,
        "hours_per_week": 8.0,
        "skill_gain": 85.0,
        "career_relevance": 88.0,
        "prestige_rating": 82.0,
        "difficulty_factor": 0.50
    },
    {
        "id": "OPT-04",
        "title": "AWS Certified Solutions Architect Associate Prep",
        "provider": "CloudGuild",
        "cost_usd": 100.0,
        "hours_per_week": 10.0,
        "skill_gain": 80.0,
        "career_relevance": 94.0,
        "prestige_rating": 95.0,
        "difficulty_factor": 0.60
    },
    {
        "id": "OPT-05",
        "title": "Data Structures & Competitive Algorithms Sprint",
        "provider": "AlgoElite",
        "cost_usd": 40.0,
        "hours_per_week": 12.0,
        "skill_gain": 90.0,
        "career_relevance": 85.0,
        "prestige_rating": 80.0,
        "difficulty_factor": 0.75
    },
    {
        "id": "OPT-06",
        "title": "Cybersecurity Analyst & Threat Hunting Bootcamp",
        "provider": "CyberShield Defense",
        "cost_usd": 180.0,
        "hours_per_week": 22.0,
        "skill_gain": 88.0,
        "career_relevance": 80.0,
        "prestige_rating": 87.0,
        "difficulty_factor": 0.80
    },
    {
        "id": "OPT-07",
        "title": "Modern React & TypeScript Enterprise Development",
        "provider": "FrontendMasters Guild",
        "cost_usd": 50.0,
        "hours_per_week": 7.0,
        "skill_gain": 82.0,
        "career_relevance": 89.0,
        "prestige_rating": 84.0,
        "difficulty_factor": 0.45
    },
    {
        "id": "OPT-08",
        "title": "Autonomous AI Agents & Multi-Agent Systems Workshop",
        "provider": "AgiLabs Foundation",
        "cost_usd": 75.0,
        "hours_per_week": 9.0,
        "skill_gain": 94.0,
        "career_relevance": 92.0,
        "prestige_rating": 94.0,
        "difficulty_factor": 0.65
    },
    {
        "id": "OPT-09",
        "title": "Big Data Pipelines with Apache Spark & Kafka",
        "provider": "DataFlow Forge",
        "cost_usd": 140.0,
        "hours_per_week": 16.0,
        "skill_gain": 89.0,
        "career_relevance": 87.0,
        "prestige_rating": 88.0,
        "difficulty_factor": 0.75
    },
    {
        "id": "OPT-10",
        "title": "Executive Tech Leadership & System Design Masterclass",
        "provider": "Architect Guild",
        "cost_usd": 220.0,
        "hours_per_week": 12.0,
        "skill_gain": 78.0,
        "career_relevance": 84.0,
        "prestige_rating": 92.0,
        "difficulty_factor": 0.60
    }
]


class MultiAttributeUtilityOptimizer:
    """
    Evaluates resource bundles using Multi-Attribute Utility Theory (MAUT).
    Scores positive attributes against negative costs and penalizes constraint violations.
    """
    def __init__(
        self,
        weight_skill: float = 0.40,
        weight_relevance: float = 0.35,
        weight_prestige: float = 0.25,
        cost_weight_price: float = 0.45,
        cost_weight_time: float = 0.40,
        cost_weight_difficulty: float = 0.15,
        budget_limit_usd: float = 160.0,
        time_limit_hours: float = 18.0
    ):
        self.w_skill = weight_skill
        self.w_rel = weight_relevance
        self.w_prestige = weight_prestige
        
        self.c_price = cost_weight_price
        self.c_time = cost_weight_time
        self.c_diff = cost_weight_difficulty

        self.budget_limit = budget_limit_usd
        self.time_limit = time_limit_hours

    def calculate_bundle_utility(
        self,
        bundle: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates mathematical utility breakdown:
          Positive Gross Score: S(x) in [0, 100]
          Negative Cost Penalty: C(x) in [0, 100]
          Net Utility: U(x) = S(x) - C(x)
        """
        # Gross Positive Utility
        s_skill = bundle["skill_gain"]
        s_rel = bundle["career_relevance"]
        s_prest = bundle["prestige_rating"]

        gross_score = (
            self.w_skill * s_skill +
            self.w_rel * s_rel +
            self.w_prestige * s_prest
        )

        # Normalized Negative Costs
        # Max scale bounds for normalization: Price max $250, Time max 25h/week
        norm_price = min(100.0, (bundle["cost_usd"] / 250.0) * 100.0)
        norm_time = min(100.0, (bundle["hours_per_week"] / 25.0) * 100.0)
        norm_diff = bundle["difficulty_factor"] * 100.0

        cost_penalty = (
            self.c_price * norm_price +
            self.c_time * norm_time +
            self.c_diff * norm_diff
        )

        net_utility = gross_score - cost_penalty

        # Check constraint feasibility
        is_budget_exceeded = bundle["cost_usd"] > self.budget_limit
        is_time_exceeded = bundle["hours_per_week"] > self.time_limit
        is_feasible = (not is_budget_exceeded) and (not is_time_exceeded)

        violation_notes = []
        if is_budget_exceeded:
            violation_notes.append(f"Exceeds budget limit (${bundle['cost_usd']} > ${self.budget_limit})")
        if is_time_exceeded:
            violation_notes.append(f"Exceeds time commitment limit ({bundle['hours_per_week']}h > {self.time_limit}h)")

        return {
            "id": bundle["id"],
            "title": bundle["title"],
            "provider": bundle["provider"],
            "cost_usd": bundle["cost_usd"],
            "hours_per_week": bundle["hours_per_week"],
            "gross_score": round(gross_score, 2),
            "cost_penalty": round(cost_penalty, 2),
            "net_utility": round(net_utility, 2),
            "is_feasible": is_feasible,
            "violations": violation_notes
        }

    def optimize(
        self,
        custom_bundles: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates all candidate bundles, filters feasible options,
        and selects the global maximum utility configuration.
        """
        bundles = custom_bundles or CANDIDATE_BUNDLES
        evaluated = [self.calculate_bundle_utility(b) for b in bundles]

        # Feasible vs Infeasible
        feasible_options = [e for e in evaluated if e["is_feasible"]]
        infeasible_options = [e for e in evaluated if not e["is_feasible"]]

        # Sort feasible options descending by net utility
        feasible_options.sort(key=lambda x: x["net_utility"], reverse=True)

        optimal_bundle = feasible_options[0] if feasible_options else None

        return {
            "optimal_bundle": optimal_bundle,
            "total_options_evaluated": len(bundles),
            "feasible_count": len(feasible_options),
            "infeasible_count": len(infeasible_options),
            "ranked_feasible_options": feasible_options,
            "infeasible_options": infeasible_options,
            "constraints_applied": {
                "budget_limit_usd": self.budget_limit,
                "time_limit_hours": self.time_limit
            },
            "utility_weights": {
                "skill": self.w_skill,
                "relevance": self.w_rel,
                "prestige": self.w_prestige,
                "price": self.c_price,
                "time": self.c_time,
                "difficulty": self.c_diff
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
