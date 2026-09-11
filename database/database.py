"""
Database Session Management and CRUD Operations
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.models import Base, Student, Skill, StudentSkill, Project, Recruiter, Job, Application

# Default Database Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "career_platform.db")
DATABASE_URI = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False}, echo=False)
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
ScopedSession = scoped_session(SessionFactory)

def init_db():
    """Create all database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DB_PATH}")

@contextmanager
def get_db():
    """Context manager for thread-safe database session handling."""
    session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# ==========================================
# Student CRUD Operations
# ==========================================

def create_student(name, email, college="", degree="B.Tech", branch="Computer Science", semester=6, cgpa=8.0):
    with get_db() as db:
        existing = db.query(Student).filter(Student.email == email).first()
        if existing:
            raise ValueError(f"Student with email '{email}' already exists.")
        student = Student(
            name=name,
            email=email,
            college=college,
            degree=degree,
            branch=branch,
            semester=semester,
            cgpa=cgpa
        )
        db.add(student)
        db.flush()
        db.refresh(student)
        return student.to_dict()

def get_student_by_id(student_id):
    with get_db() as db:
        student = db.query(Student).filter(Student.id == student_id).first()
        return student.to_dict() if student else None

def get_student_by_email(email):
    with get_db() as db:
        student = db.query(Student).filter(Student.email == email).first()
        return student.to_dict() if student else None

def get_all_students():
    with get_db() as db:
        students = db.query(Student).order_by(Student.id.desc()).all()
        return [s.to_dict() for s in students]

def update_student(student_id, data):
    with get_db() as db:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None
        for key in ["name", "email", "college", "degree", "branch", "semester", "cgpa"]:
            if key in data and data[key] is not None:
                setattr(student, key, data[key])
        db.flush()
        db.refresh(student)
        return student.to_dict()

def delete_student(student_id):
    with get_db() as db:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return False
        db.delete(student)
        return True

# ==========================================
# Skills & StudentSkills CRUD Operations
# ==========================================

def get_or_create_skill(skill_name, category="General"):
    with get_db() as db:
        skill = db.query(Skill).filter(Skill.skill_name.ilike(skill_name.strip())).first()
        if not skill:
            skill = Skill(skill_name=skill_name.strip(), category=category)
            db.add(skill)
            db.flush()
            db.refresh(skill)
        return skill.to_dict()

def get_all_skills():
    with get_db() as db:
        skills = db.query(Skill).order_by(Skill.skill_name.asc()).all()
        return [s.to_dict() for s in skills]

def add_student_skill(student_id, skill_name, proficiency="Intermediate", category="General"):
    with get_db() as db:
        skill = db.query(Skill).filter(Skill.skill_name.ilike(skill_name.strip())).first()
        if not skill:
            skill = Skill(skill_name=skill_name.strip(), category=category)
            db.add(skill)
            db.flush()
        
        # Check if already added
        existing = db.query(StudentSkill).filter(
            StudentSkill.student_id == student_id,
            StudentSkill.skill_id == skill.id
        ).first()
        if existing:
            existing.proficiency = proficiency
            db.flush()
            return existing.to_dict()
        
        student_skill = StudentSkill(
            student_id=student_id,
            skill_id=skill.id,
            proficiency=proficiency
        )
        db.add(student_skill)
        db.flush()
        db.refresh(student_skill)
        return student_skill.to_dict()

def remove_student_skill(student_id, skill_id):
    with get_db() as db:
        rec = db.query(StudentSkill).filter(
            StudentSkill.student_id == student_id,
            StudentSkill.skill_id == skill_id
        ).first()
        if not rec:
            return False
        db.delete(rec)
        return True

# ==========================================
# Projects CRUD Operations
# ==========================================

def add_project(student_id, title, description="", technologies="", project_url=""):
    with get_db() as db:
        project = Project(
            student_id=student_id,
            title=title,
            description=description,
            technologies=technologies,
            project_url=project_url
        )
        db.add(project)
        db.flush()
        db.refresh(project)
        return project.to_dict()

def get_student_projects(student_id):
    with get_db() as db:
        projects = db.query(Project).filter(Project.student_id == student_id).all()
        return [p.to_dict() for p in projects]

def delete_project(project_id):
    with get_db() as db:
        p = db.query(Project).filter(Project.id == project_id).first()
        if not p:
            return False
        db.delete(p)
        return True

# ==========================================
# Recruiter CRUD Operations
# ==========================================

def create_recruiter(name, company, email, industry="Technology"):
    with get_db() as db:
        existing = db.query(Recruiter).filter(Recruiter.email == email).first()
        if existing:
            return existing.to_dict()
        recruiter = Recruiter(
            name=name,
            company=company,
            email=email,
            industry=industry
        )
        db.add(recruiter)
        db.flush()
        db.refresh(recruiter)
        return recruiter.to_dict()

def get_all_recruiters():
    with get_db() as db:
        recs = db.query(Recruiter).order_by(Recruiter.id.desc()).all()
        return [r.to_dict() for r in recs]

def get_recruiter_by_id(recruiter_id):
    with get_db() as db:
        rec = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
        return rec.to_dict() if rec else None

# ==========================================
# Job CRUD Operations
# ==========================================

def create_job(recruiter_id, title, description, required_skills, minimum_cgpa=6.0, location="Remote", job_type="Full-time"):
    with get_db() as db:
        job = Job(
            recruiter_id=recruiter_id,
            title=title,
            description=description,
            required_skills=required_skills,
            minimum_cgpa=minimum_cgpa,
            location=location,
            job_type=job_type
        )
        db.add(job)
        db.flush()
        db.refresh(job)
        return job.to_dict()

def get_all_jobs():
    with get_db() as db:
        jobs = db.query(Job).order_by(Job.id.desc()).all()
        return [j.to_dict() for j in jobs]

def get_job_by_id(job_id):
    with get_db() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        return job.to_dict() if job else None

def update_job(job_id, data):
    with get_db() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None
        for key in ["title", "description", "required_skills", "minimum_cgpa", "location", "job_type"]:
            if key in data and data[key] is not None:
                setattr(job, key, data[key])
        db.flush()
        db.refresh(job)
        return job.to_dict()

def delete_job(job_id):
    with get_db() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return False
        db.delete(job)
        return True

# ==========================================
# Application CRUD Operations
# ==========================================

def create_application(student_id, job_id, match_score=0.0):
    with get_db() as db:
        existing = db.query(Application).filter(
            Application.student_id == student_id,
            Application.job_id == job_id
        ).first()
        if existing:
            existing.match_score = match_score
            db.flush()
            return existing.to_dict()
        app = Application(
            student_id=student_id,
            job_id=job_id,
            match_score=match_score,
            status="Applied"
        )
        db.add(app)
        db.flush()
        db.refresh(app)
        return app.to_dict()

def get_all_applications():
    with get_db() as db:
        apps = db.query(Application).order_by(Application.applied_at.desc()).all()
        return [a.to_dict() for a in apps]

def get_applications_by_student(student_id):
    with get_db() as db:
        apps = db.query(Application).filter(Application.student_id == student_id).all()
        return [a.to_dict() for a in apps]

def get_applications_by_job(job_id):
    with get_db() as db:
        apps = db.query(Application).filter(Application.job_id == job_id).all()
        return [a.to_dict() for a in apps]

def update_application_status(app_id, status):
    with get_db() as db:
        app = db.query(Application).filter(Application.id == app_id).first()
        if not app:
            return None
        app.status = status
        db.flush()
        db.refresh(app)
        return app.to_dict()
