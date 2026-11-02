"""
Assignment 4.2: Knowledge Representation and Adaptive API Integration
Component: Adaptive Knowledge Service (Ontology + Live API -> Plan Adaptation)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.knowledge.ontology_engine import CareerOntologyEngine
from app.knowledge.external_api_client import ExternalCareerAPIClient, LiveKnowledgeResource


class AdaptiveKnowledgeService:
    """
    Orchestrates semantic domain ontology querying and live REST API data ingestion
    to dynamically adapt agent roadmap milestones and learning recommendations.
    """
    def __init__(self):
        self.ontology = CareerOntologyEngine.get_instance()
        self.api_client = ExternalCareerAPIClient()
        self.adaptation_history: List[Dict[str, Any]] = []

    def adapt_roadmap_with_live_knowledge(
        self,
        student_id: str,
        target_role: str,
        current_skills: List[str],
        primary_skill_gap: str
    ) -> Dict[str, Any]:
        """
        1. Query ontology for formal role criteria & prerequisite dependencies.
        2. Ingest live REST API resources for the primary skill gap.
        3. Dynamically synthesize an adapted capstone milestone action.
        """
        # 1. Ontology Validation
        role_info = self.ontology.get_role_requirements(target_role)
        prereq_check = self.ontology.check_prerequisites_satisfied(primary_skill_gap, current_skills)

        # 2. Live API Ingestion
        live_resources = self.api_client.fetch_live_skill_resources(primary_skill_gap, max_results=3)

        # 3. Dynamic Plan Adaptation Decision
        best_resource = live_resources[0] if live_resources else None
        
        adapted_milestone = {
            "title": f"Production Implementation: {primary_skill_gap} Hands-On Capstone",
            "skill": primary_skill_gap,
            "taxonomy_category": self.ontology.get_taxonomy_category(primary_skill_gap),
            "prerequisites_satisfied": prereq_check["prerequisites_satisfied"],
            "missing_prerequisites": prereq_check["missing_prerequisites"],
            "recommended_live_project": best_resource.to_dict() if best_resource else None,
            "external_reference_url": best_resource.source_url if best_resource else "https://github.com",
            "adapted_difficulty": "ADVANCED" if (best_resource and best_resource.stars_or_rating > 50000) else "INTERMEDIATE",
            "adaptation_rationale": f"Injected real-world {primary_skill_gap} repository ({best_resource.title if best_resource else 'N/A'}) with {best_resource.stars_or_rating if best_resource else 0} community stars"
        }

        adaptation_record = {
            "student_id": student_id,
            "target_role": target_role,
            "skill_gap_evaluated": primary_skill_gap,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ontology_role_tier": role_info.get("tier", "Standard") if role_info else "Standard",
            "api_endpoint_invoked": self.api_client.GITHUB_SEARCH_URL,
            "api_metadata": self.api_client.last_response_metadata,
            "resources_ingested_count": len(live_resources),
            "adapted_milestone": adapted_milestone
        }
        self.adaptation_history.append(adaptation_record)

        return {
            "status": "ADAPTATION_COMPLETE",
            "adaptation_record": adaptation_record,
            "live_resources": [r.to_dict() for r in live_resources]
        }
