"""ReadFlow FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS

from app.database import Base, engine
# Import models so SQLAlchemy registers all table definitions before create_all.
from app import models as _models  # noqa: F401
from app.routers import analytics, badges, books, logs, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convenient schema initialization for the college MVP.
    # For a production deployment, replace create_all with Alembic migrations.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="ReadFlow API",
    description="Backend API for the ReadFlow reading habit tracker",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(logs.router)
app.include_router(analytics.router)
app.include_router(badges.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to ReadFlow API", "status": "running"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "ReadFlow Backend"}
