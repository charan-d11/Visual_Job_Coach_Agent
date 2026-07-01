"""
test_agents.py
--------------
Unit tests for agent tool functions.
These test the tool logic directly — no LLM API calls needed.
"""

import pytest
from app.agents.job_agent import search_jobs, get_job_tips
from app.agents.resume_agent import format_resume_section
from app.agents.interview_agent import get_practice_questions
from app.agents.planner_agent import create_action_plan


class TestJobAgent:
    def test_search_jobs_returns_results(self):
        result = search_jobs(role="data entry", location="remote")
        assert "count" in result
        assert "jobs" in result
        assert result["count"] > 0

    def test_search_jobs_contains_required_fields(self):
        result = search_jobs(role="software developer", location="new york")
        for job in result["jobs"]:
            assert "title" in job
            assert "company" in job
            assert "location" in job

    def test_search_jobs_default_location(self):
        result = search_jobs(role="customer service")
        assert result["count"] > 0

    def test_get_job_tips_returns_tips(self):
        result = get_job_tips(role="data entry")
        assert "tips" in result
        assert len(result["tips"]) > 0

    def test_get_job_tips_general_role(self):
        result = get_job_tips(role="unknown role xyz")
        assert "tips" in result


class TestResumeAgent:
    def test_format_resume_section_basic(self):
        result = format_resume_section(section_name="Skills", content="Python, Excel, Communication")
        assert "section" in result
        assert "formatted_text" in result
        assert "SKILLS" in result["formatted_text"].upper()

    def test_format_resume_section_experience(self):
        result = format_resume_section(
            section_name="Work Experience",
            content="Worked as data entry clerk at ABC Corp for 2 years."
        )
        assert result["section"] == "Work Experience"
        assert "WORK EXPERIENCE" in result["formatted_text"].upper()

    def test_format_resume_content_included(self):
        content = "I have 5 years of experience in customer service."
        result = format_resume_section(section_name="Summary", content=content)
        assert content.strip() in result["formatted_text"]


class TestInterviewAgent:
    def test_get_practice_questions_returns_questions(self):
        result = get_practice_questions(role="customer support")
        assert "questions" in result
        assert result["count"] > 0
        assert len(result["questions"]) > 0

    def test_get_practice_questions_are_strings(self):
        result = get_practice_questions(role="data entry")
        for q in result["questions"]:
            assert isinstance(q, str)
            assert len(q) > 10

    def test_get_practice_questions_role_included(self):
        result = get_practice_questions(role="software engineer")
        assert result["role"] == "software engineer"


class TestPlannerAgent:
    def test_create_action_plan_default_days(self):
        result = create_action_plan(goal="get a remote job")
        assert "plan" in result
        assert result["duration_days"] == 7
        assert len(result["plan"]) == 7

    def test_create_action_plan_custom_days(self):
        result = create_action_plan(goal="find data entry work", days=3)
        assert result["duration_days"] == 3
        assert len(result["plan"]) == 3

    def test_create_action_plan_has_goal(self):
        goal = "become a software developer"
        result = create_action_plan(goal=goal)
        assert result["goal"] == goal

    def test_plan_has_day_and_task(self):
        result = create_action_plan(goal="test goal", days=2)
        for day_plan in result["plan"]:
            assert "day" in day_plan
            assert "task" in day_plan
