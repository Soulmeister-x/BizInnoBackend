"""
API models, for requests and responses (e.g. input validation)
"""

import enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class XUnternehmen(BaseModel):
    id: int
    name: Optional[str]
    beschreibung: Optional[str]
    schluesselwoerter: Optional[str]
    branche: Optional[str]
    email: Optional[str]
    erstellt_am: Optional[datetime] = datetime.now()
    aktualisiert_am: Optional[datetime] = datetime.now()


class XAusschreibung(BaseModel):
    id: int
    titel: Optional[str] = None
    beschreibung: Optional[str] = None
    quelle_url: Optional[str] = None
    veroeffentlichungsdatum: Optional[datetime] = None
    bewerbungsfrist: Optional[datetime] = None
    kategorien: Optional[str] = None
    ort: Optional[str] = None
    gescraped_am: Optional[datetime] = None
    embedding: Optional[list] = None


class ProposalStatus(str, enum.Enum):
    PENDING = "pending"   # Vorschlag wurde gemacht, aber noch nicht bewertet
    ACCEPTED = "accepted"  # Unternehmen hat den Vorschlag angenommen
    REJECTED = "rejected"  # Unternehmen hat den Vorschlag abgelehnt


class XVorschlag(BaseModel):
    id: int
    unternehmen_id: Optional[int]
    ausschreibung_id: Optional[int]
    matching_score: Optional[float]
    status: ProposalStatus = ProposalStatus.PENDING
    vorgeschlagen_am: Optional[datetime]
    aktualisiert_am: Optional[datetime] = datetime.now()


class XAnfrage(BaseModel):
    id: int
    vorschlag_id: int
    generierter_text: str
    erstellt_am: Optional[datetime] = datetime.now()
