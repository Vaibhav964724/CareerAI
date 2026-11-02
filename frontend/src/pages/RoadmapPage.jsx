import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import Badge from '../components/Badge';
import ProgressBar from '../components/ProgressBar';
import {
  MapPin,
  CheckCircle2,
  Clock,
  ExternalLink,
  FolderGit2,
  BookOpen,
  AlertOctagon,
  RotateCcw,
  Sparkles,
  Layers,
  ArrowRight,
  ChevronDown,
  ChevronUp,
  PlayCircle
} from 'lucide-react';

export default function RoadmapPage({ currentStudent, setActiveTab }) {
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState(null);
  const [expandedId, setExpandedId] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [successNotice, setSuccessNotice] = useState('');

  const fetchRoadmap = async () => {
    if (!currentStudent?.id) return;
    setLoading(true);
    try {
      const data = await api.getActiveRoadmap(currentStudent.id);
      setRoadmap(data);
      const firstActive = data.milestones.find(m => m.status === 'in_progress' || m.status === 'not_started');
      if (firstActive) {
        setExpandedId(firstActive.id);
      }
    } catch (err) {
      setRoadmap(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, [currentStudent]);

  const handleStatusChange = async (milestoneId, newStatus) => {
    setUpdatingId(milestoneId);
    setErrorMsg('');
    setSuccessNotice('');
    try {
      await api.updateMilestoneStatus(milestoneId, newStatus, `Student changed status to ${newStatus}`);
      setSuccessNotice(`Milestone marked as '${newStatus.replace('_', ' ')}'. Progress recalculated.`);
      await fetchRoadmap();
    } catch (err) {
      setErrorMsg(err.message || 'Failed to update milestone status.');
    } finally {
      setUpdatingId(null);
    }
  };

  const handleGenerateInitial = async () => {
    if (!currentStudent?.id) return;
    setLoading(true);
    try {
      await api.generateRoadmap(currentStudent.id, currentStudent.target_role, currentStudent.weekly_hours);
      await fetchRoadmap();
    } catch (err) {
      setErrorMsg(err.message || 'Failed to generate initial roadmap.');
    } finally {
      setLoading(false);
    }
  };

  if (!currentStudent) {
    return (
      <div className="text-center py-20 space-y-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 flex items-center justify-center mx-auto">
          <MapPin className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-white">Student Profile Required</h2>
        <p className="text-xs text-slate-400">Please complete onboarding to access your personalized roadmap.</p>
        <button
          onClick={() => setActiveTab('onboarding')}
          className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs"
        >
          Go to Onboarding
        </button>
      </div>
    );
  }

  if (!roadmap && !loading) {
    return (
      <div className="text-center py-16 space-y-4 bg-slate-900/60 border border-slate-800 rounded-3xl p-8 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto">
          <Sparkles className="w-6 h-6 animate-pulse" />
        </div>
        <h2 className="text-lg font-bold text-white">No Active Career Roadmap Found</h2>
        <p className="text-xs text-slate-400 leading-relaxed">
          CareerAI is ready to assemble a phased learning path for <strong className="text-emerald-300">{currentStudent.target_role}</strong> at {currentStudent.weekly_hours} hours/week.
        </p>
        <button
          onClick={handleGenerateInitial}
          className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs flex items-center justify-center gap-2 mx-auto shadow-md"
        >
          <span>Generate Personalized Roadmap Now</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  const phases = {};
  if (roadmap?.milestones) {
    roadmap.milestones.forEach(m => {
      const key = `Phase ${m.phase_number}: ${m.phase_name}`;
      if (!phases[key]) {
        phases[key] = [];
      }
      phases[key].push(m);
    });
  }

  return (
    <div className="space-y-6 py-6">
      {/* Top Banner */}
      <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 sm:p-6 shadow-xl backdrop-blur-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono">
              <MapPin className="w-3.5 h-3.5" />
              <span>Personalized Milestone Roadmap (Version {roadmap?.version || 1}.0)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              {roadmap?.target_role} Roadmap
            </h1>
            <p className="text-xs text-slate-400 font-mono">
              Estimated Duration: ~{roadmap?.total_estimated_weeks} Weeks • Based on {roadmap?.weekly_hours} study hrs/week commitment.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('progress')}
              className="px-3.5 py-1.5 bg-slate-850 hover:bg-slate-800 border border-slate-750 text-slate-200 text-xs font-medium rounded-xl flex items-center gap-1.5 transition-colors"
            >
              <Layers className="w-3.5 h-3.5 text-purple-400" />
              <span>Revision History</span>
            </button>
          </div>
        </div>

        {/* Overall Completion Bar */}
        <div className="pt-2">
          <ProgressBar
            value={roadmap?.completion_percentage || 0}
            max={100}
            label={`Milestone Completion (${roadmap?.completed_milestones_count || 0} of ${roadmap?.total_milestones_count || 0} Completed)`}
          />
        </div>
      </div>

      {successNotice && (
        <div className="bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 p-3.5 rounded-xl text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>{successNotice}</span>
        </div>
      )}

      {errorMsg && (
        <div className="bg-rose-950/60 border border-rose-500/30 text-rose-300 p-3.5 rounded-xl text-xs flex items-center gap-2">
          <AlertOctagon className="w-4 h-4 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Phased Milestones Sequence */}
      <div className="space-y-6">
        {Object.entries(phases).map(([phaseHeader, milestonesList], pIdx) => (
          <div key={pIdx} className="space-y-3">
            <div className="flex items-center gap-2.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">{phaseHeader}</h2>
              <span className="text-[10px] text-slate-500 font-mono">({milestonesList.length} Milestones)</span>
            </div>

            <div className="space-y-3 pl-3 sm:pl-4 border-l border-slate-800 ml-1">
              {milestonesList.map((m) => {
                const isExpanded = expandedId === m.id;
                const isCompleted = m.status === 'completed';
                const isInProgress = m.status === 'in_progress';
                const isBlocked = m.status === 'blocked';

                return (
                  <div
                    key={m.id}
                    className={`bg-slate-900/70 border rounded-2xl transition-all duration-200 overflow-hidden ${
                      isCompleted
                        ? 'border-emerald-500/30 bg-emerald-950/10'
                        : isInProgress
                        ? 'border-sky-500/40 shadow-lg shadow-sky-500/5'
                        : isBlocked
                        ? 'border-rose-500/30 bg-rose-950/10'
                        : 'border-slate-800 hover:border-slate-750'
                    }`}
                  >
                    {/* Header Item */}
                    <div className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="space-y-1.5 cursor-pointer flex-1" onClick={() => setExpandedId(isExpanded ? null : m.id)}>
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="text-xs font-mono text-slate-500 font-bold">#{m.order_index}</span>
                          <h3 className={`text-sm sm:text-base font-bold ${isCompleted ? 'line-through text-slate-400' : 'text-white'}`}>
                            {m.title}
                          </h3>
                          <Badge variant={m.status} withDot size="xs">{m.status.replace('_', ' ')}</Badge>
                          {m.priority && <Badge variant={m.priority} size="xs">{m.priority}</Badge>}
                        </div>

                        <div className="flex flex-wrap items-center gap-3 text-[11px] text-slate-400">
                          <span className="flex items-center gap-1 font-mono">
                            <Clock className="w-3 h-3 text-slate-500" />
                            <span>~{m.estimated_weeks} wks ({m.estimated_hours} hrs)</span>
                          </span>
                          {m.deadline && <span className="font-mono text-slate-400">Target: {m.deadline}</span>}
                          {m.required_skills?.length > 0 && (
                            <span className="text-slate-400">
                              Skills: <strong className="text-slate-300">{m.required_skills.join(', ')}</strong>
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Interactive Status Switcher Buttons */}
                      <div className="flex items-center gap-1.5 self-end sm:self-auto pt-1 sm:pt-0">
                        {m.status !== 'completed' && (
                          <button
                            disabled={updatingId === m.id}
                            onClick={() => handleStatusChange(m.id, 'completed')}
                            className="px-2.5 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors"
                            title="Mark as Completed"
                          >
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span className="hidden sm:inline">Complete</span>
                          </button>
                        )}

                        {m.status !== 'in_progress' && (
                          <button
                            disabled={updatingId === m.id}
                            onClick={() => handleStatusChange(m.id, 'in_progress')}
                            className="px-2.5 py-1.5 bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 border border-sky-500/30 rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors"
                            title="Mark as In Progress"
                          >
                            <PlayCircle className="w-3.5 h-3.5" />
                            <span className="hidden sm:inline">Start</span>
                          </button>
                        )}

                        {m.status !== 'not_started' && (
                          <button
                            disabled={updatingId === m.id}
                            onClick={() => handleStatusChange(m.id, 'not_started')}
                            className="px-2 py-1.5 bg-slate-800 hover:bg-slate-750 text-slate-400 hover:text-slate-200 border border-slate-700/60 rounded-lg text-xs transition-colors"
                            title="Reset to Not Started"
                          >
                            <RotateCcw className="w-3.5 h-3.5" />
                          </button>
                        )}

                        <button
                          onClick={() => setExpandedId(isExpanded ? null : m.id)}
                          className="p-1.5 text-slate-400 hover:text-white rounded-lg transition-colors ml-1"
                          aria-label={isExpanded ? 'Collapse milestone details' : 'Expand milestone details'}
                        >
                          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>

                    {/* Expandable Details Drawer */}
                    {isExpanded && (
                      <div className="border-t border-slate-800/80 bg-slate-950/60 p-4 sm:p-5 space-y-4 text-xs">
                        {m.description && (
                          <p className="text-slate-300 leading-relaxed">{m.description}</p>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {/* Recommended Resources */}
                          <div className="space-y-2">
                            <span className="text-[10px] font-mono text-emerald-400 uppercase font-semibold flex items-center gap-1.5">
                              <BookOpen className="w-3.5 h-3.5" />
                              <span>Recommended Study Materials</span>
                            </span>
                            {m.recommended_resources && m.recommended_resources.length > 0 ? (
                              <div className="space-y-1.5">
                                {m.recommended_resources.map((res, rIdx) => (
                                  <div key={rIdx} className="bg-slate-900 border border-slate-850 rounded-xl p-2.5 flex items-start justify-between gap-2">
                                    <div className="space-y-0.5">
                                      <div className="font-semibold text-white">{res.title}</div>
                                      <div className="text-[10px] text-slate-400 font-mono">
                                        Type: {res.type} • Est: {res.estimated_hours} hrs
                                      </div>
                                    </div>
                                    {res.url && (
                                      <a
                                        href={res.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-emerald-400 hover:text-emerald-300 p-1 flex-shrink-0"
                                      >
                                        <ExternalLink className="w-3.5 h-3.5" />
                                      </a>
                                    )}
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <p className="text-slate-500 italic text-[11px]">No specific resources listed.</p>
                            )}
                          </div>

                          {/* Deliverables / Project Tasks */}
                          <div className="space-y-2">
                            <span className="text-[10px] font-mono text-purple-400 uppercase font-semibold flex items-center gap-1.5">
                              <FolderGit2 className="w-3.5 h-3.5" />
                              <span>Practical Deliverables & Evidence</span>
                            </span>
                            {m.deliverables && m.deliverables.length > 0 ? (
                              <div className="space-y-1.5">
                                {m.deliverables.map((deliv, dIdx) => (
                                  <div key={dIdx} className="bg-slate-900 border border-slate-850 rounded-xl p-2.5 space-y-0.5">
                                    <div className="font-semibold text-white flex items-center gap-1.5">
                                      <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
                                      <span>{deliv.title}</span>
                                    </div>
                                    <p className="text-[11px] text-slate-400">{deliv.description}</p>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <p className="text-slate-500 italic text-[11px]">No project deliverables specified.</p>
                            )}
                          </div>
                        </div>

                        {/* Agent Decision Rationale */}
                        {m.agent_rationale && (
                          <div className="pt-2 border-t border-slate-850 text-[11px] text-slate-400">
                            <strong className="text-slate-300">Why CareerAI Placed This Here: </strong>
                            {m.agent_rationale}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
