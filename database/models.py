"""
SQLAlchemy ORM Database Models
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    college = Column(String(150), default="")
    degree = Column(String(100), default="B.Tech")
    branch = Column(String(100), default="Computer Science")
    semester = Column(Integer, default=6)
    cgpa = Column(Float, default=8.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="student", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="student", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "college": self.college,
            "degree": self.degree,
            "branch": self.branch,
            "semester": self.semester,
            "cgpa": self.cgpa,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "skills": [s.to_dict() for s in self.skills] if self.skills else [],
            "projects": [p.to_dict() for p in self.projects] if self.projects else []
        }

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), default="General")

    def to_dict(self):
        return {
            "id": self.id,
            "skill_name": self.skill_name,
            "category": self.category
        }

class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.skill_name if self.skill else "",
            "category": self.skill.category if self.skill else "",
            "proficiency": self.proficiency
        }

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    technologies = Column(String(255), default="")
    project_url = Column(String(255), default="")

    student = relationship("Student", back_populates="projects")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "title": self.title,
            "description": self.description,
            "technologies": self.technologies,
            "project_url": self.project_url
        }

class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    company = Column(String(150), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    industry = Column(String(100), default="Technology")
    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="recruiter", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "industry": self.industry,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recruiter_id = Column(Integer, ForeignKey("recruiters.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(String(255), nullable=False)  # comma-separated list
    minimum_cgpa = Column(Float, default=6.0)
    location = Column(String(100), default="Remote")
    job_type = Column(String(50), default="Full-time")  # Full-time, Internship, Contract
    created_at = Column(DateTime, default=datetime.utcnow)

    recruiter = relationship("Recruiter", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "recruiter_id": self.recruiter_id,
            "recruiter_name": self.recruiter.name if self.recruiter else "",
            "company": self.recruiter.company if self.recruiter else "",
            "title": self.title,
            "description": self.description,
            "required_skills": self.required_skills,
            "minimum_cgpa": self.minimum_cgpa,
            "location": self.location,
            "job_type": self.job_type,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, default=0.0)
    status = Column(String(50), default="Applied")  # Applied, Shortlisted, Interview, Rejected, Accepted
    applied_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="applications")
    job = relationship("Job", back_populates="applications")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student.name if self.student else "",
            "student_email": self.student.email if self.student else "",
            "student_cgpa": self.student.cgpa if self.student else 0.0,
            "job_id": self.job_id,
            "job_title": self.job.title if self.job else "",
            "company": self.job.recruiter.company if self.job and self.job.recruiter else "",
            "match_score": self.match_score,
            "status": self.status,
            "applied_at": self.applied_at.strftime("%Y-%m-%d %H:%M:%S") if self.applied_at else None
        }
