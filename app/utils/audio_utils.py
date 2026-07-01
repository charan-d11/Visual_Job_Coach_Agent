"""
audio_utils.py
--------------
Helpers for audio file handling: saving, loading, and format info.
"""

import os
import tempfile
from typing import Optional


def save_audio_bytes(audio_bytes: bytes, suffix: str = ".mp3", directory: Optional[str] = None) -> str:
    """
    Save audio bytes to a temporary file.

    Args:
        audio_bytes: Raw audio data.
        suffix: File extension (e.g. '.mp3', '.wav').
        directory: Directory to save in; defaults to system temp dir.

    Returns:
        Absolute path to the saved file.
    """
    fd, path = tempfile.mkstemp(suffix=suffix, dir=directory)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(audio_bytes)
    except Exception:
        os.close(fd)
        raise
    return path


def load_audio_bytes(file_path: str) -> bytes:
    """
    Load audio bytes from a file.

    Args:
        file_path: Path to the audio file.

    Returns:
        Raw audio bytes.
    """
    with open(file_path, "rb") as f:
        return f.read()


def get_audio_info(file_path: str) -> dict:
    """
    Return basic info about an audio file.

    Args:
        file_path: Path to the audio file.

    Returns:
        Dict with 'path', 'size_bytes', 'extension'.
    """
    return {
        "path": file_path,
        "size_bytes": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
        "extension": os.path.splitext(file_path)[1].lower(),
        "exists": os.path.exists(file_path),
    }


def cleanup_temp_file(file_path: str) -> bool:
    """Delete a temporary audio file. Returns True if deleted."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def is_valid_audio_size(audio_bytes: bytes, max_mb: float = 10.0) -> bool:
    """Check if audio bytes are within the allowed size limit."""
    max_bytes = int(max_mb * 1024 * 1024)
    return len(audio_bytes) <= max_bytes
