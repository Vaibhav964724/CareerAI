import React, { useState } from 'react';
import ModeBadge from './ModeBadge';
import {
  Compass,
  LayoutDashboard,
  Target,
  MapPin,
  Bot,
  Activity,
  User,
  Menu,
  X,
  Sparkles,
  FlaskConical,
  ChevronDown
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, currentStudent, allStudents = [], onSelectStudent }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'landing', label: 'Home', icon: Compass },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'skill-gaps', label: 'Skill Gaps', icon: Target },
    { id: 'roadmap', label: 'Roadmap', icon: MapPin },
    { id: 'lab', label: 'Agent Lab', icon: FlaskConical },
    { id: 'assistant', label: 'Assistant', icon: Bot },
    { id: 'progress', label: 'Activity', icon: Activity },
    { id: 'onboarding', label: currentStudent ? 'Profile' : 'Onboard', icon: User },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-950/85 backdrop-blur-md border-b border-slate-800/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Branding */}
          <div
            onClick={() => setActiveTab('landing')}
            className="flex items-center gap-3 cursor-pointer group select-none"
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform duration-200">
              <Sparkles className="w-4 h-4 text-slate-950 font-bold" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base font-bold tracking-tight text-white group-hover:text-emerald-300 transition-colors">
                  CareerAI
                </span>
                <span className="text-[10px] px-1.5 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 font-mono border border-emerald-500/20 font-medium">
                  AGENT
                </span>
              </div>
              <p className="text-[10px] text-slate-400 hidden xl:block leading-none mt-0.5">
                Autonomous Career Guidance System
              </p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-slate-800/90 text-emerald-400 border border-slate-700/80 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-850/60'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-emerald-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Header: Student Badge & Mode Badge */}
          <div className="hidden sm:flex items-center gap-3">
            <ModeBadge />

            {/* Student Selector / Current Student Badge */}
            {allStudents && allStudents.length > 1 ? (
              <div className="relative flex items-center">
                <select
                  value={currentStudent?.id || ''}
                  onChange={(e) => onSelectStudent && onSelectStudent(Number(e.target.value))}
                  aria-label="Select Active Student Profile"
                  className="appearance-none bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs text-slate-200 font-medium rounded-xl pl-3 pr-8 py-1.5 focus:outline-none focus:border-emerald-500/50 transition-colors cursor-pointer"
                >
                  {allStudents.map(s => (
                    <option key={s.id} value={s.id}>
                      {s.name} • {s.target_role}
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 pointer-events-none" />
              </div>
            ) : currentStudent ? (
              <div
                onClick={() => setActiveTab('onboarding')}
                className="flex items-center gap-2 bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl px-3 py-1.5 cursor-pointer transition-colors"
                title="Click to view/edit profile"
              >
                <div className="w-5 h-5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center text-[10px] font-bold">
                  {currentStudent.name.charAt(0)}
                </div>
                <div className="text-left">
                  <div className="text-xs font-semibold text-white leading-none">{currentStudent.name}</div>
                  <div className="text-[10px] text-slate-400 leading-none mt-0.5">{currentStudent.target_role}</div>
                </div>
              </div>
            ) : null}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex lg:hidden items-center gap-2">
            <div className="sm:hidden">
              <ModeBadge />
            </div>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle navigation menu"
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-800 focus:outline-none transition-colors"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-slate-800 bg-slate-950/95 backdrop-blur-xl px-4 pt-3 pb-5 space-y-3">
          {currentStudent && (
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center text-xs font-bold">
                  {currentStudent.name.charAt(0)}
                </div>
                <div>
                  <div className="text-xs font-semibold text-white">{currentStudent.name}</div>
                  <div className="text-[10px] text-slate-400">{currentStudent.target_role} ({currentStudent.weekly_hours} hrs/wk)</div>
                </div>
              </div>
              {allStudents.length > 1 && (
                <select
                  value={currentStudent.id}
                  onChange={(e) => {
                    onSelectStudent && onSelectStudent(Number(e.target.value));
                    setMobileMenuOpen(false);
                  }}
                  aria-label="Switch active student"
                  className="bg-slate-850 border border-slate-700 text-[11px] text-slate-300 rounded-lg px-2 py-1"
                >
                  {allStudents.map(s => (
                    <option key={s.id} value={s.id}>{s.name}</option>
                  ))}
                </select>
              )}
            </div>
          )}

          <div className="grid grid-cols-2 gap-1.5 pt-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-slate-850 text-emerald-400 border border-slate-700'
                      : 'text-slate-400 hover:text-white hover:bg-slate-900'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
}
