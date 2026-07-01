"""
job_model.py
------------
Pydantic models for job search requests and responses.
"""

from typing import Optional
from pydantic import BaseModel, Field


class Job(BaseModel):
    """A single job listing."""
    id: str = ""
    title: str
    company: str
    location: str
    description: str = ""
    url: str = ""
    salary: str = ""
    job_type: str = "Full-time"
    remote: bool = False
    accessibility_note: str = ""
    posted_at: str = ""


class JobSearchRequest(BaseModel):
    """Request body for searching jobs."""
    role: str = Field(..., min_length=1, max_length=200, description="Job title or role to search for")
    location: str = Field(default="remote", max_length=100, description="Preferred location")
    remote_only: bool = Field(default=False, description="Only show remote jobs")
    job_type: Optional[str] = Field(default=None, description="e.g. full-time, part-time, contract")
    limit: int = Field(default=10, ge=1, le=50, description="Number of results to return")


class JobSearchResponse(BaseModel):
    """Response for a job search query."""
    query: str
    location: str
    count: int
    jobs: list[Job]
    source: str = "mock"  # "mock" or "jsearch"
