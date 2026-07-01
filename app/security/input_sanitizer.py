"""
input_sanitizer.py
------------------
Input sanitization helpers to strip dangerous content before passing
user input to LLM agents or storing it.
"""

import re
import html

MAX_TEXT_LENGTH = 2000  # characters
MAX_NAME_LENGTH = 100


def sanitize_text(text: str, max_length: int = MAX_TEXT_LENGTH) -> str:
    """
    Sanitize free-form text input:
    - Strip leading/trailing whitespace
    - Collapse multiple spaces/newlines
    - Truncate to max_length
    - HTML-escape to prevent injection
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.strip()
    text = re.sub(r"\s{3,}", "  ", text)      # collapse 3+ whitespace to 2
    text = html.escape(text)                  # prevent HTML injection
    return text[:max_length]


def sanitize_name(name: str) -> str:
    """Sanitize a name field — only allow letters, spaces, hyphens, apostrophes."""
    if not isinstance(name, str):
        name = str(name)
    name = name.strip()
    # Keep only safe name characters
    name = re.sub(r"[^a-zA-Z\s\-\']", "", name)
    return name[:MAX_NAME_LENGTH]


def sanitize_location(location: str) -> str:
    """Sanitize a location string."""
    if not isinstance(location, str):
        location = str(location)
    location = location.strip()
    location = re.sub(r"[^a-zA-Z0-9\s,\-\.]", "", location)
    return location[:100]


def sanitize_role(role: str) -> str:
    """Sanitize a job role string."""
    if not isinstance(role, str):
        role = str(role)
    role = role.strip()
    role = re.sub(r"[^a-zA-Z0-9\s\-\+\/\#]", "", role)
    return role[:200]


def is_safe_input(text: str) -> bool:
    """
    Quick check: returns False if input contains obvious injection patterns.
    Not a replacement for proper sanitization but a fast first filter.
    """
    dangerous_patterns = [
        r"<script",
        r"javascript:",
        r"on\w+\s*=",
        r"DROP TABLE",
        r"SELECT \* FROM",
        r"INSERT INTO",
        r"--\s*$",
    ]
    text_lower = text.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return False
    return True
