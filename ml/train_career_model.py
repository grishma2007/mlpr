"""
Career Role Prediction Model Training and Evaluation Pipeline
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.preprocess import prepare_career_train_test, get_career_preprocessor
from ml.tune_models import tune_random_forest

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

def train_and_compare_career_models():
    print("=========================================================")
    print("  1. TRAINING & COMPARING CAREER PREDICTION MODELS")
    print("=========================================================")
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # 1. Load and Split Data
    X_train, X_test, y_train, y_test, label_encoder = prepare_career_train_test()
    print(f"Dataset Split: {len(X_train)} Train Samples, {len(X_test)} Test Samples")
    print(f"Target Classes ({len(label_encoder.classes_)}): {list(label_encoder.classes_)}")
    
    # 2. Fit Preprocessor
    preprocessor = get_career_preprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    # 3. Initialize 4 Candidate Classification Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Support Vector Machine": SVC(kernel="rbf", probability=True, random_state=42),
        "Random Forest (Ensemble)": RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    print("\n--- Model Benchmark & Comparison ---")
    for name, clf in models.items():
        clf.fit(X_train_proc, y_train)
        y_pred = clf.predict(X_test_proc)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        
        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "model_obj": clf
        }
        print(f"[{name}] -> Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1-Score: {f1:.4f}")
        
    # 4. Hyperparameter Tuning on Best Model (Random Forest Ensemble)
    print("\n--- Hyperparameter Tuning on Random Forest (GridSearchCV) ---")
    rf_untuned = models["Random Forest (Ensemble)"]
    untuned_acc = results["Random Forest (Ensemble)"]["accuracy"]
    
    best_rf, best_params, best_cv_score = tune_random_forest(X_train_proc, y_train)
    y_pred_tuned = best_rf.predict(X_test_proc)
    tuned_acc = accuracy_score(y_test, y_pred_tuned)
    tuned_f1 = f1_score(y_test, y_pred_tuned, average="weighted", zero_division=0)
    tuned_prec = precision_score(y_test, y_pred_tuned, average="weighted", zero_division=0)
    tuned_rec = recall_score(y_test, y_pred_tuned, average="weighted", zero_division=0)
    
    print(f"Best Hyperparameters: {best_params}")
    print(f"Accuracy Before Tuning: {untuned_acc:.4f} | Accuracy After Tuning: {tuned_acc:.4f}")
    
    # 5. Confusion Matrix & Detailed Report
    cm = confusion_matrix(y_test, y_pred_tuned).tolist()
    cr = classification_report(y_test, y_pred_tuned, target_names=label_encoder.classes_, output_dict=True, zero_division=0)
    
    # 6. Save Model, Preprocessor and Label Encoder
    model_payload = {
        "model": best_rf,
        "preprocessor": preprocessor,
        "label_encoder": label_encoder,
        "features": list(X_train.columns),
        "target_classes": list(label_encoder.classes_)
    }
    
    model_path = os.path.join(MODELS_DIR, "career_model.joblib")
    preprocessor_path = os.path.join(MODELS_DIR, "career_preprocessor.joblib")
    
    joblib.dump(model_payload, model_path)
    joblib.dump(preprocessor, preprocessor_path)
    print(f"\nSaved Best Model to: {model_path}")
    print(f"Saved Preprocessor to: {preprocessor_path}")
    
    # Return structured metrics dictionary for evaluation persistence
    career_metrics = {
        "comparison": {
            k: {
                "accuracy": v["accuracy"],
                "precision": v["precision"],
                "recall": v["recall"],
                "f1_score": v["f1_score"]
            } for k, v in results.items()
        },
        "tuning": {
            "model": "Random Forest Classifier",
            "best_parameters": best_params,
            "accuracy_before": round(float(untuned_acc), 4),
            "accuracy_after": round(float(tuned_acc), 4),
            "f1_after": round(float(tuned_f1), 4),
            "precision_after": round(float(tuned_prec), 4),
            "recall_after": round(float(tuned_rec), 4)
        },
        "confusion_matrix": cm,
        "classes": list(label_encoder.classes_),
        "classification_report": cr
    }
    
    return career_metrics

if __name__ == "__main__":
    train_and_compare_career_models()
