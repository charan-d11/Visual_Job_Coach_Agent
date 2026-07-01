"""
main.py
-------
FastAPI application entry point for the Visual Job Coach Agent.

This file:
- Creates the FastAPI app
- Applies security middleware (rate limiting)
- Registers all route modules
- Exposes /health and /api/chat endpoints
"""

import os
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.security.rate_limiter import limiter, rate_limit_handler

# ----- Route imports -----
from app.routes import job_routes, resume_routes, interview_routes, voice_routes

# ----- Model imports -----
from app.models.session_model import ChatRequest, ChatResponse

# ----- Memory imports -----
from app.memory import session_memory

# Create the FastAPI app with accessibility-focused metadata
app = FastAPI(
    title="Visual Job Coach Agent",
    description=(
        "A voice-first, multi-agent career assistant for visually impaired "
        "job seekers. Helps with job search, resume building, interview prep, "
        "and career planning. Powered by Google Gemini via Google ADK."
    ),
    version="1.0.0",
)

# ----- Rate limiter -----
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# ----- CORS -----
# In production, restrict allow_origins to your real frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Register routers -----
app.include_router(job_routes.router)
app.include_router(resume_routes.router)
app.include_router(interview_routes.router)
app.include_router(voice_routes.router)


# ----- Core endpoints -----

@app.get("/", tags=["System"])
def root():
    """Landing endpoint with app info."""
    return {
        "app": "Visual Job Coach Agent",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "chat": "/api/chat",
    }


@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint.
    Used by deployment platforms (Docker healthcheck, Cloud Run, etc.)
    """
    return {
        "status": "healthy",
        "env": settings.app_env,
        "llm_configured": bool(settings.google_api_key),
    }


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main conversational endpoint. Send a text message and get an AI response.

    The orchestrator agent will route your request to the appropriate specialist:
    - Job searching → job_agent
    - Resume help → resume_agent
    - Interview prep → interview_agent
    - Career planning → planner_agent

    Provide a `session_id` to continue a conversation. If omitted, a new session is created.
    """
    if not settings.google_api_key:
        raise HTTPException(
            status_code=503,
            detail="Google API key not configured. Set GOOGLE_API_KEY in your .env file.",
        )

    from app.security.input_sanitizer import sanitize_text, is_safe_input

    message = sanitize_text(request.message, max_length=2000)
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    if not is_safe_input(message):
        raise HTTPException(status_code=400, detail="Message contains invalid content.")

    # Get or create session
    session = session_memory.get_or_create_session(
        session_id=request.session_id,
        user_id=request.user_id,
    )

    # Record user message
    session_memory.add_message(session.session_id, role="user", content=message)

    # Call the ADK orchestrator agent
    try:
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
        import google.generativeai as genai
        genai.configure(api_key=settings.google_api_key)

        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai.types import Content, Part

        from app.agents.orchestrator_agent import root_agent

        session_service = InMemorySessionService()
        runner = Runner(
            agent=root_agent,
            app_name="visual_job_coach",
            session_service=session_service,
        )

        adk_session = await session_service.create_session(
            app_name="visual_job_coach",
            user_id=request.user_id or "anonymous",
        )

        user_content = Content(role="user", parts=[Part(text=message)])
        reply_text = ""
        agent_used = None

        async for event in runner.run_async(
            user_id=request.user_id or "anonymous",
            session_id=adk_session.id,
            new_message=user_content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        reply_text += part.text
                if hasattr(event, "author"):
                    agent_used = event.author

    except Exception as e:
        # Graceful fallback if ADK runner fails
        reply_text = (
            f"I'm sorry, I encountered an issue processing your request. "
            f"Please check that your Google API key is valid. Error: {str(e)[:200]}"
        )
        agent_used = "error_handler"

    if not reply_text:
        reply_text = "I didn't receive a response. Please try again."

    # Record assistant message
    session_memory.add_message(
        session.session_id,
        role="assistant",
        content=reply_text,
        agent=agent_used,
    )

    return ChatResponse(
        reply=reply_text,
        session_id=session.session_id,
        agent_used=agent_used,
    )


@app.get("/api/session/{session_id}", tags=["Chat"])
def get_session(session_id: str):
    """Retrieve conversation history for a session."""
    session = session_memory.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {
        "session_id": session.session_id,
        "message_count": len(session.messages),
        "messages": [m.model_dump() for m in session.messages],
        "created_at": session.created_at,
    }


@app.delete("/api/session/{session_id}", tags=["Chat"])
def delete_session(session_id: str):
    """Delete a conversation session."""
    deleted = session_memory.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"deleted": True, "session_id": session_id}