from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import logging
import enum

from app.core.config import settings
from app.db.mock_data import load_mock_data, get_user_profiles
from app.db.database import SessionLocal, engine, Base, initialize_database, query_alle, insert_into_database, query_by_id, delete_from_database_by_id
from app.api.models import XAnfrage, XAusschreibung, XUnternehmen, XVorschlag

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
        logger.info("Database tables created or already exist.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
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


def get_db():
    # handle database sessions (provide and close)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Tags(enum.Enum):
    AUSSCHREIBUNG = "ausschreibung"
    UNTERNEHMEN = "unternehmen"
    ANFRAGE = "anfrage"
    VORSCHLAG = "vorschlag"


router_ausschreibung = APIRouter(
    prefix=f"/api/v1/{Tags.AUSSCHREIBUNG.value}", tags=[Tags.AUSSCHREIBUNG.name.capitalize()])
router_unternehmen = APIRouter(
    prefix=f"/api/v1/{Tags.UNTERNEHMEN.value}", tags=[Tags.UNTERNEHMEN.name.capitalize()])
router_anfrage = APIRouter(
    prefix=f"/api/v1/{Tags.ANFRAGE.value}", tags=[Tags.ANFRAGE.name.capitalize()])
router_vorschlag = APIRouter(
    prefix=f"/api/v1/{Tags.VORSCHLAG.value}", tags=[Tags.VORSCHLAG.name.capitalize()])


@app.get("/api/v1/", tags=["Root"])
def read_root():
    # health check
    return {"message": "Willkommen zur KMU Ausschreibungsplattform API v1"}


@app.on_event("startup")
async def startup_event():
    # initialize database on app start
    logger.info("Application startup event triggered.")
    create_db_tables()
    user_profile, inbox_messages, tenders = load_mock_data()
    logger.info("Database tables checked/created. Application ready.")


@router_ausschreibung.get("/")
def get_tenders():
    return query_alle("ausschreibung")


@router_ausschreibung.get("/{tender_id}")
def get_tender_by_id(tender_id: int):
    return query_by_id("ausschreibung", tender_id)


@router_unternehmen.get("/")
def get_profile():
    return query_alle("unternehmen")


@router_unternehmen.get("/{unternehmen_id}")
def get_profile_by_id(unternehmen_id: int):
    return query_by_id("unternehmen", unternehmen_id)


@router_vorschlag.get("/")
def get_inbox():
    return query_alle("vorschlag")


@router_vorschlag.get("/{inbox_id}")
def get_message_by_id(inbox_id: int):
    return query_by_id("vorschlag", inbox_id)


@router_anfrage.get("/")
def get_inquiries():
    return query_alle("anfrage")


@router_anfrage.get("/{anfrage_id}")
def get_anfrage_by_id(anfrage_id: int):
    return query_by_id("anfrage", anfrage_id)


@router_vorschlag.get("/{message_id}")
def get_inbox(message_id: int):
    return find_list_entry(inbox_messages, "id", message_id)


@router_ausschreibung.post("/")
def write_tender_to_database(data: XAusschreibung):
    insert_into_database(Tags.AUSSCHREIBUNG.value, data)


@router_unternehmen.post("/")
def write_profile_to_database(data: XUnternehmen):
    insert_into_database(Tags.UNTERNEHMEN.value, data)


@router_anfrage.post("/")
def write_anfrage_to_database(data: XAnfrage):
    insert_into_database("anfrage", data)


@router_vorschlag.post("/")
def write_inbox_to_database(data: XVorschlag):
    insert_into_database("inbox", data)


@router_unternehmen.post("/{profile_id}")
def switch_profile(profile_id: int):
    global user_profile
    try:
        user_profile = find_list_entry(user_profiles, "id", profile_id)
        msg = "Profile update successfully"
    except IndexError as e:
        msg = f"Profile update FAILED: {e}"
    return {"message": msg}


@router_unternehmen.delete("/{profile_id}")
def delete_profile(profile_id: int):
    entry = delete_from_database_by_id("unternehmen", profile_id)
    return {"message": "Profile deleted successfully", "body": entry}


@router_anfrage.delete("/{profile_id}")
def delete_profile(profile_id: int):
    entry = delete_from_database_by_id("anfrage", profile_id)
    return {"message": "Profile deleted successfully", "body": entry}


@router_ausschreibung.delete("/{profile_id}")
def delete_profile(profile_id: int):
    entry = delete_from_database_by_id("ausschreibung", profile_id)
    return {"message": "Profile deleted successfully", "body": entry}


@router_vorschlag.delete("/{profile_id}")
def delete_profile(profile_id: int):
    entry = delete_from_database_by_id("vorschlag", profile_id)
    return {"message": "Profile deleted successfully", "body": entry}


@router_unternehmen.post("/default")
async def reset_default_profile():
    global user_profile
    user_profile, _, _ = load_mock_data()
    return {"message": "User profile was reset to default values."}


app.include_router(router_anfrage)
app.include_router(router_ausschreibung)
app.include_router(router_unternehmen)
app.include_router(router_vorschlag)
