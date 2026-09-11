"""
Explainable Job Matching Engine using TF-IDF, Cosine Similarity & Weighted Compatibility
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp.skill_extractor import extract_skills_from_text

def compute_job_match(student_profile, job):
    """
    Computes an explainable multi-component job match score:
    - 40% Skill Match
    - 35% TF-IDF & Cosine Resume Similarity
    - 15% Academic / CGPA Compatibility
    - 10% Experience / Internship Compatibility
    """
    # 1. Parse Required Job Skills
    job_skills_raw = job.get("required_skills", "")
    if isinstance(job_skills_raw, list):
        job_skills = [s.strip() for s in job_skills_raw if s.strip()]
    else:
        job_skills = [s.strip() for s in job_skills_raw.split(",") if s.strip()]
        
    student_skills_raw = student_profile.get("skills", [])
    if isinstance(student_skills_raw, list):
        if student_skills_raw and isinstance(student_skills_raw[0], dict):
            student_skills = [s.get("skill_name", "") for s in student_skills_raw if s.get("skill_name")]
        else:
            student_skills = [str(s).strip() for s in student_skills_raw if str(s).strip()]
    else:
        student_skills = [s.strip() for s in str(student_skills_raw).split(",") if s.strip()]
        
    student_skills_lower = set(s.lower() for s in student_skills)
    
    # Skill matching
    matching_skills = []
    missing_skills = []
    for js in job_skills:
        js_lower = js.lower()
        if js_lower in student_skills_lower or any(js_lower in ss or ss in js_lower for ss in student_skills_lower):
            matching_skills.append(js)
        else:
            missing_skills.append(js)
            
    skill_match_score = (len(matching_skills) / max(1, len(job_skills))) * 100.0
    
    # 2. TF-IDF & Cosine Similarity on Full Text
    student_text = f"{student_profile.get('name', '')} {student_profile.get('degree', '')} {student_profile.get('branch', '')} {' '.join(student_skills)} {student_profile.get('resume_text', '')}"
    job_text = f"{job.get('title', '')} {job.get('description', '')} {' '.join(job_skills)}"
    
    try:
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform([student_text, job_text])
        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        resume_sim_score = max(0.0, min(100.0, float(cos_sim) * 100.0))
    except Exception:
        resume_sim_score = 50.0
        
    # 3. CGPA Compatibility Score
    min_cgpa = float(job.get("minimum_cgpa", 6.0))
    student_cgpa = float(student_profile.get("cgpa", 7.0))
    if student_cgpa >= min_cgpa:
        cgpa_score = 100.0
    else:
        # Proportional deduction
        cgpa_score = max(0.0, (student_cgpa / max(0.1, min_cgpa)) * 100.0)
        
    # 4. Internship / Experience Compatibility
    has_internship = student_profile.get("internship", 0) or len(student_profile.get("projects", [])) > 1
    experience_score = 100.0 if has_internship else 50.0
    
    # 5. Explainable Weighted Combination
    overall_match_score = round(
        0.40 * skill_match_score +
        0.35 * resume_sim_score +
        0.15 * cgpa_score +
        0.10 * experience_score,
        1
    )
    
    # Improvement Suggestions
    suggestions = []
    if missing_skills:
        suggestions.append(f"Acquire high-demand skills: {', '.join(missing_skills[:3])}")
    if student_cgpa < min_cgpa:
        suggestions.append(f"Job minimum CGPA is {min_cgpa}; student CGPA is {student_cgpa}")
    if not has_internship:
        suggestions.append("Add verified project or internship experience to boost ranking")
    if not suggestions:
        suggestions.append("Candidate profile meets all critical requirements for this role!")
        
    return {
        "job_id": job.get("id"),
        "job_title": job.get("title"),
        "company": job.get("company", "Company"),
        "overall_match_score": overall_match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "score_breakdown": {
            "skill_match": round(skill_match_score, 1),
            "resume_similarity": round(resume_sim_score, 1),
            "cgpa_compatibility": round(cgpa_score, 1),
            "experience_score": round(experience_score, 1)
        },
        "suggestions": suggestions
    }
