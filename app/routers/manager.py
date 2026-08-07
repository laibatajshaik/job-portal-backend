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


COMPANY_SPECIFICATIONS = {
    "Shnoor Technologies": {
        "website": "https://shnoor.com",
        "description": "Leading software solutions and IT technology company.",
        "industry": "Information Technology",
        "company_size": "50-200 Employees",
        "location": "Bengaluru, India",
        "email": "company@example.com",
        "company_type": "Private Company",
        "founded_year": "2020"
    },
    "Razorpay": {
        "website": "https://razorpay.com",
        "description": "Financial technology company providing payment and business banking solutions.",
        "industry": "FinTech",
        "company_size": "1000-5000 Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@razorpay.com",
        "company_type": "Private Company",
        "founded_year": "2014"
    },
    "Zomato": {
        "website": "https://www.zomato.com",
        "description": "Online food delivery and restaurant discovery platform.",
        "industry": "Food Technology",
        "company_size": "5000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "info@zomato.com",
        "company_type": "Public Company",
        "founded_year": "2008"
    },
    "Swiggy": {
        "website": "https://www.swiggy.com",
        "description": "Online food ordering and delivery platform.",
        "industry": "Food Technology",
        "company_size": "5000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@swiggy.in",
        "company_type": "Public Company",
        "founded_year": "2014"
    },
    "Google": {
        "website": "https://www.google.com",
        "description": "Global technology company specializing in internet services and digital products.",
        "industry": "Information Technology",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@google.com",
        "company_type": "Public Company",
        "founded_year": "1998"
    },
    "Meta": {
        "website": "https://www.meta.com",
        "description": "Technology company focused on social networking and immersive digital experiences.",
        "industry": "Information Technology",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@meta.com",
        "company_type": "Public Company",
        "founded_year": "2004"
    },
    "Microsoft": {
        "website": "https://www.microsoft.com",
        "description": "Global technology company providing software, cloud and digital services.",
        "industry": "Information Technology",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@microsoft.com",
        "company_type": "Public Company",
        "founded_year": "1975"
    },
    "Amazon": {
        "website": "https://www.amazon.com",
        "description": "Global technology and e-commerce company offering online retail and cloud services.",
        "industry": "E-Commerce and Technology",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@amazon.com",
        "company_type": "Public Company",
        "founded_year": "1994"
    },
    "Paytm": {
        "website": "https://paytm.com",
        "description": "Digital payments and financial services platform.",
        "industry": "FinTech",
        "company_size": "5000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "care@paytm.com",
        "company_type": "Public Company",
        "founded_year": "2010"
    },
    "Zepto": {
        "website": "https://www.zeptonow.com",
        "description": "Quick commerce platform providing rapid grocery delivery.",
        "industry": "E-Commerce",
        "company_size": "1000-5000 Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@zeptonow.com",
        "company_type": "Private Company",
        "founded_year": "2021"
    },
    "Cred": {
        "website": "https://cred.club",
        "description": "FinTech platform offering credit card and financial management services.",
        "industry": "FinTech",
        "company_size": "1000-5000 Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@cred.club",
        "company_type": "Private Company",
        "founded_year": "2018"
    },
    "PhonePe": {
        "website": "https://www.phonepe.com",
        "description": "Digital payments and financial services technology company.",
        "industry": "FinTech",
        "company_size": "5000+ Employees",
        "location": "Pune, Maharashtra",
        "email": "support@phonepe.com",
        "company_type": "Private Company",
        "founded_year": "2015"
    },
    "Flipkart": {
        "website": "https://www.flipkart.com",
        "description": "Major Indian e-commerce platform offering products and digital services.",
        "industry": "E-Commerce",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "cs@flipkart.com",
        "company_type": "Private Company",
        "founded_year": "2007"
    },
    "Infosys": {
        "website": "https://www.infosys.com",
        "description": "Global information technology and consulting services company.",
        "industry": "Information Technology",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "askus@infosys.com",
        "company_type": "Public Company",
        "founded_year": "1981"
    },
    "Reliance Jio": {
        "website": "https://www.jio.com",
        "description": "Digital services and telecommunications company providing connectivity and technology services.",
        "industry": "Telecommunications",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "care@jio.com",
        "company_type": "Private Company",
        "founded_year": "2016"
    },
    "Wipro": {
        "website": "https://www.wipro.com",
        "description": "Global information technology, consulting and business process services company.",
        "industry": "Information Technology",
        "company_size": "10000+ Employees",
        "location": "Pune, Maharashtra",
        "email": "info@wipro.com",
        "company_type": "Public Company",
        "founded_year": "1945"
    },
    "TCS": {
        "website": "https://www.tcs.com",
        "description": "Global IT services, consulting and business solutions company.",
        "industry": "Information Technology",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "corporate.communications@tcs.com",
        "company_type": "Public Company",
        "founded_year": "1968"
    },
    "HCL Tech": {
        "website": "https://www.hcltech.com",
        "description": "Global technology company providing IT services and digital transformation solutions.",
        "industry": "Information Technology",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "info@hcltech.com",
        "company_type": "Public Company",
        "founded_year": "1976"
    },
    "Tata Motors": {
        "website": "https://www.tatamotors.com",
        "description": "Automotive company manufacturing passenger and commercial vehicles.",
        "industry": "Automotive",
        "company_size": "10000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "customercare@tatamotors.com",
        "company_type": "Public Company",
        "founded_year": "1945"
    },
    "Ola Cabs": {
        "website": "https://www.olacabs.com",
        "description": "Mobility company providing ride-hailing and transportation services.",
        "industry": "Transportation Technology",
        "company_size": "5000+ Employees",
        "location": "Bengaluru, Karnataka",
        "email": "support@olacabs.com",
        "company_type": "Private Company",
        "founded_year": "2010"
    }
}

@router.get("/company")
def get_company():
    return {
        "company": current_company
    }


@router.get("/companies")
def get_companies():
    db_jobs = load_jobs()
    companies = {}

    for job in db_jobs:
        company_name = job.get("company_name")

        if not company_name:
            continue

        if company_name not in companies:
            details = COMPANY_SPECIFICATIONS.get(
                company_name,
                {}
            )

            companies[company_name] = {
                "name": company_name,
                "website": details.get("website", ""),
                "description": details.get("description", ""),
                "industry": details.get(
                    "industry",
                    "Information Technology"
                ),
                "company_size": details.get("company_size", ""),
                "location": details.get(
                    "location",
                    job.get("location", "")
                ),
                "email": details.get("email", ""),
                "company_type": details.get("company_type", ""),
                "founded_year": details.get("founded_year", ""),
                "recruitment_status": details.get(
                    "recruitment_status",
                    "Active"
                ),
                "benefits": details.get("benefits", []),
                "total_jobs": 0,
                "jobs": []
            }

        companies[company_name]["total_jobs"] += 1

        companies[company_name]["jobs"].append({
            "id": job.get("id"),
            "title": job.get("title", ""),
            "location": job.get("location", ""),
            "salary": job.get("salary", ""),
            "job_type": job.get("job_type", ""),
            "skills": job.get("skills", ""),
            "expiry_date": job.get("expiry_date", "")
        })

    return {
        "companies": list(companies.values())
    }


@router.get("/companies/{company_name}")
def get_company_by_name(company_name: str):
    db_jobs = load_jobs()

    company_jobs = [
        job
        for job in db_jobs
        if job.get("company_name", "").lower()
        == company_name.lower()
    ]

    if not company_jobs:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    actual_company_name = company_jobs[0].get(
        "company_name",
        company_name
    )

    details = COMPANY_SPECIFICATIONS.get(
        actual_company_name,
        {}
    )

    company_data = {
        "name": actual_company_name,
        "website": details.get("website", ""),
        "description": details.get("description", ""),
        "industry": details.get(
            "industry",
            "Information Technology"
        ),
        "company_size": details.get("company_size", ""),
        "location": details.get(
            "location",
            company_jobs[0].get("location", "")
        ),
        "email": details.get("email", ""),
        "company_type": details.get("company_type", ""),
        "founded_year": details.get("founded_year", ""),
        "recruitment_status": details.get(
            "recruitment_status",
            "Active"
        ),
        "benefits": details.get("benefits", []),
        "total_jobs": len(company_jobs),
        "jobs": []
    }

    for job in company_jobs:
        company_data["jobs"].append({
            "id": job.get("id"),
            "title": job.get("title", ""),
            "description": job.get("description", ""),
            "location": job.get("location", ""),
            "salary": job.get("salary", ""),
            "job_type": job.get("job_type", ""),
            "skills": job.get("skills", ""),
            "expiry_date": job.get("expiry_date", "")
        })

    return {
        "company": company_data
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

    COMPANY_SPECIFICATIONS[company.name] = current_company.copy()

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

    COMPANY_SPECIFICATIONS[company.name] = current_company.copy()

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
            email = target_app.get("candidate_email")
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
            email = target_app.get("candidate_email")
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
