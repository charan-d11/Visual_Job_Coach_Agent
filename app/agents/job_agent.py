"""
job_agent.py
------------
The Job Search specialist agent (ADK LlmAgent).
Uses the real job_api service for richer results.
"""

from google.adk.agents import LlmAgent

from app.services.llm_service import get_model_name
from app.services.job_api import search_jobs_sync
from app.utils.prompts import JOB_AGENT_PROMPT


def search_jobs(role: str, location: str = "remote") -> dict:
    """
    Search for job openings matching a role and location.

    Args:
        role: The job title or role the user wants (e.g., "data entry").
        location: Preferred location, defaults to "remote".

    Returns:
        A dict with a list of matching jobs including title, company, location, salary, and accessibility notes.
    """
    return search_jobs_sync(role=role, location=location, limit=5)


def get_job_tips(role: str) -> dict:
    """
    Return job search tips tailored to the given role for visually impaired job seekers.

    Args:
        role: The job role being searched (e.g., "customer service").

    Returns:
        A dict with practical job search tips.
    """
    general_tips = [
        "Search on LinkedIn, Indeed, and Abledata for accessible employer listings.",
        "Look for employers with explicit disability inclusion policies.",
        "Contact the employer's HR to ask about screen reader compatibility before applying.",
        "Consider reaching out to vocational rehabilitation services in your area for support.",
        "Network through blind/visually impaired professional associations.",
    ]
    role_tips = {
        "data entry": ["Ensure the employer's system is compatible with JAWS or NVDA."],
        "customer service": ["Ask if calls use accessible CRM software."],
        "software": ["Mention your experience with assistive tech — it's a differentiator."],
    }
    role_lower = role.lower()
    specific = next((v for k, v in role_tips.items() if k in role_lower), [])
    all_tips = specific + general_tips
    return {"role": role, "tips": all_tips[:5], "count": 5}


# Define the agent with both tools
job_agent = LlmAgent(
    name="job_agent",
    model=get_model_name(),
    description="Finds and summarizes job openings for the user.",
    instruction=JOB_AGENT_PROMPT,
    tools=[search_jobs, get_job_tips],
)