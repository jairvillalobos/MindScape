# main.py
from fastapi import FastAPI
from infrastructure.database import create_tables

app = FastAPI()

create_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}
