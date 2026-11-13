"""
app/api/admin/categories.py
Routes d'administration pour la gestion des catégories de démarches.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.procedure import CategorieCreate, CategorieUpdate, CategorieResponse
from app.repositories.procedure_repository import ProcedureRepository
from app.security.deps import get_current_admin

router = APIRouter(prefix="/admin/categories", tags=["Administration - Catégories"])


@router.get("", response_model=List[CategorieResponse], summary="Lister les catégories")
def list_categories(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    repo = ProcedureRepository(db)
    return repo.list_categories()


@router.post("", response_model=CategorieResponse, status_code=status.HTTP_201_CREATED, summary="Créer une catégorie")
def create_categorie(cat_in: CategorieCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    repo = ProcedureRepository(db)
    if repo.get_categorie_by_slug(cat_in.slug):
        raise HTTPException(status_code=400, detail="Ce slug de catégorie existe déjà")
    return repo.create_categorie(cat_in)


@router.put("/{cat_id}", response_model=CategorieResponse, summary="Modifier une catégorie")
def update_categorie(cat_id: int, cat_in: CategorieUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    repo = ProcedureRepository(db)
    updated = repo.update_categorie(cat_id, cat_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return updated


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer une catégorie")
def delete_categorie(cat_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    repo = ProcedureRepository(db)
    if not repo.delete_categorie(cat_id):
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return None

