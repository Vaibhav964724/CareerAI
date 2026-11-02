"""
Knowledge Representation and Adaptive API Package
Exports CareerOntologyEngine, ExternalCareerAPIClient, and AdaptiveKnowledgeService
"""

from app.knowledge.ontology_engine import CareerOntologyEngine
from app.knowledge.external_api_client import ExternalCareerAPIClient, LiveKnowledgeResource
from app.knowledge.adaptive_knowledge_service import AdaptiveKnowledgeService

__all__ = [
    "CareerOntologyEngine",
    "ExternalCareerAPIClient",
    "LiveKnowledgeResource",
    "AdaptiveKnowledgeService"
]
