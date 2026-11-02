# CareerAI: Autonomous Career Guidance Agent for College Students

**CareerAI** is an autonomous, persistent, and personalized AI career guidance agent designed for college students. Developed for the final-year **Agent Technology** curriculum, it translates a student's academic background and technical competencies into a structured, milestone-based career roadmap.

Unlike a static career website or generic chatbot, CareerAI implements a true **7-stage autonomous agent execution loop** (Observe → Reason → Plan → Act → Verify → Persist → Report), utilizes **12 testable agent tools**, maintains **persistent SQLite memory**, and dynamically adapts roadmaps when study hours or career aspirations change while strictly preserving completed milestones.

---

## 🌟 Key Capabilities

1. **7-Stage Autonomous Agent Controller**: Closed-loop reasoning cycle that evaluates profile changes, detects learning bottlenecks, and balances timelines.
2. **Deterministic Skill Gap Analysis**: Evaluates skills against standardized role profiles on a deterministic 0 to 5 scale (`Gap = max(0, Target - Current)`).
3. **Phased Milestone Roadmap Generation**: Sequences learning into 5 phases (Foundations, Core Competencies, Tooling, Portfolio Capstone, Career Readiness) with verified documentation links.
4. **Completed Work Preservation**: When available study hours drop or target roles change, previously completed milestones are never discarded.
5. **Context-Aware AI Career Assistant**: Directly retrieves saved student state, roadmap progress, and evaluated gaps before answering queries.
6. **Dual Operational Modes**:
   - **Mode A (Claude LLM)**: Activates when an Anthropic API key is provided.
   - **Mode B (Rule-Based Fallback)**: Runs 100% locally with zero paid API keys needed, ensuring full functionality during college vivas.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React, Recharts
- **Backend**: Python 3.10+, FastAPI, Pydantic V2, SQLAlchemy
- **Database**: SQLite (default local file storage) / PostgreSQL compatible
- **Testing**: pytest (13/13 automated tests passing)

---

## 💻 Windows Setup & Execution Guide (PowerShell / VS Code)

Follow these exact steps to run CareerAI locally on Windows.

### Prerequisites

Verify that the required software is installed:

```powershell
python --version   # Python 3.10, 3.11, 3.12, or 3.13
node --version     # Node.js v18 or newer
npm --version      # npm v9 or newer
```

---

### Step 1: Open Terminal in Project Root

Open Visual Studio Code and open the `CareerAI` workspace folder:

```powershell
cd C:\Users\VAIBHAV\Downloads\AI_Agent\CareerAI
```

---

### Step 2: Set Up Backend Virtual Environment

Open a new PowerShell terminal for the **Backend**:

```powershell
# Set working directory to backend
cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If PowerShell blocks script activation, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Install backend dependencies
pip install -r requirements.txt
```

---

### Step 3: Configure Environment Variables

Create your local `.env` file from the example template:

```powershell
# From the backend folder:
Copy-Item ..\.env.example .env
```

*(Optional: If you wish to enable Claude LLM mode, open `.env` and paste your `ANTHROPIC_API_KEY=your_key_here`. Otherwise, leave blank to use the built-in zero-cost Rule-Based Fallback Engine).*

---

### Step 4: Start the FastAPI Backend Server

In your backend terminal with `venv` activated:

```powershell
# Working directory: CareerAI\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

You should see:
```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

- **Interactive API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

---

### Step 5: Start the React Frontend Application

Open a **second terminal window** in Visual Studio Code:

```powershell
# Navigate to the frontend directory
cd C:\Users\VAIBHAV\Downloads\AI_Agent\CareerAI\frontend

# Install frontend dependencies (if not already installed)
npm install

# Start the Vite development server
npm run dev
```

You should see:
```text
  VITE v5.3.4  ready in 320 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Open your web browser and navigate to:
👉 **[http://localhost:5173](http://localhost:5173)**

---

## 🧪 Running Automated Tests

To run the complete automated test suite verifying profile CRUD, skill-gap math, roadmap generation, hours revision, role switching, completed work preservation, and API routes:

Open a terminal in `CareerAI\backend`:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run pytest
pytest tests -v
```

**Actual Observed Test Output**:
```text
CareerAI/backend/tests/test_agent.py::test_agent_controller_full_cycle PASSED [  7%]
CareerAI/backend/tests/test_agent.py::test_agent_detects_hours_change_and_adapts PASSED [ 15%]
CareerAI/backend/tests/test_agent.py::test_evaluate_next_best_action PASSED [ 23%]
CareerAI/backend/tests/test_api.py::test_api_health_check PASSED         [ 30%]
CareerAI/backend/tests/test_api.py::test_api_student_lifecycle PASSED    [ 38%]
CareerAI/backend/tests/test_roadmap.py::test_generate_roadmap_structure PASSED [ 46%]
CareerAI/backend/tests/test_roadmap.py::test_milestone_completion_and_hours_revision PASSED [ 53%]
CareerAI/backend/tests/test_roadmap.py::test_role_change_preserves_completed_milestones PASSED [ 61%]
CareerAI/backend/tests/test_skill_gaps.py::test_skill_gap_calculation_deterministic PASSED [ 69%]
CareerAI/backend/tests/test_skill_gaps.py::test_skill_gap_when_exceeding_target PASSED [ 76%]
CareerAI/backend/tests/test_skill_gaps.py::test_compare_career_roles PASSED [ 84%]
CareerAI/backend/tests/test_student.py::test_create_student_profile PASSED [ 92%]
CareerAI/backend/tests/test_student.py::test_update_student_profile PASSED [100%]
====================== 13 passed in 0.92s ======================
```

---

## 🚀 Running the 15-Step End-to-End Demonstration Verification

An automated verification script executes the exact 15-step lifecycle scenario:

```powershell
# Working directory: CareerAI\backend
python verify_demo_scenario.py
```

It validates:
1. Profile creation (Arjun Sen)
2. Target role set to Data Analyst
3. Python & SQL proficiency entered
4. Skill-gap calculation verified
5. 8-milestone roadmap generated
6. SQL marked as completed
7. Hours changed from 10 to 5 hrs/week
8. Agent controller runs and detects hours mismatch
9. Milestones rebalanced; SQL completion preserved
10. Target role changed to Data Scientist
11. Agent runs transition cycle
12. New requirements identified
13. Transferable completed milestones preserved
14. Backend disconnected and restarted
15. Full persistence across server restart verified

---

## 📁 Project Structure

```text
CareerAI/
├── README.md                      # Windows setup & guide
├── .gitignore                     # Git exclusion rules
├── .env.example                   # Environment template
├── requirements.txt               # Backend dependencies
├── backend/
│   ├── requirements.txt
│   ├── verify_demo_scenario.py    # 15-step demo script
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── config.py              # Configuration & env loader
│   │   ├── database.py            # SQLite engine & session
│   │   ├── models/                # SQLAlchemy database models
│   │   │   ├── student.py
│   │   │   ├── career.py
│   │   │   ├── roadmap.py
│   │   │   └── agent_log.py
│   │   ├── schemas/               # Pydantic V2 schemas
│   │   │   ├── student.py
│   │   │   ├── career.py
│   │   │   ├── roadmap.py
│   │   │   └── agent.py
│   │   ├── api/                   # RESTful API routers
│   │   │   ├── routes_student.py
│   │   │   ├── routes_career.py
│   │   │   ├── routes_roadmap.py
│   │   │   ├── routes_agent.py
│   │   │   └── routes_assistant.py
│   │   ├── agent/                 # Autonomous Agent Core
│   │   │   ├── controller.py      # 7-stage controller
│   │   │   ├── state.py           # Structured agent state
│   │   │   ├── memory.py          # Persistent memory manager
│   │   │   ├── decision_engine.py # Rule-based reasoning
│   │   │   ├── planner.py         # Goal-oriented action planner
│   │   │   └── tools.py           # 12 testable agent tools
│   │   ├── services/              # Domain services
│   │   │   ├── career_service.py  # Gaps & role dataset
│   │   │   ├── roadmap_service.py # Phased roadmap engine
│   │   │   └── llm_service.py     # Claude + fallback engine
│   │   └── data/
│   │       ├── career_roles.json  # 8 career profiles
│   │       └── project_catalog.json # Project catalog
│   └── tests/                     # Automated pytest suite
│       ├── conftest.py
│       ├── test_student.py
│       ├── test_skill_gaps.py
│       ├── test_roadmap.py
│       ├── test_agent.py
│       └── test_api.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── components/            # Reusable UI components
│       │   ├── Navbar.jsx
│       │   ├── Footer.jsx
│       │   ├── ModeBadge.jsx
│       │   ├── StatCard.jsx
│       │   ├── ProgressBar.jsx
│       │   └── Badge.jsx
│       ├── pages/                 # Application pages
│       │   ├── LandingPage.jsx    # Page A: Landing Page
│       │   ├── OnboardingPage.jsx # Page B: Onboarding & Edit
│       │   ├── DashboardPage.jsx  # Page C: Main Dashboard
│       │   ├── SkillGapPage.jsx   # Page D: Skill Gap Matrix
│       │   ├── RoadmapPage.jsx    # Page E: Phased Roadmap
│       │   ├── AssistantPage.jsx  # Page F: AI Career Assistant
│       │   └── ProgressPage.jsx   # Page G: Audit & Explanations
│       └── services/
│           └── api.js             # Centralized API client
└── docs/
    ├── architecture.md            # System architecture document
    ├── agent_workflow.md          # 7-stage agent deep dive
    ├── test_scenarios.md          # Test scenarios & matrices
    ├── project_report.md          # 26-section college report
    └── viva_questions.md          # Viva questions & demo script
```
