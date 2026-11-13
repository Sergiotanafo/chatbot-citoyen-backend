"""
app/api/admin/stats.py
Routes d'administration pour la consultation des statistiques et indicateurs de performance.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.admin_service import AdminService
from app.security.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Administration - Statistiques"])


@router.get("/stats", summary="Indicateurs de performance du chatbot")
def get_stats(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return AdminService.get_dashboard_stats(db)

