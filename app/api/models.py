"""
API models, for requests and responses (e.g. input validation)
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Profile(BaseModel):
    id: int
    name: Optional[str]
    beschreibung: Optional[str]
    schluesselwoerter: Optional[str]
    branche: Optional[str]
    email: Optional[str]
    erstellt_am: Optional[datetime] = datetime.now()
    aktualisiert_am: Optional[datetime] = datetime.now()


class Ausschreibung(BaseModel):
    id: int
    titel: Optional[str]
    beschreibung: Optional[str]
    quelle_url: Optional[str]
    veroeffentlichungsdatum: Optional[datetime]
    bewerbungsfrist: Optional[datetime]
    kategorien: Optional[str]
    ort: Optional[str]
    gescraped_am: Optional[datetime]
    embedding: Optional[list]


class ProposalStatus(str, enum.Enum):
    PENDING = "pending"   # Vorschlag wurde gemacht, aber noch nicht bewertet
    ACCEPTED = "accepted"  # Unternehmen hat den Vorschlag angenommen
    REJECTED = "rejected"  # Unternehmen hat den Vorschlag abgelehnt


class Vorschlag(BaseModel):
    id: int
    unternehmen_id: Optional[int]
    ausschreibung_id: Optional[int]
    matching_score: Optional[float]
    status: ProposalStatus = ProposalStatus.PENDING
    vorgeschlagen_am: Optional[datetime]
    aktualisiert_am: Optional[datetime] = datetime.now()


class Anfrage(BaseModel):
    id: int
    vorschlag_id: int
    generierter_text: str
    erstellt_am: Optional[datetime] = datetime.now()
