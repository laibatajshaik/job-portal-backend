from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    salary: int
    job_type: str
    skills: str =""