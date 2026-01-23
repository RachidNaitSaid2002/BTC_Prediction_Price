from fastapi import FastAPI
from routes import getAllUsers_router, login_router, prediction_router, register_router, analyis_router, analyis_daily_volume_router
from db.db_connection import Base, engine

# Créer l'application
app = FastAPI()

Base.metadata.create_all(bind=engine)


# Inclure les routers
app.include_router(login_router.router)
app.include_router(register_router.router)
app.include_router(getAllUsers_router.router)
app.include_router(prediction_router.router)
app.include_router(analyis_router.router)
app.include_router(analyis_daily_volume_router.router)