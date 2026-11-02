import React from 'react';

export default function Badge({ children, variant = 'default', size = 'sm', withDot = false }) {
  const styles = {
    completed: 'bg-emerald-950/60 border-emerald-500/30 text-emerald-300',
    in_progress: 'bg-sky-950/60 border-sky-500/30 text-sky-300',
    not_started: 'bg-slate-800/80 border-slate-700/60 text-slate-300',
    blocked: 'bg-rose-950/60 border-rose-500/30 text-rose-300',
    high: 'bg-amber-950/60 border-amber-500/30 text-amber-300',
    critical: 'bg-rose-950/60 border-rose-500/30 text-rose-300',
    medium: 'bg-sky-950/60 border-sky-500/30 text-sky-300',
    low: 'bg-slate-800/80 border-slate-700/60 text-slate-400',
    active: 'bg-emerald-950/60 border-emerald-500/30 text-emerald-300',
    purple: 'bg-purple-950/60 border-purple-500/30 text-purple-300',
    default: 'bg-slate-800/80 border-slate-700/60 text-slate-300'
  };

  const dotColors = {
    completed: 'bg-emerald-400',
    in_progress: 'bg-sky-400 animate-pulse',
    not_started: 'bg-slate-500',
    blocked: 'bg-rose-400',
    high: 'bg-amber-400',
    critical: 'bg-rose-400 animate-ping',
    medium: 'bg-sky-400',
    low: 'bg-slate-500',
    active: 'bg-emerald-400',
    purple: 'bg-purple-400',
    default: 'bg-slate-400'
  };

  const sizeClasses = {
    xs: 'px-2 py-0.5 text-[10px]',
    sm: 'px-2.5 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm'
  };

  const normalized = (variant || 'default').toLowerCase().replace(' ', '_');
  const activeStyle = styles[normalized] || styles.default;
  const activeDot = dotColors[normalized] || dotColors.default;

  return (
    <span className={`inline-flex items-center gap-1.5 font-medium rounded-full border tracking-wide transition-colors ${activeStyle} ${sizeClasses[size] || sizeClasses.sm}`}>
      {withDot && <span className={`w-1.5 h-1.5 rounded-full ${activeDot}`} />}
      <span>{children}</span>
    </span>
  );
}
