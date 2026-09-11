"""
Learning Recommendations Interface
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_learning_recommendations_api

st.set_page_config(page_title="Learning Recommendations", page_icon="📚", layout="wide")

st.title("📚 Personalized Learning Resource Recommender")
st.markdown("""
Get targeted courses, certifications, and hands-on tutorials specifically matched to your identified skill gaps.
""")

# Pre-select common missing skills
all_tech_options = [
    "SQL", "Deep Learning", "Docker", "TensorFlow", "PyTorch", "Cloud",
    "Data Visualization", "Web Development", "Python", "Java", "C++"
]

selected_skills = st.multiselect(
    "Select Missing Skills to Upskill:",
    options=all_tech_options,
    default=["SQL", "Deep Learning", "Docker"]
)

if selected_skills:
    with st.spinner("Fetching curated learning catalog recommendations..."):
        status_code, res_data = get_learning_recommendations_api(selected_skills)
        
    if status_code == 200 and res_data.get("success"):
        courses = res_data.get("recommended_courses", [])
        st.subheader(f"🎓 Recommended Courses ({len(courses)} Found)")
        
        for idx, c in enumerate(courses):
            with st.container():
                st.markdown(f"""
                <div style="background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 1.25rem; margin-bottom: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #60a5fa !important;">{c['course_name']}</h4>
                        <span style="background: #0f172a; color: #38bdf8; border: 1px solid #0284c7; padding: 0.25rem 0.6rem; border-radius: 6px; font-weight: 600; font-size: 0.8rem;">{c['level']}</span>
                    </div>
                    <p style="margin-top: 0.5rem; color: #cbd5e1 !important; margin-bottom: 0.35rem;"><b>Target Skill:</b> <span style="color: #38bdf8; font-weight: 600;">{c['skill']}</span> | <b>Platform:</b> {c['platform']}</p>
                    <p style="color: #94a3b8 !important; font-size: 0.92rem; margin-bottom: 0.5rem;">{c['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"🔗 View Course on {c['platform']}", c.get("url", "https://coursera.org"), key=f"course_btn_{idx}")
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.error(f"Failed to fetch recommendations: {res_data.get('error')}")
else:
    st.info("Please select at least one skill above to view learning recommendations.")
