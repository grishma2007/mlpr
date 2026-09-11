"""
Career Prediction REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import pandas as pd
from flask import Blueprint, request, jsonify
from flask_api.utils.model_loader import model_manager
from flask_api.utils.validators import validate_career_input

career_bp = Blueprint("career_bp", __name__)

@career_bp.route("/predict/career", methods=["POST"])
def predict_career():
    """
    POST /api/predict/career
    Predicts suitable career role based on student academic scores and tech skills.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid or missing JSON payload in request."}), 400
        
    is_valid, err_msg = validate_career_input(data)
    if not is_valid:
        return jsonify({"success": False, "error": err_msg}), 400
        
    model_payload = model_manager.get_career_model()
    if not model_payload:
        return jsonify({"success": False, "error": "Career prediction model is not available. Please run ml/train_career_model.py"}), 500
        
    try:
        model = model_payload["model"]
        preprocessor = model_payload["preprocessor"]
        label_encoder = model_payload["label_encoder"]
        
        # Assemble feature vector
        features_dict = {
            "cgpa": [float(data.get("cgpa", 7.5))],
            "python": [int(data.get("python", 0))],
            "java": [int(data.get("java", 0))],
            "cpp": [int(data.get("cpp", 0))],
            "sql": [int(data.get("sql", 0))],
            "machine_learning": [int(data.get("machine_learning", 0))],
            "deep_learning": [int(data.get("deep_learning", 0))],
            "data_visualization": [int(data.get("data_visualization", 0))],
            "web_development": [int(data.get("web_development", 0))],
            "cloud": [int(data.get("cloud", 0))],
            "projects_count": [int(data.get("projects_count", 1))],
            "internship": [int(data.get("internship", 0))],
            "certifications_count": [int(data.get("certifications_count", 0))]
        }
        
        input_df = pd.DataFrame(features_dict)
        input_proc = preprocessor.transform(input_df)
        
        # Predict class and probabilities
        pred_encoded = model.predict(input_proc)[0]
        predicted_role = label_encoder.inverse_transform([pred_encoded])[0]
        
        confidence = 0.85
        top_roles = []
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_proc)[0]
            confidence = round(float(proba[pred_encoded]), 4)
            # Get top 3 predicted roles
            top_indices = proba.argsort()[-3:][::-1]
            for idx in top_indices:
                top_roles.append({
                    "role": label_encoder.inverse_transform([idx])[0],
                    "probability": round(float(proba[idx]), 4)
                })
        else:
            top_roles.append({"role": predicted_role, "probability": 1.0})
            
        return jsonify({
            "success": True,
            "predicted_career": predicted_role,
            "confidence": confidence,
            "top_career_roles": top_roles,
            "model_used": type(model).__name__,
            "inputs_received": {k: v[0] for k, v in features_dict.items()}
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Prediction failed: {str(e)}"}), 500
