const API_BASE = '/api/v1';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const res = await fetch(url, config);
    if (!res.ok) {
      let errorMsg = `HTTP Error ${res.status}`;
      try {
        const errJson = await res.json();
        errorMsg = errJson.detail || errJson.message || errorMsg;
      } catch (e) {
        // Fallback to status text
        errorMsg = res.statusText || errorMsg;
      }
      throw new Error(errorMsg);
    }
    return await res.json();
  } catch (error) {
    console.error(`API Call failed [${options.method || 'GET'} ${endpoint}]:`, error);
    throw error;
  }
}

export const api = {
  // Health
  getHealth: () => request('/health'),

  // Students
  getStudents: () => request('/students'),
  getStudent: (id) => request(`/students/${id}`),
  createStudent: (data) => request('/students', { method: 'POST', body: JSON.stringify(data) }),
  updateStudent: (id, data) => request(`/students/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Careers
  getCareers: () => request('/careers'),
  getCareer: (id) => request(`/careers/${id}`),
  analyzeSkillGaps: (studentId, targetRole) =>
    request('/careers/skill-gaps', {
      method: 'POST',
      body: JSON.stringify({ student_id: studentId, target_role: targetRole }),
    }),
  compareCareers: (currentRole, newRole, studentSkills = {}) =>
    request('/careers/compare', {
      method: 'POST',
      body: JSON.stringify({ current_role: currentRole, new_role: newRole, student_skills: studentSkills }),
    }),

  // Roadmaps
  generateRoadmap: (studentId, targetRole, weeklyHours) =>
    request('/roadmaps/generate', {
      method: 'POST',
      body: JSON.stringify({ student_id: studentId, target_role: targetRole, weekly_hours: weeklyHours }),
    }),
  getActiveRoadmap: (studentId) => request(`/roadmaps/student/${studentId}`),
  updateMilestoneStatus: (milestoneId, newStatus, notes = '') =>
    request(`/roadmaps/milestones/${milestoneId}`, {
      method: 'PATCH',
      body: JSON.stringify({ new_status: newStatus, notes }),
    }),
  getRoadmapRevisions: (studentId) => request(`/roadmaps/revisions/${studentId}`),

  // Agent
  evaluateAgent: (studentId, trigger = 'manual_dashboard_evaluation') =>
    request(`/agent/evaluate/${studentId}`, {
      method: 'POST',
      body: JSON.stringify({ trigger }),
    }),
  getAgentObservations: (studentId) => request(`/agent/observations/${studentId}`),
  getAgentActions: (studentId) => request(`/agent/actions/${studentId}`),
  getNextBestAction: (studentId) => request(`/agent/next-action/${studentId}`),
  getAgentMode: () => request('/agent/mode'),

  // Assistant
  sendAssistantChat: (studentId, message) =>
    request('/assistant/chat', {
      method: 'POST',
      body: JSON.stringify({ student_id: studentId, message }),
    }),

  // Agent Technology Course Assignments
  getSampleTelemetry: () => request('/assignments/1-2/sample-telemetry'),
  processReflexStream: (packetCount = 5, customPackets = null) =>
    request('/assignments/1-2/reflex-stream', {
      method: 'POST',
      body: JSON.stringify({ packet_count: packetCount, custom_packets: customPackets }),
    }),
  getDaemonMetrics: () => request('/assignments/2-1/daemon-status'),
  toggleDaemon: (action, intervalSeconds = 2.0) =>
    request('/assignments/2-1/daemon-toggle', {
      method: 'POST',
      body: JSON.stringify({ action, interval_seconds: intervalSeconds }),
    }),
  executeSocketTransfer: (payload = {}) =>
    request('/assignments/2-2/socket-transfer', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  executeNegotiation: (params = {}) =>
    request('/assignments/3-1/negotiate', {
      method: 'POST',
      body: JSON.stringify(params),
    }),
  executeUtilityOptimization: (params = {}) =>
    request('/assignments/3-2/optimize', {
      method: 'POST',
      body: JSON.stringify(params),
    }),
  getCandidateBundles: () => request('/assignments/3-2/bundles'),

  // Assignment 4.1: BDI Cognitive Engine
  getBdiState: () => request('/assignments/4-1/bdi-state'),
  executeBdiStep: () => request('/assignments/4-1/bdi-step', { method: 'POST' }),
  triggerBdiReconsider: (params = {}) =>
    request('/assignments/4-1/bdi-reconsider', {
      method: 'POST',
      body: JSON.stringify(params),
    }),
  resetBdiAgent: () => request('/assignments/4-1/bdi-reset', { method: 'POST' }),

  // Assignment 4.2: Knowledge Ontology & Live API
  getCareerOntology: () => request('/assignments/4-2/ontology'),
  getRolePrerequisites: (roleName) =>
    request(`/assignments/4-2/prerequisites/${encodeURIComponent(roleName)}`),
  fetchLiveSkillResources: (skill = 'FastAPI', maxResults = 3) =>
    request('/assignments/4-2/live-resources', {
      method: 'POST',
      body: JSON.stringify({ skill, max_results: maxResults }),
    }),
  adaptLearningPlanWithApi: (params = {}) =>
    request('/assignments/4-2/adapt-plan', {
      method: 'POST',
      body: JSON.stringify(params),
    }),

  // Assignment 5.1: Cryptographic Security & Host Authentication
  getTrustedHostsRegistry: () => request('/assignments/5-1/trusted-hosts'),
  createSignedEnvelope: (params = {}) =>
    request('/assignments/5-1/create-envelope', {
      method: 'POST',
      body: JSON.stringify(params),
    }),
  verifySecureCommand: (envelope) =>
    request('/assignments/5-1/verify-command', {
      method: 'POST',
      body: JSON.stringify({ envelope }),
    }),
  simulateSecurityAttack: (attackType = 'TAMPER_PAYLOAD') =>
    request('/assignments/5-1/simulate-attack', {
      method: 'POST',
      body: JSON.stringify({ attack_type: attackType }),
    }),
  getSecurityAuditLogs: () => request('/assignments/5-1/audit-logs'),

  // Assignment 5.2: Capstone Master Orchestration
  getCapstoneSystemState: () => request('/assignments/5-2/system-state'),
  runCapstoneConsolidatedCycle: (params = {}) =>
    request('/assignments/5-2/capstone-cycle', {
      method: 'POST',
      body: JSON.stringify(params),
    }),
};
