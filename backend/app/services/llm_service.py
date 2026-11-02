import os
import json
from typing import Dict, Any, List, Optional, Tuple
from app.config import settings

def is_llm_active() -> bool:
    """Return True if an Anthropic API key is provided in settings/environment."""
    return bool(settings.ANTHROPIC_API_KEY and len(settings.ANTHROPIC_API_KEY.strip()) > 10)

def get_active_mode() -> str:
    """Returns 'llm' or 'rule-based'."""
    return "llm" if is_llm_active() else "rule-based"

def generate_assistant_response(
    student_profile: Dict[str, Any],
    active_roadmap: Optional[Dict[str, Any]],
    skill_gaps: Optional[List[Dict[str, Any]]],
    user_query: str
) -> Tuple[str, str, Dict[str, Any], List[str]]:
    """
    Generate an intelligent response to a student question using either Claude LLM
    or the robust Rule-Based Fallback Engine.
    Returns (reply_text, mode_used, relevant_context, suggested_questions).
    """
    mode = get_active_mode()
    query_lower = user_query.strip().lower()

    # Extract student context
    student_name = student_profile.get("name", "Student")
    target_role = student_profile.get("target_role", "Target Role")
    weekly_hours = student_profile.get("weekly_hours", 10.0)

    milestones = active_roadmap.get("milestones", []) if active_roadmap else []
    completed_m = [m for m in milestones if m.get("status") == "completed"]
    in_progress_m = [m for m in milestones if m.get("status") == "in_progress"]
    not_started_m = [m for m in milestones if m.get("status") == "not_started"]

    context_summary = {
        "student_name": student_name,
        "target_role": target_role,
        "weekly_hours": weekly_hours,
        "completed_count": len(completed_m),
        "in_progress_count": len(in_progress_m),
        "pending_count": len(not_started_m),
        "total_gaps": len(skill_gaps) if skill_gaps else 0
    }

    # If LLM key is configured, try calling Anthropic Claude
    if mode == "llm":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            
            system_prompt = (
                f"You are CareerAI, an autonomous and personalized career guidance mentor for college students. "
                f"You have direct access to the student's academic profile and active career roadmap.\n\n"
                f"STUDENT CONTEXT:\n"
                f"- Name: {student_name}\n"
                f"- Target Career Role: {target_role}\n"
                f"- Weekly Study Hours: {weekly_hours} hrs/week\n"
                f"- Degree/Branch: {student_profile.get('degree')} in {student_profile.get('branch')}\n"
                f"- Current Roadmaps Milestones: {len(completed_m)} completed, {len(in_progress_m)} in-progress, {len(not_started_m)} pending.\n"
                f"- Evaluated Skill Gaps: {json.dumps(skill_gaps[:5] if skill_gaps else [])}\n\n"
                f"GUIDELINES:\n"
                f"1. Give direct, practical, and highly personalized advice.\n"
                f"2. Cite their specific target role and current milestones.\n"
                f"3. Do not invent fake certifications or URLs.\n"
                f"4. Keep explanations encouraging and clear for a college student."
            )

            response = client.messages.create(
                model=settings.LLM_MODEL,
                max_tokens=600,
                system=system_prompt,
                messages=[{"role": "user", "content": user_query}]
            )
            reply_text = response.content[0].text
            suggested = [
                "What should I learn this week?",
                "Which skill gap is my highest priority?",
                "Recommend a project to build for my portfolio."
            ]
            return reply_text, "llm", context_summary, suggested

        except Exception as e:
            # Fallback seamlessly if API call fails
            mode = "rule-based"

    # --- RULE-BASED FALLBACK ENGINE ---
    # Intelligently handles key queries based on student's database state
    suggested = [
        "What should I learn this week?",
        f"Which skills am I missing for {target_role}?",
        "Recommend a project based on my current skills.",
        "I have only 5 hours per week. How does my plan adapt?",
        "I completed SQL. What should I do next?"
    ]

    # Query 1: "What should I learn this week?" / next step
    if any(k in query_lower for k in ["this week", "next step", "what should i learn", "what to study", "start now"]):
        if in_progress_m:
            curr = in_progress_m[0]
            reply = (
                f"👋 Hi {student_name}! Based on your current roadmap for **{target_role}**, you are actively working on:\n\n"
                f"🎯 **{curr.get('title')}** (Phase {curr.get('phase_number')}: {curr.get('phase_name')})\n\n"
                f"📝 **Description**: {curr.get('description')}\n"
                f"⏱️ **Target Pace**: ~{curr.get('estimated_weeks')} weeks at your commitment of {weekly_hours} hours/week.\n"
                f"✅ **Completion Criteria**: {curr.get('completion_criteria')}\n\n"
                f"💡 **Recommended Action**: Focus on completing this milestone's practical exercises before advancing to downstream prerequisites."
            )
        elif not_started_m:
            next_m = not_started_m[0]
            reply = (
                f"👋 Hi {student_name}! Your next scheduled milestone for **{target_role}** is:\n\n"
                f"🚀 **{next_m.get('title')}** (Phase {next_m.get('phase_number')}: {next_m.get('phase_name')})\n\n"
                f"📝 **Objective**: {next_m.get('description')}\n"
                f"⏱️ **Estimated Duration**: {next_m.get('estimated_weeks')} weeks ({next_m.get('estimated_hours')} study hours).\n"
                f"🏁 **Goal**: {next_m.get('completion_criteria')}\n\n"
                f"You can mark this milestone as **In Progress** on your Roadmap page to begin tracking your active progress!"
            )
        else:
            reply = (
                f"🎉 Congratulations {student_name}! All milestones in your current roadmap for **{target_role}** are completed! "
                f"You are ready to compile your portfolio, polish your resume, and begin targeting entry-level positions."
            )

    # Query 2: Missing skills / skill gap breakdown
    elif any(k in query_lower for k in ["missing", "skill gap", "skills am i missing", "gap", "weakness"]):
        if skill_gaps:
            top_gaps = [g for g in skill_gaps if g.get("gap", 0) > 0]
            if top_gaps:
                gap_lines = []
                for g in top_gaps[:4]:
                    gap_lines.append(
                        f"- **{g.get('skill_name')}** (Current: {g.get('current_proficiency')}/5 → Target: {g.get('target_proficiency')}/5) | Priority: **{g.get('priority')}**\n"
                        f"  *Reason*: {g.get('reason')}"
                    )
                reply = (
                    f"📊 **Skill Gap Analysis for {target_role}**:\n\n"
                    f"Here are the most critical skills you need to build:\n\n" +
                    "\n".join(gap_lines) +
                    f"\n\n🎯 Your roadmap automatically organizes these gaps into phased milestones respecting prerequisite dependencies."
                )
            else:
                reply = f"✨ Great job! You currently meet or exceed the target proficiency in all core skills required for **{target_role}**."
        else:
            reply = f"Run the **Skill Gap Analysis** from the navigation bar to evaluate your profile against the benchmark requirements for {target_role}."

    # Query 3: Project recommendations
    elif any(k in query_lower for k in ["recommend a project", "project", "portfolio project", "what to build"]):
        if active_roadmap and milestones:
            # Pick capstone or current milestone's project
            capstone = next((m for m in milestones if m.get("phase_number") == 4), None)
            if capstone and capstone.get("recommended_project"):
                proj = capstone.get("recommended_project")
                if isinstance(proj, str):
                    try:
                        proj = json.loads(proj)
                    except:
                        proj = {}
                reply = (
                    f"🛠️ **Recommended Portfolio Project for {target_role}**:\n\n"
                    f"📌 **{proj.get('title', 'Capstone Industry Project')}**\n\n"
                    f"📄 **Overview**: {proj.get('description', 'Comprehensive end-to-end practical project.')}\n\n"
                    f"📦 **Key Deliverables**:\n" +
                    "\n".join([f"- {d}" for d in proj.get("deliverables", ["Source code on GitHub", "Clean documentation"])]) +
                    f"\n\n💡 Building this validates your applied skills for prospective technical interviewers."
                )
            else:
                reply = (
                    f"🛠️ For a **{target_role}**, we recommend building an end-to-end data pipeline or application "
                    f"with public GitHub commits, README documentation, and a live or reproducible demonstration."
                )
        else:
            reply = "Generate your personalized roadmap to see tailored portfolio projects aligned with your target role."

    # Query 4: Study hours adjustment (e.g. "5 hours per week")
    elif any(k in query_lower for k in ["5 hours", "five hours", "hours per week", "available time", "study time", "less time"]):
        reply = (
            f"⏱️ **Adapting to Available Study Time**:\n\n"
            f"If your weekly study time changes (e.g., from 10 hours/week to 5 hours/week), CareerAI's agent controller "
            f"will automatically recalculate the duration of all remaining milestones without discarding your completed work!\n\n"
            f"- At **5 hours/week**, milestones take proportionally longer, ensuring a realistic, achievable schedule without burnout.\n"
            f"- You can update your available hours on the **Student Profile** page and click **Evaluate My Progress** on the dashboard to apply the revision."
        )

    # Query 5: Milestone completed (e.g. "completed sql")
    elif any(k in query_lower for k in ["completed sql", "finished sql", "i completed", "what next"]):
        reply = (
            f"🎉 Excellent work completing your milestone!\n\n"
            f"When you mark a milestone as **Completed** on your Roadmap page:\n"
            f"1. CareerAI immediately logs a progress update.\n"
            f"2. Your overall roadmap completion percentage increases.\n"
            f"3. Any downstream milestones that depended on it as a prerequisite become unlocked.\n\n"
            f"Next, proceed to your next sequential milestone or check the dashboard for your agent's **Next Best Action**!"
        )

    # Query 6: Career change (e.g. "Data Scientist instead")
    elif any(k in query_lower for k in ["data scientist", "switch role", "change goal", "change role", "become a"]):
        reply = (
            f"🔄 **Switching Career Path**:\n\n"
            f"If you switch your target goal (for instance, from **Data Analyst** to **Data Scientist**):\n"
            f"1. **Transferable Skills Are Preserved**: Common foundations like Python fundamentals and SQL queries carry over directly with your completed progress intact.\n"
            f"2. **New Skill Requirements Are Added**: Data Scientist introduces advanced requirements such as Machine Learning algorithms, statistical modeling, and deep learning basics.\n"
            f"3. **Milestone Rebalancing**: CareerAI archives obsolete milestones while inserting new, targeted phases for your new goal."
        )

    # Default fallback
    else:
        reply = (
            f"👋 Hello {student_name}! I am CareerAI's autonomous career guidance assistant.\n\n"
            f"You are currently preparing for the **{target_role}** role with an allocation of **{weekly_hours} hours/week**.\n"
            f"Your roadmap currently has **{len(completed_m)} completed** and **{len(not_started_m)} pending** milestones.\n\n"
            f"Feel free to ask me:\n"
            f"- *'What should I learn this week?'*\n"
            f"- *'Which skills am I missing for {target_role}?'*\n"
            f"- *'Recommend a project based on my current skills.'*\n"
            f"- *'How does my plan change if I have 5 hours per week?'*"
        )

    return reply, "rule-based", context_summary, suggested
