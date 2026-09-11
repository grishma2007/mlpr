"""
Student Dashboard Page
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import (
    get_all_students_api,
    get_student_applications_api,
    predict_career_api,
    predict_academic_risk_api
)
from components.charts import create_gauge_chart, create_radar_skill_chart

st.set_page_config(page_title="Student Dashboard", page_icon="🎓", layout="wide")

st.title("🎓 Student Career & Academic Dashboard")
st.markdown("Comprehensive overview of academic standing, predicted career trajectory, skill competencies, and active job applications.")

# Fetch students
_, students_res = get_all_students_api()
students = students_res.get("students", [])

if not students:
    st.warning("No student profiles found. Please create a profile in the **Student Profile** page.")
    st.stop()

# Select Active Student
student_names = {s["id"]: f"{s['name']} ({s['email']}) - CGPA: {s.get('cgpa', 0.0)}" for s in students}
selected_id = st.selectbox("Select Active Student Profile:", options=list(student_names.keys()), format_func=lambda x: student_names[x])

student = next((s for s in students if s["id"] == selected_id), students[0])

# Top Profile Overview Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Candidate Name", student["name"])
with col2:
    st.metric("Academic CGPA", f"{student.get('cgpa', 0.0)} / 10.0")
with col3:
    st.metric("Current Semester", f"Sem {student.get('semester', 6)}")
with col4:
    st.metric("Branch / Major", student.get("branch", "Computer Science"))

st.markdown("---")

# ML Predictions Quick Assessment
st.subheader("⚡ Real-Time AI Predictions & Readiness")

# Build feature payload from student profile
student_skills = [s.get("skill_name", "").lower() for s in student.get("skills", [])]
features = {
    "cgpa": student.get("cgpa", 8.0),
    "python": 1 if "python" in student_skills else 0,
    "java": 1 if "java" in student_skills else 0,
    "cpp": 1 if "c++" in student_skills or "cpp" in student_skills else 0,
    "sql": 1 if "sql" in student_skills else 0,
    "machine_learning": 1 if "machine learning" in student_skills else 0,
    "deep_learning": 1 if "deep learning" in student_skills else 0,
    "data_visualization": 1 if "data visualization" in student_skills else 0,
    "web_development": 1 if "web development" in student_skills or "html/css" in student_skills else 0,
    "cloud": 1 if "cloud" in student_skills or "aws" in student_skills else 0,
    "projects_count": len(student.get("projects", [])),
    "internship": 1 if len(student.get("projects", [])) > 1 else 0,
    "certifications_count": 2
}

p1, p2, p3 = st.columns([1.2, 1.2, 1.6])

with p1:
    st.markdown("##### 🔮 AI Predicted Career Role")
    status_c, c_res = predict_career_api(features)
    if status_c == 200 and c_res.get("success"):
        pred_role = c_res.get("predicted_career", "Machine Learning Engineer")
        conf = c_res.get("confidence", 0.85)
        st.success(f"**{pred_role}**")
        st.caption(f"Model Confidence: **{conf*100:.1f}%** (Random Forest Ensemble)")
    else:
        st.info("Career Prediction API ready.")
        
with p2:
    st.markdown("##### ⚠️ Academic Risk Assessment")
    acad_payload = {
        "previous_marks": student.get("cgpa", 8.0) * 10,
        "attendance": 88.0,
        "study_hours": 5.0,
        "assignment_completion": 90.0,
        "internal_marks": 25.0,
        "failed_subjects": 0,
        "cgpa": student.get("cgpa", 8.0)
    }
    status_a, a_res = predict_academic_risk_api(acad_payload)
    if status_a == 200 and a_res.get("success"):
        risk = a_res.get("academic_risk", "Low Risk")
        if risk == "Low Risk":
            st.success(f"🟢 **{risk}**")
        elif risk == "Medium Risk":
            st.warning(f"🟡 **{risk}**")
        else:
            st.error(f"🔴 **{risk}**")
        st.caption("Status: Consistent Good Standing")
    else:
        st.info("Academic Risk API ready.")

with p3:
    st.markdown("##### 📈 Career Readiness Indicator")
    readiness_score = min(100, int((student.get("cgpa", 7.0) * 5) + (len(student_skills) * 8) + (len(student.get("projects", [])) * 10)))
    st.plotly_chart(create_gauge_chart(readiness_score, title="Overall Readiness", color="#10b981"), use_container_width=True)

st.markdown("---")

# Two column layout: Skills & Applications
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🛠️ Technical Skills & Competency")
    skills_list = student.get("skills", [])
    if skills_list:
        skills_df = pd.DataFrame([
            {"Skill": s["skill_name"], "Category": s.get("category", "General"), "Proficiency": s.get("proficiency", "Intermediate")}
            for s in skills_list
        ])
        st.dataframe(skills_df, use_container_width=True, hide_index=True)
    else:
        st.info("No skills added yet.")
        
    st.markdown("##### 📂 Portfolio Projects")
    projects_list = student.get("projects", [])
    if projects_list:
        for p in projects_list:
            with st.expander(f"📁 {p['title']}"):
                st.write(p.get("description", ""))
                st.caption(f"Technologies: {p.get('technologies', 'N/A')}")
    else:
        st.info("No portfolio projects added yet.")

with col_right:
    st.subheader("💼 Active Job Applications")
    _, app_res = get_student_applications_api(student["id"])
    apps = app_res.get("applications", [])
    if apps:
        app_df = pd.DataFrame([
            {
                "Job Title": a.get("job_title", "N/A"),
                "Company": a.get("company", "N/A"),
                "Match Score": f"{a.get('match_score', 0.0)}%",
                "Status": a.get("status", "Applied"),
                "Applied Date": a.get("applied_at", "")[:10] if a.get("applied_at") else ""
            }
            for a in apps
        ])
        st.dataframe(app_df, use_container_width=True, hide_index=True)
    else:
        st.info("No applications submitted yet. Browse jobs in **Job Matching** page.")
        
    st.markdown("##### 📊 Skill Radar Profile")
    radar_dict = {
        "Programming": 85 if any(s in student_skills for s in ["python", "java", "c++", "javascript"]) else 40,
        "AI / ML": 90 if "machine learning" in student_skills else 30,
        "Data Analytics": 80 if "data visualization" in student_skills or "sql" in student_skills else 35,
        "Web & Cloud": 75 if "web development" in student_skills or "cloud" in student_skills else 30,
        "Academics": int(student.get("cgpa", 7.0) * 10)
    }
    st.plotly_chart(create_radar_skill_chart(radar_dict), use_container_width=True)
