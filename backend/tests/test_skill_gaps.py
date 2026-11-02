import json
from app.models.student import Student, StudentSkillAssessment
from app.services.career_service import calculate_skill_gaps, compare_roles

def test_skill_gap_calculation_deterministic(db_session):
    student = Student(
        name="Vikram Rao",
        degree="B.Tech",
        branch="CSE",
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.flush()

    # Enter Python proficiency 2 and SQL proficiency 2
    # In Data Analyst role: SQL target is 4, Python target is 3
    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=2))
    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="SQL", proficiency=2))
    db_session.commit()

    result = calculate_skill_gaps(db_session, student.id, "Data Analyst")
    assert result.target_role == "Data Analyst"
    assert result.total_skills_evaluated >= 5
    
    # Check SQL gap: target 4 - current 2 = 2 gap
    sql_gap = next((g for g in result.gaps if g.skill_name.lower() == "sql"), None)
    assert sql_gap is not None
    assert sql_gap.target_proficiency == 4
    assert sql_gap.current_proficiency == 2
    assert sql_gap.gap == 2
    assert sql_gap.priority == "High"

    # Check Python gap: target 3 - current 2 = 1 gap
    python_gap = next((g for g in result.gaps if g.skill_name.lower() == "python"), None)
    assert python_gap is not None
    assert python_gap.target_proficiency == 3
    assert python_gap.current_proficiency == 2
    assert python_gap.gap == 1

def test_skill_gap_when_exceeding_target(db_session):
    student = Student(
        name="Ananya Sen",
        degree="B.Tech",
        branch="AI/DS",
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.flush()

    # If student has Python 5 (target is 3), gap must be exactly 0 (max(0, 3 - 5) = 0)
    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=5))
    db_session.commit()

    result = calculate_skill_gaps(db_session, student.id, "Data Analyst")
    python_gap = next(g for g in result.gaps if g.skill_name.lower() == "python")
    assert python_gap.gap == 0

def test_compare_career_roles(db_session):
    student_skills = {"python": 3, "sql": 4}
    res = compare_roles(db_session, "Data Analyst", "Data Scientist", student_skills)
    assert res.current_role == "Data Analyst"
    assert res.new_role == "Data Scientist"
    assert "Python" in res.transferable_skills or "python" in [s.lower() for s in res.transferable_skills]
    assert len(res.comparison_table) > 0
