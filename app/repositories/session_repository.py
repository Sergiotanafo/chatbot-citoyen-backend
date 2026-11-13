"""
app/repositories/session_repository.py
Accès aux données pour les sessions de conversation et les journaux de requêtes.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.session import ChatSession, ChatLog

logger = logging.getLogger(__name__)


class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Récupère l'historique des messages d'une session."""
        session = self.db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not session or not session.messages:
            return []
        msgs = session.messages
        if isinstance(msgs, str):
            try:
                msgs = json.loads(msgs)
            except Exception:
                return []
        return msgs if isinstance(msgs, list) else []

    def append_exchange(self, session_id: str, user_text: str, bot_text: str) -> None:
        """Ajoute un échange (question utilisateur + réponse bot) à la session."""
        try:
            session = self.db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
            if not session:
                session = ChatSession(session_id=session_id, messages=[])
                self.db.add(session)

            history = session.messages or []
            if isinstance(history, str):
                history = json.loads(history)

            history.append({"type": "human", "content": user_text})
            history.append({"type": "ai", "content": bot_text})

            # Conserver au maximum les 20 derniers messages pour éviter l'enflure
            if len(history) > 20:
                history = history[-20:]

            session.messages = history
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erreur enregistrement échange session {session_id}: {e}")

    def clear(self, session_id: str) -> bool:
        """Efface l'historique d'une session."""
        session = self.db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False

    def log_interaction(
        self,
        question: str,
        procedure_found: Optional[str],
        confidence: Optional[float],
        source: str
    ) -> None:
        """Enregistre un événement de question/réponse dans les logs."""
        try:
            log_entry = ChatLog(
                question=question,
                procedure_found=procedure_found,
                confidence=confidence,
                response_source=source
            )
            self.db.add(log_entry)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erreur log interaction chat : {e}")

