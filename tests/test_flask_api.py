"""
Integration Tests for Flask REST API Endpoints
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import unittest
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_api.app import create_app

class TestFlaskAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("models_status", data)

    def test_02_predict_career_endpoint(self):
        payload = {
            "cgpa": 8.5,
            "python": 1,
            "java": 0,
            "cpp": 0,
            "sql": 1,
            "machine_learning": 1,
            "deep_learning": 1,
            "data_visualization": 1,
            "web_development": 0,
            "cloud": 1,
            "projects_count": 4,
            "internship": 1,
            "certifications_count": 2
        }
        response = self.client.post("/api/predict/career", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("predicted_career", data)
        self.assertIn("confidence", data)

    def test_03_predict_career_invalid_input(self):
        response = self.client.post("/api/predict/career", json={"cgpa": "invalid_number"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_04_predict_academic_risk_endpoint(self):
        payload = {
            "previous_marks": 82.0,
            "attendance": 88.0,
            "study_hours": 5.5,
            "assignment_completion": 90.0,
            "internal_marks": 25.0,
            "failed_subjects": 0,
            "cgpa": 8.2
        }
        response = self.client.post("/api/predict/academic-risk", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn(data["academic_risk"], ["Low Risk", "Medium Risk", "High Risk"])

    def test_05_student_and_job_crud_endpoints(self):
        # 1. Create Student
        st_data = {
            "name": "Integration Tester",
            "email": "integration.tester@univ.edu",
            "cgpa": 8.1
        }
        res_st = self.client.post("/api/students", json=st_data)
        self.assertIn(res_st.status_code, [201, 400]) # 400 if already exists
        
        # 2. Get Students
        res_list = self.client.get("/api/students")
        self.assertEqual(res_list.status_code, 200)
        
        # 3. Get Jobs
        res_jobs = self.client.get("/api/jobs")
        self.assertEqual(res_jobs.status_code, 200)

    def test_06_association_and_rl_endpoints(self):
        # Association benchmark
        res_assoc = self.client.get("/api/association/benchmark?min_support=0.08&min_confidence=0.3")
        self.assertEqual(res_assoc.status_code, 200)
        data_assoc = res_assoc.get_json()
        self.assertTrue(data_assoc["success"])
        self.assertIn("benchmark", data_assoc)
        
        # RL Path Optimizer
        res_rl = self.client.post("/api/rl/optimize-path", json={"episodes": 100})
        self.assertEqual(res_rl.status_code, 200)
        data_rl = res_rl.get_json()
        self.assertTrue(data_rl["success"])
        self.assertIn("simulation", data_rl)

if __name__ == "__main__":
    unittest.main()
