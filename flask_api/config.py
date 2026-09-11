"""
Flask API Configuration
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "academic-ai-platform-secret-key-503")
    CAREER_MODEL_PATH = os.path.join(MODELS_DIR, "career_model.joblib")
    CAREER_PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "career_preprocessor.joblib")
    ACADEMIC_MODEL_PATH = os.path.join(MODELS_DIR, "academic_risk_model.joblib")
    ACADEMIC_PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "academic_preprocessor.joblib")
    METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "career_platform.db")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB Max Upload
