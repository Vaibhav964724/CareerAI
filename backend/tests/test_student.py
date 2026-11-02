import json
from app.models.student import Student, StudentSkillAssessment

def test_create_student_profile(db_session):
    student = Student(
        name="Aarav Sharma",
        email="aarav@university.edu",
        degree="B.Tech Computer Science",
        branch="Computer Science & Engineering",
        year_of_study=3,
        gpa=8.4,
        interests=json.dumps(["Machine Learning", "Data Analysis"]),
        existing_projects=json.dumps(["Library Management System"]),
        completed_certifications=json.dumps(["Intro to Python"]),
        target_role="Data Analyst",
        preferred_industry="Technology",
        weekly_hours=10.0,
        timeline_months=6
    )
    db_session.add(student)
    db_session.flush()

    skill1 = StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=2)
    skill2 = StudentSkillAssessment(student_id=student.id, skill_name="SQL", proficiency=2)
    db_session.add_all([skill1, skill2])
    db_session.commit()

    retrieved = db_session.query(Student).filter(Student.id == student.id).first()
    assert retrieved is not None
    assert retrieved.name == "Aarav Sharma"
    assert len(retrieved.skill_assessments) == 2
    assert retrieved.target_role == "Data Analyst"

def test_update_student_profile(db_session):
    student = Student(
        name="Priya Patel",
        degree="B.E. Information Technology",
        branch="IT",
        year_of_study=4,
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.commit()

    # Update hours to 5 and role to Data Scientist
    student.weekly_hours = 5.0
    student.target_role = "Data Scientist"
    db_session.commit()

    updated = db_session.query(Student).filter(Student.id == student.id).first()
    assert updated.weekly_hours == 5.0
    assert updated.target_role == "Data Scientist"
