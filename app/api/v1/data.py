from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.market_data_points import MarketDataPoint, MetricType
from app.models.user import User
from app.schemas.data import DataPointResponse
router = APIRouter()
@router.get("/data", response_model=list[DataPointResponse])
def list_data_points(
    region: Optional[str] = None,
    sector: Optional[str] = None,
    role_category: Optional[str] = None,
    metric_type: Optional[MetricType] = None,
    page: int = Query(1, ge=1),         
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = select(MarketDataPoint)
    if region:
        data = data.where(MarketDataPoint.region == region)
    if sector:
        data = data.where(MarketDataPoint.sector==sector)
    if role_category:
        data = data.where(MarketDataPoint.role_category==role_category)
    if metric_type:
        data = data.where(MarketDataPoint.metric_type==metric_type)
    data = data.offset((page - 1) * limit).limit(limit)
    return db.execute(data).scalars().all()
@router.get("/data/{id}",response_model = DataPointResponse)
def get_current_user(user_id:UUID,
        db:Session=Depends(get_db),
        current_user:User = Depends(get_current_user),
        ):
    user = db.get(MarketDataPoint,id)
    if user in None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User is not in the data list",
        )
    return user
