from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy.orm import Session
from app.auth.token_auth import create_access_token, Token
from app.core.config import settings
from ..db.db_connection import get_db_session as get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    """Modèle de requête pour le login"""
    username: str
    password: str


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or user.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id
        },
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


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


@router.get("/me")
def get_me(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    return {
        "message": "Pour obtenir vos infos, utilisez le token dans Authorization header",
        "total_users": total_users,
        "token_expires_in_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }