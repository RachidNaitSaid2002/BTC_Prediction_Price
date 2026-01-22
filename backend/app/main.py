from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes import getAllUsers_router, login_router, prediction_router, register_router


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
app.include_router(login_router.router)
app.include_router(register_router.router)
app.include_router(getAllUsers_router.router)
app.include_router(prediction_router.router)
