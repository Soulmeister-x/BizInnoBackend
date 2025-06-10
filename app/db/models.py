import enum
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
# from pgvector.sqlalchemy import Vector

from app.db.database import Base  # TODO: Importiert create Base in database.py


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
    # embedding = Column(Vector(1536)) # TODO: embedding-size!

    vorschlaege = relationship("Vorschlag", back_populates="ausschreibung")


class ProposalStatus(str, enum.Enum):
    PENDING = "pending"   # Vorschlag wurde gemacht, aber noch nicht bewertet
    ACCEPTED = "accepted"  # Unternehmen hat den Vorschlag angenommen
    REJECTED = "rejected"  # Unternehmen hat den Vorschlag abgelehnt


class Vorschlag(Base):
    """
    Stellt einen Vorschlag einer Ausschreibung für ein Unternehmen dar.
    Enthält den Matching-Score und den Status der Bewertung durch das Unternehmen.
    """
    __tablename__ = "vorschlag"

    id = Column(Integer, primary_key=True, index=True)

    # Fremdschlüssel zu Unternehmen
    unternehmen_id = Column(Integer, ForeignKey(
        "unternehmen.id"), index=True, nullable=False)
    # Fremdschlüssel zu Ausschreibung
    ausschreibung_id = Column(Integer, ForeignKey(
        "ausschreibung.id"), index=True, nullable=False)

    # Der berechnete Score für die Passung
    matching_score = Column(Float, nullable=False)
    # Status der Bewertung durch das Unternehmen
    status = Column(Enum(ProposalStatus),
                    default=ProposalStatus.PENDING, nullable=False)

    # Zeitpunkt des Vorschlags
    vorgeschlagen_am = Column(DateTime, server_default=func.now())
    aktualisiert_am = Column(DateTime, onupdate=func.now(
    ), server_default=func.now())  # Letzte Aktualisierung des Status

    # Beziehungen zu anderen Modellen
    unternehmen = relationship("Unternehmen", back_populates="vorschlaege")
    ausschreibung = relationship("Ausschreibung", back_populates="vorschlaege")
    # Ein Vorschlag hat maximal eine Anfrage
    anfrage = relationship(
        "Anfrage", back_populates="vorschlag", uselist=False)


class Anfrage(Base):
    """
    Stellt eine generierte Anfrage für eine angenommene Ausschreibung dar.
    """
    __tablename__ = "anfrage"

    id = Column(Integer, primary_key=True, index=True)

    # Fremdschlüssel zum Vorschlag, auf dem die Anfrage basiert
    # Unique, da ein Vorschlag nur eine Anfrage haben sollte
    vorschlag_id = Column(Integer, ForeignKey(
        "vorschlag.id"), unique=True, nullable=False)

    # Der vollständige generierte Anfrage-Text
    generierter_text = Column(Text, nullable=False)

    # Zeitpunkt der Generierung
    erstellt_am = Column(DateTime, server_default=func.now())

    # Beziehung zum Vorschlag
    vorschlag = relationship("Vorschlag", back_populates="anfrage")


class User(Base):
    """
    User Model für Authentifizierung
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(Text)  # , zum Speichern des gehashten Passworts)
    # is_active = (Boolean, z.B. fÃ¼r E-Mail-Verifizierung oder Deaktivierung des Kontos)
    erstellt_am = Column(DateTime, server_default=func.now())
    aktualisiert_am = Column(DateTime, server_default=func.now())


# Platzhalter-Embedding
# In einer echten Anwendung würde dies durch Ihren processing_service.py generiert werden.
# Die Dimension 1536 ist hier beispielhaft für Modelle wie OpenAI's text-embedding-ada-002.
PLACEHOLDER_EMBEDDING = [0.0] * 1536


now = datetime.datetime.now()


mock_data = [
    Ausschreibung(
        id=1,
        titel="Neubau Verwaltungsgebäude – Rohbauarbeiten",
        beschreibung="Umfassende Rohbauarbeiten für ein fünfstöckiges Verwaltungsgebäude im Stadtzentrum. Umfasst Aushub, Fundamentierung, Beton- und Maurerarbeiten. Erfahrung in Großprojekten im Bereich Hochbau erwünscht.",
        quelle_url="https://example-tender.com/tender/2025-001",
        veroeffentlichungsdatum=datetime.datetime(2025, 5, 28, 9, 30, 0),
        bewerbungsfrist=datetime.datetime(2025, 6, 25, 17, 0, 0),
        kategorien="Hochbau,Neubau,Rohbau",
        ort="Berlin",
        gescraped_am=now - datetime.timedelta(days=12, hours=3),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=2,
        titel="Sanierung historischer Brücke – Tiefbauarbeiten",
        beschreibung="Instandsetzungs- und Sanierungsarbeiten an einer historischen Stahlbrücke. Erfordert spezielle Kenntnisse im Tiefbau und Umgang mit Denkmalschutzauflagen. Maßnahmen umfassen Korrosionsschutz und Betoninstandsetzung.",
        quelle_url="https://example-tender.com/tender/2025-002",
        veroeffentlichungsdatum=datetime.datetime(2025, 5, 29, 11, 0, 0),
        bewerbungsfrist=datetime.datetime(2025, 6, 28, 16, 0, 0),
        kategorien="Tiefbau,Brückenbau,Sanierung,Denkmalschutz",
        ort="Dresden",
        gescraped_am=now - datetime.timedelta(days=10, hours=5),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=3,
        titel="Straßenbau: Erneuerung Fahrbahn B17 – Ingenieurbauleistungen",
        beschreibung="Komplette Erneuerung und Verbreiterung eines 5 km langen Bundesstraßenabschnitts. Umfasst Erdarbeiten, Entwässerungssysteme, Fahrbahnaufbau und Markierungen. Erfahrungen im Straßenbau und in der Verkehrsführung sind Voraussetzung.",
        quelle_url="https://example-tender.com/tender/2025-003",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 1, 8, 45, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 1, 10, 0, 0),
        kategorien="Straßenbau,Infrastruktur,Tiefbau",
        ort="Leipzig",
        gescraped_am=now - datetime.timedelta(days=8, hours=2),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=4,
        titel="Umbau und Erweiterung einer Schulturnhalle",
        beschreibung="Anbau einer neuen Sektion an eine bestehende Turnhalle und Modernisierung der vorhandenen Strukturen. Erfordert Kenntnisse in Holz- und Stahlbau sowie energieeffizienten Sanierungsmaßnahmen. Bauarbeiten im laufenden Betrieb.",
        quelle_url="https://example-tender.com/tender/2025-004",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 2, 14, 0, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 5, 12, 0, 0),
        kategorien="Hochbau,Umbau,Sanierung,Schulbau",
        ort="München",
        gescraped_am=now - datetime.timedelta(days=7, hours=1),
        embedding=PLACEHELDER_EMBEDDING
    ),
    Ausschreibung(
        id=5,
        titel="Bauleistungen für Kläranlage – Erweiterung & Modernisierung",
        beschreibung="Umfassende Bauarbeiten zur Erweiterung und Modernisierung einer kommunalen Kläranlage. Spezialisierte Kenntnisse im Wasserbau, Betonbau für Becken und Installation von Maschinentechnik erforderlich.",
        quelle_url="https://example-tender.com/tender/2025-005",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 3, 10, 0, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 8, 15, 0, 0),
        kategorien="Wasserbau,Tiefbau,Infrastruktur",
        ort="Hamburg",
        gescraped_am=now - datetime.timedelta(days=6, hours=4),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=6,
        titel="Dachsanierung historisches Gebäude – Zimmerer- & Dachdeckerarbeiten",
        beschreibung="Umfassende Instandsetzung des Daches eines alten Gutshauses, inklusive Zimmererarbeiten am Dachstuhl und Neueindeckung. Erfahrung mit historischen Baumaterialien und Denkmalschutz ist von Vorteil.",
        quelle_url="https://example-tender.com/tender/2025-006",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 4, 11, 0, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 10, 11, 0, 0),
        kategorien="Hochbau,Sanierung,Dachbau,Denkmalschutz",
        ort="Köln",
        gescraped_am=now - datetime.timedelta(days=5, hours=0),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=7,
        titel="Bau von Lärmschutzwänden an Autobahn A9",
        beschreibung="Errichtung von ca. 3 km Lärmschutzwänden entlang der Autobahn A9. Umfasst Fundamentierung, Anlieferung und Montage von Betonfertigteilen. Erfahrung mit Bauarbeiten im Bereich von Verkehrswegen notwendig.",
        quelle_url="https://example-tender.com/tender/2025-007",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 5, 9, 0, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 12, 14, 0, 0),
        kategorien="Infrastruktur,Straßenbau,Betonbau",
        ort="Nürnberg",
        gescraped_am=now - datetime.timedelta(days=4, hours=2),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=8,
        titel="Grünflächen- & Wegegestaltung – Landschaftsbauarbeiten",
        beschreibung="Neugestaltung eines öffentlichen Parks inklusive Wegebau, Pflasterarbeiten, Errichtung kleinerer Gebäude (Pavillons) und Anlage von Grünflächen. Erfahrung im Landschaftsbau und Umgang mit öffentlichen Auftraggebern.",
        quelle_url="https://example-tender.com/tender/2025-008",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 6, 15, 30, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 15, 10, 0, 0),
        kategorien="Landschaftsbau,Wegebau,Grünflächen",
        ort="Stuttgart",
        gescraped_am=now - datetime.timedelta(days=3, hours=6),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=9,
        titel="Innenausbau und Trockenbau für Bürogebäude",
        beschreibung="Umfassende Innenausbauarbeiten für ein dreistöckiges Bürogebäude. Umfasst Trockenbauwände, Akustikdecken, Brandschutzmaßnahmen und die Vorbereitung für technische Installationen.",
        quelle_url="https://example-tender.com/tender/2025-009",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 7, 12, 0, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 18, 16, 0, 0),
        kategorien="Innenausbau,Trockenbau,Bürobau",
        ort="Frankfurt am Main",
        gescraped_am=now - datetime.timedelta(days=2, hours=0),
        embedding=PLACEHOLDER_EMBEDDING
    ),
    Ausschreibung(
        id=10,
        titel="Abbrucharbeiten & Entsorgung Industriegelände",
        beschreibung="Professioneller Rückbau von Industrieanlagen und Gebäuden auf einem ehemaligen Fabrikgelände. Umfasst selektiven Abbruch, Entsorgung von Gefahrstoffen und Wiederherstellung des Geländes bis zur Baufreigabe. Spezielle Genehmigungen erforderlich.",
        quelle_url="https://example-tender.com/tender/2025-010",
        veroeffentlichungsdatum=datetime.datetime(2025, 6, 8, 14, 0, 0),
        bewerbungsfrist=datetime.datetime(2025, 7, 20, 11, 0, 0),
        kategorien="Abbruch,Rückbau,Entsorgung,Industrie",
        ort="Düsseldorf",
        gescraped_am=now - datetime.timedelta(days=1, hours=7),
        embedding=PLACEHOLDER_EMBEDDING
    )
]
