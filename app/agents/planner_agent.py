"""
planner_agent.py
----------------
The Career Planner specialist agent (ADK LlmAgent).
Breaks the job hunt into clear, ordered, achievable steps.
"""

from google.adk.agents import LlmAgent

from app.services.llm_service import get_model_name
from app.utils.prompts import PLANNER_AGENT_PROMPT


def create_action_plan(goal: str, days: int = 7) -> dict:
    """
    Create a simple step-by-step job-hunt plan.

    Args:
        goal: The user's goal (e.g., "get a remote data entry job").
        days: Number of days to spread the plan over (default 7).

    Returns:
        A dict containing ordered daily steps.
    """
    # A basic template plan; the agent will personalize it in conversation.
    steps = [
        "Define target roles and update your resume.",
        "Search and save 5 suitable job openings.",
        "Tailor your resume to 2 of those openings.",
        "Practice 3 common interview questions out loud.",
        "Apply to 3 jobs.",
        "Follow up on applications and network with 1 contact.",
        "Review progress and plan next week.",
    ]
    plan = [{"day": i + 1, "task": steps[i % len(steps)]} for i in range(days)]
    return {"goal": goal, "duration_days": days, "plan": plan}


planner_agent = LlmAgent(
    name="planner_agent",
    model=get_model_name(),
    description="Builds and tracks a step-by-step job-search plan.",
    instruction=PLANNER_AGENT_PROMPT,
    tools=[create_action_plan],
)