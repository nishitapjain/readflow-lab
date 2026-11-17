"""Application settings loaded from environment variables."""

import os
from dotenv import load_dotenv

# Loads backend/.env when the server is started from the backend directory.
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/readflow",
)
APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Asia/Kolkata")
APP_ENV = os.getenv("APP_ENV", "development")

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    if origin.strip()
]
