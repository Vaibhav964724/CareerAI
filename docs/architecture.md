# System Architecture: CareerAI

## 1. High-Level Architectural Overview

CareerAI is designed as an autonomous, persistent, multi-layered career guidance system composed of three core tiers:
1. **Interactive Client Tier**: React.js SPA built with Vite and Tailwind CSS.
2. **Autonomous Agent & Service Tier**: FastAPI backend running Python 3.10+ with a dedicated 7-Stage Agent Controller, 12 testable agent tools, a deterministic rule engine, and an optional Claude LLM service module.
3. **Persistence & Data Tier**: Relational SQLite database accessed via SQLAlchemy ORM with foreign-key cascades, storing profiles, roadmaps, milestones, observations, and revision audit logs.

```mermaid
graph TD
    subgraph "Client Layer (React.js + Tailwind CSS)"
        UI[User Interface / 7 Application Pages]
        API_CLIENT[Centralized API Client / services/api.js]
        UI --> API_CLIENT
    end

    subgraph "API Gateway Layer (FastAPI)"
        ROUTERS[FastAPI REST Routers /api/v1]
        CORS[CORS & Middleware]
        API_CLIENT --> CORS --> ROUTERS
    end

    subgraph "Autonomous Agent Layer"
        CONTROLLER[7-Stage Agent Controller]
        DECISION[Deterministic Decision Engine]
        PLANNER[Goal-Oriented Action Planner]
        TOOLS[12 Testable Agent Tools]
        MEMORY[Agent Persistent Memory Manager]

        CONTROLLER --> DECISION
        CONTROLLER --> PLANNER
        CONTROLLER --> TOOLS
        CONTROLLER --> MEMORY
    end

    subgraph "Domain & Intelligence Services"
        CAREER_SRV[Career Requirements & Gap Engine]
        ROADMAP_SRV[Phased Roadmap Generation & Revision]
        LLM_SRV[LLM Service / Claude 3.5 Sonnet + Rule Fallback]
        
        TOOLS --> CAREER_SRV
        TOOLS --> ROADMAP_SRV
        ROUTERS --> LLM_SRV
    end

    subgraph "Persistence Layer (SQLite / PostgreSQL Compatible)"
        DB[(careerai.db / SQLAlchemy ORM)]
        CAREER_ROLES[career_roles.json]
        PROJECT_CATALOG[project_catalog.json]
        
        MEMORY --> DB
        ROADMAP_SRV --> DB
        CAREER_SRV --> DB
        CAREER_SRV -. seeds .- CAREER_ROLES
        ROADMAP_SRV -. references .- PROJECT_CATALOG
    end
```

---

## 2. Data Flow & Autonomous Execution Loop

The Agent Controller coordinates seven distinct lifecycle stages during an evaluation cycle:

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as Frontend Dashboard
    participant API as FastAPI Router
    participant Agent as Agent Controller
    participant Engine as Decision Engine
    participant Tools as Agent Tools
    participant DB as SQLite Database

    Student->>UI: Clicks "Evaluate My Progress"
    UI->>API: POST /api/v1/agent/evaluate/{student_id}
    API->>Agent: run_evaluation_cycle(trigger)
    
    Note over Agent: Stage 1: OBSERVE
    Agent->>DB: Query Student Profile, Roadmaps, Milestones, Delays
    DB-->>Agent: Raw State Snapshot

    Note over Agent: Stage 2: REASON
    Agent->>Engine: Evaluate gaps, delays, hour changes, role shifts
    Engine-->>Agent: Reasoned Factors & Detected State Changes

    Note over Agent: Stage 3: PLAN
    Agent->>Agent: Prioritize target actions (rebalance hours, adapt role, flag delays)

    Note over Agent: Stage 4: ACT
    Agent->>Tools: Invoke selected tools (revise_roadmap, evaluate_next_action)
    Tools->>DB: Update roadmap durations & milestones

    Note over Agent: Stage 5: VERIFY
    Agent->>Agent: Validate schema, prerequisite sequence, and completed work preservation

    Note over Agent: Stage 6: PERSIST
    Agent->>DB: Save AgentObservation & AgentActionLog

    Note over Agent: Stage 7: REPORT
    Agent-->>API: Formulate concise summary ("Why CareerAI Recommended This")
    API-->>UI: Return AgentEvaluationResponse
    UI-->>Student: Update dashboard indicators & display decision explanation
```

---

## 3. Database Schema Design (Entity-Relationship)

The relational SQLite schema maintains referential integrity through foreign keys and cascade deletes:

```mermaid
erDiagram
    STUDENTS ||--o{ STUDENT_SKILL_ASSESSMENTS : "assesses"
    STUDENTS ||--o{ ROADMAPS : "owns"
    STUDENTS ||--o{ AGENT_OBSERVATIONS : "logs"
    STUDENTS ||--o{ AGENT_ACTION_LOGS : "audits"
    STUDENTS ||--o{ PROGRESS_UPDATES : "tracks"
    
    CAREER_ROLES ||--o{ ROLE_REQUIREMENTS : "defines"
    
    ROADMAPS ||--o{ ROADMAP_MILESTONES : "contains"
    ROADMAPS ||--o{ ROADMAP_REVISION_HISTORY : "tracks"
    
    ROADMAP_MILESTONES ||--o{ PROGRESS_UPDATES : "records"

    STUDENTS {
        int id PK
        string name
        string email
        string degree
        string branch
        int year_of_study
        float gpa
        text interests
        text existing_projects
        string target_role
        float weekly_hours
        int timeline_months
        datetime created_at
    }

    STUDENT_SKILL_ASSESSMENTS {
        int id PK
        int student_id FK
        string skill_name
        int proficiency
        datetime verified_at
    }

    CAREER_ROLES {
        int id PK
        string slug
        string title
        text description
        string industry
        string average_salary_range
        string job_outlook
    }

    ROLE_REQUIREMENTS {
        int id PK
        int role_id FK
        string skill_name
        int target_proficiency
        string importance
        text prerequisites
        text example_activities
        text suggested_projects
    }

    ROADMAPS {
        int id PK
        int student_id FK
        string target_role
        float total_estimated_weeks
        float weekly_hours
        string status
        int version
        datetime created_at
    }

    ROADMAP_MILESTONES {
        int id PK
        int roadmap_id FK
        string title
        int phase_number
        string phase_name
        text description
        text required_skills
        string priority
        float estimated_hours
        float estimated_weeks
        text prerequisites
        text learning_resources
        text recommended_project
        text completion_criteria
        string deadline
        string status
        int order_index
        datetime completed_at
    }
```

---

## 4. Key Architectural Decisions

1. **Deterministic Logic vs. Pure LLM**: Business rules (skill gap math, duration formulas, completed milestone preservation) are executed by deterministic Python logic rather than unconstrained prompt engineering. This eliminates arithmetic hallucinations and guarantees consistent test results.
2. **Dual Operational Modes**: By implementing a complete Rule-Based Fallback Engine, the application runs out-of-the-box in local environments without requiring paid third-party API credentials.
3. **Relational Data Integrity**: Roadmaps and milestones are stored as individual database entities with primary keys rather than serialized JSON blobs. This allows direct status updates (`PATCH /api/v1/roadmaps/milestones/{id}`) and granular audit tracking.
