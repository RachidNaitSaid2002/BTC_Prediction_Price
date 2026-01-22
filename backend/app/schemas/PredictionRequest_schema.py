from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PredictRequest(BaseModel):
    # Features numériques
    MA_5: float = Field(..., description="Moyenne mobile 5 périodes")
    high: float = Field(..., description="Prix le plus haut")
    low: float = Field(..., description="Prix le plus bas")
    open: float = Field(..., description="Prix d'ouverture")
    close: float = Field(..., description="Prix de clôture")
    MA_10: float = Field(..., description="Moyenne mobile 10 périodes")
    prev_close: float = Field(..., description="Clôture précédente")
    return_val: float = Field(..., alias="return", description="Retour")
    
    class Config:
        populate_by_name = True  
        json_schema_extra = {
            "example": {
                "MA_5": 45100.00,
                "high": 45500.00,
                "low": 44800.00,
                "open": 45000.50,
                "close": 45200.00,
                "MA_10": 45050.00,
                "prev_close": 45000.00,
                "return": 0.0044
            }
        }

class PredictResponse(BaseModel):
    predicted_price: float = Field(..., description="Prix prédit")
    timestamp: datetime = Field(default_factory=datetime.now)
    prediction_id: Optional[int] = None
    