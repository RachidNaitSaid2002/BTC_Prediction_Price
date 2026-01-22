from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SK: str
    ALG: str = "HS256"
    HF_TOKEN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DB_HOST: str 
    DB_PORT: int 
    DB_NAME: str 
    DB_USER: str 
    DB_PASSWORD: str 
    
    # Chemin correct pour le modèle dans le conteneur
    MODEL_PATH: str = "/app/ml/Machine Learning/model/bitcoin_pipeline_model"

    model_config = {
        "extra": "ignore",
        "env_file": ".env",
        "case_sensitive": True
    }

settings = Settings()