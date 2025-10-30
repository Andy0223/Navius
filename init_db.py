#!/usr/bin/env python3
"""
Database initialization script
"""
from app.core.database import Base, engine
from app.models import user, health_data

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")


if __name__ == "__main__":
    init_db()

