"""
test_routes.py
--------------
FastAPI route tests using TestClient. Tests all major endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestSystemEndpoints:
    def test_root_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "running"

    def test_health_returns_healthy(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"

    def test_docs_accessible(self):
        r = client.get("/docs")
        assert r.status_code == 200


class TestJobRoutes:
    def test_search_jobs_basic(self):
        r = client.post("/api/jobs/search", json={"role": "data entry", "location": "remote"})
        assert r.status_code == 200
        data = r.json()
        assert "jobs" in data
        assert data["count"] >= 0

    def test_search_jobs_missing_role_fails(self):
        r = client.post("/api/jobs/search", json={"location": "remote"})
        assert r.status_code == 422  # Pydantic validation error

    def test_suggest_jobs(self):
        r = client.get("/api/jobs/suggest?keywords=data")
        assert r.status_code == 200
        data = r.json()
        assert "suggestions" in data
        assert len(data["suggestions"]) > 0


class TestResumeRoutes:
    def test_format_section_success(self):
        r = client.post("/api/resume/format", json={
            "section_name": "Skills",
            "content": "Python, Excel, Data Entry, Communication",
        })
        assert r.status_code == 200
        data = r.json()
        assert "formatted_text" in data
        assert "SKILLS" in data["formatted_text"].upper()

    def test_format_section_empty_content_fails(self):
        r = client.post("/api/resume/format", json={
            "section_name": "Skills",
            "content": "",
        })
        assert r.status_code in (400, 422)

    def test_list_sections(self):
        r = client.get("/api/resume/sections")
        assert r.status_code == 200
        data = r.json()
        assert "sections" in data
        assert len(data["sections"]) > 0


class TestInterviewRoutes:
    def test_get_questions_success(self):
        r = client.get("/api/interview/questions/customer service")
        assert r.status_code == 200
        data = r.json()
        assert "questions" in data
        assert data["count"] > 0

    def test_get_questions_general_role(self):
        r = client.get("/api/interview/questions/unknown role")
        assert r.status_code == 200
        assert "questions" in r.json()

    def test_interview_feedback_success(self):
        r = client.post("/api/interview/feedback", json={
            "role": "customer service",
            "question": "Tell me about yourself.",
            "answer": "I have worked in customer service for 3 years. In my last role, I managed 50 calls per day and achieved a 95% satisfaction rating. I love helping people solve problems.",
        })
        assert r.status_code == 200
        data = r.json()
        assert "strengths" in data
        assert "improvements" in data
        assert "star_used" in data

    def test_interview_feedback_short_answer(self):
        r = client.post("/api/interview/feedback", json={
            "role": "admin",
            "question": "Why do you want this job?",
            "answer": "I need the money.",
        })
        assert r.status_code == 200
        data = r.json()
        assert "improvements" in data
        assert len(data["improvements"]) > 0


class TestVoiceRoutes:
    def test_voice_status(self):
        r = client.get("/api/voice/status")
        assert r.status_code == 200
        data = r.json()
        assert "text_to_speech" in data
        assert "speech_to_text" in data

    def test_speak_text_returns_audio_or_error(self):
        r = client.post("/api/voice/speak", json={"text": "Hello, this is a test."})
        # Either returns audio (200) or service unavailable (503) — both acceptable
        assert r.status_code in (200, 503)
        if r.status_code == 200:
            assert r.headers["content-type"] == "audio/mpeg"

    def test_speak_empty_text_fails(self):
        r = client.post("/api/voice/speak", json={"text": "   "})
        assert r.status_code in (400, 503)


class TestSessionEndpoints:
    def test_get_nonexistent_session(self):
        r = client.get("/api/session/00000000-0000-0000-0000-000000000000")
        assert r.status_code == 404

    def test_delete_nonexistent_session(self):
        r = client.delete("/api/session/00000000-0000-0000-0000-000000000000")
        assert r.status_code == 404
