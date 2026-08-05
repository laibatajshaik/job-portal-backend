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

class ApplicationUpdateStatus(BaseModel):
    status: str

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
    
    db_users = load_users()
    candidate_name = "Candidate"
    for u in db_users:
        if u["email"].lower() == email.lower():
            candidate_name = u["name"]
            break

    db_jobs = load_jobs()
    job_title = f"Job #{application.job_id}"
    company_name = "Demo Company"
    if application.job_id == -1:
        job_title = "Uploaded Resume"
        company_name = "Personal Archive"
    else:
        for job in db_jobs:
            if job.get("id") == application.job_id:
                job_title = job.get("title")
                company_name = job.get("company_name", "Demo Company")
                break

    ats_score = random.randint(55, 98)
    status = "Shortlisted" if ats_score >= 80 else "Pending"

    db_apps = load_applications()
    new_application = {
        "id": len(db_apps) + 1,
        "job_id": application.job_id,
        "resume_url": application.resume_url,
        "cover_letter": application.cover_letter,
        "job_title": job_title,
        "company_name": company_name,
        "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": status,
        "ats_score": ats_score,
        "candidate_email": email,
        "candidate_name": candidate_name
    }

    db_apps.append(new_application)
    save_applications(db_apps)

    try:
        from app.auth.email_sender import send_notification_email
        subject = f"Application Submitted - {job_title} at {company_name}"
        body = f"Hi {candidate_name},\n\nThank you for applying to the {job_title} position at {company_name}! We have successfully received your application.\n\nOur team will review your application and keep you updated on the next steps.\n\nBest regards,\nRecruitment Team"
        send_notification_email(email, subject, body)
    except Exception as ex:
        print(f"Failed to send submission email to {email}: {ex}")

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

@router.get("/my-applications")
def get_my_applications_list(authorization: str = Header(None)):
    email = get_current_user_email(authorization)
    db_apps = load_applications()
    my_apps = [app for app in db_apps if app.get("candidate_email", "").lower() == email.lower()]
    return my_apps

@router.get("/job/{job_id}")
def get_applications_by_job(job_id: int):
    db_apps = load_applications()
    job_apps = [app for app in db_apps if app.get("job_id") == job_id]
    return job_apps

@router.patch("/{app_id}")
def update_application_status(app_id: int, update_data: ApplicationUpdateStatus):
    db_apps = load_applications()
    updated = False
    for app in db_apps:
        if app.get("id") == app_id:
            app["status"] = update_data.status
            updated = True
            break
    if not updated:
        if 0 < app_id <= len(db_apps):
            db_apps[app_id - 1]["status"] = update_data.status
            updated = True
            
    if updated:
        save_applications(db_apps)
        try:
            from app.auth.email_sender import send_notification_email
            target_app = None
            for a in db_apps:
                if a.get("id") == app_id:
                    target_app = a
                    break
            if target_app and target_app.get("candidate_email"):
                email = target_app.get("candidate_email")
                name = target_app.get("candidate_name", "Candidate")
                title = target_app.get("job_title", "Position")
                comp = target_app.get("company_name", "Shnoor Technologies")
                status = update_data.status
                
                subject = ""
                body = ""
                if status in ["Shortlisted", "Selected"]:
                     subject = f"Congratulations! You've been shortlisted for {title}"
                     body = f"Hi {name},\n\nWe have exciting news! Your application for the {title} position at {comp} has been shortlisted.\n\nWe will be in touch shortly to discuss the next steps in our hiring process.\n\nBest regards,\nRecruitment Team"
                elif status == "Rejected":
                     subject = f"Application Update - {title} at {comp}"
                     body = f"Hi {name},\n\nThank you for your interest in the {title} position at {comp}.\n\nAfter careful consideration, we regret to inform you that we will not be moving forward with your application at this time. We appreciate the time and effort you put into applying, and we wish you the best in your future endeavors.\n\nBest regards,\nRecruitment Team"
                elif status == "Interviewing":
                     subject = f"Interview Scheduled - {title} at {comp}"
                     body = f"Hi {name},\n\nGood news! An interview has been scheduled for your application for the {title} position at {comp}.\n\nPlease keep an eye on your inbox for calendar invites and details regarding the meeting link or venue.\n\nBest regards,\nRecruitment Team"
                 
                if subject and body:
                     send_notification_email(email, subject, body)
        except Exception as ex:
            print(f"Failed to send status update email: {ex}")
        return {"message": "Application status updated successfully"}
        
    raise HTTPException(status_code=404, detail="Application not found")

import os
import shutil
import uuid
from fastapi import UploadFile, File

@router.post("/upload-cv")
def upload_cv(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join("uploads", unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_url = f"/uploads/{unique_filename}"
    return {
        "message": "File uploaded successfully",
        "file_url": file_url,
        "filename": file.filename
    }