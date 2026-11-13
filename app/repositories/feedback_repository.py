"""
app/repositories/feedback_repository.py
Accès aux données pour les retours utilisateurs (👍/👎).
"""

import logging
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.session import Feedback

logger = logging.getLogger(__name__)


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, session_id: str, message_index: int, rating: int) -> Feedback:
        feedback = Feedback(
            session_id=session_id,
            message_index=message_index,
            rating=rating
        )
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def get_stats(self) -> dict:
        total = self.db.query(func.count(Feedback.id)).scalar() or 0
        positives = self.db.query(func.count(Feedback.id)).filter(Feedback.rating == 1).scalar() or 0
        negatives = self.db.query(func.count(Feedback.id)).filter(Feedback.rating == -1).scalar() or 0
        satisfaction_pct = round((positives / total * 100), 1) if total > 0 else 0

        return {
            "total": total,
            "positives": positives,
            "negatives": negatives,
            "satisfaction_pct": satisfaction_pct,
        }

