from fastapi import APIRouter, HTTPException
from typing import Optional
from app.db import (
    load_users,
    save_users,
    load_jobs,
    save_jobs,
    load_applications,
    save_applications
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def dashboard():
    db_users = load_users()
    db_jobs = load_jobs()
    db_apps = load_applications()
    
    companies = set()
    for job in db_jobs:
        comp = job.get("company_name")
        if comp:
            companies.add(comp)
            
    return {
        "total_users": len(db_users),
        "total_jobs": len(db_jobs),
        "total_applications": len(db_apps),
        "total_companies": max(len(companies), 1)
    }


@router.get("/users")
def get_users():
    db_users = load_users()
    # Ensure every user has an id based on index
    for idx, u in enumerate(db_users):
        if "id" not in u:
            u["id"] = idx + 1
    return {
        "users": db_users
    }


@router.get("/jobs")
def get_jobs():
    db_jobs = load_jobs()
    # Ensure every job has an id based on index
    for idx, job in enumerate(db_jobs):
        if "id" not in job:
            job["id"] = idx
    return {
        "jobs": db_jobs
    }


@router.get("/applications")
def get_applications():
    db_apps = load_applications()
    # Ensure every application has an id based on index
    for idx, app in enumerate(db_apps):
        if "id" not in app:
            app["id"] = idx + 1
    return {
        "applications": db_apps
    }


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    db_users = load_users()
    found_idx = -1
    for idx, u in enumerate(db_users):
        if idx + 1 == user_id or u.get("id") == user_id:
            found_idx = idx
            break
            
    if found_idx != -1:
        db_users.pop(found_idx)
        save_users(db_users)
        return {
            "message": "User deleted successfully"
        }
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    db_jobs = load_jobs()
    found_idx = -1
    for idx, job in enumerate(db_jobs):
        if job.get("id") == job_id or (job.get("id") is None and idx == job_id):
            found_idx = idx
            break
            
    if found_idx != -1:
        db_jobs.pop(found_idx)
        save_jobs(db_jobs)
        return {
            "message": "Job deleted successfully"
        }
    raise HTTPException(status_code=404, detail="Job not found")


@router.delete("/applications/{app_id}")
def delete_application(app_id: int):
    db_apps = load_applications()
    found_idx = -1
    for idx, app in enumerate(db_apps):
        if app.get("id") == app_id or (app.get("id") is None and idx + 1 == app_id):
            found_idx = idx
            break
            
    if found_idx != -1:
        db_apps.pop(found_idx)
        save_applications(db_apps)
        return {
            "message": "Application deleted successfully"
        }
    raise HTTPException(status_code=404, detail="Application not found")