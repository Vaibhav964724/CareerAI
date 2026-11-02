import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Cpu, Sparkles } from 'lucide-react';

export default function ModeBadge() {
  const [modeData, setModeData] = useState({ mode: 'rule-based', is_llm_active: false });

  useEffect(() => {
    api.getAgentMode()
      .then(res => setModeData(res))
      .catch(() => setModeData({ mode: 'rule-based', is_llm_active: false }));
  }, []);

  const isLLM = modeData.is_llm_active;

  return (
    <div
      title={isLLM ? "Anthropic Claude LLM integration is active." : "Operating in deterministic Rule-Based Fallback Mode without external API key required."}
      className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
        isLLM
          ? 'bg-purple-950/50 border-purple-500/30 text-purple-300'
          : 'bg-emerald-950/50 border-emerald-500/30 text-emerald-300'
      }`}
    >
      <span className="relative flex h-2 w-2">
        <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isLLM ? 'bg-purple-400' : 'bg-emerald-400'}`} />
        <span className={`relative inline-flex rounded-full h-2 w-2 ${isLLM ? 'bg-purple-500' : 'bg-emerald-500'}`} />
      </span>
      {isLLM ? (
        <span className="font-mono text-[11px]">Claude LLM Active</span>
      ) : (
        <span className="font-mono text-[11px]">Rule-Based (Zero-Cost)</span>
      )}
    </div>
  );
}
