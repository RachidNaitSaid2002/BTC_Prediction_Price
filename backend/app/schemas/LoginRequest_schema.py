from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Modèle de requête pour le login"""
    username: str
    password: str