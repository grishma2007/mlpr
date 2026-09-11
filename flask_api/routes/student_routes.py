"""
Student CRUD REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from flask import Blueprint, request, jsonify
from database.database import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,
    add_student_skill,
    remove_student_skill,
    add_project,
    delete_project,
    get_all_skills
)
from flask_api.utils.validators import validate_student_input

student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/students", methods=["GET"])
def list_students():
    """GET /api/students - List all student profiles."""
    students = get_all_students()
    return jsonify({"success": True, "count": len(students), "students": students}), 200

@student_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """GET /api/students/<id> - Get single student profile."""
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
    return jsonify({"success": True, "student": student}), 200

@student_bp.route("/students", methods=["POST"])
def register_student():
    """POST /api/students - Register a new student profile."""
    data = request.get_json(silent=True)
    is_valid, err_msg = validate_student_input(data)
    if not is_valid:
        return jsonify({"success": False, "error": err_msg}), 400
        
    try:
        student = create_student(
            name=data["name"].strip(),
            email=data["email"].strip(),
            college=data.get("college", ""),
            degree=data.get("degree", "B.Tech"),
            branch=data.get("branch", "Computer Science"),
            semester=int(data.get("semester", 6)),
            cgpa=float(data.get("cgpa", 8.0))
        )
        return jsonify({"success": True, "message": "Student created successfully.", "student": student}), 201
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to create student: {str(e)}"}), 500

@student_bp.route("/students/<int:student_id>", methods=["PUT"])
def edit_student(student_id):
    """PUT /api/students/<id> - Update student profile."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "No update data provided."}), 400
        
    updated = update_student(student_id, data)
    if not updated:
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
        
    return jsonify({"success": True, "message": "Student updated successfully.", "student": updated}), 200

@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
def remove_student(student_id):
    """DELETE /api/students/<id> - Delete student profile."""
    success = delete_student(student_id)
    if not success:
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
    return jsonify({"success": True, "message": f"Student {student_id} deleted successfully."}), 200

@student_bp.route("/students/<int:student_id>/skills", methods=["POST"])
def add_skill(student_id):
    """POST /api/students/<id>/skills - Add skill to student."""
    data = request.get_json(silent=True)
    if not data or "skill_name" not in data:
        return jsonify({"success": False, "error": "Missing 'skill_name' in request."}), 400
        
    skill_rec = add_student_skill(
        student_id=student_id,
        skill_name=data["skill_name"].strip(),
        proficiency=data.get("proficiency", "Intermediate"),
        category=data.get("category", "General")
    )
    return jsonify({"success": True, "message": "Skill added.", "skill": skill_rec}), 201

@student_bp.route("/students/<int:student_id>/skills/<int:skill_id>", methods=["DELETE"])
def delete_skill(student_id, skill_id):
    """DELETE /api/students/<id>/skills/<skill_id> - Remove skill from student."""
    success = remove_student_skill(student_id, skill_id)
    if not success:
        return jsonify({"success": False, "error": "Skill record not found."}), 404
    return jsonify({"success": True, "message": "Skill removed successfully."}), 200

@student_bp.route("/students/<int:student_id>/projects", methods=["POST"])
def add_student_project(student_id):
    """POST /api/students/<id>/projects - Add project to student profile."""
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"success": False, "error": "Missing 'title' in project data."}), 400
        
    proj = add_project(
        student_id=student_id,
        title=data["title"].strip(),
        description=data.get("description", ""),
        technologies=data.get("technologies", ""),
        project_url=data.get("project_url", "")
    )
    return jsonify({"success": True, "message": "Project added successfully.", "project": proj}), 201

@student_bp.route("/students/projects/<int:project_id>", methods=["DELETE"])
def remove_project(project_id):
    """DELETE /api/students/projects/<project_id> - Delete project."""
    success = delete_project(project_id)
    if not success:
        return jsonify({"success": False, "error": "Project not found."}), 404
    return jsonify({"success": True, "message": "Project deleted successfully."}), 200

@student_bp.route("/skills", methods=["GET"])
def list_all_skills():
    """GET /api/skills - List all catalog skills."""
    skills = get_all_skills()
    return jsonify({"success": True, "skills": skills}), 200
