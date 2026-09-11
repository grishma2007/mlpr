"""
Job Matching & Application Interface
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import (
    get_all_students_api,
    get_student_api,
    get_all_jobs_api,
    match_job_api,
    apply_for_job_api
)
from components.charts import create_gauge_chart

st.set_page_config(page_title="Job Matching", page_icon="💼", layout="wide")

st.title("💼 AI Job Matching & Application System")
st.markdown("""
Calculate explainable job compatibility using **TF-IDF Vectorization, Cosine Similarity, Skill Overlap, and Academic Requirements**.
""")

# Fetch Students and Jobs
_, std_res = get_all_students_api()
students = std_res.get("students", [])

_, jobs_res = get_all_jobs_api()
jobs = jobs_res.get("jobs", [])

if not students or not jobs:
    st.warning("Ensure at least one student profile and job posting exist.")
    st.stop()

col_sel_st, col_sel_job = st.columns(2)

with col_sel_st:
    st_opts = {s["id"]: f"{s['name']} (CGPA: {s.get('cgpa')})" for s in students}
    sel_st_id = st.selectbox("1️⃣ Select Candidate Student:", options=list(st_opts.keys()), format_func=lambda x: st_opts[x])
    _, s_obj = get_student_api(sel_st_id)
    student = s_obj.get("student", {})

with col_sel_job:
    job_opts = {j["id"]: f"{j['title']} @ {j.get('company', 'Company')} ({j.get('location')})" for j in jobs}
    sel_job_id = st.selectbox("2️⃣ Select Job Opening to Match:", options=list(job_opts.keys()), format_func=lambda x: job_opts[x])
    selected_job = next((j for j in jobs if j["id"] == sel_job_id), jobs[0])

st.markdown("---")

# Display Job Details
st.subheader(f"🏢 {selected_job['title']} - {selected_job.get('company', 'Company')}")
st.write(selected_job.get("description", ""))
st.caption(f"**Required Skills:** {selected_job.get('required_skills')} | **Min CGPA:** {selected_job.get('minimum_cgpa')} | **Type:** {selected_job.get('job_type')}")

# Match Calculation
if st.button("🔍 Compute Explainable Match Score", type="primary"):
    with st.spinner("Executing TF-IDF vectorization and multi-factor compatibility engine..."):
        status_code, res_data = match_job_api(student, selected_job)
        
    if status_code == 200 and res_data.get("success"):
        match_info = res_data.get("match_result", {})
        overall_score = match_info.get("overall_match_score", 0.0)
        breakdown = match_info.get("score_breakdown", {})
        
        st.success("### 🎯 Compatibility Assessment")
        
        m_col1, m_col2 = st.columns([1, 1.2])
        
        with m_col1:
            st.plotly_chart(create_gauge_chart(overall_score, title="Overall Match Score", color="#2563eb"), use_container_width=True)
            
        with m_col2:
            st.markdown("#### 📊 Explainable Score Breakdown")
            st.write(f"• **40% Skill Match:** {breakdown.get('skill_match', 0)}%")
            st.write(f"• **35% TF-IDF & Cosine Similarity:** {breakdown.get('resume_similarity', 0)}%")
            st.write(f"• **15% CGPA Compatibility:** {breakdown.get('cgpa_compatibility', 0)}%")
            st.write(f"• **10% Project / Experience:** {breakdown.get('experience_score', 0)}%")
            
            st.markdown("##### 📌 Suggestions for Improvement:")
            for sug in match_info.get("suggestions", []):
                st.info(f"👉 {sug}")
                
        st.markdown("---")
        
        # Apply Button
        st.subheader("📝 Submit Application")
        st.write(f"Apply as **{student.get('name')}** for **{selected_job.get('title')}** at **{selected_job.get('company')}**.")
        if st.button("🚀 Confirm & Submit Application (HTTP POST)", type="primary"):
            app_code, app_res = apply_for_job_api(student["id"], selected_job["id"], match_score=overall_score)
            if app_code == 201 and app_res.get("success"):
                st.success("🎉 Application submitted successfully! Recruiter can now view and rank your application.")
            else:
                st.error(f"Application error: {app_res.get('error')}")
                
    else:
        st.error(f"Matching error: {res_data.get('error')}")
