"""
Assignment 4.2: Knowledge Representation and Adaptive API Integration
Component: Structured Domain Ontology Engine
"""

import json
import os
from typing import Dict, Any, List, Optional, Set


class CareerOntologyEngine:
    """
    Manages and queries formal structured domain knowledge:
      - Role skill taxonomies
      - Prerequisite dependency graphs
      - Bloom's proficiency level semantics
      - Role certification mappings
    """
    _instance: Optional['CareerOntologyEngine'] = None

    def __init__(self, ontology_path: Optional[str] = None):
        if ontology_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ontology_path = os.path.join(current_dir, "career_ontology.json")
        self.ontology_path = ontology_path
        self._data: Dict[str, Any] = {}
        self.load_ontology()

    @classmethod
    def get_instance(cls) -> 'CareerOntologyEngine':
        if cls._instance is None:
            cls._instance = CareerOntologyEngine()
        return cls._instance

    def load_ontology(self):
        if os.path.exists(self.ontology_path):
            with open(self.ontology_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {"roles": {}, "prerequisite_graph": {}, "skill_taxonomies": {}}

    def get_all_roles(self) -> List[str]:
        return list(self._data.get("roles", {}).keys())

    def get_all_categories(self) -> List[str]:
        return list(self._data.get("skill_taxonomies", {}).keys())

    def get_prerequisite_graph(self) -> Dict[str, List[str]]:
        return self._data.get("prerequisite_graph", {})

    def get_role_requirements(self, role_name: str) -> Optional[Dict[str, Any]]:
        return self._data.get("roles", {}).get(role_name)

    def get_prerequisites_for_skill(self, skill_name: str) -> List[str]:
        return self._data.get("prerequisite_graph", {}).get(skill_name, [])

    def check_prerequisites_satisfied(self, target_skill: str, acquired_skills: List[str]) -> Dict[str, Any]:
        """
        Validates prerequisite tree: determines if student can begin learning target_skill
        or must first resolve foundational prerequisites.
        """
        prereqs = self.get_prerequisites_for_skill(target_skill)
        acquired_set = {s.lower() for s in acquired_skills}
        missing_prereqs = [p for p in prereqs if p.lower() not in acquired_set]
        
        return {
            "target_skill": target_skill,
            "prerequisites_required": prereqs,
            "prerequisites_satisfied": len(missing_prereqs) == 0,
            "missing_prerequisites": missing_prereqs
        }

    def get_taxonomy_category(self, skill_name: str) -> str:
        for cat, skills in self._data.get("skill_taxonomies", {}).items():
            if any(skill_name.lower() == s.lower() for s in skills):
                return cat
        return "GENERAL_COMPUTING"

    def get_raw_ontology(self) -> Dict[str, Any]:
        return self._data
