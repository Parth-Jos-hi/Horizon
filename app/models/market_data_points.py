import enum
import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import String, Enum, func, DateTime, Float, Date, ForeignKey
from app.db.base import Base
class MetricType(enum.Enum):
    JOB_POSTINGS_COUNT = "job_postings_count"
    AVG_SALARY = "avg_salary"
    UNEMPLOYMENT_RATE = "unemployment_rate"
    SECTOR_GROWTH_RATE = "sector_growth_rate"
class MarketDataPoint(Base):
    __tablename__ = "market_data_points"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    data_source_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("data_sources.id"), nullable=False
    )
    metric_type: Mapped[MetricType] = mapped_column(Enum(MetricType), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    period_date: Mapped[date] = mapped_column(Date, nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    raw_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    def __repr__(self) -> str:
        return (
            f"MarketDataPoint(id={self.id!r}, metric_type={self.metric_type!r}, "
            f"region={self.region!r}, period_date={self.period_date!r}, "
            f"value={self.value!r}, ingested_at={self.ingested_at!r})"
        )