"""
Model Evaluation, Comparison & Tuning Dashboard
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_metrics_api
from components.charts import (
    create_model_comparison_bar_chart,
    create_confusion_matrix_heatmap
)

st.set_page_config(page_title="Model Evaluation & Tuning", page_icon="📈", layout="wide")

st.title("📈 Machine Learning Model Evaluation & Hyperparameter Tuning")
st.markdown("""
Comprehensive evaluation dashboard for **503 – Applied Artificial Intelligence**.
All metrics, confusion matrices, and tuning comparisons are dynamically retrieved from genuine model training execution artifacts (`models/model_metrics.json`).
""")

# Fetch live metrics from Flask API
status_code, res_data = get_metrics_api()

if status_code != 200 or not res_data.get("success"):
    st.error("Model metrics could not be loaded from API. Ensure Flask is running and `ml/evaluate_models.py` has been executed.")
    st.stop()

metrics = res_data.get("metrics", {})
career_data = metrics.get("career_prediction", {})
academic_data = metrics.get("academic_risk", {})

tab_career, tab_academic, tab_ensemble = st.tabs([
    "🎯 Model 1: Career Role Prediction",
    "⚠️ Model 2: Academic Risk Classification",
    "🌲 Ensemble Learning & Parameter Tuning Analysis"
])

# ----------------- TAB 1: CAREER PREDICTION MODEL -----------------
with tab_career:
    st.subheader("🎯 Career Role Prediction - 4 Candidate Models Benchmark")
    
    career_comp = career_data.get("comparison", {})
    if career_comp:
        rows = []
        for m_name, vals in career_comp.items():
            rows.append({
                "Model Architecture": m_name,
                "Accuracy": f"{vals.get('accuracy', 0.0):.4f}",
                "Precision (Weighted)": f"{vals.get('precision', 0.0):.4f}",
                "Recall (Weighted)": f"{vals.get('recall', 0.0):.4f}",
                "F1-Score (Weighted)": f"{vals.get('f1_score', 0.0):.4f}"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        
        st.plotly_chart(
            create_model_comparison_bar_chart(career_comp, metric="accuracy", title="Career Prediction Accuracy Comparison"),
            use_container_width=True
        )
        
    st.markdown("---")
    st.subheader("🔧 Hyperparameter Tuning Results (GridSearchCV)")
    tuning_c = career_data.get("tuning", {})
    
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        st.metric("Untuned Model Accuracy", f"{tuning_c.get('accuracy_before', 0.0)*100:.2f}%")
    with tc2:
        st.metric("GridSearchCV Tuned Accuracy", f"{tuning_c.get('accuracy_after', 0.0)*100:.2f}%", f"{round((tuning_c.get('accuracy_after', 0.0) - tuning_c.get('accuracy_before', 0.0))*100, 2)}%")
    with tc3:
        st.metric("Tuned Model F1-Score", f"{tuning_c.get('f1_after', 0.0)*100:.2f}%")
        
    st.markdown(f"**Optimal Hyperparameters Identified:** `{tuning_c.get('best_parameters')}`")
    
    st.markdown("---")
    st.subheader("📊 Multi-Class Confusion Matrix (10 Career Roles)")
    cm_c = career_data.get("confusion_matrix", [])
    classes_c = career_data.get("classes", [])
    if cm_c and classes_c:
        st.plotly_chart(create_confusion_matrix_heatmap(cm_c, classes_c, title="Career Role Prediction Confusion Matrix"), use_container_width=True)

# ----------------- TAB 2: ACADEMIC RISK MODEL -----------------
with tab_academic:
    st.subheader("⚠️ Academic Risk Model - Benchmark & Single vs Ensemble Comparison")
    
    acad_comp = academic_data.get("comparison", {})
    if acad_comp:
        rows_a = []
        for m_name, vals in acad_comp.items():
            rows_a.append({
                "Model Architecture": m_name,
                "Accuracy": f"{vals.get('accuracy', 0.0):.4f}",
                "Precision": f"{vals.get('precision', 0.0):.4f}",
                "Recall": f"{vals.get('recall', 0.0):.4f}",
                "F1-Score": f"{vals.get('f1_score', 0.0):.4f}"
            })
        st.dataframe(pd.DataFrame(rows_a), use_container_width=True, hide_index=True)
        
        st.plotly_chart(
            create_model_comparison_bar_chart(acad_comp, metric="accuracy", title="Academic Risk Accuracy Comparison"),
            use_container_width=True
        )
        
    st.markdown("---")
    st.subheader("📊 Risk Classification Confusion Matrix (3 Levels)")
    cm_a = academic_data.get("confusion_matrix", [])
    classes_a = academic_data.get("classes", [])
    if cm_a and classes_a:
        st.plotly_chart(create_confusion_matrix_heatmap(cm_a, classes_a, title="Academic Risk Confusion Matrix"), use_container_width=True)

# ----------------- TAB 3: ENSEMBLE LEARNING & TUNING -----------------
with tab_ensemble:
    st.subheader("🌲 Ensemble Learning Concept Demonstration (Syllabus Concept)")
    st.markdown("""
    **Ensemble Learning** is a machine learning paradigm where multiple base models (such as individual Decision Trees) are combined to produce a superior predictive model.
    In **Random Forest**, bagging (Bootstrap Aggregation) and feature subsampling are utilized to reduce variance and combat overfitting.
    """)
    
    sve = academic_data.get("single_vs_ensemble", {})
    if sve:
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("#### 🌳 Single Model: Decision Tree")
            st.metric("Decision Tree Accuracy", f"{sve.get('single_accuracy', 0.0)*100:.2f}%")
            st.metric("Decision Tree F1-Score", f"{sve.get('single_f1', 0.0)*100:.2f}%")
            st.caption("Prone to high variance and sensitivity to training data fluctuations.")
            
        with sc2:
            st.markdown("#### 🌲 Ensemble Model: Random Forest")
            st.metric("Random Forest Accuracy", f"{sve.get('ensemble_accuracy', 0.0)*100:.2f}%", f"+{round((sve.get('ensemble_accuracy', 0.0)-sve.get('single_accuracy', 0.0))*100, 2)}%")
            st.metric("Random Forest F1-Score", f"{sve.get('ensemble_f1', 0.0)*100:.2f}%")
            st.caption("Aggregates N independent decision trees with voting to ensure robust generalization.")
            
    st.markdown("---")
    st.subheader("⚙️ Parameter Tuning Comparison: Before vs After")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("##### Career Prediction Model (Random Forest)")
        tc = career_data.get("tuning", {})
        st.write(f"• **Before Tuning Accuracy:** `{tc.get('accuracy_before')}`")
        st.write(f"• **After Tuning Accuracy:** `{tc.get('accuracy_after')}`")
        st.write(f"• **Best GridSearchCV Parameters:** `{tc.get('best_parameters')}`")
        
    with col_t2:
        st.markdown("##### Academic Risk Model (Random Forest)")
        ta = academic_data.get("tuning", {})
        st.write(f"• **Before Tuning Accuracy:** `{ta.get('accuracy_before')}`")
        st.write(f"• **After Tuning Accuracy:** `{ta.get('accuracy_after')}`")
        st.write(f"• **Best GridSearchCV Parameters:** `{ta.get('best_parameters')}`")
