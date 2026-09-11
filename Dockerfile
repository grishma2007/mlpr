FROM python:3.10-slim

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Initialize and seed database if not already present
RUN python scripts/initialize_database.py

# Expose Flask API & Streamlit ports
EXPOSE 5000 8501

# Default startup command (Flask Backend & HTML Web UI)
CMD ["gunicorn", "flask_api.app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]
