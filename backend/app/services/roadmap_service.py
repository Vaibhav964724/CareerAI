import json
import math
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.config import settings
from app.models.student import Student, StudentSkillAssessment
from app.models.career import CareerRole
from app.models.roadmap import Roadmap, RoadmapMilestone, ProgressUpdate, RoadmapRevisionHistory
from app.services.career_service import get_role_by_slug_or_title, calculate_skill_gaps

VERIFIED_LEARNING_RESOURCES = {
    "sql": [
        {"name": "PostgreSQL Official Tutorial", "url": "https://www.postgresqltutorial.com/", "type": "interactive", "provider": "PostgreSQL Tutorial"},
        {"name": "SQLBolt Interactive Lessons", "url": "https://sqlbolt.com/", "type": "interactive", "provider": "SQLBolt"}
    ],
    "python": [
        {"name": "Official Python 3 Documentation", "url": "https://docs.python.org/3/tutorial/", "type": "documentation", "provider": "Python Software Foundation"},
        {"name": "Real Python Tutorials & Guides", "url": "https://realpython.com/", "type": "tutorial", "provider": "Real Python"}
    ],
    "data visualization & bi": [
        {"name": "Seaborn Statistical Data Visualization", "url": "https://seaborn.pydata.org/", "type": "documentation", "provider": "PyData"},
        {"name": "Microsoft Power BI Guided Learning", "url": "https://learn.microsoft.com/en-us/power-bi/guidance/", "type": "course", "provider": "Microsoft Learn"}
    ],
    "machine learning": [
        {"name": "Scikit-Learn User Guide & API", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "documentation", "provider": "Scikit-Learn"},
        {"name": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "type": "course", "provider": "Google Developers"}
    ],
    "deep learning": [
        {"name": "PyTorch Official Deep Learning Tutorials", "url": "https://pytorch.org/tutorials/", "type": "tutorial", "provider": "PyTorch Foundation"},
        {"name": "Deep Learning Specialization Notes", "url": "https://www.deeplearning.ai/", "type": "course", "provider": "DeepLearning.AI"}
    ],
    "data structures & algorithms": [
        {"name": "Open Data Structures", "url": "https://opendatastructures.org/", "type": "documentation", "provider": "Open Data Structures"},
        {"name": "GeeksforGeeks DSA Guide", "url": "https://www.geeksforgeeks.org/data-structures/", "type": "tutorial", "provider": "GeeksforGeeks"}
    ],
    "javascript / typescript": [
        {"name": "MDN Web Docs: JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "type": "documentation", "provider": "Mozilla MDN"},
        {"name": "TypeScript Official Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "documentation", "provider": "Microsoft"}
    ],
    "backend development (node/fastapi/express)": [
        {"name": "FastAPI Official Documentation", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "documentation", "provider": "FastAPI Tiangolo"},
        {"name": "MDN Express Web Framework Guide", "url": "https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs", "type": "tutorial", "provider": "Mozilla MDN"}
    ],
    "cloud platforms (aws / azure / gcp)": [
        {"name": "AWS Skill Builder Cloud Essentials", "url": "https://explore.skillbuilder.aws/", "type": "course", "provider": "Amazon Web Services"},
        {"name": "Google Cloud Training Free Tier", "url": "https://cloud.google.com/training", "type": "tutorial", "provider": "Google Cloud"}
    ],
    "network fundamentals & protocols": [
        {"name": "Wireshark User Guide", "url": "https://www.wireshark.org/docs/wsug_html_chunked/", "type": "documentation", "provider": "Wireshark Foundation"},
        {"name": "NIST Computer Security Resource Center", "url": "https://csrc.nist.gov/", "type": "documentation", "provider": "NIST"}
    ]
}

def load_project_catalog() -> List[Dict[str, Any]]:
    if not settings.PROJECT_CATALOG_FILE.exists():
        return []
    with open(settings.PROJECT_CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_resources_for_skills(skills: List[str]) -> List[Dict[str, Any]]:
    resources = []
    seen_urls = set()
    for s in skills:
        key = s.strip().lower()
        matched = VERIFIED_LEARNING_RESOURCES.get(key, [])
        for r in matched:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                resources.append(r)
    if not resources:
        # Default verified general software documentation
        resources.append({
            "name": "Mozilla Developer Network (MDN)",
            "url": "https://developer.mozilla.org/",
            "type": "documentation",
            "provider": "MDN Web Docs"
        })
    return resources

def get_project_for_role_and_skills(role_title: str, skills: List[str]) -> Optional[Dict[str, Any]]:
    catalog = load_project_catalog()
    clean_role = role_title.strip().lower()
    
    # Priority 1: Match role and skills
    for proj in catalog:
        matching_roles = [r.lower() for r in proj.get("target_roles", [])]
        if clean_role in matching_roles:
            return proj
    
    # Priority 2: Return first catalog item
    if catalog:
        return catalog[0]
    return None

def generate_roadmap(db: Session, student_id: int, target_role_title: str, weekly_hours: float) -> Roadmap:
    """Generate a clean, phased, personalized career roadmap for a student."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError(f"Student {student_id} not found.")

    role = get_role_by_slug_or_title(db, target_role_title)
    if not role:
        raise ValueError(f"Role '{target_role_title}' not found.")

    # Check for existing active roadmap; archive if generating a brand new one
    active_rm = db.query(Roadmap).filter(Roadmap.student_id == student_id, Roadmap.status == "active").first()
    version = 1
    if active_rm:
        version = active_rm.version + 1
        active_rm.status = "archived"
        db.add(active_rm)
        db.flush()

    gap_analysis = calculate_skill_gaps(db, student_id, role.title)
    gaps = gap_analysis.gaps

    # Group skills by phase based on prerequisites and priority
    # Phase 1: High priority prerequisites & fundamental gaps
    # Phase 2: Core role technical skills
    # Phase 3: Advanced techniques and statistical / architectural refinement
    # Phase 4: Capstone Industry Portfolio Project
    # Phase 5: Interview Prep & Mock Evaluations

    new_roadmap = Roadmap(
        student_id=student.id,
        target_role=role.title,
        weekly_hours=weekly_hours if weekly_hours > 0 else 10.0,
        status="active",
        version=version,
        total_estimated_weeks=0.0
    )
    db.add(new_roadmap)
    db.flush()

    milestones: List[RoadmapMilestone] = []
    order_idx = 0
    total_hours = 0.0

    # Categorize skills into phase groups
    foundation_skills = [g for g in gaps if len(g.prerequisites) == 0 and g.priority in ["High", "Medium"]]
    core_skills = [g for g in gaps if g not in foundation_skills and g.priority in ["High", "Medium"]]
    supplementary_skills = [g for g in gaps if g.priority == "Low"]

    # 1. Foundation Milestones
    for g in foundation_skills:
        hours = max(10, g.gap * 8)
        weeks = max(1.0, round(hours / weekly_hours, 1))
        total_hours += hours
        order_idx += 1
        status = "completed" if g.gap == 0 else "not_started"
        
        milestone = RoadmapMilestone(
            roadmap_id=new_roadmap.id,
            title=f"Master {g.skill_name} Foundations",
            phase_number=1,
            phase_name="Foundational Skills",
            description=f"Develop solid fundamentals in {g.skill_name} to bridge existing proficiency ({g.current_proficiency}/5) to target ({g.target_proficiency}/5).",
            required_skills=json.dumps([g.skill_name]),
            priority=g.priority.lower(),
            estimated_hours=float(hours),
            estimated_weeks=float(weeks),
            prerequisites=json.dumps([]),
            learning_resources=json.dumps(get_resources_for_skills([g.skill_name])),
            recommended_project=json.dumps({
                "title": f"Introductory {g.skill_name} Practical Workbook",
                "description": g.recommended_activity,
                "deliverables": [f"Completed exercise notebook or script repository for {g.skill_name}"]
            }),
            completion_criteria=f"Achieve level {g.target_proficiency} in {g.skill_name} and complete core exercises.",
            deadline=f"Week {round(total_hours / weekly_hours)}",
            status=status,
            order_index=order_idx,
            completed_at=datetime.utcnow() if status == "completed" else None
        )
        milestones.append(milestone)

    # 2. Core Role Milestones
    for g in core_skills:
        hours = max(15, g.gap * 10)
        weeks = max(1.0, round(hours / weekly_hours, 1))
        total_hours += hours
        order_idx += 1
        status = "completed" if g.gap == 0 else "not_started"

        milestone = RoadmapMilestone(
            roadmap_id=new_roadmap.id,
            title=f"Core Competency: {g.skill_name}",
            phase_number=2,
            phase_name="Core Role Competencies",
            description=f"Deep-dive into practical industry applications of {g.skill_name}. Bridge {g.gap}-level gap.",
            required_skills=json.dumps([g.skill_name]),
            priority=g.priority.lower(),
            estimated_hours=float(hours),
            estimated_weeks=float(weeks),
            prerequisites=json.dumps(g.prerequisites),
            learning_resources=json.dumps(get_resources_for_skills([g.skill_name])),
            recommended_project=json.dumps({
                "title": f"Applied {g.skill_name} Domain Mini-Project",
                "description": g.recommended_activity,
                "deliverables": [f"Functional project implementation with code documentation"]
            }),
            completion_criteria=f"Demonstrate proficient implementation matching {g.skill_name} target.",
            deadline=f"Week {round(total_hours / weekly_hours)}",
            status=status,
            order_index=order_idx,
            completed_at=datetime.utcnow() if status == "completed" else None
        )
        milestones.append(milestone)

    # 3. Supplementary Milestones
    if supplementary_skills:
        supp_names = [s.skill_name for s in supplementary_skills]
        hours = 20.0
        weeks = max(1.0, round(hours / weekly_hours, 1))
        total_hours += hours
        order_idx += 1
        all_done = all(s.gap == 0 for s in supplementary_skills)
        status = "completed" if all_done else "not_started"

        milestone = RoadmapMilestone(
            roadmap_id=new_roadmap.id,
            title="Supplementary Skills & Tooling Polish",
            phase_number=3,
            phase_name="Tooling & Refinement",
            description=f"Refine supporting proficiencies: {', '.join(supp_names)}.",
            required_skills=json.dumps(supp_names),
            priority="low",
            estimated_hours=hours,
            estimated_weeks=weeks,
            prerequisites=json.dumps([]),
            learning_resources=json.dumps(get_resources_for_skills(supp_names)),
            recommended_project=json.dumps({
                "title": "Supporting Toolchain Integration Practice",
                "description": "Integrate supporting tools into automated workflow.",
                "deliverables": ["Documented workflow and configuration setup"]
            }),
            completion_criteria="Complete practical verification checklist for supplementary skills.",
            deadline=f"Week {round(total_hours / weekly_hours)}",
            status=status,
            order_index=order_idx,
            completed_at=datetime.utcnow() if status == "completed" else None
        )
        milestones.append(milestone)

    # 4. Capstone Portfolio Project Milestone
    capstone_project = get_project_for_role_and_skills(role.title, [g.skill_name for g in gaps])
    cap_hours = float(capstone_project.get("estimated_hours", 25)) if capstone_project else 25.0
    cap_weeks = max(1.0, round(cap_hours / weekly_hours, 1))
    total_hours += cap_hours
    order_idx += 1

    milestones.append(RoadmapMilestone(
        roadmap_id=new_roadmap.id,
        title=f"Capstone Portfolio Project: {capstone_project.get('title', 'End-to-End Industry Project') if capstone_project else 'Industry Capstone'}",
        phase_number=4,
        phase_name="Portfolio Capstone",
        description=capstone_project.get("description", f"Build an end-to-end portfolio project validating your skills for {role.title}.") if capstone_project else "Build an end-to-end portfolio project.",
        required_skills=json.dumps(capstone_project.get("primary_skills", [g.skill_name for g in gaps[:3]])) if capstone_project else json.dumps([]),
        priority="high",
        estimated_hours=cap_hours,
        estimated_weeks=cap_weeks,
        prerequisites=json.dumps([m.title for m in milestones if m.phase_number in [1, 2]]),
        learning_resources=json.dumps(get_resources_for_skills([g.skill_name for g in gaps[:3]])),
        recommended_project=json.dumps(capstone_project or {}),
        completion_criteria="Deploy working codebase to GitHub with complete documentation, architecture diagram, and README.",
        deadline=f"Week {round(total_hours / weekly_hours)}",
        status="not_started",
        order_index=order_idx
    ))

    # 5. Career & Interview Readiness
    readiness_hours = 15.0
    readiness_weeks = max(1.0, round(readiness_hours / weekly_hours, 1))
    total_hours += readiness_hours
    order_idx += 1

    milestones.append(RoadmapMilestone(
        roadmap_id=new_roadmap.id,
        title=f"Interview Preparation & Resume Alignment for {role.title}",
        phase_number=5,
        phase_name="Career Readiness",
        description=f"Curate your GitHub portfolio, practice technical domain interview problems, and align resume bullets for {role.title}.",
        required_skills=json.dumps([g.skill_name for g in gaps[:4]]),
        priority="high",
        estimated_hours=readiness_hours,
        estimated_weeks=readiness_weeks,
        prerequisites=json.dumps([milestones[-1].title]),
        learning_resources=json.dumps([{
            "name": "Tech Interview Handbook",
            "url": "https://www.techinterviewhandbook.org/",
            "type": "guide",
            "provider": "Tech Interview Handbook"
        }]),
        recommended_project=json.dumps({
            "title": "Professional Portfolio Site & Case Study Presentations",
            "description": "Publish live demos and write 2 technical case study articles.",
            "deliverables": ["Live GitHub portfolio repo", "Case study documentation"]
        }),
        completion_criteria="Conduct 3 mock technical interviews and finalize targeted resume.",
        deadline=f"Week {round(total_hours / weekly_hours)}",
        status="not_started",
        order_index=order_idx
    ))

    # Add all milestones
    for m in milestones:
        db.add(m)

    new_roadmap.total_estimated_weeks = round(total_hours / weekly_hours, 1)
    db.commit()
    db.refresh(new_roadmap)
    return new_roadmap

def revise_roadmap(
    db: Session,
    student_id: int,
    trigger_reason: str,
    new_weekly_hours: Optional[float] = None,
    new_target_role: Optional[str] = None
) -> Dict[str, Any]:
    """
    Revise an existing roadmap while strictly PRESERVING all completed milestones!
    - If new_weekly_hours is provided: re-estimates remaining milestones' duration and deadlines.
    - If new_target_role is provided: preserves completed milestones matching skills, adds new ones.
    """
    active_rm = db.query(Roadmap).filter(
        Roadmap.student_id == student_id,
        Roadmap.status == "active"
    ).first()

    if not active_rm:
        # If no active roadmap, generate an initial one
        student = db.query(Student).filter(Student.id == student_id).first()
        target = new_target_role or (student.target_role if student else "Data Analyst")
        hours = new_weekly_hours or (student.weekly_hours if student else 10.0)
        rm = generate_roadmap(db, student_id, target, hours)
        return {
            "roadmap_id": rm.id,
            "revision_trigger": trigger_reason,
            "preserved_count": 0,
            "summary": "Initial roadmap generated.",
            "changes": {"action": "initial_generation", "target_role": target, "weekly_hours": hours}
        }

    # Extract currently completed milestones
    completed_milestones = [m for m in active_rm.milestones if m.status == "completed"]
    preserved_count = len(completed_milestones)

    changes_applied = {}
    summary_parts = []

    # Case A: Weekly study hours changed
    if new_weekly_hours and new_weekly_hours != active_rm.weekly_hours:
        old_hours = active_rm.weekly_hours
        active_rm.weekly_hours = new_weekly_hours
        changes_applied["weekly_hours"] = {"old": old_hours, "new": new_weekly_hours}
        summary_parts.append(f"Adjusted weekly study hours from {old_hours} hrs/wk to {new_weekly_hours} hrs/wk.")

        cumulative_hours = 0.0
        for m in active_rm.milestones:
            if m.status != "completed":
                # Recalculate estimated weeks for remaining milestones
                m.estimated_weeks = max(1.0, round(m.estimated_hours / new_weekly_hours, 1))
            cumulative_hours += m.estimated_hours
            m.deadline = f"Week {max(1, round(cumulative_hours / new_weekly_hours))}"
            db.add(m)

        active_rm.total_estimated_weeks = round(cumulative_hours / new_weekly_hours, 1)
        summary_parts.append(f"Roadmap completion timeline revised to {active_rm.total_estimated_weeks} weeks.")

    # Case B: Target career goal changed
    if new_target_role and new_target_role.strip().lower() != active_rm.target_role.strip().lower():
        old_role = active_rm.target_role
        changes_applied["target_role"] = {"old": old_role, "new": new_target_role}
        summary_parts.append(f"Transitioned target career path from {old_role} to {new_target_role}.")

        # Generate a new roadmap for the new role, but copy completed statuses for transferable skills
        student = db.query(Student).filter(Student.id == student_id).first()
        student.target_role = new_target_role
        db.add(student)
        db.flush()

        # Archive old roadmap
        active_rm.status = "archived"
        db.add(active_rm)
        db.flush()

        # Generate new roadmap
        new_rm = generate_roadmap(db, student_id, new_target_role, active_rm.weekly_hours)

        # Transfer completed milestones: check skills overlap
        completed_skills = set()
        for cm in completed_milestones:
            skills = json.loads(cm.required_skills) if cm.required_skills else []
            for s in skills:
                completed_skills.add(s.strip().lower())

        transferred_count = 0
        for nm in new_rm.milestones:
            nm_skills = json.loads(nm.required_skills) if nm.required_skills else []
            if any(s.strip().lower() in completed_skills for s in nm_skills):
                nm.status = "completed"
                nm.completed_at = datetime.utcnow()
                db.add(nm)
                transferred_count += 1

        db.commit()
        db.refresh(new_rm)

        active_rm = new_rm
        preserved_count = transferred_count
        summary_parts.append(f"Successfully preserved {transferred_count} completed milestones matching the new role.")

    # Record revision history
    active_rm.version += 1
    db.add(active_rm)

    revision_summary = " ".join(summary_parts) if summary_parts else f"Roadmap refreshed based on {trigger_reason}."
    rev_history = RoadmapRevisionHistory(
        roadmap_id=active_rm.id,
        student_id=student_id,
        revision_trigger=trigger_reason,
        summary=revision_summary,
        changes_applied=json.dumps(changes_applied),
        preserved_milestones_count=preserved_count
    )
    db.add(rev_history)
    db.commit()

    return {
        "roadmap_id": active_rm.id,
        "revision_trigger": trigger_reason,
        "preserved_count": preserved_count,
        "summary": revision_summary,
        "changes": changes_applied
    }
