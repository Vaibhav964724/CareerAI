import React, { useState } from 'react';
import {
  Compass,
  ArrowRight,
  Target,
  Sparkles,
  Cpu,
  Layers,
  Database,
  CheckCircle2,
  Calendar,
  Clock,
  ShieldCheck,
  TrendingUp,
  Bot,
  Play,
  RotateCw,
  Sliders,
  Check,
  AlertCircle
} from 'lucide-react';

export default function LandingPage({ setActiveTab, currentStudent }) {
  const [selectedStage, setSelectedStage] = useState(0);
  const [demoScenario, setDemoScenario] = useState('hours_changed');

  const steps = [
    {
      step: 1,
      id: "OBSERVE",
      name: "Observe",
      icon: Database,
      tagline: "Persistent Context Retrieval",
      shortDesc: "Gathers student state, skill levels, and active roadmap from SQLite.",
      input: "Student profile #{id}, skill matrix [0–5], roadmap version, study hours/week",
      tool: "fetch_student_context()",
      transformation: "Constructs normalized observation snapshot with chronological audit timestamp.",
      invariant: "Idempotent read: Zero mutations allowed during observation phase."
    },
    {
      step: 2,
      id: "REASON",
      name: "Reason",
      icon: Target,
      tagline: "Deterministic Gap & Blocker Logic",
      shortDesc: "Calculates gaps (Target - Current) and validates prerequisite chains.",
      input: "Target role benchmark, prerequisite dependency graph, milestone completion flags",
      tool: "analyze_skill_gaps() + detect_blockers()",
      transformation: "Classifies gaps into Critical/High/Medium priorities and identifies bottlenecks.",
      invariant: "Soundness: Gap = max(0, Target - Current). Never suggests negative values."
    },
    {
      step: 3,
      id: "PLAN",
      name: "Plan",
      icon: Calendar,
      tagline: "Adaptive Milestone Sequencing",
      shortDesc: "Synthesizes milestone phases based on weekly study capacity.",
      input: "Unmet skill gaps, available weekly study hours, target completion deadline",
      tool: "synthesize_roadmap_plan()",
      transformation: "Orders learning objectives into Phase 1 (Foundations) through Phase 3 (Projects).",
      invariant: "Feasibility: Milestone hours match student weekly study budget."
    },
    {
      step: 4,
      id: "ACT",
      name: "Act",
      icon: Cpu,
      tagline: "Schema-Validated Tool Invocation",
      shortDesc: "Executes Pydantic-typed agent tools to update milestones and roadmaps.",
      input: "Structured tool parameters: student_id, milestone_id, new_status, reason",
      tool: "execute_agent_tool(tool_name, payload)",
      transformation: "Executes deterministic state transitions in transaction scope.",
      invariant: "Type safety: Strict Pydantic schema validation on all 12 agent tools."
    },
    {
      step: 5,
      id: "VERIFY",
      name: "Verify",
      icon: ShieldCheck,
      tagline: "Invariant & Integrity Assertion",
      shortDesc: "Guarantees completed work is preserved and prerequisites remain valid.",
      input: "Candidate updated roadmap vs. previous active roadmap state",
      tool: "verify_roadmap_invariants()",
      transformation: "Asserts completed milestone IDs exist in candidate plan with unaltered status.",
      invariant: "Preservation: Completed milestones count in new plan >= old plan."
    },
    {
      step: 6,
      id: "PERSIST",
      name: "Persist",
      icon: Layers,
      tagline: "Durable SQLite State Storage",
      shortDesc: "Writes observations, action logs, and new roadmap versions to database.",
      input: "Verified roadmap record, agent action log, revision rationale",
      tool: "commit_agent_transaction()",
      transformation: "Increments roadmap version (e.g. v1.0 → v2.0) and records audit trail.",
      invariant: "Atomicity: Full rollback if any persistence constraint fails."
    },
    {
      step: 7,
      id: "REPORT",
      name: "Report",
      icon: TrendingUp,
      tagline: "Explainable Student Insights",
      shortDesc: "Generates clear explanations and the single Next Best Action.",
      input: "Committed revision record, newly unblocked milestones",
      tool: "generate_explanation_summary()",
      transformation: "Outputs 'Why CareerAI Recommended This' and practical project guidance.",
      invariant: "Clarity: Simple English explanations with transparent algorithmic rationale."
    }
  ];

  const features = [
    {
      title: "Deterministic Skill Gap Engine",
      desc: "Calculates precise gaps on a 0 to 5 proficiency scale with automated priority classification and prerequisite dependency ordering.",
      icon: Target,
      tag: "Deterministic Logic"
    },
    {
      title: "Phased Milestone Roadmap",
      desc: "Generates structured roadmaps partitioned into sequential phases with verified resources and real-world project deliverables.",
      icon: Compass,
      tag: "Personalized"
    },
    {
      title: "Completed Work Preservation",
      desc: "When study hours change or career goals shift, the agent automatically adapts schedules while strictly preserving completed milestones.",
      icon: ShieldCheck,
      tag: "Adaptive Replanning"
    },
    {
      title: "Persistent SQLite Memory",
      desc: "Maintains student progress, agent observations, and revision history across restarts without relying on transient in-memory dictionaries.",
      icon: Database,
      tag: "Durable State"
    },
    {
      title: "AI Career Assistant",
      desc: "Context-aware guidance assistant that accesses database state before answering student questions about next steps and projects.",
      icon: Bot,
      tag: "Context-Aware"
    },
    {
      title: "Zero-Cost Fallback Mode",
      desc: "Runs 100% of core planning, calculation, and conversational workflows locally with no paid API keys required.",
      icon: Cpu,
      tag: "Zero Cost"
    }
  ];

  const activeStageObj = steps[selectedStage];

  return (
    <div className="space-y-16 py-6">
      {/* Hero Section */}
      <section className="relative pt-6 pb-4">
        <div className="max-w-4xl mx-auto text-center space-y-5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold tracking-wide">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            <span>Autonomous Career Guidance Agent</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight sm:leading-tight">
            Autonomous Career Guidance for{' '}
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
              College Students
            </span>
          </h1>

          <p className="text-sm sm:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
            CareerAI observes your skills, evaluates gaps against target roles, generates phased roadmaps, and proactively adapts your schedule as your time and interests evolve.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <button
              onClick={() => setActiveTab(currentStudent ? 'dashboard' : 'onboarding')}
              className="w-full sm:w-auto px-7 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 transition-all group"
            >
              <span>{currentStudent ? 'Go to Student Dashboard' : 'Get Started — Create Profile'}</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>

            <button
              onClick={() => setActiveTab('skill-gaps')}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 font-semibold text-sm transition-all"
            >
              Explore Skill Gaps
            </button>
          </div>

          {/* Quick Metrics Bar */}
          <div className="pt-8 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto border-t border-slate-850">
            <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-lg font-bold text-white font-mono">7 Stages</div>
              <div className="text-[11px] text-slate-400">Closed-Loop Controller</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-lg font-bold text-emerald-400 font-mono">12 Tools</div>
              <div className="text-[11px] text-slate-400">Pydantic-Typed Agent Tools</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-lg font-bold text-sky-400 font-mono">0 – 5 Scale</div>
              <div className="text-[11px] text-slate-400">Deterministic Benchmarks</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800/80">
              <div className="text-lg font-bold text-purple-400 font-mono">100% Durable</div>
              <div className="text-[11px] text-slate-400">SQLite Cross-Session Memory</div>
            </div>
          </div>
        </div>
      </section>

      {/* 7-Stage Autonomous Agent Controller Visualizer */}
      <section className="bg-slate-900/70 border border-slate-800/80 rounded-3xl p-6 sm:p-8 shadow-xl backdrop-blur-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-5">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-widest font-mono">
              <span>Agent Technology Core</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight mt-1">
              The 7-Stage Autonomous Agent Controller
            </h2>
          </div>
          <p className="text-xs text-slate-400 max-w-md">
            Click any stage below to inspect its inputs, transformations, tool executions, and safety invariants.
          </p>
        </div>

        {/* Horizontal Pipeline Stepper */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
          {steps.map((st, idx) => {
            const Icon = st.icon;
            const isSelected = selectedStage === idx;
            return (
              <button
                key={st.id}
                onClick={() => setSelectedStage(idx)}
                className={`flex flex-col items-start p-3 rounded-xl text-left border transition-all relative ${
                  isSelected
                    ? 'bg-slate-800/90 border-emerald-500/50 shadow-md shadow-emerald-500/10'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-850/60'
                }`}
              >
                <div className="flex items-center justify-between w-full mb-2">
                  <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                    isSelected ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'
                  }`}>
                    0{st.step}
                  </span>
                  <Icon className={`w-3.5 h-3.5 ${isSelected ? 'text-emerald-400' : 'text-slate-500'}`} />
                </div>
                <div className={`text-xs font-bold ${isSelected ? 'text-white' : 'text-slate-300'}`}>
                  {st.id}
                </div>
                <div className="text-[10px] text-slate-400 truncate w-full mt-0.5">
                  {st.tagline}
                </div>
              </button>
            );
          })}
        </div>

        {/* Detailed Stage Inspector Panel */}
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-5 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-850 pb-3">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
                <activeStageObj.icon className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-emerald-400 font-semibold">STAGE {activeStageObj.step} OF 7</span>
                  <span className="text-slate-600">•</span>
                  <span className="text-sm font-bold text-white">{activeStageObj.name}: {activeStageObj.tagline}</span>
                </div>
                <p className="text-xs text-slate-400">{activeStageObj.shortDesc}</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-[11px] text-slate-500 font-mono">Tool:</span>
              <code className="text-[11px] px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-emerald-300 font-mono">
                {activeStageObj.tool}
              </code>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-850 space-y-1">
              <span className="text-[10px] font-mono text-slate-400 uppercase font-semibold">Input Payload</span>
              <p className="text-slate-300 font-sans leading-relaxed">{activeStageObj.input}</p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-850 space-y-1">
              <span className="text-[10px] font-mono text-sky-400 uppercase font-semibold">Execution & Transformation</span>
              <p className="text-slate-300 font-sans leading-relaxed">{activeStageObj.transformation}</p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-850 space-y-1">
              <span className="text-[10px] font-mono text-amber-400 uppercase font-semibold">Safety Invariant Check</span>
              <p className="text-slate-300 font-sans leading-relaxed">{activeStageObj.invariant}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Demonstration: Proactive Replanning Simulation */}
      <section className="bg-slate-900/70 border border-slate-800/80 rounded-3xl p-6 sm:p-8 shadow-xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-sky-400 uppercase tracking-widest font-mono">
              <span>Interactive Decision Simulator</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight mt-1">
              How CareerAI Proactively Adapts
            </h2>
          </div>

          <div className="flex items-center gap-2 bg-slate-950 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setDemoScenario('hours_changed')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                demoScenario === 'hours_changed'
                  ? 'bg-slate-800 text-emerald-300 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Study Hours Adjusted (15h → 8h)
            </button>
            <button
              onClick={() => setDemoScenario('milestone_completed')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                demoScenario === 'milestone_completed'
                  ? 'bg-slate-800 text-emerald-300 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Milestone Completed (SQL Mastered)
            </button>
          </div>
        </div>

        {/* Live Simulation Card */}
        {demoScenario === 'hours_changed' ? (
          <div className="bg-slate-950/70 border border-slate-800 rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-300">Trigger Event: Student reduced study capacity from 15h to 8h/week due to college midterms</span>
              <span className="px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20 text-amber-300 font-mono text-[11px]">
                Replanning Triggered
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-slate-400">1. OBSERVE & REASON</span>
                <p className="text-slate-300">Detected 47% reduction in weekly study velocity. Current active roadmap will overshoot graduation deadline without adjustment.</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-emerald-400">2. INVARIANT CHECK</span>
                <p className="text-slate-300">Work Preservation rule activated: 3 previously completed milestones marked immutable. Only remaining 5 pending milestones rescaled.</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-sky-400">3. PLAN & ACT</span>
                <p className="text-slate-300">Generated revised schedule: Phase 2 elongated from 3 to 5 weeks. High-priority milestones reordered to preserve core outcomes.</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-purple-400">4. PERSIST & REPORT</span>
                <p className="text-slate-300">Saved as Roadmap v2.0 in SQLite with full revision log. Student notified with updated weekly targets and preserved credentials.</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-slate-950/70 border border-slate-800 rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-300">Trigger Event: Student checked off 'SQL for Data Analysis' milestone</span>
              <span className="px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 font-mono text-[11px]">
                Prerequisites Unblocked
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-slate-400">1. OBSERVE & REASON</span>
                <p className="text-slate-300">Milestone status updated to 'completed'. Student's evaluated SQL proficiency re-benchmarked from 2/5 to 4/5.</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-emerald-400">2. DEPENDENCY GRAPH</span>
                <p className="text-slate-300">Prerequisite check on downstream node: 'Database Design & Indexing' now has all prerequisites satisfied.</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-sky-400">3. NEXT ACTION ENGINE</span>
                <p className="text-slate-300">Next Best Action updated: Promoted 'PostgreSQL Schema Design' to active learning objective with priority score 0.92.</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-purple-400">4. PROGRESS AUDIT</span>
                <p className="text-slate-300">Recorded action into audit log. Dashboard milestone completion rate updated from 25% to 37.5%.</p>
              </div>
            </div>
          </div>
        )}
      </section>

      {/* Key Capabilities Grid */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <div className="text-xs font-bold text-emerald-400 uppercase tracking-widest font-mono">Core Capabilities</div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Engineered for Academic Rigor & Real Student Success
          </h2>
          <p className="text-xs sm:text-sm text-slate-400">
            A comprehensive implementation of Autonomous Agent Technology concepts for college career guidance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div
                key={idx}
                className="group bg-slate-900/60 border border-slate-800/80 rounded-2xl p-5 hover:border-slate-700 hover:bg-slate-900 transition-all duration-200"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700/60 text-emerald-400 group-hover:scale-105 transition-transform duration-200">
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-750">
                    {feat.tag}
                  </span>
                </div>
                <h3 className="text-sm font-bold text-white mb-1.5">{feat.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{feat.desc}</p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
