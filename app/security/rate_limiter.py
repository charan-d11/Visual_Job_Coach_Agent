"""
rate_limiter.py
---------------
SlowAPI rate limiting setup for FastAPI.

Usage in main.py:
    from app.security.rate_limiter import limiter, rate_limit_handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
"""

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import Request
from fastapi.responses import JSONResponse

from app.config import settings

# Create limiter instance — uses client IP as the key
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.rate_limit_per_minute}/minute"])


async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Custom 429 response when rate limit is exceeded."""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": f"Too many requests. Limit: {settings.rate_limit_per_minute} per minute.",
            "retry_after_seconds": 60,
        },
    )
