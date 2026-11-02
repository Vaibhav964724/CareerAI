import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  GraduationCap,
  Target,
  Clock,
  Sparkles,
  Plus,
  Trash2,
  CheckCircle,
  AlertCircle,
  User,
  Sliders
} from 'lucide-react';

const PROFICIENCY_LABELS = [
  '0 — Not Learned',
  '1 — Beginner',
  '2 — Basic Practical Knowledge',
  '3 — Intermediate',
  '4 — Advanced',
  '5 — Expert'
];

export default function OnboardingPage({ currentStudent, onProfileSaved, setActiveTab }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    degree: 'B.Tech Computer Science',
    branch: 'Computer Science & Engineering',
    year_of_study: 3,
    gpa: '',
    target_role: 'Data Analyst',
    preferred_industry: 'Technology',
    weekly_hours: 10,
    timeline_months: 6,
    interests: 'Data Science, Machine Learning, Automation',
    existing_projects: 'College Database Portal, Weather API Dashboard',
    completed_certifications: 'Python for Beginners'
  });

  const [skills, setSkills] = useState([
    { skill_name: 'Python', proficiency: 2 },
    { skill_name: 'SQL', proficiency: 2 },
    { skill_name: 'Spreadsheets (Excel/Sheets)', proficiency: 3 }
  ]);

  const [availableRoles, setAvailableRoles] = useState([]);
  const [newSkillName, setNewSkillName] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    api.getCareers().then(roles => {
      setAvailableRoles(roles);
    }).catch(err => console.error(err));

    if (currentStudent) {
      setFormData({
        name: currentStudent.name || '',
        email: currentStudent.email || '',
        degree: currentStudent.degree || '',
        branch: currentStudent.branch || '',
        year_of_study: currentStudent.year_of_study || 3,
        gpa: currentStudent.gpa !== null && currentStudent.gpa !== undefined ? currentStudent.gpa : '',
        target_role: currentStudent.target_role || 'Data Analyst',
        preferred_industry: currentStudent.preferred_industry || 'Technology',
        weekly_hours: currentStudent.weekly_hours || 10,
        timeline_months: currentStudent.timeline_months || 6,
        interests: Array.isArray(currentStudent.interests) ? currentStudent.interests.join(', ') : '',
        existing_projects: Array.isArray(currentStudent.existing_projects) ? currentStudent.existing_projects.join(', ') : '',
        completed_certifications: Array.isArray(currentStudent.completed_certifications) ? currentStudent.completed_certifications.join(', ') : ''
      });

      if (currentStudent.skills && currentStudent.skills.length > 0) {
        setSkills(currentStudent.skills);
      }
    }
  }, [currentStudent]);

  const handleSkillChange = (index, value) => {
    const updated = [...skills];
    updated[index].proficiency = parseInt(value, 10);
    setSkills(updated);
  };

  const handleAddSkill = () => {
    if (!newSkillName.trim()) return;
    if (skills.some(s => s.skill_name.toLowerCase() === newSkillName.trim().toLowerCase())) {
      setErrorMsg(`Skill '${newSkillName.trim()}' is already listed.`);
      return;
    }
    setSkills([...skills, { skill_name: newSkillName.trim(), proficiency: 1 }]);
    setNewSkillName('');
    setErrorMsg('');
  };

  const handleRemoveSkill = (index) => {
    setSkills(skills.filter((_, idx) => idx !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');
    setSuccessMsg('');

    if (!formData.name.trim()) {
      setErrorMsg('Student name is required.');
      setLoading(false);
      return;
    }
    if (!formData.degree.trim() || !formData.branch.trim()) {
      setErrorMsg('Degree and branch are required.');
      setLoading(false);
      return;
    }

    const payload = {
      name: formData.name.trim(),
      email: formData.email.trim() || null,
      degree: formData.degree.trim(),
      branch: formData.branch.trim(),
      year_of_study: parseInt(formData.year_of_study, 10),
      gpa: formData.gpa ? parseFloat(formData.gpa) : null,
      target_role: formData.target_role,
      preferred_industry: formData.preferred_industry,
      weekly_hours: parseFloat(formData.weekly_hours),
      timeline_months: parseInt(formData.timeline_months, 10),
      interests: formData.interests.split(',').map(s => s.trim()).filter(Boolean),
      existing_projects: formData.existing_projects.split(',').map(s => s.trim()).filter(Boolean),
      completed_certifications: formData.completed_certifications.split(',').map(s => s.trim()).filter(Boolean),
      skills: skills
    };

    try {
      let savedStudent;
      if (currentStudent && currentStudent.id) {
        savedStudent = await api.updateStudent(currentStudent.id, payload);
      } else {
        savedStudent = await api.createStudent(payload);
      }

      setSuccessMsg('Academic profile saved successfully! Initializing Career Roadmap...');
      onProfileSaved(savedStudent);

      setTimeout(async () => {
        try {
          await api.evaluateAgent(savedStudent.id, 'profile_updated');
        } catch (err) {
          console.warn('Initial evaluation error:', err);
        }
        setActiveTab('dashboard');
      }, 1000);

    } catch (err) {
      setErrorMsg(err.message || 'Failed to save student profile.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-6 space-y-6">
      {/* Title Header */}
      <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-5 sm:p-6 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              {currentStudent ? 'Edit Academic Profile & Preferences' : 'Student Onboarding'}
            </h1>
            <p className="text-xs text-slate-400">
              Provide your academic background, current technical competencies, and goal target role.
            </p>
          </div>
        </div>
      </div>

      {errorMsg && (
        <div className="bg-rose-950/60 border border-rose-500/30 text-rose-300 p-3.5 rounded-xl text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {successMsg && (
        <div className="bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 p-3.5 rounded-xl text-xs flex items-center gap-2">
          <CheckCircle className="w-4 h-4 flex-shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Section 1: Basic Information */}
        <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-4">
          <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
            <User className="w-3.5 h-3.5 text-emerald-400" />
            <span>1. Academic Information</span>
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">Full Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="e.g. Vaibhav Singh"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>

            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">College Email (Optional)</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="e.g. vaibhav@srmist.edu.in"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>

            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">Degree *</label>
              <input
                type="text"
                required
                value={formData.degree}
                onChange={(e) => setFormData({ ...formData, degree: e.target.value })}
                placeholder="e.g. B.Tech Computer Science"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>

            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">Branch / Department *</label>
              <input
                type="text"
                required
                value={formData.branch}
                onChange={(e) => setFormData({ ...formData, branch: e.target.value })}
                placeholder="e.g. Computer Science & Engineering"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>

            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">Current Year of Study</label>
              <select
                value={formData.year_of_study}
                onChange={(e) => setFormData({ ...formData, year_of_study: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500/50 transition-colors cursor-pointer"
              >
                <option value={1}>1st Year (Freshman)</option>
                <option value={2}>2nd Year (Sophomore)</option>
                <option value={3}>3rd Year (Junior)</option>
                <option value={4}>4th Year (Senior)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">GPA / Score (Scale 10.0)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="10"
                value={formData.gpa}
                onChange={(e) => setFormData({ ...formData, gpa: e.target.value })}
                placeholder="e.g. 8.7"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>
          </div>
        </div>

        {/* Section 2: Technical Skills Assessment */}
        <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
                <Target className="w-3.5 h-3.5 text-emerald-400" />
                <span>2. Current Technical Skills (0 to 5 Proficiency Scale)</span>
              </h2>
              <p className="text-[11px] text-slate-400 mt-0.5">
                Rate your practical confidence level from 0 (Not learned) to 5 (Expert).
              </p>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="text"
                value={newSkillName}
                onChange={(e) => setNewSkillName(e.target.value)}
                placeholder="Add custom skill..."
                className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
              <button
                type="button"
                onClick={handleAddSkill}
                className="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl text-xs flex items-center gap-1 transition-colors"
              >
                <Plus className="w-3 h-3" />
                <span>Add</span>
              </button>
            </div>
          </div>

          <div className="space-y-2.5 pt-1">
            {skills.map((skill, index) => (
              <div
                key={index}
                className="bg-slate-950/80 border border-slate-850 rounded-xl p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div className="flex items-center justify-between sm:w-1/3">
                  <span className="text-xs font-semibold text-white">{skill.skill_name}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-emerald-300 font-mono sm:hidden">
                    Level {skill.proficiency}/5
                  </span>
                </div>

                <div className="flex-1 flex items-center gap-3">
                  <input
                    type="range"
                    min="0"
                    max="5"
                    step="1"
                    value={skill.proficiency}
                    onChange={(e) => handleSkillChange(index, e.target.value)}
                    className="w-full accent-emerald-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
                  />
                  <span className="text-xs text-slate-300 font-mono w-44 hidden sm:inline-block">
                    {PROFICIENCY_LABELS[skill.proficiency]}
                  </span>
                </div>

                <button
                  type="button"
                  onClick={() => handleRemoveSkill(index)}
                  className="text-slate-500 hover:text-rose-400 p-1 self-end sm:self-auto transition-colors"
                  title="Remove skill"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Section 3: Career Aspirations & Commitment */}
        <div className="bg-slate-900/70 border border-slate-800/80 rounded-2xl p-5 sm:p-6 space-y-4">
          <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-purple-400" />
            <span>3. Career Goal & Learning Commitment</span>
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">Target Career Role *</label>
              <select
                value={formData.target_role}
                onChange={(e) => setFormData({ ...formData, target_role: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white font-medium focus:outline-none focus:border-emerald-500/50 transition-colors cursor-pointer"
              >
                {availableRoles.length > 0 ? (
                  availableRoles.map(r => (
                    <option key={r.id} value={r.title}>{r.title} ({r.industry})</option>
                  ))
                ) : (
                  <>
                    <option value="Data Analyst">Data Analyst</option>
                    <option value="Data Scientist">Data Scientist</option>
                    <option value="AI/ML Engineer">AI/ML Engineer</option>
                    <option value="Software Developer">Software Developer</option>
                    <option value="Full-Stack Developer">Full-Stack Developer</option>
                    <option value="Data Engineer">Data Engineer</option>
                    <option value="Cybersecurity Analyst">Cybersecurity Analyst</option>
                    <option value="Cloud Engineer">Cloud Engineer</option>
                  </>
                )}
              </select>
            </div>

            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">Preferred Industry</label>
              <input
                type="text"
                value={formData.preferred_industry}
                onChange={(e) => setFormData({ ...formData, preferred_industry: e.target.value })}
                placeholder="e.g. Technology, Finance, Healthcare"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-1.5">
                <label className="text-slate-300 font-medium">Weekly Study Commitment *</label>
                <span className="font-mono text-emerald-400 font-bold">{formData.weekly_hours} hrs/week</span>
              </div>
              <input
                type="range"
                min="2"
                max="40"
                step="1"
                value={formData.weekly_hours}
                onChange={(e) => setFormData({ ...formData, weekly_hours: e.target.value })}
                className="w-full accent-emerald-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
              <p className="text-[11px] text-slate-500 mt-1 font-mono">
                The agent calculates milestone timelines based on this weekly capacity.
              </p>
            </div>

            <div>
              <label className="block text-slate-300 mb-1.5 font-medium">Target Timeline (Months)</label>
              <input
                type="number"
                min="1"
                max="24"
                value={formData.timeline_months}
                onChange={(e) => setFormData({ ...formData, timeline_months: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>

            <div className="sm:col-span-2">
              <label className="block text-slate-300 mb-1.5 font-medium">Technical Interests (Comma-separated)</label>
              <input
                type="text"
                value={formData.interests}
                onChange={(e) => setFormData({ ...formData, interests: e.target.value })}
                placeholder="e.g. Natural Language Processing, Autonomous Agents, Cloud Systems"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>

            <div className="sm:col-span-2">
              <label className="block text-slate-300 mb-1.5 font-medium">Existing Projects & Experience (Comma-separated)</label>
              <input
                type="text"
                value={formData.existing_projects}
                onChange={(e) => setFormData({ ...formData, existing_projects: e.target.value })}
                placeholder="e.g. Database Portal, Portfolio Website"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50 transition-colors"
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end pt-1">
          <button
            type="submit"
            disabled={loading}
            className="px-7 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 text-slate-950 font-bold rounded-xl text-xs shadow-md shadow-emerald-500/20 disabled:opacity-50 flex items-center gap-2 transition-all"
          >
            {loading ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                <span>Processing Profile & Roadmaps...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-3.5 h-3.5" />
                <span>{currentStudent ? 'Save Changes & Update Agent' : 'Save Profile & Generate Roadmap'}</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
