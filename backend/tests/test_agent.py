import json
from app.models.student import Student, StudentSkillAssessment
from app.models.agent_log import AgentObservation, AgentActionLog
from app.agent.controller import AgentController
from app.agent.tools import evaluate_next_best_action

def test_agent_controller_full_cycle(db_session):
    student = Student(
        name="Sneha Roy",
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

    controller = AgentController(db_session, student.id)
    state = controller.run_evaluation_cycle(trigger="initial_onboarding")

    assert state.cycle_status == "completed"
    assert len(state.actions_taken) >= 1
    assert state.verification_passed is True
    assert "Why CareerAI Recommended This" in state.report_summary

    # Verify persistent memory logged to SQLite
    obs_count = db_session.query(AgentObservation).filter(AgentObservation.student_id == student.id).count()
    assert obs_count >= 1

    actions_count = db_session.query(AgentActionLog).filter(AgentActionLog.student_id == student.id).count()
    assert actions_count >= 1

def test_agent_detects_hours_change_and_adapts(db_session):
    student = Student(
        name="Manish Gupta",
        degree="B.Tech",
        branch="IT",
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.flush()
    db_session.add(StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=2))
    db_session.commit()

    # Run initial cycle to generate roadmap
    controller = AgentController(db_session, student.id)
    controller.run_evaluation_cycle(trigger="initial_setup")

    # Now simulate student modifying their available hours to 5 hrs/week
    student.weekly_hours = 5.0
    db_session.add(student)
    db_session.commit()

    # Trigger second evaluation cycle
    state2 = controller.run_evaluation_cycle(trigger="student_hours_updated")
    assert state2.has_hours_mismatch is True
    assert any("Available study time changed" in change for change in state2.detected_changes)
    assert any("revise_roadmap_hours" in str(a) for a in state2.actions_taken)

def test_evaluate_next_best_action(db_session):
    student = Student(
        name="Rahul Joshi",
        degree="B.Tech",
        branch="CSE",
        target_role="Data Analyst",
        weekly_hours=10.0
    )
    db_session.add(student)
    db_session.commit()

    # Before roadmap exists, recommended action should be generating roadmap
    action = evaluate_next_best_action(db_session, student.id)
    assert action["action_type"] == "generate_initial_roadmap"
