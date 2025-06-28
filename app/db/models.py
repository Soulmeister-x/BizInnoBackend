import enum
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from app.db.database import Base

# Platzhalter-Embedding
# Die Dimension 1536 ist hier beispielhaft für Modelle wie OpenAI's text-embedding-ada-002.

N_DIM = 1536
PLACEHOLDER_EMBEDDING = [0.0] * N_DIM


class ProposalStatus(str, enum.Enum):
    PENDING = "pending"   # Vorschlag wurde gemacht, aber noch nicht bewertet
    ACCEPTED = "accepted"  # Unternehmen hat den Vorschlag angenommen
    REJECTED = "rejected"  # Unternehmen hat den Vorschlag abgelehnt


class Unternehmen(Base):
    """
    Unternehmen Model: Stellt einen Benutzer / ein Unternehmen dar.
    """
    __tablename__ = "unternehmen"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    # , zum Speichern des gehashten Passworts)
    hashed_password = Column(String)
    # is_active = (Boolean, z.B. fÃ¼r E-Mail-Verifizierung oder Deaktivierung des Kontos)

    # Company data
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    keywords = Column(String)
    branche = Column(String)
    embedding = Column(Vector(N_DIM))

    erstellt_am = Column(DateTime, server_default=func.now())
    aktualisiert_am = Column(DateTime, server_default=func.now())

    vorschlaege = relationship("Vorschlag", back_populates="unternehmen")


class Ausschreibung(Base):
    __tablename__ = "ausschreibung"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titel = Column(String, index=True)
    beschreibung = Column(String)
    quelle_url = Column(String)
    veroeffentlichungsdatum = Column(DateTime)
    bewerbungsfrist = Column(DateTime)
    kategorien = Column(String)
    ort = Column(String)
    gescraped_am = Column(DateTime)
    embedding = Column(Vector(N_DIM))

    vorschlaege = relationship("Vorschlag", back_populates="ausschreibung")


class Vorschlag(Base):
    """
    Stellt einen Vorschlag einer Ausschreibung für ein Unternehmen dar.
    Enthält den Matching-Score und den Status der Bewertung durch das Unternehmen.
    """
    __tablename__ = "vorschlaege"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Fremdschlüssel zu Unternehmen
    unternehmen_id = Column(Integer, ForeignKey(
        "users.id"), index=True, nullable=False)
    # Fremdschlüssel zu Ausschreibung
    ausschreibung_id = Column(Integer, ForeignKey(
        "ausschreibung.id"), index=True, nullable=False)

    # Der berechnete Score für die Passung
    matching_score = Column(Float, nullable=False)
    # Status der Bewertung durch das Unternehmen
    # status = Column(String,
    #                default=ProposalStatus.PENDING, nullable=False)

    # Zeitpunkt des Vorschlags
    vorgeschlagen_am = Column(DateTime, server_default=func.now())
    aktualisiert_am = Column(DateTime, onupdate=func.now(
    ), server_default=func.now())  # Letzte Aktualisierung des Status

    # Beziehungen zu anderen Modellen
    user = relationship("Unternehmen", back_populates="vorschlaege")
    ausschreibung = relationship("Ausschreibung", back_populates="vorschlaege")
    # Ein Vorschlag hat maximal eine Anfrage
    anfrage = relationship(
        "Anfrage", back_populates="vorschlaege", uselist=False)


class Anfrage(Base):
    """
    Stellt eine generierte Anfrage für eine angenommene Ausschreibung dar.
    """
    __tablename__ = "anfrage"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Fremdschlüssel zum Vorschlag, auf dem die Anfrage basiert
    # Unique, da ein Vorschlag nur eine Anfrage haben sollte
    vorschlag_id = Column(Integer, ForeignKey(
        "vorschlaege.id"), unique=True, nullable=False)

    # Der vollständige generierte Anfrage-Text
    generierter_text = Column(String, nullable=False)

    # Zeitpunkt der Generierung
    erstellt_am = Column(DateTime, server_default=func.now())

    # Beziehung zum Vorschlag
    vorschlag = relationship("Vorschlag", back_populates="anfrage")
