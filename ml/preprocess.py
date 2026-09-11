"""
Data Preprocessing and Pipeline Utilities
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

CAREER_DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "career_dataset.csv")
ACADEMIC_DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "academic_dataset.csv")

CAREER_NUMERIC_FEATURES = ["cgpa", "projects_count", "certifications_count"]
CAREER_BINARY_FEATURES = [
    "python", "java", "cpp", "sql", "machine_learning", 
    "deep_learning", "data_visualization", "web_development", "cloud", "internship"
]
CAREER_ALL_FEATURES = [
    "cgpa", "python", "java", "cpp", "sql", "machine_learning",
    "deep_learning", "data_visualization", "web_development", "cloud",
    "projects_count", "internship", "certifications_count"
]

ACADEMIC_NUMERIC_FEATURES = [
    "previous_marks", "attendance", "study_hours", 
    "assignment_completion", "internal_marks", "failed_subjects", "cgpa"
]

def load_career_data(filepath=CAREER_DATASET_PATH):
    """Load and validate raw career dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Career dataset not found at {filepath}. Run scripts/create_dataset.py first.")
    df = pd.read_csv(filepath)
    # Check for missing values
    df = df.dropna().reset_index(drop=True)
    return df

def load_academic_data(filepath=ACADEMIC_DATASET_PATH):
    """Load and validate raw academic risk dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Academic dataset not found at {filepath}. Run scripts/create_dataset.py first.")
    df = pd.read_csv(filepath)
    df = df.dropna().reset_index(drop=True)
    return df

def get_career_preprocessor():
    """Build preprocessor transformer for career features."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), CAREER_NUMERIC_FEATURES),
            ("bin", "passthrough", CAREER_BINARY_FEATURES)
        ],
        remainder="drop"
    )
    return preprocessor

def get_academic_preprocessor():
    """Build preprocessor transformer for academic features."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ACADEMIC_NUMERIC_FEATURES)
        ],
        remainder="drop"
    )
    return preprocessor

def prepare_career_train_test(test_size=0.2, random_state=42):
    """Prepare train/test sets for career role prediction."""
    df = load_career_data()
    X = df[CAREER_ALL_FEATURES]
    y = df["career_role"]
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
    )
    return X_train, X_test, y_train, y_test, label_encoder

def prepare_academic_train_test(test_size=0.2, random_state=42):
    """Prepare train/test sets for academic risk prediction."""
    df = load_academic_data()
    X = df[ACADEMIC_NUMERIC_FEATURES]
    y = df["risk_level"]
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
    )
    return X_train, X_test, y_train, y_test, label_encoder
