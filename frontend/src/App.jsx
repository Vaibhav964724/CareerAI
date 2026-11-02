import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import LandingPage from './pages/LandingPage';
import OnboardingPage from './pages/OnboardingPage';
import DashboardPage from './pages/DashboardPage';
import SkillGapPage from './pages/SkillGapPage';
import RoadmapPage from './pages/RoadmapPage';
import AssistantPage from './pages/AssistantPage';
import ProgressPage from './pages/ProgressPage';
import AgentLabPage from './pages/AgentLabPage';

export default function App() {
  const [activeTab, setActiveTab] = useState('landing');
  const [currentStudent, setCurrentStudent] = useState(null);
  const [allStudents, setAllStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadStudents = async () => {
    try {
      const students = await api.getStudents();
      setAllStudents(students);
      if (students.length > 0 && !currentStudent) {
        // Set first student as active
        setCurrentStudent(students[0]);
      }
    } catch (err) {
      console.warn("Could not load initial students:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStudents();
  }, []);

  const handleSelectStudent = async (studentId) => {
    try {
      const student = await api.getStudent(studentId);
      setCurrentStudent(student);
    } catch (err) {
      console.error("Failed to select student:", err);
    }
  };

  const handleProfileSaved = (savedStudent) => {
    setCurrentStudent(savedStudent);
    loadStudents();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-brand-500 selection:text-slate-950">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentStudent={currentStudent}
        allStudents={allStudents}
        onSelectStudent={handleSelectStudent}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
        {activeTab === 'landing' && (
          <LandingPage setActiveTab={setActiveTab} currentStudent={currentStudent} />
        )}

        {activeTab === 'onboarding' && (
          <OnboardingPage
            currentStudent={currentStudent}
            onProfileSaved={handleProfileSaved}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'dashboard' && (
          <DashboardPage currentStudent={currentStudent} setActiveTab={setActiveTab} />
        )}

        {activeTab === 'skill-gaps' && (
          <SkillGapPage currentStudent={currentStudent} setActiveTab={setActiveTab} />
        )}

        {activeTab === 'roadmap' && (
          <RoadmapPage currentStudent={currentStudent} setActiveTab={setActiveTab} />
        )}

        {activeTab === 'lab' && (
          <AgentLabPage currentStudent={currentStudent} setActiveTab={setActiveTab} />
        )}

        {activeTab === 'assistant' && (
          <AssistantPage currentStudent={currentStudent} setActiveTab={setActiveTab} />
        )}

        {activeTab === 'progress' && (
          <ProgressPage currentStudent={currentStudent} setActiveTab={setActiveTab} />
        )}
      </main>

      <Footer />
    </div>
  );
}
