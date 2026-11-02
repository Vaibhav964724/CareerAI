# CareerAI - Agent Technology Assignments Demonstration Guide

This guide provides step-by-step instructions for demonstrating all five university **Agent Technology** assignments integrated into **CareerAI**.

You can demonstrate each assignment either:
1. **Interactively via the Web UI** using the **Agent Technology Lab** tab.
2. **Via Standalone Terminal Console Scripts** for deterministic command-line verification.

---

## Quick Reference Summary

| Assignment | Course Unit | Concept | Web UI Route | Terminal CLI Command |
|---|---|---|---|---|
| **1.2** | Unit 1 | Rule-Based Simple Reflex Agent | Agent Lab &rarr; 1.2 Reflex Reasoner | `python assignments/assignment_1_2_reflex_agent.py` |
| **2.1** | Unit 2 | Concurrent Task Daemonization | Agent Lab &rarr; 2.1 Task Daemon | `python assignments/assignment_2_1_daemon_worker.py` |
| **2.2** | Unit 2 | Distributed Socket Messaging | Agent Lab &rarr; 2.2 Socket Mesh | `python assignments/assignment_2_2_socket_messaging.py` |
| **3.1** | Unit 3 | Multi-Agent Negotiation Protocol | Agent Lab &rarr; 3.1 Multi-Agent | `python assignments/assignment_3_1_negotiation.py` |
| **3.2** | Unit 3 | Utility Optimization (10 Options) | Agent Lab &rarr; 3.2 Utility Optimizer | `python assignments/assignment_3_2_utility_optimizer.py` |

---

## 1. One-Click Batch Test Runner

To execute all 5 assignments in sequence and generate a unified terminal report:

```bash
cd backend
python assignments/run_all_assignments.py
```

**Expected Result:**
```
======================================================================================
                     CONSOLIDATED EXECUTION SUMMARY REPORT
======================================================================================
Assignment ID      | Description                                | Status     | Duration
--------------------------------------------------------------------------------------
Assignment 1.2     | Rule-Based Environmental Reasoner (Unit-1) | PASS       | 3.89s
Assignment 2.1     | Concurrent Task Daemonization (Unit-2)     | PASS       | 6.50s
Assignment 2.2     | Distributed Agent Sockets (Unit-2)         | PASS       | 2.95s
Assignment 3.1     | Multi-Agent Coordination Protocol (Unit-3) | PASS       | 2.60s
Assignment 3.2     | Self-Interested Utility Optimizer (Unit-3) | PASS       | 3.85s
--------------------------------------------------------------------------------------
Final Score: 5/5 Assignments Executed Successfully.
======================================================================================
```

To run the automated pytest suite:
```bash
cd backend
pytest tests/test_assignments.py -v
```

---

## 2. Assignment 1.2: Rule-Based Environmental Reasoner

### Objective
Demonstrate a **Simple Reflex Agent** implementing explicit **Condition-Action production rules** over dynamic sensory telemetry without internal state history.

### Demonstrating via Web UI
1. Navigate to **Agent Lab** in the navigation bar.
2. Select the **1.2 Reflex Reasoner** tab.
3. Choose the packet count (e.g., 6 frames) and click **"Inject Telemetry Stream"**.
4. Observe:
   - Dynamic telemetry attributes: Study Hours, Burnout Index, and Market Surge.
   - Severity tags: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
   - Condition matches: `RULE_01_MARKET_DEMAND_SURGE`, `RULE_02_SCHEDULE_COMPRESSION`, `RULE_03_BURNOUT_GUARD`, etc.
   - Immediate reactive action recommendations fired by the agent.

### Demonstrating via CLI
```bash
cd backend
python assignments/assignment_1_2_reflex_agent.py
```

### Viva / Examiner Q&A
- **Q:** *Why is this a Simple Reflex Agent?*
  **A:** Because decisions are computed directly from the current sensory percept $f(P) \to A$ using condition-action production rules without searching deep future state trees or relying on complex internal state memory.
- **Q:** *How are conflicting rules resolved?*
  **A:** Rules have explicit priority tiers (`priority=10` down to `priority=6`). The highest-priority satisfied condition is selected first.

---

## 3. Assignment 2.1: Concurrent Task Daemonization

### Objective
Demonstrate multi-threading in agent architectures by running an asynchronous background daemon thread (`daemon=True`) that continuously monitors milestone deadlines and computes latency without freezing the web interface.

### Demonstrating via Web UI
1. Select the **2.1 Task Daemon** tab in the Agent Lab.
2. Click **"Start Daemon Worker"**.
3. Observe:
   - The green animated pulsing status (`RUNNING`).
   - The real-time cycle counter incrementing every 1.5 seconds.
   - Cycle latency in milliseconds (typically 0.15ms to 2.5ms).
   - Thread-safe invariance confirmation mediated by `threading.Lock`.
4. Click **"Stop Daemon Worker"** to confirm clean graceful termination.

### Demonstrating via CLI
```bash
cd backend
python assignments/assignment_2_1_daemon_worker.py
```

### Viva / Examiner Q&A
- **Q:** *Why must the background worker be a daemon thread?*
  **A:** A daemon thread automatically terminates when the main Python runtime shuts down, preventing dangling or orphaned processes that hold locks or ports open.
- **Q:** *How do you guarantee thread safety?*
  **A:** Metrics updates and state snapshots are wrapped in Python's reentrant lock `threading.Lock()`, ensuring atomic reads/writes between the daemon and FastAPI web requests.

---

## 4. Assignment 2.2: Distributed Socket Messaging

### Objective
Demonstrate distributed multi-node agent communication across raw TCP sockets using serialized JSON frames with a 4-byte length prefix transport protocol.

### Demonstrating via Web UI
1. Select the **2.2 Socket Mesh** tab in the Agent Lab.
2. Review or customize the target TCP port (e.g., 9124) and student parameters.
3. Click **"Transmit Socket Frame"**.
4. Observe:
   - The TCP wire audit trail showing socket binding, connection handshake, and byte payload transmission.
   - Agent-B (Placement Node) autonomously evaluating student eligibility.
   - Candidate classification (e.g. `Gold Candidate` or `Silver Candidate`).
   - Digital cryptographic handshake signature (e.g. `SIG-AGENT-B-XXXXXX`).
   - Round-trip transmission latency in milliseconds.

### Demonstrating via CLI
```bash
cd backend
python assignments/assignment_2_2_socket_messaging.py
```

### Viva / Examiner Q&A
- **Q:** *Why is length-prefix framing used instead of raw delimiters?*
  **A:** TCP is a continuous byte stream without packet boundaries. Prepending a 4-byte big-endian integer (`struct.pack("!I", length)`) ensures the receiving socket knows exactly how many payload bytes to read before deserializing JSON, preventing fragmentation bugs.

---

## 5. Assignment 3.1: Multi-Agent Negotiation Protocol

### Objective
Demonstrate a multi-agent coordination protocol (Contract Net / Bidding) between two self-interested agents (`StudentAgent` and `RecruiterAgent`) that exchange proposals using time-dependent utility concession curves until reaching consensus.

### Demonstrating via Web UI
1. Select the **3.1 Multi-Agent** tab in the Agent Lab.
2. Adjust the sliders:
   - Student Target Stipend (e.g., \$2,200/mo)
   - Recruiter Budget Ceiling (e.g., \$2,400/mo)
   - Max Negotiation Turns (e.g., 6)
3. Click **"Execute Negotiation"**.
4. Observe:
   - Turn-by-turn bidding cards showing proposal terms: Monthly Stipend, Weekly Hours, Mentorship Sessions.
   - Dual utility calculations for both agents at each turn ($U_{\text{student}}$ and $U_{\text{recruiter}}$).
   - Consensus outcome with agreement details and SHA-256 agreement signature.

### Demonstrating via CLI
```bash
cd backend
python assignments/assignment_3_1_negotiation.py
```

### Viva / Examiner Q&A
- **Q:** *How does concession work in this negotiation?*
  **A:** Each agent uses a time-dependent polynomial concession function $\alpha(t) = P_{\text{min}} + (P_{\text{max}} - P_{\text{min}}) \cdot (t / T_{\text{max}})^k$. As time elapses ($t \to T_{\text{max}}$), agents concede toward the opponent's reservation threshold until utilities overlap.

---

## 6. Assignment 3.2: Self-Interested Agent Utility Optimization

### Objective
Demonstrate Multi-Attribute Utility Theory (MAUT) by formulating an explicit mathematical objective function $U(x)$, evaluating 10 complex resource bundles, enforcing hard budget and time constraints, and selecting the global optimum.

### Demonstrating via Web UI
1. Select the **3.2 Utility Optimizer** tab in the Agent Lab.
2. Adjust constraints and weights:
   - Budget Limit (\$160)
   - Weekly Time Limit (18h/week)
   - Attribute Weights (Skill $w_1$, Relevance $w_2$, Prestige $w_3$)
3. Click **"Compute Optimal Utility"**.
4. Observe:
   - The Global Maximum Winner card highlighted in green with its Net Utility score $U(x)$.
   - The full breakdown table of all 10 candidates.
   - Automatic identification and rejection of infeasible options exceeding budget or time constraints (e.g., OPT-06 and OPT-10).

### Demonstrating via CLI
```bash
cd backend
python assignments/assignment_3_2_utility_optimizer.py
```

### Viva / Examiner Q&A
- **Q:** *What is the mathematical formulation of the utility function?*
  **A:**
  $$U(x) = \left( w_1 \cdot \text{Skill}(x) + w_2 \cdot \text{Relevance}(x) + w_3 \cdot \text{Prestige}(x) \right) - \left( c_1 \cdot \text{CostNorm}(x) + c_2 \cdot \text{TimeNorm}(x) + c_3 \cdot \text{DiffNorm}(x) \right)$$
  Subject to:
  $$\text{Cost}(x) \le B_{\text{max}} \quad \text{and} \quad \text{Time}(x) \le T_{\text{max}}$$
