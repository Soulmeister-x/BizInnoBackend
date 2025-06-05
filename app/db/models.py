from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.db.database import Base # TODO: Importiert create Base in database.py

class Unternehmen(Base):
  __tablename__ = "unternehmen"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  beschreibung = Column(String)
  schluesselwoerter = Column(String)
  branche = Column(String)
  kontakt_email = Column(String)
  erstellt_am = Column(DateTime)
  aktualisiert_am = Column(DateTime)

  vorschlaege = relationship("Vorschlag", back_populates="unternehmen")

class Ausschreibung(Base):
  __tablename__ = "ausschreibung"
  id = Column(Integer, primary_key=True, index=True)
  titel = Column(String, index=True)
  beschreibung = Column(String)
  quelle_url = Column(String)
  veroeffentlichungsdatum = Column(DateTime)
  bewerbungsfrist = Column(DateTime)
  kategorien = Column(String)
  ort = Column(String)
  gescraped_am = Column(DateTime)
  #embedding = Column(Vector(1536)) # TODO: embedding-size!

  vorschlaege = relationship("Vorschlag", back_populates="ausschreibung")

import enum
class ProposalStatus(str, enum.Enum):
  PENDING = "pending"   # Vorschlag wurde gemacht, aber noch nicht bewertet
  ACCEPTED = "accepted" # Unternehmen hat den Vorschlag angenommen
  REJECTED = "rejected" # Unternehmen hat den Vorschlag abgelehnt


class Vorschlag(Base):
  """
  Stellt einen Vorschlag einer Ausschreibung für ein Unternehmen dar.
  Enthält den Matching-Score und den Status der Bewertung durch das Unternehmen.
  """
  __tablename__ = "vorschlag"

  id = Column(Integer, primary_key=True, index=True)
  
  # Fremdschlüssel zu Unternehmen
  unternehmen_id = Column(Integer, ForeignKey("unternehmen.id"), index=True, nullable=False)
  # Fremdschlüssel zu Ausschreibung
  ausschreibung_id = Column(Integer, ForeignKey("ausschreibung.id"), index=True, nullable=False)

  matching_score = Column(Float, nullable=False) # Der berechnete Score für die Passung
  status = Column(Enum(ProposalStatus), default=ProposalStatus.PENDING, nullable=False) # Status der Bewertung durch das Unternehmen

  vorgeschlagen_am = Column(DateTime, server_default=func.now()) # Zeitpunkt des Vorschlags
  aktualisiert_am = Column(DateTime, onupdate=func.now(), server_default=func.now()) # Letzte Aktualisierung des Status

  # Beziehungen zu anderen Modellen
  unternehmen = relationship("Unternehmen", back_populates="vorschlaege")
  ausschreibung = relationship("Ausschreibung", back_populates="vorschlaege")
  anfrage = relationship("Anfrage", back_populates="vorschlag", uselist=False) # Ein Vorschlag hat maximal eine Anfrage


class Anfrage(Base):
  """
  Stellt eine generierte Anfrage für eine angenommene Ausschreibung dar.
  """
  __tablename__ = "anfrage"

  id = Column(Integer, primary_key=True, index=True)
  
  # Fremdschlüssel zum Vorschlag, auf dem die Anfrage basiert
  vorschlag_id = Column(Integer, ForeignKey("vorschlag.id"), unique=True, nullable=False) # Unique, da ein Vorschlag nur eine Anfrage haben sollte
  
  generierter_text = Column(Text, nullable=False) # Der vollständige generierte Anfrage-Text
  
  erstellt_am = Column(DateTime, server_default=func.now()) # Zeitpunkt der Generierung

  # Beziehung zum Vorschlag
  vorschlag = relationship("Vorschlag", back_populates="anfrage")


class User(Base):
  """
  User Model für Authentifizierung
  """
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(Text) #, zum Speichern des gehashten Passworts)
  #is_active = (Boolean, z.B. fÃ¼r E-Mail-Verifizierung oder Deaktivierung des Kontos)
  erstellt_am = Column(DateTime, server_default=func.now())
  aktualisiert_am = Column(DateTime, server_default=func.now())
