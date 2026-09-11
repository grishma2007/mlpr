/**
 * AI-Powered Student Career & Recruitment Platform
 * Client-Side JavaScript Logic & REST API Integrations
 * Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
 */

const API_BASE = '/api';
let careerChartInstance = null;
let currentStudentsList = [];
let currentJobsList = [];

// ==========================================
// Initialization & Navigation
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  checkHealth();
  loadDashboardData();
  loadStudents();
  loadJobs();
  loadModelMetrics();
  loadAssociationMining();
});

function switchSection(sectionId) {
  // Hide all sections
  document.querySelectorAll('.content-section').forEach(sec => {
    sec.style.display = 'none';
  });

  // Show target section
  const target = document.getElementById(sectionId);
  if (target) {
    target.style.display = 'block';
  }

  // Update active sidebar nav item
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.remove('active');
  });
  const activeNav = Array.from(document.querySelectorAll('.nav-item')).find(item => 
    item.getAttribute('onclick')?.includes(sectionId)
  );
  if (activeNav) activeNav.classList.add('active');

  // Trigger section-specific refresh
  if (sectionId === 'section-profile') loadStudents();
  if (sectionId === 'section-jobs') loadJobs();
  if (sectionId === 'section-recruiter') loadRecruiterApplications();
  if (sectionId === 'section-ranking') loadRankingJobDropdown();
  if (sectionId === 'section-evaluation') loadModelMetrics();
}

function switchTab(tabId, btn) {
  const parent = btn.closest('.card');
  parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  parent.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  
  btn.classList.add('active');
  const content = document.getElementById(tabId);
  if (content) content.classList.add('active');
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const icon = type === 'success' ? 'fa-circle-check' : (type === 'error' ? 'fa-circle-xmark' : 'fa-circle-info');
  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ==========================================
// Health & Overview
// ==========================================

async function checkHealth() {
  const pill = document.getElementById('backend-status-pill');
  const text = document.getElementById('backend-status-text');
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (res.ok) {
      pill.className = 'status-pill';
      text.innerText = 'Flask REST API Connected (Port 5000)';
    } else {
      pill.className = 'status-pill offline';
      text.innerText = 'Flask Status: Error';
    }
  } catch (err) {
    pill.className = 'status-pill offline';
    text.innerText = 'Flask Offline (run python flask_api/app.py)';
  }
}

async function loadDashboardData() {
  try {
    const [stRes, jbRes, apRes] = await Promise.all([
      fetch(`${API_BASE}/students`).then(r => r.json()),
      fetch(`${API_BASE}/jobs`).then(r => r.json()),
      fetch(`${API_BASE}/applications`).then(r => r.json())
    ]);

    document.getElementById('kpi-students').innerText = stRes.count ?? 0;
    document.getElementById('kpi-jobs').innerText = jbRes.count ?? 0;
    document.getElementById('kpi-apps').innerText = apRes.count ?? 0;
  } catch (err) {
    console.error('Error loading dashboard counts:', err);
  }
}

// ==========================================
// Student Profile CRUD
// ==========================================

async function loadStudents() {
  try {
    const res = await fetch(`${API_BASE}/students`);
    const data = await res.json();
    currentStudentsList = data.students || [];

    const tbody = document.getElementById('students-table-body');
    const select = document.getElementById('skill-student-select');
    
    if (currentStudentsList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No student profiles found. Create one above!</td></tr>';
      select.innerHTML = '<option value="">No students available</option>';
      return;
    }

    tbody.innerHTML = currentStudentsList.map(st => `
      <tr>
        <td><b>#${st.id}</b></td>
        <td>${st.name}</td>
        <td>${st.email}</td>
        <td>${st.degree} (${st.branch})</td>
        <td>Sem ${st.semester}</td>
        <td><span class="badge badge-green">${st.cgpa} / 10</span></td>
        <td>${st.skills ? st.skills.length : 0} skills</td>
        <td>
          <button class="btn btn-danger" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;" onclick="handleDeleteStudent(${st.id})"><i class="fa-solid fa-trash"></i></button>
        </td>
      </tr>
    `).join('');

    select.innerHTML = currentStudentsList.map(st => `
      <option value="${st.id}">${st.name} (${st.email})</option>
    `).join('');

  } catch (err) {
    showToast('Failed to load students list from Flask API', 'error');
  }
}

async function handleCreateStudent(e) {
  e.preventDefault();
  const payload = {
    name: document.getElementById('st-name').value.trim(),
    email: document.getElementById('st-email').value.trim(),
    college: document.getElementById('st-college').value.trim(),
    degree: document.getElementById('st-degree').value,
    branch: document.getElementById('st-branch').value,
    semester: parseInt(document.getElementById('st-semester').value),
    cgpa: parseFloat(document.getElementById('st-cgpa').value)
  };

  try {
    const res = await fetch(`${API_BASE}/students`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast(`Student profile for '${payload.name}' created!`, 'success');
      document.getElementById('create-student-form').reset();
      loadStudents();
      loadDashboardData();
    } else {
      showToast(data.error || 'Failed to create student', 'error');
    }
  } catch (err) {
    showToast('Network error communicating with Flask backend', 'error');
  }
}

async function handleDeleteStudent(id) {
  if (!confirm('Are you sure you want to delete this student profile?')) return;
  try {
    const res = await fetch(`${API_BASE}/students/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast('Student deleted successfully', 'success');
      loadStudents();
      loadDashboardData();
    } else {
      showToast(data.error || 'Delete failed', 'error');
    }
  } catch (err) {
    showToast('Network error', 'error');
  }
}

async function handleAddSkill() {
  const studentId = document.getElementById('skill-student-select').value;
  const skillName = document.getElementById('new-skill-name').value.trim();
  const prof = document.getElementById('new-skill-prof').value;

  if (!studentId || !skillName) {
    showToast('Please select a student and enter a skill name.', 'error');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/students/${studentId}/skills`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skill_name: skillName, proficiency: prof })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast(`Skill '${skillName}' attached to student!`, 'success');
      document.getElementById('new-skill-name').value = '';
      loadStudents();
    } else {
      showToast(data.error || 'Failed to attach skill', 'error');
    }
  } catch (err) {
    showToast('Error communicating with API', 'error');
  }
}

async function handleAddProject() {
  const studentId = document.getElementById('skill-student-select').value;
  const title = document.getElementById('new-proj-title').value.trim();
  const desc = document.getElementById('new-proj-desc').value.trim();
  const tech = document.getElementById('new-proj-tech').value.trim();

  if (!studentId || !title) {
    showToast('Please select a student and enter project title.', 'error');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/students/${studentId}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description: desc, technologies: tech })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast(`Project '${title}' added!`, 'success');
      document.getElementById('new-proj-title').value = '';
      document.getElementById('new-proj-desc').value = '';
      document.getElementById('new-proj-tech').value = '';
      loadStudents();
    } else {
      showToast(data.error || 'Failed to add project', 'error');
    }
  } catch (err) {
    showToast('Error communicating with API', 'error');
  }
}

// ==========================================
// Career Prediction
// ==========================================

async function handleCareerPredict(e) {
  e.preventDefault();
  const payload = {
    cgpa: parseFloat(document.getElementById('c-cgpa').value),
    python: document.getElementById('c-python').checked ? 1 : 0,
    java: document.getElementById('c-java').checked ? 1 : 0,
    cpp: document.getElementById('c-cpp').checked ? 1 : 0,
    sql: document.getElementById('c-sql').checked ? 1 : 0,
    machine_learning: document.getElementById('c-ml').checked ? 1 : 0,
    deep_learning: document.getElementById('c-dl').checked ? 1 : 0,
    data_visualization: document.getElementById('c-dataviz').checked ? 1 : 0,
    web_development: document.getElementById('c-webdev').checked ? 1 : 0,
    cloud: document.getElementById('c-cloud').checked ? 1 : 0,
    projects_count: parseInt(document.getElementById('c-projects').value),
    internship: parseInt(document.getElementById('c-internship').value),
    certifications_count: parseInt(document.getElementById('c-certs').value)
  };

  try {
    const res = await fetch(`${API_BASE}/predict/career`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok && data.success) {
      document.getElementById('career-result-placeholder').style.display = 'none';
      document.getElementById('career-result-content').style.display = 'block';

      document.getElementById('pred-role-title').innerText = data.predicted_career;
      document.getElementById('pred-conf-disp').innerText = `${Math.round(data.confidence * 100)}%`;

      // Render Chart.js Donut
      const topRoles = data.top_career_roles || [];
      const labels = topRoles.map(r => r.role);
      const values = topRoles.map(r => Math.round(r.probability * 100));

      const ctx = document.getElementById('careerChart').getContext('2d');
      if (careerChartInstance) careerChartInstance.destroy();

      careerChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: ['#3b82f6', '#06b6d4', '#8b5cf6', '#10b981', '#f59e0b'],
            borderWidth: 1,
            borderColor: '#1e293b'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { color: '#94a3b8' } }
          }
        }
      });
      showToast('Career role prediction completed!', 'success');
    } else {
      showToast(data.error || 'Prediction failed', 'error');
    }
  } catch (err) {
    showToast('Network error on career prediction', 'error');
  }
}

// ==========================================
// Academic Risk Prediction
// ==========================================

async function handleAcademicPredict(e) {
  e.preventDefault();
  const payload = {
    attendance: parseFloat(document.getElementById('a-attendance').value),
    previous_marks: parseFloat(document.getElementById('a-prevmarks').value),
    study_hours: parseFloat(document.getElementById('a-hours').value),
    assignment_completion: parseFloat(document.getElementById('a-assign').value),
    internal_marks: parseFloat(document.getElementById('a-internal').value),
    failed_subjects: parseInt(document.getElementById('a-failed').value),
    cgpa: parseFloat(document.getElementById('a-cgpa').value)
  };

  try {
    const res = await fetch(`${API_BASE}/predict/academic-risk`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok && data.success) {
      document.getElementById('academic-result-placeholder').style.display = 'none';
      document.getElementById('academic-result-content').style.display = 'block';

      const banner = document.getElementById('risk-banner');
      const title = document.getElementById('risk-level-title');
      const desc = document.getElementById('risk-desc-text');

      if (data.academic_risk === 'Low Risk') {
        banner.style.background = 'linear-gradient(135deg, #065f46, #10b981)';
        title.innerText = '🟢 LOW ACADEMIC RISK';
      } else if (data.academic_risk === 'Medium Risk') {
        banner.style.background = 'linear-gradient(135deg, #92400e, #f59e0b)';
        title.innerText = '🟡 MEDIUM ACADEMIC RISK';
      } else {
        banner.style.background = 'linear-gradient(135deg, #991b1b, #ef4444)';
        title.innerText = '🔴 HIGH ACADEMIC RISK';
      }
      desc.innerText = `Classification Confidence: ${Math.round(data.confidence * 100)}% | Random Forest Classifier`;

      const ul = document.getElementById('risk-recommendations');
      ul.innerHTML = (data.recommendations || []).map(r => `<li>${r}</li>`).join('');
      showToast('Academic risk classified!', 'success');
    } else {
      showToast(data.error || 'Risk evaluation failed', 'error');
    }
  } catch (err) {
    showToast('Network error on academic risk prediction', 'error');
  }
}

// ==========================================
// Resume NLP Parser
// ==========================================

async function handleAnalyzeResume() {
  const fileInput = document.getElementById('resume-file');
  const textInput = document.getElementById('resume-text');
  const outputBox = document.getElementById('resume-output-box');

  let body;
  let headers = {};

  if (fileInput.files.length > 0) {
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    body = formData;
  } else if (textInput.value.trim().length > 0) {
    body = JSON.stringify({ text: textInput.value.trim() });
    headers = { 'Content-Type': 'application/json' };
  } else {
    showToast('Please upload a PDF / DOCX file or paste resume text.', 'error');
    return;
  }

  outputBox.innerHTML = '<p style="color: var(--text-muted); text-align: center;">Running NLP extraction engine...</p>';

  try {
    const res = await fetch(`${API_BASE}/resume/analyze`, { method: 'POST', headers, body });
    const data = await res.json();
    if (res.ok && data.success) {
      const p = data.parsed_resume || {};
      const catSkills = p.categorized_skills || {};
      const skillsHtml = Object.keys(catSkills).map(cat => `
        <div style="margin-bottom: 0.4rem;">
          <span style="font-size: 0.78rem; color: #94a3b8; font-weight: 600;">${cat}:</span><br>
          ${catSkills[cat].map(s => `<span class="badge badge-blue" style="margin: 2px;">${s}</span>`).join('')}
        </div>
      `).join('') || '<span style="color: var(--text-muted);">No skills detected</span>';

      outputBox.innerHTML = `
        <div style="margin-bottom: 0.85rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.6rem;">
          <h3 style="color: #60a5fa; margin: 0;">${p.name || 'Candidate'}</h3>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem;">
            📧 <b>Email:</b> ${p.email || 'N/A'} &nbsp;|&nbsp; 
            📞 <b>Phone:</b> ${p.phone || 'N/A'} &nbsp;|&nbsp; 
            📊 <b>CGPA:</b> <span style="color: #34d399; font-weight: 700;">${p.cgpa || 8.0} / 10</span>
          </p>
        </div>
        <div style="margin-bottom: 0.65rem;">
          <b style="color: var(--accent); font-size: 0.88rem;">🎓 Education & Degrees:</b>
          <div style="color: var(--text-main); font-size: 0.85rem; margin-top: 0.2rem;">${(p.education || []).join(' • ') || 'N/A'}</div>
        </div>
        <div style="margin-bottom: 0.65rem;">
          <b style="color: #38bdf8; font-size: 0.88rem;">🛠️ Extracted Skills (${p.skills?.length || 0}):</b>
          <div style="margin-top: 0.35rem;">${skillsHtml}</div>
        </div>
        <div style="margin-bottom: 0.65rem;">
          <b style="color: #fbbf24; font-size: 0.88rem;">💼 Experience & Internships:</b>
          <ul style="padding-left: 1.25rem; font-size: 0.82rem; color: var(--text-muted); margin-top: 0.2rem;">
            ${(p.experience || ['No explicit experience section.']).map(e => `<li>${e}</li>`).join('')}
          </ul>
        </div>
        <div>
          <b style="color: #c084fc; font-size: 0.88rem;">🚀 Projects & Highlights:</b>
          <ul style="padding-left: 1.25rem; font-size: 0.82rem; color: var(--text-muted); margin-top: 0.2rem;">
            ${(p.projects || ['AI Academic Capstone Project']).map(pr => `<li>${pr}</li>`).join('')}
          </ul>
        </div>
      `;
      showToast('Resume parsed successfully!', 'success');
    } else {
      showToast(data.error || 'Failed to parse resume', 'error');
    }
  } catch (err) {
    showToast('Network error analyzing resume', 'error');
  }
}

// ==========================================
// Skill Gap & Learning Recommendations
// ==========================================

async function handleSkillGapAnalysis() {
  const skillsText = document.getElementById('gap-current-skills').value;
  const targetRole = document.getElementById('gap-target-role').value;
  const skills = skillsText.split(',').map(s => s.trim()).filter(s => s);

  try {
    const res = await fetch(`${API_BASE}/skills/gap`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skills, target_role: targetRole })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      const gap = data.gap_analysis || {};
      document.getElementById('gap-results-container').style.display = 'block';

      document.getElementById('gap-matching-pills').innerHTML = (gap.matching_skills || []).map(s => `
        <span class="badge badge-green">✓ ${s}</span>
      `).join('') || '<span style="color: var(--text-muted);">No direct matches</span>';

      document.getElementById('gap-missing-pills').innerHTML = (gap.missing_skills || []).map(s => `
        <span class="badge badge-red">✗ ${s}</span>
      `).join('') || '<span style="color: #34d399;">Possesses all key skills!</span>';

      // Fetch Learning Courses for Missing Skills
      const recRes = await fetch(`${API_BASE}/recommendations/learning`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ missing_skills: gap.missing_skills })
      });
      const recData = await recRes.json();
      const catalog = recData.recommended_courses || [];

      document.getElementById('learning-catalog-grid').innerHTML = catalog.map(c => `
        <div style="background: #0f172a; border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
            <h5 style="color: #60a5fa; font-size: 0.95rem; margin: 0;">${c.course_name}</h5>
            <span class="badge badge-blue">${c.level}</span>
          </div>
          <p style="font-size: 0.8rem; color: var(--accent); margin-bottom: 0.35rem;"><b>Skill:</b> ${c.skill} | ${c.platform}</p>
          <p style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 0.75rem;">${c.description}</p>
          <a href="${c.url}" target="_blank" class="btn btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.78rem;"><i class="fa-solid fa-arrow-up-right-from-square"></i> Open Course</a>
        </div>
      `).join('');

      showToast(`Skill gap analyzed: ${gap.match_percentage}% readiness`, 'success');
    }
  } catch (err) {
    showToast('Error analyzing skill gap', 'error');
  }
}

// ==========================================
// Job Matching & Apply
// ==========================================

async function loadJobs() {
  try {
    const res = await fetch(`${API_BASE}/jobs`);
    const data = await res.json();
    currentJobsList = data.jobs || [];
    const container = document.getElementById('jobs-container');

    if (currentJobsList.length === 0) {
      container.innerHTML = '<p style="color: var(--text-muted);">No job listings posted yet.</p>';
      return;
    }

    container.innerHTML = currentJobsList.map(j => `
      <div class="card" style="margin-bottom: 0;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
          <div>
            <h3 style="color: #60a5fa; margin: 0; font-size: 1.15rem;">${j.title}</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem;">🏢 ${j.company || 'Tech Corp'} | 📍 ${j.location || 'Remote'} | 💼 ${j.job_type || 'Full-time'}</p>
          </div>
          <span class="badge badge-purple">Min CGPA: ${j.minimum_cgpa}</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 0.75rem; line-height: 1.5;">${j.description}</p>
        <p style="font-size: 0.82rem; color: var(--text-dim); margin-bottom: 1rem;"><b>Required Skills:</b> <code style="color: #38bdf8;">${j.required_skills}</code></p>
        <button class="btn btn-primary" onclick="handleApplyJob(${j.id}, '${j.title}')"><i class="fa-solid fa-paper-plane"></i> Quick Apply (Demo Student)</button>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load jobs', err);
  }
}

async function handleApplyJob(jobId, jobTitle) {
  try {
    const res = await fetch(`${API_BASE}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: 1, job_id: jobId, match_score: 88.5 })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast(`Application submitted for '${jobTitle}'!`, 'success');
      loadDashboardData();
    } else {
      showToast(data.error || 'Application failed', 'error');
    }
  } catch (err) {
    showToast('Network error submitting application', 'error');
  }
}

// ==========================================
// Recruiter Operations
// ==========================================

async function loadRecruiterApplications() {
  try {
    const res = await fetch(`${API_BASE}/applications`);
    const data = await res.json();
    const tbody = document.getElementById('recruiter-apps-table-body');
    const apps = data.applications || [];

    if (apps.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No candidate applications received yet.</td></tr>';
      return;
    }

    tbody.innerHTML = apps.map(a => `
      <tr>
        <td><b>#${a.id}</b></td>
        <td>${a.student_name}</td>
        <td>${a.student_email}</td>
        <td>${a.job_title}</td>
        <td>${a.company}</td>
        <td><span class="badge badge-green">${a.match_score}%</span></td>
        <td><span class="badge badge-blue">${a.status}</span></td>
        <td>
          <select class="form-control" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; width: auto;" onchange="handleUpdateStatus(${a.id}, this.value)">
            <option value="Applied" ${a.status==='Applied'?'selected':''}>Applied</option>
            <option value="Shortlisted" ${a.status==='Shortlisted'?'selected':''}>Shortlisted</option>
            <option value="Interview" ${a.status==='Interview'?'selected':''}>Interview</option>
            <option value="Accepted" ${a.status==='Accepted'?'selected':''}>Accepted</option>
            <option value="Rejected" ${a.status==='Rejected'?'selected':''}>Rejected</option>
          </select>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Error loading recruiter applications', err);
  }
}

async function handleUpdateStatus(appId, newStatus) {
  try {
    const res = await fetch(`${API_BASE}/applications/${appId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast(`Status updated to '${newStatus}'!`, 'success');
    }
  } catch (err) {
    showToast('Failed to update status', 'error');
  }
}

async function handlePostJob(e) {
  e.preventDefault();
  const payload = {
    recruiter_id: 1,
    title: document.getElementById('job-title').value.trim(),
    required_skills: document.getElementById('job-skills').value.trim(),
    location: document.getElementById('job-location').value.trim(),
    minimum_cgpa: parseFloat(document.getElementById('job-cgpa').value),
    job_type: document.getElementById('job-type').value,
    description: document.getElementById('job-desc').value.trim()
  };

  try {
    const res = await fetch(`${API_BASE}/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast('Job listing posted successfully!', 'success');
      document.getElementById('post-job-form').reset();
      loadJobs();
      loadDashboardData();
    } else {
      showToast(data.error || 'Failed to post job', 'error');
    }
  } catch (err) {
    showToast('Network error posting job', 'error');
  }
}

// ==========================================
// Candidate AI Ranking
// ==========================================

async function loadRankingJobDropdown() {
  const select = document.getElementById('rank-job-select');
  if (currentJobsList.length === 0) await loadJobs();
  select.innerHTML = currentJobsList.map(j => `
    <option value="${j.id}">${j.title} @ ${j.company || 'Company'}</option>
  `).join('');
  if (currentJobsList.length > 0) handleRankCandidates();
}

async function handleRankCandidates() {
  const jobId = document.getElementById('rank-job-select').value;
  if (!jobId) return;

  const tbody = document.getElementById('rankings-tbody');
  tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Running AI ranking algorithm...</td></tr>';

  try {
    const res = await fetch(`${API_BASE}/jobs/${jobId}/rank-candidates`);
    const data = await res.json();
    if (res.ok && data.success) {
      const rankings = data.rankings || [];
      tbody.innerHTML = rankings.map(c => `
        <tr>
          <td><span class="badge badge-purple">#${c.rank}</span></td>
          <td><b>${c.name}</b></td>
          <td>${c.cgpa}/10</td>
          <td><span class="badge badge-green">${c.match_score}%</span></td>
          <td>${c.status_badge}</td>
          <td style="font-size: 0.82rem; color: var(--text-muted);">${c.explanation}</td>
        </tr>
      `).join('');
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="6" style="color: var(--danger); text-align: center;">Failed to rank candidates.</td></tr>';
  }
}

// ==========================================
// ML Evaluation & Association Mining
// ==========================================

async function loadModelMetrics() {
  try {
    const res = await fetch(`${API_BASE}/metrics`);
    const data = await res.json();
    if (res.ok && data.success) {
      const m = data.metrics || {};
      const cComp = m.career_prediction?.comparison || {};
      const aComp = m.academic_risk?.comparison || {};

      document.getElementById('eval-career-tbody').innerHTML = Object.keys(cComp).map(name => `
        <tr>
          <td><b>${name}</b></td>
          <td>${(cComp[name].accuracy * 100).toFixed(2)}%</td>
          <td>${(cComp[name].f1_score * 100).toFixed(2)}%</td>
        </tr>
      `).join('');

      document.getElementById('eval-academic-tbody').innerHTML = Object.keys(aComp).map(name => `
        <tr>
          <td><b>${name}</b></td>
          <td>${(aComp[name].accuracy * 100).toFixed(2)}%</td>
          <td>${(aComp[name].f1_score * 100).toFixed(2)}%</td>
        </tr>
      `).join('');

      const cTune = m.career_prediction?.tuning || {};
      const aTune = m.academic_risk?.tuning || {};
      document.getElementById('eval-tuning-summary').innerHTML = `
        • <b>Career Prediction (Random Forest):</b> Before Tuning: <code>${(cTune.accuracy_before*100).toFixed(2)}%</code> | After GridSearchCV: <code>${(cTune.accuracy_after*100).toFixed(2)}%</code><br>
        • <b>Academic Risk (Random Forest):</b> Before Tuning: <code>${(aTune.accuracy_before*100).toFixed(2)}%</code> | After GridSearchCV: <code>${(aTune.accuracy_after*100).toFixed(2)}%</code><br>
        • <b>Optimal Parameters:</b> <code>${JSON.stringify(cTune.best_parameters || {})}</code>
      `;
    }
  } catch (err) {
    console.error('Metrics loading error', err);
  }
}

async function loadAssociationMining() {
  try {
    const res = await fetch(`${API_BASE}/association/benchmark?min_support=0.06&min_confidence=0.3`);
    const data = await res.json();
    if (res.ok && data.success) {
      const b = data.benchmark || {};
      document.getElementById('assoc-apriori-time').innerText = `${b.apriori?.execution_time} s`;
      document.getElementById('assoc-fpgrowth-time').innerText = `${b.fpgrowth?.execution_time} s`;
      document.getElementById('assoc-speedup').innerText = b.speedup_ratio || '--';

      const rules = b.sample_top_rules || [];
      document.getElementById('assoc-rules-tbody').innerHTML = rules.map(r => `
        <tr>
          <td><span class="badge badge-blue">${r.antecedents}</span></td>
          <td><span class="badge badge-green">${r.consequents}</span></td>
          <td>${r.support}</td>
          <td>${r.confidence}</td>
          <td><span class="badge badge-purple">${r.lift}</span></td>
        </tr>
      `).join('');
    }
  } catch (err) {
    console.error('Association mining error', err);
  }
}

// ==========================================
// Q-Learning RL Demo
// ==========================================

async function handleRunRL() {
  try {
    const res = await fetch(`${API_BASE}/rl/optimize-path`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ episodes: 300 })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      const steps = data.simulation?.optimal_path || [];
      document.getElementById('rl-results').style.display = 'block';
      document.getElementById('rl-steps-container').innerHTML = steps.map(s => `
        <div style="background: #0f172a; border-left: 4px solid #8b5cf6; padding: 0.85rem 1rem; border-radius: 0 var(--radius-md) var(--radius-md) 0; margin-bottom: 0.5rem;">
          <b>Step ${s.step}:</b> At <span style="color: #c4b5fd;">[${s.current_state}]</span>
          ➔ Take Action: <span class="badge badge-purple">${s.recommended_action}</span> (Q-Value: <b>${s.q_value}</b>)
          ➔ Next State: <span style="color: #34d399;">[${s.next_state}]</span>
        </div>
      `).join('');
      showToast('Q-Learning agent converged on optimal path!', 'success');
    }
  } catch (err) {
    showToast('Failed to run RL simulation', 'error');
  }
}
