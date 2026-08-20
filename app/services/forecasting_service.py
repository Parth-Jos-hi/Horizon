# services/forecasting_service.py
from datetime import date
from typing import Optional
from uuid import UUID
import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.market_data_points import MarketDataPoint, MetricType
from app.models.forecast import Forecast, Horizon
HORIZON_MONTHS = {
    Horizon.ONE_MONTH: 1,
    Horizon.THREE_MONTH: 3,
    Horizon.ONE_YEAR: 12,
}
def get_historical_window(
    session: Session,
    metric_type: MetricType,
    region: str,
    sector: Optional[str],
    role_category: Optional[str],      
) -> list[MarketDataPoint]:
    stmt = (
        select(MarketDataPoint)
        .where(
            MarketDataPoint.metric_type == metric_type,
            MarketDataPoint.region == region,
            MarketDataPoint.sector == sector,
            MarketDataPoint.role_category == role_category,
        )
        .order_by(MarketDataPoint.period_date)
    )
    return list(session.execute(stmt).scalars().all())
def apply_linear_trend(
    points: list[MarketDataPoint], horizon_months: int
) -> tuple[float, Optional[float], Optional[float]]:
    """v1 [FORECASTING_METHOD]: ordinary least squares over historical
    values, projected forward. Returns (predicted_value, confidence_low,
    confidence_high) — the interval comes from the fit's own standard
    error, not a fabricated number."""
    x = np.array([p.period_date.toordinal() for p in points], dtype=float)
    y = np.array([p.value for p in points], dtype=float)

    slope, intercept = np.polyfit(x, y, deg=1)

    future_ordinal = points[-1].period_date.toordinal() + (horizon_months * 30)
    predicted = slope * future_ordinal + intercept

    residuals = y - (slope * x + intercept)
    std_error = float(np.std(residuals)) if len(residuals) > 2 else None
    confidence_low = predicted - 1.96 * std_error if std_error is not None else None
    confidence_high = predicted + 1.96 * std_error if std_error is not None else None
    return float(predicted), confidence_low, confidence_high
def generate_forecast(
    session: Session,
    metric_type: MetricType,
    region: str,
    sector: Optional[str],
    role_category: Optional[str],
    horizon: Horizon,
    requested_by_user_id: Optional[UUID] = None,
) -> Forecast:
    history = get_historical_window(session, metric_type, region, sector, role_category)

    if len(history) < 2:
        raise ValueError(
            "Not enough historical data to generate a forecast for this combination"
        )

    predicted_value, confidence_low, confidence_high = apply_linear_trend(
        history, HORIZON_MONTHS[horizon]
    )

    forecast = Forecast(
        requested_by_user_id=requested_by_user_id,
        metric_type=metric_type,
        region=region,
        sector=sector,
        role_category=role_category,
        horizon=horizon,
        predicted_value=predicted_value,
        confidence_low=confidence_low,
        confidence_high=confidence_high,
        method="linear_trend_extrapolation",
        based_on_period_start=history[0].period_date,
        based_on_period_end=history[-1].period_date,
    )
    session.add(forecast)
    session.commit()
    session.refresh(forecast)
    return forecast