"""
app/security/rate_limiter.py
Gestionnaire de limitation de débit (Rate Limiting) basé sur l'IP cliente.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

