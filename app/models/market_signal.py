import uuid
from datetime import date, datetime
import enum
from typing import Optional
from sqlalchemy import String, Enum, func, DateTime, Date, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class MetricType(enum.Enum):
    JOB_POSTINGS_COUNT = "job_postings_count"
    AVG_SALARY = "avg_salary"
    UNEMPLOYMENT_RATE = "unemployment_rate"
    SECTOR_GROWTH_RATE = "sector_growth_rate"
class MarketDataPoint(Base):
    __tablename__ = "market_data_points"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=func.uuid_generate_v4(),  
    )
    data_source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("data_sources.id"), nullable=False
    )
    metric_type: Mapped[MetricType] = mapped_column(Enum(MetricType), nullable=False)
    region: Mapped[str] = mapped_column(String(55), nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    role_category: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    period_date: Mapped[date] = mapped_column(Date, nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    raw_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)