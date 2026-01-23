from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.db_connection import Base

class BitcoinPrediction(Base):
    __tablename__ = "bitcoin_predictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Features d'entrée
    MA_5 = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    open = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    MA_10 = Column(Float, nullable=False)
    prev_close = Column(Float, nullable=False)
    return_val = Column(Float, nullable=False)

    # Prédiction
    predicted_price = Column(Float, nullable=False)
    
    # Timestamp et user
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)