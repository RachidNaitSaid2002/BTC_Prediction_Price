from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Modèle de réponse pour le token"""
    message: str
    access_token: str


class TokenData(BaseModel):
    """Données extraites du token"""
    user_id: Optional[int] = None
    username: Optional[str] = None