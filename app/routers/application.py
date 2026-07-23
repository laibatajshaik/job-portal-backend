from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime
from jose import jwt
import random
from app.auth.jwt_handler import SECRET_KEY, ALGORITHM
from app.db import load_applications, save_applications, load_jobs, load_users

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


class ApplicationCreate(BaseModel):
    job_id: int
    resume_url: str
    cover_letter: str


def get_current_user_email(authorization: str = Header(None)) -> str:
    if not authorization:
        return "user@gmail.com"
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return email or "user@gmail.com"
    except Exception:
        return "user@gmail.com"


@router.post("/")
def apply_job(application: ApplicationCreate, authorization: str = Header(None)):
    email = get_current_user_email(authorization)
    
    # Fetch candidate name
    db_users = load_users()
    candidate_name = "Candidate"
    for u in db_users:
        if u["email"].lower() == email.lower():
            candidate_name = u["name"]
            break

    # Fetch job title
    db_jobs = load_jobs()
    job_title = f"Job #{application.job_id}"
    for job in db_jobs:
        if job.get("id") == application.job_id:
            job_title = job.get("title")
            break

    # ATS Scoring: Generate a score between 55 and 98
    ats_score = random.randint(55, 98)
    status = "Shortlisted" if ats_score >= 80 else "Pending"

    db_apps = load_applications()
    new_application = {
        "id": len(db_apps) + 1,
        "job_id": application.job_id,
        "resume_url": application.resume_url,
        "cover_letter": application.cover_letter,
        "job_title": job_title,
        "company_name": "Shnoor Technologies",
        "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": status,
        "ats_score": ats_score,
        "candidate_email": email,
        "candidate_name": candidate_name
    }

    db_apps.append(new_application)
    save_applications(db_apps)

    return {
        "message": "Application submitted successfully",
        "application": new_application
    }


@router.get("/my")
def get_my_applications(authorization: str = Header(None)):
    email = get_current_user_email(authorization)
    db_apps = load_applications()
    my_apps = [app for app in db_apps if app.get("candidate_email", "").lower() == email.lower()]
    return {
        "applications": my_apps
    }