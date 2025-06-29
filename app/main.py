from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
import logging

# import settings and data models
from app.core.config import settings
from app.db.mock_data import load_mock_data, get_user_profiles
from app.db.database import SessionLocal, engine, Base, initialize_database, query_alle, insert_into_database, query_by_id
# from app.api import auth, companies, tenders, ingestion # Importiert die Router-Objekte aus den Modulen
from app.api.models import Profile, Ausschreibung, Vorschlag, Anfrage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_profile = {}
inbox_messages = []
tenders = []

user_profiles = get_user_profiles()


def find_list_entry(lst: list, key: str, value):
    for entry in lst:
        if entry.get(key) == value:
            return entry
    raise IndexError(f"Error trying to find entry in list: {e}")


def create_db_tables():
    logger.info("Attempting to create database tables...")
    try:
        initialize_database(base=Base)
        # TODO: reset DB and init with mock data
        logger.info("Database tables created or already exist.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # TODO: add valid error handling and potential retry methods
        sys.exit(1)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Prototyp für KMU-Ausschreibungsplattform",
    # TODO: add contact, license
)

# allow CORS to allow frontend request this service
origins = [
    "http://localhost:5173",
    "http://localhost:8000",
    "https://biz-inno-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# handle database sessions (provide and close)


def get_db():
    yield mock_data
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    """

# routers for API-endpoints in app/api/
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(companies.router, prefix="/api/v1/companies", tags=["Companies"])
# app.include_router(tenders.router, prefix="/api/v1/tenders", tags=["Tenders"])
# app.include_router(ingestion.router, prefix="/api/v1/ingestion", tags=["Ingestion"])
# TODO: replace basic routes with routers


@app.get("/api/v1/", tags=["Root"])
def read_root():
    # health check
    return {"message": "Willkommen zur KMU Ausschreibungsplattform API v1"}


@app.on_event("startup")
async def startup_event():
    # initialize database on app start
    logger.info("Application startup event triggered.")
    create_db_tables()
    global user_profile
    global inbox_messages
    global tenders
    user_profile, inbox_messages, tenders = load_mock_data()
    logger.info("Database tables checked/created. Application ready.")


@app.get("/api/v1/test")
def test_db_request():
    return {"message": test_db()}


@app.get("/api/v1/ausschreibung")
@app.get("/api/v1/ausschreibungen")
@app.get("/api/v1/tenders", tags=["Tenders"])
def get_tenders():
    return query_alle("ausschreibung")


@app.get("/api/v1/tenders/{tender_id}", tags=["Tenders"])
def get_tender_by_id(tender_id: int):
    return query_by_id("ausschreibung", tender_id)


@app.get("/api/v1/company")
@app.get("/api/v1/unternehmen")
@app.get("/api/v1/profile", tags=["Profile"])
def get_profile():
    return query_alle("unternehmen")


@app.get("/api/v1/profile/{unternehmen_id}", tags=["Profile"])
def get_profile_by_id(unternehmen_id: int):
    return query_by_id("unternehmen", unternehmen_id)


@app.get("/api/v1/messages")
@app.get("/api/v1/vorschlag")
@app.get("/api/v1/vorschlaege")
@app.get("/api/v1/inbox", tags=["Inbox"])
def get_inbox():
    return query_alle("vorschlag")


@app.get("/api/v1/inbox/{inbox_id}", tags=["Inbox"])
def get_message_by_id(inbox_id: int):
    return query_by_id("vorschlag", inbox_id)


@app.get("/api/v1/anfrage")
@app.get("/api/v1/anfragen")
@app.get("/api/v1/inquiry", tags=["Anfrage"])
def get_inquiries():
    return query_alle("anfrage")


@app.get("/api/v1/anfrage/{anfrage_id}", tags=["Anfrage"])
def get_anfrage_by_id(anfrage_id: int):
    return query_by_id("anfrage", anfrage_id)


@app.get("/api/v1/inbox/{message_id}", tags=["Inbox"])
def get_inbox(message_id: int):
    return find_list_entry(inbox_messages, "id", message_id)


@app.post("/api/v1/profile/{profile_id}", tags=["Profile"])
def switch_profile(profile_id: int):
    global user_profile
    try:
        user_profile = find_list_entry(user_profiles, "id", profile_id)
        msg = "Profile update successfully"
    except IndexError as e:
        msg = f"Profile update FAILED: {e}"
    return {"message": msg}


@app.delete("/api/v1/profile", tags=["Profile"])
def delete_profile():
    global user_profile
    user_profile = {}
    return {"message": "Profile deleted successfully"}


@app.post("/api/v1/profile/default", tags=["Profile"])
async def reset_default_profile():
    global user_profile
    user_profile, _, _ = load_mock_data()
    return {"message": "User profile was reset to default values."}


@app.post("/api/v1/ingest/tenders", tags=["Ingestion", "Tenders"])
async def ingest_tenders(data: dict):
    logger.info("POST tender")
    global tenders
    # TODO: Logik für das Aktualisieren eines Angebots
    try:
        return {"message": "Received POST tender", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ingest/profile", tags=["Ingestion", "Profile"])
async def ingest_profile(data: Profile):
    logger.info("POST profile")
    global user_profile
    try:
        # user_profile.name = data.get("name", user_profile.name)
        # user_profile.email = data.get("email", user_profile.email)
        return {"message": "Profile updated successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ingest/inbox", tags=["Ingestion", "Inbox"])
async def ingest_inbox_messages(data: dict):
    logger.info("POST inbox")
    global inbox_messages
    # TODO: Logik für das Aktualisieren des Posteingangs
    try:
        data = await request.json()
        inbox_messages.append()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
