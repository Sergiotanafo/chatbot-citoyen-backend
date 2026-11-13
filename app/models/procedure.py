"""
app/models/procedure.py
Modèles SQLAlchemy pour les démarches administratives, bureaux et urgences au Mali.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ARRAY
from sqlalchemy.sql import func

from app.models.base import Base


class Categorie(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)


class Procedure(Base):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categorie_id = Column(Integer)
    titre = Column(String(255), nullable=False)
    description_globale = Column(Text)
    procedure_lieux = Column(Text)
    documents = Column(Text)
    cout = Column(Text)
    delai = Column(Text)
    service_en_ligne = Column(Text)
    references_legales = Column(Text)
    services_contact = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    body = Column(Text, nullable=False)
    language = Column(String(10), default="fr")
    category = Column(String(100))
    tags = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AdministrativeOffice(Base):
    __tablename__ = "administrative_offices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(300), nullable=False)
    type_bureau = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    adresse = Column(Text)
    telephone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class NumeroUrgence(Base):
    __tablename__ = "numeros_urgence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_fr = Column(String(200), nullable=False)
    service_bm = Column(String(200))
    numero = Column(String(30), nullable=False)
    description_fr = Column(Text)
    description_bm = Column(Text)
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

