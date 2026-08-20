from typing import Optional
from uuid import UUID
from sqlalchemy import Select
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from app.services.forecasting_service import get_historical_window
from app.models.market_data_points import MarketDataPoint, MetricType
# from app.dependencies import get_db, get_current_user
router = APIRouter()
@router.get("/forecast",response_model = list[get_historical_window])
def list_forecast(
    db:Session,
    metric_type : Optional[MetricType] = None,
    region : Optional[str] = None,
    sector:Optional[str] = None,
    role_category:Optional[str] = None,
    page: int = Query(1, ge=1),         
    limit: int = Query(50, ge=1, le=200),
):
    data = Select(MarketDataPoint)
    if metric_type:
        data = data.where(MarketDataPoint.metric_type == metric_type)
    if region:
        data = data.where(MarketDataPoint.metric_type == region)
    if sector:
        data = data.where(MarketDataPoint.metric_type == sector)
    if role_category:
        data = data.where(MarketDataPoint.metric_type == role_category)
    
    data = data.offset((page - 1) * limit).limit(limit)
    return db.execute(data).scalars().all()