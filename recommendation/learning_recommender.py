"""
Learning Recommendation System
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import pandas as pd

RESOURCES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "learning_resources.csv")

def load_learning_resources():
    if not os.path.exists(RESOURCES_PATH):
        return pd.DataFrame()
    return pd.read_csv(RESOURCES_PATH)

def recommend_learning_resources(missing_skills):
    """
    Recommends high-quality learning resources for a list of missing skills.
    """
    df = load_learning_resources()
    if df.empty:
        return []
    
    recommendations = []
    missing_lower = [s.strip().lower() for s in missing_skills if s.strip()]
    
    for _, row in df.iterrows():
        skill_name = str(row["skill"]).strip().lower()
        if any(skill_name in m or m in skill_name for m in missing_lower):
            recommendations.append({
                "skill": row["skill"],
                "course_name": row["course_name"],
                "platform": row["platform"],
                "level": row["level"],
                "description": row["description"],
                "url": row["url"]
            })
            
    # If no specific matches, provide popular foundation courses
    if not recommendations:
        for _, row in df.head(4).iterrows():
            recommendations.append({
                "skill": row["skill"],
                "course_name": row["course_name"],
                "platform": row["platform"],
                "level": row["level"],
                "description": row["description"],
                "url": row["url"]
            })
            
    return recommendations
