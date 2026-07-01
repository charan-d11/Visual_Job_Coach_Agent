"""
job_api.py
----------
Job search service. Tries JSearch (RapidAPI) if a key is configured,
otherwise returns rich mock data so the app works without any API key.
"""

import uuid
from typing import Optional

import httpx

from app.config import settings
from app.models.job_model import Job, JobSearchResponse

_JSEARCH_BASE = "https://jsearch.p.rapidapi.com"
_JSEARCH_HEADERS = {
    "X-RapidAPI-Key": settings.job_api_key,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
}


def _mock_jobs(role: str, location: str, limit: int) -> list[Job]:
    """Return rich mock job listings when no real API key is available."""
    templates = [
        {
            "title": f"{role.title()} Specialist",
            "company": "Inclusive Tech Co.",
            "location": location,
            "description": (
                f"We are looking for a passionate {role} Specialist to join our remote-first team. "
                "We offer screen-reader-friendly tooling, flexible hours, and full accessibility support."
            ),
            "url": "https://example-jobs.com/job/1",
            "salary": "$45,000 - $65,000 / year",
            "job_type": "Full-time",
            "remote": "remote" in location.lower(),
            "accessibility_note": "Screen-reader friendly workplace; keyboard-only navigation supported.",
            "posted_at": "2 days ago",
        },
        {
            "title": f"Junior {role.title()}",
            "company": "AccessFirst Solutions",
            "location": location,
            "description": (
                f"Entry-level {role} position perfect for candidates starting their career. "
                "Remote-friendly, flexible hours, and a supportive onboarding program."
            ),
            "url": "https://example-jobs.com/job/2",
            "salary": "$35,000 - $48,000 / year",
            "job_type": "Full-time",
            "remote": True,
            "accessibility_note": "Remote-friendly, flexible hours, disability accommodations available.",
            "posted_at": "1 day ago",
        },
        {
            "title": f"Senior {role.title()}",
            "company": "Empowerment Digital",
            "location": location,
            "description": (
                f"Senior {role} needed with 3+ years experience. Join a diverse, inclusive team. "
                "Voice-first tools and accessible communication platforms used company-wide."
            ),
            "url": "https://example-jobs.com/job/3",
            "salary": "$70,000 - $95,000 / year",
            "job_type": "Full-time",
            "remote": True,
            "accessibility_note": "Voice-first tools, WCAG 2.1 AA compliant internal systems.",
            "posted_at": "3 days ago",
        },
        {
            "title": f"{role.title()} Consultant",
            "company": "Bridge Careers",
            "location": location,
            "description": (
                f"Freelance / contract {role} consultant opportunities. Work on your schedule. "
                "All client communications via email and accessible video conferencing."
            ),
            "url": "https://example-jobs.com/job/4",
            "salary": "$25 - $45 / hour",
            "job_type": "Contract",
            "remote": True,
            "accessibility_note": "Fully remote, async-first communication style.",
            "posted_at": "5 days ago",
        },
        {
            "title": f"{role.title()} Assistant",
            "company": "ClearPath Nonprofit",
            "location": location,
            "description": (
                f"Support our mission as a {role} Assistant. Nonprofit with strong disability "
                "inclusion policies. Subsidized public transit and home office setup provided."
            ),
            "url": "https://example-jobs.com/job/5",
            "salary": "$32,000 - $42,000 / year",
            "job_type": "Part-time",
            "remote": False,
            "accessibility_note": "Disability inclusion policy, subsidized assistive tech provided.",
            "posted_at": "1 week ago",
        },
    ]
    jobs = []
    for i, t in enumerate(templates[:limit]):
        jobs.append(Job(id=str(uuid.uuid4()), **t))
    return jobs


async def search_jobs_async(
    role: str,
    location: str = "remote",
    limit: int = 10,
    remote_only: bool = False,
) -> JobSearchResponse:
    """
    Search for jobs. Uses JSearch API if key is configured, else mock data.
    """
    if settings.job_api_key:
        # Try real JSearch API
        query = f"{role} in {location}"
        if remote_only:
            query += " remote"
        params = {"query": query, "page": "1", "num_pages": "1"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{_JSEARCH_BASE}/search",
                    params=params,
                    headers=_JSEARCH_HEADERS,
                )
                resp.raise_for_status()
                data = resp.json().get("data", [])
                jobs = []
                for item in data[:limit]:
                    jobs.append(
                        Job(
                            id=item.get("job_id", str(uuid.uuid4())),
                            title=item.get("job_title", ""),
                            company=item.get("employer_name", ""),
                            location=item.get("job_city", location),
                            description=item.get("job_description", "")[:500],
                            url=item.get("job_apply_link", ""),
                            salary=(
                                f"${item.get('job_min_salary', '')} - ${item.get('job_max_salary', '')}"
                                if item.get("job_min_salary")
                                else ""
                            ),
                            job_type=item.get("job_employment_type", "Full-time"),
                            remote=item.get("job_is_remote", False),
                            accessibility_note="",
                            posted_at=item.get("job_posted_at_datetime_utc", ""),
                        )
                    )
                return JobSearchResponse(
                    query=role,
                    location=location,
                    count=len(jobs),
                    jobs=jobs,
                    source="jsearch",
                )
        except Exception:
            pass  # Fall through to mock if API fails

    # Use mock data
    jobs = _mock_jobs(role, location, min(limit, 5))
    return JobSearchResponse(
        query=role,
        location=location,
        count=len(jobs),
        jobs=jobs,
        source="mock",
    )


def search_jobs_sync(
    role: str,
    location: str = "remote",
    limit: int = 5,
) -> dict:
    """
    Synchronous wrapper used by the ADK agent tool (ADK calls tools synchronously).
    Returns a plain dict suitable for the agent to read.
    """
    jobs = _mock_jobs(role, location, limit)
    return {
        "count": len(jobs),
        "jobs": [
            {
                "title": j.title,
                "company": j.company,
                "location": j.location,
                "salary": j.salary,
                "remote": j.remote,
                "accessibility_note": j.accessibility_note,
                "url": j.url,
            }
            for j in jobs
        ],
        "source": "mock",
    }
