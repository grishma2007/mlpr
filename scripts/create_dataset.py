"""
Dataset Generation Script for Academic Demonstration
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment

Generates:
1. data/raw/career_dataset.csv (Career Role Prediction)
2. data/raw/academic_dataset.csv (Academic Risk Classification)
3. data/raw/learning_resources.csv (Skill Gap Recommendations)
4. data/raw/skill_transactions.csv (Apriori & FP-Growth Association Mining)
"""

import os
import random
import numpy as np
import pandas as pd

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def create_career_dataset(num_samples=2500, output_path="data/raw/career_dataset.csv"):
    """
    Generates synthetic career prediction dataset with realistic feature distributions.
    Target Roles:
    - Data Scientist
    - Machine Learning Engineer
    - Data Analyst
    - AI Engineer
    - Software Developer
    - Web Developer
    - Backend Developer
    - Frontend Developer
    - Business Analyst
    - Cloud Engineer
    """
    set_seed(42)
    roles = [
        "Data Scientist",
        "Machine Learning Engineer",
        "Data Analyst",
        "AI Engineer",
        "Software Developer",
        "Web Developer",
        "Backend Developer",
        "Frontend Developer",
        "Business Analyst",
        "Cloud Engineer"
    ]
    
    # Skill affinity archetypes (base probability of possessing skill given role)
    role_archetypes = {
        "Data Scientist": {
            "cgpa_mean": 8.3, "python": 0.95, "java": 0.25, "cpp": 0.20, "sql": 0.90,
            "machine_learning": 0.95, "deep_learning": 0.70, "data_visualization": 0.90,
            "web_development": 0.20, "cloud": 0.45, "projects_mean": 4.0, "internship_prob": 0.65, "cert_mean": 3.0
        },
        "Machine Learning Engineer": {
            "cgpa_mean": 8.4, "python": 0.98, "java": 0.35, "cpp": 0.50, "sql": 0.75,
            "machine_learning": 0.98, "deep_learning": 0.85, "data_visualization": 0.60,
            "web_development": 0.25, "cloud": 0.60, "projects_mean": 4.5, "internship_prob": 0.70, "cert_mean": 3.2
        },
        "Data Analyst": {
            "cgpa_mean": 7.6, "python": 0.75, "java": 0.15, "cpp": 0.10, "sql": 0.95,
            "machine_learning": 0.45, "deep_learning": 0.15, "data_visualization": 0.95,
            "web_development": 0.15, "cloud": 0.30, "projects_mean": 3.0, "internship_prob": 0.55, "cert_mean": 2.5
        },
        "AI Engineer": {
            "cgpa_mean": 8.6, "python": 0.98, "java": 0.30, "cpp": 0.60, "sql": 0.70,
            "machine_learning": 0.98, "deep_learning": 0.95, "data_visualization": 0.65,
            "web_development": 0.20, "cloud": 0.70, "projects_mean": 5.0, "internship_prob": 0.75, "cert_mean": 3.5
        },
        "Software Developer": {
            "cgpa_mean": 7.8, "python": 0.70, "java": 0.85, "cpp": 0.80, "sql": 0.65,
            "machine_learning": 0.25, "deep_learning": 0.10, "data_visualization": 0.20,
            "web_development": 0.55, "cloud": 0.40, "projects_mean": 3.8, "internship_prob": 0.60, "cert_mean": 2.2
        },
        "Web Developer": {
            "cgpa_mean": 7.3, "python": 0.50, "java": 0.40, "cpp": 0.25, "sql": 0.60,
            "machine_learning": 0.10, "deep_learning": 0.05, "data_visualization": 0.30,
            "web_development": 0.98, "cloud": 0.35, "projects_mean": 3.5, "internship_prob": 0.50, "cert_mean": 2.0
        },
        "Backend Developer": {
            "cgpa_mean": 7.9, "python": 0.85, "java": 0.85, "cpp": 0.65, "sql": 0.90,
            "machine_learning": 0.20, "deep_learning": 0.10, "data_visualization": 0.15,
            "web_development": 0.80, "cloud": 0.65, "projects_mean": 4.2, "internship_prob": 0.65, "cert_mean": 2.4
        },
        "Frontend Developer": {
            "cgpa_mean": 7.2, "python": 0.30, "java": 0.25, "cpp": 0.15, "sql": 0.35,
            "machine_learning": 0.05, "deep_learning": 0.05, "data_visualization": 0.50,
            "web_development": 0.98, "cloud": 0.30, "projects_mean": 3.4, "internship_prob": 0.50, "cert_mean": 1.8
        },
        "Business Analyst": {
            "cgpa_mean": 7.7, "python": 0.45, "java": 0.15, "cpp": 0.10, "sql": 0.85,
            "machine_learning": 0.30, "deep_learning": 0.10, "data_visualization": 0.90,
            "web_development": 0.15, "cloud": 0.25, "projects_mean": 2.8, "internship_prob": 0.55, "cert_mean": 2.8
        },
        "Cloud Engineer": {
            "cgpa_mean": 8.0, "python": 0.75, "java": 0.60, "cpp": 0.35, "sql": 0.65,
            "machine_learning": 0.20, "deep_learning": 0.10, "data_visualization": 0.20,
            "web_development": 0.40, "cloud": 0.98, "projects_mean": 3.8, "internship_prob": 0.65, "cert_mean": 3.4
        }
    }
    
    records = []
    samples_per_role = num_samples // len(roles)
    
    for role in roles:
        arch = role_archetypes[role]
        for _ in range(samples_per_role):
            # CGPA bounded between 5.0 and 10.0
            cgpa = np.clip(np.random.normal(arch["cgpa_mean"], 0.7), 5.0, 10.0)
            
            # Skills sampled as binary variables with archetype probabilities
            python_skill = 1 if random.random() < arch["python"] else 0
            java_skill = 1 if random.random() < arch["java"] else 0
            cpp_skill = 1 if random.random() < arch["cpp"] else 0
            sql_skill = 1 if random.random() < arch["sql"] else 0
            ml_skill = 1 if random.random() < arch["machine_learning"] else 0
            dl_skill = 1 if random.random() < arch["deep_learning"] else 0
            dataviz_skill = 1 if random.random() < arch["data_visualization"] else 0
            webdev_skill = 1 if random.random() < arch["web_development"] else 0
            cloud_skill = 1 if random.random() < arch["cloud"] else 0
            
            # Projects count (integer 0 to 8)
            projects_count = int(np.clip(np.random.poisson(arch["projects_mean"]), 0, 8))
            
            # Internship (0 or 1)
            internship = 1 if random.random() < arch["internship_prob"] else 0
            
            # Certifications count (integer 0 to 6)
            certifications_count = int(np.clip(np.random.poisson(arch["cert_mean"]), 0, 6))
            
            records.append({
                "cgpa": round(float(cgpa), 2),
                "python": python_skill,
                "java": java_skill,
                "cpp": cpp_skill,
                "sql": sql_skill,
                "machine_learning": ml_skill,
                "deep_learning": dl_skill,
                "data_visualization": dataviz_skill,
                "web_development": webdev_skill,
                "cloud": cloud_skill,
                "projects_count": projects_count,
                "internship": internship,
                "certifications_count": certifications_count,
                "career_role": role
            })
            
    df = pd.DataFrame(records)
    # Shuffle records
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records for Career Dataset at: {output_path}")
    return df

def create_academic_dataset(num_samples=2000, output_path="data/raw/academic_dataset.csv"):
    """
    Generates synthetic academic risk dataset for classification demonstration.
    Target:
    - Low Risk
    - Medium Risk
    - High Risk
    """
    set_seed(42)
    records = []
    
    # 3 Risk Archetypes
    risk_configs = [
        {"risk": "Low Risk", "count": int(num_samples * 0.45), "cgpa_mu": 8.5, "att_mu": 88, "prev_mu": 84, "hours_mu": 7.5, "assign_mu": 92, "internal_mu": 26, "fail_mu": 0.05},
        {"risk": "Medium Risk", "count": int(num_samples * 0.35), "cgpa_mu": 6.8, "att_mu": 72, "prev_mu": 65, "hours_mu": 4.2, "assign_mu": 70, "internal_mu": 19, "fail_mu": 0.6},
        {"risk": "High Risk", "count": int(num_samples * 0.20), "cgpa_mu": 5.2, "att_mu": 54, "prev_mu": 48, "hours_mu": 2.0, "assign_mu": 45, "internal_mu": 13, "fail_mu": 2.2}
    ]
    
    for cfg in risk_configs:
        for _ in range(cfg["count"]):
            cgpa = np.clip(np.random.normal(cfg["cgpa_mu"], 0.6), 4.0, 10.0)
            attendance = np.clip(np.random.normal(cfg["att_mu"], 7.0), 30.0, 100.0)
            previous_marks = np.clip(np.random.normal(cfg["prev_mu"], 8.0), 35.0, 100.0)
            study_hours = np.clip(np.random.normal(cfg["hours_mu"], 1.5), 0.5, 12.0)
            assignment_completion = np.clip(np.random.normal(cfg["assign_mu"], 9.0), 20.0, 100.0)
            internal_marks = np.clip(np.random.normal(cfg["internal_mu"], 3.0), 5.0, 30.0)
            failed_subjects = int(np.clip(np.random.poisson(cfg["fail_mu"]), 0, 6))
            
            # Recalculate deterministic risk score with mild noise to maintain consistency
            score = (
                (attendance / 100.0) * 0.25 +
                (cgpa / 10.0) * 0.25 +
                (assignment_completion / 100.0) * 0.20 +
                (internal_marks / 30.0) * 0.15 +
                (study_hours / 10.0) * 0.15 -
                (failed_subjects * 0.12)
            )
            
            if score >= 0.70 and failed_subjects == 0:
                risk_level = "Low Risk"
            elif score >= 0.48 and failed_subjects <= 1:
                risk_level = "Medium Risk"
            else:
                risk_level = "High Risk"
                
            records.append({
                "previous_marks": round(float(previous_marks), 2),
                "attendance": round(float(attendance), 2),
                "study_hours": round(float(study_hours), 2),
                "assignment_completion": round(float(assignment_completion), 2),
                "internal_marks": round(float(internal_marks), 2),
                "failed_subjects": failed_subjects,
                "cgpa": round(float(cgpa), 2),
                "risk_level": risk_level
            })
            
    df = pd.DataFrame(records)
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records for Academic Dataset at: {output_path}")
    return df

def create_learning_resources_dataset(output_path="data/raw/learning_resources.csv"):
    """
    Curated learning catalog for skill gap recommendations.
    """
    resources = [
        {"skill": "Python", "course_name": "Python for Everybody Specialization", "platform": "Coursera", "level": "Beginner", "description": "Master Python basics, data structures, and web scraping.", "url": "https://www.coursera.org/specializations/python"},
        {"skill": "Python", "course_name": "Complete Python Bootcamp: Go from zero to hero", "platform": "Udemy", "level": "Intermediate", "description": "OOP, decorators, generators, and comprehensive project building.", "url": "https://www.udemy.com/course/complete-python-bootcamp/"},
        {"skill": "SQL", "course_name": "SQL for Data Science & Analytics", "platform": "Coursera / UC Davis", "level": "Beginner", "description": "Write complex SQL queries, JOINs, aggregations, and subqueries.", "url": "https://www.coursera.org/learn/sql-for-data-science"},
        {"skill": "SQL", "course_name": "The Complete SQL Bootcamp: Go from Zero to Hero", "platform": "Udemy", "level": "Intermediate", "description": "PostgreSQL database administration, GROUP BY, window functions.", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/"},
        {"skill": "Machine Learning", "course_name": "Machine Learning Specialization", "platform": "Coursera / DeepLearning.AI", "level": "Intermediate", "description": "Supervised learning, linear/logistic regression, neural networks, decision trees.", "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
        {"skill": "Machine Learning", "course_name": "Hands-On Machine Learning with Scikit-Learn", "platform": "O'Reilly / Video Series", "level": "Intermediate", "description": "Classification, regression, ensemble methods, clustering, and PCA.", "url": "https://www.oreilly.com/"},
        {"skill": "Deep Learning", "course_name": "Deep Learning Specialization", "platform": "Coursera / Andrew Ng", "level": "Advanced", "description": "CNNs, RNNs, Transformers, optimization algorithms, and hyperparameter tuning.", "url": "https://www.coursera.org/specializations/deep-learning"},
        {"skill": "Deep Learning", "course_name": "PyTorch for Deep Learning Bootcamp", "platform": "Udemy / ZTM", "level": "Advanced", "description": "Computer vision, NLP, custom architectures using PyTorch and Torchvision.", "url": "https://www.udemy.com/"},
        {"skill": "Data Visualization", "course_name": "Data Visualization with Tableau Specialization", "platform": "Coursera", "level": "Beginner", "description": "Design interactive dashboards, storytelling with data, and visual analytics.", "url": "https://www.coursera.org/specializations/data-visualization"},
        {"skill": "Data Visualization", "course_name": "Python Data Visualization: Matplotlib, Seaborn & Plotly", "platform": "Udemy", "level": "Intermediate", "description": "Interactive data charts, heatmaps, geographical plots, and custom visualizations.", "url": "https://www.udemy.com/"},
        {"skill": "Web Development", "course_name": "The Complete 2026 Web Development Bootcamp", "platform": "Udemy / Angela Yu", "level": "Beginner", "description": "HTML5, CSS3, JavaScript, React, Node.js, Express, and REST APIs.", "url": "https://www.udemy.com/course/the-complete-web-development-bootcamp/"},
        {"skill": "Web Development", "course_name": "Full Stack Open: Modern Web Development", "platform": "University of Helsinki", "level": "Intermediate", "description": "React, Redux, Node.js, REST APIs, GraphQL, TypeScript, and CI/CD.", "url": "https://fullstackopen.com/en/"},
        {"skill": "Cloud", "course_name": "AWS Certified Cloud Practitioner & Solutions Architect", "platform": "A Cloud Guru / Udemy", "level": "Beginner", "description": "EC2, S3, IAM, Lambda, VPC, RDS, and cloud architecture best practices.", "url": "https://acloudguru.com/"},
        {"skill": "Cloud", "course_name": "Google Cloud Associate Cloud Engineer Certification", "platform": "Coursera / Google Cloud", "level": "Intermediate", "description": "GCP infrastructure, Compute Engine, Kubernetes Engine (GKE), and BigQuery.", "url": "https://www.coursera.org/professional-certificates/gcp-cloud-architect"},
        {"skill": "Java", "course_name": "Java Programming Masterclass", "platform": "Udemy / Tim Buchalka", "level": "Beginner", "description": "OOP, Java 17/21 features, collections framework, multithreading, and Spring Boot basics.", "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/"},
        {"skill": "C++", "course_name": "Beginning C++ Programming - From Beginner to Beyond", "platform": "Udemy", "level": "Beginner", "description": "Pointers, memory management, STL containers, modern C++14/17/20 concepts.", "url": "https://www.udemy.com/course/beginning-c-plus-plus-programming/"},
        {"skill": "Docker", "course_name": "Docker & Kubernetes: The Practical Guide", "platform": "Udemy / Academind", "level": "Intermediate", "description": "Containerization, Docker Compose, Kubernetes orchestration, CI/CD integration.", "url": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"},
        {"skill": "TensorFlow", "course_name": "DeepLearning.AI TensorFlow Developer Professional Certificate", "platform": "Coursera", "level": "Intermediate", "description": "Build and train neural networks, CNNs for computer vision, NLP models, and time series.", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice"}
    ]
    df = pd.DataFrame(resources)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} learning resources at: {output_path}")
    return df

def create_skill_transactions(num_transactions=1000, output_path="data/raw/skill_transactions.csv"):
    """
    Generates skill transaction dataset for Association Rule Mining (Apriori and FP-Growth).
    """
    set_seed(42)
    common_skill_clusters = [
        ["Python", "Machine Learning", "Data Visualization", "SQL"],
        ["Python", "SQL", "Data Visualization", "Business Analytics"],
        ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
        ["Java", "Spring Boot", "SQL", "Docker", "Backend Development"],
        ["HTML", "CSS", "JavaScript", "React", "Frontend Development"],
        ["JavaScript", "Node.js", "Express", "MongoDB", "Full Stack Development"],
        ["Python", "Cloud", "Docker", "Kubernetes", "Linux", "DevOps"],
        ["C++", "Data Structures", "Algorithms", "Problem Solving", "Software Development"],
        ["Python", "Deep Learning", "NLP", "Computer Vision", "AI Engineer"],
        ["SQL", "Tableau", "PowerBI", "Excel", "Data Analyst"]
    ]
    
    transactions = []
    for _ in range(num_transactions):
        # Pick 1 or 2 cluster bases
        chosen_cluster = random.choice(common_skill_clusters).copy()
        # Randomly keep 70-100% of the cluster
        k = random.randint(max(2, len(chosen_cluster) - 2), len(chosen_cluster))
        skills_set = set(random.sample(chosen_cluster, k))
        
        # 30% chance to add 1-2 random extra skills
        if random.random() < 0.35:
            extra = random.choice(["Git", "AWS", "FastAPI", "Pandas", "Scikit-Learn", "PostgreSQL"])
            skills_set.add(extra)
            
        transactions.append({"transaction_id": _ + 1, "skills": ", ".join(sorted(list(skills_set)))})
        
    df = pd.DataFrame(transactions)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} transactions for Association Mining at: {output_path}")
    return df

def generate_all():
    print("=== Generating All Academic Demonstration Datasets ===")
    create_career_dataset()
    create_academic_dataset()
    create_learning_resources_dataset()
    create_skill_transactions()
    print("=== Dataset Generation Complete ===")

if __name__ == "__main__":
    generate_all()
