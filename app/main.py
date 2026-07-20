import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.job import router as job_router
from app.routers.manager import router as manager_router
from app.routers.user import router as user_router
from app.routers.admin import router as admin_router
from app.routers.application import router as application_router

app = FastAPI(title="Job Portal Backend")

# Define allowed origins cleanly without wildcard '*' to avoid Starlette CORS assertion errors
origins = [
    "https://job-portal-frontend-rys7.onrender.com",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]

env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    for item in env_origins.split(","):
        item_clean = item.strip()
        if item_clean and item_clean != "*" and item_clean not in origins:
            origins.append(item_clean)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(job_router)
app.include_router(manager_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(application_router)


@app.get("/")
def home():
    return {"message": "Job Portal Backend Running"}