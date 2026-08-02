import enum
import uuid
from datetime import datetime,date
from sqlalchemy import String,Enum,func,DateTime,ForeignKey,Float,Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
from app.models import user
from typing import Optional
from app.models.market_data_points import MetricType
class Horizon(enum.Enum):
    ONE_MONTH="ONE_MONTH"
    THREE_MONTHS = "three_months"
    ONE_YEAR = "ONE_YEAR"
class Forecasts(Base):
    __tablename__ = "forecasts"
    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        nullable = False,
        server_default = func.uuid_generate_v4()
        )
    requested_by_user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"),nullable = True)
    metric_type:Mapped[MetricType] = mapped_column(Enum(MetricType),nullable = False)
    region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sector: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    horizon: Mapped[Horizon] = mapped_column(Enum(Horizon), nullable=False)
    predicted_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_low: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence_high: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    method: Mapped[str] = mapped_column(String(100), nullable=False)
    based_on_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    based_on_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone = True),server_default = func.now(),nullable = False)
    def __repr__(self)->str:
        return (
            f"Forecast(id={self.id!r}, metric_type={self.metric_type!r}, "
            f"region={self.region!r}, sector={self.sector!r}, "
            f"horizon={self.horizon!r}, predicted_value={self.predicted_value!r}, "
            f"created_at={self.created_at!r})"
        )








                                                       