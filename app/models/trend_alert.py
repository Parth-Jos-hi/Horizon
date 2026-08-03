import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import func, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class TrendAlert(Base): 
    __tablename__ = "trend_alerts"  
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=func.uuid_generate_v4()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_profiles.id"),
        nullable=False
    )
    summary: Mapped[str] = mapped_column(  
        Text,
        nullable=False
    )
    based_on_signal_ids: Mapped[List[uuid.UUID]] = mapped_column(JSONB, nullable=False)
    triggered_reason: Mapped[Optional[str]] = mapped_column(  
        Text,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  
        nullable=False
    )
    def __repr__(self) -> str:
        return (
            f"TrendAlert(id={self.id!r}, user_id={self.user_id!r}, "
            f"profile_id={self.profile_id!r}, created_at={self.created_at!r})"
        )