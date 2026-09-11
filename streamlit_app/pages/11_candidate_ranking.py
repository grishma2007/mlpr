"""
Candidate AI Ranking Interface
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_all_jobs_api, rank_candidates_api

st.set_page_config(page_title="Candidate Ranking", page_icon="🏆", layout="wide")

st.title("🏆 AI Candidate Ranking Engine")
st.markdown("""
Recruiter candidate ranking algorithm using explainable weighted scoring:
`Score = 40% Skill Match + 25% Resume Similarity + 15% Academic CGPA + 10% Projects + 10% Internship`
""")

# Fetch Jobs
_, jobs_res = get_all_jobs_api()
jobs = jobs_res.get("jobs", [])

if not jobs:
    st.warning("No jobs posted yet. Please create a job opening in **Manage Jobs**.")
    st.stop()

j_opts = {j["id"]: f"{j['title']} @ {j.get('company', 'Company')} ({j.get('location')})" for j in jobs}
sel_job_id = st.selectbox("Select Target Job for Ranking:", options=list(j_opts.keys()), format_func=lambda x: j_opts[x])
selected_job = next((j for j in jobs if j["id"] == sel_job_id), jobs[0])

st.markdown(f"**Required Job Skills:** `{selected_job.get('required_skills')}` | **Min CGPA:** `{selected_job.get('minimum_cgpa')}`")

if st.button("🚀 Run AI Candidate Ranking Engine", type="primary"):
    with st.spinner("Evaluating and ranking all candidate profiles..."):
        status_code, res_data = rank_candidates_api(sel_job_id)
        
    if status_code == 200 and res_data.get("success"):
        rankings = res_data.get("rankings", [])
        st.success(f"### 🎖️ Ranked {len(rankings)} Candidates for {selected_job.get('title')}")
        
        # Leaderboard Table
        table_rows = []
        for c in rankings:
            table_rows.append({
                "Rank": f"#{c['rank']}",
                "Candidate Name": c["name"],
                "Email": c["email"],
                "CGPA": f"{c['cgpa']}/10",
                "Match Score": f"{c['match_score']}%",
                "Recommendation Status": c["status_badge"]
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("🔍 Explainable Evaluation Rationale for Each Candidate")
        
        for c in rankings:
            with st.expander(f"🏅 Rank #{c['rank']} - {c['name']} ({c['match_score']}%) - {c['status_badge']}"):
                ec1, ec2 = st.columns([1.5, 1])
                with ec1:
                    st.markdown("##### 📝 Natural Language Explanation:")
                    st.info(c["explanation"])
                    
                    st.markdown("##### 🛠️ Matching Technical Skills:")
                    if c["matching_skills"]:
                        st.success(", ".join(c["matching_skills"]))
                    else:
                        st.warning("No explicit skills match.")
                        
                    if c["missing_skills"]:
                        st.markdown("##### ❌ Missing Skills:")
                        st.caption(", ".join(c["missing_skills"]))
                        
                with ec2:
                    st.markdown("##### 📊 Multi-Factor Weight Breakdown:")
                    b = c.get("breakdown", {})
                    st.write(f"• **Skill Match (40%):** {b.get('skill_match', 0)}%")
                    st.write(f"• **Resume Similarity (25%):** {b.get('resume_similarity', 0)}%")
                    st.write(f"• **Academic CGPA (15%):** {b.get('academic_score', 0)}%")
                    st.write(f"• **Projects Factor (10%):** {b.get('project_score', 0)}%")
                    st.write(f"• **Internship Factor (10%):** {b.get('internship_score', 0)}%")
    else:
        st.error(f"Ranking failed: {res_data.get('error', 'API error')}")
