# main.py

from fastapi import FastAPI
from api import auth_routes

# 1. Vytvoření instance FastAPI aplikace
app = FastAPI(
    title="Šrumec Auth Service",
    description="Mikroslužba pro autentizaci a správu uživatelů.",
    version="0.1.0",
)

app.include_router(auth_routes.router)