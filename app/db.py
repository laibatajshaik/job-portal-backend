import json
import os
import threading
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")

db_lock = threading.Lock()

def _load_file(filepath: str, default: Any) -> Any:
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save_file(filepath: str, data: Any):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to {filepath}: {e}")

# Users
def load_users() -> List[Dict[str, Any]]:
    with db_lock:
        return _load_file(USERS_FILE, [])

def save_users(users: List[Dict[str, Any]]):
    with db_lock:
        _save_file(USERS_FILE, users)

# Jobs
def load_jobs() -> List[Dict[str, Any]]:
    with db_lock:
        # Default jobs if file is empty or doesn't exist
        jobs = _load_file(JOBS_FILE, [])
        if not jobs:
            jobs = [
                {
                    "id": 0,
                    "title": "Frontend Developer",
                    "description": "We are looking for a skilled React.js frontend developer to build responsive user interfaces.",
                    "location": "Bengaluru, KA",
                    "salary": 900000,
                    "job_type": "Full Time",
                    "skills": "React, JavaScript, TailwindCSS, HTML/CSS"
                },
                {
                    "id": 1,
                    "title": "Full Stack Python Developer",
                    "description": "Join our engineering team to build scalable FastAPI web APIs and modern web applications.",
                    "location": "Mumbai, MH",
                    "salary": 1150000,
                    "job_type": "Full Time",
                    "skills": "Python, FastAPI, React, PostgreSQL"
                },
                {
                    "id": 2,
                    "title": "UI/UX Designer",
                    "description": "Design intuitive user journeys, wireframes, and high-fidelity mockups for our web platform.",
                    "location": "Hyderabad, TS",
                    "salary": 850000,
                    "job_type": "Contract",
                    "skills": "Figma, UI Design, Prototyping"
                },
                {
                    "id": 3,
                    "title": "Data Analyst",
                    "description": "Analyze key product metrics, generate actionable business reports, and manage SQL data models.",
                    "location": "Pune, MH",
                    "salary": 800000,
                    "job_type": "Full Time",
                    "skills": "SQL, Python, Excel, Tableau"
                }
            ]
            _save_file(JOBS_FILE, jobs)
        
        # Enforce every job has a valid int ID
        modified = False
        for idx, job in enumerate(jobs):
            if "id" not in job:
                job["id"] = idx
                modified = True
        if modified:
            _save_file(JOBS_FILE, jobs)
            
        return jobs

def save_jobs(jobs: List[Dict[str, Any]]):
    with db_lock:
        _save_file(JOBS_FILE, jobs)

# Applications
def load_applications() -> List[Dict[str, Any]]:
    with db_lock:
        return _load_file(APPLICATIONS_FILE, [])

def save_applications(applications: List[Dict[str, Any]]):
    with db_lock:
        _save_file(APPLICATIONS_FILE, applications)
