import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CareerRole(Base):
    __tablename__ = "career_roles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(80), unique=True, index=True, nullable=False)
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    industry = Column(String(100), default="Technology")
    average_salary_range = Column(String(80), nullable=True)
    job_outlook = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    requirements = relationship("RoleRequirement", back_populates="role", cascade="all, delete-orphan")


class RoleRequirement(Base):
    __tablename__ = "role_requirements"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False, index=True)
    target_proficiency = Column(Integer, default=3) # 1 to 5
    importance = Column(String(30), default="high") # critical, high, medium, low
    prerequisites = Column(Text, default="[]")      # JSON list of prerequisite skill names
    example_activities = Column(Text, default="[]") # JSON list of activities
    suggested_projects = Column(Text, default="[]") # JSON list of suggested projects

    role = relationship("CareerRole", back_populates="requirements")
