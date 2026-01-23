from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.db_connection import get_db_session
from auth.token_auth import get_current_user


router = APIRouter(prefix="/Analys", tags=["Analytics"])


@router.post("/")
def get_avg_close_hour(rdb: Session = Depends(get_db_session), user_id: dict = Depends(get_current_user)):
    """Analyse endpoint"""
    try:
          result = rdb.execute(text("""
            WITH avg_hour AS (
                SELECT 
                    EXTRACT(HOUR FROM open_time) AS hour,
                    AVG(close) AS avg_close
                FROM silver_data_test
                GROUP BY 1
            )
            SELECT hour, avg_close
            FROM avg_hour
            ORDER BY hour;
        """))

    except Exception as e:
        rdb.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

    return result.mappings().all()