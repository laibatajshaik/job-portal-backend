from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.schemas.job import JobCreate
from app.db import (
    load_jobs,
    save_jobs,
    load_applications,
    save_applications
)

router = APIRouter(
    prefix="/manager",
    tags=["Manager"]
)


class CompanySchema(BaseModel):
    name: str
    website: Optional[str] = ""
    description: Optional[str] = ""
    industry: Optional[str] = ""
    company_size: Optional[str] = ""
    location: Optional[str] = ""
    email: Optional[str] = ""
    company_type: Optional[str] = ""
    founded_year: Optional[str] = ""
    recruitment_status: Optional[str] = "Active"
    benefits: List[str] = []


current_company = {
    "name": "Shnoor Technologies",
    "website": "https://shnoor.com",
    "description": "Leading software solutions and IT technology company.",
    "industry": "Information Technology",
    "company_size": "50-200 Employees",
    "location": "Bengaluru, India",
    "email": "company@example.com",
    "company_type": "Private Company",
    "founded_year": "2020",
    "recruitment_status": "Active",
    "benefits": [
        "Health Insurance",
        "Flexible Work",
        "Learning & Development",
        "Paid Leave",
        "Performance Benefits"
    ]
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
        "description": company.description or "",
        "industry": company.industry or "",
        "company_size": company.company_size or "",
        "location": company.location or "",
        "email": company.email or "",
        "company_type": company.company_type or "",
        "founded_year": company.founded_year or "",
        "recruitment_status": company.recruitment_status or "Active",
        "benefits": company.benefits or []
    }

    return {
        "message": "Company Registered Successfully",
        "company": current_company
    }


@router.put("/company")
def update_company(company: CompanySchema):
    global current_company

    current_company = {
        "name": company.name,
        "website": company.website or "",
        "description": company.description or "",
        "industry": company.industry or "",
        "company_size": company.company_size or "",
        "location": company.location or "",
        "email": company.email or "",
        "company_type": company.company_type or "",
        "founded_year": company.founded_year or "",
        "recruitment_status": company.recruitment_status or "Active",
        "benefits": company.benefits or []
    }

    return {
        "message": "Company Specifications Updated Successfully",
        "company": current_company
    }


@router.post("/jobs")
def create_job(job: JobCreate):
    db_jobs = load_jobs()

    new_id = 1

    if db_jobs:
        existing_ids = [
            item.get("id", 0)
            for item in db_jobs
            if isinstance(item.get("id", 0), int)
        ]

        if existing_ids:
            new_id = max(existing_ids) + 1

    new_job = {
        "id": new_id,
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
        db_apps = [
            app
            for app in db_apps
            if app.get("job_id") == job_id
        ]

    return {
        "applicants": db_apps
    }


@router.put("/jobs/{job_id}")
def edit_job(job_id: int, job: JobCreate):
    db_jobs = load_jobs()

    target_job = None

    for item in db_jobs:
        if item.get("id") == job_id:
            target_job = item
            break

    if target_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    target_job["title"] = job.title
    target_job["description"] = job.description
    target_job["location"] = job.location
    target_job["salary"] = job.salary
    target_job["job_type"] = job.job_type
    target_job["skills"] = job.skills
    target_job["expiry_date"] = job.expiry_date

    save_jobs(db_jobs)

    return {
        "message": "Job Updated Successfully",
        "job": target_job
    }


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    db_jobs = load_jobs()

    updated_jobs = [
        job
        for job in db_jobs
        if job.get("id") != job_id
    ]

    if len(updated_jobs) == len(db_jobs):
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    save_jobs(updated_jobs)

    return {
        "message": f"Job {job_id} Deleted Successfully"
    }


@router.put("/applicants/{candidate_id}/shortlist")
def shortlist_candidate(candidate_id: int):
    db_apps = load_applications()

    updated = False
    target_app = None

    for idx, app in enumerate(db_apps):

        if (
            app.get("id") == candidate_id
            or (
                app.get("id") is None
                and idx + 1 == candidate_id
            )
        ):
            app["status"] = "Shortlisted"

            if "id" not in app:
                app["id"] = idx + 1

            target_app = app
            updated = True
            break

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    save_applications(db_apps)

    try:
        from app.auth.email_sender import send_notification_email

        if target_app.get("candidate_email"):

            email = target_app.get(
                "candidate_email"
            )

            name = target_app.get(
                "candidate_name",
                "Candidate"
            )

            title = target_app.get(
                "job_title",
                "Position"
            )

            comp = target_app.get(
                "company_name",
                current_company.get(
                    "name",
                    "Company"
                )
            )

            subject = (
                f"Congratulations! You've been "
                f"shortlisted for {title}"
            )

            body = (
                f"Hi {name},\n\n"
                f"We have exciting news! Your "
                f"application for the {title} "
                f"position at {comp} has been "
                f"shortlisted.\n\n"
                f"We will be in touch shortly to "
                f"discuss the next steps in our "
                f"hiring process.\n\n"
                f"Best regards,\n"
                f"Recruitment Team"
            )

            send_notification_email(
                email,
                subject,
                body
            )

    except Exception as ex:
        print(
            f"Failed to trigger shortlist email: {ex}"
        )

    return {
        "message": (
            f"Candidate {candidate_id} "
            f"Shortlisted Successfully"
        )
    }


@router.put("/applicants/{candidate_id}/reject")
def reject_candidate(candidate_id: int):
    db_apps = load_applications()

    updated = False
    target_app = None

    for idx, app in enumerate(db_apps):

        if (
            app.get("id") == candidate_id
            or (
                app.get("id") is None
                and idx + 1 == candidate_id
            )
        ):
            app["status"] = "Rejected"

            if "id" not in app:
                app["id"] = idx + 1

            target_app = app
            updated = True
            break

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    save_applications(db_apps)

    try:
        from app.auth.email_sender import send_notification_email

        if target_app.get("candidate_email"):

            email = target_app.get(
                "candidate_email"
            )

            name = target_app.get(
                "candidate_name",
                "Candidate"
            )

            title = target_app.get(
                "job_title",
                "Position"
            )

            comp = target_app.get(
                "company_name",
                current_company.get(
                    "name",
                    "Company"
                )
            )

            subject = (
                f"Application Update - "
                f"{title} at {comp}"
            )

            body = (
                f"Hi {name},\n\n"
                f"Thank you for your interest "
                f"in the {title} position at "
                f"{comp}.\n\n"
                f"After careful consideration, "
                f"we regret to inform you that "
                f"we will not be moving forward "
                f"with your application at this "
                f"time. We appreciate the time "
                f"and effort you put into applying, "
                f"and we wish you the best in your "
                f"future endeavors.\n\n"
                f"Best regards,\n"
                f"Recruitment Team"
            )

            send_notification_email(
                email,
                subject,
                body
            )

    except Exception as ex:
        print(
            f"Failed to trigger rejection email: {ex}"
        )

    return {
        "message": (
            f"Candidate {candidate_id} "
            f"Rejected Successfully"
        )
    }
