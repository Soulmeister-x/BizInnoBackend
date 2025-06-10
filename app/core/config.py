from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  """Klasse zum Verwalten der Anwendungseinstellungen (FastAPI)
  geladen aus Umgebungsvariablen oder .env Dateien
  """

  PROJECT_NAME: str = "Business Innovation"
  API_VERSION: str = "0.0.1"
  API_VERSION_PREFIX: str = "/api/v1"

  """
  # Datenbank-Einstellungen
  DATABASE_URL: str # Beispiel: "postgresql+psycopg2://user:password@host:port/dbname"
                    # Füllen Sie dies in Ihrer .env-Datei aus
  
  # JWT-Authentifizierungs-Einstellungen
  SECRET_KEY: str # Ein geheimer Schlüssel für die JWT-Signatur
                  # Generieren Sie einen langen, zufälligen String (z.B. mit 'openssl rand -hex 32')
  ALGORITHM: str = "HS256" # Algorithmus für JWT-Signatur
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # Gültigkeit des Access Tokens in Minuten (hier: 24 Stunden)

  # Optional: API-Key für externe Dienste (z.B. OpenAI für Embeddings)
  OPENAI_API_KEY: Optional[str] = None 
  
  # CORS-Einstellungen für das Frontend
  # Trennen Sie URLs mit Kommas im .env-File (z.B. "http://localhost:5173,https://your-frontend.vercel.app")
  BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"] 


  # Pydantic-Settings-Konfiguration
  # Liest Umgebungsvariablen aus der .env-Datei im Projekt-Root
  model_config = SettingsConfigDict(
      env_file=".env", 
      extra="ignore" # Ignoriert zusätzliche Umgebungsvariablen, die nicht definiert sind
  )
  """


settings = Settings()
