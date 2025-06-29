from sqlalchemy import create_engine, text, select, insert, bindparam
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


def query_alle(db_name: Literal["ausschreibung", "unternehmen", "anfrage", "vorschlag"]):
    db = SessionLocal()
    with db.begin():
        try:
            match db_name:
                case "ausschreibung":
                    db_model = Ausschreibung
                case "unternehmen":
                    db_model = Unternehmen
                case "anfrage":
                    db_model = Anfrage
                case "vorschlag":
                    db_model = Vorschlag
                case _:
                    raise KeyError(f"invalid key: {db_name}")

            alle = db.execute(
                select(db_model).order_by(db_model.id)).scalars().fetchall()

            match db_name:
                case "ausschreibung":
                    ret = [
                        {
                            "id": a.id,
                            "titel": a.titel,
                            "beschreibung": a.beschreibung,
                            "quelle_url": a.quelle_url,
                            "veroeffentlichungsdatum": a.veroeffentlichungsdatum,
                            "bewerbungsfrist": a.bewerbungsfrist,
                            "kategorien": a.kategorien,
                            "ort": a.ort,
                            "gescraped_am": a.gescraped_am
                        } for a in alle
                    ]
                case "unternehmen":
                    ret = [
                        {
                            "id": u.id,
                            "name": u.name,
                            "email": u.email,
                            "description": u.description,
                            "keywords": u.keywords,
                            "branche": u.branche,
                            "erstellt_am": u.erstellt_am,
                            "aktualisiert_am": u.aktualisiert_am,
                        } for u in alle
                    ]
                case "anfrage":
                    ret = [
                        {
                            "id": x.id,
                            "vorschlag_id": x.vorschlag_id,
                            "generierter_text": x.generierter_text,
                            "erstellt_am": x.erstellt_am,
                        } for x in alle
                    ]
                case "vorschlag":
                    ret = [
                        {
                            "id": x.id,
                            "unternehmen_id": x.unternehmen_id,
                            "ausschreibung_id": x.ausschreibung_id,
                            "matching_score": x.matching_score,
                            "vorgeschlagen_am": x.vorgeschlagen_am,
                            "aktualisiert_am": x.aktualisiert_am,
                        } for x in alle
                    ]

        except Exception as e:
            logger.error(f"Error while trying to query all 'unternehmen': {e}")
    return ret


def query_by_id(db_name: Literal["ausschreibung", "unternehmen", "anfrage", "vorschlag"], entry_id: int):
    db = SessionLocal()
    with db.begin() as transaction:
        match db_name:
            case "ausschreibung":
                db_model = Ausschreibung
            case "unternehmen":
                db_model = Unternehmen
            case "anfrage":
                db_model = Anfrage
            case "vorschlag":
                db_model = Vorschlag
            case _:
                raise KeyError(f"invalid key: {db_name}")
        entry = db.scalars(
            select(db_model)
            .where(db_model.id == entry_id)
        ).first()

    return entry.to_dict()


def insert_into_database(db_name: Literal["ausschreibung", "unternehmen", "anfrage", "vorschlag"], data):
    db = SessionLocal()
    data = data.model_dump()
    with db.begin() as transaction:
        match db_name:
            case "ausschreibung":
                new_entry = Ausschreibung(**data)
            case "unternehmen":
                new_entry = Unternehmen(**data)
            case "anfrage":
                new_entry = Anfrage(**data)
            case "vorschlag":
                new_entry = Vorschlag(**data)
            case _:
                raise KeyError(f"invalid key: {db_name}")

        db.add(new_entry)
        transaction.commit()

    return new_entry.to_dict()


def insert_embedding(embedding):
    db = SessionLocal()
    with db.begin() as connection:
        new_embedding = TextEmbedding(embedding=embedding)
        connection.add(new_embedding)
        connection.commit()
