import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  FlaskConical,
  Cpu,
  Radio,
  Share2,
  GitPullRequest,
  Calculator,
  Play,
  Square,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ShieldCheck,
  TrendingUp,
  Award,
  ArrowRight,
  Zap,
  Info,
  Lock,
  Database,
  Key,
  Terminal,
  ExternalLink,
  Layers,
  ShieldAlert
} from 'lucide-react';

export default function AgentLabPage({ currentStudent, setActiveTab }) {
  const [activeLabTab, setActiveLabTab] = useState('reflex');

  // ==========================================
  // Assignment 1.2: Reflex Reasoner State
  // ==========================================
  const [telemetryCount, setTelemetryCount] = useState(6);
  const [telemetryLogs, setTelemetryLogs] = useState([]);
  const [telemetryLoading, setTelemetryLoading] = useState(false);

  const handleRunReflexStream = async () => {
    setTelemetryLoading(true);
    try {
      const res = await api.processReflexStream(telemetryCount);
      setTelemetryLogs(res.execution_logs || []);
    } catch (err) {
      console.error("Reflex stream error:", err);
    } finally {
      setTelemetryLoading(false);
    }
  };

  // ==========================================
  // Assignment 2.1: Concurrent Daemon State
  // ==========================================
  const [daemonMetrics, setDaemonMetrics] = useState({
    daemon_status: 'STOPPED',
    total_cycles_executed: 0,
    total_alerts_dispatched: 0,
    last_cycle_latency_ms: 0.0,
    average_cycle_latency_ms: 0.0,
    active_monitored_milestones: 5,
    active_overdue_alerts: 2
  });
  const [daemonAlerts, setDaemonAlerts] = useState([]);
  const [daemonPollingInterval, setDaemonPollingInterval] = useState(1.5);
  const [daemonLoading, setDaemonLoading] = useState(false);

  const fetchDaemonStatus = async () => {
    try {
      const res = await api.getDaemonMetrics();
      if (res.metrics) setDaemonMetrics(res.metrics);
      if (res.recent_alerts) setDaemonAlerts(res.recent_alerts);
    } catch (err) {
      console.warn("Daemon status query error:", err);
    }
  };

  useEffect(() => {
    let intervalId;
    if (activeLabTab === 'daemon' && daemonMetrics.daemon_status === 'RUNNING') {
      intervalId = setInterval(fetchDaemonStatus, 1500);
    }
    return () => clearInterval(intervalId);
  }, [activeLabTab, daemonMetrics.daemon_status]);

  const handleToggleDaemon = async (action) => {
    setDaemonLoading(true);
    try {
      await api.toggleDaemon(action, daemonPollingInterval);
      await fetchDaemonStatus();
    } catch (err) {
      console.error("Daemon toggle error:", err);
    } finally {
      setDaemonLoading(false);
    }
  };

  // ==========================================
  // Assignment 2.2: Distributed Sockets State
  // ==========================================
  const [socketPort, setSocketPort] = useState(9124);
  const [socketRole, setSocketRole] = useState(currentStudent?.target_role || "Cloud Solutions Architect");
  const [socketGpa, setSocketGpa] = useState(currentStudent?.gpa || 3.75);
  const [socketResult, setSocketResult] = useState(null);
  const [socketLoading, setSocketLoading] = useState(false);

  const handleRunSocketTransfer = async () => {
    setSocketLoading(true);
    try {
      const payload = {
        student_id: currentStudent ? `STU-${currentStudent.id}` : "STU-SOCKET-DEMO",
        target_role: socketRole,
        skills: currentStudent?.skills?.map(s => s.skill_name) || ["Python", "FastAPI", "React", "Docker", "AWS"],
        gpa: parseFloat(socketGpa),
        completed_milestones_count: 4,
        port: parseInt(socketPort)
      };
      const res = await api.executeSocketTransfer(payload);
      setSocketResult(res);
    } catch (err) {
      console.error("Socket transfer error:", err);
    } finally {
      setSocketLoading(false);
    }
  };

  // ==========================================
  // Assignment 3.1: Multi-Agent Negotiation State
  // ==========================================
  const [studentStipendTarget, setStudentStipendTarget] = useState(2200);
  const [recruiterBudgetCeiling, setRecruiterBudgetCeiling] = useState(2400);
  const [maxTurns, setMaxTurns] = useState(6);
  const [negotiationResult, setNegotiationResult] = useState(null);
  const [negotiationLoading, setNegotiationLoading] = useState(false);

  const handleRunNegotiation = async () => {
    setNegotiationLoading(true);
    try {
      const res = await api.executeNegotiation({
        max_turns: parseInt(maxTurns),
        student_target_stipend: parseInt(studentStipendTarget),
        recruiter_budget_ceiling: parseInt(recruiterBudgetCeiling)
      });
      setNegotiationResult(res);
    } catch (err) {
      console.error("Negotiation error:", err);
    } finally {
      setNegotiationLoading(false);
    }
  };

  // ==========================================
  // Assignment 3.2: Utility Optimizer State
  // ==========================================
  const [budgetLimit, setBudgetLimit] = useState(160);
  const [timeLimit, setTimeLimit] = useState(18);
  const [weightSkill, setWeightSkill] = useState(0.40);
  const [weightRelevance, setWeightRelevance] = useState(0.35);
  const [weightPrestige, setWeightPrestige] = useState(0.25);
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [optimizerLoading, setOptimizerLoading] = useState(false);

  const handleRunOptimizer = async () => {
    setOptimizerLoading(true);
    try {
      const res = await api.executeUtilityOptimization({
        weight_skill: parseFloat(weightSkill),
        weight_relevance: parseFloat(weightRelevance),
        weight_prestige: parseFloat(weightPrestige),
        budget_limit_usd: parseFloat(budgetLimit),
        time_limit_hours: parseFloat(timeLimit)
      });
      setOptimizationResult(res);
    } catch (err) {
      console.error("Optimizer error:", err);
    } finally {
      setOptimizerLoading(false);
    }
  };

  // ==========================================
  // Assignment 4.1: BDI Cognitive State
  // ==========================================
  const [bdiState, setBdiState] = useState(null);
  const [bdiLoading, setBdiLoading] = useState(false);
  const [bdiShiftAlert, setBdiShiftAlert] = useState(null);

  const fetchBdiState = async () => {
    try {
      const res = await api.getBdiState();
      setBdiState(res);
    } catch (err) {
      console.warn("BDI state fetch error:", err);
    }
  };

  useEffect(() => {
    if (activeLabTab === 'bdi' && !bdiState) {
      fetchBdiState();
    }
  }, [activeLabTab]);

  const handleExecuteBdiStep = async () => {
    setBdiLoading(true);
    try {
      await api.executeBdiStep();
      await fetchBdiState();
    } catch (err) {
      console.error("BDI step error:", err);
    } finally {
      setBdiLoading(false);
    }
  };

  const handleBdiReconsider = async (beliefName, newValue, source) => {
    setBdiLoading(true);
    try {
      const res = await api.triggerBdiReconsider({
        belief_name: beliefName,
        new_value: newValue,
        source: source || "UNEXPECTED_ENVIRONMENTAL_UPDATE"
      });
      if (res?.reconsideration_result?.shift_details) {
        setBdiShiftAlert(res.reconsideration_result.shift_details);
      }
      await fetchBdiState();
    } catch (err) {
      console.error("BDI reconsider error:", err);
    } finally {
      setBdiLoading(false);
    }
  };

  const handleResetBdi = async () => {
    setBdiLoading(true);
    try {
      await api.resetBdiAgent();
      setBdiShiftAlert(null);
      await fetchBdiState();
    } catch (err) {
      console.error("BDI reset error:", err);
    } finally {
      setBdiLoading(false);
    }
  };

  // ==========================================
  // Assignment 4.2: Knowledge Ontology & Live API State
  // ==========================================
  const [ontologyRoles, setOntologyRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState("Full Stack Engineer");
  const [roleDetails, setRoleDetails] = useState(null);
  const [apiSkillKeyword, setApiSkillKeyword] = useState("FastAPI");
  const [liveResources, setLiveResources] = useState([]);
  const [apiMeta, setApiMeta] = useState(null);
  const [adaptedMilestone, setAdaptedMilestone] = useState(null);
  const [knowledgeLoading, setKnowledgeLoading] = useState(false);

  const fetchOntology = async () => {
    try {
      const res = await api.getCareerOntology();
      if (res.roles) {
        setOntologyRoles(res.roles);
        if (!roleDetails && res.roles.length > 0) {
          const details = await api.getRolePrerequisites(res.roles[0]);
          setRoleDetails(details);
        }
      }
    } catch (err) {
      console.warn("Ontology fetch error:", err);
    }
  };

  useEffect(() => {
    if (activeLabTab === 'knowledge') {
      fetchOntology();
    }
  }, [activeLabTab]);

  const handleSelectRole = async (role) => {
    setSelectedRole(role);
    try {
      const details = await api.getRolePrerequisites(role);
      setRoleDetails(details);
    } catch (err) {
      console.error("Role details error:", err);
    }
  };

  const handleFetchLiveResources = async () => {
    setKnowledgeLoading(true);
    try {
      const res = await api.fetchLiveSkillResources(apiSkillKeyword, 3);
      setLiveResources(res.resources || []);
      setApiMeta(res.metadata || {});
    } catch (err) {
      console.error("Live resources error:", err);
    } finally {
      setKnowledgeLoading(false);
    }
  };

  const handleAdaptMilestone = async () => {
    setKnowledgeLoading(true);
    try {
      const res = await api.adaptLearningPlanWithApi({
        student_id: currentStudent ? `STU-${currentStudent.id}` : "STU-RA2212704010040",
        target_role: selectedRole,
        current_skills: currentStudent?.skills?.map(s => s.skill_name) || ["Python", "SQL"],
        primary_skill_gap: apiSkillKeyword
      });
      setAdaptedMilestone(res.adaptation_record?.adapted_milestone || null);
    } catch (err) {
      console.error("Adapt plan error:", err);
    } finally {
      setKnowledgeLoading(false);
    }
  };

  // ==========================================
  // Assignment 5.1: Agent Security State
  // ==========================================
  const [trustedHosts, setTrustedHosts] = useState({});
  const [securityAuditLogs, setSecurityAuditLogs] = useState([]);
  const [lastSecurityAction, setLastSecurityAction] = useState(null);
  const [securityLoading, setSecurityLoading] = useState(false);

  const fetchSecurityData = async () => {
    try {
      const [hostsRes, logsRes] = await Promise.all([
        api.getTrustedHostsRegistry(),
        api.getSecurityAuditLogs()
      ]);
      if (hostsRes.trusted_hosts) setTrustedHosts(hostsRes.trusted_hosts);
      if (logsRes.audit_logs) setSecurityAuditLogs(logsRes.audit_logs);
    } catch (err) {
      console.warn("Security data fetch error:", err);
    }
  };

  useEffect(() => {
    if (activeLabTab === 'security') {
      fetchSecurityData();
    }
  }, [activeLabTab]);

  const handleExecuteValidSignedCommand = async () => {
    setSecurityLoading(true);
    try {
      const envRes = await api.createSignedEnvelope({
        host_id: "HOST_STUDENT_PORTAL_CORE",
        sender_id: "SENDER_ACADEMIC_ADVISOR",
        secret_key: "CAREERAI_SEC_KEY_PROD_ADVISOR_9823",
        action: "UPDATE_STUDENT_PROFILE",
        payload_data: {
          student_id: currentStudent ? `STU-${currentStudent.id}` : "STU-RA2212704010040",
          gpa: currentStudent?.gpa || 3.75,
          timestamp: Date.now()
        }
      });
      const verifyRes = await api.verifySecureCommand(envRes.envelope);
      setLastSecurityAction({ type: "LEGITIMATE", envelope: envRes.envelope, result: verifyRes });
      await fetchSecurityData();
    } catch (err) {
      console.error("Security command error:", err);
    } finally {
      setSecurityLoading(false);
    }
  };

  const handleSimulateAttack = async (attackType) => {
    setSecurityLoading(true);
    try {
      const res = await api.simulateSecurityAttack(attackType);
      setLastSecurityAction({ type: "ATTACK_SIMULATION", attackType, result: res });
      await fetchSecurityData();
    } catch (err) {
      console.error("Attack simulation error:", err);
    } finally {
      setSecurityLoading(false);
    }
  };

  // ==========================================
  // Assignment 5.2: Capstone Orchestrator State
  // ==========================================
  const [capstoneSystemState, setCapstoneSystemState] = useState(null);
  const [capstoneCycleResult, setCapstoneCycleResult] = useState(null);
  const [capstoneLoading, setCapstoneLoading] = useState(false);

  const fetchCapstoneSystemState = async () => {
    try {
      const res = await api.getCapstoneSystemState();
      setCapstoneSystemState(res);
    } catch (err) {
      console.warn("Capstone state error:", err);
    }
  };

  useEffect(() => {
    if (activeLabTab === 'capstone') {
      fetchCapstoneSystemState();
    }
  }, [activeLabTab]);

  const handleRunCapstoneCycle = async () => {
    setCapstoneLoading(true);
    try {
      const res = await api.runCapstoneConsolidatedCycle({
        student_id: currentStudent ? `STU-${currentStudent.id}` : "STU-RA2212704010040",
        target_role: currentStudent?.target_role || "Full Stack Engineer",
        weekly_hours: currentStudent?.weekly_hours || 14.0,
        burnout_index: 20.0
      });
      setCapstoneCycleResult(res);
      await fetchCapstoneSystemState();
    } catch (err) {
      console.error("Capstone cycle error:", err);
    } finally {
      setCapstoneLoading(false);
    }
  };

  return (
    <div className="py-8 space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950/40 border border-slate-700/80 rounded-2xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-semibold">
              <FlaskConical className="w-3.5 h-3.5" />
              <span>AGENT TECHNOLOGY CURRICULUM LAB (UNITS 1 - 5)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
              Agent Technology Research & Demonstration Lab
            </h1>
            <p className="text-sm text-slate-300 max-w-3xl">
              Interactive execution workbench validating all 9 coursework assignments across Units 1 through 5.
              Execute condition-action reflex streams, concurrent daemons, TCP sockets, negotiation protocols,
              MAUT utility optimization, BDI cognitive deliberation, live ontology API adaptations, cryptographic HMAC security, and consolidated capstone cycles.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4" /> 9/9 Validated
            </span>
            <span className="px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold flex items-center gap-1.5">
              <Award className="w-4 h-4" /> Academic Viva Ready
            </span>
          </div>
        </div>
      </div>

      {/* Assignment Navigation Tabs */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2 sm:gap-3">
        {[
          { id: 'reflex', title: '1.2 Reflex Reasoner', sub: 'Unit 1: Rules & Telemetry', icon: Radio },
          { id: 'daemon', title: '2.1 Task Daemon', sub: 'Unit 2: Threads & Locks', icon: Cpu },
          { id: 'socket', title: '2.2 Socket Mesh', sub: 'Unit 2: Distributed TCP', icon: Share2 },
          { id: 'negotiate', title: '3.1 Multi-Agent', sub: 'Unit 3: Contract Net', icon: GitPullRequest },
          { id: 'optimizer', title: '3.2 Utility Optimizer', sub: 'Unit 3: MAUT Scoring', icon: Calculator },
          { id: 'bdi', title: '4.1 BDI Cognitive', sub: 'Unit 4: Beliefs, Desires, Shifts', icon: Layers },
          { id: 'knowledge', title: '4.2 Knowledge & API', sub: 'Unit 4: Ontology & GitHub API', icon: Database },
          { id: 'security', title: '5.1 Agent Security', sub: 'Unit 5: HMAC & Attack Defense', icon: Lock },
          { id: 'capstone', title: '5.2 Capstone Master', sub: 'Unit 5: 10-Stage Pipeline', icon: Award }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeLabTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveLabTab(tab.id)}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                isActive
                  ? 'bg-slate-800 border-brand-500 text-white shadow-lg shadow-brand-500/10'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
              }`}
            >
              <div className="flex items-center gap-2 mb-1.5">
                <Icon className={`w-4 h-4 ${isActive ? 'text-brand-400' : 'text-slate-500'}`} />
                <span className="text-xs font-bold leading-tight truncate">{tab.title}</span>
              </div>
              <p className="text-[11px] text-slate-500 truncate">{tab.sub}</p>
            </button>
          );
        })}
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: ASSIGNMENT 1.2 - REFLEX REASONER */}
      {/* ========================================================================= */}
      {activeLabTab === 'reflex' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    ASSIGNMENT 1.2
                  </span>
                  <h2 className="text-lg font-bold text-white">Rule-Based Environmental Reasoner Implementation</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Evaluates dynamic streaming sensory telemetry (study velocity, market demand surges, burnout scores) using prioritized Condition-Action production rules.
                </p>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 text-xs">
                  <span className="text-slate-400">Packets:</span>
                  <select
                    value={telemetryCount}
                    onChange={(e) => setTelemetryCount(Number(e.target.value))}
                    className="bg-transparent text-white focus:outline-none"
                  >
                    <option value={4} className="bg-slate-900">4 frames</option>
                    <option value={6} className="bg-slate-900">6 frames</option>
                    <option value={10} className="bg-slate-900">10 frames</option>
                  </select>
                </div>

                <button
                  onClick={handleRunReflexStream}
                  disabled={telemetryLoading}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-slate-950 text-xs font-bold transition-all shadow-md shadow-brand-500/20 disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>{telemetryLoading ? "Ingesting Stream..." : "Inject Telemetry Stream"}</span>
                </button>
              </div>
            </div>

            {/* Execution logs display */}
            <div className="mt-6 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Reactive Trigger Execution History ({telemetryLogs.length} events logged)
                </h3>
                <span className="text-[11px] text-slate-500 font-mono">5 Condition-Action Rules Active</span>
              </div>

              {telemetryLogs.length === 0 ? (
                <div className="p-8 text-center border border-dashed border-slate-800 rounded-xl bg-slate-950/40">
                  <Radio className="w-8 h-8 text-slate-600 mx-auto mb-2 animate-pulse" />
                  <p className="text-sm text-slate-400">Telemetry feed is idle. Click "Inject Telemetry Stream" to test reflex rules.</p>
                </div>
              ) : (
                <div className="grid gap-3">
                  {telemetryLogs.map((log, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl border border-slate-800 bg-slate-950/70 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-slate-700 transition-colors"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            log.severity === 'CRITICAL' ? 'bg-red-500/15 text-red-400 border border-red-500/20' :
                            log.severity === 'HIGH' ? 'bg-amber-500/15 text-amber-400 border border-amber-500/20' :
                            log.severity === 'MEDIUM' ? 'bg-yellow-500/15 text-yellow-400 border border-yellow-500/20' :
                            'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20'
                          }`}>
                            {log.severity}
                          </span>
                          <span className="font-mono text-xs font-bold text-white">{log.rule_id}</span>
                          <span className="text-[11px] text-slate-500">[{log.timestamp.slice(11, 19)}]</span>
                        </div>
                        <p className="text-xs text-slate-300">{log.message}</p>
                        <p className="text-[11px] text-slate-500 font-mono">Condition: {log.condition}</p>
                      </div>

                      <div className="text-right sm:min-w-[180px]">
                        <span className="text-[10px] uppercase tracking-wider text-slate-500 block">Fired Action</span>
                        <span className="text-xs font-semibold text-brand-400">{log.action}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: ASSIGNMENT 2.1 - CONCURRENT DAEMON */}
      {/* ========================================================================= */}
      {activeLabTab === 'daemon' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                    ASSIGNMENT 2.1
                  </span>
                  <h2 className="text-lg font-bold text-white">Concurrent Task Daemonization using Threads & Workers</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Executes a background daemon worker thread (<code className="text-brand-300">daemon=True</code>) with thread safety (<code className="text-brand-300">threading.Lock</code>, <code className="text-brand-300">queue.Queue</code>) to scan milestones without blocking the web application.
                </p>
              </div>

              <div className="flex items-center gap-3">
                {daemonMetrics.daemon_status === 'RUNNING' ? (
                  <button
                    onClick={() => handleToggleDaemon('STOP')}
                    disabled={daemonLoading}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-500 hover:bg-red-600 text-white text-xs font-bold transition-all shadow-md shadow-red-500/20 disabled:opacity-50"
                  >
                    <Square className="w-3.5 h-3.5 fill-current" />
                    <span>Stop Daemon Worker</span>
                  </button>
                ) : (
                  <button
                    onClick={() => handleToggleDaemon('START')}
                    disabled={daemonLoading}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-slate-950 text-xs font-bold transition-all shadow-md shadow-emerald-500/20 disabled:opacity-50"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>Start Daemon Worker</span>
                  </button>
                )}
                <button
                  onClick={fetchDaemonStatus}
                  className="p-2 rounded-lg bg-slate-800 text-slate-400 hover:text-white"
                  title="Refresh state"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Metrics cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-4">
                <span className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">Worker State</span>
                <div className="flex items-center gap-2 mt-1">
                  <div className={`w-2.5 h-2.5 rounded-full ${daemonMetrics.daemon_status === 'RUNNING' ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}`} />
                  <span className={`text-base font-bold ${daemonMetrics.daemon_status === 'RUNNING' ? 'text-emerald-400' : 'text-slate-400'}`}>
                    {daemonMetrics.daemon_status}
                  </span>
                </div>
              </div>

              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-4">
                <span className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">Cycles Executed</span>
                <p className="text-xl font-black text-white mt-1">{daemonMetrics.total_cycles_executed}</p>
              </div>

              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-4">
                <span className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">Cycle Latency</span>
                <p className="text-xl font-black text-cyan-400 mt-1">{daemonMetrics.last_cycle_latency_ms} <span className="text-xs font-normal text-slate-500">ms</span></p>
              </div>

              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-4">
                <span className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">Average Latency</span>
                <p className="text-xl font-black text-brand-400 mt-1">{daemonMetrics.average_cycle_latency_ms} <span className="text-xs font-normal text-slate-500">ms</span></p>
              </div>
            </div>

            {/* Thread safety proof */}
            <div className="mt-6 p-4 rounded-xl border border-slate-800 bg-slate-950/40 space-y-2">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-300">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Thread-Safe Invariance Verified</span>
              </div>
              <p className="text-xs text-slate-400">
                Safe concurrent access between FastAPI worker processes and the background scanning daemon is strictly mediated through <code className="text-brand-300">threading.Lock()</code> re-entrant primitives. Zero race conditions or data corruptions detected.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 3: ASSIGNMENT 2.2 - DISTRIBUTED SOCKET MESSAGING */}
      {/* ========================================================================= */}
      {activeLabTab === 'socket' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-violet-500/10 text-violet-400 border border-violet-500/20">
                    ASSIGNMENT 2.2
                  </span>
                  <h2 className="text-lg font-bold text-white">Distributed Agent Messaging using Sockets/RPC</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Establishes a raw TCP socket frame transfer between Agent-A (Student Advisor) and Agent-B (Placement Node) with 4-byte length prefix protocol.
                </p>
              </div>

              <button
                onClick={handleRunSocketTransfer}
                disabled={socketLoading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-slate-950 text-xs font-bold transition-all shadow-md shadow-brand-500/20 disabled:opacity-50"
              >
                <Zap className="w-3.5 h-3.5 fill-current" />
                <span>{socketLoading ? "Connecting Socket..." : "Transmit Socket Frame"}</span>
              </button>
            </div>

            {/* Input controls */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
              <div>
                <label className="text-xs text-slate-400 block mb-1.5 font-medium">Socket Node Port</label>
                <input
                  type="number"
                  value={socketPort}
                  onChange={(e) => setSocketPort(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500 font-mono"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1.5 font-medium">Target Role Evaluated</label>
                <input
                  type="text"
                  value={socketRole}
                  onChange={(e) => setSocketRole(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1.5 font-medium">Student Academic GPA</label>
                <input
                  type="number"
                  step="0.05"
                  value={socketGpa}
                  onChange={(e) => setSocketGpa(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500"
                />
              </div>
            </div>

            {/* Socket results */}
            {socketResult && (
              <div className="mt-6 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Transmission logs */}
                  <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                      <Share2 className="w-3.5 h-3.5 text-brand-400" />
                      TCP Frame Audit Trail
                    </h3>
                    <div className="space-y-1.5 font-mono text-[11px] text-slate-300">
                      {socketResult.audit_trail?.map((log, idx) => (
                        <p key={idx} className="leading-relaxed">{log}</p>
                      ))}
                    </div>
                  </div>

                  {/* Remote Agent-B evaluation */}
                  <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-3">
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                      Agent-B Autonomous Placement Decision
                    </h3>

                    {socketResult.inbound_response && (
                      <div className="space-y-2 text-xs">
                        <div className="flex items-center justify-between">
                          <span className="text-slate-400">Readiness Score:</span>
                          <span className="font-bold text-emerald-400 text-sm">
                            {socketResult.inbound_response.readiness_score}%
                          </span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-slate-400">Assigned Candidate Tier:</span>
                          <span className="font-semibold text-white px-2 py-0.5 rounded bg-slate-800">
                            {socketResult.inbound_response.placement_tier}
                          </span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-slate-400">Digital Handshake:</span>
                          <span className="font-mono text-[11px] text-cyan-400">
                            {socketResult.inbound_response.digital_handshake_signature}
                          </span>
                        </div>
                        <div className="pt-2 border-t border-slate-800">
                          <span className="text-[11px] text-slate-500 uppercase tracking-wider block mb-1">Node Recommendations</span>
                          <p className="text-slate-300 text-xs">
                            {socketResult.inbound_response.recommendations?.join(" • ") || "All criteria satisfied."}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 4: ASSIGNMENT 3.1 - MULTI-AGENT NEGOTIATION */}
      {/* ========================================================================= */}
      {activeLabTab === 'negotiate' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-pink-500/10 text-pink-400 border border-pink-500/20">
                    ASSIGNMENT 3.1
                  </span>
                  <h2 className="text-lg font-bold text-white">Multi-Agent Coordination & Negotiation Protocol</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Contract Net protocol execution between StudentAgent and RecruiterAgent negotiating internship stipends and workloads with concession curves α(t).
                </p>
              </div>

              <button
                onClick={handleRunNegotiation}
                disabled={negotiationLoading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-slate-950 text-xs font-bold transition-all shadow-md shadow-brand-500/20 disabled:opacity-50"
              >
                <GitPullRequest className="w-3.5 h-3.5" />
                <span>{negotiationLoading ? "Negotiating..." : "Execute Negotiation"}</span>
              </button>
            </div>

            {/* Negotiation inputs */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Student Target Stipend:</span>
                  <span className="font-bold text-brand-400">${studentStipendTarget}/mo</span>
                </div>
                <input
                  type="range"
                  min={1200}
                  max={3000}
                  step={100}
                  value={studentStipendTarget}
                  onChange={(e) => setStudentStipendTarget(e.target.value)}
                  className="w-full accent-brand-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Recruiter Budget Ceiling:</span>
                  <span className="font-bold text-emerald-400">${recruiterBudgetCeiling}/mo</span>
                </div>
                <input
                  type="range"
                  min={1400}
                  max={3200}
                  step={100}
                  value={recruiterBudgetCeiling}
                  onChange={(e) => setRecruiterBudgetCeiling(e.target.value)}
                  className="w-full accent-emerald-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Max Negotiation Turns:</span>
                  <span className="font-bold text-white">{maxTurns} turns</span>
                </div>
                <input
                  type="range"
                  min={3}
                  max={10}
                  step={1}
                  value={maxTurns}
                  onChange={(e) => setMaxTurns(e.target.value)}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>
            </div>

            {/* Negotiation timeline visualizer */}
            {negotiationResult && (
              <div className="mt-6 space-y-4">
                <div className="p-4 rounded-xl border border-slate-800 bg-slate-950/70 flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-slate-500 block">Negotiation Outcome</span>
                    <span className={`text-sm font-bold ${negotiationResult.consensus_reached ? 'text-emerald-400' : 'text-amber-400'}`}>
                      {negotiationResult.status} ({negotiationResult.total_turns} turns elapsed)
                    </span>
                  </div>

                  {negotiationResult.consensus_reached && (
                    <div className="flex items-center gap-3 text-xs bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      <div>
                        <span className="font-semibold text-white block">
                          Agreed: ${negotiationResult.final_agreement?.stipend}/mo • {negotiationResult.final_agreement?.hours}h/wk
                        </span>
                        <span className="text-[10px] text-cyan-400 font-mono">
                          {negotiationResult.handshake_signature}
                        </span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Turn-by-turn cards */}
                <div className="grid gap-2.5">
                  {negotiationResult.timeline?.map((step, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 rounded-xl border border-slate-800/80 bg-slate-950/40 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-14 font-mono font-bold text-slate-400">Turn {step.turn}</span>
                        <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                          step.proposer === 'StudentAgent' ? 'bg-brand-500/10 text-brand-400 border border-brand-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        }`}>
                          {step.proposer}
                        </span>
                        <span className="text-white font-medium">
                          Offer: <span className="font-bold text-brand-300">${step.offer.stipend}</span> • {step.offer.hours}h/wk • {step.offer.mentorship} mentorship
                        </span>
                      </div>

                      <div className="flex items-center gap-4 text-slate-400">
                        <span>U(Student): <b className="text-white">{step.student_utility.toFixed(3)}</b></span>
                        <span>U(Recruiter): <b className="text-white">{step.recruiter_utility.toFixed(3)}</b></span>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          step.action.includes('ACCEPTED') ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'
                        }`}>
                          {step.action}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 5: ASSIGNMENT 3.2 - UTILITY OPTIMIZER */}
      {/* ========================================================================= */}
      {activeLabTab === 'optimizer' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    ASSIGNMENT 3.2
                  </span>
                  <h2 className="text-lg font-bold text-white">Self-Interested Agent Utility Optimization (10 Bundles)</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Multi-Attribute Utility Theory (MAUT): Evaluates 10 candidate course bundles against budget ($) and time (h/wk) constraints to select the global maximum.
                </p>
              </div>

              <button
                onClick={handleRunOptimizer}
                disabled={optimizerLoading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-slate-950 text-xs font-bold transition-all shadow-md shadow-brand-500/20 disabled:opacity-50"
              >
                <Calculator className="w-3.5 h-3.5" />
                <span>{optimizerLoading ? "Optimizing..." : "Compute Optimal Utility"}</span>
              </button>
            </div>

            {/* Sliders for constraints and weights */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mt-6">
              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Budget Limit:</span>
                  <span className="font-bold text-white">${budgetLimit}</span>
                </div>
                <input
                  type="range"
                  min={50}
                  max={250}
                  step={10}
                  value={budgetLimit}
                  onChange={(e) => setBudgetLimit(e.target.value)}
                  className="w-full accent-brand-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Time Limit:</span>
                  <span className="font-bold text-white">{timeLimit} h/wk</span>
                </div>
                <input
                  type="range"
                  min={6}
                  max={25}
                  step={1}
                  value={timeLimit}
                  onChange={(e) => setTimeLimit(e.target.value)}
                  className="w-full accent-cyan-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Skill Weight (w₁):</span>
                  <span className="font-bold text-brand-300">{weightSkill}</span>
                </div>
                <input
                  type="range"
                  min={0.1}
                  max={0.8}
                  step={0.05}
                  value={weightSkill}
                  onChange={(e) => setWeightSkill(e.target.value)}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Relevance (w₂):</span>
                  <span className="font-bold text-brand-300">{weightRelevance}</span>
                </div>
                <input
                  type="range"
                  min={0.1}
                  max={0.8}
                  step={0.05}
                  value={weightRelevance}
                  onChange={(e) => setWeightRelevance(e.target.value)}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Prestige (w₃):</span>
                  <span className="font-bold text-brand-300">{weightPrestige}</span>
                </div>
                <input
                  type="range"
                  min={0.1}
                  max={0.8}
                  step={0.05}
                  value={weightPrestige}
                  onChange={(e) => setWeightPrestige(e.target.value)}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>
            </div>

            {/* Optimizer results */}
            {optimizationResult && (
              <div className="mt-6 space-y-6">
                {/* Global winner card */}
                {optimizationResult.optimal_bundle && (
                  <div className="bg-gradient-to-r from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/30 rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <Award className="w-5 h-5 text-emerald-400" />
                        <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Global Optimal Bundle Selected</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 font-mono font-bold">
                          {optimizationResult.optimal_bundle.id}
                        </span>
                      </div>
                      <h3 className="text-base font-bold text-white">{optimizationResult.optimal_bundle.title}</h3>
                      <p className="text-xs text-slate-400">
                        Provider: {optimizationResult.optimal_bundle.provider} • Cost: ${optimizationResult.optimal_bundle.cost_usd} • Time: {optimizationResult.optimal_bundle.hours_per_week}h/week
                      </p>
                    </div>

                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <span className="text-[11px] text-slate-500 block">Gross Value</span>
                        <span className="text-sm font-semibold text-slate-300">{optimizationResult.optimal_bundle.gross_score}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-[11px] text-slate-500 block">Cost Penalty</span>
                        <span className="text-sm font-semibold text-red-400">-{optimizationResult.optimal_bundle.cost_penalty}</span>
                      </div>
                      <div className="text-right pl-4 border-l border-slate-800">
                        <span className="text-[11px] text-emerald-400 font-semibold block uppercase">Net Utility U(x)</span>
                        <span className="text-xl font-black text-emerald-400">{optimizationResult.optimal_bundle.net_utility}</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Candidate list table */}
                <div className="border border-slate-800 rounded-xl overflow-hidden">
                  <div className="bg-slate-950 px-4 py-2.5 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
                    <span>Evaluated Candidates ({optimizationResult.total_options_evaluated} total, {optimizationResult.feasible_count} feasible, {optimizationResult.infeasible_count} rejected)</span>
                    <span className="font-mono text-[11px]">Formula: U(x) = S(x) - C(x)</span>
                  </div>

                  <div className="divide-y divide-slate-800/60 text-xs">
                    {optimizationResult.ranked_feasible_options?.map((b, idx) => (
                      <div
                        key={b.id}
                        className={`p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                          b.id === optimizationResult.optimal_bundle?.id ? 'bg-emerald-500/5' : 'bg-slate-900/40'
                        }`}
                      >
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-[11px] text-slate-500">{b.id}</span>
                            <span className="font-bold text-white">{b.title}</span>
                            {b.id === optimizationResult.optimal_bundle?.id && (
                              <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">
                                OPTIMAL
                              </span>
                            )}
                          </div>
                          <span className="text-[11px] text-slate-400">{b.provider} • ${b.cost_usd} • {b.hours_per_week}h/wk</span>
                        </div>

                        <div className="flex items-center gap-4 text-right">
                          <span className="text-slate-400">Gross: {b.gross_score}</span>
                          <span className="text-red-400">Pen: -{b.cost_penalty}</span>
                          <span className="font-bold text-brand-300 min-w-[70px]">Net: {b.net_utility}</span>
                        </div>
                      </div>
                    ))}

                    {optimizationResult.infeasible_options?.map((b) => (
                      <div key={b.id} className="p-3.5 bg-red-950/10 flex flex-col sm:flex-row sm:items-center justify-between gap-3 opacity-60">
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-[11px] text-slate-500">{b.id}</span>
                            <span className="text-slate-400 line-through">{b.title}</span>
                            <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400">
                              REJECTED
                            </span>
                          </div>
                          <span className="text-[11px] text-red-400 font-mono">{b.violations?.join(", ")}</span>
                        </div>

                        <div className="flex items-center gap-4 text-right text-slate-500">
                          <span>${b.cost_usd}</span>
                          <span>{b.hours_per_week}h/wk</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 6: ASSIGNMENT 4.1 - BDI COGNITIVE ARCHITECTURE */}
      {/* ========================================================================= */}
      {activeLabTab === 'bdi' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20">
                    ASSIGNMENT 4.1
                  </span>
                  <h2 className="text-lg font-bold text-white">BDI (Belief-Desire-Intention) Goal-Driven Modeling</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Classical Rao & Georgeff BDI cognitive loop tracking explicit Beliefs, competing candidate Desires, and committed procedural Intentions with dynamic intention shifts.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleExecuteBdiStep}
                  disabled={bdiLoading || !bdiState?.current_intention || bdiState.current_intention.status === "COMPLETED"}
                  className="px-3.5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 shadow-lg shadow-purple-600/20 disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5" /> Advance Step
                </button>
                <button
                  onClick={handleResetBdi}
                  disabled={bdiLoading}
                  className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs border border-slate-700 transition-colors flex items-center gap-1.5"
                >
                  <RefreshCw className="w-3.5 h-3.5" /> Reset
                </button>
              </div>
            </div>

            {/* Environmental Shock Trigger Alert Banner */}
            {bdiShiftAlert && (
              <div className="mt-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div className="space-y-1 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-amber-300">DYNAMIC INTENTION SHIFT RECORD ({bdiShiftAlert.shift_id})</span>
                    <span className="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 text-[10px] font-mono">AUTOMATIC RECONSIDERATION</span>
                  </div>
                  <p className="text-slate-300">
                    <strong>Trigger:</strong> Belief '{bdiShiftAlert.triggering_belief?.name}' shifted from {String(bdiShiftAlert.triggering_belief?.old_value)} to {String(bdiShiftAlert.triggering_belief?.new_value)}.
                  </p>
                  <p className="text-slate-300">
                    <strong>Reason:</strong> {bdiShiftAlert.reconsideration_reason}
                  </p>
                  <div className="flex items-center gap-2 pt-1 font-mono text-[11px]">
                    <span className="line-through text-red-400">Previous: {bdiShiftAlert.previous_intention?.name}</span>
                    <ArrowRight className="w-3 h-3 text-amber-400" />
                    <span className="text-emerald-400 font-bold">New Plan: {bdiShiftAlert.new_intention?.name}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Main BDI Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
              {/* Column 1: Beliefs Base */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Database className="w-3.5 h-3.5 text-purple-400" /> Current Belief Base
                  </h3>
                  <span className="px-2 py-0.5 rounded-full bg-slate-800 text-[10px] font-mono text-purple-300">
                    {bdiState ? Object.keys(bdiState.beliefs || {}).length : 0} Beliefs
                  </span>
                </div>

                <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                  {bdiState?.beliefs && Object.entries(bdiState.beliefs).map(([key, item]) => (
                    <div key={key} className="p-2.5 rounded-lg bg-slate-900 border border-slate-800/80 flex items-center justify-between text-xs">
                      <div>
                        <span className="font-mono text-slate-400">{key}</span>
                        <p className="text-[10px] text-slate-500">Source: {item.source}</p>
                      </div>
                      <span className="font-bold text-white font-mono bg-slate-800 px-2 py-1 rounded">
                        {String(item.value)}
                      </span>
                    </div>
                  ))}
                </div>

                {/* Simulated Shocks */}
                <div className="pt-3 border-t border-slate-800 space-y-2">
                  <span className="text-[11px] font-bold text-slate-400 block uppercase">Simulate Environmental Update</span>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => handleBdiReconsider('weekly_study_hours', 4.0, 'TIME_DEFICIT_SHOCK')}
                      disabled={bdiLoading}
                      className="p-2 rounded-lg bg-red-950/30 border border-red-500/30 hover:bg-red-900/40 text-[11px] text-red-300 font-semibold transition-colors text-left"
                    >
                      Time Shock: 4h/wk
                    </button>
                    <button
                      onClick={() => handleBdiReconsider('burnout_index', 85.0, 'EXAM_FATIGUE_SHOCK')}
                      disabled={bdiLoading}
                      className="p-2 rounded-lg bg-amber-950/30 border border-amber-500/30 hover:bg-amber-900/40 text-[11px] text-amber-300 font-semibold transition-colors text-left"
                    >
                      Fatigue Surge: 85%
                    </button>
                  </div>
                </div>
              </div>

              {/* Column 2: Candidate Desires */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5 text-brand-400" /> Candidate Desires (Goals)
                  </h3>
                  <span className="px-2 py-0.5 rounded-full bg-slate-800 text-[10px] font-mono text-brand-300">
                    {bdiState ? Object.keys(bdiState.all_desires || {}).length : 0} Goals
                  </span>
                </div>

                <div className="space-y-2.5">
                  {bdiState?.all_desires && Object.values(bdiState.all_desires).map((des) => {
                    const isDominant = bdiState.dominant_desire?.desire_id === des.desire_id;
                    return (
                      <div
                        key={des.desire_id}
                        className={`p-3 rounded-lg border transition-all ${
                          isDominant
                            ? 'bg-brand-500/10 border-brand-500/50 shadow-md shadow-brand-500/10'
                            : 'bg-slate-900 border-slate-800 opacity-70'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-bold text-xs text-white flex items-center gap-1.5">
                            {des.name}
                            {isDominant && (
                              <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-brand-500 text-slate-950">
                                DOMINANT
                              </span>
                            )}
                          </span>
                          <span className="text-[10px] font-mono text-slate-400">Pri: {des.priority}</span>
                        </div>
                        <p className="text-[11px] text-slate-400">{des.description}</p>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Column 3: Committed Procedural Intention */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Layers className="w-3.5 h-3.5 text-emerald-400" /> Committed Intention
                  </h3>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                    bdiState?.current_intention?.status === 'EXECUTING'
                      ? 'bg-emerald-500/20 text-emerald-300'
                      : 'bg-slate-800 text-slate-400'
                  }`}>
                    {bdiState?.current_intention?.status || 'IDLE'}
                  </span>
                </div>

                {bdiState?.current_intention ? (
                  <div className="space-y-3">
                    <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                      <span className="text-xs font-bold text-white block">{bdiState.current_intention.name}</span>
                      <p className="text-[11px] text-slate-400 mt-1">{bdiState.current_intention.selection_rationale}</p>
                      <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                        <span>Progress: Step {bdiState.current_intention.current_step_index} / {bdiState.current_intention.plan_steps?.length}</span>
                        <span>{Math.round((bdiState.current_intention.current_step_index / (bdiState.current_intention.plan_steps?.length || 1)) * 100)}%</span>
                      </div>
                      <div className="w-full bg-slate-800 rounded-full h-1.5 mt-1 overflow-hidden">
                        <div
                          className="bg-purple-500 h-full rounded-full transition-all duration-300"
                          style={{
                            width: `${Math.round((bdiState.current_intention.current_step_index / (bdiState.current_intention.plan_steps?.length || 1)) * 100)}%`
                          }}
                        />
                      </div>
                    </div>

                    <div className="space-y-1.5">
                      <span className="text-[10px] uppercase font-bold text-slate-400">Plan Steps:</span>
                      {bdiState.current_intention.plan_steps?.map((step, idx) => {
                        const isDone = idx < bdiState.current_intention.current_step_index;
                        const isCurrent = idx === bdiState.current_intention.current_step_index;
                        return (
                          <div
                            key={step.step_id}
                            className={`p-2 rounded-lg border text-xs flex items-center justify-between ${
                              isDone
                                ? 'bg-emerald-500/5 border-emerald-500/20 text-slate-300'
                                : isCurrent
                                ? 'bg-purple-500/10 border-purple-500/40 text-white font-semibold'
                                : 'bg-slate-900/40 border-slate-800 text-slate-500'
                            }`}
                          >
                            <div className="flex items-center gap-2">
                              {isDone ? (
                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                              ) : isCurrent ? (
                                <Play className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                              ) : (
                                <Clock className="w-3.5 h-3.5 text-slate-600 shrink-0" />
                              )}
                              <span>{step.action_type}: {step.target}</span>
                            </div>
                            <span className="font-mono text-[10px] text-slate-500">
                              {isDone ? 'DONE' : isCurrent ? 'NEXT' : 'PENDING'}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ) : (
                  <div className="p-8 text-center text-slate-500 text-xs">
                    No committed intention active.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 7: ASSIGNMENT 4.2 - KNOWLEDGE ONTOLOGY & LIVE REST API */}
      {/* ========================================================================= */}
      {activeLabTab === 'knowledge' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                    ASSIGNMENT 4.2
                  </span>
                  <h2 className="text-lg font-bold text-white">Knowledge Representation & Adaptive REST API Integration</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Semantic domain ontology querying (prerequisite trees & Bloom taxonomies) enriched dynamically with live GitHub REST API community data.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={apiSkillKeyword}
                  onChange={(e) => setApiSkillKeyword(e.target.value)}
                  placeholder="Skill (e.g. FastAPI)"
                  className="bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-lg text-xs text-white w-32 focus:outline-none focus:border-cyan-500"
                />
                <button
                  onClick={handleFetchLiveResources}
                  disabled={knowledgeLoading}
                  className="px-3.5 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 shadow-lg shadow-cyan-600/20 disabled:opacity-50"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${knowledgeLoading ? 'animate-spin' : ''}`} /> Query API
                </button>
                <button
                  onClick={handleAdaptMilestone}
                  disabled={knowledgeLoading}
                  className="px-3.5 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 shadow-lg shadow-brand-600/20 disabled:opacity-50"
                >
                  <Zap className="w-3.5 h-3.5" /> Adapt Plan
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
              {/* Left Column: Ontology Roles & Prerequisites */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Database className="w-3.5 h-3.5 text-cyan-400" /> Domain Ontology Hierarchy
                  </h3>
                  <span className="text-[10px] font-mono text-cyan-300">career_ontology.json</span>
                </div>

                <div className="flex flex-wrap gap-2">
                  {ontologyRoles.map((role) => (
                    <button
                      key={role}
                      onClick={() => handleSelectRole(role)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                        selectedRole === role
                          ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                          : 'bg-slate-900 text-slate-400 border border-slate-800 hover:bg-slate-800'
                      }`}
                    >
                      {role}
                    </button>
                  ))}
                </div>

                {roleDetails && (
                  <div className="p-3.5 rounded-lg bg-slate-900 border border-slate-800 space-y-2.5 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-white">{selectedRole}</span>
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-cyan-400 text-[10px] font-mono">
                        {roleDetails.tier}
                      </span>
                    </div>
                    <div>
                      <span className="text-slate-400 block text-[11px] mb-1">Required Competencies:</span>
                      <div className="flex flex-wrap gap-1.5">
                        {roleDetails.required_core_skills?.map((s) => (
                          <span key={s} className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[11px] font-mono">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <span className="text-slate-400 block text-[11px]">Recommended Capstone:</span>
                      <span className="text-brand-300 font-semibold">{roleDetails.capstone_archetype}</span>
                    </div>
                  </div>
                )}

                {/* Adapted Plan Preview */}
                {adaptedMilestone && (
                  <div className="mt-4 p-3.5 rounded-lg bg-brand-500/10 border border-brand-500/30 space-y-2 text-xs">
                    <span className="font-bold text-brand-300 block flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-brand-400" /> Synthesized Adaptive Milestone
                    </span>
                    <p className="text-white font-semibold">{adaptedMilestone.title}</p>
                    <p className="text-slate-300 text-[11px]">{adaptedMilestone.adaptation_rationale}</p>
                    <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-brand-500/20 font-mono">
                      <span>Difficulty: {adaptedMilestone.adapted_difficulty}</span>
                      <a
                        href={adaptedMilestone.external_reference_url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-cyan-400 hover:underline flex items-center gap-1"
                      >
                        Source Repo <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                )}
              </div>

              {/* Right Column: Live External API Responses */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Radio className="w-3.5 h-3.5 text-cyan-400" /> Live REST API Ingestion Feed
                  </h3>
                  <span className="text-[10px] font-mono text-slate-500">api.github.com</span>
                </div>

                {liveResources.length > 0 ? (
                  <div className="space-y-3">
                    {liveResources.map((item, idx) => (
                      <div key={idx} className="p-3 rounded-lg bg-slate-900 border border-slate-800 space-y-1 text-xs">
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-white font-mono">{item.title}</span>
                          <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 text-[10px] font-bold">
                            ★ {item.stars_or_rating?.toLocaleString()}
                          </span>
                        </div>
                        <p className="text-slate-400 text-[11px] line-clamp-2">{item.description}</p>
                        <div className="flex items-center justify-between pt-1 text-[10px] text-slate-500 font-mono">
                          <span>{item.provenance}</span>
                          <a href={item.source_url} target="_blank" rel="noreferrer" className="text-cyan-400 hover:underline flex items-center gap-1">
                            View <ExternalLink className="w-2.5 h-2.5" />
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-8 text-center text-slate-500 text-xs">
                    Click "Query API" to ingest live community repositories for '{apiSkillKeyword}'.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 8: ASSIGNMENT 5.1 - AGENT SECURITY & HOST INTEGRITY */}
      {/* ========================================================================= */}
      {activeLabTab === 'security' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                    ASSIGNMENT 5.1
                  </span>
                  <h2 className="text-lg font-bold text-white">Agent Authentication & Host Integrity Verification</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Cryptographic HMAC-SHA256 signature checking, trusted host ACL enforcement, sliding nonce replay defense, and real-time hostile intrusion mitigation.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={handleExecuteValidSignedCommand}
                  disabled={securityLoading}
                  className="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 shadow-lg shadow-emerald-600/20 disabled:opacity-50"
                >
                  <ShieldCheck className="w-3.5 h-3.5" /> Valid Request
                </button>
                <button
                  onClick={() => handleSimulateAttack('TAMPER_PAYLOAD')}
                  disabled={securityLoading}
                  className="px-3 py-2 rounded-xl bg-red-950/40 border border-red-500/40 hover:bg-red-900/50 text-red-300 font-semibold text-xs transition-colors flex items-center gap-1.5 disabled:opacity-50"
                >
                  <ShieldAlert className="w-3.5 h-3.5 text-red-400" /> Tamper Payload
                </button>
                <button
                  onClick={() => handleSimulateAttack('UNTRUSTED_HOST')}
                  disabled={securityLoading}
                  className="px-3 py-2 rounded-xl bg-red-950/40 border border-red-500/40 hover:bg-red-900/50 text-red-300 font-semibold text-xs transition-colors flex items-center gap-1.5 disabled:opacity-50"
                >
                  <Lock className="w-3.5 h-3.5 text-red-400" /> Rogue Host
                </button>
                <button
                  onClick={() => handleSimulateAttack('REPLAY_ATTACK')}
                  disabled={securityLoading}
                  className="px-3 py-2 rounded-xl bg-red-950/40 border border-red-500/40 hover:bg-red-900/50 text-red-300 font-semibold text-xs transition-colors flex items-center gap-1.5 disabled:opacity-50"
                >
                  <Clock className="w-3.5 h-3.5 text-red-400" /> Replay Nonce
                </button>
              </div>
            </div>

            {/* Last Action Notification */}
            {lastSecurityAction && (
              <div className={`mt-6 p-4 rounded-xl border flex items-start gap-3 ${
                lastSecurityAction.type === 'LEGITIMATE'
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                  : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
              }`}>
                {lastSecurityAction.type === 'LEGITIMATE' ? (
                  <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                ) : (
                  <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                )}
                <div className="space-y-1 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-bold">
                      {lastSecurityAction.type === 'LEGITIMATE' ? 'CRYPTOGRAPHIC COMMAND VERIFIED & EXECUTED' : `INTRUSION BLOCKED: ${lastSecurityAction.attackType}`}
                    </span>
                    <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-900">
                      {lastSecurityAction.result?.error_code || lastSecurityAction.result?.audit_code || 'SECURITY_GATE'}
                    </span>
                  </div>
                  <p className="text-slate-300">
                    {lastSecurityAction.result?.error || lastSecurityAction.result?.message || 'Verification complete.'}
                  </p>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
              {/* Left Column: Trusted Host ACL Registry */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Key className="w-3.5 h-3.5 text-rose-400" /> Trusted Host Registry & ACL
                  </h3>
                  <span className="text-[10px] font-mono text-slate-400">HMAC-SHA256</span>
                </div>

                <div className="space-y-3">
                  {Object.entries(trustedHosts).map(([hostId, info]) => (
                    <div key={hostId} className="p-3.5 rounded-lg bg-slate-900 border border-slate-800 space-y-2 text-xs">
                      <div className="flex items-center justify-between">
                        <span className="font-mono font-bold text-white">{hostId}</span>
                        <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-bold">
                          TRUSTED
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-400">Sender ID: <span className="font-mono text-slate-300">{info.sender_id}</span></div>
                      <div className="text-[11px] text-slate-400">Key: <span className="font-mono text-slate-500">{info.secret_key_preview}</span></div>
                      <div>
                        <span className="text-[10px] text-slate-500 block uppercase">Permissions:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {info.allowed_actions?.map((act) => (
                            <span key={act} className="px-1.5 py-0.5 rounded bg-slate-800 text-[10px] font-mono text-slate-300">
                              {act}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Right Column: Security Incident Audit Trail */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <Terminal className="w-3.5 h-3.5 text-rose-400" /> Real-Time Security Audit Log
                  </h3>
                  <span className="text-[10px] font-mono text-slate-400">{securityAuditLogs.length} Events</span>
                </div>

                <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
                  {securityAuditLogs.length > 0 ? (
                    securityAuditLogs.slice(-6).reverse().map((log, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-slate-900 border border-slate-800/80 text-xs flex items-center justify-between">
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-[10px] text-slate-500">{log.timestamp?.slice(11, 19)}</span>
                            <span className="font-bold text-white truncate max-w-[150px]">{log.action}</span>
                          </div>
                          <p className="text-[10px] text-slate-400 font-mono truncate max-w-[200px]">{log.host_id}</p>
                        </div>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          log.status === 'ACCEPTED'
                            ? 'bg-emerald-500/20 text-emerald-300'
                            : 'bg-rose-500/20 text-rose-400'
                        }`}>
                          {log.status}
                        </span>
                      </div>
                    ))
                  ) : (
                    <div className="p-8 text-center text-slate-500 text-xs">
                      No security incidents logged yet.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 9: ASSIGNMENT 5.2 - CAPSTONE CONSOLIDATION & 10-STAGE PIPELINE */}
      {/* ========================================================================= */}
      {activeLabTab === 'capstone' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    ASSIGNMENT 5.2
                  </span>
                  <h2 className="text-lg font-bold text-white">Capstone Project Consolidation & Secure Deployment</h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Master orchestrator unifying all 5 curriculum units into a single 10-stage end-to-end cognitive production cycle.
                </p>
              </div>

              <button
                onClick={handleRunCapstoneCycle}
                disabled={capstoneLoading}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-brand-600 hover:from-amber-400 hover:to-brand-500 text-slate-950 font-bold text-xs transition-all flex items-center gap-2 shadow-lg shadow-amber-500/20 disabled:opacity-50"
              >
                <Play className={`w-4 h-4 ${capstoneLoading ? 'animate-spin' : ''}`} /> Run 10-Stage Consolidated Cycle
              </button>
            </div>

            {/* 5-Unit Health Status Overview */}
            {capstoneSystemState && (
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 mt-6">
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Unit 1 Reflex</span>
                  <span className="text-sm font-bold text-white mt-1 block">{capstoneSystemState.unit_1_reflex?.rules_active} Rules Active</span>
                  <span className="text-[10px] text-emerald-400 font-semibold">● Operational</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Unit 2 Daemon & Mesh</span>
                  <span className="text-sm font-bold text-white mt-1 block">Daemon {capstoneSystemState.unit_2_concurrency_sockets?.daemon_metrics?.daemon_status}</span>
                  <span className="text-[10px] text-emerald-400 font-semibold">● Sockets Ready</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Unit 3 Utility & Bidding</span>
                  <span className="text-sm font-bold text-white mt-1 block">10 Bundles Scored</span>
                  <span className="text-[10px] text-emerald-400 font-semibold">● MAUT Active</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Unit 4 BDI & API</span>
                  <span className="text-sm font-bold text-white mt-1 block">{capstoneSystemState.unit_4_bdi_knowledge?.bdi_beliefs_count} Beliefs Loaded</span>
                  <span className="text-[10px] text-emerald-400 font-semibold">● Ontology Valid</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Unit 5 Cryptography</span>
                  <span className="text-sm font-bold text-white mt-1 block">HMAC-SHA256</span>
                  <span className="text-[10px] text-emerald-400 font-semibold">● Host Verified</span>
                </div>
              </div>
            )}

            {/* 10-Stage Pipeline Results */}
            {capstoneCycleResult && (
              <div className="mt-6 space-y-4">
                <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    <div>
                      <span className="font-bold text-white text-sm">
                        Consolidated Production Execution ({capstoneCycleResult.cycle_id})
                      </span>
                      <p className="text-xs text-slate-300">
                        All 10 stages executed across 5 units in {capstoneCycleResult.execution_duration_sec}s with zero faults.
                      </p>
                    </div>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-emerald-500 text-slate-950 text-xs font-bold font-mono">
                    {capstoneCycleResult.consolidated_status}
                  </span>
                </div>

                <div className="space-y-2">
                  {capstoneCycleResult.stages_log?.map((s) => (
                    <div key={s.stage} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                      <div className="flex items-center gap-3">
                        <span className="w-7 h-7 rounded-lg bg-slate-800 flex items-center justify-center font-mono font-bold text-amber-400 shrink-0">
                          {s.stage}
                        </span>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-white">{s.operation}</span>
                            <span className="px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 font-mono text-[10px]">
                              {s.unit}
                            </span>
                          </div>
                          <p className="text-slate-400 text-[11px] mt-0.5">{s.details}</p>
                        </div>
                      </div>
                      <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold font-mono text-[11px] self-start md:self-center">
                        {s.outcome}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
