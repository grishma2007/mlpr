"""
Main Flask REST API & Web Application Server
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import sys
import json
from flask import Flask, jsonify, render_template, request

# Add workspace root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_api.config import Config
from flask_api.utils.model_loader import model_manager
from database.database import init_db

# Import Blueprints
from flask_api.routes.career_routes import career_bp
from flask_api.routes.academic_routes import academic_bp
from flask_api.routes.resume_routes import resume_bp
from flask_api.routes.student_routes import student_bp
from flask_api.routes.job_routes import job_bp
from flask_api.routes.application_routes import application_bp
from flask_api.routes.association_routes import association_bp
from flask_api.routes.rl_routes import rl_bp

def create_app():
    # Configure template and static directories
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)

    # Initialize SQLite database on startup
    init_db()

    # Preload ML models
    model_manager.load_models()

    # Register Blueprints under /api prefix
    app.register_blueprint(career_bp, url_prefix="/api")
    app.register_blueprint(academic_bp, url_prefix="/api")
    app.register_blueprint(resume_bp, url_prefix="/api")
    app.register_blueprint(student_bp, url_prefix="/api")
    app.register_blueprint(job_bp, url_prefix="/api")
    app.register_blueprint(application_bp, url_prefix="/api")
    app.register_blueprint(association_bp, url_prefix="/api")
    app.register_blueprint(rl_bp, url_prefix="/api")

    # Global CORS support
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    # Root Web Frontend Endpoint
    @app.route("/", methods=["GET"])
    def root():
        # If client explicitly requests JSON
        if request.headers.get("Accept") == "application/json":
            return jsonify({
                "service": "AI-Powered Student Career & Recruitment Platform - REST API",
                "subject": "503 – Applied Artificial Intelligence: Model Development and Deployment",
                "status": "online"
            }), 200
        # Otherwise serve HTML/CSS Frontend
        return render_template("index.html")

    # Health Check API
    @app.route("/api/health", methods=["GET"])
    def health_check():
        career_ready = model_manager.career_model_payload is not None
        academic_ready = model_manager.academic_model_payload is not None
        return jsonify({
            "status": "healthy",
            "service": "AI Student Career & Recruitment Platform API",
            "subject": "503 – Applied Artificial Intelligence: Model Development and Deployment",
            "models_status": {
                "career_prediction_model": "loaded" if career_ready else "not_loaded",
                "academic_risk_model": "loaded" if academic_ready else "not_loaded"
            },
            "version": "1.0.0"
        }), 200

    # Model Evaluation Metrics API
    @app.route("/api/metrics", methods=["GET"])
    def get_metrics():
        if os.path.exists(Config.METRICS_PATH):
            with open(Config.METRICS_PATH, "r") as f:
                data = json.load(f)
            return jsonify({"success": True, "metrics": data}), 200
        return jsonify({"success": False, "error": "Metrics file not found. Run ml/evaluate_models.py"}), 404

    # Global HTTP Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": "Resource or endpoint not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": "HTTP method not allowed for this endpoint."}), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"success": False, "error": "Internal server error occurred."}), 500

    return app

app = create_app()

if __name__ == "__main__":
    print("==================================================================")
    print("  AI CAREER & RECRUITMENT PLATFORM RUNNING ON http://127.0.0.1:5000")
    print("  HTML/CSS Web Frontend: http://127.0.0.1:5000/")
    print("  Streamlit Web UI:     http://localhost:8501")
    print("  RESTful APIs:         http://127.0.0.1:5000/api/...")
    print("==================================================================")
    app.run(host="127.0.0.1", port=5000, debug=False)
