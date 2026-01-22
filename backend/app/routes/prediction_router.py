from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas.PredictionRequest_schema import PredictRequest, PredictResponse
from services.prediction_service import get_prediction_service
from models.prediction_model import BitcoinPrediction
from db.db_connection import get_db_session
from auth.token_auth import get_current_user


router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/", response_model=PredictResponse)
def predict_price(request: PredictRequest,db: Session = Depends(get_db_session),user_id: int = Depends(get_current_user)):
    """Prédit le prix """
    try:
        service = get_prediction_service()
        
        # Prédire
        predicted_price = service.predict(request)
        
        # Sauvegarder en DB
        prediction = BitcoinPrediction(
            MA_5=request.MA_5,
            high=request.high,
            low=request.low,
            open=request.open,
            close=request.close,
            MA_10=request.MA_10,
            prev_close=request.prev_close,
            return_val=request.return_val,
            predicted_price=predicted_price,
            user_id=user_id
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return PredictResponse(
            predicted_price=round(predicted_price, 2),
            timestamp=prediction.timestamp,
            prediction_id=prediction.id
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
