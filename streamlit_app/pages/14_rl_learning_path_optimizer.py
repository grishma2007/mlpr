"""
Reinforcement Learning Educational Demo: Q-Learning Path Optimizer
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import run_rl_optimizer_api
from components.charts import create_rl_learning_curve

st.set_page_config(page_title="RL Path Optimizer", page_icon="🤖", layout="wide")

st.title("🤖 Reinforcement Learning: Q-Learning Path Optimizer")
st.markdown("""
Educational module demonstrating **Reinforcement Learning** concepts using **Q-Learning** for student learning path trajectory optimization.
- **Agent State:** Student Skill Mastery Tier (Beginner -> Core -> Advanced AI -> Industry Ready).
- **Actions:** Selecting technical study topics and projects.
- **Reward:** Competency gain and course completion bonus.
- **Bellman Equation:** $Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$
""")

# Hyperparameters
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    episodes = st.slider("Training Episodes", min_value=50, max_value=500, value=300, step=50)
with col_p2:
    lr = st.slider("Learning Rate (α)", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
with col_p3:
    gamma = st.slider("Discount Factor (γ)", min_value=0.5, max_value=0.99, value=0.9, step=0.01)

if st.button("🚀 Train Q-Learning Agent & Optimize Learning Path", type="primary"):
    with st.spinner("Training Q-table agent over simulated episodes..."):
        status_code, res_data = run_rl_optimizer_api(episodes=episodes, alpha=lr, gamma=gamma)
        
    if status_code == 200 and res_data.get("success"):
        sim = res_data.get("simulation", {})
        path = sim.get("optimal_path", [])
        q_table_data = sim.get("q_table", {})
        rewards = sim.get("episode_rewards", [])
        
        st.success("### 🎯 Optimal Learning Trajectory Identified by Q-Learning Agent")
        
        for step in path:
            st.markdown(f"""
            <div style="background: #1e293b; border-left: 4px solid #8b5cf6; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155; padding: 1rem 1.25rem; border-radius: 0 8px 8px 0; margin-bottom: 0.75rem; color: #f1f5f9 !important;">
                <b>Step {step['step']}:</b> From State <span style="color: #c4b5fd; font-weight: 600;">[{step['current_state']}]</span>
                👉 Recommended Action: <span style="background: #4c1d95; color: #ede9fe; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600;">{step['recommended_action']}</span>
                (Q-Value: <b>{step['q_value']}</b>) ➔ Progresses To: <span style="color: #6ee7b7; font-weight: 600;">[{step['next_state']}]</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        col_q1, col_q2 = st.columns([1.2, 1])
        with col_q1:
            st.markdown("#### 📈 Cumulative Reward Learning Progression")
            st.plotly_chart(create_rl_learning_curve(rewards), use_container_width=True)
            
        with col_q2:
            st.markdown("#### 🧮 Learned Q-Table Matrix")
            if q_table_data:
                q_df = pd.DataFrame(q_table_data)
                st.dataframe(q_df, use_container_width=True)
    else:
        st.error(f"Simulation failed: {res_data.get('error')}")
