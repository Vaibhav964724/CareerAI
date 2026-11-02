import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.student import Student, StudentSkillAssessment
from app.models.career import CareerRole, RoleRequirement
from app.models.roadmap import Roadmap, RoadmapMilestone, ProgressUpdate
from app.models.agent_log import AgentObservation, AgentActionLog
from app.services.career_service import (
    get_role_by_slug_or_title,
    calculate_skill_gaps as calc_gaps,
    compare_roles as comp_roles
)
from app.services.roadmap_service import (
    generate_roadmap as gen_roadmap,
    revise_roadmap as rev_roadmap,
    get_resources_for_skills,
    get_project_for_role_and_skills
)

# 1. get_student_profile
def get_student_profile(db: Session, student_id: int) -> Dict[str, Any]:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    skills = [
        {"skill_name": s.skill_name, "proficiency": s.proficiency}
        for s in student.skill_assessments
    ]

    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "degree": student.degree,
        "branch": student.branch,
        "year_of_study": student.year_of_study,
        "gpa": student.gpa,
        "interests": json.loads(student.interests) if student.interests else [],
        "existing_projects": json.loads(student.existing_projects) if student.existing_projects else [],
        "completed_certifications": json.loads(student.completed_certifications) if student.completed_certifications else [],
        "target_role": student.target_role,
        "preferred_industry": student.preferred_industry,
        "weekly_hours": student.weekly_hours,
        "timeline_months": student.timeline_months,
        "skills": skills,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "updated_at": student.updated_at.isoformat() if student.updated_at else None
    }

# 2. get_career_requirements
def get_career_requirements(db: Session, role_title_or_slug: str) -> Dict[str, Any]:
    role = get_role_by_slug_or_title(db, role_title_or_slug)
    if not role:
        raise ValueError(f"Career role '{role_title_or_slug}' not found.")

    reqs = []
    for r in role.requirements:
        reqs.append({
            "skill_name": r.skill_name,
            "target_proficiency": r.target_proficiency,
            "importance": r.importance,
            "prerequisites": json.loads(r.prerequisites) if r.prerequisites else [],
            "example_activities": json.loads(r.example_activities) if r.example_activities else [],
            "suggested_projects": json.loads(r.suggested_projects) if r.suggested_projects else []
        })

    return {
        "id": role.id,
        "slug": role.slug,
        "title": role.title,
        "description": role.description,
        "industry": role.industry,
        "average_salary_range": role.average_salary_range,
        "job_outlook": role.job_outlook,
        "skills": reqs
    }

# 3. analyze_skill_gaps
def analyze_skill_gaps(db: Session, student_id: int, target_role: str) -> Dict[str, Any]:
    res = calc_gaps(db, student_id, target_role)
    return res.model_dump()

# 4. generate_career_roadmap
def generate_career_roadmap(db: Session, student_id: int, target_role: str, weekly_hours: float) -> Dict[str, Any]:
    rm = gen_roadmap(db, student_id, target_role, weekly_hours)
    
    milestones_data = []
    for m in rm.milestones:
        milestones_data.append({
            "id": m.id,
            "title": m.title,
            "phase_number": m.phase_number,
            "phase_name": m.phase_name,
            "description": m.description,
            "required_skills": json.loads(m.required_skills) if m.required_skills else [],
            "priority": m.priority,
            "estimated_hours": m.estimated_hours,
            "estimated_weeks": m.estimated_weeks,
            "completion_criteria": m.completion_criteria,
            "deadline": m.deadline,
            "status": m.status
        })

    return {
        "id": rm.id,
        "student_id": rm.student_id,
        "target_role": rm.target_role,
        "total_estimated_weeks": rm.total_estimated_weeks,
        "weekly_hours": rm.weekly_hours,
        "status": rm.status,
        "version": rm.version,
        "milestones_count": len(milestones_data),
        "milestones": milestones_data
    }

# 5. recommend_learning_resources
def recommend_learning_resources(skills: List[str]) -> List[Dict[str, Any]]:
    return get_resources_for_skills(skills)

# 6. recommend_projects
def recommend_projects(skills: List[str], target_role: str) -> Optional[Dict[str, Any]]:
    return get_project_for_role_and_skills(target_role, skills)

# 7. update_milestone_progress
def update_milestone_progress(db: Session, milestone_id: int, new_status: str, notes: Optional[str] = None) -> Dict[str, Any]:
    milestone = db.query(RoadmapMilestone).filter(RoadmapMilestone.id == milestone_id).first()
    if not milestone:
        raise ValueError(f"Milestone {milestone_id} not found.")

    old_status = milestone.status
    milestone.status = new_status
    if new_status == "completed":
        milestone.completed_at = datetime.utcnow()
    elif old_status == "completed" and new_status != "completed":
        milestone.completed_at = None

    db.add(milestone)

    # Log ProgressUpdate
    prog = ProgressUpdate(
        student_id=milestone.roadmap.student_id,
        milestone_id=milestone.id,
        previous_status=old_status,
        new_status=new_status,
        notes=notes or f"Updated status to {new_status}"
    )
    db.add(prog)
    db.commit()
    db.refresh(milestone)

    return {
        "milestone_id": milestone.id,
        "title": milestone.title,
        "previous_status": old_status,
        "new_status": milestone.status,
        "completed_at": milestone.completed_at.isoformat() if milestone.completed_at else None
    }

# 8. detect_learning_delays
def detect_learning_delays(db: Session, student_id: int) -> List[Dict[str, Any]]:
    delays = []
    active_rm = db.query(Roadmap).filter(Roadmap.student_id == student_id, Roadmap.status == "active").first()
    if not active_rm:
        return delays

    for m in active_rm.milestones:
        # Check blocked items
        if m.status == "blocked":
            delays.append({
                "milestone_id": m.id,
                "title": m.title,
                "type": "blocked_milestone",
                "severity": "high",
                "message": f"Milestone '{m.title}' is currently marked as blocked."
            })
        
        # Check if milestone in progress has exceeded estimated weeks based on creation / progress update
        if m.status == "in_progress":
            latest_update = db.query(ProgressUpdate).filter(
                ProgressUpdate.milestone_id == m.id
            ).order_by(ProgressUpdate.timestamp.desc()).first()

            if latest_update:
                elapsed_days = (datetime.utcnow() - latest_update.timestamp).days
                max_allowed_days = max(14, int(m.estimated_weeks * 7) + 7)
                if elapsed_days > max_allowed_days:
                    delays.append({
                        "milestone_id": m.id,
                        "title": m.title,
                        "type": "overdue_progress",
                        "severity": "medium",
                        "message": f"Milestone '{m.title}' has been in progress for {elapsed_days} days without completion."
                    })
    return delays

# 9. revise_career_roadmap
def revise_career_roadmap(
    db: Session,
    student_id: int,
    trigger_reason: str,
    new_weekly_hours: Optional[float] = None,
    new_target_role: Optional[str] = None
) -> Dict[str, Any]:
    return rev_roadmap(db, student_id, trigger_reason, new_weekly_hours, new_target_role)

# 10. save_agent_observation
def save_agent_observation(db: Session, student_id: int, observation_type: str, summary: str, details: Dict[str, Any]) -> Dict[str, Any]:
    obs = AgentObservation(
        student_id=student_id,
        observation_type=observation_type,
        summary=summary,
        details=json.dumps(details)
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return {
        "id": obs.id,
        "student_id": obs.student_id,
        "observation_type": obs.observation_type,
        "summary": obs.summary,
        "created_at": obs.created_at.isoformat()
    }

# 11. compare_career_roles
def compare_career_roles(db: Session, current_role: str, new_role: str, student_skills: Dict[str, int]) -> Dict[str, Any]:
    res = comp_roles(db, current_role, new_role, student_skills)
    return res.model_dump()

# 12. evaluate_next_best_action
def evaluate_next_best_action(db: Session, student_id: int) -> Dict[str, Any]:
    active_rm = db.query(Roadmap).filter(Roadmap.student_id == student_id, Roadmap.status == "active").first()
    if not active_rm:
        student = db.query(Student).filter(Student.id == student_id).first()
        return {
            "student_id": student_id,
            "action_type": "generate_initial_roadmap",
            "title": "Generate Career Roadmap",
            "description": f"Generate your personalized milestone roadmap for {student.target_role if student else 'target role'}.",
            "reason": "No active roadmap found for student profile.",
            "priority": "high",
            "milestone_id": None
        }

    # Check for blocked milestones
    blocked = [m for m in active_rm.milestones if m.status == "blocked"]
    if blocked:
        return {
            "student_id": student_id,
            "action_type": "resolve_blocker",
            "title": f"Resolve Blocker on: {blocked[0].title}",
            "description": f"Milestone '{blocked[0].title}' is blocked. Review prerequisite concepts or consult learning materials.",
            "reason": "Blocked milestone prevents downstream progress.",
            "priority": "high",
            "milestone_id": blocked[0].id
        }

    # Check for in_progress milestone
    in_prog = [m for m in active_rm.milestones if m.status == "in_progress"]
    if in_prog:
        return {
            "student_id": student_id,
            "action_type": "continue_milestone",
            "title": f"Continue Working on: {in_prog[0].title}",
            "description": f"Current focus: {in_prog[0].description}",
            "reason": "Milestone is actively underway.",
            "priority": "high",
            "milestone_id": in_prog[0].id
        }

    # Check next not_started milestone
    not_started = [m for m in active_rm.milestones if m.status == "not_started"]
    if not_started:
        next_m = not_started[0]
        return {
            "student_id": student_id,
            "action_type": "start_milestone",
            "title": f"Start Milestone: {next_m.title}",
            "description": next_m.description,
            "reason": f"Next logical step in phase {next_m.phase_number} ({next_m.phase_name}).",
            "priority": "high",
            "milestone_id": next_m.id
        }

    return {
        "student_id": student_id,
        "action_type": "all_completed",
        "title": "All Milestones Completed!",
        "description": "You have accomplished all roadmap goals. Focus on mock interviews and active job applications.",
        "reason": "All milestones have been successfully completed.",
        "priority": "medium",
        "milestone_id": None
    }
