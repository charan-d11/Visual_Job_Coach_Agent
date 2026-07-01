"""
test_security.py
----------------
Tests for security modules: auth, input sanitizer, PII redaction, validators.
"""

import pytest
from app.security.input_sanitizer import sanitize_text, sanitize_role, is_safe_input
from app.security.pii_redaction import redact_pii, contains_pii
from app.utils.validators import validate_text, validate_role, validate_session_id


class TestInputSanitizer:
    def test_sanitize_text_strips_whitespace(self):
        result = sanitize_text("  hello world  ")
        assert result == "hello world"

    def test_sanitize_text_max_length(self):
        long_text = "a" * 3000
        result = sanitize_text(long_text, max_length=100)
        assert len(result) <= 100

    def test_sanitize_text_html_escape(self):
        result = sanitize_text("<script>alert('xss')</script>")
        assert "<script>" not in result

    def test_sanitize_role_removes_invalid_chars(self):
        result = sanitize_role("data entry!@#$%")
        assert "!" not in result
        assert "@" not in result

    def test_is_safe_input_detects_sql(self):
        assert not is_safe_input("SELECT * FROM users")
        assert not is_safe_input("DROP TABLE jobs")

    def test_is_safe_input_normal_text(self):
        assert is_safe_input("Find me a data entry job in New York")
        assert is_safe_input("Tell me about interview tips")


class TestPIIRedaction:
    def test_redact_email(self):
        result = redact_pii("Contact me at john.doe@example.com please.")
        assert "john.doe@example.com" not in result
        assert "[EMAIL REDACTED]" in result

    def test_redact_phone(self):
        result = redact_pii("Call me at 555-123-4567 anytime.")
        assert "555-123-4567" not in result
        assert "[PHONE REDACTED]" in result

    def test_redact_ssn(self):
        result = redact_pii("My SSN is 123-45-6789.")
        assert "123-45-6789" not in result
        assert "[SSN REDACTED]" in result

    def test_no_pii_unchanged(self):
        text = "I am looking for a data entry job."
        assert redact_pii(text) == text

    def test_contains_pii_true(self):
        assert contains_pii("My email is user@test.com")

    def test_contains_pii_false(self):
        assert not contains_pii("I want a remote job in accounting.")


class TestValidators:
    def test_validate_text_valid(self):
        valid, msg = validate_text("Hello world", min_length=1, max_length=100)
        assert valid is True
        assert msg == ""

    def test_validate_text_too_short(self):
        valid, msg = validate_text("", min_length=1)
        assert valid is False

    def test_validate_text_too_long(self):
        valid, msg = validate_text("a" * 200, max_length=100)
        assert valid is False

    def test_validate_role_valid(self):
        valid, msg = validate_role("Software Developer")
        assert valid is True

    def test_validate_role_with_invalid_chars(self):
        valid, msg = validate_role("job<script>alert()</script>")
        assert valid is False

    def test_validate_session_id_valid_uuid(self):
        valid, msg = validate_session_id("550e8400-e29b-41d4-a716-446655440000")
        assert valid is True

    def test_validate_session_id_invalid(self):
        valid, msg = validate_session_id("not-a-uuid")
        assert valid is False
