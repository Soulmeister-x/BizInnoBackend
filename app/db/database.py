from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Literal

from app.core.config import settings

logger = logging.getLogger(__name__)

# Der Datenbank-Verbindungsstring wird aus Ihren Einstellungen geladen
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


# Erstellen der SQLAlchemy Engine
# Der 'pool_pre_ping=True' hilft, die Verbindung aktiv zu halten und
# Probleme mit getrennten Verbindungen zu vermeiden.
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL,
                           pool_pre_ping=True, echo=True)

    # Deklarative Basis für Ihre SQLAlchemy-Modelle
    # Alle Ihre Datenbankmodelle (wie Unternehmen, Ausschreibung, Vorschlag, Anfrage, User)
    # werden von dieser Base-Klasse erben.
    Base = declarative_base()

    from .models import Unternehmen, Vorschlag, Anfrage, Ausschreibung

    logger.info(f"SQLAlchemy Engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create SQLAlchemy Engine: {e}")
    raise

# Erstellen einer SessionLocal-Klasse
# Diese Klasse wird als 'Fabrik' für neue Session-Objekte verwendet.
# - autocommit=False: Datenbankänderungen müssen explizit mit session.commit() bestätigt werden.
# - autoflush=False: Objekte werden nicht automatisch in die DB geschrieben.
# - bind=engine: Die Session wird an unsere Datenbank-Engine gebunden.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # Dependency für FastAPI, um eine Datenbank-Session pro Request bereitzustellen
    # Diese Funktion wird von FastAPI aufgerufen und stellt eine Session bereit,
    # die nach dem Request automatisch geschlossen wird.
    db = SessionLocal()
    try:
        yield db  # Stellt die Session dem Endpunkt zur Verfügung
    except SQLAlchemyError as e:
        db.rollback()  # Bei Fehlern Rollback der Transaktion
        logger.error(f"Database error during request: {e}")
        raise  # Fehler weiterleiten
    finally:
        db.close()  # Stellt sicher, dass die Session immer geschlossen wird


def initialize_database(base):
    """
    Initialisiert die Datenbank:
    - Erstellt eine neue Session.
    - Fügt einen neuen Eintrag für das Unternehmen "Peter Test" hinzu.
    - Führt eine Abfrage aus, um alle Einträge abzurufen und auszugeben.
    """
    try:
        with engine.connect() as connection:
            # Beginne eine Transaktion, um den Befehl sicher auszuführen
            with connection.begin():
                connection.execute(
                    text("CREATE EXTENSION IF NOT EXISTS vector;"))
            logger.info("'vector' extension ensured to be present.")

        logger.info("Attempting to create database tables...")
        base.metadata.create_all(bind=engine)
        logger.info("Database tables created or already exist.")
    except Exception as e:
        logger.error(
            f"Error during database initialization (extension or tables): {e}")
        raise
    finally:
        db.close()
    """
    with db.begin() as transaction:
        new_unternehmen = Unternehmen(
            id=999, name="Peter Test", email="test@domain.org")
        transaction.add(new_unternehmen)
        # Führe eine Abfrage aus, um alle Einträge abzurufen und auszugeben
        alle_unternehmen = transaction.query(Unternehmen).all()
        for u in alle_unternehmen:
            print(u)
        transaction.commit()
    """


def insert_into_database():
    db = SessionLocal()
    with db.begin() as transaction:
        new_unternehmen = Unternehmen(
            id=999, name="Peter Test", email="test@domain.org")
        transaction.add(new_unternehmen)


def insert_embedding(embedding):
    db = SessionLocal()
    with db.begin() as connection:
        new_embedding = TextEmbedding(embedding=embedding)
        connection.add(new_embedding)
        connection.commit()
