from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from shared.config import settings
from shared.database import Base, engine
from app.api.endpoints import ai

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Service",
    version=settings.APP_VERSION,
    description="AI/ML Microservice for Health Plans",
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

app.include_router(ai.router, prefix="/api/ai", tags=["AI"])


@app.get("/")
async def root():
    return {
        "service": "ai-service",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-service"}

