import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.agent_log import AgentObservation, AgentActionLog

class AgentMemory:
    """Manages persistent SQLite memory for the CareerAI Agent."""

    def __init__(self, db: Session, student_id: int):
        self.db = db
        self.student_id = student_id

    def get_recent_observations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve the most recent observations for this student."""
        obs_records = self.db.query(AgentObservation).filter(
            AgentObservation.student_id == self.student_id
        ).order_by(AgentObservation.created_at.desc()).limit(limit).all()

        return [
            {
                "id": o.id,
                "observation_type": o.observation_type,
                "summary": o.summary,
                "details": json.loads(o.details) if o.details else {},
                "created_at": o.created_at.isoformat()
            }
            for o in reversed(obs_records)
        ]

    def log_observation(self, observation_type: str, summary: str, details: Optional[Dict[str, Any]] = None) -> AgentObservation:
        """Persist a new observation to the database."""
        obs = AgentObservation(
            student_id=self.student_id,
            observation_type=observation_type,
            summary=summary,
            details=json.dumps(details or {})
        )
        self.db.add(obs)
        self.db.commit()
        self.db.refresh(obs)
        return obs

    def log_action(
        self,
        action_name: str,
        stage: str = "ACT",
        status: str = "success",
        reason: Optional[str] = None,
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None
    ) -> AgentActionLog:
        """Persist an agent action log to the database."""
        log = AgentActionLog(
            student_id=self.student_id,
            action_name=action_name,
            stage=stage,
            status=status,
            reason=reason,
            input_data=json.dumps(input_data or {}),
            output_data=json.dumps(output_data or {})
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_action_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieve recent action logs."""
        logs = self.db.query(AgentActionLog).filter(
            AgentActionLog.student_id == self.student_id
        ).order_by(AgentActionLog.created_at.desc()).limit(limit).all()

        return [
            {
                "id": l.id,
                "action_name": l.action_name,
                "stage": l.stage,
                "status": l.status,
                "reason": l.reason,
                "input_data": json.loads(l.input_data) if l.input_data else {},
                "output_data": json.loads(l.output_data) if l.output_data else {},
                "created_at": l.created_at.isoformat()
            }
            for l in logs
        ]
