"""
app/api/bambara.py
Contrôleur HTTP pour les fonctionnalités vocales en langue Bambara.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Response, Depends
from pydantic import BaseModel
from app.services.bambara_service import BambaraService
from app.security.api_key import verify_api_key

router = APIRouter(prefix="/bambara", tags=["Bambara Vocal"])


class TTSRequest(BaseModel):
    text: str


@router.post("/stt", summary="Reconnaissance vocale : Audio -> Texte Bambara")
async def speech_to_text(
    audio: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    """Reçoit un fichier audio (WebM/Opus) et retourne la transcription en Bambara."""
    try:
        content = await audio.read()
        return await BambaraService.transcribe(content, audio_format="webm")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur ASR Bambara : {str(e)}")


@router.post("/tts", summary="Synthèse vocale : Texte Bambara -> Audio WAV")
async def text_to_speech(
    req: TTSRequest,
    api_key: str = Depends(verify_api_key)
):
    """Convertit un texte en Bambara en audio WAV 16 kHz."""
    try:
        audio_bytes = await BambaraService.synthesize(req.text)
        return Response(content=audio_bytes, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur TTS Bambara : {str(e)}")


@router.post("/chat", summary="Chat vocal complet : Audio -> Réponse Audio")
async def vocal_chat(
    audio: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    """Pipeline complet direct : envoi d'une question vocale, réception directe de la réponse vocale."""
    try:
        content = await audio.read()
        audio_response = await BambaraService.vocal_chat(content, audio_format="webm")
        return Response(content=audio_response, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur chat vocal : {str(e)}")

