"""
text_to_speech.py
-----------------
Converts text to audio using gTTS (Google Text-to-Speech).
Returns audio as bytes so it can be streamed directly in API responses.
"""

import io

try:
    from gtts import gTTS
    _GTTS_AVAILABLE = True
except ImportError:
    _GTTS_AVAILABLE = False


def text_to_speech_bytes(
    text: str,
    lang: str = "en",
    slow: bool = False,
) -> dict:
    """
    Convert text to MP3 audio bytes using gTTS.

    Args:
        text: The text to convert to speech.
        lang: Language code (e.g., 'en', 'es', 'fr').
        slow: If True, speak more slowly.

    Returns:
        dict with 'audio_bytes' (bytes), 'success' (bool), 'error' (str or None).
    """
    if not _GTTS_AVAILABLE:
        return {
            "success": False,
            "audio_bytes": b"",
            "error": "gTTS not installed. Run: pip install gTTS",
        }

    if not text or not text.strip():
        return {
            "success": False,
            "audio_bytes": b"",
            "error": "No text provided.",
        }

    try:
        tts = gTTS(text=text.strip(), lang=lang, slow=slow)
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return {
            "success": True,
            "audio_bytes": buffer.read(),
            "error": None,
            "format": "mp3",
        }
    except Exception as e:
        return {
            "success": False,
            "audio_bytes": b"",
            "error": f"TTS failed: {e}",
        }


def text_to_speech_file(text: str, output_path: str, lang: str = "en", slow: bool = False) -> dict:
    """
    Convert text to speech and save to file.

    Args:
        text: Text to convert.
        output_path: File path to save the audio (e.g., '/tmp/output.mp3').
        lang: Language code.
        slow: If True, speak slowly.

    Returns:
        dict with 'success' and 'path'.
    """
    if not _GTTS_AVAILABLE:
        return {"success": False, "path": "", "error": "gTTS not installed."}
    try:
        tts = gTTS(text=text.strip(), lang=lang, slow=slow)
        tts.save(output_path)
        return {"success": True, "path": output_path, "error": None}
    except Exception as e:
        return {"success": False, "path": "", "error": str(e)}


def is_tts_available() -> bool:
    """Check if text-to-speech is available."""
    return _GTTS_AVAILABLE
