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
        "skills": job.skills
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
    
    # Auto-assign IDs if missing in stored records
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
        # Match by explicit ID or fallback index (1-based index matching candidate_id)
        if app.get("id") == candidate_id or (app.get("id") is None and idx + 1 == candidate_id):
            app["status"] = "Shortlisted"
            if "id" not in app:
                app["id"] = idx + 1
            updated = True
            break
            
    if updated:
        save_applications(db_apps)
        return {
            "message": f"Candidate {candidate_id} Shortlisted Successfully"
        }
    raise HTTPException(status_code=404, detail="Application not found")


@router.put("/applicants/{candidate_id}/reject")
def reject_candidate(candidate_id: int):
    db_apps = load_applications()
    updated = False
    for idx, app in enumerate(db_apps):
        # Match by explicit ID or fallback index (1-based index matching candidate_id)
        if app.get("id") == candidate_id or (app.get("id") is None and idx + 1 == candidate_id):
            app["status"] = "Rejected"
            if "id" not in app:
                app["id"] = idx + 1
            updated = True
            break
            
    if updated:
        save_applications(db_apps)
        return {
            "message": f"Candidate {candidate_id} Rejected Successfully"
        }
    raise HTTPException(status_code=404, detail="Application not found")