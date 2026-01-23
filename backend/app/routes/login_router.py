from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from sqlalchemy.orm import Session

from auth.token_auth import create_access_token
from core.config import settings
from db.db_connection import get_db_session as get_db
from models.user_model import User
from schemas.LoginRequest_schema import LoginRequest
from schemas.Token_schema import Token


router = APIRouter(prefix="/auth", tags=["Login"])


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

    return {
        "message": "Login réussi",
        "access_token": access_token,
    }
