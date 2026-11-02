import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student, StudentSkillAssessment
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, SkillAssessmentItem

router = APIRouter(prefix="/students", tags=["Students"])

def student_to_response(student: Student) -> StudentResponse:
    skills = [
        SkillAssessmentItem(skill_name=s.skill_name, proficiency=s.proficiency)
        for s in student.skill_assessments
    ]
    return StudentResponse(
        id=student.id,
        name=student.name,
        email=student.email,
        degree=student.degree,
        branch=student.branch,
        year_of_study=student.year_of_study,
        gpa=student.gpa,
        interests=json.loads(student.interests) if student.interests else [],
        existing_projects=json.loads(student.existing_projects) if student.existing_projects else [],
        completed_certifications=json.loads(student.completed_certifications) if student.completed_certifications else [],
        target_role=student.target_role,
        preferred_industry=student.preferred_industry,
        weekly_hours=student.weekly_hours,
        timeline_months=student.timeline_months,
        skills=skills,
        created_at=student.created_at,
        updated_at=student.updated_at
    )

@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student academic profile and skill assessments."""
    student = Student(
        name=payload.name,
        email=payload.email,
        degree=payload.degree,
        branch=payload.branch,
        year_of_study=payload.year_of_study,
        gpa=payload.gpa,
        interests=json.dumps(payload.interests),
        existing_projects=json.dumps(payload.existing_projects),
        completed_certifications=json.dumps(payload.completed_certifications),
        target_role=payload.target_role,
        preferred_industry=payload.preferred_industry,
        weekly_hours=payload.weekly_hours,
        timeline_months=payload.timeline_months
    )
    db.add(student)
    db.flush()

    # Add skill assessments
    for s in payload.skills:
        assessment = StudentSkillAssessment(
            student_id=student.id,
            skill_name=s.skill_name,
            proficiency=s.proficiency
        )
        db.add(assessment)

    db.commit()
    db.refresh(student)
    return student_to_response(student)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Retrieve an existing student profile by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student_to_response(student)

@router.get("", response_model=List[StudentResponse])
def list_students(limit: int = 10, db: Session = Depends(get_db)):
    """List registered students."""
    students = db.query(Student).order_by(Student.id.desc()).limit(limit).all()
    return [student_to_response(s) for s in students]

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    """Update student profile details and proficiency scores."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    if payload.name is not None:
        student.name = payload.name
    if payload.email is not None:
        student.email = payload.email
    if payload.degree is not None:
        student.degree = payload.degree
    if payload.branch is not None:
        student.branch = payload.branch
    if payload.year_of_study is not None:
        student.year_of_study = payload.year_of_study
    if payload.gpa is not None:
        student.gpa = payload.gpa
    if payload.interests is not None:
        student.interests = json.dumps(payload.interests)
    if payload.existing_projects is not None:
        student.existing_projects = json.dumps(payload.existing_projects)
    if payload.completed_certifications is not None:
        student.completed_certifications = json.dumps(payload.completed_certifications)
    if payload.target_role is not None:
        student.target_role = payload.target_role
    if payload.preferred_industry is not None:
        student.preferred_industry = payload.preferred_industry
    if payload.weekly_hours is not None:
        student.weekly_hours = payload.weekly_hours
    if payload.timeline_months is not None:
        student.timeline_months = payload.timeline_months

    if payload.skills is not None:
        # Update or add skills
        existing_skills = {s.skill_name.lower(): s for s in student.skill_assessments}
        for s in payload.skills:
            key = s.skill_name.lower()
            if key in existing_skills:
                existing_skills[key].proficiency = s.proficiency
                db.add(existing_skills[key])
            else:
                new_skill = StudentSkillAssessment(
                    student_id=student.id,
                    skill_name=s.skill_name,
                    proficiency=s.proficiency
                )
                db.add(new_skill)

    db.commit()
    db.refresh(student)
    return student_to_response(student)
