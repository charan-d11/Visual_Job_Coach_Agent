"""
resume_agent.py
---------------
The Resume specialist agent (ADK LlmAgent).
Helps the user build or improve a resume through conversation.
"""

from google.adk.agents import LlmAgent

from app.services.llm_service import get_model_name
from app.utils.prompts import RESUME_AGENT_PROMPT


def format_resume_section(section_name: str, content: str) -> dict:
    """
    Format a resume section into clean, accessible plain text.

    Args:
        section_name: e.g., "Experience", "Skills", "Education".
        content: The raw text the user provided for that section.

    Returns:
        A dict with the nicely formatted section.
    """
    # Simple, screen-reader-friendly formatting (no fancy visual markup).
    formatted = f"{section_name.upper()}\n{content.strip()}"
    return {"section": section_name, "formatted_text": formatted}


resume_agent = LlmAgent(
    name="resume_agent",
    model=get_model_name(),
    description="Helps create and improve the user's resume.",
    instruction=RESUME_AGENT_PROMPT,
    tools=[format_resume_section],
)