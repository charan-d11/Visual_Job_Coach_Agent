"""
interview_agent.py
------------------
The Interview Coach specialist agent (ADK LlmAgent).
Provides practice questions, tips, and mock interviews.
"""

from google.adk.agents import LlmAgent

from app.services.llm_service import get_model_name
from app.utils.prompts import INTERVIEW_AGENT_PROMPT


def get_practice_questions(role: str) -> dict:
    """
    Return common interview questions for a given role.

    Args:
        role: The target job role (e.g., "customer support").

    Returns:
        A dict with a list of practice questions.
    """
    # TODO (Phase 5): load from data/questions.json for a richer question bank.
    questions = [
        f"Tell me about yourself and why you're interested in a {role} role.",
        "Describe a challenge you overcame at work or in your studies.",
        "What are your biggest strengths, and how do they fit this job?",
        "Where do you see yourself in a few years?",
    ]
    return {"role": role, "count": len(questions), "questions": questions}


interview_agent = LlmAgent(
    name="interview_agent",
    model=get_model_name(),
    description="Coaches the user for job interviews with questions and feedback.",
    instruction=INTERVIEW_AGENT_PROMPT,
    tools=[get_practice_questions],
)