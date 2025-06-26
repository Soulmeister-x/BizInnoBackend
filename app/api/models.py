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
    erstellt_am: Optional[datetime]
    aktualisiert_am: Optional[datetime]
