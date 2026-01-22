from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..db.db_connection import get_db_session as get_db
from backend.app.models.user_model import User
from backend.app.schemas.LoginRequest_schema import LoginRequest


router = APIRouter(prefix="/auth", tags=["Registration"])


@router.post("/register")
def register(request: LoginRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet utilisateur existe déjà"
        )
    
    new_user = User(
        username=request.username,
        password=request.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "Utilisateur créé avec succès",
        "user_id": new_user.id,
        "username": new_user.username
    }
