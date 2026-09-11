# 🎓 AI-Powered Student Career & Recruitment Platform

**Subject:** 503 – Applied Artificial Intelligence: Model Development and Deployment  
**Domain:** End-to-End Machine Learning, Model Deployment, Dual Frontend Architecture (HTML/CSS & Streamlit), and Intelligent Recruitment Systems.

---

## 📌 1. Project Overview

The **AI-Powered Student Career & Recruitment Platform** is a complete, production-ready, multi-tier artificial intelligence application that bridges the gap between university students and corporate recruiters.

The platform provides **Dual Frontends**:
1. **🌐 Modern HTML5 / Vanilla CSS3 / JavaScript Web Frontend:** Served directly at `http://127.0.0.1:5000/` featuring glassmorphism, responsive navigation, modal dialogs, and real-time Chart.js visualizations.
2. **🎈 Streamlit Interactive Multi-Page Application:** Running on `http://localhost:8501` featuring interactive forms, Plotly charts, and student/recruiter portals.

Both frontends communicate seamlessly with the **Flask REST API Backend** and **SQLite Database** (`SQLAlchemy ORM`).

---

## 🏗️ 2. Dual-Frontend System Architecture

```text
                                USER / BROWSER
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
            ┌───────────────────────────┐ ┌───────────────────────────┐
            │  HTML / CSS / JS Frontend │ │   Streamlit Web UI        │
            │  (http://127.0.0.1:5000)  │ │   (http://localhost:8501) │
            └─────────────┬─────────────┘ └─────────────┬─────────────┘
                          │                             │
                          └──────────────┬──────────────┘
                                         ▼
                                   HTTP Request
                                         ▼
                            ┌───────────────────────────┐
                            │   Flask REST API Backend  │ (Port 5000)
                            │ (Modular Blueprints)      │
                            └───────────────────────────┘
                                         │
                      ┌──────────────────┼──────────────────┐
                      ▼                  ▼                  ▼
                Career Model       Academic Model      AI / NLP Engine
               (Random Forest)    (Random Forest)   (TF-IDF / Apriori / Q-Learning)
              career_model.joblib academic_risk_model.joblib
                      │                  │                  │
                      └──────────────────┼──────────────────┘
                                         ▼
                            ┌───────────────────────────┐
                            │     SQLite Database       │
                            │    (SQLAlchemy ORM)       │
                            └───────────────────────────┘
```

---

## 🚀 3. Dual Frontend Options

| Feature / Capability | 🌐 HTML/CSS/JS Frontend (`:5000`) | 🎈 Streamlit Frontend (`:8501`) |
| :--- | :--- | :--- |
| **URL** | `http://127.0.0.1:5000/` | `http://localhost:8501` |
| **UI Technology** | HTML5, Vanilla CSS3 (Glassmorphism), Chart.js | Streamlit 1.6x, Plotly charts, Python components |
| **Student Profile CRUD** | ✅ Modal & Inline forms, Skill/Project manager | ✅ Multi-tab CRUD with form inputs |
| **Career Prediction** | ✅ Sliders + Skill toggles + Donut chart | ✅ Interactive form + Gauge & Distribution |
| **Academic Risk Classifier** | ✅ Real-time risk cards & recommendations | ✅ Interactive sliders & prescriptive badges |
| **Resume Parser (NLP)** | ✅ PDF upload / Text paste & entity viewer | ✅ PyPDF2 parser & 1-click sync |
| **Skill Gap & Learning** | ✅ Target role comparison & course catalog | ✅ Dynamic readiness gauge & resource cards |
| **Job Matching & Apply** | ✅ TF-IDF match score + 1-click quick apply | ✅ Explainable multi-factor breakdown |
| **Recruiter Dashboard** | ✅ Job posting modal & status switcher | ✅ Metrics cards & applicant tables |
| **Candidate AI Ranking** | ✅ Explainable leaderboard & score breakdown | ✅ Weighted scoring & natural language rationale |
| **Model Evaluation Lab** | ✅ 4-model benchmark & GridSearchCV logs | ✅ Confusion matrix heatmaps & report tables |
| **Apriori vs FP-Growth** | ✅ Runtime speedup cards & rules table | ✅ Interactive threshold sliders & benchmarks |
| **RL Q-Learning Demo** | ✅ Step-by-step optimal trajectory viewer | ✅ Reward convergence curve & Q-table |

---

## ⚡ 4. How to Run Both Frontends

### Terminal 1: Start Flask Backend & HTML Frontend
```bash
python flask_api/app.py
```
👉 Open `http://127.0.0.1:5000/` in your browser to access the **HTML/CSS/JS Web App**!

### Terminal 2: Start Streamlit Frontend
```bash
streamlit run streamlit_app/app.py
```
👉 Open `http://localhost:8501` in your browser to access the **Streamlit Web App**!

---

## 🧪 5. Automated Verification & Testing

Run all unit and integration test suites:
```bash
python -m unittest discover tests
```
*(All 14 tests passing)*

---

## 🌐 6. Cloud & Docker Deployment

### 🐳 Option A: One-Command Docker Compose
Run both the Flask REST API/HTML UI and the Streamlit UI together:
```bash
docker compose up -d --build
```
- **HTML5/CSS3 Frontend + REST API:** `http://localhost:5000`
- **Streamlit Multi-Page UI:** `http://localhost:8501`

### ☁️ Option B: Free Cloud Deployment (Streamlit Cloud + Render)
1. **Deploy Flask API on [Render.com](https://render.com):**
   - Click **New Web Service** $\rightarrow$ Connect this GitHub repository.
   - Build Command: `pip install -r requirements.txt && python scripts/initialize_database.py`
   - Start Command: `gunicorn flask_api.app:app --bind 0.0.0.0:$PORT`
   - Yields your public URL (e.g. `https://career-platform-api.onrender.com`).
2. **Deploy Streamlit on [Streamlit Community Cloud](https://share.streamlit.io):**
   - Click **New App** $\rightarrow$ Select this GitHub repository.
   - Main file path: `streamlit_app/app.py`
   - In **Advanced Settings** $\rightarrow$ **Secrets**, add:
     ```toml
     FLASK_API_BASE_URL = "https://your-flask-service.onrender.com/api"
     ```
   - Click **Deploy!**

