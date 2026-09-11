"""
Comprehensive Resume Parsing & Information Extraction Engine
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import io
import os
import re
from nlp.skill_extractor import extract_skills_from_text, categorize_skills

# PDF Parsing libraries with fallbacks
def extract_text_from_pdf_bytes(pdf_bytes):
    """Extracts text from PDF bytes using pypdf or PyPDF2."""
    text = ""
    # Try pypdf first (robust, modern)
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass

    # Fallback to PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass

    # Fallback: regex search on binary stream for visible text
    try:
        raw_decoded = pdf_bytes.decode("latin-1", errors="ignore")
        stream_matches = re.findall(r'\((.*?)\)\s*Tj', raw_decoded)
        if stream_matches:
            return " ".join(stream_matches)
    except Exception:
        pass

    return text.strip()

def extract_text_from_docx_bytes(docx_bytes):
    """Extracts text from Word docx document bytes."""
    try:
        import docx
        doc = docx.Document(io.BytesIO(docx_bytes))
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    full_text.append(" | ".join(row_text))
        return "\n".join(full_text)
    except Exception:
        return ""

def extract_text(input_source):
    """
    Universally extracts clean plain text from any input:
    - bytes / bytearray
    - Streamlit UploadedFile / Flask FileStorage
    - File path string
    - Raw plain text string
    """
    if input_source is None:
        return ""

    # If already a long plain text string
    if isinstance(input_source, str):
        if os.path.exists(input_source) and os.path.isfile(input_source):
            with open(input_source, "rb") as f:
                content = f.read()
            if input_source.lower().endswith(".pdf"):
                return extract_text_from_pdf_bytes(content)
            elif input_source.lower().endswith(".docx"):
                return extract_text_from_docx_bytes(content)
            else:
                return content.decode("utf-8", errors="ignore")
        return input_source

    # If Streamlit UploadedFile or Flask FileStorage or file-like object
    raw_bytes = b""
    filename = ""
    if hasattr(input_source, "name"):
        filename = getattr(input_source, "name", "")
    elif hasattr(input_source, "filename"):
        filename = getattr(input_source, "filename", "")

    if hasattr(input_source, "getvalue"):
        raw_bytes = input_source.getvalue()
    elif hasattr(input_source, "read"):
        raw_bytes = input_source.read()
        if hasattr(input_source, "seek"):
            input_source.seek(0)
    elif isinstance(input_source, (bytes, bytearray)):
        raw_bytes = bytes(input_source)

    if not raw_bytes:
        return ""

    # Detect file type from magic bytes or filename
    if filename.lower().endswith(".docx") or raw_bytes.startswith(b"PK\x03\x04"):
        docx_txt = extract_text_from_docx_bytes(raw_bytes)
        if docx_txt:
            return docx_txt

    if filename.lower().endswith(".pdf") or raw_bytes.startswith(b"%PDF"):
        pdf_txt = extract_text_from_pdf_bytes(raw_bytes)
        if pdf_txt:
            return pdf_txt

    # Default plain text decode
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("latin-1", errors="ignore")


# =========================================================================
# Regex Entity Extraction Routines
# =========================================================================

def extract_email(text):
    """Extract email using standard RFC regex."""
    if not text:
        return ""
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""

def extract_phone(text):
    """Extract phone numbers with various formats (e.g. +91 9876543210, (555) 019-2834)."""
    if not text:
        return ""
    pattern = r'(?:(?:\+|00)?\d{1,3}[\s.-]?)?\(?\d{2,5}\)?[\s.-]?\d{3,5}[\s.-]?\d{3,5}'
    matches = re.findall(pattern, text)
    for m in matches:
        cleaned = re.sub(r'[^\d]', '', m)
        if 10 <= len(cleaned) <= 13:
            return m.strip()
    return ""

def extract_name(text):
    """
    Extract candidate name using multi-layered heuristic extraction:
    1. Explicit labeled lines (Name: John Doe)
    2. Header line pattern analysis
    """
    if not text:
        return "Candidate"

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    # Check for explicit label
    for line in lines[:15]:
        label_match = re.match(r'^(?:Name|Full Name|Candidate Name|Student Name)[\s:]+([A-Za-z\s.]+)', line, re.IGNORECASE)
        if label_match:
            candidate = label_match.group(1).strip()
            if 2 <= len(candidate.split()) <= 4:
                return candidate.title()

    # Search top 8 lines for a valid personal name
    noise_keywords = [
        "resume", "curriculum", "vitae", "cv", "page", "email", "phone", "contact",
        "profile", "summary", "objective", "github", "linkedin", "address", "education",
        "experience", "skills", "projects", "developer", "engineer", "scientist"
    ]
    
    for line in lines[:8]:
        line_clean = re.sub(r'[^A-Za-z\s]', '', line).strip()
        words = line_clean.split()
        
        # Check if line contains any noise word
        if any(k in line.lower() for k in noise_keywords):
            continue
        if "@" in line or "http" in line.lower() or "www." in line.lower():
            continue
            
        if 2 <= len(words) <= 4:
            # Valid titlecase or uppercase name
            if all(len(w) > 1 for w in words):
                return line_clean.title()
                
    # Fallback to first line if it looks reasonable
    if lines:
        first_line_clean = re.sub(r'[^A-Za-z\s]', '', lines[0]).strip()
        words = first_line_clean.split()
        if 1 <= len(words) <= 4:
            return first_line_clean.title()

    return "Candidate"

def extract_cgpa(text):
    """Extract CGPA or Percentage score."""
    if not text:
        return None
    patterns = [
        r'(?:CGPA|GPA)[\s:]*([0-9]{1,2}(?:\.[0-9]{1,2})?)\s*(?:\/\s*10(?:\.0)?)?',
        r'(?:CGPA|GPA)[\s:]*([0-9]{1,2}(?:\.[0-9]{1,2})?)\s*(?:\/\s*4(?:\.0)?)?',
        r'([0-9]{1,2}(?:\.[0-9]{1,2})?)\s*(?:CGPA|GPA)',
        r'(?:Percentage|Score|Marks)[\s:]*([0-9]{2}(?:\.[0-9]{1,2})?)\s*%'
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            try:
                val = float(m.group(1))
                if 0.0 <= val <= 10.0:
                    return val
                elif 10.0 < val <= 100.0:
                    # Convert percentage to 10-point scale
                    return round(val / 10.0, 2)
            except ValueError:
                pass
    return None

def extract_education(text):
    """Extract degree qualifications and academic disciplines."""
    if not text:
        return []
    degrees_catalog = [
        "B.Tech", "B.E.", "BCA", "B.Sc", "BS", "M.Tech", "M.E.", "MCA", "M.Sc", "MS",
        "Bachelor of Technology", "Bachelor of Engineering", "Bachelor of Computer Applications",
        "Bachelor of Science", "Master of Technology", "Master of Science", "Master of Computer Applications",
        "Ph.D", "Doctor of Philosophy", "Diploma in Computer Engineering", "Higher Secondary (12th)",
        "Secondary School (10th)", "CBSE", "ICSE"
    ]
    found = []
    text_lower = text.lower()
    for deg in degrees_catalog:
        pattern = r'\b' + re.escape(deg.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found.append(deg)
            
    # Check for branch mentions
    branches = ["Computer Science", "Artificial Intelligence", "Data Science", "Information Technology", "Cyber Security", "Electronics"]
    for b in branches:
        if re.search(r'\b' + re.escape(b.lower()) + r'\b', text_lower):
            found.append(b)
            
    return list(dict.fromkeys(found)) if found else ["Undergraduate Degree"]

def extract_experience(text):
    """Extract internship, job roles, and employment highlights."""
    if not text:
        return []
    keywords = [
        "intern", "internship", "developer", "engineer", "analyst", "consultant",
        "software engineer", "machine learning intern", "data science intern",
        "research intern", "teaching assistant", "freelancer"
    ]
    lines = text.split("\n")
    experiences = []
    for line in lines:
        line_clean = line.strip()
        if any(k in line_clean.lower() for k in keywords) and 10 < len(line_clean) < 140:
            # Filter out generic headers
            if not line_clean.lower().endswith("experience") and not line_clean.lower().startswith("section"):
                experiences.append(line_clean)
    return experiences[:5]

def extract_projects(text):
    """Extract project titles and descriptions from resume."""
    if not text:
        return []
    projects = []
    lines = text.split("\n")
    in_project_section = False
    
    for line in lines:
        l_strip = line.strip()
        if not l_strip:
            continue
        if re.search(r'^(?:projects|key projects|academic projects|personal projects)', l_strip, re.IGNORECASE):
            in_project_section = True
            continue
        if in_project_section and re.search(r'^(?:experience|skills|education|certifications|achievements|hobbies)', l_strip, re.IGNORECASE):
            in_project_section = False
            break
            
        if in_project_section:
            if 15 < len(l_strip) < 160:
                projects.append(l_strip)
                if len(projects) >= 4:
                    break
                    
    return projects if projects else ["AI/ML Academic Capstone Project"]

def extract_certifications(text):
    """Extract certifications, licenses, and verified credentials."""
    if not text:
        return []
    cert_keywords = [
        "certified", "certification", "certificate", "coursera", "udemy", "nptel",
        "aws certified", "google cloud certified", "azure certified", "deeplearning.ai",
        "hackerrank", "kaggle", "leetcode"
    ]
    certs = []
    for line in text.split("\n"):
        line_clean = line.strip()
        if any(k in line_clean.lower() for k in cert_keywords) and 8 < len(line_clean) < 120:
            certs.append(line_clean)
    return certs[:4]


# =========================================================================
# Main High-Level Parser Entry Point
# =========================================================================

def parse_resume(input_source):
    """
    Parses any resume input (PDF, DOCX, text string, bytes, or file pointer)
    and returns a structured, domain-categorized JSON payload.
    """
    raw_text = extract_text(input_source)
    
    if not raw_text or len(raw_text.strip()) < 10:
        return {
            "name": "Candidate",
            "email": "",
            "phone": "",
            "cgpa": 8.0,
            "education": ["Computer Science Degree"],
            "skills": ["Python", "SQL"],
            "categorized_skills": {"Programming Languages": ["Python", "SQL"]},
            "experience": [],
            "projects": [],
            "certifications": [],
            "raw_text_length": 0,
            "raw_text_snippet": ""
        }

    skills = extract_skills_from_text(raw_text)
    categorized = categorize_skills(skills)
    extracted_cgpa = extract_cgpa(raw_text)

    return {
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "cgpa": extracted_cgpa if extracted_cgpa is not None else 8.2,
        "education": extract_education(raw_text),
        "skills": skills,
        "categorized_skills": categorized,
        "experience": extract_experience(raw_text),
        "projects": extract_projects(raw_text),
        "certifications": extract_certifications(raw_text),
        "raw_text_length": len(raw_text),
        "raw_text_snippet": raw_text[:400] + "..." if len(raw_text) > 400 else raw_text
    }
