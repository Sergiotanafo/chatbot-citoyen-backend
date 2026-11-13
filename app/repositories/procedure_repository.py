"""
app/repositories/procedure_repository.py
Accès aux données pour les procédures administratives, catégories, contenus et bureaux.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.procedure import (
    Categorie,
    Procedure,
    Content,
    AdministrativeOffice,
    NumeroUrgence,
)
from app.models.session import QuestionRecord
from app.schemas.procedure import (
    CategorieCreate,
    CategorieUpdate,
    ProcedureCreate,
    ProcedureUpdate,
)


class ProcedureRepository:
    def __init__(self, db: Session):
        self.db = db

    # ── Catégories ───────────────────────────────────────────────────────────
    def list_categories(self) -> List[Categorie]:
        return self.db.query(Categorie).order_by(Categorie.nom).all()

    def get_categorie_by_slug(self, slug: str) -> Optional[Categorie]:
        return self.db.query(Categorie).filter(Categorie.slug == slug).first()

    def create_categorie(self, cat_in: CategorieCreate) -> Categorie:
        cat = Categorie(nom=cat_in.nom, slug=cat_in.slug)
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def update_categorie(self, cat_id: int, cat_in: CategorieUpdate) -> Optional[Categorie]:
        cat = self.db.query(Categorie).filter(Categorie.id == cat_id).first()
        if not cat:
            return None
        if cat_in.nom is not None:
            cat.nom = cat_in.nom
        if cat_in.slug is not None:
            cat.slug = cat_in.slug
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def delete_categorie(self, cat_id: int) -> bool:
        cat = self.db.query(Categorie).filter(Categorie.id == cat_id).first()
        if not cat:
            return False
        self.db.delete(cat)
        self.db.commit()
        return True

    # ── Procédures ───────────────────────────────────────────────────────────
    def list_procedures(self, skip: int = 0, limit: int = 100) -> List[Procedure]:
        return self.db.query(Procedure).order_by(Procedure.titre).offset(skip).limit(limit).all()

    def get_procedure_by_id(self, proc_id: int) -> Optional[Procedure]:
        return self.db.query(Procedure).filter(Procedure.id == proc_id).first()

    def create_procedure(self, proc_in: ProcedureCreate) -> Procedure:
        proc = Procedure(**proc_in.model_dump())
        self.db.add(proc)
        self.db.commit()
        self.db.refresh(proc)
        return proc

    def update_procedure(self, proc_id: int, proc_in: ProcedureUpdate) -> Optional[Procedure]:
        proc = self.db.query(Procedure).filter(Procedure.id == proc_id).first()
        if not proc:
            return None
        for field, value in proc_in.model_dump(exclude_unset=True).items():
            setattr(proc, field, value)
        self.db.commit()
        self.db.refresh(proc)
        return proc

    def delete_procedure(self, proc_id: int) -> bool:
        proc = self.db.query(Procedure).filter(Procedure.id == proc_id).first()
        if not proc:
            return False
        self.db.delete(proc)
        self.db.commit()
        return True

    # ── Bureaux & Numéros d'urgence ──────────────────────────────────────────
    def list_offices(self) -> List[AdministrativeOffice]:
        return self.db.query(AdministrativeOffice).order_by(AdministrativeOffice.nom).all()

    def list_emergencies(self) -> List[NumeroUrgence]:
        return self.db.query(NumeroUrgence).filter(NumeroUrgence.actif == True).all()

    # ── Questions non traitées ───────────────────────────────────────────────
    def list_questions(self, status: Optional[str] = None) -> List[QuestionRecord]:
        query = self.db.query(QuestionRecord)
        if status:
            query = query.filter(QuestionRecord.status == status)
        return query.order_by(QuestionRecord.created_at.desc()).all()

