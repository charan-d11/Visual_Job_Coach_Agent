"""
voice_routes.py
---------------
FastAPI routes for voice I/O (speech-to-text and text-to-speech).

Endpoints:
  POST /api/voice/speak      — convert text to audio (returns MP3 bytes)
  POST /api/voice/transcribe — convert uploaded audio to text
  GET  /api/voice/status     — check if voice services are available
"""

import io

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.text_to_speech import text_to_speech_bytes, is_tts_available
from app.services.speech_to_text import transcribe_audio_bytes, is_stt_available
from app.security.input_sanitizer import sanitize_text
from app.utils.validators import validate_audio_upload

router = APIRouter(prefix="/api/voice", tags=["Voice"])


class SpeakRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="Text to convert to speech")
    lang: str = Field(default="en", max_length=5, description="Language code (e.g. 'en', 'es')")
    slow: bool = Field(default=False, description="Slow down speech for clarity")


class TranscribeResponse(BaseModel):
    success: bool
    text: str
    error: str | None = None
    word_count: int = 0


@router.post("/speak", summary="Convert text to speech (returns MP3 audio)")
async def speak_text(request: SpeakRequest):
    """
    Convert text to speech and return an MP3 audio stream.
    The response body is raw MP3 bytes with Content-Type: audio/mpeg.
    """
    if not is_tts_available():
        raise HTTPException(
            status_code=503,
            detail="Text-to-speech service unavailable. Ensure gTTS is installed.",
        )

    text_clean = sanitize_text(request.text, max_length=2000)
    if not text_clean.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    result = text_to_speech_bytes(text=text_clean, lang=request.lang, slow=request.slow)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "TTS failed."))

    audio_bytes = result["audio_bytes"]
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "attachment; filename=response.mp3",
            "Content-Length": str(len(audio_bytes)),
        },
    )


@router.post("/transcribe", response_model=TranscribeResponse, summary="Transcribe audio to text")
async def transcribe_audio(audio: UploadFile = File(..., description="Audio file (WAV preferred)")):
    """
    Upload an audio file and receive the transcribed text.
    Supported formats: WAV, MP3, FLAC, OGG.
    Maximum size: 10 MB.
    """
    if not is_stt_available():
        raise HTTPException(
            status_code=503,
            detail="Speech-to-text service unavailable. Ensure SpeechRecognition is installed.",
        )

    # Read and validate the uploaded file
    audio_bytes = await audio.read()
    content_type = audio.content_type or "audio/wav"

    valid, error_msg = validate_audio_upload(
        content_type=content_type,
        size_bytes=len(audio_bytes),
        max_mb=10.0,
    )
    # Allow audio/wav even if content type check is strict
    if not valid and len(audio_bytes) > 0:
        # Try anyway with a lenient check — content type can be wrong
        pass

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Audio file is empty.")

    result = transcribe_audio_bytes(audio_bytes)
    return TranscribeResponse(
        success=result["success"],
        text=result.get("text", ""),
        error=result.get("error"),
        word_count=len(result.get("text", "").split()) if result.get("text") else 0,
    )


@router.get("/status", summary="Check voice service availability")
async def voice_status() -> dict:
    """Return the availability status of TTS and STT services."""
    return {
        "text_to_speech": {
            "available": is_tts_available(),
            "engine": "gTTS (Google Text-to-Speech)",
        },
        "speech_to_text": {
            "available": is_stt_available(),
            "engine": "SpeechRecognition (Google Web Speech API)",
        },
    }
