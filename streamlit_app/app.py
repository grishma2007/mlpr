"""
AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
Main Entry Point
"""

import streamlit as st
from api_client import check_backend_health, get_all_students_api, get_all_jobs_api, get_all_applications_api

st.set_page_config(
    page_title="AI Career & Recruitment Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Dark & Light Mode Universal High-Contrast Support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 2.2rem 2rem;
        border-radius: 16px;
        color: #ffffff !important;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
    }
    
    .main-header h1 {
        color: #ffffff !important;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #e0f2fe !important;
        font-size: 1.05rem;
        max-width: 800px;
    }
    
    .badge-status {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .badge-online {
        background-color: #064e3b;
        color: #6ee7b7 !important;
        border: 1px solid #10b981;
    }
    
    .badge-offline {
        background-color: #7f1d1d;
        color: #fca5a5 !important;
        border: 1px solid #ef4444;
    }
    
    .feature-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 1.4rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
        color: #f1f5f9 !important;
        margin-bottom: 1rem;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -3px rgba(59, 130, 246, 0.25);
        border-color: #60a5fa;
    }
    
    .feature-card h3 {
        color: #60a5fa !important;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.15rem;
        font-weight: 700;
    }
    
    .feature-card p {
        color: #cbd5e1 !important;
        font-size: 0.92rem;
        line-height: 1.45;
    }
    
    .feature-card i, .feature-card b {
        color: #38bdf8 !important;
    }
    
    .portal-banner {
        background: #0f172a;
        color: #f1f5f9 !important;
        border-left: 4px solid #3b82f6;
        border-top: 1px solid #334155;
        border-right: 1px solid #334155;
        border-bottom: 1px solid #334155;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    
    .guide-box {
        background: #1e1e38;
        border: 1px solid #6366f1;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        color: #e0e7ff !important;
    }
    .guide-box h4 {
        color: #a5b4fc !important;
        margin-top: 0;
    }
    .guide-box ol {
        margin-bottom: 0;
        padding-left: 1.25rem;
    }
    .guide-box li {
        margin-bottom: 0.4rem;
        color: #e0e7ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Check Flask REST API connection
is_healthy, health_data = check_backend_health()

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>🎓 AI-Powered Student Career & Recruitment Platform</h1>
    <p>503 – Applied Artificial Intelligence: Model Development and Deployment | End-to-End Machine Learning Architecture</p>
</div>
""", unsafe_allow_html=True)

# System Health & Connectivity Banner
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    if is_healthy:
        st.markdown(f"""
        <div class="badge-status badge-online">
            🟢 Flask REST API Connected (http://127.0.0.1:5000) | Models: Career ({health_data['models_status']['career_prediction_model']}), Academic ({health_data['models_status']['academic_risk_model']})
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="badge-status badge-offline">
            🔴 Flask REST API Offline (In terminal, run: <code>python flask_api/app.py</code>)
        </div>
        """, unsafe_allow_html=True)

with col_h2:
    st.caption("AI Subsystem: Active & Synced")

st.markdown("<br>", unsafe_allow_html=True)

# Quick Step-by-Step Guide for Adding Student Data
st.markdown("""
<div class="guide-box">
    <h4>💡 Quick Guide: How Students Enter Data</h4>
    <ol>
        <li><b>Create / Edit Profile:</b> Go to sidebar 👉 <b>2_student_profile</b>. Use <b>➕ Create New Student</b> tab to enter your Name, Email, CGPA, Branch, Semester.</li>
        <li><b>Add Skills & Projects:</b> In <b>2_student_profile</b> under <b>🛠️ Manage Skills & Projects</b>, add your skills (Python, ML, SQL, Web) and project details.</li>
        <li><b>Auto-extract from Resume:</b> In <b>5_resume_analyzer</b>, upload your PDF resume; it automatically extracts your skills and syncs them to your profile!</li>
        <li><b>Run Predictions:</b> In <b>3_career_prediction</b> and <b>4_academic_prediction</b>, select your profile from the sidebar to automatically pre-fill all inputs, or tweak them manually.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Fetch overview counts
_, students_res = get_all_students_api()
_, jobs_res = get_all_jobs_api()
_, apps_res = get_all_applications_api()

total_students = len(students_res.get("students", []))
total_jobs = len(jobs_res.get("jobs", []))
total_apps = len(apps_res.get("applications", []))

# KPI Metrics Ribbon
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Registered Students", total_students, "+1 active demo (Grishma)")
with m2:
    st.metric("Active Job Postings", total_jobs, "Top tech firms")
with m3:
    st.metric("Total Applications", total_apps, "Tracked in real-time")
with m4:
    st.metric("ML Deployed Models", "2 Classifiers", "Random Forest Ensemble")

st.markdown("---")

# Navigation Hub & Portals
st.subheader("🌐 Explore Platform Portals")

tab_student, tab_recruiter, tab_aiml = st.tabs([
    "🎓 Student Portal", 
    "🏢 Recruiter Portal", 
    "🔬 Applied AI / ML Systems"
])

with tab_student:
    st.markdown("""
    <div class="portal-banner">
        <b>Student Experience Suite:</b> Manage academic profile, analyze resumes, run multi-feature career and risk predictions, discover missing skills, and apply to compatible job roles.
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3>👤 Student Profile & CRUD</h3>
            <p>Create, view, edit, and delete student records, technical skills, certifications, and portfolio projects.</p>
            <p>👉 <i>Navigate to Page <b>2_student_profile</b> in sidebar</i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔮 Career Prediction</h3>
            <p>Supervised ML model predicting 10 industry roles based on CGPA, coding skills, AI expertise, and experience.</p>
            <p>👉 <i>Navigate to Page <b>3_career_prediction</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3>⚠️ Academic Risk Prediction</h3>
            <p>Classify academic performance into Low, Medium, or High risk with prescriptive improvement recommendations.</p>
            <p>👉 <i>Navigate to Page <b>4_academic_prediction</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Resume Analyzer</h3>
            <p>Upload PDF resumes to extract contact information, education, skills, and portfolio highlights via NLP.</p>
            <p>👉 <i>Navigate to Page <b>5_resume_analyzer</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with c5:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Skill Gap & Learning</h3>
            <p>Compare student skills against industry requirements and get curated course recommendations for missing skills.</p>
            <p>👉 <i>Navigate to Page <b>6_skill_gap_analysis</b> & <b>7_learning_recommendations</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with c6:
        st.markdown("""
        <div class="feature-card">
            <h3>💼 Job Matching & Application</h3>
            <p>Calculate TF-IDF & Cosine similarity job match scores and submit one-click job applications.</p>
            <p>👉 <i>Navigate to Page <b>8_job_matching</b></i></p>
        </div>
        """, unsafe_allow_html=True)

with tab_recruiter:
    st.markdown("""
    <div class="portal-banner">
        <b>Recruiter Talent Suite:</b> Post tech jobs, view applications, and rank candidate pools using explainable multi-factor scoring.
    </div>
    """, unsafe_allow_html=True)
    
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        <div class="feature-card">
            <h3>🏢 Recruiter Dashboard</h3>
            <p>Monitor hiring metrics, candidate volumes, application statuses, and interview shortlists.</p>
            <p>👉 <i>Navigate to Page <b>9_recruiter_dashboard</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with r2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Job Management CRUD</h3>
            <p>Post new job openings, configure minimum CGPA and skill requirements, update details, or delete listings.</p>
            <p>👉 <i>Navigate to Page <b>10_manage_jobs</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with r3:
        st.markdown("""
        <div class="feature-card">
            <h3>🏆 Candidate AI Ranking</h3>
            <p>Explainable weighted ranking (40% Skill + 25% Resume + 15% CGPA + 10% Projects + 10% Internship).</p>
            <p>👉 <i>Navigate to Page <b>11_candidate_ranking</b></i></p>
        </div>
        """, unsafe_allow_html=True)

with tab_aiml:
    st.markdown("""
    <div class="portal-banner">
        <b>Syllabus Concepts Lab (503):</b> Deep dive into model comparison, hyperparameter tuning, Apriori vs FP-Growth, and Q-Learning.
    </div>
    """, unsafe_allow_html=True)
    
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Model Evaluation & Tuning</h3>
            <p>Interactive evaluation metrics, classification reports, confusion matrices, and Before vs After tuning comparisons.</p>
            <p>👉 <i>Navigate to Page <b>12_model_evaluation</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with a2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔗 Apriori vs FP-Growth Mining</h3>
            <p>Discover frequent skill sets and benchmark runtime performance between candidate generation vs FP-Tree.</p>
            <p>👉 <i>Navigate to Page <b>13_skill_association_apriori_fp</b></i></p>
        </div>
        """, unsafe_allow_html=True)
        
    with a3:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Q-Learning Path Optimizer</h3>
            <p>Educational Reinforcement Learning simulation optimizing step-by-step student learning trajectories.</p>
            <p>👉 <i>Navigate to Page <b>14_rl_learning_path_optimizer</b></i></p>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.title("Navigation")
st.sidebar.info("Use the sidebar pages to navigate between the different portals and modules.")
st.sidebar.markdown("---")
st.sidebar.caption("Subject: 503 – Applied AI: Model Development and Deployment")
