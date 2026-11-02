import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    target_role = Column(String(120), nullable=False)
    total_estimated_weeks = Column(Float, default=12.0)
    weekly_hours = Column(Float, default=10.0)
    status = Column(String(30), default="active")   # active, archived, completed
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="roadmaps")
    milestones = relationship("RoadmapMilestone", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapMilestone.order_index")
    revisions = relationship("RoadmapRevisionHistory", back_populates="roadmap", cascade="all, delete-orphan")


class RoadmapMilestone(Base):
    __tablename__ = "roadmap_milestones"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(160), nullable=False)
    phase_number = Column(Integer, default=1)
    phase_name = Column(String(100), default="Foundation")
    description = Column(Text, nullable=False)
    required_skills = Column(Text, default="[]")           # JSON list of strings
    priority = Column(String(20), default="high")          # high, medium, low
    estimated_hours = Column(Float, default=20.0)
    estimated_weeks = Column(Float, default=2.0)
    prerequisites = Column(Text, default="[]")             # JSON list of prerequisite milestone titles
    learning_resources = Column(Text, default="[]")        # JSON list of resource objects {name, url, type, provider}
    recommended_project = Column(Text, default="{}")       # JSON object {title, description, deliverables}
    completion_criteria = Column(Text, nullable=False)
    deadline = Column(String(60), nullable=True)           # e.g., "Week 4" or ISO date string
    status = Column(String(30), default="not_started")     # not_started, in_progress, completed, blocked
    order_index = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)

    roadmap = relationship("Roadmap", back_populates="milestones")
    progress_updates = relationship("ProgressUpdate", back_populates="milestone", cascade="all, delete-orphan")


class ProgressUpdate(Base):
    __tablename__ = "progress_updates"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    milestone_id = Column(Integer, ForeignKey("roadmap_milestones.id", ondelete="CASCADE"), nullable=False)
    previous_status = Column(String(30), nullable=False)
    new_status = Column(String(30), nullable=False)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="progress_updates")
    milestone = relationship("RoadmapMilestone", back_populates="progress_updates")


class RoadmapRevisionHistory(Base):
    __tablename__ = "roadmap_revision_history"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    revision_trigger = Column(String(100), nullable=False) # e.g. "available_hours_change", "target_role_change", "milestone_delay"
    summary = Column(Text, nullable=False)
    changes_applied = Column(Text, default="{}")           # JSON summary of what changed
    preserved_milestones_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    roadmap = relationship("Roadmap", back_populates="revisions")
