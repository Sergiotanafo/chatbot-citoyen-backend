"""
app/main.py
Point d'entrée principal de l'application FastAPI — Backend Chatbot Citoyen Malien.
Architecture légère : sans modèles de Deep Learning embarqués, délègue l'IA au DSP via gRPC.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.config import settings
from app.database import engine, SessionLocal
from app.models.base import Base
from app.models.user import User
from app.security.auth import get_password_hash
from app.security.rate_limiter import limiter
from app.security.lan_filter import LanFilterMiddleware
from app.api import api_router

# Configuration du système de journalisation
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("citizenbot.backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cycle de vie de l'application : initialisation et fermeture sécurisées."""
    logger.info("🚀 Démarrage du Backend Chatbot Citoyen (v6.0-poc)...")

    # 1. Synchronisation des tables PostgreSQL applicatives
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables de la base de données synchronisées.")
    except Exception as e:
        logger.error(f"❌ Erreur lors de la synchronisation des tables BDD : {e}")

    # 2. Création ou réinitialisation du compte administrateur par défaut
    try:
        with SessionLocal() as db:
            admin_user = db.query(User).filter(User.username == "admin").first()
            if not admin_user:
                default_admin = User(
                    username="admin",
                    email="admin@citoyen.ml",
                    hashed_password=get_password_hash("AdminCitoyen2026!"),
                    role="admin",
                    is_active=True
                )
                db.add(default_admin)
                db.commit()
                logger.info("👤 Compte administrateur par défaut créé : admin / AdminCitoyen2026!")
            else:
                admin_user.hashed_password = get_password_hash("AdminCitoyen2026!")
                admin_user.is_active = True
                db.commit()
                logger.info("🔄 Compte 'admin' mis à jour avec mot de passe 'AdminCitoyen2026!'")
    except Exception as e:
        logger.error(f"❌ Erreur initialisation admin : {e}")

    logger.info("✨ Backend opérationnel en écoute (Délégation DSP active).")
    yield
    logger.info("🛑 Arrêt propre du Backend.")


# Initialisation de l'application FastAPI
app = FastAPI(
    title="Chatbot Citoyen Malien — Backend API",
    description="API REST & passerelle d'orchestration pour le Chatbot Citoyen (Mali). Communique avec le DSP via gRPC.",
    version="6.0.0-poc",
    lifespan=lifespan
)

# Configuration Rate Limiter SlowAPI
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware de restriction LAN (réseau local sécurisé)
app.add_middleware(LanFilterMiddleware)

# Middleware CORS pour les interfaces React (chatbot-ui & admin-ui)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gestion des requêtes OPTIONS pour les navigateurs
@app.options("/{full_path:path}")
def options_handler(full_path: str):
    return Response(status_code=204)


# Inclusion de toutes les routes de l'API
app.include_router(api_router)

