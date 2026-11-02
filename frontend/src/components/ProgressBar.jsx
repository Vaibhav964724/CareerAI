import React from 'react';

export default function ProgressBar({ value = 0, max = 100, label = '', showPercentage = true, color = 'emerald' }) {
  const percentage = Math.min(100, Math.max(0, Math.round((value / max) * 100))) || 0;

  const colorClasses = {
    emerald: 'bg-gradient-to-r from-emerald-500 to-teal-400',
    blue: 'bg-gradient-to-r from-sky-500 to-blue-400',
    purple: 'bg-gradient-to-r from-purple-500 to-indigo-400',
    amber: 'bg-gradient-to-r from-amber-500 to-yellow-400'
  };

  const activeColor = colorClasses[color] || colorClasses.emerald;

  return (
    <div className="w-full space-y-1.5">
      {(label || showPercentage) && (
        <div className="flex justify-between items-center text-xs font-medium text-slate-300">
          <span className="truncate">{label}</span>
          {showPercentage && <span className="font-mono font-semibold text-white ml-2">{percentage}%</span>}
        </div>
      )}
      <div className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden border border-slate-700/40 p-0.5">
        <div
          className={`h-full rounded-full transition-all duration-700 ease-out ${activeColor}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
