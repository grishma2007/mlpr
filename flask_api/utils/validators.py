"""
Input Validation and Error Formatting Utilities
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

def validate_career_input(data):
    """Validates incoming JSON payload for career prediction."""
    if not isinstance(data, dict):
        return False, "Input payload must be a JSON object."
    
    required_keys = ["cgpa"]
    for key in required_keys:
        if key not in data:
            return False, f"Missing required feature: '{key}'"
            
    try:
        cgpa = float(data["cgpa"])
        if cgpa < 0.0 or cgpa > 10.0:
            return False, "CGPA must be a valid numeric score between 0.0 and 10.0"
    except (ValueError, TypeError):
        return False, "CGPA must be a valid numeric float."
        
    return True, None

def validate_academic_input(data):
    """Validates incoming JSON payload for academic risk prediction."""
    if not isinstance(data, dict):
        return False, "Input payload must be a JSON object."
        
    required_numeric = ["attendance", "cgpa", "study_hours"]
    for k in required_numeric:
        if k not in data:
            return False, f"Missing required academic feature: '{k}'"
        try:
            val = float(data[k])
            if val < 0:
                return False, f"Feature '{k}' cannot be negative."
        except (ValueError, TypeError):
            return False, f"Feature '{k}' must be a valid number."
            
    attendance = float(data.get("attendance", 0))
    if attendance < 0.0 or attendance > 100.0:
        return False, "Attendance percentage must be between 0 and 100."
        
    return True, None

def validate_student_input(data):
    """Validates student profile registration and update."""
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object."
    if "name" not in data or not str(data["name"]).strip():
        return False, "Student name is required."
    if "email" not in data or "@" not in str(data["email"]):
        return False, "A valid email address is required."
    return True, None

def validate_job_input(data):
    """Validates recruiter job posting data."""
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object."
    if "title" not in data or not str(data["title"]).strip():
        return False, "Job title is required."
    if "required_skills" not in data or not str(data["required_skills"]).strip():
        return False, "Required skills must be specified."
    return True, None
