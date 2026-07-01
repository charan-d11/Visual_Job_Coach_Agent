"""
orchestrator_agent.py
---------------------
The ROOT agent of the multi-agent system.

This is the core of the project's "multi-agent" design (key rubric concept).
It does NOT do the specialized work itself — instead it understands the user's
intent and DELEGATES to the correct specialist sub-agent using ADK's
'sub_agents' mechanism. ADK handles the routing/transfer automatically based
on each sub-agent's name + description.
"""

from google.adk.agents import LlmAgent

from app.services.llm_service import get_model_name
from app.utils.prompts import ORCHESTRATOR_PROMPT

# Import the four specialist agents
from app.agents.job_agent import job_agent
from app.agents.resume_agent import resume_agent
from app.agents.interview_agent import interview_agent
from app.agents.planner_agent import planner_agent

# The root orchestrator. Listing agents in `sub_agents` lets ADK delegate to them.
root_agent = LlmAgent(
    name="orchestrator_agent",
    model=get_model_name(),
    description="Root coordinator that routes user requests to specialist career agents.",
    instruction=ORCHESTRATOR_PROMPT,
    sub_agents=[
        job_agent,
        resume_agent,
        interview_agent,
        planner_agent,
    ],
)