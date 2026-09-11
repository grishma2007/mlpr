"""
Academic Risk Prediction Interface
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import predict_academic_risk_api, get_all_students_api, get_student_api
from components.charts import create_donut_chart, create_gauge_chart

st.set_page_config(page_title="Academic Risk Prediction", page_icon="⚠️", layout="wide")

st.title("⚠️ Academic Performance Risk Classifier")
st.markdown("""
Supervised Machine Learning classification model evaluating academic risk into **Low Risk**, **Medium Risk**, or **High Risk**.
Communicates via HTTP POST with Flask backend: `POST /api/predict/academic-risk`.
""")

# Autofill option from student profile
_, std_res = get_all_students_api()
students = std_res.get("students", [])

st.sidebar.header("Pre-fill from Student Profile")
selected_student = None
if students:
    st_opts = {0: "-- Manual Input --"}
    for s in students:
        st_opts[s["id"]] = f"{s['name']} (CGPA: {s.get('cgpa')})"
    sel_st_id = st.sidebar.selectbox("Select Student:", options=list(st_opts.keys()), format_func=lambda x: st_opts[x], key="acad_sel")
    if sel_st_id != 0:
        _, s_obj = get_student_api(sel_st_id)
        selected_student = s_obj.get("student")

default_cgpa = float(selected_student.get("cgpa", 8.2)) if selected_student else 8.2

with st.form("academic_risk_form"):
    st.subheader("Academic Indicators & Performance Metrics")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        cgpa = st.number_input("Cumulative CGPA (0.0 - 10.0)", min_value=0.0, max_value=10.0, value=default_cgpa, step=0.1)
        attendance = st.slider("Class Attendance Percentage (%)", min_value=30.0, max_value=100.0, value=88.0, step=1.0)
        
    with c2:
        prev_marks = st.slider("Previous Semester Marks / Percentage (%)", min_value=30.0, max_value=100.0, value=82.0, step=1.0)
        internal_marks = st.number_input("Internal Exam Marks (out of 30)", min_value=0.0, max_value=30.0, value=25.0, step=0.5)
        
    with c3:
        study_hours = st.slider("Daily Self-Study Hours", min_value=0.5, max_value=12.0, value=4.5, step=0.5)
        assign_comp = st.slider("Assignment Completion Rate (%)", min_value=20.0, max_value=100.0, value=92.0, step=1.0)
        failed_subs = st.number_input("Number of Failed / Backlog Subjects", min_value=0, max_value=8, value=0)
        
    predict_acad_btn = st.form_submit_button("🔍 Classify Academic Risk via Flask API", type="primary", use_container_width=True)

if predict_acad_btn:
    payload = {
        "previous_marks": prev_marks,
        "attendance": attendance,
        "study_hours": study_hours,
        "assignment_completion": assign_comp,
        "internal_marks": internal_marks,
        "failed_subjects": failed_subs,
        "cgpa": cgpa
    }
    
    with st.spinner("Classifying Academic Risk Level..."):
        status_code, response_data = predict_academic_risk_api(payload)
        
    if status_code == 200 and response_data.get("success"):
        risk_level = response_data.get("academic_risk")
        confidence = response_data.get("confidence", 0.90)
        risk_probs = response_data.get("risk_probabilities", {})
        recommendations = response_data.get("recommendations", [])
        
        st.success("### 📊 Assessment Complete!")
        
        rc1, rc2 = st.columns([1.2, 1])
        with rc1:
            if risk_level == "Low Risk":
                card_bg = "linear-gradient(135deg, #065f46, #10b981)"
                badge = "🟢 LOW ACADEMIC RISK"
            elif risk_level == "Medium Risk":
                card_bg = "linear-gradient(135deg, #92400e, #f59e0b)"
                badge = "🟡 MEDIUM ACADEMIC RISK"
            else:
                card_bg = "linear-gradient(135deg, #991b1b, #ef4444)"
                badge = "🔴 HIGH ACADEMIC RISK"
                
            st.markdown(f"""
            <div style="background: {card_bg}; padding: 1.5rem; border-radius: 12px; color: white;">
                <h3 style="color: white; margin-bottom: 0.25rem;">Academic Risk Classification:</h3>
                <h1 style="color: white; font-size: 2.2rem; margin: 0;">{badge}</h1>
                <p style="margin-top: 0.5rem; color: #f0fdf4;">Model: <b>{response_data.get('model_used', 'RandomForestClassifier')}</b> | Endpoint: <code>POST /api/predict/academic-risk</code></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 💡 Prescriptive Academic Recommendations")
            for rec in recommendations:
                st.info(f"👉 {rec}")
                
        with rc2:
            st.markdown("#### 📈 Probability Distribution")
            if risk_probs:
                st.plotly_chart(create_donut_chart(risk_probs, title="Risk Level Probabilities"), use_container_width=True)
            else:
                st.plotly_chart(create_gauge_chart(confidence * 100, title="Confidence", color="#10b981"), use_container_width=True)
                
    else:
        st.error(f"Prediction Error: {response_data.get('error', 'Flask API connection failed.')}")
