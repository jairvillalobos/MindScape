# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.models import Base

# Tus detalles de la base de datos
DATABASE_URL = "postgresql://postgres:postgres@localhost/mindscape"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    # Crea todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)
