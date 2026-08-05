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
                    "description": "About the Role:\nAs a Frontend Developer at Razorpay, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of React, JavaScript, TailwindCSS, HTML/CSS.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 650000,
                    "job_type": "Full Time",
                    "skills": "React, JavaScript, TailwindCSS, HTML/CSS",
                    "company_name": "Razorpay",
                    "expiry_date": "2026-08-10"
                },
                {
                    "id": 1,
                    "title": "Full Stack Python Developer",
                    "description": "About the Role:\nAs a Full Stack Python Developer at Zomato, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Python, FastAPI, React, PostgreSQL.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 840000,
                    "job_type": "Full Time",
                    "skills": "Python, FastAPI, React, PostgreSQL",
                    "company_name": "Zomato",
                    "expiry_date": "2026-08-11"
                },
                {
                    "id": 2,
                    "title": "UI/UX Designer",
                    "description": "About the Role:\nAs a UI/UX Designer at Swiggy, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Figma, UI Design, Prototyping, Wireframing.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 605000,
                    "job_type": "Contract",
                    "skills": "Figma, UI Design, Prototyping, Wireframing",
                    "company_name": "Swiggy",
                    "expiry_date": "2026-08-12"
                },
                {
                    "id": 3,
                    "title": "Data Analyst",
                    "description": "About the Role:\nAs a Data Analyst at Paytm, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of SQL, Python, Excel, Tableau, PowerBI.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Noida, UP",
                    "salary": 575000,
                    "job_type": "Full Time",
                    "skills": "SQL, Python, Excel, Tableau, PowerBI",
                    "company_name": "Paytm",
                    "expiry_date": "2026-08-13"
                },
                {
                    "id": 4,
                    "title": "Backend Engineer (Go/Python)",
                    "description": "About the Role:\nAs a Backend Engineer (Go/Python) at Zepto, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Go, Python, Redis, Docker, Microservices.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 1080000,
                    "job_type": "Full Time",
                    "skills": "Go, Python, Redis, Docker, Microservices",
                    "company_name": "Zepto",
                    "expiry_date": "2026-08-14"
                },
                {
                    "id": 5,
                    "title": "DevOps Engineer",
                    "description": "About the Role:\nAs a DevOps Engineer at Cred, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of AWS, Kubernetes, Docker, CI/CD, Terraform.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 750000,
                    "job_type": "Full Time",
                    "skills": "AWS, Kubernetes, Docker, CI/CD, Terraform",
                    "company_name": "Cred",
                    "expiry_date": "2026-08-15"
                },
                {
                    "id": 6,
                    "title": "Mobile App Developer (Flutter)",
                    "description": "About the Role:\nAs a Mobile App Developer (Flutter) at PhonePe, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Flutter, Dart, React Native, iOS, Android.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 735000,
                    "job_type": "Full Time",
                    "skills": "Flutter, Dart, React Native, iOS, Android",
                    "company_name": "PhonePe",
                    "expiry_date": "2026-08-16"
                },
                {
                    "id": 7,
                    "title": "Machine Learning Engineer",
                    "description": "About the Role:\nAs a Machine Learning Engineer at Flipkart, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Python, PyTorch, TensorFlow, Scikit-Learn.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Pune, MH",
                    "salary": 1045000,
                    "job_type": "Full Time",
                    "skills": "Python, PyTorch, TensorFlow, Scikit-Learn",
                    "company_name": "Flipkart",
                    "expiry_date": "2026-08-17"
                },
                {
                    "id": 8,
                    "title": "Cloud Infrastructure Architect",
                    "description": "About the Role:\nAs a Cloud Infrastructure Architect at Infosys, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Azure, GCP, Cloud Security, Enterprise Architecture.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Hyderabad, TS",
                    "salary": 1380000,
                    "job_type": "Full Time",
                    "skills": "Azure, GCP, Cloud Security, Enterprise Architecture",
                    "company_name": "Infosys",
                    "expiry_date": "2026-08-18"
                },
                {
                    "id": 9,
                    "title": "Cybersecurity Analyst",
                    "description": "About the Role:\nAs a Cybersecurity Analyst at Reliance Jio, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Penetration Testing, Kali Linux, SIEM, Firewalls.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Chennai, TN",
                    "salary": 720000,
                    "job_type": "Full Time",
                    "skills": "Penetration Testing, Kali Linux, SIEM, Firewalls",
                    "company_name": "Reliance Jio",
                    "expiry_date": "2026-08-19"
                },
                {
                    "id": 10,
                    "title": "Product Manager",
                    "description": "About the Role:\nAs a Product Manager at Google, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Product Roadmap, Agile/Scrum, User Analytics, Jira.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 1200000,
                    "job_type": "Full Time",
                    "skills": "Product Roadmap, Agile/Scrum, User Analytics, Jira",
                    "company_name": "Google",
                    "expiry_date": "2026-08-20"
                },
                {
                    "id": 11,
                    "title": "Software Engineering Intern",
                    "description": "About the Role:\nAs a Software Engineering Intern at Meta, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Java, Python, Git, Basic Data Structures.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mysuru, KA",
                    "salary": 252000,
                    "job_type": "Internship",
                    "skills": "Java, Python, Git, Basic Data Structures",
                    "company_name": "Meta",
                    "expiry_date": "2026-08-21"
                },
                {
                    "id": 12,
                    "title": "Systems Engineer",
                    "description": "About the Role:\nAs a Systems Engineer at Microsoft, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Linux, Server Admin, Active Directory, Networking.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Navi Mumbai, MH",
                    "salary": 495000,
                    "job_type": "Full Time",
                    "skills": "Linux, Server Admin, Active Directory, Networking",
                    "company_name": "Microsoft",
                    "expiry_date": "2026-08-22"
                },
                {
                    "id": 13,
                    "title": "Embedded Systems Developer",
                    "description": "About the Role:\nAs a Embedded Systems Developer at Amazon, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of C/C++, Microcontrollers, RTOS, CAN bus.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Pune, MH",
                    "salary": 690000,
                    "job_type": "Full Time",
                    "skills": "C/C++, Microcontrollers, RTOS, CAN bus",
                    "company_name": "Amazon",
                    "expiry_date": "2026-08-23"
                },
                {
                    "id": 14,
                    "title": "QA Automation Engineer",
                    "description": "About the Role:\nAs a QA Automation Engineer at Wipro, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Selenium, Java, Playwright, E2E Testing.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 600000,
                    "job_type": "Full Time",
                    "skills": "Selenium, Java, Playwright, E2E Testing",
                    "company_name": "Wipro",
                    "expiry_date": "2026-08-24"
                },
                {
                    "id": 15,
                    "title": "Frontend React Developer",
                    "description": "About the Role:\nAs a Frontend React Developer at TCS, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of React, Redux, Jest, CSS3.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 580000,
                    "job_type": "Full Time",
                    "skills": "React, Redux, Jest, CSS3",
                    "company_name": "TCS",
                    "expiry_date": "2026-08-10"
                },
                {
                    "id": 16,
                    "title": "Backend Node.js Developer",
                    "description": "About the Role:\nAs a Backend Node.js Developer at HCL Tech, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Node.js, Express, MongoDB, Redis.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 892500,
                    "job_type": "Full Time",
                    "skills": "Node.js, Express, MongoDB, Redis",
                    "company_name": "HCL Tech",
                    "expiry_date": "2026-08-11"
                },
                {
                    "id": 17,
                    "title": "Database Administrator (DBA)",
                    "description": "About the Role:\nAs a Database Administrator (DBA) at Tata Motors, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of PostgreSQL, MySQL, Oracle, Backup/Recovery.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 792000,
                    "job_type": "Full Time",
                    "skills": "PostgreSQL, MySQL, Oracle, Backup/Recovery",
                    "company_name": "Tata Motors",
                    "expiry_date": "2026-08-12"
                },
                {
                    "id": 18,
                    "title": "Cloud Security Engineer",
                    "description": "About the Role:\nAs a Cloud Security Engineer at Ola Cabs, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of AWS, CloudTrail, IAM, KMS, Security Group.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Hyderabad, TS",
                    "salary": 1127000,
                    "job_type": "Full Time",
                    "skills": "AWS, CloudTrail, IAM, KMS, Security Group",
                    "company_name": "Ola Cabs",
                    "expiry_date": "2026-08-13"
                },
                {
                    "id": 19,
                    "title": "Android Developer",
                    "description": "About the Role:\nAs a Android Developer at Razorpay, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Kotlin, Android SDK, Dagger Hilt, Retrofit.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 984000,
                    "job_type": "Full Time",
                    "skills": "Kotlin, Android SDK, Dagger Hilt, Retrofit",
                    "company_name": "Razorpay",
                    "expiry_date": "2026-08-14"
                },
                {
                    "id": 20,
                    "title": "iOS Engineer",
                    "description": "About the Role:\nAs a iOS Engineer at Zomato, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Swift, SwiftUI, Combine, Cocoapods.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Pune, MH",
                    "salary": 880000,
                    "job_type": "Full Time",
                    "skills": "Swift, SwiftUI, Combine, Cocoapods",
                    "company_name": "Zomato",
                    "expiry_date": "2026-08-15"
                },
                {
                    "id": 21,
                    "title": "Data Scientist",
                    "description": "About the Role:\nAs a Data Scientist at Swiggy, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Python, R, Jupyter, SQL, Statistics.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Noida, UP",
                    "salary": 1155000,
                    "job_type": "Full Time",
                    "skills": "Python, R, Jupyter, SQL, Statistics",
                    "company_name": "Swiggy",
                    "expiry_date": "2026-08-16"
                },
                {
                    "id": 22,
                    "title": "Technical Writer",
                    "description": "About the Role:\nAs a Technical Writer at Paytm, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Markdown, API Documentation, Git, Technical Guides.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Remote",
                    "salary": 440000,
                    "job_type": "Full Time",
                    "skills": "Markdown, API Documentation, Git, Technical Guides",
                    "company_name": "Paytm",
                    "expiry_date": "2026-08-17"
                },
                {
                    "id": 23,
                    "title": "SRE Engineer",
                    "description": "About the Role:\nAs a SRE Engineer at Zepto, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Kubernetes, Prometheus, Grafana, Ansible, AWS.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 1058000,
                    "job_type": "Full Time",
                    "skills": "Kubernetes, Prometheus, Grafana, Ansible, AWS",
                    "company_name": "Zepto",
                    "expiry_date": "2026-08-18"
                },
                {
                    "id": 24,
                    "title": "UI Engineer",
                    "description": "About the Role:\nAs a UI Engineer at Cred, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of CSS, HTML5, Canvas, WebGL, TailwindCSS.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 624000,
                    "job_type": "Full Time",
                    "skills": "CSS, HTML5, Canvas, WebGL, TailwindCSS",
                    "company_name": "Cred",
                    "expiry_date": "2026-08-19"
                },
                {
                    "id": 25,
                    "title": "Frontend Developer",
                    "description": "About the Role:\nAs a Frontend Developer at PhonePe, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of React, JavaScript, TailwindCSS, HTML/CSS.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 650000,
                    "job_type": "Full Time",
                    "skills": "React, JavaScript, TailwindCSS, HTML/CSS",
                    "company_name": "PhonePe",
                    "expiry_date": "2026-08-20"
                },
                {
                    "id": 26,
                    "title": "Full Stack Python Developer",
                    "description": "About the Role:\nAs a Full Stack Python Developer at Flipkart, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Python, FastAPI, React, PostgreSQL.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 840000,
                    "job_type": "Full Time",
                    "skills": "Python, FastAPI, React, PostgreSQL",
                    "company_name": "Flipkart",
                    "expiry_date": "2026-08-21"
                },
                {
                    "id": 27,
                    "title": "UI/UX Designer",
                    "description": "About the Role:\nAs a UI/UX Designer at Infosys, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Figma, UI Design, Prototyping, Wireframing.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 605000,
                    "job_type": "Contract",
                    "skills": "Figma, UI Design, Prototyping, Wireframing",
                    "company_name": "Infosys",
                    "expiry_date": "2026-08-22"
                },
                {
                    "id": 28,
                    "title": "Data Analyst",
                    "description": "About the Role:\nAs a Data Analyst at Reliance Jio, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of SQL, Python, Excel, Tableau, PowerBI.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Noida, UP",
                    "salary": 575000,
                    "job_type": "Full Time",
                    "skills": "SQL, Python, Excel, Tableau, PowerBI",
                    "company_name": "Reliance Jio",
                    "expiry_date": "2026-08-23"
                },
                {
                    "id": 29,
                    "title": "Backend Engineer (Go/Python)",
                    "description": "About the Role:\nAs a Backend Engineer (Go/Python) at Google, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Go, Python, Redis, Docker, Microservices.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 1080000,
                    "job_type": "Full Time",
                    "skills": "Go, Python, Redis, Docker, Microservices",
                    "company_name": "Google",
                    "expiry_date": "2026-08-24"
                },
                {
                    "id": 30,
                    "title": "DevOps Engineer",
                    "description": "About the Role:\nAs a DevOps Engineer at Meta, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of AWS, Kubernetes, Docker, CI/CD, Terraform.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 750000,
                    "job_type": "Full Time",
                    "skills": "AWS, Kubernetes, Docker, CI/CD, Terraform",
                    "company_name": "Meta",
                    "expiry_date": "2026-08-10"
                },
                {
                    "id": 31,
                    "title": "Mobile App Developer (Flutter)",
                    "description": "About the Role:\nAs a Mobile App Developer (Flutter) at Microsoft, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Flutter, Dart, React Native, iOS, Android.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 735000,
                    "job_type": "Full Time",
                    "skills": "Flutter, Dart, React Native, iOS, Android",
                    "company_name": "Microsoft",
                    "expiry_date": "2026-08-11"
                },
                {
                    "id": 32,
                    "title": "Machine Learning Engineer",
                    "description": "About the Role:\nAs a Machine Learning Engineer at Amazon, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Python, PyTorch, TensorFlow, Scikit-Learn.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Pune, MH",
                    "salary": 1045000,
                    "job_type": "Full Time",
                    "skills": "Python, PyTorch, TensorFlow, Scikit-Learn",
                    "company_name": "Amazon",
                    "expiry_date": "2026-08-12"
                },
                {
                    "id": 33,
                    "title": "Cloud Infrastructure Architect",
                    "description": "About the Role:\nAs a Cloud Infrastructure Architect at Wipro, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Azure, GCP, Cloud Security, Enterprise Architecture.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Hyderabad, TS",
                    "salary": 1380000,
                    "job_type": "Full Time",
                    "skills": "Azure, GCP, Cloud Security, Enterprise Architecture",
                    "company_name": "Wipro",
                    "expiry_date": "2026-08-13"
                },
                {
                    "id": 34,
                    "title": "Cybersecurity Analyst",
                    "description": "About the Role:\nAs a Cybersecurity Analyst at TCS, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Penetration Testing, Kali Linux, SIEM, Firewalls.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Chennai, TN",
                    "salary": 720000,
                    "job_type": "Full Time",
                    "skills": "Penetration Testing, Kali Linux, SIEM, Firewalls",
                    "company_name": "TCS",
                    "expiry_date": "2026-08-14"
                },
                {
                    "id": 35,
                    "title": "Product Manager",
                    "description": "About the Role:\nAs a Product Manager at HCL Tech, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Product Roadmap, Agile/Scrum, User Analytics, Jira.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 1200000,
                    "job_type": "Full Time",
                    "skills": "Product Roadmap, Agile/Scrum, User Analytics, Jira",
                    "company_name": "HCL Tech",
                    "expiry_date": "2026-08-15"
                },
                {
                    "id": 36,
                    "title": "Software Engineering Intern",
                    "description": "About the Role:\nAs a Software Engineering Intern at Tata Motors, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Java, Python, Git, Basic Data Structures.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mysuru, KA",
                    "salary": 252000,
                    "job_type": "Internship",
                    "skills": "Java, Python, Git, Basic Data Structures",
                    "company_name": "Tata Motors",
                    "expiry_date": "2026-08-16"
                },
                {
                    "id": 37,
                    "title": "Systems Engineer",
                    "description": "About the Role:\nAs a Systems Engineer at Ola Cabs, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Linux, Server Admin, Active Directory, Networking.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Navi Mumbai, MH",
                    "salary": 495000,
                    "job_type": "Full Time",
                    "skills": "Linux, Server Admin, Active Directory, Networking",
                    "company_name": "Ola Cabs",
                    "expiry_date": "2026-08-17"
                },
                {
                    "id": 38,
                    "title": "Embedded Systems Developer",
                    "description": "About the Role:\nAs a Embedded Systems Developer at Razorpay, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of C/C++, Microcontrollers, RTOS, CAN bus.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Pune, MH",
                    "salary": 690000,
                    "job_type": "Full Time",
                    "skills": "C/C++, Microcontrollers, RTOS, CAN bus",
                    "company_name": "Razorpay",
                    "expiry_date": "2026-08-18"
                },
                {
                    "id": 39,
                    "title": "QA Automation Engineer",
                    "description": "About the Role:\nAs a QA Automation Engineer at Zomato, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Selenium, Java, Playwright, E2E Testing.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 600000,
                    "job_type": "Full Time",
                    "skills": "Selenium, Java, Playwright, E2E Testing",
                    "company_name": "Zomato",
                    "expiry_date": "2026-08-19"
                },
                {
                    "id": 40,
                    "title": "Frontend React Developer",
                    "description": "About the Role:\nAs a Frontend React Developer at Swiggy, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of React, Redux, Jest, CSS3.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 580000,
                    "job_type": "Full Time",
                    "skills": "React, Redux, Jest, CSS3",
                    "company_name": "Swiggy",
                    "expiry_date": "2026-08-20"
                },
                {
                    "id": 41,
                    "title": "Backend Node.js Developer",
                    "description": "About the Role:\nAs a Backend Node.js Developer at Paytm, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Node.js, Express, MongoDB, Redis.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 892500,
                    "job_type": "Full Time",
                    "skills": "Node.js, Express, MongoDB, Redis",
                    "company_name": "Paytm",
                    "expiry_date": "2026-08-21"
                },
                {
                    "id": 42,
                    "title": "Database Administrator (DBA)",
                    "description": "About the Role:\nAs a Database Administrator (DBA) at Zepto, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of PostgreSQL, MySQL, Oracle, Backup/Recovery.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 792000,
                    "job_type": "Full Time",
                    "skills": "PostgreSQL, MySQL, Oracle, Backup/Recovery",
                    "company_name": "Zepto",
                    "expiry_date": "2026-08-22"
                },
                {
                    "id": 43,
                    "title": "Cloud Security Engineer",
                    "description": "About the Role:\nAs a Cloud Security Engineer at Cred, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of AWS, CloudTrail, IAM, KMS, Security Group.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Hyderabad, TS",
                    "salary": 1127000,
                    "job_type": "Full Time",
                    "skills": "AWS, CloudTrail, IAM, KMS, Security Group",
                    "company_name": "Cred",
                    "expiry_date": "2026-08-23"
                },
                {
                    "id": 44,
                    "title": "Android Developer",
                    "description": "About the Role:\nAs a Android Developer at PhonePe, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Kotlin, Android SDK, Dagger Hilt, Retrofit.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 984000,
                    "job_type": "Full Time",
                    "skills": "Kotlin, Android SDK, Dagger Hilt, Retrofit",
                    "company_name": "PhonePe",
                    "expiry_date": "2026-08-24"
                },
                {
                    "id": 45,
                    "title": "iOS Engineer",
                    "description": "About the Role:\nAs a iOS Engineer at Flipkart, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Swift, SwiftUI, Combine, Cocoapods.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Pune, MH",
                    "salary": 880000,
                    "job_type": "Full Time",
                    "skills": "Swift, SwiftUI, Combine, Cocoapods",
                    "company_name": "Flipkart",
                    "expiry_date": "2026-08-10"
                },
                {
                    "id": 46,
                    "title": "Data Scientist",
                    "description": "About the Role:\nAs a Data Scientist at Infosys, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Python, R, Jupyter, SQL, Statistics.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Noida, UP",
                    "salary": 1155000,
                    "job_type": "Full Time",
                    "skills": "Python, R, Jupyter, SQL, Statistics",
                    "company_name": "Infosys",
                    "expiry_date": "2026-08-11"
                },
                {
                    "id": 47,
                    "title": "Technical Writer",
                    "description": "About the Role:\nAs a Technical Writer at Reliance Jio, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Markdown, API Documentation, Git, Technical Guides.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Remote",
                    "salary": 440000,
                    "job_type": "Full Time",
                    "skills": "Markdown, API Documentation, Git, Technical Guides",
                    "company_name": "Reliance Jio",
                    "expiry_date": "2026-08-12"
                },
                {
                    "id": 48,
                    "title": "SRE Engineer",
                    "description": "About the Role:\nAs a SRE Engineer at Google, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of Kubernetes, Prometheus, Grafana, Ansible, AWS.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Mumbai, MH",
                    "salary": 1058000,
                    "job_type": "Full Time",
                    "skills": "Kubernetes, Prometheus, Grafana, Ansible, AWS",
                    "company_name": "Google",
                    "expiry_date": "2026-08-13"
                },
                {
                    "id": 49,
                    "title": "UI Engineer",
                    "description": "About the Role:\nAs a UI Engineer at Meta, you will work with engineering teams to deploy client-facing solutions. You will maintain system architectures, resolve bugs, and scale application performance.\n\nKey Responsibilities:\n- Design and implement clean, high-performance features in line with coding guidelines.\n- Troubleshoot service bottlenecks and resolve integration bugs.\n- Participate in team sprints, peer code reviews, and standups.\n\nRequirements & Qualifications:\n- Strong understanding of CSS, HTML5, Canvas, WebGL, TailwindCSS.\n- Analytical mindset, team-focused communication, and Git version control workflows.",
                    "location": "Bengaluru, KA",
                    "salary": 624000,
                    "job_type": "Full Time",
                    "skills": "CSS, HTML5, Canvas, WebGL, TailwindCSS",
                    "company_name": "Meta",
                    "expiry_date": "2026-08-14"
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
        apps = _load_file(APPLICATIONS_FILE, [])
        if not apps or len(apps) < 3:
            apps = [
                {
                    "id": 1,
                    "job_id": 0,
                    "resume_url": "https://drive.google.com/file/d/1abc/view",
                    "cover_letter": "I am a skilled React.js developer eager to join Razorpay.",
                    "job_title": "Frontend Developer",
                    "company_name": "Razorpay",
                    "applied_at": "2026-08-05T14:10:00Z",
                    "status": "Selected",
                    "ats_score": 98,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "React, JavaScript, TailwindCSS, HTML/CSS"
                },
                {
                    "id": 2,
                    "job_id": 2,
                    "resume_url": "https://drive.google.com/file/d/3abc/view",
                    "cover_letter": "I have experience designing mobile user interfaces in Figma.",
                    "job_title": "UI/UX Designer",
                    "company_name": "Swiggy",
                    "applied_at": "2026-08-05T11:30:00Z",
                    "status": "Interviewing",
                    "ats_score": 88,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "Figma, UI Design, Prototyping, Wireframing"
                },
                {
                    "id": 3,
                    "job_id": 4,
                    "resume_url": "https://drive.google.com/file/d/4abc/view",
                    "cover_letter": "I build concurrent and optimized Go APIs.",
                    "job_title": "Backend Engineer (Go/Python)",
                    "company_name": "Zepto",
                    "applied_at": "2026-08-05T09:15:00Z",
                    "status": "Pending",
                    "ats_score": 72,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "Go, Python, Redis, Docker, Microservices"
                },
                {
                    "id": 4,
                    "job_id": 5,
                    "resume_url": "https://drive.google.com/file/d/5abc/view",
                    "cover_letter": "SRE and Kubernetes cluster specialist.",
                    "job_title": "DevOps Engineer",
                    "company_name": "Cred",
                    "applied_at": "2026-08-04T16:45:00Z",
                    "status": "Rejected",
                    "ats_score": 58,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "AWS, Kubernetes, Docker, CI/CD, Terraform"
                },
                {
                    "id": 5,
                    "job_id": 1,
                    "resume_url": "https://drive.google.com/file/d/2abc/view",
                    "cover_letter": "I want to work on Python full stack at Zomato.",
                    "job_title": "Full Stack Python Developer",
                    "company_name": "Zomato",
                    "applied_at": "2026-08-05T12:00:00Z",
                    "status": "Interviewing",
                    "ats_score": 85,
                    "candidate_email": "user@gmail.com",
                    "candidate_name": "Demo Candidate",
                    "skills": "Python, FastAPI, React, PostgreSQL"
                },
                {
                    "id": 6,
                    "job_id": 6,
                    "resume_url": "https://drive.google.com/file/d/6abc/view",
                    "cover_letter": "Experienced Flutter mobile coder.",
                    "job_title": "Mobile App Developer (Flutter/React Native)",
                    "company_name": "PhonePe",
                    "applied_at": "2026-08-05T08:30:00Z",
                    "status": "Pending",
                    "ats_score": 78,
                    "candidate_email": "user@gmail.com",
                    "candidate_name": "Demo Candidate",
                    "skills": "Flutter, Dart, React Native, iOS, Android"
                }
            ]
            _save_file(APPLICATIONS_FILE, apps)
        return apps

def save_applications(applications: List[Dict[str, Any]]):
    with db_lock:
        _save_file(APPLICATIONS_FILE, applications)
