"""
speech_to_text.py
-----------------
Converts audio input (bytes or file path) to text using SpeechRecognition.
Uses Google Web Speech API by default (free, no key needed for basic use).
"""

import io
import os
import tempfile
from typing import Optional

try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False


def transcribe_audio_bytes(audio_bytes: bytes, sample_rate: int = 16000) -> dict:
    """
    Transcribe raw audio bytes to text.

    Args:
        audio_bytes: Raw audio data (WAV format preferred).
        sample_rate: Sample rate of the audio in Hz.

    Returns:
        dict with 'text' (transcription) and 'success' (bool).
    """
    if not _SR_AVAILABLE:
        return {
            "success": False,
            "text": "",
            "error": "SpeechRecognition library not installed. Run: pip install SpeechRecognition",
        }

    try:
        recognizer = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return {"success": True, "text": text, "error": None}
    except sr.UnknownValueError:
        return {"success": False, "text": "", "error": "Could not understand the audio."}
    except sr.RequestError as e:
        return {"success": False, "text": "", "error": f"Speech recognition service error: {e}"}
    except Exception as e:
        return {"success": False, "text": "", "error": f"Transcription failed: {e}"}


def transcribe_audio_file(file_path: str) -> dict:
    """
    Transcribe audio from a file path.

    Args:
        file_path: Path to audio file (WAV, AIFF, FLAC supported).

    Returns:
        dict with 'text' and 'success'.
    """
    if not _SR_AVAILABLE:
        return {"success": False, "text": "", "error": "SpeechRecognition not installed."}

    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return {"success": True, "text": text, "error": None}
    except Exception as e:
        return {"success": False, "text": "", "error": str(e)}


def is_stt_available() -> bool:
    """Check if speech-to-text is available."""
    return _SR_AVAILABLE
