# app/db/models/data_source.py
import enum
import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum, func, DateTime
from app.db.base import Base
class SourceType(enum.Enum):
    API = "api"
    SCRAPER = "scraper"
    UPLOAD = "csv_upload"  
class DataSource(Base):
    __tablename__ = "data_sources"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=func.uuid_generate_v4(),
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    source_type: Mapped[SourceType] = mapped_column(
        Enum(SourceType), nullable=False
    )
    reference_url: Mapped[str] = mapped_column(String(255), nullable=True)
    last_synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    enabled: Mapped[bool] = mapped_column(default=True)

    # Timestamp when the data source record was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    def __repr__(self) -> str:
        return (
            f"DataSource(id={self.id!r}, name={self.name!r}, "
            f"source_type={self.source_type!r}, created_at={self.created_at!r})"
        )