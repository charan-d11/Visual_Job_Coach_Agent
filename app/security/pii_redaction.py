"""
pii_redaction.py
----------------
Regex-based PII (Personally Identifiable Information) redaction.
Used to scrub sensitive data from logs and stored conversation history.
"""

import re

# Regex patterns for common PII
_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    "phone_us": re.compile(r"\b(\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}\b"),
    "phone_intl": re.compile(r"\+\d{1,3}[\s.\-]?\d{2,4}[\s.\-]?\d{4,10}"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d{4}[\s\-]?){3}\d{4}\b"),
    "ip_address": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
}

_REPLACEMENTS = {
    "email": "[EMAIL REDACTED]",
    "phone_us": "[PHONE REDACTED]",
    "phone_intl": "[PHONE REDACTED]",
    "ssn": "[SSN REDACTED]",
    "credit_card": "[CARD REDACTED]",
    "ip_address": "[IP REDACTED]",
}


def redact_pii(text: str) -> str:
    """
    Remove PII from text by replacing it with placeholder tokens.

    Args:
        text: Input string that may contain PII.

    Returns:
        Text with PII replaced by placeholder tokens.
    """
    if not isinstance(text, str):
        return text
    for pii_type, pattern in _PATTERNS.items():
        text = pattern.sub(_REPLACEMENTS[pii_type], text)
    return text


def contains_pii(text: str) -> bool:
    """
    Quick check: returns True if the text likely contains PII.
    Useful for deciding whether to log or store a message.
    """
    for pattern in _PATTERNS.values():
        if pattern.search(text):
            return True
    return False


def redact_dict(data: dict) -> dict:
    """
    Recursively redact PII from all string values in a dict.
    Useful for sanitizing log entries.
    """
    result = {}
    for key, value in data.items():
        if isinstance(value, str):
            result[key] = redact_pii(value)
        elif isinstance(value, dict):
            result[key] = redact_dict(value)
        elif isinstance(value, list):
            result[key] = [
                redact_pii(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            result[key] = value
    return result
