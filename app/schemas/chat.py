"""
app/schemas/chat.py
Schémas Pydantic pour les requêtes conversationnelles et les retours d'expérience.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="Question posée par le citoyen")
    model: str = Field(default="hybrid", description="Modèle ciblé (hybrid par défaut)")
    session_id: str = Field(default="default", description="Identifiant unique de la session de discussion")
    langue: str = Field(default="fr", description="Langue de l'échange ('fr' ou 'bambara')")


class ChatResponse(BaseModel):
    answer: str
    source: Optional[str] = Field(default="dsp", description="Source de la réponse (cache, local_kb, rasa, rag_ollama)")
    response_time_ms: Optional[int] = Field(default=None, description="Temps total de traitement en millisecondes")


class StreamChunkPayload(BaseModel):
    text: str
    source: Optional[str] = None
    is_chunk: bool = True
    metadata: Optional[Dict[str, Any]] = None


class FeedbackRequest(BaseModel):
    session_id: str
    message_index: int
    rating: int = Field(..., ge=-1, le=1, description="1 pour un vote positif (👍), -1 pour un vote négatif (👎)")

