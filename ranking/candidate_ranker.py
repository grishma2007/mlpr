"""
Recruiter Candidate Ranking Engine
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from recommendation.job_matcher import compute_job_match

def rank_candidates_for_job(job, candidate_profiles):
    """
    Ranks a list of candidate profiles for a given job posting.
    Formula:
      Score = 40% Skill Match + 25% Resume Similarity + 15% Academic CGPA + 10% Projects + 10% Internship
    """
    scored_candidates = []
    
    for candidate in candidate_profiles:
        match_result = compute_job_match(candidate, job)
        
        # Additional Candidate Academic and Portfolio Factor calculations
        cgpa = float(candidate.get("cgpa", 7.0))
        cgpa_normalized = min(100.0, (cgpa / 10.0) * 100.0)
        
        projects = candidate.get("projects", [])
        project_score = min(100.0, len(projects) * 35.0)
        
        has_internship = candidate.get("internship", 0)
        internship_score = 100.0 if has_internship else (50.0 if len(projects) >= 2 else 20.0)
        
        skill_score = match_result["score_breakdown"]["skill_match"]
        resume_sim = match_result["score_breakdown"]["resume_similarity"]
        
        # Explicit Weighted Rank Formula
        composite_score = round(
            0.40 * skill_score +
            0.25 * resume_sim +
            0.15 * cgpa_normalized +
            0.10 * project_score +
            0.10 * internship_score,
            1
        )
        
        # Recommendation Tier
        if composite_score >= 80.0:
            status = "Recommended"
            status_badge = "🟢 Highly Recommended"
        elif composite_score >= 65.0:
            status = "Strong"
            status_badge = "🟡 Strong Fit"
        elif composite_score >= 50.0:
            status = "Moderate"
            status_badge = "🟠 Moderate Match"
        else:
            status = "Needs Development"
            status_badge = "⚪ Under Consideration"
            
        # Detailed Natural Language Explanation for Viva and Recruiter
        explanation = (
            f"Match Score: {composite_score}%. "
            f"Possesses {len(match_result['matching_skills'])} matching skills ({', '.join(match_result['matching_skills'][:3]) or 'None'}). "
            f"CGPA: {cgpa}/10.0, {len(projects)} completed project(s), "
            f"{'with' if has_internship else 'without'} prior internship experience."
        )
        
        scored_candidates.append({
            "student_id": candidate.get("id"),
            "name": candidate.get("name", "Student"),
            "email": candidate.get("email", ""),
            "cgpa": cgpa,
            "match_score": composite_score,
            "status": status,
            "status_badge": status_badge,
            "matching_skills": match_result["matching_skills"],
            "missing_skills": match_result["missing_skills"],
            "breakdown": {
                "skill_match": skill_score,
                "resume_similarity": resume_sim,
                "academic_score": round(cgpa_normalized, 1),
                "project_score": round(project_score, 1),
                "internship_score": round(internship_score, 1)
            },
            "explanation": explanation
        })
        
    # Sort by match_score descending
    scored_candidates.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Assign ranks
    for idx, c in enumerate(scored_candidates):
        c["rank"] = idx + 1
        
    return scored_candidates
