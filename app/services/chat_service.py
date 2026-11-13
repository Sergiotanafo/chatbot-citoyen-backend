"""
app/services/chat_service.py
Service d'orchestration pour le traitement des questions citoyennes et du streaming.
"""

import time
import uuid
from typing import AsyncGenerator, Dict, Any
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest, ChatResponse
from app.clients.dsp_client import dsp_client
from app.repositories.session_repository import SessionRepository


class ChatService:
    @staticmethod
    async def handle_chat(req: ChatRequest, db: Session) -> ChatResponse:
        """
        Traite une requête de discussion complète :
        1. Invoque le DSP
        2. Sauvegarde l'échange dans la session utilisateur
        3. Enregistre les métriques dans les logs
        """
        start_time = time.time()
        correlation_id = str(uuid.uuid4())
        session_repo = SessionRepository(db)

        # 1. Appel au DSP via gRPC
        dsp_result = await dsp_client.ask(
            question=req.question,
            session_id=req.session_id,
            langue=req.langue,
            correlation_id=correlation_id
        )

        answer = dsp_result.get("answer", "")
        source = dsp_result.get("source", "dsp")
        elapsed_ms = int((time.time() - start_time) * 1000)

        # 2. Persistance de la session
        session_repo.append_exchange(
            session_id=req.session_id,
            user_text=req.question,
            bot_text=answer
        )

        # 3. Journalisation de l'interaction
        session_repo.log_interaction(
            question=req.question,
            procedure_found=dsp_result.get("documents", [None])[0] if dsp_result.get("documents") else None,
            confidence=1.0 if source != "dsp_mock" else 0.5,
            source=source
        )

        return ChatResponse(
            answer=answer,
            source=source,
            response_time_ms=elapsed_ms
        )

    @staticmethod
    async def handle_chat_stream(req: ChatRequest, db: Session) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Générateur asynchrone relayant les fragments de réponse en streaming (SSE).
        """
        correlation_id = str(uuid.uuid4())
        session_repo = SessionRepository(db)
        accumulated_answer = []

        async for chunk_data in dsp_client.ask_stream(
            question=req.question,
            session_id=req.session_id,
            langue=req.langue,
            correlation_id=correlation_id
        ):
            text_chunk = chunk_data.get("text", "")
            if text_chunk:
                accumulated_answer.append(text_chunk)
            yield chunk_data

        # Enregistrement final en fin de flux
        full_answer = "".join(accumulated_answer)
        if full_answer:
            session_repo.append_exchange(
                session_id=req.session_id,
                user_text=req.question,
                bot_text=full_answer
            )

