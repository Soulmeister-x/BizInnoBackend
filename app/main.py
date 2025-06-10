from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
import logging

# import settings and data models
from app.core.config import settings
from app.db.mock_data import mock_data
# from app.db.database import SessionLocal, engine, Base
# from app.api import auth, companies, tenders, ingestion # Importiert die Router-Objekte aus den Modulen

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_db_tables():
    logger.info("Attempting to create database tables...")
    try:
        # TODO: use after engine is defined
        # Base.metadata.create_all(bind=engine)
        logger.info("Database tables created or already exist.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # TODO: add valid error handling and potential retry methods


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Prototyp für KMU-Ausschreibungsplattform",
    # TODO: add contact, license
)

# allow CORS to allow frontend request this service
origins = [
    "http://localhost:5173",  # default-port for Svelte-Dev-Server
    "http://localhost:8000",
    # TODO: add frontend url
    # "https://your-svelte-frontend-on-vercel.vercel.app",
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

# health check


@app.get("/api/v1/", tags=["Root"])
def read_root():
    return {"message": "Willkommen zur KMU Ausschreibungsplattform API v1"}

# initialize database on app start


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup event triggered.")
    create_db_tables()
    logger.info("Database tables checked/created. Application ready.")


@app.get("/api/v1/tenders")
def get_tenders():
    return mock_data
