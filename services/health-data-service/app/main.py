from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from shared.config import settings
from shared.database import Base, engine
from app.api.endpoints import health

# Create database tables if they don't exist
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass  # Tables might already exist

app = FastAPI(
    title="Health Data Service",
    version=settings.APP_VERSION,
    description="Health Data Management Microservice",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/health", tags=["Health"])


@app.get("/")
async def root():
    return {
        "service": "health-data-service",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "health-data-service"}

