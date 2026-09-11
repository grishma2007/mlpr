"""
Comprehensive Model Evaluation & Metrics Persistence
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.train_career_model import train_and_compare_career_models
from ml.train_academic_model import train_and_compare_academic_models

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

def evaluate_all_and_save_metrics():
    print("=========================================================")
    print("  RUNNING FULL MACHINE LEARNING EVALUATION WORKFLOW")
    print("=========================================================")
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    career_metrics = train_and_compare_career_models()
    academic_metrics = train_and_compare_academic_models()
    
    all_metrics = {
        "career_prediction": career_metrics,
        "academic_risk": academic_metrics,
        "metadata": {
            "evaluation_engine": "Scikit-Learn 1.7+",
            "tuning_method": "GridSearchCV with 5-Fold Cross Validation",
            "ensemble_algorithm": "Random Forest Classifier (Bagging + Feature Subsampling)",
            "status": "Production Ready"
        }
    }
    
    with open(METRICS_PATH, "w") as f:
        json.dump(all_metrics, f, indent=4)
        
    print(f"\nSuccessfully evaluated all models and saved metrics to: {METRICS_PATH}")
    return all_metrics

if __name__ == "__main__":
    evaluate_all_and_save_metrics()
