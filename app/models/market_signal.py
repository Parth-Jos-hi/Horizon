import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, func, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class MarketSignal(Base):
    __tablename__ = "market_signals"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=func.uuid_generate_v4()
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_profiles.id"),
        nullable=False
    )
    query: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    relevance: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    def __repr__(self) -> str:
        return (
            f"MarketSignal(id={self.id!r}, profile_id={self.profile_id!r}, "
            f"query={self.query!r}, discovered_at={self.discovered_at!r})"
        )
    