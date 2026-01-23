from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.db_connection import get_db_session
from auth.token_auth import get_current_user


router = APIRouter(prefix="/Analys", tags=["Analytics"])


@router.get("/daily_volume")
def get_daily_volume(rdb: Session = Depends(get_db_session), user_id: dict = Depends(get_current_user)):
    result = rdb.execute(text("""
        SELECT
            DATE(open_time) AS day,
            SUM(volume) AS total_volume
        FROM silver_data_test
        GROUP BY day
        ORDER BY day;
    """))
    return result.mappings().all()
