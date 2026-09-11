"""
Model Cache & Loader Singleton
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import joblib
from flask_api.config import Config

class ModelManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance.career_model_payload = None
            cls._instance.academic_model_payload = None
            cls._instance.load_models()
        return cls._instance

    def load_models(self):
        """Loads trained Joblib models into memory on server boot."""
        if os.path.exists(Config.CAREER_MODEL_PATH):
            try:
                self.career_model_payload = joblib.load(Config.CAREER_MODEL_PATH)
                print(f"[ModelManager] Loaded Career Model from: {Config.CAREER_MODEL_PATH}")
            except Exception as e:
                print(f"[ModelManager Error] Failed to load Career Model: {e}")
        else:
            print(f"[ModelManager Warning] Career Model not found at: {Config.CAREER_MODEL_PATH}")

        if os.path.exists(Config.ACADEMIC_MODEL_PATH):
            try:
                self.academic_model_payload = joblib.load(Config.ACADEMIC_MODEL_PATH)
                print(f"[ModelManager] Loaded Academic Risk Model from: {Config.ACADEMIC_MODEL_PATH}")
            except Exception as e:
                print(f"[ModelManager Error] Failed to load Academic Risk Model: {e}")
        else:
            print(f"[ModelManager Warning] Academic Risk Model not found at: {Config.ACADEMIC_MODEL_PATH}")

    def get_career_model(self):
        if not self.career_model_payload:
            self.load_models()
        return self.career_model_payload

    def get_academic_model(self):
        if not self.academic_model_payload:
            self.load_models()
        return self.academic_model_payload

model_manager = ModelManager()
