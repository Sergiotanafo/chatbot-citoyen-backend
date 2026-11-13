"""
app/schemas/procedure.py
Schémas Pydantic pour la gestion des catégories, procédures administratives et bureaux.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Catégories ───────────────────────────────────────────────────────────────
class CategorieBase(BaseModel):
    nom: str
    slug: str


class CategorieCreate(CategorieBase):
    pass


class CategorieUpdate(BaseModel):
    nom: Optional[str] = None
    slug: Optional[str] = None


class CategorieResponse(CategorieBase):
    id: int

    class Config:
        from_attributes = True


# ── Procédures Administratives ────────────────────────────────────────────────
class ProcedureBase(BaseModel):
    categorie_id: Optional[int] = None
    titre: str
    description_globale: Optional[str] = None
    procedure_lieux: Optional[str] = None
    documents: Optional[str] = None
    cout: Optional[str] = None
    delai: Optional[str] = None
    service_en_ligne: Optional[str] = None
    references_legales: Optional[str] = None
    services_contact: Optional[str] = None


class ProcedureCreate(ProcedureBase):
    pass


class ProcedureUpdate(BaseModel):
    categorie_id: Optional[int] = None
    titre: Optional[str] = None
    description_globale: Optional[str] = None
    procedure_lieux: Optional[str] = None
    documents: Optional[str] = None
    cout: Optional[str] = None
    delai: Optional[str] = None
    service_en_ligne: Optional[str] = None
    references_legales: Optional[str] = None
    services_contact: Optional[str] = None


class ProcedureResponse(ProcedureBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Questions non traitées ────────────────────────────────────────────────────
class QuestionUpdate(BaseModel):
    reponse: str
    status: str = "traitee"
    intent: Optional[str] = None

