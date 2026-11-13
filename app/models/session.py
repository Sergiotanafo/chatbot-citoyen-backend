"""
app/models/session.py
Modèles SQLAlchemy pour les conversations citoyennes, logs et retours utilisateurs.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, SmallInteger, JSON
from sqlalchemy.sql import func

from app.models.base import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(128), unique=True, nullable=False, index=True)
    messages = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    procedure_found = Column(String(300))
    confidence = Column(Float)
    response_source = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(128), nullable=False, index=True)
    message_index = Column(Integer, nullable=False)
    rating = Column(SmallInteger, nullable=False)  # 1 = 👍, -1 = 👎
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QuestionRecord(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(Text, nullable=False)
    langue = Column(String(20), default="fr")
    sender_id = Column(String(128))
    status = Column(String(30), default="non_traitee")
    reponse = Column(Text)
    intent = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

