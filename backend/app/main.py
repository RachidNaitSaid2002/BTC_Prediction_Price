from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import prediction_router, auth_router
from app.db.db_connection import engine, Base
from app.services.prediction_service import get_prediction_service
    


# Créer l'application
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclure les routers
app.include_router(auth_router.router)
app.include_router(prediction_router.router)