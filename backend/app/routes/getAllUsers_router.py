from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.db_connection import get_db_session as get_db
from models.user_model import User


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(db: Session = Depends(get_db)):
    """Récupère tous les utilisateurs de la base de données"""
    users = db.query(User).all()
    
    # Formatter les utilisateurs sans exposer les mots de passe
    users_list = [
        {"id": user.id, "username": user.username} 
        for user in users
    ]
    
    return {
        "total_users": len(users_list),
        "users": users_list
    }
