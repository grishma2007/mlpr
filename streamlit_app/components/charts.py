"""
Reusable Plotly Interactive Visualization Components
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_gauge_chart(score, title="Match Score", color="#3b82f6"):
    """Creates a circular gauge chart for scores between 0 and 100."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": title, "font": {"size": 20, "color": "#1e293b"}},
        number={"suffix": "%", "font": {"size": 28, "color": "#0f172a"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#f1f5f9",
            "borderwidth": 2,
            "bordercolor": "#cbd5e1",
            "steps": [
                {"range": [0, 50], "color": "#fee2e2"},
                {"range": [50, 75], "color": "#fef3c7"},
                {"range": [75, 100], "color": "#d1fae5"}
            ],
            "threshold": {
                "line": {"color": "#10b981", "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig

def create_model_comparison_bar_chart(comparison_dict, metric="accuracy", title="Model Performance Comparison"):
    """Bar chart comparing multiple candidate classifiers."""
    models = list(comparison_dict.keys())
    scores = [comparison_dict[m].get(metric, 0.0) for m in models]
    
    colors = ["#6366f1", "#06b6d4", "#f59e0b", "#10b981"]
    
    fig = go.Figure(data=[
        go.Bar(
            x=models,
            y=scores,
            text=[f"{s:.4f}" for s in scores],
            textposition="auto",
            marker=dict(color=colors[:len(models)], line=dict(color="#1e293b", width=1))
        )
    ])
    fig.update_layout(
        title=f"<b>{title} ({metric.capitalize()})</b>",
        xaxis_title="Candidate Model",
        yaxis_title=metric.capitalize(),
        yaxis=dict(range=[0, 1.05]),
        height=380,
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor="#f8fafc"
    )
    return fig

def create_confusion_matrix_heatmap(cm, classes, title="Confusion Matrix"):
    """Heatmap visualization for classification confusion matrix."""
    fig = px.imshow(
        cm,
        labels=dict(x="Predicted Class", y="True Class", color="Count"),
        x=classes,
        y=classes,
        text_auto=True,
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        title=f"<b>{title}</b>",
        height=480,
        margin=dict(l=50, r=30, t=60, b=50),
        xaxis_tickangle=-45
    )
    return fig

def create_radar_skill_chart(skills_dict, title="Student Skill Competency Profile"):
    """Radar chart for student skill categories."""
    categories = list(skills_dict.keys())
    values = list(skills_dict.values())
    
    if not categories:
        categories = ["Programming", "AI/ML", "Web", "Database", "Cloud"]
        values = [80, 85, 70, 75, 60]
        
    categories += [categories[0]]
    values += [values[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(59, 130, 246, 0.3)",
        line=dict(color="#2563eb", width=2),
        name="Skill Score"
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        title=f"<b>{title}</b>",
        height=360,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def create_execution_time_comparison(apriori_time, fpgrowth_time):
    """Bar chart comparing runtime between Apriori and FP-Growth."""
    fig = go.Figure(data=[
        go.Bar(
            x=["Apriori (Candidate Generation)", "FP-Growth (FP-Tree Traversal)"],
            y=[apriori_time, fpgrowth_time],
            text=[f"{apriori_time:.5f}s", f"{fpgrowth_time:.5f}s"],
            textposition="auto",
            marker=dict(color=["#ef4444", "#10b981"])
        )
    ])
    fig.update_layout(
        title="<b>Algorithm Execution Time Comparison (Seconds)</b>",
        yaxis_title="Time (seconds) - Lower is Better",
        height=360,
        margin=dict(l=40, r=20, t=50, b=40)
    )
    return fig

def create_rl_learning_curve(rewards):
    """Line plot showing Q-Learning cumulative reward optimization."""
    episodes = [i + 1 for i in range(len(rewards))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=episodes,
        y=rewards,
        mode="lines+markers",
        line=dict(color="#8b5cf6", width=2),
        marker=dict(size=5, color="#6d28d9"),
        name="Episode Reward"
    ))
    fig.update_layout(
        title="<b>Q-Learning Optimization: Reward Progression over Training Episodes</b>",
        xaxis_title="Training Checkpoints",
        yaxis_title="Cumulative Reward",
        height=360,
        margin=dict(l=40, r=20, t=50, b=40)
    )
    return fig

def create_donut_chart(probabilities_dict, title="Prediction Probability Breakdown"):
    """Donut chart for class probabilities."""
    labels = list(probabilities_dict.keys())
    values = list(probabilities_dict.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.45,
        textinfo="label+percent",
        marker=dict(colors=["#10b981", "#f59e0b", "#ef4444", "#3b82f6", "#8b5cf6"])
    )])
    fig.update_layout(
        title=f"<b>{title}</b>",
        height=340,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig
