"""
resume_routes.py
----------------
FastAPI routes for resume building.

Endpoints:
  POST /api/resume/format   — format a resume section
  GET  /api/resume/sections — list available resume sections
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.security.input_sanitizer import sanitize_text

router = APIRouter(prefix="/api/resume", tags=["Resume"])


class ResumeSectionRequest(BaseModel):
    section_name: str = Field(..., min_length=1, max_length=50, description="e.g. 'Experience', 'Skills'")
    content: str = Field(..., min_length=1, max_length=3000, description="Raw text for the section")
    user_id: str | None = Field(default=None, description="Optional user ID to save the section")


class ResumeSectionResponse(BaseModel):
    section: str
    formatted_text: str
    word_count: int
    tips: list[str]


RESUME_SECTIONS = [
    "Contact Information",
    "Professional Summary",
    "Work Experience",
    "Education",
    "Skills",
    "Certifications",
    "Volunteer Work",
    "Projects",
    "Languages",
    "References",
]

SECTION_TIPS = {
    "work experience": [
        "Use action verbs like 'managed', 'developed', 'improved'.",
        "Include measurable results where possible (e.g. 'increased efficiency by 20%').",
        "List most recent experience first.",
    ],
    "skills": [
        "Group skills by category (e.g. Technical, Communication, Tools).",
        "Only list skills you're comfortable being asked about in an interview.",
        "Include assistive technology skills if relevant (e.g. JAWS, NVDA, Dragon NaturallySpeaking).",
    ],
    "professional summary": [
        "Keep it to 3-4 sentences.",
        "Highlight your most relevant experience and key strength.",
        "Tailor it to each job application.",
    ],
    "education": [
        "List degree, institution, and graduation year.",
        "Include relevant coursework or academic achievements if less than 5 years of experience.",
    ],
}

DEFAULT_TIPS = [
    "Keep content clear and concise.",
    "Use plain language that is easy to understand.",
    "Proofread for spelling and grammar.",
]


@router.post("/format", response_model=ResumeSectionResponse, summary="Format a resume section")
async def format_resume_section(request: ResumeSectionRequest) -> ResumeSectionResponse:
    """
    Format raw text into a clean, accessible resume section.

    - **section_name**: Which section (e.g. 'Work Experience', 'Skills')
    - **content**: Your raw notes/text for that section
    """
    section = sanitize_text(request.section_name, max_length=50).strip()
    content = sanitize_text(request.content, max_length=3000).strip()

    if not section:
        raise HTTPException(status_code=400, detail="Section name cannot be empty.")
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty.")

    # Format with clear header and cleaned content
    formatted = f"{section.upper()}\n{'—' * len(section)}\n{content}"

    # Get relevant tips
    section_lower = section.lower()
    tips = SECTION_TIPS.get(section_lower, DEFAULT_TIPS)

    word_count = len(content.split())

    # Optionally save to user profile
    if request.user_id:
        try:
            from app.memory.user_memory import load_profile, save_profile
            profile = load_profile(request.user_id)
            if profile:
                profile.resume_sections[section] = formatted
                save_profile(profile)
        except Exception:
            pass  # Don't fail if profile save fails

    return ResumeSectionResponse(
        section=section,
        formatted_text=formatted,
        word_count=word_count,
        tips=tips,
    )


@router.get("/sections", summary="List available resume sections")
async def list_sections() -> dict:
    """Return the list of standard resume sections."""
    return {
        "sections": RESUME_SECTIONS,
        "count": len(RESUME_SECTIONS),
    }
