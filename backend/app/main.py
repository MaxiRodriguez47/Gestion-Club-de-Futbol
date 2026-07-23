from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models  # importa todos los modelos antes de create_all
from app.routers import jugadores, socios, partidos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Club de Fútbol API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # origen del frontend (Vite)
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jugadores.router)
app.include_router(socios.router)
app.include_router(partidos.router)
