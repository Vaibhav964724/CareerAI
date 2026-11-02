import React from 'react';
import { Sparkles, Terminal, BookOpen, ShieldCheck, Cpu } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-850/80 bg-slate-950/80 text-slate-400 py-10 text-xs mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="col-span-1 md:col-span-2 space-y-3">
            <div className="flex items-center gap-2 text-white font-bold text-sm">
              <div className="w-6 h-6 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                <Sparkles className="w-3.5 h-3.5" />
              </div>
              <span>CareerAI — College Agent Technology Capstone</span>
            </div>
            <p className="text-slate-400 max-w-md leading-relaxed text-xs">
              An Autonomous, Persistent, and Personalized AI Career Guidance Agent for College Students.
              Demonstrates continuous state observation, deterministic reasoning, tool execution, persistent SQLite memory, and adaptive replanning.
            </p>
            <div className="flex items-center gap-2 pt-1">
              <span className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-[10px] font-mono text-emerald-400">
                22/22 Tests Passing
              </span>
              <span className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-[10px] font-mono text-sky-400">
                Units 1–5 Implemented
              </span>
              <span className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-[10px] font-mono text-purple-400">
                FastAPI + React 18
              </span>
            </div>
          </div>

          <div>
            <h4 className="text-slate-200 font-semibold mb-3 text-xs tracking-wider uppercase">Agent Architecture</h4>
            <ul className="space-y-2 text-slate-400 text-xs">
              <li className="flex items-center gap-1.5">• <span>7-Stage Autonomous Loop</span></li>
              <li className="flex items-center gap-1.5">• <span>12 Dedicated Agent Tools</span></li>
              <li className="flex items-center gap-1.5">• <span>SQLite Persistent Memory</span></li>
              <li className="flex items-center gap-1.5">• <span>Claude LLM + Zero-Cost Fallback</span></li>
            </ul>
          </div>

          <div>
            <h4 className="text-slate-200 font-semibold mb-3 text-xs tracking-wider uppercase">Course Information</h4>
            <ul className="space-y-2 text-slate-400 text-xs">
              <li className="flex items-center gap-1.5">• <span>Course: Agent Technology</span></li>
              <li className="flex items-center gap-1.5">• <span>Faculty: Dr. Prabhu Sir</span></li>
              <li className="flex items-center gap-1.5">• <span>Student: Vaibhav Singh</span></li>
              <li className="flex items-center gap-1.5">• <span>Reg: RA2212704010040</span></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-900 pt-6 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500 gap-3">
          <p>© {new Date().getFullYear()} CareerAI. Academic Demonstration Prototype.</p>
          <div className="flex items-center gap-4 font-mono text-[11px]">
            <span>Backend: :8000</span>
            <span>Frontend: :5173</span>
            <span>API Docs: /docs</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
