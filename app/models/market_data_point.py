import uuid
import enum
from sqlalchemy import String ,Enum,func,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models import data_source
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
class MetricType(enum.Enum):
    JOBPOSTINGCOUNT ="count"
    AVGSALARY = "avg_salary"
    UNEMPLOYMENT_RATE = "unemployment_rate"
    SECTORGROWTH = "growthbysector"
class MarketDataPoints(Base):
    __tablename__ = "market_data_points"
    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable = False,
        primary_key = True,
        server_default = func.uuid_generate_v4()
    )
    data_source_id:Mapped[int] = mapped_column(ForeignKey("data_source.id"))
    metric_type:Mapped[MetricType] =  mapped_column(Enum(MetricType),nullable = False)
    region:Mapped[str] = mapped_column(String(55))
    sector:Mapped[str] = mapped_column(String(55),nullable = False)
    role_category:Mapped[str] = mapped_column(String(55),nullable = False)
    value :Mapped[int] = mapped_column(default = 0)
    period_date:Mapped[]


