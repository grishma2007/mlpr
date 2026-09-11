"""
Unit Tests for Database Models and CRUD Operations
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import (
    init_db,
    create_student,
    get_student_by_id,
    update_student,
    delete_student,
    add_student_skill,
    remove_student_skill,
    create_job,
    get_job_by_id,
    create_application,
    get_applications_by_student
)

class TestDatabaseCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_01_create_and_read_student(self):
        email = "test.student@univ.edu"
        # Cleanup if exists
        from database.database import get_student_by_email
        existing = get_student_by_email(email)
        if existing:
            delete_student(existing["id"])
            
        student = create_student(
            name="Test Student",
            email=email,
            college="Test Engineering College",
            degree="B.Tech",
            branch="Data Science",
            semester=5,
            cgpa=8.8
        )
        self.assertIsNotNone(student)
        self.assertEqual(student["name"], "Test Student")
        self.assertEqual(student["cgpa"], 8.8)
        
        fetched = get_student_by_id(student["id"])
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["email"], email)

    def test_02_update_and_delete_student(self):
        email = "update.test@univ.edu"
        student = create_student(name="Before Update", email=email, cgpa=7.0)
        
        updated = update_student(student["id"], {"name": "After Update", "cgpa": 9.1})
        self.assertEqual(updated["name"], "After Update")
        self.assertEqual(updated["cgpa"], 9.1)
        
        # Test add skill
        skill_rec = add_student_skill(student["id"], "Python", proficiency="Advanced")
        self.assertIsNotNone(skill_rec)
        
        deleted = delete_student(student["id"])
        self.assertTrue(deleted)
        self.assertIsNone(get_student_by_id(student["id"]))

    def test_03_job_and_application_crud(self):
        job = create_job(
            recruiter_id=1,
            title="Unit Test AI Engineer",
            description="Testing job description",
            required_skills="Python, PyTorch",
            minimum_cgpa=7.5
        )
        self.assertIsNotNone(job)
        self.assertEqual(job["title"], "Unit Test AI Engineer")
        
        # Create student and apply
        st = create_student(name="Applicant Test", email="applicant.test@univ.edu", cgpa=8.0)
        app = create_application(student_id=st["id"], job_id=job["id"], match_score=92.0)
        self.assertIsNotNone(app)
        self.assertEqual(app["match_score"], 92.0)
        
        student_apps = get_applications_by_student(st["id"])
        self.assertGreaterEqual(len(student_apps), 1)
        
        # Cleanup
        delete_student(st["id"])

if __name__ == "__main__":
    unittest.main()
