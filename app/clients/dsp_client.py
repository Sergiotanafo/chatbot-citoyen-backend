"""
app/clients/dsp_client.py
Client de communication avec le Data Science Package (DSP) via gRPC.
Intègre un mode mock/secours intelligent pour permettre les tests même si le DSP n'est pas encore démarré.
"""

import asyncio
import logging
import uuid
from typing import AsyncGenerator, Dict, Any, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class DspClient:
    """
    Client de haut niveau pour invoquer les services d'IA hébergés dans le DSP.
    Gère la sérialisation, les timeouts et la résilience réseau.
    """

    def __init__(self, target_host: Optional[str] = None):
        self.target_host = target_host or settings.dsp_grpc_host
        self._is_connected = False
        logger.info(f"DspClient initialisé (cible gRPC : {self.target_host})")

    async def check_health(self) -> bool:
        """Vérifie la disponibilité du serveur DSP gRPC."""
        try:
            # En mode test/développement avec fallback activé
            if settings.dsp_mock_fallback:
                return True
            # TODO : appel réel gRPC HealthCheck
            return True
        except Exception as e:
            logger.warning(f"Le DSP n'est pas joignable : {e}")
            return False

    async def ask(
        self,
        question: str,
        session_id: str = "default",
        langue: str = "fr",
        correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Exécute le pipeline d'IA complet (Cache -> NLU -> RAG -> LLM).
        Retourne la réponse générée, la source et les métadonnées.
        """
        corr_id = correlation_id or str(uuid.uuid4())
        logger.info(f"[{corr_id}] Appel DSP.Ask : '{question[:50]}...' (langue={langue})")

        try:
            # 1. Tentative d'appel gRPC réel vers le serveur DSP
            # (Lorsque le protobuf compilé et le DSP sont actifs)
            # stubs = ...
            pass
        except Exception as e:
            logger.warning(f"[{corr_id}] Échec gRPC vers DSP ({e}). Bascule sur le fallback.")

        # 2. Mode Fallback / Mock pour développement indépendant
        if settings.dsp_mock_fallback:
            return self._mock_ask(question, langue)

        raise RuntimeError("Service DSP indisponible et fallback désactivé.")

    async def ask_stream(
        self,
        question: str,
        session_id: str = "default",
        langue: str = "fr",
        correlation_id: Optional[str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Exécute le pipeline d'IA et renvoie les fragments de texte générés en streaming.
        Utilisé pour alimenter l'endpoint Server-Sent Events (SSE).
        """
        corr_id = correlation_id or str(uuid.uuid4())
        logger.info(f"[{corr_id}] Appel DSP.AskStream : '{question[:50]}...'")

        # Fallback de streaming simulant la génération mot à mot
        mock_response = self._mock_ask(question, langue)
        full_text = mock_response["answer"]
        words = full_text.split(" ")

        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.04)  # Simulation de l'inférence LLM
            yield {
                "text": chunk,
                "source": mock_response["source"],
                "is_chunk": True,
            }

        yield {
            "text": "",
            "source": mock_response["source"],
            "is_chunk": False,
            "metadata": {"status": "completed"}
        }

    async def transcribe_audio(self, audio_bytes: bytes, audio_format: str = "webm", langue: str = "bambara") -> Dict[str, Any]:
        """Délègue la transcription vocale (ASR Whisper) au DSP."""
        logger.info(f"Appel DSP.TranscribeAudio ({len(audio_bytes)} octets, format={audio_format})")
        # Fallback pour le dev
        return {
            "text": "I ni ce, n b'a fɛ ka pasipori sɔrɔ",
            "langue": langue,
            "confidence": 0.95
        }

    async def synthesize_speech(self, text: str, langue: str = "bambara") -> bytes:
        """Délègue la synthèse vocale (TTS VITS) au DSP."""
        logger.info(f"Appel DSP.SynthesizeSpeech ('{text[:30]}...')")
        # Retourne un buffer audio vide ou d'amorce
        return b""

    # ── MOCK INTERNE POUR DÉVELOPPEMENT ──────────────────────────────────────
    def _mock_ask(self, question: str, langue: str) -> Dict[str, Any]:
        q_lower = question.lower()
        if "passeport" in q_lower or "pasipori" in q_lower:
            answer = (
                "Pour obtenir un passeport au Mali :\n"
                "📍 Lieu : Direction Générale de la Police Nationale ou consulat.\n"
                "📄 Documents requis : Extrait d'acte de naissance, certificat de nationalité, carte NINA/CNI, 2 photos d'identité.\n"
                "💰 Coût : 55 000 FCFA (tarif officiel).\n"
                "⏳ Délai moyen : 2 à 3 semaines."
            )
            source = "rag_pgvector"
        elif "bonjour" in q_lower or "salut" in q_lower or "i ni ce" in q_lower:
            answer = "Bonjour ! Je suis l'assistant officiel du gouvernement du Mali. En quoi puis-je vous aider pour vos démarches administratives ?"
            source = "local_kb"
        else:
            answer = (
                f"Votre question concernant '{question[:40]}' a bien été reçue. "
                "Le module d'intelligence artificielle DSP est en cours d'intégration."
            )
            source = "dsp_mock"

        return {
            "answer": answer,
            "source": source,
            "documents": ["Guide des démarches administratives du Mali 2026"],
            "response_time_ms": 120,
            "status": "success"
        }


# Instance partagée singleton
dsp_client = DspClient()

