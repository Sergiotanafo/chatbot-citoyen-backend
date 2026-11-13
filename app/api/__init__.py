"""
app/api/__init__.py
Centralisation de tous les routeurs de l'API.
"""

from fastapi import APIRouter

from app.api.chat import router as chat_router
from app.api.bambara import router as bambara_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.admin.procedures import router as admin_procedures_router
from app.api.admin.categories import router as admin_categories_router
from app.api.admin.stats import router as admin_stats_router

api_router = APIRouter()

api_router.include_router(chat_router)
api_router.include_router(bambara_router)
api_router.include_router(auth_router)
api_router.include_router(health_router)
api_router.include_router(admin_procedures_router)
api_router.include_router(admin_categories_router)
api_router.include_router(admin_stats_router)

__all__ = ["api_router"]

