from fastapi import FastAPI
from infrastructure.database import SessionLocal, engine
from domain.models import Base

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Crear una nueva sesión de base de datos al iniciar la aplicación
    app.state.db = SessionLocal()

@app.on_event("shutdown")
async def shutdown():
    # Cerrar la sesión de base de datos al cerrar la aplicación
    app.state.db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Aquí puedes agregar tus rutas/endpoints
