import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Badge from '../components/Badge';
import ProgressBar from '../components/ProgressBar';
import {
  Target,
  ArrowRight,
  TrendingUp,
  FolderGit2,
  AlertCircle,
  ArrowRightLeft,
  Sparkles,
  ChevronDown
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';

export default function SkillGapPage({ currentStudent, setActiveTab }) {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState(currentStudent?.target_role || 'Data Analyst');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  // Role Comparison State
  const [compareRole, setCompareRole] = useState('Data Scientist');
  const [comparisonResult, setComparisonResult] = useState(null);
  const [comparing, setComparing] = useState(false);

  useEffect(() => {
    api.getCareers().then(data => {
      setRoles(data);
      if (currentStudent?.target_role) {
        setSelectedRole(currentStudent.target_role);
      }
    }).catch(err => console.error(err));
  }, [currentStudent]);

  useEffect(() => {
    if (!currentStudent?.id || !selectedRole) return;
    setLoading(true);
    api.analyzeSkillGaps(currentStudent.id, selectedRole)
      .then(res => {
        setAnalysis(res);
        setErrorMsg('');
      })
      .catch(err => {
        setErrorMsg(err.message || 'Failed to analyze skill gaps.');
      })
      .finally(() => setLoading(false));
  }, [currentStudent, selectedRole]);

  const handleRunComparison = async () => {
    if (!selectedRole || !compareRole || selectedRole === compareRole) return;
    setComparing(true);
    try {
      const studentSkillsDict = {};
      (currentStudent?.skills || []).forEach(s => {
        studentSkillsDict[s.skill_name.toLowerCase()] = s.proficiency;
      });

      const res = await api.compareCareers(selectedRole, compareRole, studentSkillsDict);
      setComparisonResult(res);
    } catch (err) {
      console.error("Role comparison failed:", err);
    } finally {
      setComparing(false);
    }
  };

  if (!currentStudent) {
    return (
      <div className="text-center py-20 space-y-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 flex items-center justify-center mx-auto">
          <Target className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-white">Student Profile Required</h2>
        <p className="text-xs text-slate-400">Complete onboarding to run deterministic skill gap analysis.</p>
        <button
          onClick={() => setActiveTab('onboarding')}
          className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs transition-all"
        >
          Go to Onboarding
        </button>
      </div>
    );
  }

  const chartData = (analysis?.gaps || []).map(g => ({
    skill: g.skill_name.length > 14 ? g.skill_name.substring(0, 13) + '…' : g.skill_name,
    Current: g.current_proficiency,
    Target: g.target_proficiency,
    Gap: g.gap
  }));

  return (
    <div className="space-y-6 py-6">
      {/* Top Header & Role Selector */}
      <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 sm:p-6 shadow-xl backdrop-blur-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono">
              <Target className="w-3.5 h-3.5" />
              <span>Skill Gap Evaluation Engine (0 to 5 Metric)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Role Competency Benchmark
            </h1>
            <p className="text-xs text-slate-400 font-mono">
              Formula: <code className="bg-slate-950 px-1.5 py-0.5 rounded text-emerald-300 font-mono">Gap = max(0, Target - Current)</code>
            </p>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-300 font-medium">Target Role:</label>
            <div className="relative">
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="appearance-none bg-slate-950 border border-slate-800 hover:border-slate-700 rounded-xl pl-3 pr-8 py-2 text-xs font-semibold text-white focus:outline-none focus:border-emerald-500/50 transition-colors cursor-pointer"
              >
                {roles.map(r => (
                  <option key={r.id} value={r.title}>{r.title}</option>
                ))}
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
            </div>
          </div>
        </div>

        {/* Overall Match Progress */}
        {analysis && (
          <div className="mt-5 pt-4 border-t border-slate-800/80 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <span className="text-xs font-semibold text-slate-200">
                Overall Competency Match for {analysis.target_role}:
              </span>
              <span className="text-xs font-mono font-bold text-emerald-400">
                {analysis.matched_skills_count} of {analysis.total_skills_evaluated} skills satisfied ({analysis.overall_match_percentage}%)
              </span>
            </div>
            <ProgressBar value={analysis.overall_match_percentage} max={100} showPercentage={false} />
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/80 p-3.5 rounded-xl border border-slate-850">
              {analysis.summary}
            </p>
          </div>
        )}
      </div>

      {errorMsg && (
        <div className="bg-rose-950/60 border border-rose-500/30 text-rose-300 p-3.5 rounded-xl text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Visual Chart: Current vs Target Proficiency */}
      {chartData.length > 0 && (
        <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
              <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
              <span>Skill Proficiency Distribution (Current vs Target Level)</span>
            </h2>
            <span className="text-[11px] text-slate-400 font-mono">Scale 0 (Not Learned) to 5 (Expert)</span>
          </div>

          <div className="h-64 sm:h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="skill" stroke="#64748b" tick={{ fontSize: 10, fill: '#94a3b8' }} angle={-20} textAnchor="end" />
                <YAxis domain={[0, 5]} stroke="#64748b" tick={{ fontSize: 10, fill: '#94a3b8' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#090d16', borderColor: '#1f293d', borderRadius: '8px', fontSize: '11px', color: '#fff' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="Current" fill="#0ea5e9" radius={[4, 4, 0, 0]} name="Current Level" />
                <Bar dataKey="Target" fill="#10b981" radius={[4, 4, 0, 0]} name="Target Requirement" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Detailed Skill Gap Matrix Table */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
            <Target className="w-3.5 h-3.5 text-emerald-400" />
            <span>Detailed Skill Gaps & Recommended Learning Activities</span>
          </h2>
          <span className="text-xs text-slate-400 font-mono">{analysis?.gaps?.length || 0} Skills Assessed</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px] tracking-wider font-mono">
                <th className="py-2.5 px-3">Skill Name</th>
                <th className="py-2.5 px-3 text-center">Current</th>
                <th className="py-2.5 px-3 text-center">Target</th>
                <th className="py-2.5 px-3 text-center">Gap Size</th>
                <th className="py-2.5 px-3">Priority & Rationale</th>
                <th className="py-2.5 px-3">Recommended Practical Activity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {(analysis?.gaps || []).map((gap, idx) => (
                <tr key={idx} className="hover:bg-slate-850/40 transition-colors">
                  <td className="py-3 px-3 font-semibold text-white">
                    <div>{gap.skill_name}</div>
                    {gap.prerequisites?.length > 0 && (
                      <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                        Prereqs: {gap.prerequisites.join(', ')}
                      </div>
                    )}
                  </td>
                  <td className="py-3 px-3 text-center font-mono text-slate-300">
                    <span className="px-2 py-0.5 rounded bg-slate-800/80">{gap.current_proficiency}/5</span>
                  </td>
                  <td className="py-3 px-3 text-center font-mono text-emerald-400 font-bold">
                    <span className="px-2 py-0.5 rounded bg-emerald-950/40 border border-emerald-500/20">{gap.target_proficiency}/5</span>
                  </td>
                  <td className="py-3 px-3 text-center font-mono font-bold">
                    {gap.gap > 0 ? (
                      <span className="text-amber-400">+{gap.gap}</span>
                    ) : (
                      <span className="text-emerald-400">0 (Met)</span>
                    )}
                  </td>
                  <td className="py-3 px-3 max-w-xs">
                    <div className="mb-1">
                      <Badge variant={gap.priority} size="xs">{gap.priority} Priority</Badge>
                    </div>
                    <p className="text-[11px] text-slate-300 leading-tight">{gap.reason}</p>
                  </td>
                  <td className="py-3 px-3 max-w-sm">
                    <p className="text-[11px] text-slate-200 leading-tight mb-1">{gap.recommended_activity}</p>
                    {gap.suggested_project && (
                      <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1 mt-1">
                        <FolderGit2 className="w-3 h-3" />
                        <span>Project: {gap.suggested_project}</span>
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Role Comparison Tool */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
              <ArrowRightLeft className="w-3.5 h-3.5 text-purple-400" />
              <span>Career Transition Feasibility Comparator</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Simulate switching target roles to evaluate transferable skills and learning effort.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <select
              value={compareRole}
              onChange={(e) => setCompareRole(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-500 transition-colors"
            >
              {roles.filter(r => r.title !== selectedRole).map(r => (
                <option key={r.id} value={r.title}>{r.title}</option>
              ))}
            </select>

            <button
              onClick={handleRunComparison}
              disabled={comparing}
              className="px-3.5 py-1.5 bg-purple-600 hover:bg-purple-500 text-white font-semibold rounded-xl text-xs flex items-center gap-1.5 transition-colors disabled:opacity-50"
            >
              <Sparkles className="w-3 h-3" />
              <span>{comparing ? 'Comparing...' : 'Compare Roles'}</span>
            </button>
          </div>
        </div>

        {comparisonResult && (
          <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              <div className="bg-slate-950/80 border border-slate-850 rounded-xl p-3">
                <span className="text-[10px] text-slate-400 uppercase font-mono font-semibold">Transition Feasibility</span>
                <div className="text-sm font-bold text-white mt-1">
                  <Badge variant={comparisonResult.transition_feasibility === 'Smooth' ? 'completed' : 'high'}>
                    {comparisonResult.transition_feasibility}
                  </Badge>
                </div>
              </div>

              <div className="bg-slate-950/80 border border-slate-850 rounded-xl p-3">
                <span className="text-[10px] text-slate-400 uppercase font-mono font-semibold">Directly Transferable</span>
                <div className="text-sm font-bold text-emerald-400 mt-1 font-mono">
                  {comparisonResult.transferable_skills.length} Skills
                </div>
              </div>

              <div className="bg-slate-950/80 border border-slate-850 rounded-xl p-3">
                <span className="text-[10px] text-slate-400 uppercase font-mono font-semibold">Est. Additional Effort</span>
                <div className="text-sm font-bold text-amber-400 mt-1 font-mono">
                  ~{comparisonResult.estimated_additional_weeks} Weeks
                </div>
              </div>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-850 text-xs text-slate-300">
              <span className="font-semibold text-white">Agent Recommendation: </span>
              {comparisonResult.recommendation}
            </div>

            <div className="flex flex-wrap gap-1.5 text-xs">
              <span className="text-slate-400 font-medium text-[11px]">Transferable:</span>
              {comparisonResult.transferable_skills.map((s, idx) => (
                <span key={idx} className="px-2 py-0.5 rounded-md bg-emerald-950/50 border border-emerald-500/20 text-emerald-300 font-mono text-[10px]">
                  ✓ {s}
                </span>
              ))}
            </div>

            <div className="flex flex-wrap gap-1.5 text-xs">
              <span className="text-slate-400 font-medium text-[11px]">New Skills Needed:</span>
              {comparisonResult.new_skills_needed.map((s, idx) => (
                <span key={idx} className="px-2 py-0.5 rounded-md bg-purple-950/50 border border-purple-500/20 text-purple-300 font-mono text-[10px]">
                  + {s}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
