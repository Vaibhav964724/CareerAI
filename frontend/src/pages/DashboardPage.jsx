import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import StatCard from '../components/StatCard';
import ProgressBar from '../components/ProgressBar';
import Badge from '../components/Badge';
import {
  Compass,
  Target,
  CheckCircle2,
  Clock,
  AlertTriangle,
  RotateCw,
  Sparkles,
  ArrowRight,
  TrendingUp,
  Cpu,
  Layers,
  ChevronRight,
  User
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip
} from 'recharts';

export default function DashboardPage({ currentStudent, setActiveTab }) {
  const [roadmap, setRoadmap] = useState(null);
  const [skillGaps, setSkillGaps] = useState([]);
  const [nextAction, setNextAction] = useState(null);
  const [recentObs, setRecentObs] = useState([]);
  const [evaluating, setEvaluating] = useState(false);
  const [evalReport, setEvalReport] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    if (!currentStudent?.id) {
      setLoading(false);
      return;
    }
    setLoading(true);
    try {
      try {
        const rmData = await api.getActiveRoadmap(currentStudent.id);
        setRoadmap(rmData);
      } catch (err) {
        setRoadmap(null);
      }

      try {
        const gapData = await api.analyzeSkillGaps(currentStudent.id, currentStudent.target_role);
        setSkillGaps(gapData.gaps || []);
      } catch (err) {
        setSkillGaps([]);
      }

      try {
        const actionData = await api.getNextBestAction(currentStudent.id);
        setNextAction(actionData);
      } catch (err) {
        setNextAction(null);
      }

      try {
        const obsData = await api.getAgentObservations(currentStudent.id);
        setRecentObs(obsData.slice(0, 5));
      } catch (err) {
        setRecentObs([]);
      }

    } catch (err) {
      console.error("Dashboard data fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [currentStudent]);

  const handleRunEvaluation = async () => {
    if (!currentStudent?.id) return;
    setEvaluating(true);
    try {
      const res = await api.evaluateAgent(currentStudent.id, 'manual_dashboard_evaluation');
      setEvalReport(res);
      await fetchDashboardData();
    } catch (err) {
      console.error("Evaluation cycle failed:", err);
    } finally {
      setEvaluating(false);
    }
  };

  if (!currentStudent) {
    return (
      <div className="text-center py-20 space-y-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 flex items-center justify-center mx-auto">
          <User className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-white">No Student Profile Loaded</h2>
        <p className="text-xs text-slate-400 leading-relaxed">
          Please complete student onboarding to establish your academic standing, current skills, and target career role.
        </p>
        <button
          onClick={() => setActiveTab('onboarding')}
          className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs shadow-md transition-all"
        >
          Create Student Profile
        </button>
      </div>
    );
  }

  const completedCount = roadmap?.completed_milestones_count || 0;
  const totalCount = roadmap?.total_milestones_count || 0;
  const pendingCount = totalCount - completedCount;
  const completionPct = roadmap?.completion_percentage || 0;

  const pieData = [
    { name: 'Completed', value: completedCount, color: '#10b981' },
    { name: 'Remaining', value: Math.max(0, pendingCount), color: '#334155' }
  ];

  return (
    <div className="space-y-6 py-6">
      {/* Top Profile Header Banner */}
      <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 sm:p-6 shadow-xl backdrop-blur-sm relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-5">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ACTIVE STUDENT #{currentStudent.id}
              </span>
              <span className="text-xs text-slate-400 font-mono">• {currentStudent.year_of_study ? `Year ${currentStudent.year_of_study}` : 'College Student'}</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Welcome back, {currentStudent.name}
            </h1>
            <p className="text-xs sm:text-sm text-slate-300">
              Target Career: <strong className="text-emerald-400 font-semibold">{currentStudent.target_role}</strong> • {currentStudent.degree} ({currentStudent.branch}) • <span className="font-mono text-slate-300">{currentStudent.weekly_hours} hrs/week</span>
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
            <button
              onClick={handleRunEvaluation}
              disabled={evaluating}
              className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs shadow-md shadow-emerald-500/15 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
              {evaluating ? (
                <>
                  <RotateCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Agent Evaluating...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Run Agent Evaluation</span>
                </>
              )}
            </button>

            <button
              onClick={() => setActiveTab('assistant')}
              className="px-4 py-2.5 bg-slate-850 hover:bg-slate-800 border border-slate-750 text-slate-200 font-semibold rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all"
            >
              <span>Ask Assistant</span>
              <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
            </button>
          </div>
        </div>

        {/* Evaluation Drawer Result */}
        {evalReport && (
          <div className="mt-5 pt-4 border-t border-slate-800">
            <div className="flex items-start justify-between gap-3">
              <div className="space-y-1.5 w-full">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Agent Cycle Completed ({evalReport.cycle_status})</span>
                </div>
                <div className="text-xs text-slate-300 whitespace-pre-line leading-relaxed font-sans bg-slate-950/80 p-3.5 rounded-xl border border-slate-850">
                  {evalReport.report_summary}
                </div>
              </div>
              <button
                onClick={() => setEvalReport(null)}
                className="text-slate-500 hover:text-slate-300 text-xs px-2 py-1 rounded"
              >
                ✕
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        <StatCard
          title="Roadmap Completion"
          value={`${completionPct}%`}
          subtitle={`${completedCount} of ${totalCount} milestones completed`}
          icon={TrendingUp}
          color="emerald"
          onClick={() => setActiveTab('roadmap')}
        />

        <StatCard
          title="Assessed Skill Gaps"
          value={skillGaps.filter(g => g.gap > 0).length}
          subtitle={`Across ${skillGaps.length} evaluated requirements`}
          icon={Target}
          color="amber"
          onClick={() => setActiveTab('skill-gaps')}
        />

        <StatCard
          title="Estimated Timeline"
          value={`${roadmap?.total_estimated_weeks || 0} Wks`}
          subtitle={`At ${currentStudent.weekly_hours} study hrs / week`}
          icon={Clock}
          color="blue"
        />

        <StatCard
          title="Roadmap Version"
          value={`v${roadmap?.version || 1}.0`}
          subtitle={roadmap?.status === 'active' ? 'Active & Monitored' : 'Initial Draft'}
          icon={Layers}
          color="purple"
          onClick={() => setActiveTab('progress')}
        />
      </div>

      {/* Recommended Next Action & Roadmap Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Next Best Action Card */}
        <div className="lg:col-span-2 bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono">
              <Cpu className="w-3.5 h-3.5" />
              <span>Recommended Next Action</span>
            </div>
            {nextAction && <Badge variant={nextAction.priority} withDot>{nextAction.priority} Priority</Badge>}
          </div>

          {nextAction ? (
            <div className="bg-slate-950/80 border border-slate-850 rounded-xl p-4 sm:p-5 space-y-2.5">
              <h3 className="text-sm sm:text-base font-bold text-white">{nextAction.title}</h3>
              <p className="text-xs text-slate-300 leading-relaxed">{nextAction.description}</p>
              <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 text-xs border-t border-slate-850/80">
                <span className="text-slate-400 text-[11px] italic">Rationale: {nextAction.reason}</span>
                <button
                  onClick={() => setActiveTab('roadmap')}
                  className="px-3.5 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded-lg font-semibold flex items-center gap-1.5 transition-colors self-start sm:self-auto text-xs"
                >
                  <span>Open Roadmap Milestone</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          ) : (
            <div className="text-xs text-slate-400 py-6 text-center border border-dashed border-slate-800 rounded-xl">
              Click &quot;Run Agent Evaluation&quot; above to generate your agent recommendation.
            </div>
          )}

          {/* Quick Skill Gap Highlights */}
          <div className="pt-1 space-y-2.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-300">Top Priority Skill Gaps</span>
              <button
                onClick={() => setActiveTab('skill-gaps')}
                className="text-emerald-400 hover:text-emerald-300 flex items-center gap-1 text-[11px] font-medium"
              >
                <span>View Full Matrix</span>
                <ChevronRight className="w-3 h-3" />
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {skillGaps.filter(g => g.gap > 0).slice(0, 4).map((g, idx) => (
                <div key={idx} className="bg-slate-950/60 border border-slate-850 rounded-xl p-3 flex items-center justify-between">
                  <div>
                    <div className="text-xs font-semibold text-white">{g.skill_name}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                      Current: {g.current_proficiency}/5 → Target: {g.target_proficiency}/5
                    </div>
                  </div>
                  <Badge variant={g.priority}>{g.gap} Level Gap</Badge>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Completion Donut & Summary Card */}
        <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between mb-1">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">Roadmap Progress</h3>
              <span className="text-[10px] text-emerald-400 font-mono">{completionPct}% Done</span>
            </div>
            <p className="text-xs text-slate-400">{currentStudent.target_role} Milestone Distribution</p>

            <div className="h-40 flex items-center justify-center my-1">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={46}
                    outerRadius={65}
                    paddingAngle={4}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#090d16', borderColor: '#1f293d', borderRadius: '8px', fontSize: '11px', color: '#fff' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="space-y-1.5 text-xs pt-1">
              <div className="flex justify-between items-center text-slate-300">
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400" />
                  Completed Milestones
                </span>
                <span className="font-mono font-bold text-white">{completedCount}</span>
              </div>
              <div className="flex justify-between items-center text-slate-300">
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-slate-600" />
                  Remaining Milestones
                </span>
                <span className="font-mono font-bold text-white">{pendingCount}</span>
              </div>
            </div>
          </div>

          <button
            onClick={() => setActiveTab('roadmap')}
            className="w-full py-2 bg-slate-850 hover:bg-slate-800 border border-slate-750 text-slate-200 font-semibold rounded-xl text-xs flex items-center justify-center gap-1.5 transition-colors"
          >
            <span>Open Interactive Roadmap</span>
            <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
          </button>
        </div>
      </div>

      {/* Recent Agent Decisions & Observations Feed */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">
            <Compass className="w-3.5 h-3.5 text-emerald-400" />
            <span>Recent Agent Decisions & Observations</span>
          </div>
          <button
            onClick={() => setActiveTab('progress')}
            className="text-xs text-emerald-400 hover:text-emerald-300 flex items-center gap-1 font-medium"
          >
            <span>Full Audit Trail</span>
            <ChevronRight className="w-3 h-3" />
          </button>
        </div>

        <div className="divide-y divide-slate-850">
          {recentObs.length > 0 ? (
            recentObs.map((obs) => (
              <div key={obs.id} className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                <div className="space-y-0.5">
                  <div className="font-semibold text-slate-200">{obs.summary}</div>
                  <div className="text-[10px] text-slate-400 font-mono">
                    Type: <span className="text-slate-300">{obs.observation_type}</span> • Timestamp: {new Date(obs.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                <Badge variant="in_progress" size="xs">Observed</Badge>
              </div>
            ))
          ) : (
            <div className="text-xs text-slate-400 py-4 text-center">
              No recent observations recorded. Run the evaluation cycle above to initiate agent logging.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
