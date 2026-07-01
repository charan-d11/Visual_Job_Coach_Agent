"""
llm_service.py
--------------
Configures the underlying Large Language Model (Google Gemini) used by all agents.

Design note:
- We define the model name in ONE place so every agent stays consistent.
- The actual API key is read from settings (.env), never hardcoded.
"""

from app.config import settings

# The Gemini model all agents will use.
# gemini-2.0-flash is fast and cost-effective — good for a responsive voice assistant.
DEFAULT_MODEL = "gemini-2.0-flash"


def get_model_name() -> str:
    """Return the model name used across all agents."""
    return DEFAULT_MODEL


def is_llm_configured() -> bool:
    """
    Quick check that an API key exists.
    Helps us fail early with a clear message instead of a confusing API error.
    """
    return bool(settings.google_api_key)