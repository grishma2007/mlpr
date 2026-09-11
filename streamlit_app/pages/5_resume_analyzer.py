"""
AI-Powered Resume Analyzer & Information Extraction Interface
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import analyze_resume_api, get_all_students_api, add_student_skill_api, create_student_api

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & Information Extractor")
st.markdown("""
Upload a candidate's **PDF**, **Word (.docx)**, or **Text (.txt)** resume to automatically extract contact details, education, technical skills taxonomy, work experience, projects, and certifications using NLP.
""")

tab_upload, tab_paste, tab_samples = st.tabs([
    "📤 Upload Resume File (PDF / DOCX / TXT)",
    "📝 Paste Resume Text",
    "✨ Try Sample Resume Profiles"
])

file_to_analyze = None
text_to_analyze = None

with tab_upload:
    uploaded_file = st.file_uploader(
        "Choose a Resume File (PDF, DOCX, or TXT):",
        type=["pdf", "docx", "txt"],
        help="Upload standard resume document format."
    )
    if uploaded_file:
        file_to_analyze = uploaded_file

with tab_paste:
    sample_text = """GRISHMA PATEL
Email: grishma@university.edu | Phone: +91 98765 43210
Education: B.Tech in Computer Science and Artificial Intelligence, Institute of Technology, CGPA: 8.8/10.0

SKILLS & TECHNOLOGIES:
- Programming Languages: Python, Java, C++, JavaScript, TypeScript, SQL, HTML, CSS
- AI & Data Science: Machine Learning, Deep Learning, PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, Data Visualization
- Cloud & DevOps: Docker, Kubernetes, AWS, Git, GitHub, Linux, CI/CD
- Web & Frameworks: Flask, Django, FastAPI, React, Node.js, REST API

PROJECTS:
1. AI-Powered Student Career & Recruitment Platform: End-to-end ML platform using Flask REST API, Streamlit, and Random Forest.
2. Intelligent Medical Image Classifier: Built CNN with PyTorch achieving 94% F1-score.

WORK EXPERIENCE & INTERNSHIPS:
- Machine Learning Engineer Intern at AI Innovations Lab (June 2025 - August 2025)
- Certified in Deep Learning Specialization (Coursera / DeepLearning.AI)
"""
    pasted_text = st.text_area("Paste Full Resume Text:", value=sample_text, height=240)
    if st.button("🔍 Analyze Pasted Text"):
        text_to_analyze = pasted_text

with tab_samples:
    st.markdown("Select a sample resume profile to test the extraction engine instantly:")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        if st.button("Sample A: Data Science & AI Engineer"):
            text_to_analyze = sample_text
    with c_s2:
        if st.button("Sample B: Full Stack & Cloud Developer"):
            text_to_analyze = """ROHAN SHARMA
Email: rohan.dev@techuniv.edu | Phone: +91 91234 56789
Education: Bachelor of Technology in Information Technology, CGPA: 8.2

TECHNICAL SKILLS:
Languages: Java, Python, JavaScript, TypeScript, SQL, HTML5, CSS3
Backend & Web: Node.js, Express, React, Spring Boot, RESTful API, GraphQL
Database: PostgreSQL, MongoDB, Redis, MySQL
Cloud & Tools: AWS, Docker, Git, Linux, Postman, Agile, Jira

PROJECTS:
- Cloud-Native E-Commerce Microservices: Built microservices using Node.js, Docker, and AWS ECS.
- Real-Time Chat Platform: Implemented WebSocket with Redis pub/sub.

EXPERIENCE:
- Full Stack Developer Intern at NexTech Solutions (Jan 2025 - May 2025)
- AWS Certified Cloud Practitioner (Amazon Web Services)
"""

if file_to_analyze or text_to_analyze:
    with st.spinner("Extracting resume contents and executing NLP skill taxonomy parser..."):
        if file_to_analyze:
            status_code, res_data = analyze_resume_api(file_obj=file_to_analyze)
        else:
            status_code, res_data = analyze_resume_api(raw_text=text_to_analyze)

    if status_code == 200 and res_data.get("success"):
        parsed = res_data.get("parsed_resume", {})
        st.success("### 🎉 Resume Analysis Completed Successfully!")

        # Header Details Card
        st.markdown(f"""
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h2 style="color: #60a5fa; margin: 0 0 0.25rem 0;">{parsed.get('name', 'Candidate')}</h2>
                    <p style="color: #cbd5e1; margin: 0; font-size: 0.95rem;">
                        📧 <b>Email:</b> {parsed.get('email') or 'Not Found'} &nbsp;|&nbsp; 
                        📞 <b>Phone:</b> {parsed.get('phone') or 'Not Found'} &nbsp;|&nbsp; 
                        📊 <b>Extracted CGPA:</b> <span style="color: #34d399; font-weight: 700;">{parsed.get('cgpa', 8.0)} / 10.0</span>
                    </p>
                </div>
                <span style="background: #0f172a; color: #38bdf8; border: 1px solid #0284c7; padding: 0.4rem 0.85rem; border-radius: 9999px; font-weight: 700; font-size: 0.85rem;">
                    {len(parsed.get('skills', []))} Technical Skills Extracted
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2 Column layout: Education & Experience
        col_ed, col_exp = st.columns(2)
        with col_ed:
            st.markdown("#### 🎓 Education & Degree Qualifications")
            edu_list = parsed.get("education", [])
            if edu_list:
                for deg in edu_list:
                    st.markdown(f"• **{deg}**")
            else:
                st.info("Undergraduate Degree inferred from resume context.")

        with col_exp:
            st.markdown("#### 💼 Experience & Internships")
            exp_list = parsed.get("experience", [])
            if exp_list:
                for item in exp_list:
                    st.markdown(f"• {item}")
            else:
                st.info("No explicit experience entries detected.")

        st.markdown("---")

        # Categorized Skills Display
        st.markdown("#### 🛠️ Categorized Technical Skills Taxonomy")
        categorized = parsed.get("categorized_skills", {})
        all_skills = parsed.get("skills", [])

        if categorized:
            cat_keys = list(categorized.keys())
            cols = st.columns(min(len(cat_keys), 3))
            for idx, cat_name in enumerate(cat_keys):
                with cols[idx % len(cols)]:
                    st.markdown(f"**{cat_name}**")
                    for sk in categorized[cat_name]:
                        st.markdown(f"""<span style="background: #0f172a; color: #60a5fa; border: 1px solid #1e3a8a; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 0.15rem;">✓ {sk}</span>""", unsafe_allow_html=True)
                    st.write("")
        else:
            st.warning("No technical skills detected in the document text.")

        # Projects & Certifications
        col_p, col_c = st.columns(2)
        with col_p:
            st.markdown("#### 🚀 Key Projects & Implementations")
            projs = parsed.get("projects", [])
            if projs:
                for p in projs:
                    st.markdown(f"• {p}")
            else:
                st.info("Academic capstone projects inferred.")

        with col_c:
            st.markdown("#### 🏆 Certifications & Credentials")
            certs = parsed.get("certifications", [])
            if certs:
                for c in certs:
                    st.markdown(f"🏆 **{c}**")
            else:
                st.info("No external certifications listed.")

        st.markdown("---")

        # Profile Actions (Sync to Profile OR Create New Student from Resume)
        st.subheader("💾 Apply Resume to Student Database (CRUD)")
        act_tab1, act_tab2 = st.tabs(["➕ Sync Skills to Existing Student Profile", "👤 Create New Student From Resume Data"])

        with act_tab1:
            _, std_res = get_all_students_api()
            students = std_res.get("students", [])
            if students:
                st_sync_opts = {s["id"]: f"{s['name']} ({s['email']}) - Current Skills: {len(s.get('skills', []))}" for s in students}
                sync_id = st.selectbox("Select Student Profile to Sync Skills:", options=list(st_sync_opts.keys()), format_func=lambda x: st_sync_opts[x])

                if st.button("🚀 Sync All Extracted Skills to Selected Student", type="primary"):
                    added = 0
                    for sk in all_skills:
                        c, _ = add_student_skill_api(sync_id, sk, proficiency="Intermediate")
                        if c in [200, 201]:
                            added += 1
                    st.success(f"🎉 Successfully synced {added} extracted skills to student record #{sync_id}!")
            else:
                st.info("No registered students found. Create one in the next tab.")

        with act_tab2:
            st.markdown("Directly register a new student using the parsed resume information:")
            c_n1, c_n2 = st.columns(2)
            with c_n1:
                new_name = st.text_input("Name:", value=parsed.get("name", "New Student"))
                new_email = st.text_input("Email:", value=parsed.get("email", "student@university.edu"))
                new_degree = st.selectbox("Degree:", ["B.Tech", "BCA", "B.Sc", "M.Tech", "MCA"])
            with c_n2:
                new_branch = st.selectbox("Branch:", ["Computer Science", "Artificial Intelligence", "Data Science", "Information Technology"])
                new_cgpa = st.number_input("CGPA:", min_value=0.0, max_value=10.0, value=float(parsed.get("cgpa", 8.5)), step=0.1)
                new_sem = st.slider("Semester:", 1, 8, 6)

            if st.button("➕ Create Student Record (HTTP POST)"):
                st_code, st_data = create_student_api({
                    "name": new_name,
                    "email": new_email,
                    "college": "Institute of Technology & Science",
                    "degree": new_degree,
                    "branch": new_branch,
                    "semester": new_sem,
                    "cgpa": new_cgpa
                })
                if st_code in [200, 201] and st_data.get("success"):
                    created_id = st_data.get("student", {}).get("id")
                    # Sync skills
                    for sk in all_skills:
                        if created_id:
                            add_student_skill_api(created_id, sk, proficiency="Intermediate")
                    st.success(f"🎉 Created profile for '{new_name}' with {len(all_skills)} attached skills!")
                else:
                    st.error(f"Failed to create profile: {st_data.get('error')}")

        with st.expander("🔍 View Raw Extracted Resume Text"):
            st.text(parsed.get("raw_text_snippet", "No raw text available."))

    else:
        st.error(f"Analysis failed: {res_data.get('error', 'Flask API Connection Error')}")
