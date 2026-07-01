"""
validators.py
-------------
Input validation helpers used by routes and services.
"""

import re
from typing import Optional


def validate_text(text: str, min_length: int = 1, max_length: int = 2000) -> tuple[bool, str]:
    """
    Validate a text string.

    Returns:
        (is_valid, error_message). error_message is empty if valid.
    """
    if not isinstance(text, str):
        return False, "Input must be a string."
    if len(text.strip()) < min_length:
        return False, f"Text must be at least {min_length} character(s) long."
    if len(text) > max_length:
        return False, f"Text must not exceed {max_length} characters."
    return True, ""


def validate_role(role: str) -> tuple[bool, str]:
    """Validate a job role string."""
    valid, msg = validate_text(role, min_length=2, max_length=200)
    if not valid:
        return False, msg
    if re.search(r"[<>{}\[\]\\|]", role):
        return False, "Job role contains invalid characters."
    return True, ""


def validate_location(location: str) -> tuple[bool, str]:
    """Validate a location string."""
    valid, msg = validate_text(location, min_length=2, max_length=100)
    if not valid:
        return False, msg
    return True, ""


def validate_session_id(session_id: str) -> tuple[bool, str]:
    """Validate a UUID-style session ID."""
    uuid_pattern = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        re.IGNORECASE,
    )
    if not uuid_pattern.match(session_id):
        return False, "Invalid session ID format."
    return True, ""


def validate_audio_upload(content_type: str, size_bytes: int, max_mb: float = 10.0) -> tuple[bool, str]:
    """
    Validate an uploaded audio file.

    Args:
        content_type: MIME type (e.g. 'audio/wav').
        size_bytes: Size of the upload in bytes.
        max_mb: Maximum allowed size in MB.
    """
    allowed_types = {"audio/wav", "audio/wave", "audio/x-wav", "audio/mpeg", "audio/mp3", "audio/flac", "audio/ogg"}
    if content_type not in allowed_types:
        return False, f"Unsupported audio format: {content_type}. Supported: WAV, MP3, FLAC, OGG."
    max_bytes = int(max_mb * 1024 * 1024)
    if size_bytes > max_bytes:
        return False, f"Audio file too large. Maximum size: {max_mb} MB."
    if size_bytes == 0:
        return False, "Audio file is empty."
    return True, ""


def validate_user_id(user_id: str) -> tuple[bool, str]:
    """Validate a user ID (alphanumeric with hyphens/underscores)."""
    if not re.match(r"^[a-zA-Z0-9_\-]{3,64}$", user_id):
        return False, "User ID must be 3-64 characters, alphanumeric with hyphens/underscores only."
    return True, ""
