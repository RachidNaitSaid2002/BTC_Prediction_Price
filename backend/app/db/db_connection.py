# Database connection configuration
#* app/db/db_connection.py 

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings
import os

Base = declarative_base()

# Pour psycopg2 
def get_db_connection():
    # Connexion PostgreSQL avec psycopg2
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    return conn

# Pour SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

def get_db_session():
    # Générateur de session SQLAlchemy
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()