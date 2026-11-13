"""
app/api/admin/procedures.py
Routes d'administration pour la gestion des démarches administratives.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.procedure import ProcedureCreate, ProcedureUpdate, ProcedureResponse
from app.repositories.procedure_repository import ProcedureRepository
from app.security.deps import get_current_admin

router = APIRouter(prefix="/admin/procedures", tags=["Administration - Procédures"])


@router.get("", response_model=List[ProcedureResponse], summary="Lister les démarches administratives")
def list_procedures(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    repo = ProcedureRepository(db)
    return repo.list_procedures(skip=skip, limit=limit)


@router.post("", response_model=ProcedureResponse, status_code=status.HTTP_201_CREATED, summary="Créer une démarche administrative")
def create_procedure(
    proc_in: ProcedureCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    repo = ProcedureRepository(db)
    return repo.create_procedure(proc_in)


@router.get("/{proc_id}", response_model=ProcedureResponse, summary="Obtenir le détail d'une démarche")
def get_procedure(
    proc_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    repo = ProcedureRepository(db)
    proc = repo.get_procedure_by_id(proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Démarche introuvable")
    return proc


@router.put("/{proc_id}", response_model=ProcedureResponse, summary="Modifier une démarche")
def update_procedure(
    proc_id: int,
    proc_in: ProcedureUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    repo = ProcedureRepository(db)
    updated = repo.update_procedure(proc_id, proc_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Démarche introuvable")
    return updated


@router.delete("/{proc_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer une démarche")
def delete_procedure(
    proc_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    repo = ProcedureRepository(db)
    if not repo.delete_procedure(proc_id):
        raise HTTPException(status_code=404, detail="Démarche introuvable")
    return None

