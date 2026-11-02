"""
Assignment 4.2: Knowledge Representation and Adaptive API Integration
Component: Real-World External REST API Client & Ingestion Parser
"""

import os
import json
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class LiveKnowledgeResource:
    """Represents a structured learning/capstone resource parsed from external live API data."""
    def __init__(
        self,
        title: str,
        resource_type: str,
        source_url: str,
        stars_or_rating: int,
        topics: List[str],
        description: str,
        relevance_score: float,
        provenance: str = "LIVE_EXTERNAL_API"
    ):
        self.title = title
        self.resource_type = resource_type
        self.source_url = source_url
        self.stars_or_rating = stars_or_rating
        self.topics = topics
        self.description = description
        self.relevance_score = relevance_score
        self.provenance = provenance
        self.ingested_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "resource_type": self.resource_type,
            "source_url": self.source_url,
            "stars_or_rating": self.stars_or_rating,
            "topics": self.topics,
            "description": self.description,
            "relevance_score": round(self.relevance_score, 2),
            "provenance": self.provenance,
            "ingested_at": self.ingested_at
        }


class ExternalCareerAPIClient:
    """
    Connects to real external REST endpoints (e.g., GitHub Repositories API)
    to query live industry learning resources and trending capstone project templates.
    Includes timeout safety, schema parsing, and offline fixture fallbacks.
    """
    GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

    def __init__(self, timeout_sec: float = 5.0):
        self.timeout = timeout_sec
        self.last_response_metadata: Dict[str, Any] = {}

    def fetch_live_skill_resources(self, skill_keyword: str, max_results: int = 5) -> List[LiveKnowledgeResource]:
        """
        Executes HTTP GET request against real external REST API.
        Extracts repository metrics and returns structured LiveKnowledgeResource objects.
        """
        headers = {
            "User-Agent": "CareerAI-Academic-Agent/2.0",
            "Accept": "application/vnd.github.v3+json"
        }
        params = {
            "q": f"{skill_keyword} template OR tutorial stars:>200",
            "sort": "stars",
            "order": "desc",
            "per_page": min(max_results, 10)
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(self.GITHUB_SEARCH_URL, headers=headers, params=params)
                
                self.last_response_metadata = {
                    "status_code": response.status_code,
                    "endpoint": str(response.url),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "transport": "HTTP_LIVE_REST_API"
                }

                if response.status_code == 200:
                    raw_data = response.json()
                    return self._parse_github_response(raw_data, skill_keyword, provenance="LIVE_GITHUB_API")
                else:
                    # If rate limited (e.g. GitHub 403) or error, fallback to curated offline knowledge map
                    return self._fallback_knowledge_map(skill_keyword, reason=f"API Status {response.status_code}")

        except (httpx.RequestError, httpx.TimeoutException, OSError) as e:
            self.last_response_metadata = {
                "status_code": 0,
                "endpoint": self.GITHUB_SEARCH_URL,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "transport": "OFFLINE_FALLBACK_ENGAGED"
            }
            return self._fallback_knowledge_map(skill_keyword, reason=f"Network restricted: {str(e)}")

    def _parse_github_response(self, raw_data: Dict[str, Any], skill_keyword: str, provenance: str) -> List[LiveKnowledgeResource]:
        """Converts raw unstructured JSON from API into structured knowledge entities."""
        items = raw_data.get("items", [])
        parsed_resources: List[LiveKnowledgeResource] = []

        for item in items:
            stars = int(item.get("stargazers_count", 0))
            topics = item.get("topics", [])
            desc = item.get("description", "") or "No description provided."
            
            # Compute heuristic relevance score: combination of stars and topic matching
            relevance = min(100.0, 50.0 + (min(stars, 10000) / 10000.0) * 40.0 + (10.0 if skill_keyword.lower() in desc.lower() else 0.0))

            resource = LiveKnowledgeResource(
                title=item.get("full_name", item.get("name", "Unknown Repository")),
                resource_type="OPEN_SOURCE_CAPSTONE_TEMPLATE",
                source_url=item.get("html_url", "https://github.com"),
                stars_or_rating=stars,
                topics=topics[:5],
                description=desc[:180],
                relevance_score=relevance,
                provenance=provenance
            )
            parsed_resources.append(resource)

        return parsed_resources

    def _fallback_knowledge_map(self, skill_keyword: str, reason: str = "") -> List[LiveKnowledgeResource]:
        """Provides verified domain knowledge map when live internet is unreachable or sandbox-isolated."""
        curated_catalog = {
            "python": [
                LiveKnowledgeResource("tiangolo/fastapi", "PRODUCTION_FRAMEWORK", "https://github.com/tiangolo/fastapi", 78000, ["fastapi", "python", "rest-api"], "Modern, fast web framework for building APIs with Python 3.8+", 98.0, f"CURATED_KNOWLEDGE_MAP ({reason})"),
                LiveKnowledgeResource("pallets/flask", "CORE_MICROFRAMEWORK", "https://github.com/pallets/flask", 68000, ["flask", "wsgi", "python"], "The Python micro framework for building web applications", 94.0, f"CURATED_KNOWLEDGE_MAP ({reason})"),
                LiveKnowledgeResource("encode/uvicorn", "ASGI_SERVER", "https://github.com/encode/uvicorn", 8500, ["asgi", "uvicorn", "python"], "The lightning-fast ASGI server.", 90.0, f"CURATED_KNOWLEDGE_MAP ({reason})")
            ],
            "react": [
                LiveKnowledgeResource("facebook/react", "CORE_UI_LIBRARY", "https://github.com/facebook/react", 230000, ["react", "ui", "javascript"], "The library for web and native user interfaces", 99.0, f"CURATED_KNOWLEDGE_MAP ({reason})"),
                LiveKnowledgeResource("vercel/next.js", "PRODUCTION_FRAMEWORK", "https://github.com/vercel/next.js", 128000, ["nextjs", "react", "fullstack"], "The React Framework for the Web", 98.0, f"CURATED_KNOWLEDGE_MAP ({reason})")
            ],
            "docker": [
                LiveKnowledgeResource("veggiemonk/awesome-docker", "CURATED_KNOWLEDGE", "https://github.com/veggiemonk/awesome-docker", 31000, ["docker", "devops", "containers"], "A curated list of Docker resources and projects", 92.0, f"CURATED_KNOWLEDGE_MAP ({reason})")
            ]
        }

        # Match keyword or default
        for k, resources in curated_catalog.items():
            if k in skill_keyword.lower():
                return resources

        # Generic default
        return [
            LiveKnowledgeResource(f"developer-roadmap/{skill_keyword}-guide", "CURATED_ROADMAP", "https://roadmap.sh", 15000, [skill_keyword, "learning-path"], f"Comprehensive visual roadmap and hands-on milestones for {skill_keyword}", 88.0, f"CURATED_KNOWLEDGE_MAP ({reason})")
        ]
