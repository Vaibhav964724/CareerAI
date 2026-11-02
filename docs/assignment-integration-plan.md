# Assignment Integration Plan: Agent Technology & CareerAI

## 1. Executive Summary

This integration plan systematically aligns the five university **Agent Technology** curriculum assignments with the existing **CareerAI** production codebase. Rather than building separate, disconnected toy scripts, all five assignments are engineered as first-class architectural modules embedded directly into CareerAI:
1. **Assignment 1.2**: Simple Reflex Agent & Environmental Telemetry Reasoner.
2. **Assignment 2.1**: Concurrent Background Worker Daemon & Thread-Safe Monitoring.
3. **Assignment 2.2**: Distributed TCP Socket Messaging & State Serialization Mesh.
4. **Assignment 3.1**: Multi-Agent Negotiation Protocol (Contract Net / Bidding Consensus).
5. **Assignment 3.2**: Self-Interested Agent Utility Optimization & Resource Allocation.

All assignments are accessible both through an interactive web-based **Agent Technology Lab** in the React frontend and through standalone, fully-commented console CLI scripts in `backend/assignments/`.

---

## 2. Assignment-to-CareerAI Mapping Matrix

| Assignment ID | Original Title & Objective | Agent Tech Concept | Existing CareerAI Feature | Integration Status | Required Architectural Additions | Demonstration & Verification Method |
|---|---|---|---|---|---|---|
| **Assignment 1.2** | **Rule-Based Environmental Reasoner Implementation**<br>Implement a simple reflex agent architecture processing incoming telemetry and triggering condition-action rules. | Simple Reflex Agent, Condition-Action Rules, Telemetry Stream Parsing | Existing `DecisionEngine` evaluates static database state during evaluation cycles. | **Partially Implemented** (Extended to real-time stream) | Implement `ReflexReasoner` parsing streaming telemetry packets (student velocity, market demand, burnout index) and triggering reactive logs. | **Web UI**: Interactive Telemetry Stream Simulator in Agent Lab.<br>**CLI**: `python assignment_1_2_reflex_agent.py`. |
| **Assignment 2.1** | **Concurrent Task Daemonization using Threads and Workers**<br>Implement background daemon worker with thread-safe queues/locks to avoid blocking UI or event loops. | Multi-threading, Daemon Worker Threads, Thread Safety (`threading.Lock`, `queue.Queue`), Performance Latency Logs | Existing FastAPI handles requests asynchronously, but lacked a dedicated continuous daemon thread. | **New Feature Added** | Implement `CareerMonitorDaemon` running as a background thread with thread-safe queue and lock, periodically calculating health metrics without blocking UI. | **Web UI**: Live Daemon Monitor dashboard with latency telemetry.<br>**CLI**: `python assignment_2_1_daemon_worker.py`. |
| **Assignment 2.2** | **Distributed Agent Messaging using Sockets/RPC Communication**<br>Establish raw Socket/RPC endpoints to transfer typed state payloads between Agent-A and Agent-B. | Distributed Sockets, State Serialization, Remote Inter-Agent Messaging, Client-Server Protocol | Existing FastAPI uses HTTP REST; raw TCP socket communication for dual-agent remote sync was missing. | **New Feature Added** | Implement `SocketAgentA` (Student Advisor) and `SocketAgentB` (Placement Node) communicating via raw TCP sockets with serialized JSON state frames. | **Web UI**: Socket Message Dispatcher in Agent Lab.<br>**CLI**: `python assignment_2_2_socket_messaging.py` (Dual-terminal socket verification). |
| **Assignment 3.1** | **Multi-Agent Coordination Protocol Execution**<br>Code a controlled negotiation protocol between distinct agent instances converging to a consensus handshake. | Multi-Agent Systems (MAS), Contract Net Protocol, Multi-Turn Negotiation, Concession Curves, Consensus Handshake | Existing system was single-agent; lacked inter-agent bidding and negotiation protocol. | **New Feature Added** | Implement `StudentAgent` and `RecruiterAgent` negotiating project stipends, timelines, and deliverables across multi-turn bids with utility concession curves. | **Web UI**: Step-by-Step Negotiation Timeline Visualizer.<br>**CLI**: `python assignment_3_1_negotiation.py`. |
| **Assignment 3.2** | **Self-Interested Agent Utility Optimization for E-Commerce / Resource Allocation**<br>Formulate mathematical utility scoring mechanics to select the optimal resource configuration out of 10 complex options. | Multi-Attribute Utility Theory (MAUT), Constrained Optimization, Combinatorial Decision Making | Existing system prioritized skill gaps, but lacked explicit multi-term economic utility functions over budget/time constraints. | **New Feature Added** | Implement `UtilityOptimizer` with mathematical scoring formula: $U(x) = \sum w_i S_i(x) - \sum c_j C_j(x)$, filtering 10 complex course/project bundles to select the global maximum. | **Web UI**: Interactive Weight & Constraint Optimizer with bar chart rankings.<br>**CLI**: `python assignment_3_2_utility_optimizer.py`. |

---

## 3. Detailed Assignment Analysis

### Assignment 1.2: Rule-Based Environmental Reasoner
- **Rubrics Checklist (5 Marks)**:
  - Code Execution & Syntax (2 Marks): Clean PEP 8 Python 3.10+ implementation with zero runtime errors.
  - Sensory Parsing Logic (1.5 Marks): Parses incoming telemetry feeds containing timestamp, study hours, market demand index, and exam proximity.
  - Condition-Action Dynamic Triggering (1.5 Marks): Explicit rules triggering dynamic alerts (e.g. Schedule Compression, Market Surge, Milestone Unlock).

### Assignment 2.1: Concurrent Task Daemonization
- **Rubrics Checklist (5 Marks)**:
  - Multi-threading/Worker Infrastructure (2 Marks): Dedicated worker thread spawned with `daemon=True`.
  - Daemon Monitoring Functionality (1.5 Marks): Periodically scans active student milestones, detects overdue deadlines, and computes system latency metrics.
  - Thread Safety & Concurrency Handling (1.5 Marks): Inter-thread variable sharing governed by `threading.Lock` and thread-safe queues.

### Assignment 2.2: Distributed Agent Messaging
- **Rubrics Checklist (5 Marks)**:
  - Network Socket/RPC Stability (2 Marks): Robust TCP socket server and client handling connect/disconnect/timeout gracefully.
  - Data Serialization & Transport (1.5 Marks): Encodes structured agent parameters into serialized JSON frames with length-prefix framing.
  - Proactive Remote Message Handling (1.5 Marks): Agent-B ingests remote payload, evaluates student criteria, and autonomously dispatches verification response.

### Assignment 3.1: Multi-Agent Coordination Protocol
- **Rubrics Checklist (5 Marks)**:
  - Multi-Instance Setup Stability (1.5 Marks): Independent instances of `StudentAgent` and `RecruiterAgent` with private utility parameters.
  - Negotiation Protocol Implementation (2 Marks): Formal proposal-counterproposal exchange with dynamic concession formula $\alpha(t) = P_{\text{min}} + (P_{\text{max}} - P_{\text{min}}) \cdot (t / T_{\text{max}})^2$.
  - Consensus Handshake Termination (1.5 Marks): Convergence to agreement within reservation threshold and emission of signed handshake payload.

### Assignment 3.2: Self-Interested Agent Utility Optimization
- **Rubrics Checklist (5 Marks)**:
  - Utility Evaluation Equation Logic (2 Marks): Explicit multi-term utility formula weighing skill gain, career relevance, cost, and time commitment.
  - Optimization Search Algorithm Implementation (2 Marks): Evaluates all 10 candidate bundles, enforces budget & time constraints, and returns ranked utility scores.
  - Error/Constraint Boundary Resilience (1 Mark): Gracefully flags infeasible configurations exceeding budget or available hours.

---

## 4. Implementation Plan

1. **Backend Agent Modules**:
   - `CareerAI/backend/app/agent/reflex_reasoner.py`
   - `CareerAI/backend/app/agent/daemon_worker.py`
   - `CareerAI/backend/app/agent/socket_messaging.py`
   - `CareerAI/backend/app/agent/negotiation_protocol.py`
   - `CareerAI/backend/app/agent/utility_optimizer.py`
2. **Backend API Endpoints**:
   - `CareerAI/backend/app/api/routes_assignments.py` (mounted at `/api/v1/assignments`)
3. **Standalone Console Scripts**:
   - `CareerAI/backend/assignments/assignment_1_2_reflex_agent.py`
   - `CareerAI/backend/assignments/assignment_2_1_daemon_worker.py`
   - `CareerAI/backend/assignments/assignment_2_2_socket_messaging.py`
   - `CareerAI/backend/assignments/assignment_3_1_negotiation.py`
   - `CareerAI/backend/assignments/assignment_3_2_utility_optimizer.py`
   - `CareerAI/backend/assignments/run_all_assignments.py`
4. **Automated Test Suite**:
   - `CareerAI/backend/tests/test_assignments.py`
5. **Interactive Frontend Lab**:
   - `CareerAI/frontend/src/pages/AgentLabPage.jsx`
   - Navigation link in `Navbar.jsx`
   - Centralized API methods in `api.js`
