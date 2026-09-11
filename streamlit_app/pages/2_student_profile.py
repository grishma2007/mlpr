"""
Student Profile Management with Full CRUD Operations
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import (
    get_all_students_api,
    get_student_api,
    create_student_api,
    update_student_api,
    delete_student_api,
    add_student_skill_api,
    delete_student_skill_api,
    add_student_project_api,
    delete_student_project_api
)

st.set_page_config(page_title="Student Profile CRUD", page_icon="👤", layout="wide")

st.title("👤 Student Profile Management")
st.markdown("Perform complete **CRUD (Create, Read, Update, Delete)** operations on student academic and skill profiles.")

# Fetch students
_, students_res = get_all_students_api()
students = students_res.get("students", [])

tab_view, tab_create, tab_edit, tab_skills_proj = st.tabs([
    "🔍 View Profiles", 
    "➕ Create New Student", 
    "✏️ Edit / Delete Profile",
    "🛠️ Manage Skills & Projects"
])

# ----------------- TAB 1: VIEW PROFILES -----------------
with tab_view:
    st.subheader("📋 Registered Student Directory")
    if not students:
        st.info("No students registered yet.")
    else:
        student_opts = {s["id"]: f"{s['name']} - {s['email']} (CGPA: {s.get('cgpa', 0.0)})" for s in students}
        sel_id = st.selectbox("Select Student to Inspect:", options=list(student_opts.keys()), format_func=lambda x: student_opts[x])
        
        _, cur_student_res = get_student_api(sel_id)
        cur_student = cur_student_res.get("student", {})
        
        if cur_student:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Name:** {cur_student['name']}")
                st.markdown(f"**Email:** {cur_student['email']}")
                st.markdown(f"**College:** {cur_student.get('college', 'N/A')}")
                st.markdown(f"**Degree:** {cur_student.get('degree', 'B.Tech')}")
            with c2:
                st.markdown(f"**Branch / Stream:** {cur_student.get('branch', 'Computer Science')}")
                st.markdown(f"**Semester:** {cur_student.get('semester', 6)}")
                st.markdown(f"**CGPA:** {cur_student.get('cgpa', 8.0)}")
                st.markdown(f"**Registered At:** {cur_student.get('created_at', 'N/A')}")
                
            st.markdown("---")
            st.markdown("##### 🛠️ Recorded Skills")
            skills = cur_student.get("skills", [])
            if skills:
                cols = st.columns(4)
                for idx, sk in enumerate(skills):
                    cols[idx % 4].success(f"**{sk['skill_name']}** ({sk.get('proficiency', 'Intermediate')})")
            else:
                st.info("No skills attached.")
                
            st.markdown("##### 📂 Portfolio Projects")
            projects = cur_student.get("projects", [])
            if projects:
                for p in projects:
                    st.write(f"🔹 **{p['title']}** - *Tech: {p.get('technologies', '')}*")
                    st.caption(p.get("description", ""))
            else:
                st.info("No projects attached.")

# ----------------- TAB 2: CREATE STUDENT -----------------
with tab_create:
    st.subheader("➕ Register New Student Profile")
    with st.form("create_student_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            new_name = st.text_input("Full Name *", placeholder="e.g. Grishma Patel")
            new_email = st.text_input("Email Address *", placeholder="e.g. grishma@university.edu")
            new_college = st.text_input("College / Institute", value="Institute of Technology and Science")
            new_degree = st.selectbox("Degree", ["B.Tech", "B.E.", "B.Sc (CS)", "BCA", "M.Tech", "MCA"])
        with col_b:
            new_branch = st.selectbox("Branch / Specialization", ["Computer Science", "Artificial Intelligence", "Data Science", "Information Technology", "Electronics"])
            new_semester = st.slider("Current Semester", min_value=1, max_value=8, value=6)
            new_cgpa = st.number_input("Cumulative CGPA (0.0 - 10.0) *", min_value=0.0, max_value=10.0, value=8.5, step=0.1)
            
        submitted = st.form_submit_button("Create Profile (HTTP POST)")
        
        if submitted:
            if not new_name.strip() or not new_email.strip():
                st.error("Name and valid email are required fields.")
            else:
                payload = {
                    "name": new_name.strip(),
                    "email": new_email.strip(),
                    "college": new_college,
                    "degree": new_degree,
                    "branch": new_branch,
                    "semester": new_semester,
                    "cgpa": new_cgpa
                }
                status, res = create_student_api(payload)
                if status == 201 and res.get("success"):
                    st.success(f"Student profile for '{new_name}' created successfully via Flask API!")
                    st.rerun()
                else:
                    st.error(f"Failed to create profile: {res.get('error', 'Unknown error')}")

# ----------------- TAB 3: EDIT / DELETE PROFILE -----------------
with tab_edit:
    st.subheader("✏️ Update or Delete Student Record")
    if not students:
        st.info("No students to edit.")
    else:
        edit_opts = {s["id"]: f"{s['name']} ({s['email']})" for s in students}
        edit_id = st.selectbox("Select Student to Edit/Delete:", options=list(edit_opts.keys()), format_func=lambda x: edit_opts[x], key="edit_sel")
        
        _, edit_student_res = get_student_api(edit_id)
        est = edit_student_res.get("student", {})
        
        if est:
            with st.form("edit_student_form"):
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    e_name = st.text_input("Name", value=est.get("name", ""))
                    e_email = st.text_input("Email", value=est.get("email", ""))
                    e_college = st.text_input("College", value=est.get("college", ""))
                    e_degree = st.text_input("Degree", value=est.get("degree", "B.Tech"))
                with e_col2:
                    e_branch = st.text_input("Branch", value=est.get("branch", "Computer Science"))
                    e_sem = st.slider("Semester", min_value=1, max_value=8, value=int(est.get("semester", 6)))
                    e_cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=float(est.get("cgpa", 8.0)), step=0.1)
                    
                update_btn = st.form_submit_button("Save Changes (HTTP PUT)")
                if update_btn:
                    up_data = {
                        "name": e_name, "email": e_email, "college": e_college,
                        "degree": e_degree, "branch": e_branch, "semester": e_sem, "cgpa": e_cgpa
                    }
                    st_code, st_res = update_student_api(edit_id, up_data)
                    if st_code == 200 and st_res.get("success"):
                        st.success("Student updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Update failed: {st_res.get('error')}")
                        
            st.markdown("---")
            st.markdown("##### 🗑️ Danger Zone")
            if st.button(f"Delete Profile for {est.get('name')}", type="primary"):
                del_code, del_res = delete_student_api(edit_id)
                if del_code == 200 and del_res.get("success"):
                    st.success("Student profile deleted.")
                    st.rerun()
                else:
                    st.error(f"Deletion failed: {del_res.get('error')}")

# ----------------- TAB 4: MANAGE SKILLS & PROJECTS -----------------
with tab_skills_proj:
    st.subheader("🛠️ Add / Remove Skills & Projects")
    if not students:
        st.info("No students available.")
    else:
        sk_opts = {s["id"]: f"{s['name']} ({s['email']})" for s in students}
        sk_id = st.selectbox("Select Student:", options=list(sk_opts.keys()), format_func=lambda x: sk_opts[x], key="sk_proj_sel")
        
        _, sk_student_res = get_student_api(sk_id)
        sst = sk_student_res.get("student", {})
        
        col_sk, col_pr = st.columns(2)
        
        with col_sk:
            st.markdown("##### ➕ Add Technical Skill")
            with st.form("add_skill_form"):
                new_skill_name = st.selectbox("Select Skill", [
                    "Python", "Java", "C++", "JavaScript", "SQL", "Machine Learning",
                    "Deep Learning", "Data Visualization", "Web Development", "Cloud",
                    "Docker", "TensorFlow", "PyTorch", "React", "Node.js", "Spring Boot", "Tableau"
                ])
                new_skill_prof = st.selectbox("Proficiency", ["Beginner", "Intermediate", "Advanced"])
                submit_sk = st.form_submit_button("Add Skill")
                if submit_sk:
                    s_code, s_res = add_student_skill_api(sk_id, new_skill_name, new_skill_prof)
                    if s_code == 201 and s_res.get("success"):
                        st.success(f"Added {new_skill_name}!")
                        st.rerun()
                    else:
                        st.error(f"Failed: {s_res.get('error')}")
                        
            st.markdown("##### Current Skills")
            for sk in sst.get("skills", []):
                sc1, sc2 = st.columns([3, 1])
                sc1.write(f"• **{sk['skill_name']}** ({sk.get('proficiency')})")
                if sc2.button("Remove", key=f"del_sk_{sk['id']}"):
                    delete_student_skill_api(sk_id, sk["id"])
                    st.rerun()
                    
        with col_pr:
            st.markdown("##### ➕ Add Portfolio Project")
            with st.form("add_project_form"):
                p_title = st.text_input("Project Title *", placeholder="e.g. AI-Powered Healthcare Diagnostics")
                p_desc = st.text_area("Description", placeholder="Summary of problem statement, architecture, and outcomes...")
                p_tech = st.text_input("Technologies Used", placeholder="e.g. Python, PyTorch, Streamlit, Docker")
                p_url = st.text_input("Project URL (GitHub / Demo)", placeholder="https://github.com/example/project")
                submit_pr = st.form_submit_button("Add Project")
                if submit_pr:
                    if not p_title.strip():
                        st.error("Project title is required.")
                    else:
                        pr_payload = {"title": p_title, "description": p_desc, "technologies": p_tech, "project_url": p_url}
                        pr_code, pr_res = add_student_project_api(sk_id, pr_payload)
                        if pr_code == 201 and pr_res.get("success"):
                            st.success("Project added successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed: {pr_res.get('error')}")
                            
            st.markdown("##### Current Projects")
            for pr in sst.get("projects", []):
                pc1, pc2 = st.columns([3, 1])
                pc1.write(f"• **{pr['title']}**")
                if pc2.button("Delete", key=f"del_pr_{pr['id']}"):
                    delete_student_project_api(pr["id"])
                    st.rerun()
