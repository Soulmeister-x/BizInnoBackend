from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging

# Importieren Sie die Einstellungen Ihrer Anwendung
from app.core.config import settings

logger = logging.getLogger(__name__)

# Der Datenbank-Verbindungsstring wird aus Ihren Einstellungen geladen
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Erstellen der SQLAlchemy Engine
# Der 'pool_pre_ping=True' hilft, die Verbindung aktiv zu halten und
# Probleme mit getrennten Verbindungen zu vermeiden.
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    logger.info("SQLAlchemy Engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create SQLAlchemy Engine: {e}")
    raise

# Erstellen einer SessionLocal-Klasse
# Diese Klasse wird als 'Fabrik' für neue Session-Objekte verwendet.
# - autocommit=False: Datenbankänderungen müssen explizit mit session.commit() bestätigt werden.
# - autoflush=False: Objekte werden nicht automatisch in die DB geschrieben.
# - bind=engine: Die Session wird an unsere Datenbank-Engine gebunden.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Deklarative Basis für Ihre SQLAlchemy-Modelle
# Alle Ihre Datenbankmodelle (wie Unternehmen, Ausschreibung, Vorschlag, Anfrage, User)
# werden von dieser Base-Klasse erben.
Base = declarative_base()

# Dependency für FastAPI, um eine Datenbank-Session pro Request bereitzustellen
# Diese Funktion wird von FastAPI aufgerufen und stellt eine Session bereit,
# die nach dem Request automatisch geschlossen wird.


def get_db():
    db = SessionLocal()
    try:
        yield db  # Stellt die Session dem Endpunkt zur Verfügung
    except SQLAlchemyError as e:
        db.rollback()  # Bei Fehlern Rollback der Transaktion
        logger.error(f"Database error during request: {e}")
        raise  # Fehler weiterleiten
    finally:
        db.close()  # Stellt sicher, dass die Session immer geschlossen wird
