from fastapi import APIRouter, HTTPException
from app.schemas.job import JobCreate
from app.db import load_jobs, save_jobs

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/")
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
        "message": "Job Created Successfully",
        "job": new_job
    }


@router.get("/")
def get_jobs():
    db_jobs = load_jobs()
    for idx, job in enumerate(db_jobs):
        if "id" not in job:
            job["id"] = idx
    return db_jobs


@router.get("/{job_id}")
def get_job(job_id: int):
    db_jobs = load_jobs()
    found_job = None
    for job in db_jobs:
        if job.get("id") == job_id:
            found_job = job
            break

    if found_job is None:
        if 0 <= job_id < len(db_jobs):
            found_job = db_jobs[job_id]
            found_job["id"] = job_id

    if found_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    salary_val = found_job.get("salary")
    salary_str = ""
    if isinstance(salary_val, int):
        salary_str = f"₹{salary_val:,}"
    else:
        str_val = str(salary_val or '900000')
        salary_str = f"₹{str_val}" if not str_val.startswith('₹') else str_val

    return {
        "job": {
            "id": found_job.get("id"),
            "title": found_job.get("title"),
            "description": found_job.get("description"),
            "location": found_job.get("location"),
            "salary": salary_str,
            "job_type": found_job.get("job_type", "Full Time"),
            "company_name": "Shnoor Technologies"
        }
    }