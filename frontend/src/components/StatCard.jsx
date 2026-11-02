import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, color = 'emerald', onClick }) {
  const colorMap = {
    emerald: {
      iconBg: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
      hoverBorder: 'hover:border-emerald-500/40'
    },
    blue: {
      iconBg: 'text-sky-400 bg-sky-500/10 border-sky-500/20',
      hoverBorder: 'hover:border-sky-500/40'
    },
    purple: {
      iconBg: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
      hoverBorder: 'hover:border-purple-500/40'
    },
    amber: {
      iconBg: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
      hoverBorder: 'hover:border-amber-500/40'
    },
    rose: {
      iconBg: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
      hoverBorder: 'hover:border-rose-500/40'
    }
  };

  const scheme = colorMap[color] || colorMap.emerald;

  return (
    <div
      onClick={onClick}
      className={`group relative bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 backdrop-blur-sm transition-all duration-200 ${
        onClick ? `cursor-pointer ${scheme.hoverBorder} hover:bg-slate-900 hover:shadow-lg hover:shadow-black/20` : ''
      }`}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-2 rounded-xl border transition-transform duration-200 group-hover:scale-105 ${scheme.iconBg}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>
      <div className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight font-sans">{value}</div>
      {subtitle && <p className="text-xs text-slate-400 mt-1.5 flex items-center gap-1.5">{subtitle}</p>}
    </div>
  );
}
