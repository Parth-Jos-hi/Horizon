import uuid
from datetime import datetime
import enum
from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String , Enum,func,DateTime
from typing import Optional
class source(enum.Enum):
    API="api",
    SCRAPER="scraper",
    upload= "csv_upload"

class data_sources(Base):
    __tablename__ = "Info_source"
    id : Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key = True,
    nullable = False,
    server_default = func.uuid_generate_v4() 
    )
    name:Mapped[str] = mapped_column(
        String(30),
        nullable = False
        )
    source_type : Mapped[source] = mapped_column(
        Enum(source),
        nullable = False
        )
    refrence_url:Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable = False
        )
    last_synced_at:Mapped[DateTime] = mapped_column(
        DateTime(TimeZone = True),
        server_default = func.now(),
        onupdate=func.now(),
        nullable = False
        )
    enabled:Mapped[bool] = mapped_column(default = True)
    created_at:Mapped[DateTime] = mapped_column(
        DateTime(TimeZone = True)
        ,server_default = func.now()
        ,nullable = False)
