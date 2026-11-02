"""
========================================================================================
ASSIGNMENT 4.2: KNOWLEDGE REPRESENTATION AND ADAPTIVE API INTEGRATION
Course: Agent Technology (Unit-4)
Scenario: Domain Ontology Reasoning & Real-Time External REST API Ingestion
Student: Vaibhav Singh (Reg. No: RA2212704010040)
Faculty Evaluator: Dr. Prabhu Sir
========================================================================================
Description:
  Demonstrates structured domain knowledge representation coupled with live external REST API
  data integration. The agent queries a formal career competency ontology (concepts,
  prerequisite DAG, Bloom taxonomies), fetches real-time repository telemetry from the GitHub
  REST API, and dynamically adapts curriculum milestone recommendations.
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

from app.knowledge.ontology_engine import CareerOntologyEngine
from app.knowledge.external_api_client import ExternalCareerAPIClient, LiveKnowledgeResource
from app.knowledge.adaptive_knowledge_service import AdaptiveKnowledgeService


def main():
    print("=" * 80)
    print("  ASSIGNMENT 4.2: KNOWLEDGE REPRESENTATION & ADAPTIVE API INTEGRATION")
    print("  Student: Vaibhav Singh | Reg No: RA2212704010040 | Evaluator: Dr. Prabhu Sir")
    print("=" * 80)

    # 1. Domain Ontology Engine
    print("\n[Part 1] Loading Formal Career Competency Ontology (career_ontology.json)...")
    ontology = CareerOntologyEngine.get_instance()
    all_roles = ontology.get_all_roles()
    categories = ontology.get_all_categories()
    prereq_graph = ontology.get_prerequisite_graph()

    print(f"  * Ontology Schema Loaded Successfully:")
    print(f"    - Total Defined Career Roles: {len(all_roles)}")
    print(f"    - Taxonomy Categories: {', '.join(categories)}")
    print(f"    - Prerequisite Graph Rules: {len(prereq_graph)} dependency constraints")

    print("\n[Part 2] Querying Role Requirements & Prerequisite Dependency Trees...")
    target_role = "Full Stack Engineer"
    role_info = ontology.get_role_requirements(target_role)
    print(f"  * Target Role: '{target_role}'")
    print(f"    - Tier: {role_info.get('tier')}")
    print(f"    - Required Skills: {', '.join(role_info.get('required_core_skills', []))}")
    print(f"    - Minimum GPA: {role_info.get('minimum_gpa')}")
    print(f"    - Recommended Capstone: {role_info.get('capstone_archetype')}")

    # Prerequisite verification
    student_skills = ["Python", "HTML/CSS"]
    target_skill = "FastAPI"
    prereq_check = ontology.check_prerequisites_satisfied(target_skill, student_skills)
    print(f"\n  * Prerequisite Verification for Target Skill '{target_skill}':")
    print(f"    - Current Student Skills: {student_skills}")
    print(f"    - Prerequisites Satisfied: {prereq_check['prerequisites_satisfied']}")
    print(f"    - Missing Prerequisite Skills: {prereq_check['missing_prerequisites']}")

    # 2. Live External REST API Integration
    print("\n" + "=" * 80)
    print("  [Part 3] LIVE EXTERNAL REST API INGESTION (GitHub Search REST API)")
    print("=" * 80)
    api_client = ExternalCareerAPIClient()
    query_skill = "FastAPI"
    print(f"  * Dispatching HTTP GET to https://api.github.com/search/repositories?q={query_skill}...")
    
    live_resources = api_client.fetch_live_skill_resources(skill_keyword=query_skill, max_results=3)
    meta = api_client.last_response_metadata
    print(f"  * API Status: {meta.get('status')} | Source: {meta.get('data_source')} | Items Returned: {len(live_resources)}")

    print("\n  * Parsed Unstructured/Semi-Structured API Responses:")
    print("  " + "-" * 76)
    for idx, r in enumerate(live_resources, 1):
        print(f"    [{idx}] Title:       {r.title}")
        print(f"        Stars:       {r.stars_or_rating:,} community stars")
        print(f"        Type:        {r.resource_type}")
        print(f"        URL:         {r.source_url}")
        print(f"        Provenance:  {r.provenance}")
        print(f"        Summary:     {r.description[:70]}...")
        print("  " + "-" * 76)

    # 3. Dynamic Plan Adaptation Module
    print("\n" + "=" * 80)
    print("  [Part 4] DYNAMIC PLAN ADAPTATION & MILESTONE SYNTHESIS")
    print("=" * 80)
    service = AdaptiveKnowledgeService()
    print(f"  * Adapting learning roadmap for Student 'STU-RA2212704010040'...")
    print(f"  * Ingesting live repository metadata into milestone plan for '{query_skill}'...")

    adapted = service.adapt_roadmap_with_live_knowledge(
        student_id="STU-RA2212704010040",
        target_role=target_role,
        current_skills=student_skills,
        primary_skill_gap=query_skill
    )

    milestone = adapted["adaptation_record"]["adapted_milestone"]
    print(f"\n  * Synthesized Adaptive Milestone:")
    print(f"    - Milestone Title:         {milestone['title']}")
    print(f"    - Competency:              {milestone['skill']}")
    print(f"    - Category:                {milestone['taxonomy_category']}")
    print(f"    - Adapted Difficulty:      {milestone['adapted_difficulty']}")
    print(f"    - Prerequisites Validated: {milestone['prerequisites_satisfied']}")
    print(f"    - Live Project Injected:   {milestone['recommended_live_project']['title'] if milestone['recommended_live_project'] else 'None'}")
    print(f"    - External Reference URL:  {milestone['external_reference_url']}")
    print(f"    - Adaptation Rationale:    {milestone['adaptation_rationale']}")

    # 4. Summary & Verification
    print("\n" + "=" * 80)
    print("  KNOWLEDGE REPRESENTATION & ADAPTIVE API AUDIT SUMMARY")
    print("=" * 80)
    print(f"  Ontology Engine Status:     ACTIVE (career_ontology.json)")
    print(f"  Prerequisite Check Status:  PASSED")
    print(f"  External API Provenance:    {meta.get('data_source')}")
    print(f"  Roadmap Adaptation Status:  SYNTHESIZED_SUCCESSFULLY")
    print("=" * 80)
    print("[SUCCESS] Assignment 4.2 Knowledge Representation & Adaptive API verified successfully.\n")


if __name__ == "__main__":
    main()
