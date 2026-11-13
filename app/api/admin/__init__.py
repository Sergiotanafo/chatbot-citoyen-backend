"""
app/api/admin/__init__.py
Routers d'administration.
"""

from app.api.admin.procedures import router as procedures_router
from app.api.admin.categories import router as categories_router
from app.api.admin.stats import router as stats_router

__all__ = ["procedures_router", "categories_router", "stats_router"]

