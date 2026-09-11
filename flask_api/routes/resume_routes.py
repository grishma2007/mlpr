"""
Resume Analysis, Skill Gap & Learning Recommendation REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from flask import Blueprint, request, jsonify
from nlp.resume_parser import parse_resume
from recommendation.skill_gap import analyze_skill_gap
from recommendation.learning_recommender import recommend_learning_resources

resume_bp = Blueprint("resume_bp", __name__)

@resume_bp.route("/resume/analyze", methods=["POST"])
def analyze_resume():
    """
    POST /api/resume/analyze
    Accepts multipart PDF file upload or JSON payload containing 'text'.
    Returns structured resume information and extracted skills.
    """
    try:
        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename == "":
                return jsonify({"success": False, "error": "No file selected."}), 400
            file_bytes = uploaded_file.read()
            parsed = parse_resume(file_bytes)
        else:
            data = request.get_json(silent=True)
            if not data or "text" not in data:
                return jsonify({"success": False, "error": "Please provide a PDF file or a JSON object with 'text'."}), 400
            parsed = parse_resume(data["text"])
            
        return jsonify({
            "success": True,
            "parsed_resume": parsed
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Resume analysis failed: {str(e)}"}), 500

@resume_bp.route("/skills/gap", methods=["POST"])
def get_skill_gap():
    """
    POST /api/skills/gap
    Calculates matching skills, missing skills, and readiness percentage against a target role.
    """
    data = request.get_json(silent=True)
    if not data or "skills" not in data or "target_role" not in data:
        return jsonify({"success": False, "error": "Missing 'skills' or 'target_role' in request body."}), 400
        
    skills = data.get("skills", [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]
        
    target_role = data.get("target_role", "Machine Learning Engineer")
    gap_result = analyze_skill_gap(skills, target_role)
    
    return jsonify({
        "success": True,
        "gap_analysis": gap_result
    }), 200

@resume_bp.route("/recommendations/learning", methods=["POST"])
def get_learning_recommendations():
    """
    POST /api/recommendations/learning
    Provides targeted course recommendations for missing skills.
    """
    data = request.get_json(silent=True) or {}
    missing_skills = data.get("missing_skills", [])
    if isinstance(missing_skills, str):
        missing_skills = [s.strip() for s in missing_skills.split(",") if s.strip()]
        
    courses = recommend_learning_resources(missing_skills)
    return jsonify({
        "success": True,
        "recommended_courses": courses,
        "total_recommendations": len(courses)
    }), 200
