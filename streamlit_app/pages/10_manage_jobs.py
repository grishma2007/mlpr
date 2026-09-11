"""
Recruiter Job Management with Full CRUD Operations
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
    get_job_api,
    create_job_api,
    update_job_api,
    delete_job_api
)

st.set_page_config(page_title="Manage Jobs CRUD", page_icon="📝", layout="wide")

st.title("📝 Recruiter Job Management")
st.markdown("Perform **CRUD (Create, Read, Update, Delete)** operations on company job listings via Flask REST API endpoints.")

# Fetch Jobs
_, jobs_res = get_all_jobs_api()
jobs = jobs_res.get("jobs", [])

tab_view, tab_create, tab_edit = st.tabs([
    "📋 View Job Listings", 
    "➕ Post New Job Opening", 
    "✏️ Edit / Delete Job Posting"
])

# ---------------- TAB 1: VIEW JOBS ----------------
with tab_view:
    st.subheader("🏢 Active Job Postings")
    if not jobs:
        st.info("No jobs posted yet.")
    else:
        for j in jobs:
            with st.expander(f"💼 {j['title']} - {j.get('company', 'Company')} ({j.get('location', 'Remote')})"):
                st.write(j.get("description", ""))
                st.markdown(f"• **Required Skills:** `{j.get('required_skills')}`")
                st.markdown(f"• **Minimum CGPA:** `{j.get('minimum_cgpa')}` | **Job Type:** `{j.get('job_type')}`")
                st.caption(f"Posted On: {j.get('created_at', 'N/A')}")

# ---------------- TAB 2: CREATE JOB ----------------
with tab_create:
    st.subheader("➕ Post a New Job Opportunity")
    with st.form("create_job_form"):
        cj1, cj2 = st.columns(2)
        with cj1:
            title = st.text_input("Job Title *", placeholder="e.g. Senior Machine Learning Engineer")
            req_skills = st.text_input("Required Skills (comma-separated) *", placeholder="e.g. Python, Machine Learning, Deep Learning, Docker, SQL")
            location = st.text_input("Location", value="Bengaluru / Remote")
        with cj2:
            min_cgpa = st.number_input("Minimum Required CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
            job_type = st.selectbox("Job Type", ["Full-time", "Internship", "Part-time", "Contract"])
            
        desc = st.text_area("Job Description *", placeholder="Describe role expectations, responsibilities, and team culture...")
        
        post_btn = st.form_submit_button("Post Job Listing (HTTP POST)", type="primary")
        if post_btn:
            if not title.strip() or not req_skills.strip() or not desc.strip():
                st.error("Please fill in all required fields (Title, Skills, Description).")
            else:
                payload = {
                    "recruiter_id": 1,
                    "title": title.strip(),
                    "description": desc.strip(),
                    "required_skills": req_skills.strip(),
                    "minimum_cgpa": min_cgpa,
                    "location": location.strip(),
                    "job_type": job_type
                }
                status, res = create_job_api(payload)
                if status == 201 and res.get("success"):
                    st.success("Job posted successfully via Flask API!")
                    st.rerun()
                else:
                    st.error(f"Failed to post job: {res.get('error')}")

# ---------------- TAB 3: EDIT / DELETE JOB ----------------
with tab_edit:
    st.subheader("✏️ Edit or Remove Job Posting")
    if not jobs:
        st.info("No jobs to edit.")
    else:
        j_opts = {j["id"]: f"{j['title']} @ {j.get('company', 'Company')}" for j in jobs}
        sel_jid = st.selectbox("Select Job to Edit/Delete:", options=list(j_opts.keys()), format_func=lambda x: j_opts[x])
        
        _, cur_j_res = get_job_api(sel_jid)
        cur_job = cur_j_res.get("job", {})
        
        if cur_job:
            with st.form("edit_job_form"):
                ej1, ej2 = st.columns(2)
                with ej1:
                    e_title = st.text_input("Job Title", value=cur_job.get("title", ""))
                    e_skills = st.text_input("Required Skills", value=cur_job.get("required_skills", ""))
                    e_loc = st.text_input("Location", value=cur_job.get("location", "Remote"))
                with ej2:
                    e_cgpa = st.number_input("Min CGPA", min_value=0.0, max_value=10.0, value=float(cur_job.get("minimum_cgpa", 6.0)), step=0.1)
                    e_type = st.selectbox("Job Type", ["Full-time", "Internship", "Part-time", "Contract"], index=0 if cur_job.get("job_type")=="Full-time" else 1)
                    
                e_desc = st.text_area("Job Description", value=cur_job.get("description", ""))
                
                update_j_btn = st.form_submit_button("Save Job Updates (HTTP PUT)")
                if update_j_btn:
                    up_payload = {
                        "title": e_title, "required_skills": e_skills, "location": e_loc,
                        "minimum_cgpa": e_cgpa, "job_type": e_type, "description": e_desc
                    }
                    u_status, u_res = update_job_api(sel_jid, up_payload)
                    if u_status == 200 and u_res.get("success"):
                        st.success("Job updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Update failed: {u_res.get('error')}")
                        
            st.markdown("---")
            if st.button(f"🗑️ Delete Job: {cur_job.get('title')}", type="primary"):
                d_status, d_res = delete_job_api(sel_jid)
                if d_status == 200 and d_res.get("success"):
                    st.success("Job deleted successfully.")
                    st.rerun()
                else:
                    st.error(f"Delete failed: {d_res.get('error')}")
