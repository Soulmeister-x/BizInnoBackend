from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Der Datenbank-Verbindungsstring wird aus Ihren Einstellungen geladen
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Deklarative Basis für Ihre SQLAlchemy-Modelle
# Alle Ihre Datenbankmodelle (wie Unternehmen, Ausschreibung, Vorschlag, Anfrage, User)
# werden von dieser Base-Klasse erben.
Base = declarative_base()


# Erstellen der SQLAlchemy Engine
# Der 'pool_pre_ping=True' hilft, die Verbindung aktiv zu halten und
# Probleme mit getrennten Verbindungen zu vermeiden.
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL,
                           pool_pre_ping=True, echo=True)
    Base.metadata.create_all(engine)
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


def initialize_database():
    from .models import Unternehmen
    """
    Initialisiert die Datenbank:
    - Erstellt eine neue Session.
    - Fügt einen neuen Eintrag für das Unternehmen "Peter Test" hinzu.
    - Führt eine Abfrage aus, um alle Einträge abzurufen und auszugeben.
    """
    db = SessionLocal()
    try:
        # Erstelle eine neue Session
        db.begin()
        # Füge einen neuen Eintrag hinzu
        new_unternehmen = Unternehmen(
            id=999, name="Peter Test", email="test@domain.org")
        db.add(new_unternehmen)
        # Führe eine Abfrage aus, um alle Einträge abzurufen und auszugeben
        alle_unternehmen = db.query(Unternehmen).all()
        for u in alle_unternehmen:
            print(u)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
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


def test_db():
    from .models import Unternehmen
    print("\n\n\n############test_db############\n\n\n")
    db = SessionLocal()
    with db.begin():
        try:
            db.add(
                Unternehmen(
                    id=999,
                    email="test@domain.org",
                    name="Peter Test"
                )
            )
            db.commit()
            response = db.query(
                Unternehmen, "SELECT * FROM unternehmen;").all()
            print(response)
        except Exception as e:
            response = f"############\n\nError: {e}\n\n############"
            print(response)
    return response
