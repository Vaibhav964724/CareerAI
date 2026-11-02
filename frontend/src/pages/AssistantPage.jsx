import React, { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import ModeBadge from '../components/ModeBadge';
import {
  Bot,
  User,
  Send,
  Sparkles,
  Cpu,
  Clock,
  Target
} from 'lucide-react';

export default function AssistantPage({ currentStudent, setActiveTab }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState([
    "What should I learn this week?",
    `Which skills am I missing for ${currentStudent?.target_role || 'my role'}?`,
    "Recommend a project based on my current skills.",
    "I have only 5 hours per week. How does my plan adapt?",
    "I completed SQL. What should I do next?",
    "I want to become a Data Scientist instead. What changes?"
  ]);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  useEffect(() => {
    if (currentStudent) {
      setMessages([
        {
          sender: 'assistant',
          text: `👋 Hello ${currentStudent.name}! I am CareerAI's persistent career guidance assistant.\n\nI have loaded your profile for **${currentStudent.target_role}** (${currentStudent.weekly_hours} hrs/week). How can I assist your career progression today?`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          mode: 'rule-based'
        }
      ]);
    }
  }, [currentStudent]);

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || !currentStudent?.id) return;

    const userMsg = {
      sender: 'user',
      text: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const res = await api.sendAssistantChat(currentStudent.id, text.trim());
      const botMsg = {
        sender: 'assistant',
        text: res.reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        mode: res.mode,
        context: res.relevant_context
      };
      setMessages(prev => [...prev, botMsg]);

      if (res.suggested_questions && res.suggested_questions.length > 0) {
        setSuggestedQuestions(res.suggested_questions);
      }
    } catch (err) {
      const errorBotMsg = {
        sender: 'assistant',
        text: `⚠️ I encountered an error communicating with the agent service: ${err.message || 'Server error'}. Please verify that the backend is running.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        mode: 'error'
      };
      setMessages(prev => [...prev, errorBotMsg]);
    } finally {
      setLoading(false);
    }
  };

  if (!currentStudent) {
    return (
      <div className="text-center py-20 space-y-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 flex items-center justify-center mx-auto">
          <Bot className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-white">Student Profile Required</h2>
        <p className="text-xs text-slate-400">Please onboard or select an active student to interact with the assistant.</p>
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
    <div className="max-w-4xl mx-auto py-5 space-y-3.5 flex flex-col h-[calc(100vh-130px)]">
      {/* Active Student Context Banner */}
      <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-4 shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-3 flex-shrink-0 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center font-bold">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xs font-bold text-white uppercase tracking-wider font-mono">AI Career Assistant</h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                Context-Aware
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Observing: <strong className="text-slate-200">{currentStudent.name}</strong> • Target: <strong className="text-emerald-400">{currentStudent.target_role}</strong> ({currentStudent.weekly_hours} hrs/wk)
            </p>
          </div>
        </div>

        <ModeBadge />
      </div>

      {/* Suggested Questions Chips */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 flex-shrink-0">
        <span className="text-[10px] text-slate-500 font-semibold font-mono whitespace-nowrap flex items-center gap-1">
          <Sparkles className="w-3 h-3 text-emerald-400" />
          <span>PROMPTS:</span>
        </span>
        {suggestedQuestions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(q)}
            disabled={loading}
            className="text-[11px] font-medium bg-slate-900/80 hover:bg-slate-850 text-slate-300 hover:text-white border border-slate-800 rounded-full px-3 py-1 whitespace-nowrap transition-colors flex-shrink-0 disabled:opacity-50"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Chat Messages Body */}
      <div className="flex-1 bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 sm:p-5 overflow-y-auto space-y-3.5 backdrop-blur-sm">
        {messages.map((msg, index) => {
          const isUser = msg.sender === 'user';
          return (
            <div
              key={index}
              className={`flex items-start gap-2.5 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
            >
              {/* Avatar */}
              <div
                className={`w-7 h-7 rounded-xl flex items-center justify-center flex-shrink-0 text-xs font-bold ${
                  isUser
                    ? 'bg-emerald-500 text-slate-950 font-black'
                    : 'bg-purple-950/80 border border-purple-500/30 text-purple-300'
                }`}
              >
                {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-3.5 text-xs leading-relaxed ${
                  isUser
                    ? 'bg-emerald-600/90 text-white font-medium rounded-tr-none shadow-sm'
                    : 'bg-slate-950/90 border border-slate-800/90 text-slate-100 rounded-tl-none shadow-md'
                }`}
              >
                <div className="whitespace-pre-line font-sans">
                  {msg.text}
                </div>

                <div
                  className={`mt-2 pt-1 text-[10px] flex items-center justify-between gap-2 border-t ${
                    isUser ? 'border-emerald-700/50 text-emerald-100/70' : 'border-slate-850 text-slate-400'
                  }`}
                >
                  <span className="font-mono">{msg.timestamp}</span>
                  {!isUser && msg.mode && (
                    <span className="font-mono text-[9px] uppercase px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">
                      Engine: {msg.mode}
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-start gap-2.5">
            <div className="w-7 h-7 rounded-xl bg-purple-950/80 border border-purple-500/30 text-purple-300 flex items-center justify-center flex-shrink-0">
              <Bot className="w-3.5 h-3.5 animate-bounce" />
            </div>
            <div className="bg-slate-950/90 border border-slate-800/90 rounded-2xl p-3.5 rounded-tl-none text-xs text-slate-400 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Analyzing student profile & retrieving saved roadmap...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="flex items-center gap-2 flex-shrink-0"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={`Ask anything about your ${currentStudent.target_role} roadmap or next actions...`}
          disabled={loading}
          className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
        />
        <button
          type="submit"
          disabled={loading || !inputMessage.trim()}
          className="px-4 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs flex items-center gap-1.5 transition-all disabled:opacity-50 shadow-sm"
        >
          <span>Send</span>
          <Send className="w-3 h-3" />
        </button>
      </form>
    </div>
  );
}
