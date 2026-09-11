"""
Database Initialization and Seeding Script
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import (
    init_db,
    create_student,
    get_student_by_email,
    get_or_create_skill,
    add_student_skill,
    add_project,
    create_recruiter,
    create_job,
    create_application
)

def seed_database():
    print("=== Initializing Career Platform Database ===")
    init_db()
    
    print("--- Seeding Standard Tech Skills ---")
    skills_data = [
        ("Python", "Programming"),
        ("Java", "Programming"),
        ("C++", "Programming"),
        ("JavaScript", "Programming"),
        ("SQL", "Database"),
        ("Machine Learning", "AI/ML"),
        ("Deep Learning", "AI/ML"),
        ("Data Visualization", "Data Science"),
        ("Web Development", "Web"),
        ("Cloud", "Cloud/DevOps"),
        ("Docker", "Cloud/DevOps"),
        ("TensorFlow", "AI/ML"),
        ("PyTorch", "AI/ML"),
        ("React", "Web"),
        ("Node.js", "Web"),
        ("Spring Boot", "Programming"),
        ("Tableau", "Data Science"),
        ("PowerBI", "Data Science"),
        ("AWS", "Cloud/DevOps"),
        ("HTML/CSS", "Web")
    ]
    for name, cat in skills_data:
        get_or_create_skill(name, cat)
        
    print("--- Seeding Demonstration Student Profile (Grishma) ---")
    student = get_student_by_email("grishma@university.edu")
    if not student:
        student = create_student(
            name="Grishma",
            email="grishma@university.edu",
            college="Institute of Technology and Science",
            degree="B.Tech Computer Science & AI",
            branch="Artificial Intelligence",
            semester=6,
            cgpa=8.5
        )
        print(f"Created student: {student['name']} (ID: {student['id']})")
        
        # Add Student Skills
        student_skills = [
            ("Python", "Advanced"),
            ("C++", "Intermediate"),
            ("JavaScript", "Intermediate"),
            ("Machine Learning", "Advanced"),
            ("Data Visualization", "Advanced"),
            ("Web Development", "Intermediate"),
            ("HTML/CSS", "Advanced")
        ]
        for sk_name, prof in student_skills:
            add_student_skill(student["id"], sk_name, proficiency=prof)
            
        # Add Demonstration Project
        add_project(
            student_id=student["id"],
            title="AI-Powered Student Career & Recruitment Platform",
            description="End-to-end multi-tier ML platform with Streamlit frontend, Flask REST APIs, ensemble ML classifiers, Apriori & FP-Growth, and TF-IDF candidate ranking.",
            technologies="Python, Streamlit, Flask, Scikit-Learn, SQLite, Plotly, TF-IDF",
            project_url="https://github.com/example/ai-career-platform"
        )
        
        add_project(
            student_id=student["id"],
            title="Automated Medical Diagnosis using Deep Learning",
            description="Built a convolutional neural network for automated chest X-ray classification with 94% F1-score.",
            technologies="Python, PyTorch, OpenCV, Flask",
            project_url="https://github.com/example/medical-diagnosis"
        )
    else:
        print(f"Student {student['name']} already exists.")
        
    print("--- Seeding Tech Recruiters ---")
    rec1 = create_recruiter(
        name="Sarah Jenkins",
        company="NeuroTech AI Labs",
        email="sarah.jenkins@neurotech.io",
        industry="Artificial Intelligence"
    )
    rec2 = create_recruiter(
        name="Alex Rivera",
        company="CloudScale Systems",
        email="alex.rivera@cloudscale.com",
        industry="Cloud & Enterprise Software"
    )
    rec3 = create_recruiter(
        name="Priya Sharma",
        company="DataSphere Insights",
        email="priya.sharma@datasphere.com",
        industry="Data Analytics & FinTech"
    )
    
    print("--- Seeding Job Openings ---")
    job1 = create_job(
        recruiter_id=rec1["id"],
        title="Machine Learning Engineer",
        description="Looking for an energetic ML engineer to build, evaluate, and deploy scalable ML models into cloud production environments.",
        required_skills="Python, Machine Learning, Deep Learning, SQL, TensorFlow, Docker",
        minimum_cgpa=8.0,
        location="Bengaluru / Remote",
        job_type="Full-time"
    )
    
    job2 = create_job(
        recruiter_id=rec2["id"],
        title="Cloud Software Developer",
        description="Develop high-performance distributed microservices, APIs, and cloud infrastructure.",
        required_skills="Python, Java, Cloud, Docker, SQL, Spring Boot",
        minimum_cgpa=7.5,
        location="Hyderabad / Hybrid",
        job_type="Full-time"
    )
    
    job3 = create_job(
        recruiter_id=rec3["id"],
        title="Junior Data Analyst",
        description="Analyze large-scale student and enterprise data sets, develop executive dashboards and statistical reports.",
        required_skills="Python, SQL, Data Visualization, Tableau, PowerBI",
        minimum_cgpa=7.0,
        location="Pune / Remote",
        job_type="Full-time"
    )
    
    job4 = create_job(
        recruiter_id=rec1["id"],
        title="AI Research Intern",
        description="Internship opportunity to experiment with state-of-the-art transformer models and recommendation algorithms.",
        required_skills="Python, Machine Learning, Deep Learning, PyTorch",
        minimum_cgpa=8.0,
        location="Remote",
        job_type="Internship"
    )
    
    print("--- Seeding Sample Application ---")
    if student and job1:
        create_application(student_id=student["id"], job_id=job1["id"], match_score=87.5)
        print("Seeded sample application for Grishma -> Machine Learning Engineer.")
        
    print("=== Database Seeding Complete! ===")

if __name__ == "__main__":
    seed_database()
