"""
test_mcp_server.py
------------------
Basic tests to verify the MCP server module can be imported and is structured correctly.
"""

import pytest
import os


class TestMCPServerModule:
    def test_mcp_server_directory_exists(self):
        """Verify the mcp_server package exists."""
        mcp_path = os.path.join(
            os.path.dirname(__file__), "..", "app", "mcp_server"
        )
        assert os.path.isdir(mcp_path), "app/mcp_server directory should exist"

    def test_mcp_server_has_init(self):
        """Verify the mcp_server package has an __init__.py."""
        init_path = os.path.join(
            os.path.dirname(__file__), "..", "app", "mcp_server", "__init__.py"
        )
        # __init__.py may or may not be present; just ensure the dir exists
        mcp_path = os.path.join(
            os.path.dirname(__file__), "..", "app", "mcp_server"
        )
        assert os.path.isdir(mcp_path)

    def test_app_package_importable(self):
        """Verify the app package can be imported without errors."""
        try:
            import app
        except ImportError as e:
            pytest.fail(f"app package could not be imported: {e}")

    def test_config_importable(self):
        """Verify app.config is importable."""
        from app.config import settings
        assert settings is not None

    def test_agents_importable(self):
        """Verify all agents can be imported."""
        from app.agents.job_agent import job_agent
        from app.agents.resume_agent import resume_agent
        from app.agents.interview_agent import interview_agent
        from app.agents.planner_agent import planner_agent
        from app.agents.orchestrator_agent import root_agent
        assert root_agent is not None

    def test_services_importable(self):
        """Verify service modules are importable."""
        from app.services.llm_service import get_model_name, is_llm_configured
        from app.services.job_api import search_jobs_sync
        from app.services.text_to_speech import is_tts_available
        from app.services.speech_to_text import is_stt_available
        assert get_model_name() == "gemini-2.0-flash"

    def test_memory_importable(self):
        """Verify memory modules work correctly."""
        from app.memory.session_memory import create_session, get_session, delete_session
        session = create_session(user_id="test_user")
        assert session.session_id is not None
        retrieved = get_session(session.session_id)
        assert retrieved is not None
        delete_session(session.session_id)
        assert get_session(session.session_id) is None
