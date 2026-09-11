"""
Skill Gap Analysis Engine
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

# Canonical skill profiles required for each industry role
ROLE_SKILL_REQUIREMENTS = {
    "Data Scientist": [
        "Python", "SQL", "Machine Learning", "Deep Learning", "Data Visualization", "Pandas", "NumPy", "Statistics"
    ],
    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Docker", "SQL", "Git"
    ],
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "PyTorch", "Cloud", "Docker"
    ],
    "Data Analyst": [
        "SQL", "Python", "Data Visualization", "Tableau", "PowerBI", "Excel", "Statistics"
    ],
    "Business Analyst": [
        "SQL", "Data Visualization", "PowerBI", "Tableau", "Excel", "Python", "Business Analytics"
    ],
    "Software Developer": [
        "Java", "C++", "Python", "SQL", "Git", "Data Structures", "Algorithms"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git"
    ],
    "Backend Developer": [
        "Python", "Java", "SQL", "Node.js", "Express", "Docker", "REST API", "Git"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React", "TypeScript", "Data Visualization", "Git"
    ],
    "Cloud Engineer": [
        "Cloud", "AWS", "Docker", "Kubernetes", "Linux", "Python", "Git", "CI/CD"
    ]
}

def analyze_skill_gap(current_skills, target_role):
    """
    Compares current student skills against the requirements of a target role.
    Computes matching skills, missing skills, readiness percentage, and prioritization.
    """
    if target_role not in ROLE_SKILL_REQUIREMENTS:
        # Fallback to general ML Engineer requirements if not found
        required_skills = ROLE_SKILL_REQUIREMENTS.get("Machine Learning Engineer")
    else:
        required_skills = ROLE_SKILL_REQUIREMENTS[target_role]
        
    current_set = set(s.strip().lower() for s in current_skills if s.strip())
    
    matching_skills = []
    missing_skills = []
    
    for req in required_skills:
        req_clean = req.strip().lower()
        if req_clean in current_set or any(req_clean in cs or cs in req_clean for cs in current_set):
            matching_skills.append(req)
        else:
            missing_skills.append(req)
            
    total_required = len(required_skills)
    match_count = len(matching_skills)
    match_percentage = round((match_count / total_required) * 100.0, 1) if total_required > 0 else 0.0
    
    if match_percentage >= 75.0:
        readiness_level = "High Readiness"
        readiness_color = "#10b981"  # Emerald Green
    elif match_percentage >= 45.0:
        readiness_level = "Moderate Readiness"
        readiness_color = "#f59e0b"  # Amber
    else:
        readiness_level = "Foundational Stage"
        readiness_color = "#ef4444"  # Crimson
        
    return {
        "target_role": target_role,
        "required_skills": required_skills,
        "current_skills": current_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "readiness_level": readiness_level,
        "readiness_color": readiness_color,
        "total_required_count": total_required,
        "matching_count": match_count,
        "missing_count": len(missing_skills)
    }
