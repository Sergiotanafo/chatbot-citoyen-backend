"""
app/api/health.py
Contrôleur HTTP pour le contrôle de santé (Health Check) du backend et de ses dépendances.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.schemas.health import HealthResponse
from app.clients.dsp_client import dsp_client

router = APIRouter(tags=["Santé"])


@router.get("/health", response_model=HealthResponse, summary="Vérification de l'état du système")
async def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    dsp_is_alive = await dsp_client.check_health()
    dsp_status = "connected" if dsp_is_alive else "disconnected"

    overall_status = "ok" if (db_status == "connected" and dsp_is_alive) else "degraded"

    return HealthResponse(
        status=overall_status,
        version="6.0.0-poc",
        database=db_status,
        dsp=dsp_status,
        details={
            "service": "chatbot-citoyen-backend",
            "framework": "FastAPI",
        }
    )

