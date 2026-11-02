from fastapi import APIRouter
from app.api.routes_student import router as student_router
from app.api.routes_career import router as career_router
from app.api.routes_roadmap import router as roadmap_router
from app.api.routes_agent import router as agent_router
from app.api.routes_assistant import router as assistant_router
from app.api.routes_assignments import router as assignments_router

api_router = APIRouter()

api_router.include_router(student_router)
api_router.include_router(career_router)
api_router.include_router(roadmap_router)
api_router.include_router(agent_router)
api_router.include_router(assistant_router)
api_router.include_router(assignments_router)

@api_router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "CareerAI Agent API",
        "version": "1.0.0"
    }
