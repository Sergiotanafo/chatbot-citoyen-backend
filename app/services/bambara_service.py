"""
app/services/bambara_service.py
Service de gestion des flux vocaux en langue Bambara via le DSP.
"""

from typing import Dict, Any
from app.clients.dsp_client import dsp_client


class BambaraService:
    @staticmethod
    async def transcribe(audio_bytes: bytes, audio_format: str = "webm") -> Dict[str, Any]:
        """Convertit la voix en texte Bambara."""
        return await dsp_client.transcribe_audio(audio_bytes, audio_format, langue="bambara")

    @staticmethod
    async def synthesize(text: str) -> bytes:
        """Convertit le texte Bambara en audio WAV."""
        return await dsp_client.synthesize_speech(text, langue="bambara")

    @staticmethod
    async def vocal_chat(audio_bytes: bytes, audio_format: str = "webm") -> bytes:
        """Pipeline complet vocal : Audio -> STT -> RAG/LLM -> TTS -> Audio WAV."""
        # 1. ASR
        stt_result = await dsp_client.transcribe_audio(audio_bytes, audio_format, langue="bambara")
        transcription = stt_result.get("text", "")

        # 2. Intelligence
        chat_result = await dsp_client.ask(question=transcription, langue="bambara")
        answer_text = chat_result.get("answer", "")

        # 3. TTS
        return await dsp_client.synthesize_speech(answer_text, langue="bambara")

