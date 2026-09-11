"""
Skill Gap Analysis Interface
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_skill_gap_api, get_all_students_api, get_student_api
from components.charts import create_gauge_chart

st.set_page_config(page_title="Skill Gap Analysis", page_icon="📊", layout="wide")

st.title("📊 Skill Gap Analysis Engine")
st.markdown("""
Compare student technical skills against industry career benchmarks to compute skill match percentage, identify missing proficiencies, and evaluate career readiness.
""")

# Fetch registered students
_, std_res = get_all_students_api()
students = std_res.get("students", [])

st_opts = {0: "-- Select a Student Profile --"}
if students:
    for s in students:
        st_opts[s["id"]] = f"{s['name']} - {s['email']}"
        
sel_st_id = st.selectbox("Choose Student Profile:", options=list(st_opts.keys()), format_func=lambda x: st_opts[x])

target_roles = [
    "Machine Learning Engineer",
    "Data Scientist",
    "AI Engineer",
    "Data Analyst",
    "Business Analyst",
    "Software Developer",
    "Web Developer",
    "Backend Developer",
    "Frontend Developer",
    "Cloud Engineer"
]

target_role = st.selectbox("Select Target Career Role:", target_roles)

if sel_st_id != 0:
    _, s_obj = get_student_api(sel_st_id)
    student = s_obj.get("student", {})
    user_skills = [s.get("skill_name") for s in student.get("skills", [])]
else:
    default_skills_text = "Python, Machine Learning, Data Visualization, HTML, CSS"
    custom_skills = st.text_input("Enter Current Skills (comma-separated):", value=default_skills_text)
    user_skills = [s.strip() for s in custom_skills.split(",") if s.strip()]

if st.button("🚀 Analyze Skill Gap", type="primary", use_container_width=True):
    with st.spinner("Analyzing skill matrix and role requirements..."):
        status_code, res_data = get_skill_gap_api(user_skills, target_role)
        
    if status_code == 200 and res_data.get("success"):
        gap = res_data.get("gap_analysis", {})
        match_pct = gap.get("match_percentage", 0.0)
        readiness = gap.get("readiness_level", "Foundational")
        color = gap.get("readiness_color", "#3b82f6")
        
        st.success("### 🎯 Skill Gap Assessment Results")
        
        g1, g2 = st.columns([1, 1])
        with g1:
            st.plotly_chart(create_gauge_chart(match_pct, title=f"Role Readiness: {readiness}", color=color), use_container_width=True)
            
        with g2:
            st.markdown(f"#### 🎯 Target Role: **{target_role}**")
            st.markdown(f"• **Total Required Skills:** {gap.get('total_required_count')}")
            st.markdown(f"• **Matching Skills:** {gap.get('matching_count')}")
            st.markdown(f"• **Missing Skills:** {gap.get('missing_count')}")
            st.markdown(f"• **Match Score:** **{match_pct}%**")
            
        st.markdown("---")
        
        col_match, col_miss = st.columns(2)
        with col_match:
            st.markdown("#### ✅ Matching Current Skills")
            matching = gap.get("matching_skills", [])
            if matching:
                for m in matching:
                    st.success(f"✓ {m}")
            else:
                st.warning("No direct skill matches found for this role.")
                
        with col_miss:
            st.markdown("#### ❌ Missing Required Skills (Action Items)")
            missing = gap.get("missing_skills", [])
            if missing:
                for mis in missing:
                    st.error(f"✗ {mis}")
            else:
                st.success("🎉 You possess all essential skills for this role!")
                
        # Link to learning recommendations
        if missing:
            st.markdown("---")
            st.info("💡 Next Step: Head over to **Learning Recommendations** (Page 7) to explore curated courses and certifications for your missing skills.")
            
    else:
        st.error(f"Analysis failed: {res_data.get('error', 'Flask API error')}")
