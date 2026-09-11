"""
Academic Risk Prediction REST API Blueprint
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import pandas as pd
from flask import Blueprint, request, jsonify
from flask_api.utils.model_loader import model_manager
from flask_api.utils.validators import validate_academic_input

academic_bp = Blueprint("academic_bp", __name__)

@academic_bp.route("/predict/academic-risk", methods=["POST"])
def predict_academic_risk():
    """
    POST /api/predict/academic-risk
    Predicts student academic performance risk level: Low Risk, Medium Risk, High Risk.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid or missing JSON payload in request."}), 400
        
    is_valid, err_msg = validate_academic_input(data)
    if not is_valid:
        return jsonify({"success": False, "error": err_msg}), 400
        
    model_payload = model_manager.get_academic_model()
    if not model_payload:
        return jsonify({"success": False, "error": "Academic risk prediction model is not available. Please run ml/train_academic_model.py"}), 500
        
    try:
        model = model_payload["model"]
        preprocessor = model_payload["preprocessor"]
        label_encoder = model_payload["label_encoder"]
        
        features_dict = {
            "previous_marks": [float(data.get("previous_marks", 75.0))],
            "attendance": [float(data.get("attendance", 80.0))],
            "study_hours": [float(data.get("study_hours", 4.0))],
            "assignment_completion": [float(data.get("assignment_completion", 85.0))],
            "internal_marks": [float(data.get("internal_marks", 22.0))],
            "failed_subjects": [int(data.get("failed_subjects", 0))],
            "cgpa": [float(data.get("cgpa", 7.5))]
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
                
        # Actionable recommendations based on predicted risk level
        recommendations = []
        if predicted_risk == "High Risk":
            recommendations.append("Immediate academic counseling and remedial tutorial sessions recommended.")
            recommendations.append("Increase daily study hours to at least 4-5 hours.")
            recommendations.append("Mandatory attendance tracking to ensure attendance above 75%.")
        elif predicted_risk == "Medium Risk":
            recommendations.append("Focus on improving internal marks and assignment submission punctuality.")
            recommendations.append("Target clearing any backlog subjects early in the semester.")
            recommendations.append("Participate in peer study groups.")
        else:
            recommendations.append("Outstanding academic performance! Maintain current study habits.")
            recommendations.append("Encouraged to take advanced industry certifications and research projects.")
            
        return jsonify({
            "success": True,
            "academic_risk": predicted_risk,
            "confidence": confidence,
            "risk_probabilities": risk_breakdown,
            "recommendations": recommendations,
            "model_used": type(model).__name__,
            "inputs_received": {k: v[0] for k, v in features_dict.items()}
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Academic prediction failed: {str(e)}"}), 500
