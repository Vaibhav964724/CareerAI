import os
from pathlib import Path
from dotenv import load_dotenv

# Locate base directory and load .env if present
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv(BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "CareerAI"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration (defaults to local SQLite, extensible to PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{ (BASE_DIR / 'careerai.db').as_posix() }")
    
    # LLM Service Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-3-5-sonnet-20241022")
    
    # Agent settings
    AGENT_MAX_ITERATIONS: int = int(os.getenv("AGENT_MAX_ITERATIONS", "5"))
    
    # CORS
    CORS_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()
    ] or [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Data paths
    DATA_DIR: Path = Path(__file__).resolve().parent / "data"
    CAREER_ROLES_FILE: Path = DATA_DIR / "career_roles.json"
    PROJECT_CATALOG_FILE: Path = DATA_DIR / "project_catalog.json"

settings = Settings()
