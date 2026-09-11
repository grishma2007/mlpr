"""
Application Tracking REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from flask import Blueprint, request, jsonify
from database.database import (
    create_application,
    get_all_applications,
    get_applications_by_student,
    get_applications_by_job,
    update_application_status
)

application_bp = Blueprint("application_bp", __name__)

@application_bp.route("/applications", methods=["GET"])
def list_applications():
    """GET /api/applications - List all student job applications."""
    apps = get_all_applications()
    return jsonify({"success": True, "count": len(apps), "applications": apps}), 200

@application_bp.route("/applications", methods=["POST"])
def apply_for_job():
    """POST /api/applications - Submit a new job application."""
    data = request.get_json(silent=True)
    if not data or "student_id" not in data or "job_id" not in data:
        return jsonify({"success": False, "error": "Missing 'student_id' or 'job_id'."}), 400
        
    try:
        app = create_application(
            student_id=int(data["student_id"]),
            job_id=int(data["job_id"]),
            match_score=float(data.get("match_score", 0.0))
        )
        return jsonify({"success": True, "message": "Application submitted successfully.", "application": app}), 201
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to submit application: {str(e)}"}), 500

@application_bp.route("/applications/student/<int:student_id>", methods=["GET"])
def student_applications(student_id):
    """GET /api/applications/student/<id> - Get applications submitted by student."""
    apps = get_applications_by_student(student_id)
    return jsonify({"success": True, "count": len(apps), "applications": apps}), 200

@application_bp.route("/applications/job/<int:job_id>", methods=["GET"])
def job_applications(job_id):
    """GET /api/applications/job/<id> - Get applications received for a job."""
    apps = get_applications_by_job(job_id)
    return jsonify({"success": True, "count": len(apps), "applications": apps}), 200

@application_bp.route("/applications/<int:app_id>", methods=["PUT"])
def change_status(app_id):
    """PUT /api/applications/<id> - Update application status (Shortlist/Reject/Accept)."""
    data = request.get_json(silent=True)
    if not data or "status" not in data:
        return jsonify({"success": False, "error": "Missing 'status' field."}), 400
        
    updated = update_application_status(app_id, data["status"])
    if not updated:
        return jsonify({"success": False, "error": f"Application with ID {app_id} not found."}), 404
        
    return jsonify({"success": True, "message": "Status updated successfully.", "application": updated}), 200
