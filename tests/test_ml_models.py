"""
Unit Tests for Machine Learning Models, Tuning, Persistence & Analytics
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
import sys
import unittest
import joblib
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_api.config import Config
from association.apriori_analysis import run_apriori_analysis
from association.fpgrowth_analysis import run_fpgrowth_analysis, compare_apriori_and_fpgrowth
from rl_demo.q_learning_optimizer import run_rl_simulation
from recommendation.skill_gap import analyze_skill_gap
from recommendation.job_matcher import compute_job_match

class TestMLPipelines(unittest.TestCase):

    def test_01_career_model_persistence_and_inference(self):
        self.assertTrue(os.path.exists(Config.CAREER_MODEL_PATH), "Career model file missing.")
        payload = joblib.load(Config.CAREER_MODEL_PATH)
        self.assertIn("model", payload)
        self.assertIn("preprocessor", payload)
        self.assertIn("label_encoder", payload)
        
        model = payload["model"]
        preprocessor = payload["preprocessor"]
        label_encoder = payload["label_encoder"]
        
        sample_input = pd.DataFrame([{
            "cgpa": 8.5, "python": 1, "java": 0, "cpp": 0, "sql": 1,
            "machine_learning": 1, "deep_learning": 1, "data_visualization": 1,
            "web_development": 0, "cloud": 1, "projects_count": 4,
            "internship": 1, "certifications_count": 3
        }])
        
        proc_input = preprocessor.transform(sample_input)
        pred_encoded = model.predict(proc_input)[0]
        predicted_role = label_encoder.inverse_transform([pred_encoded])[0]
        
        self.assertIsInstance(predicted_role, str)
        self.assertIn(predicted_role, label_encoder.classes_)

    def test_02_academic_risk_model_persistence_and_inference(self):
        self.assertTrue(os.path.exists(Config.ACADEMIC_MODEL_PATH), "Academic risk model file missing.")
        payload = joblib.load(Config.ACADEMIC_MODEL_PATH)
        
        model = payload["model"]
        preprocessor = payload["preprocessor"]
        label_encoder = payload["label_encoder"]
        
        sample_input = pd.DataFrame([{
            "previous_marks": 85.0, "attendance": 90.0, "study_hours": 6.0,
            "assignment_completion": 95.0, "internal_marks": 27.0,
            "failed_subjects": 0, "cgpa": 8.8
        }])
        
        proc_input = preprocessor.transform(sample_input)
        pred_encoded = model.predict(proc_input)[0]
        risk_level = label_encoder.inverse_transform([pred_encoded])[0]
        
        self.assertIn(risk_level, ["Low Risk", "Medium Risk", "High Risk"])

    def test_03_association_mining(self):
        apriori_res = run_apriori_analysis(min_support=0.08, min_confidence=0.3)
        self.assertEqual(apriori_res["algorithm"], "Apriori")
        self.assertGreater(apriori_res["frequent_itemsets_count"], 0)
        
        fpgrowth_res = run_fpgrowth_analysis(min_support=0.08, min_confidence=0.3)
        self.assertEqual(fpgrowth_res["algorithm"], "FP-Growth")
        self.assertGreater(fpgrowth_res["frequent_itemsets_count"], 0)
        
        comp = compare_apriori_and_fpgrowth(min_support=0.08, min_confidence=0.3)
        self.assertIn("speedup_ratio", comp)

    def test_04_q_learning_reinforcement_learning(self):
        res = run_rl_simulation(episodes=150)
        self.assertIn("optimal_path", res)
        self.assertGreater(len(res["optimal_path"]), 0)

    def test_05_skill_gap_and_job_match(self):
        skills = ["Python", "Machine Learning", "Data Visualization"]
        gap = analyze_skill_gap(skills, "Machine Learning Engineer")
        self.assertIn("Python", gap["matching_skills"])
        self.assertIn("Docker", gap["missing_skills"])
        self.assertGreaterEqual(gap["match_percentage"], 0.0)

if __name__ == "__main__":
    unittest.main()
