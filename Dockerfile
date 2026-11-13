# ============================================================
# Dockerfile — Backend Chatbot Citoyen Malien
# ============================================================

FROM python:3.10-slim

WORKDIR /app

# Dépendances système minimales (compilation psycopg2, curl pour healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python allégées
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code applicatif
COPY app/ /app/app/

# Port exposé
EXPOSE 8000

# Vérification de santé du conteneur
HEALTHCHECK --interval=20s --timeout=5s --retries=5 \
    CMD curl -sf http://localhost:8000/health || exit 1

# Lancement du serveur uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

