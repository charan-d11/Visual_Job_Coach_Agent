"""
session_model.py
----------------
Pydantic models for chat sessions and messages.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in a conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    agent: Optional[str] = None  # Which sub-agent responded (e.g. "job_agent")


class ChatRequest(BaseModel):
    """Request body for sending a chat message."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    session_id: Optional[str] = Field(default=None, description="Session ID for conversation continuity")
    user_id: Optional[str] = Field(default=None, description="Optional user identifier")


class ChatResponse(BaseModel):
    """Response from the AI agent."""
    reply: str
    session_id: str
    agent_used: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Session(BaseModel):
    """A conversation session with history."""
    session_id: str
    user_id: Optional[str] = None
    messages: list[ChatMessage] = []
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    active: bool = True
