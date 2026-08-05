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

def load_users() -> List[Dict[str, Any]]:
    with db_lock:
        users = _load_file(USERS_FILE, [])
        if not users:
            users = [
                {
                    "id": 1,
                    "name": "Laiba Taj",
                    "email": "laibataj1306@gmail.com",
                    "password": "acab wfla vmlk pfnl",
                    "role": "manager"
                },
                {
                    "id": 2,
                    "name": "Laiba Candidate",
                    "email": "laiba.candidate@gmail.com",
                    "password": "laiba",
                    "role": "user"
                },
                {
                    "id": 3,
                    "name": "Demo User",
                    "email": "user@gmail.com",
                    "password": "user123",
                    "role": "user"
                },
                {
                    "id": 4,
                    "name": "Demo Manager",
                    "email": "manager@gmail.com",
                    "password": "manager123",
                    "role": "manager"
                }
            ]
            _save_file(USERS_FILE, users)
        return users

def save_users(users: List[Dict[str, Any]]):
    with db_lock:
        _save_file(USERS_FILE, users)

def load_jobs() -> List[Dict[str, Any]]:
    with db_lock:
        
        jobs = _load_file(JOBS_FILE, [])
        if not jobs or len(jobs) < 10:
            jobs = [
                {
                    "id": 0,
                    "title": "Frontend Developer",
                    "description": "We are looking for a skilled React.js frontend developer to build responsive user interfaces, integrate Rest APIs, and write clean, optimized components.",
                    "location": "Bengaluru, KA",
                    "salary": 650000,
                    "job_type": "Full Time",
                    "skills": "React, JavaScript, TailwindCSS, HTML/CSS",
                    "company_name": "Razorpay",
                    "expiry_date": "2026-08-15"
                },
                {
                    "id": 1,
                    "title": "Full Stack Python Developer",
                    "description": "Join our engineering team to build scalable FastAPI web APIs, manage PostgreSQL models, and deploy robust microservices.",
                    "location": "Mumbai, MH",
                    "salary": 800000,
                    "job_type": "Full Time",
                    "skills": "Python, FastAPI, React, PostgreSQL",
                    "company_name": "Zomato",
                    "expiry_date": "2026-08-01"
                },
                {
                    "id": 2,
                    "title": "UI/UX Designer",
                    "description": "Design intuitive user journeys, wireframes, style guides, and high-fidelity mockups for our web and mobile applications.",
                    "location": "Bengaluru, KA",
                    "salary": 550000,
                    "job_type": "Contract",
                    "skills": "Figma, UI Design, Prototyping, Wireframing",
                    "company_name": "Swiggy",
                    "expiry_date": "2026-08-20"
                },
                {
                    "id": 3,
                    "title": "Data Analyst",
                    "description": "Analyze key product metrics, generate actionable business reports, manage SQL data warehouses, and build interactive dashboards.",
                    "location": "Noida, UP",
                    "salary": 500000,
                    "job_type": "Full Time",
                    "skills": "SQL, Python, Excel, Tableau, PowerBI",
                    "company_name": "Paytm",
                    "expiry_date": "2026-07-28"
                },
                {
                    "id": 4,
                    "title": "Backend Engineer (Go/Python)",
                    "description": "Build high-performance real-time backend services, manage Redis caches, design scalable system architectures, and optimize queries.",
                    "location": "Mumbai, MH",
                    "salary": 900000,
                    "job_type": "Full Time",
                    "skills": "Go, Python, Redis, Docker, Microservices",
                    "company_name": "Zepto",
                    "expiry_date": "2026-08-12"
                },
                {
                    "id": 5,
                    "title": "DevOps Engineer",
                    "description": "Manage Kubernetes clusters, configure CI/CD pipelines (GitHub Actions/Jenkins), oversee AWS cloud infrastructure, and improve security.",
                    "location": "Bengaluru, KA",
                    "salary": 750000,
                    "job_type": "Full Time",
                    "skills": "AWS, Kubernetes, Docker, CI/CD, Terraform",
                    "company_name": "Cred",
                    "expiry_date": "2026-08-02"
                },
                {
                    "id": 6,
                    "title": "Mobile App Developer (Flutter/React Native)",
                    "description": "Develop and deploy cross-platform iOS and Android apps, optimize application performance, and integrate secure payment gateways.",
                    "location": "Bengaluru, KA",
                    "salary": 700000,
                    "job_type": "Full Time",
                    "skills": "Flutter, Dart, React Native, iOS, Android",
                    "company_name": "PhonePe",
                    "expiry_date": "2026-08-25"
                },
                {
                    "id": 7,
                    "title": "Machine Learning Engineer",
                    "description": "Research, build, and deploy machine learning models for predictive analytics, NLP pipelines, and data recommendation engines.",
                    "location": "Pune, MH",
                    "salary": 450000,
                    "job_type": "Full Time",
                    "skills": "Python, PyTorch, TensorFlow, Scikit-Learn",
                    "company_name": "Tata Consultancy Services (TCS)",
                    "expiry_date": "2026-08-30"
                },
                {
                    "id": 8,
                    "title": "Cloud Infrastructure Architect",
                    "description": "Design and architect enterprise-scale cloud migrations, manage virtual networks, implement IAM policies, and optimize costs.",
                    "location": "Hyderabad, TS",
                    "salary": 1200000,
                    "job_type": "Full Time",
                    "skills": "Azure, GCP, Cloud Security, Enterprise Architecture",
                    "company_name": "Wipro",
                    "expiry_date": "2026-07-20"
                },
                {
                    "id": 9,
                    "title": "Cybersecurity Analyst",
                    "description": "Monitor network logs, perform penetration testing, implement zero-trust access controls, and respond to security incidents.",
                    "location": "Chennai, TN",
                    "salary": 600000,
                    "job_type": "Full Time",
                    "skills": "Penetration Testing, Kali Linux, SIEM, Firewalls",
                    "company_name": "HCL Tech",
                    "expiry_date": "2026-08-18"
                },
                {
                    "id": 10,
                    "title": "Product Manager",
                    "description": "Define product roadmaps, translate user needs into technical specifications, and collaborate with design/engineering teams.",
                    "location": "Bengaluru, KA",
                    "salary": 1200000,
                    "job_type": "Full Time",
                    "skills": "Product Roadmap, Agile/Scrum, User Analytics, Jira",
                    "company_name": "Flipkart",
                    "expiry_date": "2026-08-04"
                },
                {
                    "id": 11,
                    "title": "Software Engineering Intern",
                    "description": "Gain hands-on experience working with professional engineering teams, writing unit tests, and fixing application bugs.",
                    "location": "Mysuru, KA",
                    "salary": 240000,
                    "job_type": "Internship",
                    "skills": "Java, Python, Git, Basic Data Structures",
                    "company_name": "Infosys",
                    "expiry_date": "2026-08-09"
                },
                {
                    "id": 12,
                    "title": "Systems Engineer",
                    "description": "Oversee enterprise network servers, configure active directories, manage Linux system backups, and resolve hardware issues.",
                    "location": "Navi Mumbai, MH",
                    "salary": 450000,
                    "job_type": "Full Time",
                    "skills": "Linux, Server Admin, Active Directory, Networking",
                    "company_name": "Reliance Jio",
                    "expiry_date": "2026-08-05"
                },
                {
                    "id": 13,
                    "title": "Embedded Systems Developer",
                    "description": "Write firmware in C/C++ for automotive microcontrollers, develop CAN bus protocols, and perform hardware-in-the-loop testing.",
                    "location": "Pune, MH",
                    "salary": 600000,
                    "job_type": "Full Time",
                    "skills": "C/C++, Microcontrollers, RTOS, CAN bus",
                    "company_name": "Tata Motors",
                    "expiry_date": "2026-07-31"
                },
                {
                    "id": 14,
                    "title": "QA Automation Engineer",
                    "description": "Write automated Selenium/Playwright end-to-end test suites, run integration tests, and report software bugs.",
                    "location": "Bengaluru, KA",
                    "salary": 500000,
                    "job_type": "Full Time",
                    "skills": "Selenium, Java, Playwright, E2E Testing",
                    "company_name": "Ola Cabs",
                    "expiry_date": "2026-08-22"
                }
            ]
            _save_file(JOBS_FILE, jobs)
        
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

def load_applications() -> List[Dict[str, Any]]:
    with db_lock:
        return _load_file(APPLICATIONS_FILE, [])

def save_applications(applications: List[Dict[str, Any]]):
    with db_lock:
        _save_file(APPLICATIONS_FILE, applications)
