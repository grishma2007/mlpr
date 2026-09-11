"""
Recruiter Dashboard & Talent Analytics
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import (
    get_all_jobs_api,
    get_all_applications_api,
    update_application_status_api
)
from components.charts import create_donut_chart

st.set_page_config(page_title="Recruiter Dashboard", page_icon="🏢", layout="wide")

st.title("🏢 Recruiter & Talent Acquisition Dashboard")
st.markdown("Monitor recruitment campaigns, review candidate applications, manage hiring pipelines, and track AI match scores.")

# Fetch Jobs & Applications
_, jobs_res = get_all_jobs_api()
jobs = jobs_res.get("jobs", [])

_, apps_res = get_all_applications_api()
apps = apps_res.get("applications", [])

# Top Metric Cards
total_jobs = len(jobs)
total_apps = len(apps)
shortlisted_apps = len([a for a in apps if a.get("status") in ["Shortlisted", "Interview", "Accepted"]])
avg_score = round(sum(float(a.get("match_score", 0.0)) for a in apps) / max(1, total_apps), 1) if total_apps > 0 else 0.0

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Posted Jobs", total_jobs, "Active listings")
with m2:
    st.metric("Total Applicants", total_apps, "Candidates applied")
with m3:
    st.metric("Shortlisted / Interview", shortlisted_apps, "Qualified pool")
with m4:
    st.metric("Avg Candidate Match", f"{avg_score}%", "AI composite score")

st.markdown("---")

# Applications Management Table with Status Actions
st.subheader("📥 Received Candidate Applications")

if not apps:
    st.info("No applications received yet. Students can apply via the **Job Matching** portal.")
else:
    app_rows = []
    for a in apps:
        app_rows.append({
            "App ID": a["id"],
            "Candidate Name": a.get("student_name", "N/A"),
            "Email": a.get("student_email", "N/A"),
            "CGPA": a.get("student_cgpa", 0.0),
            "Job Title": a.get("job_title", "N/A"),
            "Company": a.get("company", "N/A"),
            "Match Score": f"{a.get('match_score', 0.0)}%",
            "Status": a.get("status", "Applied"),
            "Applied Date": a.get("applied_at", "")[:10] if a.get("applied_at") else ""
        })
    df_apps = pd.DataFrame(app_rows)
    st.dataframe(df_apps, use_container_width=True, hide_index=True)
    
    st.markdown("#### 🔄 Update Application Status")
    c_sel, c_stat, c_btn = st.columns([2, 2, 1])
    with c_sel:
        sel_app_id = st.selectbox("Select Application to Update:", options=[a["id"] for a in apps], format_func=lambda x: f"App #{x} - {next((a['student_name'] for a in apps if a['id']==x), '')}")
    with c_stat:
        new_status = st.selectbox("Update Status:", ["Shortlisted", "Interview", "Accepted", "Rejected", "Applied"])
    with c_btn:
        st.write("")
        st.write("")
        if st.button("Update Status (HTTP PUT)"):
            st_code, st_res = update_application_status_api(sel_app_id, new_status)
            if st_code == 200 and st_res.get("success"):
                st.success("Application status updated!")
                st.rerun()
            else:
                st.error(f"Failed to update: {st_res.get('error')}")

st.markdown("---")

# Analytics Charts
st.subheader("📊 Recruitment Pipeline Analytics")
col_ch1, col_ch2 = st.columns(2)

with col_ch1:
    status_counts = {}
    for a in apps:
        s = a.get("status", "Applied")
        status_counts[s] = status_counts.get(s, 0) + 1
    if not status_counts:
        status_counts = {"Applied": 1, "Shortlisted": 1}
    st.plotly_chart(create_donut_chart(status_counts, title="Application Status Distribution"), use_container_width=True)

with col_ch2:
    st.markdown("#### 🏢 Active Job Openings Summary")
    if jobs:
        j_df = pd.DataFrame([
            {
                "Title": j["title"],
                "Location": j.get("location", "Remote"),
                "Type": j.get("job_type", "Full-time"),
                "Min CGPA": j.get("minimum_cgpa", 6.0),
                "Required Skills": j.get("required_skills", "")
            }
            for j in jobs
        ])
        st.dataframe(j_df, use_container_width=True, hide_index=True)
