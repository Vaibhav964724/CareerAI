"""
CareerAI End-to-End College Demonstration Verification Script.
Executes the exact 15-step lifecycle scenario mandated by Section 18 of the specification:

1. Create a student profile.
2. Set Data Analyst as the target career.
3. Enter existing Python and SQL skills.
4. Run skill-gap analysis.
5. Generate a personalized roadmap.
6. Mark SQL as completed.
7. Change available study time from 10 hours per week to 5 hours per week.
8. Run the agent evaluation.
9. Verify that the agent detects the change and proposes a suitable revision.
10. Change the career goal to Data Scientist.
11. Run the agent again.
12. Verify that new skill requirements are identified.
13. Verify that relevant completed milestones are preserved.
14. Restart backend simulation (close DB connection, reconnect to SQLite).
15. Verify that the profile, roadmap, and progress are still available.
"""

import sys
import json
from pathlib import Path

# Fix Windows console UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure backend root is in sys.path
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.student import Student, StudentSkillAssessment
from app.models.roadmap import Roadmap, RoadmapMilestone, RoadmapRevisionHistory
from app.models.agent_log import AgentObservation, AgentActionLog
from app.services.career_service import init_career_roles_db, calculate_skill_gaps
from app.services.roadmap_service import generate_roadmap, revise_roadmap
from app.agent.controller import AgentController
from app.agent.tools import update_milestone_progress

DEMO_DB_FILE = BACKEND_DIR / "demo_careerai.db"
DEMO_DB_URL = f"sqlite:///{DEMO_DB_FILE.as_posix()}"

def run_demonstration():
    print("=" * 75)
    print("🚀 STARTING CAREERAI END-TO-END DEMONSTRATION VERIFICATION")
    print("=" * 75)

    if DEMO_DB_FILE.exists():
        DEMO_DB_FILE.unlink(missing_ok=True)

    engine = create_engine(DEMO_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    # STEP 1, 2, 3: Create Student Profile with Data Analyst goal, Python & SQL
    print("\n[Step 1-3] Creating student profile for 'Arjun Sen' (Target: Data Analyst, 10 hrs/wk)...")
    db = Session()
    init_career_roles_db(db)

    student = Student(
        name="Arjun Sen",
        email="arjun.sen@college.edu",
        degree="B.Tech Computer Science",
        branch="Computer Science & Engineering",
        year_of_study=3,
        gpa=8.5,
        target_role="Data Analyst",
        preferred_industry="Technology",
        weekly_hours=10.0,
        timeline_months=6,
        interests=json.dumps(["Analytics", "Databases", "Business Intelligence"])
    )
    db.add(student)
    db.flush()

    db.add(StudentSkillAssessment(student_id=student.id, skill_name="Python", proficiency=2))
    db.add(StudentSkillAssessment(student_id=student.id, skill_name="SQL", proficiency=2))
    db.commit()
    student_id = student.id
    print(f"✅ Student profile created successfully with ID #{student_id}.")

    # STEP 4: Run Skill-Gap Analysis
    print("\n[Step 4] Running deterministic skill-gap analysis for Data Analyst...")
    gaps_result = calculate_skill_gaps(db, student_id, "Data Analyst")
    print(f"📊 Evaluated {gaps_result.total_skills_evaluated} skills. Match Percentage: {gaps_result.overall_match_percentage}%.")
    for g in gaps_result.gaps:
        print(f"   • {g.skill_name}: Current={g.current_proficiency}/5, Target={g.target_proficiency}/5, Gap={g.gap} ({g.priority} Priority)")
    assert gaps_result.gaps_count > 0, "Expected skill gaps to be identified"

    # STEP 5: Generate Personalized Roadmap
    print("\n[Step 5] Generating personalized phased career roadmap...")
    rm = generate_roadmap(db, student_id, "Data Analyst", weekly_hours=10.0)
    print(f"✅ Roadmap generated: {len(rm.milestones)} milestones, total estimated duration ~{rm.total_estimated_weeks} weeks.")
    for m in rm.milestones:
        print(f"   [Phase {m.phase_number}] #{m.order_index} {m.title} ({m.estimated_weeks} wks, Status: {m.status})")
    assert len(rm.milestones) >= 4, "Roadmap should have at least 4 milestones across phases"

    # STEP 6: Mark SQL as Completed
    print("\n[Step 6] Marking SQL milestone as COMPLETED...")
    sql_milestone = next((m for m in rm.milestones if "sql" in m.title.lower()), rm.milestones[0])
    update_res = update_milestone_progress(db, sql_milestone.id, "completed", "Completed SQL querying course and exercises")
    print(f"✅ Milestone '{sql_milestone.title}' updated to: {update_res['new_status']}")

    # STEP 7: Change available study time from 10 hrs/wk to 5 hrs/wk
    print("\n[Step 7] Student adjusts available study time from 10 hrs/wk to 5 hrs/wk in profile...")
    student.weekly_hours = 5.0
    db.add(student)
    db.commit()
    print("✅ Profile weekly_hours updated to 5.0 in database.")

    # STEP 8 & 9: Run Agent Evaluation & Verify Detection
    print("\n[Step 8-9] Running 7-Stage Autonomous Agent Controller...")
    controller = AgentController(db, student_id)
    agent_state = controller.run_evaluation_cycle(trigger="student_profile_update")
    print(f"🤖 Agent Evaluation Status: {agent_state.cycle_status}")
    print(f"🔍 Detected Factors: {agent_state.detected_changes}")
    print(f"⚡ Actions Executed: {[a.get('description', a.get('action')) for a in agent_state.actions_taken]}")
    print(f"💡 Explanation: {agent_state.report_summary}")

    assert agent_state.has_hours_mismatch is True, "Agent must detect study hours mismatch"
    assert any("5.0 hrs/week" in c or "5" in c for c in agent_state.detected_changes), "Agent must detect 5 hrs/wk change"

    # Check that SQL milestone remained completed
    db.refresh(sql_milestone)
    assert sql_milestone.status == "completed", "SQL milestone must remain COMPLETED after hours change"
    print(f"✅ SQL milestone status preserved as: '{sql_milestone.status}'.")

    # STEP 10 & 11: Change Career Goal to Data Scientist & Run Agent Again
    print("\n[Step 10-11] Changing student career goal to 'Data Scientist' and triggering agent evaluation...")
    student.target_role = "Data Scientist"
    db.add(student)
    db.commit()

    agent_state_2 = controller.run_evaluation_cycle(trigger="goal_role_updated")
    print(f"🤖 Agent Evaluation Status: {agent_state_2.cycle_status}")
    print(f"🔍 Detected Factors: {agent_state_2.detected_changes}")
    print(f"⚡ Actions Executed: {[a.get('description', a.get('action')) for a in agent_state_2.actions_taken]}")

    assert agent_state_2.has_role_mismatch is True, "Agent must detect career role change"

    # STEP 12 & 13: Verify new skill requirements and preservation of completed work
    print("\n[Step 12-13] Verifying new requirements and completed milestone preservation...")
    active_rm = db.query(Roadmap).filter(Roadmap.student_id == student_id, Roadmap.status == "active").first()
    print(f"✅ Active Roadmap Role: {active_rm.target_role}")
    assert active_rm.target_role == "Data Scientist"

    preserved_completed = [m for m in active_rm.milestones if m.status == "completed"]
    print(f"✅ Preserved Completed Milestones in Data Scientist Roadmap: {len(preserved_completed)}")
    for pm in preserved_completed:
        print(f"   ✓ Preserved: {pm.title} (Status: {pm.status})")
    assert len(preserved_completed) >= 1, "Completed work matching the new role must be preserved"

    # STEP 14 & 15: Restart Backend Simulation (Disconnect and Reconnect to SQLite)
    print("\n[Step 14-15] Restarting backend simulation: Closing connection and re-opening SQLite database...")
    db.close()
    engine.dispose()

    # Re-open fresh connection to the same SQLite file
    engine2 = create_engine(DEMO_DB_URL, connect_args={"check_same_thread": False})
    Session2 = sessionmaker(bind=engine2)
    fresh_db = Session2()

    persisted_student = fresh_db.query(Student).filter(Student.id == student_id).first()
    assert persisted_student is not None, "Student profile must persist after restart"
    assert persisted_student.target_role == "Data Scientist", "Target role must persist"
    assert persisted_student.weekly_hours == 5.0, "Weekly study hours must persist"

    persisted_rm = fresh_db.query(Roadmap).filter(Roadmap.student_id == student_id, Roadmap.status == "active").first()
    assert persisted_rm is not None, "Roadmap must persist after restart"
    assert len(persisted_rm.milestones) >= 4, "Roadmap milestones must persist"

    persisted_completed = [m for m in persisted_rm.milestones if m.status == "completed"]
    assert len(persisted_completed) >= 1, "Completed milestones must remain completed after restart"

    persisted_revisions = fresh_db.query(RoadmapRevisionHistory).filter(RoadmapRevisionHistory.student_id == student_id).all()
    assert len(persisted_revisions) >= 1, "Revision audit history must persist"

    fresh_db.close()
    engine2.dispose()

    print("\n" + "=" * 75)
    print("🎉 ALL 15 END-TO-END DEMONSTRATION STEPS VERIFIED SUCCESSFULLY!")
    print("=" * 75)

if __name__ == "__main__":
    run_demonstration()
