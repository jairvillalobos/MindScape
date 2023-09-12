"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.models import Base
import logging

# Tus detalles de la base de datos
DATABASE_URL = "postgresql://postgres:postgres@localhost/mindscape"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger(__name__)

def create_tables():
    # Crea todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)
    logger.info("Las tablas se crearon correctamente")
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # take environment variables from .env.

# Tus detalles de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Hubo un error al acceder a la base de datos: {e}")
    finally:
        db.close()

