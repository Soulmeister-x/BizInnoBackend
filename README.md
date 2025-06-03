klare und wartbare Datei- bzw. Ordnerstruktur für monolithisches Python Backend mit FastAPI.

Diese Struktur trennt Verantwortlichkeiten und erleichtert die Entwicklung des Prototypen.

---

### Python Backend Ordnerstruktur

```
.
├── app/
│   ├── __init__.py                 # Markiert 'app' als Python-Paket
│   │
│   ├── main.py                     # Haupt-FastAPI-Anwendung, Router-Registrierung
│   │
│   ├── core/                       # Globale Konfigurationen, Einstellungen, Sicherheits-Tools
│   │   ├── __init__.py
│   │   ├── config.py               # Lädt Umgebungsvariablen und definiert Anwendungs-Settings
│   │   └── security.py             # Funktionen für Passwort-Hashing, JWT-Token-Erstellung/-Validierung
│   │
│   ├── db/                         # Datenbank-spezifische Dateien
│   │   ├── __init__.py
│   │   ├── database.py             # SQLAlchemy Engine, Session-Management, Basis für Models
│   │   └── models.py               # Definitionen der SQLAlchemy/SQLModel ORM-Modelle (Unternehmen, Ausschreibung, Vorschlag, Anfrage)
│   │
│   ├── api/                        # API-Endpunkte (FastAPI Routers), gruppiert nach Domänen
│   │   ├── __init__.py
│   │   ├── auth.py                 # Routen für Authentifizierung (Registrierung, Login)
│   │   ├── companies.py            # Routen für Unternehmensprofil-Management (CRUD)
│   │   ├── tenders.py              # Routen für Ausschreibungen (Lesen, Filtern, Suchen, Empfehlungen)
│   │   └── ingestion.py            # Route zum Empfangen der gescrapten Ausschreibungsdaten vom Agenten
│   │
│   ├── services/                   # Business-Logik und komplexe Operationen
│   │   ├── __init__.py
│   │   ├── auth_service.py         # Logik für Benutzerauthentifizierung und -autorisierung
│   │   ├── company_service.py      # Geschäftslogik für Unternehmensdaten (z.B. Profil bearbeiten)
│   │   ├── tender_service.py       # Geschäftslogik für Ausschreibungsdaten (z.B. Statusänderungen)
│   │   ├── matching_service.py     # Kern-Logik für Matching-Score-Berechnung, Empfehlungen
│   │   └── processing_service.py   # Logik zur Textverarbeitung, Vektor-Generierung für Ausschreibungen
│   │
│   └── schemas/                    # Pydantic-Modelle für Datenvalidierung (Request- und Response-Modelle, DTOs)
│       ├── __init__.py
│       ├── auth.py                 # Schemas für Authentifizierung (LoginRequest, TokenResponse)
│       ├── company.py              # Schemas für Unternehmensprofile
│       ├── tender.py               # Schemas für Ausschreibungen (TenderCreate, TenderResponse)
│       ├── proposal.py             # Schemas für Vorschläge
│       └── common.py               # Allgemeine Schemas (z.B. Pagination, ErrorResponse)
│
├── tests/                          # Tests für das Backend
│   ├── __init__.py
│   ├── test_api.py                 # API-Endpunkt-Tests
│   ├── test_services.py            # Unit-Tests für die Geschäftslogik
│   └── test_db.py                  # Datenbank-Interaktions-Tests
│
├── .env.example                    # Beispiel für Umgebungsvariablen
├── requirements.txt                # Python-Abhängigkeiten (Pakete)
├── Dockerfile                      # Optional: Für Containerisierung mit Docker (später nützlich)
├── README.md                       # Projekt-Beschreibung, Setup-Anleitung
└── start.sh                        # Einfaches Start-Skript für Gunicorn mit Uvicorn-Workern
```

---

### Erläuterung der Struktur

* **`app/`**: Das Hauptverzeichnis für Ihren Anwendungscode.
    * **`__init__.py`**: Macht `app` zu einem Python-Paket.
    * **`main.py`**: Dies ist der zentrale Einstiegspunkt Ihrer FastAPI-Anwendung. Hier wird die `FastAPI()`-Instanz erstellt und alle Router aus dem `api/`-Verzeichnis werden inkludiert.
    * **`core/`**: Enthält anwendungsübergreifende Konfigurationen und Utilities.
        * `config.py`: Definiert die Einstellungen Ihrer Anwendung, oft geladen aus Umgebungsvariablen (`.env`).
        * `security.py`: Hilfsfunktionen für die Sicherheit, z.B. zum Hashen von Passwörtern oder zum Erstellen/Validieren von JWT-Token.
    * **`db/`**: Beherbergt alles, was mit der Datenbank zu tun hat.
        * `database.py`: Richtet die Datenbankverbindung ein (z.B. SQLAlchemy Engine, Session-Management) und eine Funktion, um Datenbank-Sessions für Abhängigkeiten in FastAPI bereitzustellen.
        * `models.py`: Definiert Ihre Datenbanktabellen als Python-Klassen (ORM-Modelle) mit SQLAlchemy oder SQLModel. Hier würden Sie auch `pgvector`-Typen für Ihre Vektoren definieren.
    * **`api/`**: Hier sind Ihre FastAPI-**Router** organisiert. Jeder `.py`-Datei entspricht einer logischen Gruppe von API-Endpunkten (z.B. alle Authentifizierungs-Endpunkte in `auth.py`). Die Router verwenden die Schemas für Request/Response-Validierung und rufen die entsprechende Logik in den `services/` auf.
    * **`services/`**: Dies ist das Herzstück Ihrer **Business-Logik**. Die Funktionen in diesem Verzeichnis kapseln die komplexen Operationen und verwenden die `db/` -Module, um mit der Datenbank zu interagieren. Die Router in `api/` sollten hauptsächlich diese Dienste aufrufen und nicht direkt die Datenbank-Logik enthalten.
        * `matching_service.py`: Enthält die Logik zur Berechnung des Matching-Scores, zur Vektor-Ähnlichkeitssuche und zur Filterung von Empfehlungen.
        * `processing_service.py`: Kümmert sich um die Textverarbeitung von Ausschreibungsdaten und die Generierung der Vektoren, die in der Datenbank gespeichert werden.
    * **`schemas/`**: Enthält Ihre **Pydantic-Modelle**. Diese werden von FastAPI für die automatische Validierung von Request-Bodies und die Serialisierung von Responses verwendet, um eine klare Schnittstelle zu definieren.

* **`tests/`**: Für Ihre Unit- und Integrationstests, organisiert nach den getesteten Komponenten.
* **`.env.example`**: Eine Vorlage für die Umgebungsvariablen, die Ihr Backend benötigt (z.B. `DATABASE_URL`, `SECRET_KEY`).
* **`requirements.txt`**: Listet alle Python-Pakete auf, die Ihr Projekt benötigt.
* **`Dockerfile`**: (Optional, aber gut für die Zukunft) Definiert, wie Ihre Anwendung in einen Docker-Container gepackt wird.
* **`README.md`**: Wichtige Informationen zum Projekt, Setup-Anleitung, etc.
* **`start.sh`**: Ein einfaches Shell-Skript, um Ihre Anwendung mit Gunicorn und Uvicorn-Workern zu starten.

### Beispiel `start.sh`

```bash
#!/bin/bash

# Anzahl der Worker-Prozesse (oft 2 * CPU-Kerne + 1)
WORKERS=${WORKERS:-4} # Standard auf 4, kann per Umgebungsvariable überschrieben werden

# Host und Port, auf dem der Server lauscht
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

echo "Starting Gunicorn with $WORKERS workers on $HOST:$PORT"

# Startet Gunicorn mit Uvicorn-Workern
gunicorn app.main:app \
  --workers "$WORKERS" \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind "$HOST:$PORT" \
  --log-level info \
  --reload # Nur für die Entwicklung: Entfernen oder als Bedingung in Produktion
```

