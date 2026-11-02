from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.api import api_router
from app.services.career_service import init_career_roles_db

# Create tables immediately on import
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Autonomous, Persistent, and Personalized AI Career Guidance Agent for College Students"
)

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        init_career_roles_db(db)
    finally:
        db.close()

# Enable CORS for React frontend development and Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "Welcome to CareerAI Autonomous Career Guidance Agent API",
        "version": settings.PROJECT_VERSION,
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
