from fastapi import APIRouter, HTTPException
from app.schemas.job import JobCreate

router = APIRouter(prefix="/jobs", tags=["Jobs"])

jobs = []

@router.post("/")
def create_job(job: JobCreate):
    jobs.append(job)
    return {
        "message": "Job Created Successfully",
        "job": job
    }


@router.get("/")
def get_jobs():
    return jobs

@router.get("/{job_id}")
def get_job(job_id: int):
    if job_id < 0 or job_id >= len(jobs):
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    return {
        "job": {
            "id": job_id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "job_type": job.job_type,
            "company_name": "Demo Company"
        }
    }