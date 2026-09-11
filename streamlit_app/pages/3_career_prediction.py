"""
Career Role Prediction Interactive ML Interface
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import predict_career_api, get_all_students_api, get_student_api
from components.charts import create_gauge_chart, create_donut_chart

st.set_page_config(page_title="Career Role Prediction", page_icon="🔮", layout="wide")

st.title("🔮 AI Career Role Prediction Model")
st.markdown("""
Supervised Machine Learning classification interface. Provide multiple academic and skill features to predict suitable industry roles.
**Workflow:** `Streamlit Form -> HTTP POST -> Flask REST API -> Saved ML Model (.joblib) -> JSON Response -> Interactive Result`
""")

# Autofill from existing student option
_, std_res = get_all_students_api()
students = std_res.get("students", [])

st.sidebar.header("Pre-fill from Student Profile")
selected_student = None
if students:
    st_opts = {0: "-- Manual Input --"}
    for s in students:
        st_opts[s["id"]] = f"{s['name']} (CGPA: {s.get('cgpa')})"
    sel_st_id = st.sidebar.selectbox("Select Student:", options=list(st_opts.keys()), format_func=lambda x: st_opts[x])
    if sel_st_id != 0:
        _, s_obj = get_student_api(sel_st_id)
        selected_student = s_obj.get("student")

# Default values based on selected student or standard defaults
def has_skill(skill_name):
    if not selected_student:
        return False
    user_skills = [s.get("skill_name", "").lower() for s in selected_student.get("skills", [])]
    return any(skill_name.lower() in us for us in user_skills)

default_cgpa = float(selected_student.get("cgpa", 8.5)) if selected_student else 8.5
default_projects = len(selected_student.get("projects", [])) if selected_student else 3

with st.form("career_prediction_form"):
    st.subheader("1️⃣ Academic & Foundational Attributes")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        cgpa_val = st.slider("Cumulative CGPA (0.0 - 10.0)", min_value=5.0, max_value=10.0, value=default_cgpa, step=0.1)
    with f_col2:
        projects_count = st.number_input("Number of Completed Technical Projects", min_value=0, max_value=10, value=default_projects)
    with f_col3:
        cert_count = st.number_input("Number of Technical Certifications", min_value=0, max_value=10, value=2)
        
    st.markdown("---")
    st.subheader("2️⃣ Technical Skills & Programming Capabilities")
    
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        python_skill = st.toggle("Python", value=has_skill("Python") or True)
        java_skill = st.toggle("Java", value=has_skill("Java"))
        cpp_skill = st.toggle("C / C++", value=has_skill("C++"))
    with s_col2:
        sql_skill = st.toggle("SQL / Databases", value=has_skill("SQL") or True)
        ml_skill = st.toggle("Machine Learning", value=has_skill("Machine Learning") or True)
        dl_skill = st.toggle("Deep Learning", value=has_skill("Deep Learning") or False)
    with s_col3:
        dataviz_skill = st.toggle("Data Visualization", value=has_skill("Data Visualization") or True)
        webdev_skill = st.toggle("Web Development (HTML/CSS/JS)", value=has_skill("Web Development") or False)
        cloud_skill = st.toggle("Cloud Computing (AWS/GCP/Docker)", value=has_skill("Cloud") or False)
    with s_col4:
        internship_exp = st.toggle("Internship / Work Experience", value=True if default_projects >= 2 else False)

    predict_btn = st.form_submit_button("🚀 Predict Career Role via Flask API", type="primary", use_container_width=True)

if predict_btn:
    payload = {
        "cgpa": cgpa_val,
        "python": 1 if python_skill else 0,
        "java": 1 if java_skill else 0,
        "cpp": 1 if cpp_skill else 0,
        "sql": 1 if sql_skill else 0,
        "machine_learning": 1 if ml_skill else 0,
        "deep_learning": 1 if dl_skill else 0,
        "data_visualization": 1 if dataviz_skill else 0,
        "web_development": 1 if webdev_skill else 0,
        "cloud": 1 if cloud_skill else 0,
        "projects_count": projects_count,
        "internship": 1 if internship_exp else 0,
        "certifications_count": cert_count
    }
    
    with st.spinner("Communicating with Flask REST API & Running Model Inference..."):
        status_code, response_data = predict_career_api(payload)
        
    if status_code == 200 and response_data.get("success"):
        predicted_role = response_data.get("predicted_career")
        confidence = response_data.get("confidence", 0.85)
        top_roles = response_data.get("top_career_roles", [])
        
        st.success("### 🎉 Prediction Successful!")
        
        res_c1, res_c2 = st.columns([1.2, 1])
        with res_c1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); padding: 1.5rem; border-radius: 12px; color: white;">
                <h3 style="color: white; margin-bottom: 0.25rem;">Target Career Role:</h3>
                <h1 style="color: #67e8f9; font-size: 2.2rem; margin: 0;">{predicted_role}</h1>
                <p style="margin-top: 0.5rem; color: #e0f2fe;">Model: <b>{response_data.get('model_used', 'RandomForestClassifier')}</b> | Deployed Endpoint: <code>POST /api/predict/career</code></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🔍 Top Role Probabilities")
            prob_dict = {r["role"]: r["probability"] for r in top_roles}
            st.plotly_chart(create_donut_chart(prob_dict, title="Role Probability Distribution"), use_container_width=True)
            
        with res_c2:
            st.markdown("#### 🎯 Model Prediction Confidence")
            conf_pct = round(confidence * 100, 1)
            st.plotly_chart(create_gauge_chart(conf_pct, title="Confidence Score", color="#06b6d4"), use_container_width=True)
            
            st.markdown("##### 📌 Recommended Next Steps:")
            st.info(f"1. Check **Skill Gap Analysis** for {predicted_role} to identify missing tools.")
            st.info("2. Explore **Learning Recommendations** to upskill in deficient areas.")
            st.info("3. Review available roles on the **Job Matching** portal.")
            
    else:
        st.error(f"Prediction Error: {response_data.get('error', 'Flask API communication failed.')}")
