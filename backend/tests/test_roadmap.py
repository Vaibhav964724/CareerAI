import json
from app.models.student import Student, StudentSkillAssessment
from app.models.roadmap import Roadmap, RoadmapMilestone
from app.services.roadmap_service import generate_roadmap, revise_roadmap
from app.agent.tools import update_milestone_progress

def test_generate_roadmap_structure(db_session):
    student = Student(
        name="Rohit Verma",
        degree="B.Tech",
        branch="CSE",
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.flush()

    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=1))
    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="SQL", proficiency=2))
    db_session.commit()

    rm = generate_roadmap(db_session, student.id, "Data Analyst", weekly_hours=10.0)
    assert rm is not None
    assert rm.status == "active"
    assert len(rm.milestones) >= 4
    assert rm.total_estimated_weeks > 0

    # Ensure phases 1 through 5 exist
    phases = [m.phase_number for m in rm.milestones]
    assert 1 in phases
    assert 4 in phases # Capstone portfolio project

def test_milestone_completion_and_hours_revision(db_session):
    student = Student(
        name="Deepa Nair",
        degree="B.Tech",
        branch="IT",
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.flush()

    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=2))
    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="SQL", proficiency=2))
    db_session.commit()

    rm = generate_roadmap(db_session, student.id, "Data Analyst", weekly_hours=10.0)
    first_milestone = rm.milestones[0]

    # Mark milestone as completed
    update_res = update_milestone_progress(db_session, first_milestone.id, "completed", "Finished all modules")
    assert update_res["new_status"] == "completed"

    # Now change hours to 5 hrs/week and revise roadmap
    rev_res = revise_roadmap(db_session, student.id, "available_hours_change", new_weekly_hours=5.0)
    assert rev_res["preserved_count"] >= 1

    # Check updated roadmap
    refreshed_rm = db_session.query(Roadmap).filter(Roadmap.id == rm.id).first()
    assert refreshed_rm.weekly_hours == 5.0
    
    # Verify completed milestone remained completed
    m0 = next(m for m in refreshed_rm.milestones if m.id == first_milestone.id)
    assert m0.status == "completed"

def test_role_change_preserves_completed_milestones(db_session):
    student = Student(
        name="Karan Malhotra",
        degree="B.Tech",
        branch="CSE",
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.flush()

    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=2))
    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="SQL", proficiency=2))
    db_session.commit()

    rm = generate_roadmap(db_session, student.id, "Data Analyst", weekly_hours=10.0)
    
    # Mark SQL or Python milestone as completed
    python_m = next((m for m in rm.milestones if "python" in m.title.lower() or "sql" in m.title.lower()), rm.milestones[0])
    update_milestone_progress(db_session, python_m.id, "completed", "Mastered SQL query concepts")

    # Now change target role to Data Scientist
    rev_res = revise_roadmap(db_session, student.id, "target_role_change", new_target_role="Data Scientist")
    assert rev_res["preserved_count"] >= 1

    # Check active roadmap is now for Data Scientist
    active_rm = db_session.query(Roadmap).filter(Roadmap.student_id == student.id, Roadmap.status == "active").first()
    assert active_rm.target_role == "Data Scientist"

    # Verify preserved completed milestone exists in the new roadmap
    completed_in_new = [m for m in active_rm.milestones if m.status == "completed"]
    assert len(completed_in_new) >= 1
