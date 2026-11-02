import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AgentObservation(Base):
    __tablename__ = "agent_observations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    observation_type = Column(String(80), nullable=False) # e.g. "profile_evaluated", "hours_changed", "goal_changed", "milestone_completed", "delay_detected"
    summary = Column(Text, nullable=False)
    details = Column(Text, default="{}")                 # JSON string with metrics/data
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="agent_observations")


class AgentActionLog(Base):
    __tablename__ = "agent_action_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    action_name = Column(String(100), nullable=False)    # e.g. "analyze_skill_gaps", "generate_roadmap", "revise_roadmap"
    stage = Column(String(50), default="ACT")            # OBSERVE, REASON, PLAN, ACT, VERIFY, PERSIST, REPORT
    status = Column(String(30), default="success")       # success, warning, error, pending
    reason = Column(Text, nullable=True)                 # Why this action was triggered
    input_data = Column(Text, default="{}")              # JSON string of input parameters
    output_data = Column(Text, default="{}")             # JSON string of results
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="agent_actions")
