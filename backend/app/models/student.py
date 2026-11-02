import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=True)
    degree = Column(String(100), nullable=False)           # e.g., "B.Tech Computer Science"
    branch = Column(String(100), nullable=False)           # e.g., "Computer Science & Engineering"
    year_of_study = Column(Integer, default=3)             # 1, 2, 3, 4
    gpa = Column(Float, nullable=True)                     # e.g., 3.7 or 8.5
    interests = Column(Text, default="[]")                 # JSON string list of interests
    existing_projects = Column(Text, default="[]")         # JSON string list of completed projects
    completed_certifications = Column(Text, default="[]")  # JSON string list of certifications
    target_role = Column(String(100), nullable=False)      # e.g., "Data Analyst"
    preferred_industry = Column(String(100), default="Technology")
    weekly_hours = Column(Float, default=10.0)             # Available study hours per week
    timeline_months = Column(Integer, default=6)           # Desired goal timeline
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    skill_assessments = relationship("StudentSkillAssessment", back_populates="student", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="student", cascade="all, delete-orphan")
    agent_observations = relationship("AgentObservation", back_populates="student", cascade="all, delete-orphan")
    agent_actions = relationship("AgentActionLog", back_populates="student", cascade="all, delete-orphan")
    progress_updates = relationship("ProgressUpdate", back_populates="student", cascade="all, delete-orphan")


class StudentSkillAssessment(Base):
    __tablename__ = "student_skill_assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False, index=True)
    proficiency = Column(Integer, default=0) # 0 to 5 scale
    verified_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="skill_assessments")
