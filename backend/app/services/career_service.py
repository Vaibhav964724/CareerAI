import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.config import settings
from app.models.career import CareerRole, RoleRequirement
from app.models.student import Student, StudentSkillAssessment
from app.schemas.career import SkillGapItem, SkillGapAnalysisResponse, RoleComparisonResponse, RoleComparisonItem

def load_seed_roles() -> List[Dict[str, Any]]:
    """Load default career role profiles from local JSON file."""
    if not settings.CAREER_ROLES_FILE.exists():
        return []
    with open(settings.CAREER_ROLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def init_career_roles_db(db: Session) -> None:
    """Seed career roles in the database if empty."""
    existing_count = db.query(CareerRole).count()
    if existing_count > 0:
        return

    roles_data = load_seed_roles()
    for r_data in roles_data:
        role = CareerRole(
            slug=r_data["slug"],
            title=r_data["title"],
            description=r_data["description"],
            industry=r_data.get("industry", "Technology"),
            average_salary_range=r_data.get("average_salary_range"),
            job_outlook=r_data.get("job_outlook")
        )
        db.add(role)
        db.flush()

        for s in r_data.get("skills", []):
            req = RoleRequirement(
                role_id=role.id,
                skill_name=s["skill_name"],
                target_proficiency=s["target_proficiency"],
                importance=s.get("importance", "high"),
                prerequisites=json.dumps(s.get("prerequisites", [])),
                example_activities=json.dumps(s.get("example_activities", [])),
                suggested_projects=json.dumps(s.get("suggested_projects", []))
            )
            db.add(req)
    db.commit()

def get_all_roles(db: Session) -> List[CareerRole]:
    """Retrieve all available career roles."""
    init_career_roles_db(db)
    return db.query(CareerRole).all()

def get_role_by_slug_or_title(db: Session, identifier: str) -> Optional[CareerRole]:
    """Find role by slug or exact/case-insensitive title."""
    init_career_roles_db(db)
    clean_id = identifier.strip().lower()
    role = db.query(CareerRole).filter(
        (CareerRole.slug == clean_id) | 
        (CareerRole.title.ilike(clean_id))
    ).first()
    return role

def calculate_skill_gaps(db: Session, student_id: int, target_role_title: str) -> SkillGapAnalysisResponse:
    """
    Calculate deterministic skill gaps based on the 0-5 scale.
    Gap = max(0, Target - Current)
    Deterministic priority classification:
    - High: Gap >= 2 in critical skill OR Target >= 4 with Gap >= 2
    - Medium: Gap == 1 in critical skill OR Gap >= 2 in high/medium skill
    - Low: Gap == 1 in medium/low skill
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    role = get_role_by_slug_or_title(db, target_role_title)
    if not role:
        # Fallback to student's saved role or create dynamic role representation
        role = get_role_by_slug_or_title(db, student.target_role)
    
    if not role:
        raise ValueError(f"Target career role '{target_role_title}' is not configured.")

    # Build student skill lookup
    student_skills: Dict[str, int] = {
        s.skill_name.strip().lower(): s.proficiency 
        for s in student.skill_assessments
    }

    gaps: List[SkillGapItem] = []
    total_target_points = 0
    student_achieved_points = 0
    matched_skills = 0

    requirements = role.requirements
    for req in requirements:
        skill_key = req.skill_name.strip().lower()
        current_prof = student_skills.get(skill_key, 0)
        target_prof = req.target_proficiency
        gap_size = max(0, target_prof - current_prof)

        total_target_points += target_prof
        student_achieved_points += min(current_prof, target_prof)

        if gap_size == 0:
            matched_skills += 1

        # Classify priority
        if (gap_size >= 2 and req.importance == "critical") or (target_prof >= 4 and gap_size >= 2):
            priority = "High"
            reason = f"Essential core skill with a significant {gap_size}-level proficiency gap."
        elif (gap_size == 1 and req.importance == "critical") or (gap_size >= 2):
            priority = "Medium"
            reason = f"Important skill requiring moderate advancement ({gap_size} level needed)."
        else:
            priority = "Low"
            reason = f"Minor skill gap ({gap_size} level) or supplementary skill."

        # Parse activities & projects
        activities = json.loads(req.example_activities) if req.example_activities else []
        projects = json.loads(req.suggested_projects) if req.suggested_projects else []
        prereqs = json.loads(req.prerequisites) if req.prerequisites else []

        rec_activity = activities[0] if activities else f"Practice practical hands-on exercises in {req.skill_name}."
        rec_project = projects[0] if projects else f"Build a demonstration mini-project applying {req.skill_name}."

        gaps.append(SkillGapItem(
            skill_name=req.skill_name,
            current_proficiency=current_prof,
            target_proficiency=target_prof,
            gap=gap_size,
            priority=priority,
            importance=req.importance,
            reason=reason,
            recommended_activity=rec_activity,
            suggested_project=rec_project,
            prerequisites=prereqs
        ))

    # Sort gaps: High priority first, then Medium, then Low, then alphabetically
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    gaps.sort(key=lambda g: (priority_order.get(g.priority, 3), -g.gap, g.skill_name))

    match_pct = round((student_achieved_points / total_target_points * 100), 1) if total_target_points > 0 else 0.0

    summary_text = (
        f"{student.name} currently satisfies {match_pct}% of the core competency requirements "
        f"for {role.title}. Out of {len(requirements)} required skills, {matched_skills} meet or "
        f"exceed the target proficiency, leaving {len(requirements) - matched_skills} areas for focused improvement."
    )

    return SkillGapAnalysisResponse(
        student_id=student.id,
        target_role=role.title,
        overall_match_percentage=match_pct,
        total_skills_evaluated=len(requirements),
        matched_skills_count=matched_skills,
        gaps_count=len(requirements) - matched_skills,
        gaps=gaps,
        summary=summary_text
    )

def compare_roles(db: Session, current_role_name: str, new_role_name: str, student_skills_dict: Dict[str, int]) -> RoleComparisonResponse:
    """Compare skills between current role and a potential target role."""
    current_role = get_role_by_slug_or_title(db, current_role_name)
    new_role = get_role_by_slug_or_title(db, new_role_name)

    if not current_role or not new_role:
        raise ValueError("Both current role and target role must exist to perform comparison.")

    current_skills_map = {r.skill_name.strip().lower(): (r.skill_name, r.target_proficiency) for r in current_role.requirements}
    new_skills_map = {r.skill_name.strip().lower(): (r.skill_name, r.target_proficiency) for r in new_role.requirements}

    transferable = []
    new_skills = []
    table_items = []
    additional_effort_hours = 0

    all_keys = set(current_skills_map.keys()) | set(new_skills_map.keys())

    for k in sorted(all_keys):
        c_name, c_prof = current_skills_map.get(k, (None, 0))
        n_name, n_prof = new_skills_map.get(k, (None, 0))
        display_name = n_name if n_name else c_name
        stu_prof = student_skills_dict.get(k, 0)

        if k in current_skills_map and k in new_skills_map:
            transferable.append(display_name)
            if stu_prof >= n_prof:
                status = "sufficient"
            elif n_prof > c_prof:
                status = "gap_increased"
                additional_effort_hours += (n_prof - stu_prof) * 15
            else:
                status = "retained"
        elif k in new_skills_map:
            new_skills.append(display_name)
            status = "new_requirement"
            additional_effort_hours += max(0, n_prof - stu_prof) * 20
        else:
            status = "not_in_new_role"

        table_items.append(RoleComparisonItem(
            skill_name=display_name,
            current_role_proficiency=c_prof,
            new_role_proficiency=n_prof,
            student_proficiency=stu_prof,
            status=status
        ))

    # Feasibility evaluation
    new_skills_count = len(new_skills)
    if new_skills_count <= 1:
        feasibility = "Smooth"
        rec = f"Transitioning from {current_role.title} to {new_role.title} is highly feasible as most skills directly transfer."
    elif new_skills_count <= 3:
        feasibility = "Moderate"
        rec = f"Transition requires mastering {new_skills_count} new key skills. Your existing foundations provide a solid base."
    else:
        feasibility = "Challenging"
        rec = f"Significant curriculum shift required with {new_skills_count} new technical areas."

    additional_weeks = round(additional_effort_hours / 10.0, 1)

    return RoleComparisonResponse(
        current_role=current_role.title,
        new_role=new_role.title,
        transferable_skills=transferable,
        new_skills_needed=new_skills,
        comparison_table=table_items,
        transition_feasibility=feasibility,
        estimated_additional_weeks=additional_weeks,
        recommendation=rec
    )
