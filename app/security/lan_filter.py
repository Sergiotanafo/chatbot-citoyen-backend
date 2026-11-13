"""
app/security/lan_filter.py
Middleware de restriction d'accès aux adresses IP privées du réseau local (LAN).
"""

import ipaddress
import logging
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings

logger = logging.getLogger(__name__)


def is_private_ip(ip: str) -> bool:
    """Détermine si une IP est une adresse privée ou de boucle locale."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback
    except ValueError:
        return False


class LanFilterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Permettre les pré-vols CORS OPTIONS sans blocage
        if request.method == "OPTIONS":
            return await call_next(request)

        # Si en mode debug ou localhost, tolérant
        client_host = request.client.host if request.client else "127.0.0.1"

        if not settings.debug and not is_private_ip(client_host):
            logger.warning(f"Tentative d'accès non autorisée depuis une IP externe : {client_host}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé exclusivement au réseau local sécurisé (LAN)"
            )

        return await call_next(request)

