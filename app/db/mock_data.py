import datetime
import random


# Platzhalter-Embedding
# In einer echten Anwendung würde dies durch Ihren processing_service.py generiert werden.
# Die Dimension 1536 ist hier beispielhaft für Modelle wie OpenAI's text-embedding-ada-002.
# PLACEHOLDER_EMBEDDING = [0.0] * 1536

# Aktuelles Datum als Basis für das Scraping-Datum
now = datetime.datetime.now()


def generate_mock_inbox_messages(num_messages=10):
  """Generates a list of mock inbox messages for a user profile focused on construction."""

  messages = []
  for _ in range(num_messages):
    message = {
        "datetime": f"{random.randint(2023, 2024)}-{random.randint(1, 12)}-{random.randint(1, 28)} {random.randint(9, 23)}:",
        "tender_id": f"{random.randint(1000, 9999)}",
        "title": random.choice([
            "Bau eines kleinen Bürogebäudes",
            "Renovierung eines historischen Gebäudes",
            "Erstellung einer Gewerbeetage",
            "Sanierung von Wohnräumen",
            "Neubau von einem Reihenhaus",
            "Bau eines kleinen Gemeindezentrums",
            "Erstellung einer Parkplatzausbau",
            "Bau einer Sportanlage",
            "Erstellung eines kleinen Shops",
            "Neubau eines Wohnblocks",
        ]),
        "location": random.choice(["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"]),
        "summary": f"Die Ausschreibung umfasst die {random.randint(1, 10)}m² Baufläche und die Erstellung von {random.randint(1, 5)} Wohnungen. Es werden moderne Bauweisen und nachhaltige Materialien eingesetzt. Ziel ist die Erstellung eines energieeffizienten Gebäudes mit hoher Wohnqualität.  Weitere Details können im vollständigen Ausschreibungsdokument eingesehen werden.",
        "score": round(random.uniform(7.0, 9.9), 1) #score is between 7 and 9.9
    }
    messages.append(message)
  return messages


def load_mock_data():
    """Returns user_profile, inbox_messages, tenders"""
    tenders = [
        {
            "id": 1,
            "titel": "Neubau Verwaltungsgebäude – Rohbauarbeiten",
            "beschreibung": "Umfassende Rohbauarbeiten für ein fünfstöckiges Verwaltungsgebäude im Stadtzentrum. Umfasst Aushub, Fundamentierung, Beton- und Maurerarbeiten. Erfahrung in Großprojekten im Bereich Hochbau erwünscht.",
            "quelle_url": "https://example-tender.com/tender/2025-001",
            "veroeffentlichungsdatum": datetime.datetime(2025, 5, 28, 9, 30, 0),
            "bewerbungsfrist": datetime.datetime(2025, 6, 25, 17, 0, 0),
            "kategorien": "Hochbau,Neubau,Rohbau",
            "ort": "Berlin",
            "gescraped_am": now - datetime.timedelta(days=12, hours=3),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 2,
            "titel": "Sanierung historischer Brücke – Tiefbauarbeiten",
            "beschreibung": "Instandsetzungs- und Sanierungsarbeiten an einer historischen Stahlbrücke. Erfordert spezielle Kenntnisse im Tiefbau und Umgang mit Denkmalschutzauflagen. Maßnahmen umfassen Korrosionsschutz und Betoninstandsetzung.",
            "quelle_url": "https://example-tender.com/tender/2025-002",
            "veroeffentlichungsdatum": datetime.datetime(2025, 5, 29, 11, 0, 0),
            "bewerbungsfrist": datetime.datetime(2025, 6, 28, 16, 0, 0),
            "kategorien": "Tiefbau,Brückenbau,Sanierung,Denkmalschutz",
            "ort": "Dresden",
            "gescraped_am": now - datetime.timedelta(days=10, hours=5),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 3,
            "titel": "Straßenbau: Erneuerung Fahrbahn B17 – Ingenieurbauleistungen",
            "beschreibung": "Komplette Erneuerung und Verbreiterung eines 5 km langen Bundesstraßenabschnitts. Umfasst Erdarbeiten, Entwässerungssysteme, Fahrbahnaufbau und Markierungen. Erfahrungen im Straßenbau und in der Verkehrsführung sind Voraussetzung.",
            "quelle_url": "https://example-tender.com/tender/2025-003",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 1, 8, 45, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 1, 10, 0, 0),
            "kategorien": "Straßenbau,Infrastruktur,Tiefbau",
            "ort": "Leipzig",
            "gescraped_am": now - datetime.timedelta(days=8, hours=2),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 4,
            "titel": "Umbau und Erweiterung einer Schulturnhalle",
            "beschreibung": "Anbau einer neuen Sektion an eine bestehende Turnhalle und Modernisierung der vorhandenen Strukturen. Erfordert Kenntnisse in Holz- und Stahlbau sowie energieeffizienten Sanierungsmaßnahmen. Bauarbeiten im laufenden Betrieb.",
            "quelle_url": "https://example-tender.com/tender/2025-004",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 2, 14, 0, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 5, 12, 0, 0),
            "kategorien": "Hochbau,Umbau,Sanierung,Schulbau",
            "ort": "München",
            "gescraped_am": now - datetime.timedelta(days=7, hours=1),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 5,
            "titel": "Bauleistungen für Kläranlage – Erweiterung & Modernisierung",
            "beschreibung": "Umfassende Bauarbeiten zur Erweiterung und Modernisierung einer kommunalen Kläranlage. Spezialisierte Kenntnisse im Wasserbau, Betonbau für Becken und Installation von Maschinentechnik erforderlich.",
            "quelle_url": "https://example-tender.com/tender/2025-005",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 3, 10, 0, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 8, 15, 0, 0),
            "kategorien": "Wasserbau,Tiefbau,Infrastruktur",
            "ort": "Hamburg",
            "gescraped_am": now - datetime.timedelta(days=6, hours=4),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 6,
            "titel": "Dachsanierung historisches Gebäude – Zimmerer- & Dachdeckerarbeiten",
            "beschreibung": "Umfassende Instandsetzung des Daches eines alten Gutshauses, inklusive Zimmererarbeiten am Dachstuhl und Neueindeckung. Erfahrung mit historischen Baumaterialien und Denkmalschutz ist von Vorteil.",
            "quelle_url": "https://example-tender.com/tender/2025-006",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 4, 11, 0, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 10, 11, 0, 0),
            "kategorien": "Hochbau,Sanierung,Dachbau,Denkmalschutz",
            "ort": "Köln",
            "gescraped_am": now - datetime.timedelta(days=5, hours=0),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 7,
            "titel": "Bau von Lärmschutzwänden an Autobahn A9",
            "beschreibung": "Errichtung von ca. 3 km Lärmschutzwänden entlang der Autobahn A9. Umfasst Fundamentierung, Anlieferung und Montage von Betonfertigteilen. Erfahrung mit Bauarbeiten im Bereich von Verkehrswegen notwendig.",
            "quelle_url": "https://example-tender.com/tender/2025-007",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 5, 9, 0, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 12, 14, 0, 0),
            "kategorien": "Infrastruktur,Straßenbau,Betonbau",
            "ort": "Nürnberg",
            "gescraped_am": now - datetime.timedelta(days=4, hours=2),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 8,
            "titel": "Grünflächen- & Wegegestaltung – Landschaftsbauarbeiten",
            "beschreibung": "Neugestaltung eines öffentlichen Parks inklusive Wegebau, Pflasterarbeiten, Errichtung kleinerer Gebäude (Pavillons) und Anlage von Grünflächen. Erfahrung im Landschaftsbau und Umgang mit öffentlichen Auftraggebern.",
            "quelle_url": "https://example-tender.com/tender/2025-008",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 6, 15, 30, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 15, 10, 0, 0),
            "kategorien": "Landschaftsbau,Wegebau,Grünflächen",
            "ort": "Stuttgart",
            "gescraped_am": now - datetime.timedelta(days=3, hours=6),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 9,
            "titel": "Innenausbau und Trockenbau für Bürogebäude",
            "beschreibung": "Umfassende Innenausbauarbeiten für ein dreistöckiges Bürogebäude. Umfasst Trockenbauwände, Akustikdecken, Brandschutzmaßnahmen und die Vorbereitung für technische Installationen.",
            "quelle_url": "https://example-tender.com/tender/2025-009",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 7, 12, 0, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 18, 16, 0, 0),
            "kategorien": "Innenausbau,Trockenbau,Bürobau",
            "ort": "Frankfurt am Main",
            "gescraped_am": now - datetime.timedelta(days=2, hours=0),
            # "embedding": PLACEHOLDER_EMBEDDING
        },
        {
            "id": 10,
            "titel": "Abbrucharbeiten & Entsorgung Industriegelände",
            "beschreibung": "Professioneller Rückbau von Industrieanlagen und Gebäuden auf einem ehemaligen Fabrikgelände. Umfasst selektiven Abbruch, Entsorgung von Gefahrstoffen und Wiederherstellung des Geländes bis zur Baufreigabe. Spezielle Genehmigungen erforderlich.",
            "quelle_url": "https://example-tender.com/tender/2025-010",
            "veroeffentlichungsdatum": datetime.datetime(2025, 6, 8, 14, 0, 0),
            "bewerbungsfrist": datetime.datetime(2025, 7, 20, 11, 0, 0),
            "kategorien": "Abbruch,Rückbau,Entsorgung,Industrie",
            "ort": "Düsseldorf",
            "gescraped_am": now - datetime.timedelta(days=1, hours=7),
            # "embedding": PLACEHOLDER_EMBEDDING
        }
    ]

    user_profile = {
        "id": "xxxx-xxxx",
        "name": "My Company",
        "type": "company",
        "type_name": "Baufirma",
        "specialization": "Bauarbeiten und Baukonstruktion",
        "region": {
            "search_type": "radius",
            "zipcode": "04129",
            "city": "Leipzig",
            "radius": "100"
        }
    }

    inbox_messages = generate_mock_inbox_messages(15)


    return user_profile, inbox_messages, tenders

