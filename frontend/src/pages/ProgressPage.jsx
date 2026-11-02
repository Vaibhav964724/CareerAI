import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Badge from '../components/Badge';
import {
  Activity,
  CheckCircle2,
  Clock,
  Layers,
  Sparkles,
  FileText,
  ShieldCheck,
  Cpu
} from 'lucide-react';

export default function ProgressPage({ currentStudent, setActiveTab }) {
  const [observations, setObservations] = useState([]);
  const [actions, setActions] = useState([]);
  const [revisions, setRevisions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentStudent?.id) return;
    setLoading(true);

    Promise.all([
      api.getAgentObservations(currentStudent.id).catch(() => []),
      api.getAgentActions(currentStudent.id).catch(() => []),
      api.getRoadmapRevisions(currentStudent.id).catch(() => [])
    ]).then(([obsData, actsData, revData]) => {
      setObservations(obsData);
      setActions(actsData);
      setRevisions(revData);
    }).finally(() => {
      setLoading(false);
    });
  }, [currentStudent]);

  if (!currentStudent) {
    return (
      <div className="text-center py-20 space-y-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 flex items-center justify-center mx-auto">
          <Activity className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-white">Student Profile Required</h2>
        <p className="text-xs text-slate-400">Please onboard or select an active student to view progress and audit logs.</p>
        <button
          onClick={() => setActiveTab('onboarding')}
          className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs"
        >
          Go to Onboarding
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 py-6">
      {/* Top Banner */}
      <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 sm:p-6 shadow-xl backdrop-blur-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono">
              <Activity className="w-3.5 h-3.5" />
              <span>Audit Trail & Agent Observability</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Progress & Agent Decisions
            </h1>
            <p className="text-xs text-slate-400 font-mono">
              Chronological log of state observations, tool executions, and roadmap revisions for {currentStudent.name}.
            </p>
          </div>
        </div>
      </div>

      {/* Prominent Section: "Why CareerAI Recommended This" */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 border border-emerald-500/30 rounded-2xl p-5 sm:p-6 shadow-xl relative overflow-hidden">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base sm:text-lg font-bold text-white tracking-tight">Why CareerAI Recommended This</h2>
            <p className="text-xs text-slate-400">Transparent explanations behind the agent&apos;s autonomous decisions.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
          <div className="bg-slate-950/80 border border-slate-850 rounded-xl p-4 space-y-1.5">
            <div className="text-xs font-bold text-emerald-400 uppercase font-mono">1. Prerequisite-Aware Milestones</div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Foundational skills (such as SQL and Python) are scheduled first because advanced machine learning and data pipelines require those prerequisite competencies to succeed.
            </p>
          </div>

          <div className="bg-slate-950/80 border border-slate-850 rounded-xl p-4 space-y-1.5">
            <div className="text-xs font-bold text-sky-400 uppercase font-mono">2. Hours-Balanced Durations</div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Every milestone duration is computed deterministically from your stated commitment of <strong className="text-white">{currentStudent.weekly_hours} hrs/week</strong>, preventing burnout and unrealistic timelines.
            </p>
          </div>

          <div className="bg-slate-950/80 border border-slate-850 rounded-xl p-4 space-y-1.5">
            <div className="text-xs font-bold text-purple-400 uppercase font-mono">3. Completed Work Preservation</div>
            <p className="text-xs text-slate-300 leading-relaxed">
              When your target role or weekly hours change, the agent recalculates remaining requirements while strictly preserving your previously completed milestones and credentials.
            </p>
          </div>
        </div>
      </div>

      {/* Roadmap Revision History */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
            <Layers className="w-3.5 h-3.5 text-purple-400" />
            <span>Roadmap Revision History</span>
          </h2>
          <span className="text-xs text-slate-400 font-mono">{revisions.length} Revisions Recorded</span>
        </div>

        {revisions.length > 0 ? (
          <div className="space-y-2.5">
            {revisions.map((rev) => (
              <div key={rev.id} className="bg-slate-950/80 border border-slate-850 rounded-xl p-3.5 space-y-1.5 text-xs">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant="in_progress" size="xs">{rev.revision_trigger.replace('_', ' ')}</Badge>
                    <span className="font-semibold text-white">Revision #{rev.id}</span>
                  </div>
                  <span className="text-slate-500 font-mono text-[11px]">
                    {new Date(rev.created_at).toLocaleString()}
                  </span>
                </div>
                <p className="text-slate-300 leading-relaxed">{rev.summary}</p>
                <div className="text-[11px] text-emerald-400 font-mono">
                  Preserved Milestones: {rev.preserved_milestones_count}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-xs text-slate-400 py-6 text-center border border-dashed border-slate-800 rounded-xl">
            No roadmap revisions recorded yet. Revisions are logged when available hours or target roles change.
          </div>
        )}
      </div>

      {/* Chronological Persistent Observations */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-emerald-400" />
            <span>Agent Observations Timeline (SQLite Persistent Memory)</span>
          </h2>
          <span className="text-xs text-slate-400 font-mono">{observations.length} Observations</span>
        </div>

        {observations.length > 0 ? (
          <div className="divide-y divide-slate-850 text-xs">
            {observations.map((obs) => (
              <div key={obs.id} className="py-3 space-y-0.5">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-200">{obs.summary}</span>
                  <span className="text-[11px] text-slate-500 font-mono">
                    {new Date(obs.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                <div className="text-[10px] text-slate-400 font-mono">
                  Observation Type: <span className="text-slate-300">{obs.observation_type}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-xs text-slate-400 py-6 text-center border border-dashed border-slate-800 rounded-xl">
            No observations recorded yet.
          </div>
        )}
      </div>

      {/* Agent Action Execution Logs */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
            <FileText className="w-3.5 h-3.5 text-sky-400" />
            <span>Execution Stage Action Logs</span>
          </h2>
          <span className="text-xs text-slate-400 font-mono">{actions.length} Logs</span>
        </div>

        {actions.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px] font-mono">
                  <th className="py-2.5 px-3">Stage</th>
                  <th className="py-2.5 px-3">Action Name</th>
                  <th className="py-2.5 px-3">Reason / Context</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-850">
                {actions.map((act) => (
                  <tr key={act.id} className="hover:bg-slate-850/40">
                    <td className="py-2 px-3 font-mono font-bold text-slate-300">{act.stage}</td>
                    <td className="py-2 px-3 font-semibold text-white">{act.action_name}</td>
                    <td className="py-2 px-3 text-slate-400 max-w-sm truncate">{act.reason || 'Routine cycle step'}</td>
                    <td className="py-2 px-3">
                      <Badge variant={act.status} size="xs">{act.status}</Badge>
                    </td>
                    <td className="py-2 px-3 font-mono text-slate-500 text-[11px]">
                      {new Date(act.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-xs text-slate-400 py-6 text-center border border-dashed border-slate-800 rounded-xl">
            No action logs recorded yet.
          </div>
        )}
      </div>
    </div>
  );
}
