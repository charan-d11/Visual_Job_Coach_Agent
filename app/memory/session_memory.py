"""
session_memory.py
-----------------
In-memory session store for conversation history.

Uses a simple dict keyed by session_id. In production this would be
replaced by Redis or a database, but for local/dev use this is fine.
"""

import uuid
from datetime import datetime
from typing import Optional

from app.models.session_model import Session, ChatMessage


# Module-level in-memory store
_sessions: dict[str, Session] = {}


def create_session(user_id: Optional[str] = None) -> Session:
    """Create a new session and return it."""
    session_id = str(uuid.uuid4())
    session = Session(session_id=session_id, user_id=user_id)
    _sessions[session_id] = session
    return session


def get_session(session_id: str) -> Optional[Session]:
    """Retrieve a session by ID. Returns None if not found."""
    return _sessions.get(session_id)


def get_or_create_session(session_id: Optional[str] = None, user_id: Optional[str] = None) -> Session:
    """Return existing session if valid ID provided, otherwise create new."""
    if session_id and session_id in _sessions:
        return _sessions[session_id]
    return create_session(user_id=user_id)


def add_message(session_id: str, role: str, content: str, agent: Optional[str] = None) -> bool:
    """Append a message to an existing session. Returns False if session not found."""
    session = _sessions.get(session_id)
    if not session:
        return False
    msg = ChatMessage(role=role, content=content, agent=agent)
    session.messages.append(msg)
    session.updated_at = datetime.utcnow().isoformat()
    return True


def get_history(session_id: str, limit: int = 20) -> list[ChatMessage]:
    """Return the last `limit` messages for a session."""
    session = _sessions.get(session_id)
    if not session:
        return []
    return session.messages[-limit:]


def delete_session(session_id: str) -> bool:
    """Delete a session. Returns True if it existed."""
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False


def list_sessions() -> list[str]:
    """Return all active session IDs."""
    return list(_sessions.keys())


def clear_all_sessions() -> None:
    """Clear all sessions (useful for testing)."""
    _sessions.clear()
