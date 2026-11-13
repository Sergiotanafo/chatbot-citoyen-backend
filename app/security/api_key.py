"""
app/security/api_key.py
Vérification sécurisée par HMAC de la clé API pour les requêtes publiques citoyennes.
"""

import hmac
from fastapi import Request, HTTPException, status
from app.config import settings


def verify_api_key(request: Request) -> str:
    """Vérifie le header x-api-key en temps constant (anti timing-attack)."""
    client_api_key = request.headers.get("x-api-key", "")
    if not client_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'x-api-key' manquant"
        )

    # Comparaison sécurisée en temps constant
    if not hmac.compare_digest(client_api_key.encode("utf-8"), settings.api_key.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide"
        )

    return client_api_key

