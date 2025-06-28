from typing import Optional
from os import environ

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Klasse zum Verwalten der Anwendungseinstellungen (FastAPI)
    geladen aus Umgebungsvariablen oder .env Dateien
    """

    PROJECT_NAME: str = "Business Innovation"
    API_VERSION: str = "0.0.1"
    API_VERSION_PREFIX: str = "/api/v1"
    DATABASE_URL: str = environ.get("DATABASE_URL")


settings = Settings()
