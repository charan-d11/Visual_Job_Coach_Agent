"""
job_routes.py
-------------
FastAPI routes for job search functionality.

Endpoints:
  POST /api/jobs/search  — search for job openings
  GET  /api/jobs/suggest — suggest job titles based on keywords
"""

from fastapi import APIRouter, HTTPException, Query

from app.models.job_model import JobSearchRequest, JobSearchResponse
from app.services.job_api import search_jobs_async
from app.security.input_sanitizer import sanitize_role, sanitize_location

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("/search", response_model=JobSearchResponse, summary="Search for job openings")
async def search_jobs(request: JobSearchRequest) -> JobSearchResponse:
    """
    Search for job openings matching the given role and location.

    - **role**: Job title or keywords (e.g. "data entry", "software developer")
    - **location**: City/country or "remote"
    - **remote_only**: Filter to remote-only jobs
    - **limit**: Number of results (1-50)
    """
    role = sanitize_role(request.role)
    location = sanitize_location(request.location)

    if not role:
        raise HTTPException(status_code=400, detail="Job role cannot be empty.")

    result = await search_jobs_async(
        role=role,
        location=location,
        limit=request.limit,
        remote_only=request.remote_only,
    )
    return result


@router.get("/suggest", summary="Suggest job titles")
async def suggest_jobs(
    keywords: str = Query(..., min_length=2, max_length=100, description="Keywords to suggest job titles from"),
) -> dict:
    """
    Return a list of suggested job titles based on keywords.
    Useful for autocomplete in voice/text search interfaces.
    """
    keywords_clean = sanitize_role(keywords).lower()

    # Common accessible career paths
    all_titles = [
        "Customer Service Representative",
        "Data Entry Specialist",
        "Administrative Assistant",
        "Transcriptionist",
        "Content Moderator",
        "Technical Support Specialist",
        "Software Developer",
        "Web Accessibility Consultant",
        "Social Media Manager",
        "Copy Editor",
        "Proofreader",
        "Research Analyst",
        "Virtual Assistant",
        "Bookkeeper",
        "Medical Transcriptionist",
        "Call Center Agent",
        "Online Tutor",
        "Freelance Writer",
        "Quality Assurance Tester",
        "Project Manager",
    ]

    suggestions = [t for t in all_titles if keywords_clean in t.lower()]
    if not suggestions:
        suggestions = all_titles[:5]

    return {"keywords": keywords_clean, "suggestions": suggestions[:10], "count": len(suggestions[:10])}
