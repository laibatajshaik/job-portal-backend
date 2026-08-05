from fastapi import APIRouter, HTTPException
from app.schemas.job import JobCreate
from app.db import load_jobs, save_jobs, load_applications, save_applications
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/manager",
    tags=["Manager"]
)

class CompanySchema(BaseModel):
    name: str
    website: Optional[str] = ""
    description: Optional[str] = ""

current_company = {
    "name": "Shnoor Technologies",
    "website": "https://shnoor.com",
    "description": "Leading software solutions and IT technology company."
}

@router.get("/company")
def get_company():
    return {
        "company": current_company
    }

@router.post("/company")
def register_company(company: CompanySchema):
    global current_company
    current_company = {
        "name": company.name,
        "website": company.website or "",
        "description": company.description or ""
    }
    return {
        "message": "Company Registered Successfully",
        "company": current_company
    }

@router.post("/jobs")
def create_job(job: JobCreate):
    db_jobs = load_jobs()
    new_job = {
        "id": len(db_jobs),
        "title": job.title,
        "description": job.description,
        "location": job.location,
        "salary": job.salary,
        "job_type": job.job_type,
        "skills": job.skills,
        "expiry_date": job.expiry_date
    }
    db_jobs.append(new_job)
    save_jobs(db_jobs)
    return {
        "message": "Job Posted Successfully",
        "job": new_job
    }

@router.get("/applicants")
def view_applicants(job_id: Optional[int] = None):
    db_apps = load_applications()
    
    modified = False
    for idx, app in enumerate(db_apps):
        if "id" not in app:
            app["id"] = idx + 1
            modified = True
    if modified:
        save_applications(db_apps)
        
    if job_id is not None:
        db_apps = [app for app in db_apps if app.get("job_id") == job_id]
    return {
        "applicants": db_apps
    }

@router.put("/jobs/{job_id}")
def edit_job(job_id: int):
    return {
        "message": f"Job {job_id} Updated Successfully"
    }

@router.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    return {
        "message": f"Job {job_id} Deleted Successfully"
    }

@router.put("/applicants/{candidate_id}/shortlist")
def shortlist_candidate(candidate_id: int):
    db_apps = load_applications()
    updated = False
    for idx, app in enumerate(db_apps):
        
        if app.get("id") == candidate_id or (app.get("id") is None and idx + 1 == candidate_id):
            app["status"] = "Shortlisted"
            if "id" not in app:
                app["id"] = idx + 1
            updated = True
            break
            
    if updated:
        save_applications(db_apps)
        try:
            from app.auth.email_sender import send_notification_email
            target_app = None
            for a in db_apps:
                if a.get("id") == candidate_id:
                    target_app = a
                    break
            if target_app and target_app.get("candidate_email"):
                email = target_app.get("candidate_email")
                name = target_app.get("candidate_name", "Candidate")
                title = target_app.get("job_title", "Position")
                comp = target_app.get("company_name", "Shnoor Technologies")
                subject = f"Congratulations! You've been shortlisted for {title}"
                body = f"Hi {name},\n\nWe have exciting news! Your application for the {title} position at {comp} has been shortlisted.\n\nWe will be in touch shortly to discuss the next steps in our hiring process.\n\nBest regards,\nRecruitment Team"
                send_notification_email(email, subject, body)
        except Exception as ex:
            print(f"Failed to trigger shortlist email: {ex}")
        return {
            "message": f"Candidate {candidate_id} Shortlisted Successfully"
        }
    raise HTTPException(status_code=404, detail="Application not found")

@router.put("/applicants/{candidate_id}/reject")
def reject_candidate(candidate_id: int):
    db_apps = load_applications()
    updated = False
    for idx, app in enumerate(db_apps):
        
        if app.get("id") == candidate_id or (app.get("id") is None and idx + 1 == candidate_id):
            app["status"] = "Rejected"
            if "id" not in app:
                app["id"] = idx + 1
            updated = True
            break
            
    if updated:
        save_applications(db_apps)
        try:
            from app.auth.email_sender import send_notification_email
            target_app = None
            for a in db_apps:
                if a.get("id") == candidate_id:
                    target_app = a
                    break
            if target_app and target_app.get("candidate_email"):
                email = target_app.get("candidate_email")
                name = target_app.get("candidate_name", "Candidate")
                title = target_app.get("job_title", "Position")
                comp = target_app.get("company_name", "Shnoor Technologies")
                subject = f"Application Update - {title} at {comp}"
                body = f"Hi {name},\n\nThank you for your interest in the {title} position at {comp}.\n\nAfter careful consideration, we regret to inform you that we will not be moving forward with your application at this time. We appreciate the time and effort you put into applying, and we wish you the best in your future endeavors.\n\nBest regards,\nRecruitment Team"
                send_notification_email(email, subject, body)
        except Exception as ex:
            print(f"Failed to trigger rejection email: {ex}")
        return {
            "message": f"Candidate {candidate_id} Rejected Successfully"
        }
    raise HTTPException(status_code=404, detail="Application not found")