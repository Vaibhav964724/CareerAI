"""
Generates high-resolution architecture diagrams for Assignments 4.1, 4.2, 5.1, and 5.2
using PIL (Pillow) with professional typography, color palettes, and container boxes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIRS = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "Assignment_4_1_BDI")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "Assignment_4_2_Knowledge_API")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "Assignment_5_1_Agent_Security")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "Assignment_5_2_Capstone")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "assignments", "Assignment_4.1_BDI")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "assignments", "Assignment_4.2_Knowledge_API")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "assignments", "Assignment_5.1_Agent_Security")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "submission", "assignments", "Assignment_5.2_Capstone"))
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)


def get_font(size: int, bold: bool = False):
    try:
        font_path = "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf"
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
        font_path_alt = "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
        if os.path.exists(font_path_alt):
            return ImageFont.truetype(font_path_alt, size)
    except Exception:
        pass
    return ImageFont.load_default()


def create_bdi_diagram():
    width, height = 1400, 850
    img = Image.new("RGB", (width, height), (15, 23, 42))  # slate-900
    draw = ImageDraw.Draw(img)

    # Title Banner
    draw.rectangle([(40, 30), (width - 40, 110)], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.text((60, 42), "CAREERAI - BDI (BELIEF-DESIRE-INTENTION) COGNITIVE ARCHITECTURE", fill=(255, 255, 255), font=get_font(26, True))
    draw.text((60, 78), "Assignment 4.1 | Course: Agent Technology (Unit-4) | Student: Vaibhav Singh (RA2212704010040)", fill=(148, 163, 184), font=get_font(15, False))

    # Box 1: Sensory Percept Ingestion
    draw.rounded_rectangle([(60, 150), (380, 430)], radius=12, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    draw.text((80, 170), "1. SENSORY PERCEPTION", fill=(56, 189, 248), font=get_font(18, True))
    draw.text((80, 200), "Sensory Percept Ingestion:", fill=(203, 213, 225), font=get_font(14, True))
    lines1 = [
        "- Student Telemetry Stream",
        "- Weekly Available Study Hours",
        "- Burnout / Fatigue Index (0-100)",
        "- Target Career Role Specification",
        "- Exam Deadlines & Pacing Signals",
        "- Market Demand Surge Percepts"
    ]
    for i, l in enumerate(lines1):
        draw.text((80, 230 + i * 28), l, fill=(148, 163, 184), font=get_font(13))

    # Box 2: Belief Base (BeliefBase)
    draw.rounded_rectangle([(420, 150), (740, 430)], radius=12, fill=(30, 41, 59), outline=(168, 85, 247), width=2)
    draw.text((440, 170), "2. BELIEF BASE (Knowledge)", fill=(168, 85, 247), font=get_font(18, True))
    draw.text((440, 200), "Internal World State:", fill=(203, 213, 225), font=get_font(14, True))
    lines2 = [
        "- Belief(weekly_study_hours: 14.0h)",
        "- Belief(burnout_index: 20.0%)",
        "- Belief(target_role: Full Stack)",
        "- Belief(days_to_deadline: 45)",
        "- Reactive Change Listeners",
        "- State Snapshot Query Engine"
    ]
    for i, l in enumerate(lines2):
        draw.text((440, 230 + i * 28), l, fill=(148, 163, 184), font=get_font(13))

    # Box 3: Desire Manager
    draw.rounded_rectangle([(780, 150), (1060, 430)], radius=12, fill=(30, 41, 59), outline=(245, 158, 11), width=2)
    draw.text((800, 170), "3. DESIRE MANAGER", fill=(245, 158, 11), font=get_font(18, True))
    draw.text((800, 200), "Candidate Goals Evaluated:", fill=(203, 213, 225), font=get_font(14, True))
    lines3 = [
        "- DESIRE_BURNOUT_GUARD (P: 100)",
        "- DESIRE_CRITICAL_SCHEDULE (P: 80)",
        "- DESIRE_CAPSTONE_ACCEL (P: 50)",
        "- DESIRE_RESOLVE_SKILL_GAPS (P: 7)",
        "- Trigger & Satisfaction Predicates",
        "- Dominance Utility Selection"
    ]
    for i, l in enumerate(lines3):
        draw.text((800, 230 + i * 28), l, fill=(148, 163, 184), font=get_font(13))

    # Box 4: Plan Selector & Intention
    draw.rounded_rectangle([(1100, 150), (1340, 430)], radius=12, fill=(30, 41, 59), outline=(34, 197, 94), width=2)
    draw.text((1120, 170), "4. INTENTION PLANNER", fill=(34, 197, 94), font=get_font(18, True))
    draw.text((1120, 200), "Committed Plans:", fill=(203, 213, 225), font=get_font(14, True))
    lines4 = [
        "- PlanSelector Recipes",
        "- Intensive Deep Dive",
        "- Balanced Modular Plan",
        "- Reduced-Load Recovery",
        "- Accelerated Capstone",
        "- Step Pointer Dispatch"
    ]
    for i, l in enumerate(lines4):
        draw.text((1120, 230 + i * 28), l, fill=(148, 163, 184), font=get_font(13))

    # Arrows between top boxes
    draw.line([(380, 290), (420, 290)], fill=(56, 189, 248), width=3)
    draw.line([(740, 290), (780, 290)], fill=(168, 85, 247), width=3)
    draw.line([(1060, 290), (1100, 290)], fill=(245, 158, 11), width=3)

    # Bottom Container: Dynamic Intention Shift Engine (The Belief Shock Reconsideration Loop)
    draw.rounded_rectangle([(60, 470), (1340, 780)], radius=14, fill=(15, 23, 42), outline=(239, 68, 68), width=3)
    draw.text((90, 490), "DYNAMIC INTENTION RECONSIDERATION ENGINE (Rao & Georgeff Deliberation Loop)", fill=(239, 68, 68), font=get_font(20, True))

    # Step A: Unexpected Shock
    draw.rounded_rectangle([(90, 540), (440, 750)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((110, 555), "A. Environmental Shock", fill=(255, 255, 255), font=get_font(16, True))
    draw.text((110, 590), "Percept Update Mid-Execution:", fill=(148, 163, 184), font=get_font(13))
    draw.text((110, 615), "- Student hours collapse (14.0h -> 4.0h)", fill=(239, 68, 68), font=get_font(13))
    draw.text((110, 640), "- Stress / Fatigue surges (20% -> 85%)", fill=(239, 68, 68), font=get_font(13))
    draw.text((110, 675), "Calls update_belief_and_reconsider()", fill=(56, 189, 248), font=get_font(13, True))

    # Step B: Precondition Check
    draw.rounded_rectangle([(480, 540), (870, 750)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((500, 555), "B. Viability & Conflict Check", fill=(255, 255, 255), font=get_font(16, True))
    draw.text((500, 590), "1. is_viable(beliefs) evaluated:", fill=(148, 163, 184), font=get_font(13))
    draw.text((520, 615), "-> Precondition Violated! (4.0h < 12.0h)", fill=(239, 68, 68), font=get_font(13))
    draw.text((500, 645), "2. Dominant Goal Check:", fill=(148, 163, 184), font=get_font(13))
    draw.text((520, 670), "-> DESIRE_BURNOUT_GUARD activated!", fill=(245, 158, 11), font=get_font(13))
    draw.text((500, 705), "Action: Abort Current Plan & Log Shift", fill=(203, 213, 225), font=get_font(13, True))

    # Step C: Dynamic Plan Shift
    draw.rounded_rectangle([(910, 540), (1310, 750)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((930, 555), "C. Dynamic Intention Shift", fill=(34, 197, 94), font=get_font(16, True))
    draw.text((930, 590), "Procedural Plan Adaptation:", fill=(148, 163, 184), font=get_font(13))
    draw.text((930, 615), "- Abort: Intensive Deep Dive Plan", fill=(239, 68, 68), font=get_font(13))
    draw.text((930, 640), "- Commit: Reduced-Load Recovery Plan", fill=(34, 197, 94), font=get_font(13, True))
    draw.text((930, 665), "- Inject: Rest day pacing buffer", fill=(203, 213, 225), font=get_font(13))
    draw.text((930, 690), "- Shift Record saved to audit history", fill=(168, 85, 247), font=get_font(13))
    draw.text((930, 715), "- Execution resumes without agent crash", fill=(56, 189, 248), font=get_font(13))

    # Connector lines
    draw.line([(440, 645), (480, 645)], fill=(239, 68, 68), width=3)
    draw.line([(870, 645), (910, 645)], fill=(34, 197, 94), width=3)

    return img


def create_knowledge_api_diagram():
    width, height = 1400, 850
    img = Image.new("RGB", (width, height), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Title Banner
    draw.rectangle([(40, 30), (width - 40, 110)], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.text((60, 42), "CAREERAI - KNOWLEDGE REPRESENTATION & ADAPTIVE REST API INTEGRATION", fill=(255, 255, 255), font=get_font(26, True))
    draw.text((60, 78), "Assignment 4.2 | Course: Agent Technology (Unit-4) | Student: Vaibhav Singh (RA2212704010040)", fill=(148, 163, 184), font=get_font(15, False))

    # Left Container: Domain Ontology
    draw.rounded_rectangle([(60, 150), (460, 780)], radius=14, fill=(30, 41, 59), outline=(6, 182, 212), width=2)
    draw.text((80, 170), "DOMAIN ONTOLOGY (career_ontology.json)", fill=(6, 182, 212), font=get_font(18, True))
    draw.text((80, 205), "Structured Semantic Knowledge Base:", fill=(203, 213, 225), font=get_font(14, True))
    lines_ont = [
        "* Roles Hierarchy (Tier-1 / Tier-2)",
        "  - Full Stack Engineer",
        "  - Machine Learning Engineer",
        "  - Cloud & DevOps Engineer",
        "  - Data Analyst / BI Specialist",
        "",
        "* Prerequisite Dependency Trees:",
        "  - FastAPI -> [Python, REST APIs]",
        "  - React -> [JavaScript, HTML/CSS]",
        "  - PyTorch -> [Python, Linear Algebra]",
        "  - Docker -> [Linux, CLI]",
        "  - Microservices -> [FastAPI, Docker]",
        "",
        "* Bloom's Taxonomy Scale (Levels 1-5)",
        "  - 1: Remember / Syntax",
        "  - 3: Apply / Implementation",
        "  - 5: Evaluate / Enterprise Architect",
        "",
        "* Verification via check_prerequisites_satisfied()"
    ]
    for i, l in enumerate(lines_ont):
        draw.text((80, 240 + i * 24), l, fill=(148, 163, 184), font=get_font(13))

    # Middle Container: Real External REST API Client
    draw.rounded_rectangle([(500, 150), (900, 780)], radius=14, fill=(30, 41, 59), outline=(168, 85, 247), width=2)
    draw.text((520, 170), "REAL EXTERNAL REST API INTEGRATION", fill=(168, 85, 247), font=get_font(18, True))
    draw.text((520, 205), "ExternalCareerAPIClient (GitHub API):", fill=(203, 213, 225), font=get_font(14, True))
    lines_api = [
        "* HTTP GET /search/repositories",
        "  Endpoint: api.github.com/search/repositories",
        "  Headers: Accept: application/vnd.github.v3+json",
        "  Query: q={skill}+topic:curriculum&sort=stars",
        "",
        "* Network Resilience & Provenance Handling:",
        "  - 5.0s Strict Network Timeout Safety",
        "  - In-flight Network Exception Interception",
        "  - Curated Fallback Fixture with Tagging:",
        "    - Provenance: LIVE_GITHUB_API",
        "    - Provenance: CURATED_KNOWLEDGE_MAP",
        "",
        "* Unstructured Response Parsing:",
        "  - Repository Title & Namespace",
        "  - Community Star Popularity Metric",
        "  - Open Source License Identification",
        "  - Direct Upstream Source Hyperlinks",
        "  - Structured LiveKnowledgeResource Objects"
    ]
    for i, l in enumerate(lines_api):
        draw.text((520, 240 + i * 24), l, fill=(148, 163, 184), font=get_font(13))

    # Right Container: Adaptive Knowledge Service (Plan Adaptation)
    draw.rounded_rectangle([(940, 150), (1340, 780)], radius=14, fill=(30, 41, 59), outline=(34, 197, 94), width=2)
    draw.text((960, 170), "ADAPTIVE ROADMAP PLAN SYNTHESIS", fill=(34, 197, 94), font=get_font(18, True))
    draw.text((960, 205), "AdaptiveKnowledgeService Output:", fill=(203, 213, 225), font=get_font(14, True))
    lines_syn = [
        "* Input Context:",
        "  - Student: Vaibhav Singh (RA2212704010040)",
        "  - Target Role: Full Stack Engineer",
        "  - Skill Gap: FastAPI (Prereqs Verified: True)",
        "",
        "* Live Enriched Capstone Milestone:",
        "  - Title: Production Implementation: FastAPI",
        "  - Difficulty: ADVANCED (>50,000 community stars)",
        "  - Community Project: fastapi/fastapi",
        "  - Stars: 104,258 Stars",
        "  - License: MIT License",
        "  - URL: https://github.com/fastapi/fastapi",
        "",
        "* Dynamic Adaptation Rationale:",
        "  Injected real-world GitHub repository into",
        "  student roadmap based on live popularity",
        "  telemetry and verified prerequisite mastery."
    ]
    for i, l in enumerate(lines_syn):
        draw.text((960, 240 + i * 24), l, fill=(148, 163, 184), font=get_font(13))

    # Inter-container connectors
    draw.line([(460, 465), (500, 465)], fill=(6, 182, 212), width=3)
    draw.line([(900, 465), (940, 465)], fill=(168, 85, 247), width=3)

    return img


def create_security_diagram():
    width, height = 1400, 850
    img = Image.new("RGB", (width, height), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Title Banner
    draw.rectangle([(40, 30), (width - 40, 110)], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.text((60, 42), "CAREERAI - AGENT AUTHENTICATION & HOST INTEGRITY VERIFICATION", fill=(255, 255, 255), font=get_font(26, True))
    draw.text((60, 78), "Assignment 5.1 | Course: Agent Technology (Unit-5) | Student: Vaibhav Singh (RA2212704010040)", fill=(148, 163, 184), font=get_font(15, False))

    # Top Box: Cryptographic Signed Envelope Architecture
    draw.rounded_rectangle([(60, 150), (1340, 370)], radius=14, fill=(30, 41, 59), outline=(244, 63, 94), width=2)
    draw.text((80, 170), "1. CRYPTOGRAPHIC SIGNED ENVELOPE FORMAT & 5-POINT SECURITY CHECKPOINT", fill=(244, 63, 94), font=get_font(18, True))
    
    # 5 security checkpoints
    cols = [
        ("Checkpoint 1", "Schema Integrity", "Enforces presence of host_id, sender_id, timestamp, nonce, action, payload, signature"),
        ("Checkpoint 2", "Host Authentication", "Verifies host_id in registered trusted hosts catalog with matching sender identity"),
        ("Checkpoint 3", "Timestamp Freshness", "Rejects clock-skew or expired envelopes exceeding tolerance window (300.0s)"),
        ("Checkpoint 4", "Sliding Nonce Cache", "Prevents duplicate command re-transmission via in-memory revoked nonce cache"),
        ("Checkpoint 5", "HMAC-SHA256 Sig", "Constant-time hmac.compare_digest() over canonical JSON serialized payload")
    ]
    for i, (cp, title, desc) in enumerate(cols):
        x1 = 80 + i * 248
        x2 = x1 + 235
        draw.rounded_rectangle([(x1, 210), (x2, 350)], radius=8, fill=(15, 23, 42), outline=(71, 85, 105), width=1)
        draw.text((x1 + 10, 220), cp, fill=(244, 63, 94), font=get_font(13, True))
        draw.text((x1 + 10, 240), title, fill=(255, 255, 255), font=get_font(13, True))
        # Word wrap description
        words = desc.split(" ")
        line = ""
        y_off = 265
        for w in words:
            if len(line + " " + w) > 28:
                draw.text((x1 + 10, y_off), line, fill=(148, 163, 184), font=get_font(11))
                y_off += 18
                line = w
            else:
                line += " " + w if line else w
        if line:
            draw.text((x1 + 10, y_off), line, fill=(148, 163, 184), font=get_font(11))

    # Bottom Area: 3 Attack Simulations & Mitigations
    draw.rounded_rectangle([(60, 410), (1340, 780)], radius=14, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    draw.text((80, 430), "2. HOSTILE INTRUSION VECTOR SIMULATION & VERIFIED BLOCKED AUDIT TRAILS", fill=(56, 189, 248), font=get_font(18, True))

    attacks = [
        (
            "ATTACK VECTOR 1: TAMPERED PAYLOAD",
            "Man-in-the-Middle (MITM) Alteration",
            "Adversary intercepts in-flight packet and alters student GPA from 3.75 to 4.00 without possessing host secret key.",
            "Defense: HMAC digest recalculated over canonical JSON. Digest mismatch detected. Blocked with ERR_SIGNATURE_TAMPERED.",
            (239, 68, 68)
        ),
        (
            "ATTACK VECTOR 2: UNTRUSTED ROGUE HOST",
            "Host Identity Impersonation",
            "Attacker submits payload originating from unregistered rogue host identity 'ROGUE_EXTERNAL_SPOOFER_NODE_01'.",
            "Defense: HostAuthenticator checks registered trusted hosts ACL. Unregistered identity blocked with ERR_UNTRUSTED_HOST.",
            (245, 158, 11)
        ),
        (
            "ATTACK VECTOR 3: REPLAY ATTACK",
            "Duplicate Nonce Retransmission",
            "Attacker intercepts an authentic valid signed envelope and replays it verbatim across network wire.",
            "Defense: Nonce cache detects collision for already consumed nonce token. Blocked with ERR_REPLAY_DETECTED.",
            (168, 85, 247)
        )
    ]

    for i, (title, sub, scenario, defense, color) in enumerate(attacks):
        x1 = 80 + i * 415
        x2 = x1 + 400
        draw.rounded_rectangle([(x1, 470), (x2, 750)], radius=10, fill=(30, 41, 59), outline=color, width=2)
        draw.text((x1 + 15, 485), title, fill=color, font=get_font(14, True))
        draw.text((x1 + 15, 510), sub, fill=(255, 255, 255), font=get_font(12, True))

        draw.text((x1 + 15, 540), "Scenario:", fill=(203, 213, 225), font=get_font(12, True))
        draw.text((x1 + 15, 560), scenario[:50], fill=(148, 163, 184), font=get_font(11))
        draw.text((x1 + 15, 578), scenario[50:105], fill=(148, 163, 184), font=get_font(11))
        draw.text((x1 + 15, 596), scenario[105:], fill=(148, 163, 184), font=get_font(11))

        draw.text((x1 + 15, 630), "Security Response:", fill=(203, 213, 225), font=get_font(12, True))
        draw.text((x1 + 15, 650), defense[:50], fill=(34, 197, 94), font=get_font(11, True))
        draw.text((x1 + 15, 668), defense[50:105], fill=(34, 197, 94), font=get_font(11, True))
        draw.text((x1 + 15, 686), defense[105:], fill=(34, 197, 94), font=get_font(11, True))

        draw.text((x1 + 15, 715), "[STATUS: INTRUSION BLOCKED & LOGGED]", fill=color, font=get_font(12, True))

    return img


def create_system_architecture_diagram():
    width, height = 1400, 900
    img = Image.new("RGB", (width, height), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Title Banner
    draw.rectangle([(40, 25), (width - 40, 105)], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.text((60, 36), "CAREERAI - CAPSTONE INTEGRATED MASTER AGENT SYSTEM ARCHITECTURE", fill=(255, 255, 255), font=get_font(26, True))
    draw.text((60, 72), "Assignment 5.2 | End-to-End Autonomous Pipeline Unifying Units 1-5 | Vaibhav Singh (RA2212704010040)", fill=(148, 163, 184), font=get_font(15, False))

    # Grid of 5 Units
    units = [
        ("UNIT 1: CORE REFLEX", "Condition-Action Production Rules", ["ReflexEnvironmentalReasoner", "5 Prioritized Condition Rules", "Sensory Telemetry Ingestion", "Fast 0.05ms Reflex Dispatch"], (56, 189, 248)),
        ("UNIT 2: CONCURRENCY & SOCKETS", "Task Daemon & Distributed Mesh", ["CareerMonitorDaemon (Thread)", "Sliding Lock Guard Safety", "Dual-Agent TCP Wire Frame", "SocketAgentA / SocketAgentB"], (168, 85, 247)),
        ("UNIT 3: COOPERATION & UTILITY", "Negotiation & MAUT Optimization", ["MultiAgentNegotiator (6 Turns)", "Contract Net Bidding Protocol", "MultiAttributeUtilityOptimizer", "10 Resource Bundles Scored"], (245, 158, 11)),
        ("UNIT 4: BDI & LIVE API", "Cognitive Loop & External Data", ["BDICognitiveAgent State Machine", "Dynamic Intention Shift Logic", "CareerOntologyEngine (JSON)", "ExternalCareerAPIClient (GitHub)"], (34, 197, 94)),
        ("UNIT 5: CRYPTOGRAPHIC SECURITY", "HMAC Signatures & Host Integrity", ["CryptographicSignatureManager", "HostAuthenticator 5-Pt Check", "Nonce Replay Defense Cache", "SecureCommandHandler Dispatch"], (244, 63, 94))
    ]

    for i, (u_title, u_sub, bullet_pts, col) in enumerate(units):
        x1 = 50 + i * 262
        x2 = x1 + 250
        draw.rounded_rectangle([(x1, 135), (x2, 430)], radius=12, fill=(30, 41, 59), outline=col, width=2)
        draw.text((x1 + 12, 150), u_title, fill=col, font=get_font(13, True))
        draw.text((x1 + 12, 172), u_sub, fill=(255, 255, 255), font=get_font(11, True))
        for j, b in enumerate(bullet_pts):
            draw.text((x1 + 12, 210 + j * 32), f"- {b}", fill=(148, 163, 184), font=get_font(11))

    # Bottom Master Orchestrator Container (CapstoneConsolidatedAgent)
    draw.rounded_rectangle([(50, 460), (width - 50, 860)], radius=14, fill=(15, 23, 42), outline=(245, 158, 11), width=3)
    draw.text((80, 480), "CONSOLIDATED 10-STAGE PRODUCTION EXECUTION PIPELINE (CapstoneConsolidatedAgent)", fill=(245, 158, 11), font=get_font(20, True))

    stages = [
        ("[01] Security Verification", "Unit 5: Cryptographic envelope & HMAC verification", (244, 63, 94)),
        ("[02] Sensory Perception", "Unit 1: Environmental telemetry parsing & reflex conditioning", (56, 189, 248)),
        ("[03] BDI Goal Deliberation", "Unit 4: Belief ingestion, desire evaluation, intention binding", (34, 197, 94)),
        ("[04] Ontology & Live API", "Unit 4: Formal prerequisite check & live GitHub API fetch", (6, 182, 212)),
        ("[05] Operational Dispatch", "Unit 4: Discrete action step execution & audit logging", (34, 197, 94)),
        ("[06] Dynamic Intention Shift", "Unit 4: Environmental shock recalculation & recovery plan commit", (239, 68, 68)),
        ("[07] Utility Optimization", "Unit 3: MAUT multi-attribute bundle evaluation (10 options)", (245, 158, 11)),
        ("[08] Daemon Health Check", "Unit 2: Background worker thread monitoring & lock validation", (168, 85, 247)),
        ("[09] TCP Socket Mesh Sync", "Unit 2: Dual-agent wire-frame readiness score handshake", (168, 85, 247)),
        ("[10] Multi-Agent Negotiation", "Unit 3: Contract Net placement stipend consensus protocol", (245, 158, 11))
    ]

    for i, (stg_name, stg_desc, stg_col) in enumerate(stages):
        col_idx = i % 2
        row_idx = i // 2
        x1 = 80 + col_idx * 630
        x2 = x1 + 610
        y1 = 530 + row_idx * 60
        y2 = y1 + 50

        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=8, fill=(30, 41, 59), outline=stg_col, width=1)
        draw.text((x1 + 15, y1 + 8), stg_name, fill=stg_col, font=get_font(13, True))
        draw.text((x1 + 15, y1 + 28), stg_desc, fill=(148, 163, 184), font=get_font(11))
        draw.text((x2 - 80, y1 + 16), "PASSED", fill=(34, 197, 94), font=get_font(12, True))

    return img


def main():
    print("Generating diagrams...")
    bdi_img = create_bdi_diagram()
    knowledge_img = create_knowledge_api_diagram()
    security_img = create_security_diagram()
    system_img = create_system_architecture_diagram()

    # Save to all target submission directories
    for d in OUTPUT_DIRS:
        if "4_1" in d or "4.1" in d:
            bdi_img.save(os.path.join(d, "BDI_Architecture.png"), "PNG")
            print(f"Saved: {os.path.join(d, 'BDI_Architecture.png')}")
        elif "4_2" in d or "4.2" in d:
            knowledge_img.save(os.path.join(d, "Knowledge_API_Architecture.png"), "PNG")
            print(f"Saved: {os.path.join(d, 'Knowledge_API_Architecture.png')}")
        elif "5_1" in d or "5.1" in d:
            security_img.save(os.path.join(d, "Security_Architecture.png"), "PNG")
            print(f"Saved: {os.path.join(d, 'Security_Architecture.png')}")
        elif "5_2" in d or "5.2" in d:
            system_img.save(os.path.join(d, "System_Architecture.png"), "PNG")
            print(f"Saved: {os.path.join(d, 'System_Architecture.png')}")

    print("All architecture diagrams successfully generated.")


if __name__ == "__main__":
    main()
