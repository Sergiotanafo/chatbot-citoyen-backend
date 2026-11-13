"""
app/config.py
Configuration centralisée du Backend via Pydantic BaseSettings.
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Sécurité API Citoyenne & JWT Admin
    api_key: str = Field(default="dev_secret_key", alias="API_KEY")
    jwt_secret_key: str = Field(default="dev_jwt_secret_change_in_production", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=1440, alias="ACCESS_TOKEN_EXPIRE_MINUTES") # 24 heures

    # Base de Données PostgreSQL
    db_user: str = Field(default="chatbot_user", alias="DB_USER")
    db_password: str = Field(default="Skywalk_Citoyen", alias="DB_PASSWORD")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="chatbot_citoyen", alias="DB_NAME")

    # DSP (Data Science Package) - Service gRPC
    dsp_grpc_host: str = Field(default="localhost:50051", alias="DSP_GRPC_HOST")
    dsp_timeout_seconds: int = Field(default=60, alias="DSP_TIMEOUT_SECONDS")
    dsp_mock_fallback: bool = Field(default=True, alias="DSP_MOCK_FALLBACK")

    # Environnement et CORS
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")
    allowed_origins_raw: str = Field(
        default="http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174",
        alias="ALLOWED_ORIGINS"
    )

    @property
    def database_url(self) -> str:
        from urllib.parse import quote_plus
        password_escaped = quote_plus(self.db_password)
        return f"postgresql+psycopg2://{self.db_user}:{password_escaped}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins_raw.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Retourne une instance singleton de la configuration."""
    return Settings()


settings = get_settings()

