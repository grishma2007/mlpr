"""
Skill Extraction Engine with Comprehensive Normalized Taxonomy
Project: AI-Powered Student Career & Recruitment Platform
Subject: 503 – Applied Artificial Intelligence: Model Development and Deployment
"""

import re

SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "c++", "cpp", "c#", "c", "javascript", "typescript",
        "golang", "go", "rust", "ruby", "php", "swift", "kotlin", "r", "dart",
        "scala", "shell script", "bash", "powershell"
    ],
    "AI & Machine Learning": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "neural networks", "cnn", "rnn", "lstm", "transformers",
        "huggingface", "llm", "genai", "generative ai", "tensorflow", "pytorch",
        "scikit-learn", "sklearn", "keras", "pandas", "numpy", "opencv",
        "data science", "xgboost", "lightgbm", "spacy", "nltk"
    ],
    "Data Analytics & BI": [
        "data visualization", "tableau", "power bi", "powerbi", "excel", "matplotlib",
        "seaborn", "plotly", "bigquery", "data analysis", "business analytics",
        "statistics", "data mining", "alteryx", "looker"
    ],
    "Web & Backend Development": [
        "html", "html5", "css", "css3", "web development", "react", "react.js",
        "angular", "vue", "vue.js", "next.js", "nextjs", "node.js", "nodejs",
        "express", "express.js", "django", "flask", "fastapi", "spring boot",
        "spring", "asp.net", "rest api", "restful api", "graphql", "bootstrap",
        "tailwind", "tailwindcss", "redux"
    ],
    "Cloud & DevOps": [
        "cloud", "aws", "amazon web services", "azure", "microsoft azure",
        "gcp", "google cloud", "docker", "kubernetes", "k8s", "ci/cd", "git",
        "github", "gitlab", "jenkins", "linux", "ubuntu", "terraform", "ansible",
        "devops", "microservices", "serverless"
    ],
    "Databases & Storage": [
        "sql", "mysql", "postgresql", "postgres", "mongodb", "redis",
        "sqlite", "oracle", "cassandra", "dynamodb", "firebase", "firestore",
        "prisma", "sqlalchemy", "nosql"
    ],
    "Tools & Methodologies": [
        "agile", "scrum", "jira", "postman", "vscode", "jupyter", "jupyter notebook",
        "oop", "object oriented programming", "dsa", "data structures",
        "algorithms", "unit testing", "system design"
    ]
}

# Mapping of aliases to standard canonical display names
CANONICAL_NAMES = {
    "cpp": "C++",
    "c++": "C++",
    "c#": "C#",
    "c": "C",
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "golang": "Go",
    "go": "Go",
    "rust": "Rust",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "r": "R",
    "dart": "Dart",
    "scala": "Scala",
    "bash": "Bash",
    "shell script": "Shell Script",
    "powershell": "PowerShell",
    
    "html": "HTML",
    "html5": "HTML5",
    "css": "CSS",
    "css3": "CSS3",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "sqlite": "SQLite",
    "redis": "Redis",
    "oracle": "Oracle",
    "firebase": "Firebase",
    "firestore": "Firestore",
    "nosql": "NoSQL",
    
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "computer vision": "Computer Vision",
    "neural networks": "Neural Networks",
    "cnn": "CNN",
    "rnn": "RNN",
    "lstm": "LSTM",
    "transformers": "Transformers",
    "huggingface": "HuggingFace",
    "llm": "LLM",
    "genai": "Generative AI",
    "generative ai": "Generative AI",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "keras": "Keras",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "opencv": "OpenCV",
    "data science": "Data Science",
    "xgboost": "XGBoost",
    "lightgbm": "LightGBM",
    "spacy": "spaCy",
    "nltk": "NLTK",
    
    "data visualization": "Data Visualization",
    "tableau": "Tableau",
    "power bi": "PowerBI",
    "powerbi": "PowerBI",
    "excel": "Excel",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "plotly": "Plotly",
    "bigquery": "BigQuery",
    "data analysis": "Data Analysis",
    "business analytics": "Business Analytics",
    "statistics": "Statistics",
    "data mining": "Data Mining",
    
    "web development": "Web Development",
    "react": "React",
    "react.js": "React.js",
    "angular": "Angular",
    "vue": "Vue.js",
    "vue.js": "Vue.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express": "Express.js",
    "express.js": "Express.js",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "spring boot": "Spring Boot",
    "spring": "Spring",
    "asp.net": "ASP.NET",
    "rest api": "REST API",
    "restful api": "RESTful API",
    "graphql": "GraphQL",
    "bootstrap": "Bootstrap",
    "tailwind": "TailwindCSS",
    "tailwindcss": "TailwindCSS",
    "redux": "Redux",
    
    "cloud": "Cloud Computing",
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "gcp": "GCP",
    "google cloud": "Google Cloud",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "ci/cd": "CI/CD",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "jenkins": "Jenkins",
    "linux": "Linux",
    "ubuntu": "Ubuntu",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "devops": "DevOps",
    "microservices": "Microservices",
    
    "agile": "Agile",
    "scrum": "Scrum",
    "jira": "Jira",
    "postman": "Postman",
    "vscode": "VSCode",
    "jupyter": "Jupyter Notebook",
    "jupyter notebook": "Jupyter Notebook",
    "oop": "OOP",
    "object oriented programming": "OOP",
    "dsa": "Data Structures & Algorithms",
    "data structures": "Data Structures",
    "algorithms": "Algorithms"
}

# Single-letter or very short skills requiring strict delimiter matching
STRICT_SHORT_SKILLS = {"c", "r", "go"}

def extract_skills_from_text(text):
    """
    Extracts technology skills from freeform resume text using boundary-aware regex.
    Returns a sorted list of unique canonical skill names.
    """
    if not text:
        return []
    
    text_lower = " " + text.lower().replace("\n", " ").replace("\t", " ") + " "
    # Replace common punctuation with spaces while preserving +, #, -, /
    cleaned_for_search = re.sub(r'[,;()|•▪*►–\[\]{}]', ' ', text_lower)
    
    found_skills = set()
    
    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            if skill in STRICT_SHORT_SKILLS:
                # Require space/punctuation before and after for single-letter or ambiguous words
                pattern = r'(?:[\s,/(\[])' + re.escape(skill) + r'(?:[\s,/.)\]])'
            elif skill in ["c++", "c#", "ci/cd", "node.js", "next.js", "vue.js", "react.js", "express.js"]:
                # Special characters in skill name
                pattern = r'(?:\b|[\s/])' + re.escape(skill) + r'(?:\b|[\s/])'
            else:
                pattern = r'\b' + re.escape(skill) + r'\b'
                
            if re.search(pattern, cleaned_for_search):
                canonical = CANONICAL_NAMES.get(skill, skill.title())
                found_skills.add(canonical)
                
    return sorted(list(found_skills))

def categorize_skills(skills_list):
    """
    Categorizes a list of canonical skills into standard domain areas.
    """
    categorized = {}
    for skill in skills_list:
        sk_lower = skill.lower()
        matched = False
        for category, skills in SKILL_TAXONOMY.items():
            # Check if skill or canonical name matches category
            if any(s in sk_lower or sk_lower in s for s in skills):
                categorized.setdefault(category, []).append(skill)
                matched = True
                break
        if not matched:
            categorized.setdefault("Other Tools & Technologies", []).append(skill)
            
    return categorized
