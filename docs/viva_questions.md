# Viva Preparation Guide & Project Demonstration Script

---

## 🎯 Part 1: Comprehensive Viva Questions & Simple Answers

### 1. What is an AI Agent?
**Answer**: An AI Agent is an autonomous software entity that perceives its environment through sensors or state observation, reasons about its current state against defined goals, and takes actions through actuators or tools to achieve those goals. Unlike a passive script, an agent makes independent decisions and adapts to changing environmental conditions.

---

### 2. What problem does CareerAI solve?
**Answer**: College students often struggle to translate their academic coursework into concrete industry career roadmaps. They do not know which specific skills they are missing for their target role, which projects would demonstrate those skills, or how to adapt their study schedule when their available time or career goals change. CareerAI provides an autonomous, personalized, and persistent career guidance system that addresses this problem directly.

---

### 3. Why is CareerAI an AI Agent instead of a normal chatbot?
**Answer**: A normal chatbot is purely conversational and reactive—it accepts a user prompt and generates text, but it does not maintain persistent memory across sessions, does not observe changes in a relational database, and cannot autonomously execute tools to adapt schedules. 
CareerAI is a genuine agent because it operates through a structured **7-stage execution cycle** (Observe → Reason → Plan → Act → Verify → Persist → Report), executes **12 dedicated tools**, preserves completed work, and dynamically recalculates timelines.

---

### 4. What is autonomous decision-making in CareerAI?
**Answer**: Autonomous decision-making means the system independently detects when a student's state deviates from their goal (for example, when available study time drops from 10 to 5 hours per week) and autonomously selects and executes corrective actions (recalculating milestone durations, adjusting deadlines, and flagging blockers) without requiring manual micro-management.

---

### 5. How does the agent observe student progress?
**Answer**: In **Stage 1 (OBSERVE)**, the agent queries the SQLite database for:
- The student's academic profile and target role.
- Stored technical skill proficiency scores (0 to 5 scale).
- Active roadmap milestone statuses (`not_started`, `in_progress`, `completed`, `blocked`).
- Available weekly study hours.
- Historical agent observations and recent progress timestamps.

---

### 6. How does the agent select tools?
**Answer**: In **Stage 3 (PLAN)**, the Goal Planner inspects the reasoned factors from the Decision Engine. If an hours mismatch is detected, it plans `revise_career_roadmap`. If no roadmap exists, it plans `generate_career_roadmap`. In **Stage 4 (ACT)**, the controller calls only the tools prioritized in the plan rather than executing all tools blindly.

---

### 7. What is persistent memory and why is it important?
**Answer**: Persistent memory means the agent's knowledge, observations, and milestone progress are permanently saved in database storage (SQLite) rather than kept in volatile RAM. When the backend server restarts, the student's progress, previous agent decisions, and roadmap history remain completely intact.

---

### 8. Why use SQLite for local development?
**Answer**: SQLite is serverless, zero-configuration, lightweight, and self-contained in a single file (`careerai.db`). It provides full ACID transactions and relational foreign keys while being easily migratable to PostgreSQL in production via SQLAlchemy ORM.

---

### 9. What is an LLM and how is it used in CareerAI?
**Answer**: An LLM (Large Language Model) is a deep learning model trained on vast text data to understand and generate natural language. CareerAI integrates Claude 3.5 Sonnet to provide conversational explanations and personalized guidance in the AI Assistant. Importantly, model access is abstracted in a dedicated service module with working rule-based fallback when no API key is provided.

---

### 10. How does skill-gap analysis work?
**Answer**: Each career role has target competencies scored on a 0 to 5 scale:
$$\text{Gap} = \max(0, \text{Target Proficiency} - \text{Current Proficiency})$$
Gaps are categorized as **High Priority** (large gap in a critical skill), **Medium Priority** (moderate gap or prerequisite), or **Low Priority** (minor gap in supplementary skill).

---

### 11. How is a personalized roadmap generated?
**Answer**: The roadmap service sequences milestones into 5 progressive phases:
1. **Foundations**: Core prerequisites (e.g., Python and SQL).
2. **Core Competencies**: Main domain tools (e.g., Data Visualization & BI).
3. **Tooling & Refinement**: Supporting libraries.
4. **Capstone Portfolio Project**: Practical industry deliverable with code checklist.
5. **Career Readiness**: Interview prep and resume alignment.
Milestone duration is calculated realistically: $\text{Estimated Weeks} = \text{round}(\text{Estimated Hours} / \text{Weekly Hours}, 1)$.

---

### 12. How does the system adapt when a student changes their goal?
**Answer**: When a student switches from Data Analyst to Data Scientist:
1. The agent detects the role mismatch during Stage 2 (REASON).
2. It archives the previous roadmap.
3. It identifies transferable skills (e.g., Python and SQL).
4. In the new roadmap, transferable milestones previously completed are **strictly preserved** with `completed` status intact!
5. New milestones for advanced requirements (Machine Learning, Statistics) are added.

---

### 13. How does the Rule-Based Fallback Engine work?
**Answer**: When no Anthropic API key is configured, CareerAI's deterministic decision engine and rule-based assistant generate structured, contextual explanations by querying database state directly. This ensures 100% of the demonstration works offline without spending money on API calls.

---

### 14. What are the system's limitations?
**Answer**:
1. Designed as a local prototype for educational demonstration; a production SaaS would require multi-tenant JWT authentication.
2. Skill requirements are based on curated educational datasets rather than live web scraping of job portals.

---

### 15. How can the system be improved in the future?
**Answer**:
- Integrate live job market APIs (Indeed/LinkedIn) to dynamically adapt skill benchmarks.
- Connect student GitHub repositories to automatically inspect code commits and verify project deliverables.
- Implement peer study group matching based on shared career goals.

---

## 🎤 Part 2: Five-Minute Project Demonstration Script

*Use this script during your final-year college presentation and viva.*

### Minute 1: Introduction & Problem Statement
> *"Respected examiners and faculty members, good morning. My final year project is titled **CareerAI: An Autonomous, Persistent, and Personalized AI Career Guidance Agent for College Students** for the Agent Technology course.*
>
> *Today, students often struggle to translate university coursework into real-world career roadmaps. Generic chatbots lack persistent memory and hallucinate schedules, while static websites cannot adapt. CareerAI solves this by acting as an autonomous software agent that continuously observes student progress, calculates skill gaps, and proactively revises milestone roadmaps."*

### Minute 2: Architecture & The 7-Stage Agent Loop
> *(Show Landing Page and 7-Stage diagram)*
> *"CareerAI is built using React with Tailwind CSS on the frontend, FastAPI and SQLAlchemy on the backend, and SQLite for persistent storage.
>
> What makes this an authentic AI Agent rather than a simple chatbot is our **7-Stage Execution Loop**:
> 1. **Observe**: The agent gathers the student profile, skill ratings, and roadmap state.
> 2. **Reason**: It deterministically evaluates skill gaps and checks for schedule or goal changes.
> 3. **Plan**: It selects the next best action.
> 4. **Act**: It executes dedicated Python agent tools.
> 5. **Verify**: It validates schema integrity and ensures completed work is never overwritten.
> 6. **Persist**: It records observations and action logs to SQLite.
> 7. **Report**: It provides transparent explanations in a section titled 'Why CareerAI Recommended This'."*

### Minute 3: Live Demonstration of Onboarding & Skill Gaps
> *(Navigate to Student Onboarding and Dashboard)*
> *"Let me demonstrate our live application. Here on the Onboarding page, we create a profile for 'Arjun Sen', a 3rd-year CS student targeting the **Data Analyst** role with **10 hours per week** of study time. He has Python and SQL at basic level 2 on our 0-to-5 scale.
>
> On the **Skill Gap Analysis** page, the agent calculates that SQL target is 4, so there is a 2-level gap. Python target is 3, leaving a 1-level gap. The match percentage is visually charted, and practical exercises are recommended."*

### Minute 4: Roadmap Execution & Completed Work Preservation
> *(Navigate to Career Roadmap)*
> *"On the Career Roadmap page, the agent generated an 8-milestone roadmap structured across 5 phases. Each milestone has verified documentation links and project deliverables.
>
> Now, Arjun completes his SQL milestone. I mark it **Completed**. Notice our completion bar updates.
>
> Next, Arjun's college exams arrive, and his available time drops from **10 hours to 5 hours per week**. I update his profile and click **'Evaluate My Progress'** on the dashboard.
>
> Watch the agent in action: it observes the hours change, reasons that remaining milestones require more weeks, rebalances the deadlines, and **preserves his completed SQL milestone**!
>
> Even if Arjun switches his target role to **Data Scientist**, CareerAI archives the old roadmap, generates the new requirements, and transfers his completed SQL work."*

### Minute 5: Context-Aware Assistant & Conclusion
> *(Navigate to AI Assistant page)*
> *"Finally, here is our AI Career Assistant. Notice the badge shows **'Mode: Rule-Based Fallback'**, meaning our core workflow requires zero paid API keys. When I click *'What should I learn this week?'*, it doesn't give a generic answer—it specifically references Arjun's current active milestone and available hours.
>
> In conclusion, CareerAI has been validated with **13 automated tests** passing in under 1 second and a complete 15-step end-to-end verification. Thank you, and I am now ready for your questions."*
