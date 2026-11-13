"""
app/api/chat.py
Contrôleur HTTP pour les échanges conversationnels (synchrone et SSE streaming) et les feedbacks.
"""

import json
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, FeedbackRequest
from app.services.chat_service import ChatService
from app.repositories.feedback_repository import FeedbackRepository
from app.security.api_key import verify_api_key
from app.security.rate_limiter import limiter

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse, summary="Poser une question au chatbot (synchrone)")
@limiter.limit("20/minute")
async def chat_endpoint(
    req: ChatRequest,
    request: Request,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Reçoit une question du citoyen, délègue le raisonnement au DSP et retourne la réponse."""
    return await ChatService.handle_chat(req, db)


@router.post("/chat/stream", summary="Poser une question en streaming temps réel (SSE)")
@limiter.limit("20/minute")
async def chat_stream_endpoint(
    req: ChatRequest,
    request: Request,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Retourne un flux Server-Sent Events (SSE) affichant la réponse mot par mot."""
    async def event_generator():
        async for chunk in ChatService.handle_chat_stream(req, db):
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/feedback", summary="Soumettre un avis citoyen (👍 / 👎)")
@limiter.limit("30/minute")
def submit_feedback(
    req: FeedbackRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Enregistre l'évaluation de satisfaction sur un message pour le suivi qualité."""
    repo = FeedbackRepository(db)
    repo.create(
        session_id=req.session_id,
        message_index=req.message_index,
        rating=req.rating
    )
    return {"status": "success", "message": "Feedback enregistré avec succès"}

