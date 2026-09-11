"""
Job CRUD, Matching and Candidate Ranking REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from flask import Blueprint, request, jsonify
from database.database import (
    create_job,
    get_all_jobs,
    get_job_by_id,
    update_job,
    delete_job,
    get_all_students,
    get_student_by_id,
    get_all_recruiters
)
from flask_api.utils.validators import validate_job_input
from recommendation.job_matcher import compute_job_match
from ranking.candidate_ranker import rank_candidates_for_job

job_bp = Blueprint("job_bp", __name__)

@job_bp.route("/jobs", methods=["GET"])
def list_jobs():
    """GET /api/jobs - List all active job postings."""
    jobs = get_all_jobs()
    return jsonify({"success": True, "count": len(jobs), "jobs": jobs}), 200

@job_bp.route("/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):
    """GET /api/jobs/<id> - Get single job posting."""
    job = get_job_by_id(job_id)
    if not job:
        return jsonify({"success": False, "error": f"Job with ID {job_id} not found."}), 404
    return jsonify({"success": True, "job": job}), 200

@job_bp.route("/jobs", methods=["POST"])
def post_job():
    """POST /api/jobs - Create a new recruiter job posting."""
    data = request.get_json(silent=True)
    is_valid, err_msg = validate_job_input(data)
    if not is_valid:
        return jsonify({"success": False, "error": err_msg}), 400
        
    try:
        recruiter_id = data.get("recruiter_id", 1)
        job = create_job(
            recruiter_id=recruiter_id,
            title=data["title"].strip(),
            description=data.get("description", ""),
            required_skills=data["required_skills"].strip(),
            minimum_cgpa=float(data.get("minimum_cgpa", 6.0)),
            location=data.get("location", "Remote"),
            job_type=data.get("job_type", "Full-time")
        )
        return jsonify({"success": True, "message": "Job posted successfully.", "job": job}), 201
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to create job: {str(e)}"}), 500

@job_bp.route("/jobs/<int:job_id>", methods=["PUT"])
def edit_job(job_id):
    """PUT /api/jobs/<id> - Update existing job posting."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "No update data provided."}), 400
        
    updated = update_job(job_id, data)
    if not updated:
        return jsonify({"success": False, "error": f"Job with ID {job_id} not found."}), 404
    return jsonify({"success": True, "message": "Job updated successfully.", "job": updated}), 200

@job_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
def remove_job(job_id):
    """DELETE /api/jobs/<id> - Delete job posting."""
    success = delete_job(job_id)
    if not success:
        return jsonify({"success": False, "error": f"Job with ID {job_id} not found."}), 404
    return jsonify({"success": True, "message": f"Job {job_id} deleted successfully."}), 200

@job_bp.route("/jobs/match", methods=["POST"])
def match_job():
    """
    POST /api/jobs/match
    Calculates TF-IDF & Skill Match score for a student and job.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Missing payload."}), 400
        
    student_profile = data.get("student")
    student_id = data.get("student_id")
    job_id = data.get("job_id")
    job_data = data.get("job")
    
    if student_id and not student_profile:
        student_profile = get_student_by_id(student_id)
    if job_id and not job_data:
        job_data = get_job_by_id(job_id)
        
    if not student_profile or not job_data:
        return jsonify({"success": False, "error": "Valid student profile and job data required."}), 400
        
    match_result = compute_job_match(student_profile, job_data)
    return jsonify({"success": True, "match_result": match_result}), 200

@job_bp.route("/jobs/<int:job_id>/rank-candidates", methods=["GET", "POST"])
def rank_candidates(job_id):
    """
    POST /api/jobs/<id>/rank-candidates
    Ranks all registered students against the job using weighted AI scoring.
    """
    job = get_job_by_id(job_id)
    if not job:
        return jsonify({"success": False, "error": f"Job with ID {job_id} not found."}), 404
        
    candidates = get_all_students()
    ranked = rank_candidates_for_job(job, candidates)
    
    return jsonify({
        "success": True,
        "job": job,
        "total_candidates": len(ranked),
        "rankings": ranked
    }), 200

@job_bp.route("/recruiters", methods=["GET"])
def list_recruiters():
    """GET /api/recruiters - List all recruiters."""
    recs = get_all_recruiters()
    return jsonify({"success": True, "recruiters": recs}), 200
