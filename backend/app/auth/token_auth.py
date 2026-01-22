from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from ..core.config import settings
from backend.app.schemas.Token_schema import TokenData, Token

security = HTTPBearer()





def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Créer un token JWT
    
    Args:
        data: Données à encoder dans le token
        expires_delta: Durée de validité du token (optionnel)
    
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, settings.SK, algorithm=settings.ALG)


def create_token(user_id: int) -> str:
    """
    Créer un token JWT (ancienne fonction, gardée pour rétrocompatibilité)
    
    Args:
        user_id: ID de l'utilisateur
    
    Returns:
        Token JWT encodé
    """
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, settings.SK, algorithm=settings.ALG)


def verify_token(token: str) -> TokenData:
    """
    Vérifier et décoder un token JWT
    
    Args:
        token: Token JWT à vérifier
    
    Returns:
        TokenData avec les informations de l'utilisateur
    
    Raises:
        HTTPException: Si le token est invalide ou expiré
    """
    try:
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
        user_id: int = payload.get("user_id")
        username: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token invalide"
            )
        
        return TokenData(user_id=user_id, username=username)
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expiré"
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide"
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Dépendance FastAPI pour récupérer l'utilisateur actuel depuis le token JWT
    
    Args:
        credentials: Credentials HTTP Bearer
    
    Returns:
        user_id de l'utilisateur authentifié
    
    Raises:
        HTTPException: Si le token est invalide ou expiré
    """
    token = credentials.credentials
    token_data = verify_token(token)
    return token_data.user_id