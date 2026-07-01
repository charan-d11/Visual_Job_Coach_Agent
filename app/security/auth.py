"""
auth.py
-------
Bearer token authentication for FastAPI endpoints.
Token is read from settings (set in .env as API_AUTH_TOKEN).

Usage:
    from app.security.auth import verify_token
    @router.get("/protected", dependencies=[Depends(verify_token)])
"""

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

_bearer_scheme = HTTPBearer(auto_error=False)


def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(_bearer_scheme),
) -> str:
    """
    FastAPI dependency that validates a Bearer token.
    Raises 401 if token is missing or wrong.
    Returns the token string if valid.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header. Use 'Bearer <token>'.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if credentials.credentials != settings.api_auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


def optional_token(
    credentials: HTTPAuthorizationCredentials = Security(_bearer_scheme),
) -> str | None:
    """
    FastAPI dependency that optionally validates a Bearer token.
    Returns the token if valid, None if missing — does NOT raise on missing.
    """
    if credentials is None:
        return None
    if credentials.credentials == settings.api_auth_token:
        return credentials.credentials
    return None
