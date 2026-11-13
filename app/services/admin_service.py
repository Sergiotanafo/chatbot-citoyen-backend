"""
app/services/admin_service.py
Service pour les statistiques d'administration, la supervision et l'audit.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.repositories.feedback_repository import FeedbackRepository


class AdminService:
    @staticmethod
    def get_dashboard_stats(db: Session) -> dict:
        """Calcule les indicateurs clés de performance pour le tableau de bord administrateur."""
        feedback_repo = FeedbackRepository(db)
        feedback_stats = feedback_repo.get_stats()

        total_questions = 0
        answered = 0
        unanswered = 0
        top_procedures = []
        source_stats = []

        try:
            total_questions = db.execute(text("SELECT COUNT(*) FROM chat_logs")).scalar() or 0
            answered = db.execute(text("SELECT COUNT(*) FROM chat_logs WHERE confidence > 0.4")).scalar() or 0
            unanswered = total_questions - answered

            top_procedures_raw = db.execute(text("""
                SELECT procedure_found, COUNT(*) as total
                FROM chat_logs
                WHERE procedure_found IS NOT NULL AND procedure_found != ''
                GROUP BY procedure_found
                ORDER BY total DESC
                LIMIT 5
            """)).fetchall()
            top_procedures = [{"procedure": r[0], "count": r[1]} for r in top_procedures_raw]

            source_stats_raw = db.execute(text("""
                SELECT response_source, COUNT(*) as total
                FROM chat_logs
                WHERE response_source IS NOT NULL
                GROUP BY response_source
                ORDER BY total DESC
            """)).fetchall()
            source_stats = [{"source": r[0], "count": r[1]} for r in source_stats_raw]
        except Exception:
            pass

        return {
            "total_questions": total_questions,
            "answered": answered,
            "unanswered": unanswered,
            "top_procedures": top_procedures,
            "source_distribution": source_stats,
            "feedback": feedback_stats
        }

