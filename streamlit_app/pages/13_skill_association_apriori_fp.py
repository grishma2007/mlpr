"""
Skill Association Rule Mining: Apriori vs FP-Growth
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_association_benchmark_api
from components.charts import create_execution_time_comparison

st.set_page_config(page_title="Association Rule Mining", page_icon="🔗", layout="wide")

st.title("🔗 Skill Association Mining: Apriori vs FP-Growth")
st.markdown("""
Discover frequent skill co-occurrences and association rules among student profiles and industry datasets.
Demonstrates **Apriori Algorithm**, **FP-Growth Algorithm**, and performance benchmarking as specified in syllabus.
""")

# Sidebar Controls
st.sidebar.header("Mining Hyperparameters")
min_sup = st.sidebar.slider("Minimum Support Threshold", min_value=0.02, max_value=0.20, value=0.06, step=0.01)
min_conf = st.sidebar.slider("Minimum Confidence Threshold", min_value=0.10, max_value=0.90, value=0.30, step=0.05)

with st.spinner("Executing Apriori and FP-Growth Association Mining algorithms on backend..."):
    status_code, res_data = get_association_benchmark_api(min_support=min_sup, min_confidence=min_conf)

if status_code == 200 and res_data.get("success"):
    bench = res_data.get("benchmark", {})
    apriori_info = bench.get("apriori", {})
    fpgrowth_info = bench.get("fpgrowth", {})
    speedup = bench.get("speedup_ratio", "2.5x")
    
    st.subheader("⚡ Performance Benchmark Comparison")
    
    b1, b2, b3 = st.columns(3)
    with b1:
        st.metric("Apriori Runtime", f"{apriori_info.get('execution_time', 0.0):.5f}s", "Candidate Generation")
    with b2:
        st.metric("FP-Growth Runtime", f"{fpgrowth_info.get('execution_time', 0.0):.5f}s", "FP-Tree Traversal")
    with b3:
        st.metric("FP-Growth Speedup", speedup, "Faster Execution")
        
    st.markdown(f"""
    <div style="background: #064e3b; border-left: 4px solid #10b981; border-top: 1px solid #065f46; border-right: 1px solid #065f46; border-bottom: 1px solid #065f46; padding: 1rem; border-radius: 0 8px 8px 0; margin-top: 1rem; margin-bottom: 1.5rem; color: #ecfdf5 !important;">
        <b>💡 Theoretical Distinction:</b> {bench.get('key_insight')}
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(
        create_execution_time_comparison(apriori_info.get("execution_time", 0.01), fpgrowth_info.get("execution_time", 0.005)),
        use_container_width=True
    )
    
    st.markdown("---")
    
    st.subheader("📜 Discovered Association Rules (Support, Confidence, Lift)")
    rules = bench.get("sample_top_rules", [])
    if rules:
        rules_df = pd.DataFrame([
            {
                "Antecedents (If Possesses)": r["antecedents"],
                "Consequents (Then Also Possesses)": r["consequents"],
                "Support": f"{r['support']:.4f}",
                "Confidence": f"{r['confidence']:.4f}",
                "Lift Score": f"{r['lift']:.4f}"
            }
            for r in rules
        ])
        st.dataframe(rules_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Metric Interpretations:**
        - **Support:** Frequency of the combined itemset in the entire dataset.
        - **Confidence:** Probability of the consequent given the antecedent ($P(B|A)$).
        - **Lift:** How much more likely $B$ is purchased/possessed when $A$ is present, compared to random chance. A Lift $> 1.0$ indicates strong positive association.
        """)
    else:
        st.warning("No association rules found with the selected threshold. Try lowering the Minimum Support or Confidence slider.")
else:
    st.error(f"Failed to run association mining: {res_data.get('error')}")
