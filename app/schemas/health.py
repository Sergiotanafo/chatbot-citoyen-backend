"""
app/schemas/health.py
Schémas Pydantic pour l'état de santé du backend et de ses dépendances.
"""

from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    dsp: str
    details: Optional[dict] = None

