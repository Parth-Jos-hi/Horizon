from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.market_data_points import MetricType
from app.models.forecast import Horizon
from app.services.forecasting_service import 
class ForecastCreate(BaseModel):
    metric_type: MetricType
    region: str
    sector: Optional[str] = None
    role_category: Optional[str] = None
    horizon: Horizon
class ForecastResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    requested_by_user_id: Optional[UUID] = None
    metric_type: MetricType
    region: str
    sector: Optional[str] = None
    role_category: Optional[str] = None
    horizon: Horizon
    predicted_value: float
    confidence_low: Optional[float] = None
    confidence_high: Optional[float] = None
    method: str
    based_on_period_start: date
    based_on_period_end: date
    created_at: datetime