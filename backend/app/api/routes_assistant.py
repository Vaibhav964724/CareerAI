from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.models.roadmap import Roadmap
from app.schemas.agent import AssistantQueryRequest, AssistantQueryResponse
from app.agent.tools import get_student_profile, analyze_skill_gaps
from app.services.llm_service import generate_assistant_response

router = APIRouter(prefix="/assistant", tags=["Career Assistant"])

@router.post("/chat", response_model=AssistantQueryResponse)
def chat_with_assistant(payload: AssistantQueryRequest, db: Session = Depends(get_db)):
    """
    Context-aware interactive career guidance assistant.
    Retrieves the student's actual database profile, current roadmap, and evaluated gaps.
    """
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # 1. Retrieve full saved student profile
    profile = get_student_profile(db, student.id)

    # 2. Retrieve active roadmap if any
    active_rm = db.query(Roadmap).filter(
        Roadmap.student_id == student.id,
        Roadmap.status == "active"
    ).first()

    rm_dict = None
    if active_rm:
        rm_dict = {
            "id": active_rm.id,
            "target_role": active_rm.target_role,
            "weekly_hours": active_rm.weekly_hours,
            "total_estimated_weeks": active_rm.total_estimated_weeks,
            "milestones": [
                {
                    "id": m.id,
                    "title": m.title,
                    "phase_number": m.phase_number,
                    "phase_name": m.phase_name,
                    "description": m.description,
                    "estimated_weeks": m.estimated_weeks,
                    "estimated_hours": m.estimated_hours,
                    "completion_criteria": m.completion_criteria,
                    "status": m.status,
                    "recommended_project": m.recommended_project
                }
                for m in active_rm.milestones
            ]
        }

    # 3. Retrieve skill gaps
    gaps_list = []
    try:
        gap_res = analyze_skill_gaps(db, student.id, student.target_role)
        gaps_list = gap_res.get("gaps", [])
    except Exception:
        gaps_list = []

    # 4. Generate response
    reply, mode_used, context, suggested = generate_assistant_response(
        student_profile=profile,
        active_roadmap=rm_dict,
        skill_gaps=gaps_list,
        user_query=payload.message
    )

    return AssistantQueryResponse(
        student_id=student.id,
        reply=reply,
        mode=mode_used,
        relevant_context=context,
        suggested_questions=suggested
    )
