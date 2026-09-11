"""
HTTP REST API Client for Streamlit to Flask Communication (with Robust Fallback)
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import requests
import json
import os
import sys

FLASK_API_BASE_URL = "http://127.0.0.1:5000/api"

# Helper for friendly connection error messages
def _handle_connection_error(e):
    return 503, {
        "success": False,
        "error": "Flask Backend (http://127.0.0.1:5000) is offline. Please ensure 'python flask_api/app.py' is running in a terminal."
    }

def check_backend_health():
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/health", timeout=2)
        if resp.status_code == 200:
            return True, resp.json()
        return False, {"error": f"Status Code: {resp.status_code}"}
    except Exception as e:
        return False, {"error": "Flask Backend is not running."}

# =========================================================================
# Prediction APIs
# =========================================================================

def predict_career_api(payload):
    try:
        resp = requests.post(f"{FLASK_API_BASE_URL}/predict/career", json=payload, timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError as e:
        # Fallback to direct model loader if Flask is offline
        try:
            from flask_api.utils.model_loader import model_manager
            import pandas as pd
            model_payload = model_manager.get_career_model()
            if model_payload:
                model = model_payload["model"]
                preprocessor = model_payload["preprocessor"]
                label_encoder = model_payload["label_encoder"]
                
                features_dict = {k: [payload.get(k, 0)] for k in [
                    "cgpa", "python", "java", "cpp", "sql", "machine_learning",
                    "deep_learning", "data_visualization", "web_development", "cloud",
                    "projects_count", "internship", "certifications_count"
                ]}
                input_df = pd.DataFrame(features_dict)
                input_proc = preprocessor.transform(input_df)
                pred_encoded = model.predict(input_proc)[0]
                predicted_role = label_encoder.inverse_transform([pred_encoded])[0]
                confidence = 0.85
                top_roles = [{"role": predicted_role, "probability": 1.0}]
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_proc)[0]
                    confidence = round(float(proba[pred_encoded]), 4)
                    top_indices = proba.argsort()[-3:][::-1]
                    top_roles = [{"role": label_encoder.inverse_transform([idx])[0], "probability": round(float(proba[idx]), 4)} for idx in top_indices]
                return 200, {
                    "success": True,
                    "predicted_career": predicted_role,
                    "confidence": confidence,
                    "top_career_roles": top_roles,
                    "model_used": type(model).__name__ + " (Local Fallback)",
                    "note": "Processed via Local Model Engine"
                }
        except Exception:
            pass
        return _handle_connection_error(e)
    except Exception as e:
        return 500, {"success": False, "error": str(e)}

def predict_academic_risk_api(payload):
    try:
        resp = requests.post(f"{FLASK_API_BASE_URL}/predict/academic-risk", json=payload, timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError as e:
        try:
            from flask_api.utils.model_loader import model_manager
            import pandas as pd
            model_payload = model_manager.get_academic_model()
            if model_payload:
                model = model_payload["model"]
                preprocessor = model_payload["preprocessor"]
                label_encoder = model_payload["label_encoder"]
                
                features_dict = {
                    "previous_marks": [float(payload.get("previous_marks", 75.0))],
                    "attendance": [float(payload.get("attendance", 80.0))],
                    "study_hours": [float(payload.get("study_hours", 4.0))],
                    "assignment_completion": [float(payload.get("assignment_completion", 85.0))],
                    "internal_marks": [float(payload.get("internal_marks", 22.0))],
                    "failed_subjects": [int(payload.get("failed_subjects", 0))],
                    "cgpa": [float(payload.get("cgpa", 7.5))]
                }
                input_df = pd.DataFrame(features_dict)
                input_proc = preprocessor.transform(input_df)
                pred_encoded = model.predict(input_proc)[0]
                predicted_risk = label_encoder.inverse_transform([pred_encoded])[0]
                confidence = 0.90
                risk_breakdown = {}
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_proc)[0]
                    confidence = round(float(proba[pred_encoded]), 4)
                    for idx, cls_name in enumerate(label_encoder.classes_):
                        risk_breakdown[cls_name] = round(float(proba[idx]), 4)
                        
                recs = ["Maintain consistent study habits."]
                if predicted_risk == "High Risk":
                    recs = ["Attend tutorial remedial classes.", "Target >75% attendance."]
                elif predicted_risk == "Medium Risk":
                    recs = ["Focus on assignment submission deadlines.", "Clear backlogs."]
                return 200, {
                    "success": True,
                    "academic_risk": predicted_risk,
                    "confidence": confidence,
                    "risk_probabilities": risk_breakdown,
                    "recommendations": recs,
                    "model_used": type(model).__name__ + " (Local Fallback)"
                }
        except Exception:
            pass
        return _handle_connection_error(e)
    except Exception as e:
        return 500, {"success": False, "error": str(e)}

# =========================================================================
# Resume & Recommendation APIs
# =========================================================================

def analyze_resume_api(file_obj=None, raw_text=None):
    try:
        if file_obj:
            filename = getattr(file_obj, "name", "resume.pdf")
            if hasattr(file_obj, "getvalue"):
                file_bytes = file_obj.getvalue()
            elif hasattr(file_obj, "read"):
                file_bytes = file_obj.read()
                if hasattr(file_obj, "seek"):
                    file_obj.seek(0)
            else:
                file_bytes = file_obj
            files = {"file": (filename, file_bytes, "application/pdf")}
            resp = requests.post(f"{FLASK_API_BASE_URL}/resume/analyze", files=files, timeout=10)
        else:
            resp = requests.post(f"{FLASK_API_BASE_URL}/resume/analyze", json={"text": raw_text}, timeout=10)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError as e:
        try:
            from nlp.resume_parser import parse_resume
            if file_obj:
                parsed = parse_resume(file_obj)
            else:
                parsed = parse_resume(raw_text)
            return 200, {"success": True, "parsed_resume": parsed}
        except Exception:
            pass
        return _handle_connection_error(e)
    except Exception as e:
        return 500, {"success": False, "error": str(e)}

def get_skill_gap_api(skills, target_role):
    try:
        resp = requests.post(
            f"{FLASK_API_BASE_URL}/skills/gap",
            json={"skills": skills, "target_role": target_role},
            timeout=5
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError as e:
        try:
            from recommendation.skill_gap import analyze_skill_gap
            gap = analyze_skill_gap(skills, target_role)
            return 200, {"success": True, "gap_analysis": gap}
        except Exception:
            pass
        return _handle_connection_error(e)
    except Exception as e:
        return 500, {"success": False, "error": str(e)}

def get_learning_recommendations_api(missing_skills):
    try:
        resp = requests.post(
            f"{FLASK_API_BASE_URL}/recommendations/learning",
            json={"missing_skills": missing_skills},
            timeout=5
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError as e:
        try:
            from recommendation.learning_recommender import recommend_learning_resources
            courses = recommend_learning_resources(missing_skills)
            return 200, {"success": True, "recommended_courses": courses}
        except Exception:
            pass
        return _handle_connection_error(e)
    except Exception as e:
        return 500, {"success": False, "error": str(e)}

# =========================================================================
# Student Profile CRUD APIs (with Database Fallback)
# =========================================================================

def get_all_students_api():
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/students", timeout=3)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import get_all_students
            students = get_all_students()
            return 200, {"success": True, "students": students}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex), "students": []}

def get_student_api(student_id):
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/students/{student_id}", timeout=3)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import get_student_by_id
            st = get_student_by_id(student_id)
            if st:
                return 200, {"success": True, "student": st}
            return 404, {"success": False, "error": "Student not found"}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def create_student_api(data):
    try:
        resp = requests.post(f"{FLASK_API_BASE_URL}/students", json=data, timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        # Fallback direct to SQLite database
        try:
            from database.database import create_student
            st = create_student(
                name=data["name"].strip(),
                email=data["email"].strip(),
                college=data.get("college", ""),
                degree=data.get("degree", "B.Tech"),
                branch=data.get("branch", "Computer Science"),
                semester=int(data.get("semester", 6)),
                cgpa=float(data.get("cgpa", 8.0))
            )
            return 201, {"success": True, "message": "Student created (via Local DB)", "student": st}
        except Exception as ex:
            return 400, {"success": False, "error": str(ex)}

def update_student_api(student_id, data):
    try:
        resp = requests.put(f"{FLASK_API_BASE_URL}/students/{student_id}", json=data, timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import update_student
            st = update_student(student_id, data)
            if st:
                return 200, {"success": True, "message": "Student updated (Local DB)", "student": st}
            return 404, {"success": False, "error": "Student not found"}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def delete_student_api(student_id):
    try:
        resp = requests.delete(f"{FLASK_API_BASE_URL}/students/{student_id}", timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import delete_student
            res = delete_student(student_id)
            return 200, {"success": res}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def add_student_skill_api(student_id, skill_name, proficiency="Intermediate"):
    try:
        resp = requests.post(
            f"{FLASK_API_BASE_URL}/students/{student_id}/skills",
            json={"skill_name": skill_name, "proficiency": proficiency},
            timeout=5
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import add_student_skill
            sk = add_student_skill(student_id, skill_name, proficiency=proficiency)
            return 201, {"success": True, "skill": sk}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def delete_student_skill_api(student_id, skill_id):
    try:
        resp = requests.delete(f"{FLASK_API_BASE_URL}/students/{student_id}/skills/{skill_id}", timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import remove_student_skill
            res = remove_student_skill(student_id, skill_id)
            return 200, {"success": res}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def add_student_project_api(student_id, project_data):
    try:
        resp = requests.post(
            f"{FLASK_API_BASE_URL}/students/{student_id}/projects",
            json=project_data,
            timeout=5
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import add_project
            p = add_project(
                student_id=student_id,
                title=project_data.get("title", ""),
                description=project_data.get("description", ""),
                technologies=project_data.get("technologies", ""),
                project_url=project_data.get("project_url", "")
            )
            return 201, {"success": True, "project": p}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def delete_student_project_api(project_id):
    try:
        resp = requests.delete(f"{FLASK_API_BASE_URL}/students/projects/{project_id}", timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import delete_project
            res = delete_project(project_id)
            return 200, {"success": res}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

# =========================================================================
# Jobs & Applications APIs
# =========================================================================

def get_all_jobs_api():
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/jobs", timeout=3)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import get_all_jobs
            jobs = get_all_jobs()
            return 200, {"success": True, "jobs": jobs}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex), "jobs": []}

def get_job_api(job_id):
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/jobs/{job_id}", timeout=3)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import get_job_by_id
            job = get_job_by_id(job_id)
            return 200, {"success": True, "job": job}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def create_job_api(job_data):
    try:
        resp = requests.post(f"{FLASK_API_BASE_URL}/jobs", json=job_data, timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import create_job
            job = create_job(
                recruiter_id=job_data.get("recruiter_id", 1),
                title=job_data["title"],
                description=job_data.get("description", ""),
                required_skills=job_data.get("required_skills", ""),
                minimum_cgpa=float(job_data.get("minimum_cgpa", 6.0)),
                location=job_data.get("location", "Remote"),
                job_type=job_data.get("job_type", "Full-time")
            )
            return 201, {"success": True, "job": job}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def update_job_api(job_id, job_data):
    try:
        resp = requests.put(f"{FLASK_API_BASE_URL}/jobs/{job_id}", json=job_data, timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import update_job
            job = update_job(job_id, job_data)
            return 200, {"success": True, "job": job}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def delete_job_api(job_id):
    try:
        resp = requests.delete(f"{FLASK_API_BASE_URL}/jobs/{job_id}", timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import delete_job
            res = delete_job(job_id)
            return 200, {"success": res}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def match_job_api(student_profile, job_data):
    try:
        resp = requests.post(
            f"{FLASK_API_BASE_URL}/jobs/match",
            json={"student": student_profile, "job": job_data},
            timeout=5
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from recommendation.job_matcher import compute_job_match
            match_res = compute_job_match(student_profile, job_data)
            return 200, {"success": True, "match_result": match_res}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def rank_candidates_api(job_id):
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/jobs/{job_id}/rank-candidates", timeout=8)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import get_job_by_id, get_all_students
            from ranking.candidate_ranker import rank_candidates_for_job
            job = get_job_by_id(job_id)
            candidates = get_all_students()
            rankings = rank_candidates_for_job(job, candidates)
            return 200, {"success": True, "job": job, "rankings": rankings}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def get_all_applications_api():
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/applications", timeout=3)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import get_all_applications
            apps = get_all_applications()
            return 200, {"success": True, "applications": apps}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex), "applications": []}

def get_student_applications_api(student_id):
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/applications/student/{student_id}", timeout=3)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import get_applications_by_student
            apps = get_applications_by_student(student_id)
            return 200, {"success": True, "applications": apps}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex), "applications": []}

def apply_for_job_api(student_id, job_id, match_score=0.0):
    try:
        resp = requests.post(
            f"{FLASK_API_BASE_URL}/applications",
            json={"student_id": student_id, "job_id": job_id, "match_score": match_score},
            timeout=5
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import create_application
            app = create_application(student_id, job_id, match_score=match_score)
            return 201, {"success": True, "application": app}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def update_application_status_api(app_id, status):
    try:
        resp = requests.put(
            f"{FLASK_API_BASE_URL}/applications/{app_id}",
            json={"status": status},
            timeout=5
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from database.database import update_application_status
            app = update_application_status(app_id, status)
            return 200, {"success": True, "application": app}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

# =========================================================================
# Metrics & Analytics APIs
# =========================================================================

def get_metrics_api():
    try:
        resp = requests.get(f"{FLASK_API_BASE_URL}/metrics", timeout=5)
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from flask_api.config import Config
            if os.path.exists(Config.METRICS_PATH):
                with open(Config.METRICS_PATH, "r") as f:
                    data = json.load(f)
                return 200, {"success": True, "metrics": data}
        except Exception:
            pass
        return 500, {"success": False, "error": "Metrics unavailable"}

def get_association_benchmark_api(min_support=0.05, min_confidence=0.3):
    try:
        resp = requests.get(
            f"{FLASK_API_BASE_URL}/association/benchmark?min_support={min_support}&min_confidence={min_confidence}",
            timeout=8
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from association.fpgrowth_analysis import compare_apriori_and_fpgrowth
            bench = compare_apriori_and_fpgrowth(min_support=min_support, min_confidence=min_confidence)
            return 200, {"success": True, "benchmark": bench}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}

def run_rl_optimizer_api(episodes=300, alpha=0.1, gamma=0.9):
    try:
        resp = requests.post(
            f"{FLASK_API_BASE_URL}/rl/optimize-path",
            json={"episodes": episodes, "learning_rate": alpha, "discount_factor": gamma},
            timeout=8
        )
        return resp.status_code, resp.json()
    except requests.exceptions.ConnectionError:
        try:
            from rl_demo.q_learning_optimizer import run_rl_simulation
            sim = run_rl_simulation(episodes=episodes, alpha=alpha, gamma=gamma)
            return 200, {"success": True, "simulation": sim}
        except Exception as ex:
            return 500, {"success": False, "error": str(ex)}
