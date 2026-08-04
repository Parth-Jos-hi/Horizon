import uuid
from datetime import datetime
from typing import List
from sqlalchemy import func, String, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class CareerPath(Base):
    __tablename__ = "career_paths"
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
    declining_signals: Mapped[dict] = mapped_column(JSONB, nullable=False)
    rising_signals: Mapped[dict] = mapped_column(JSONB, nullable=False)
    recommended_path: Mapped[str] = mapped_column(Text, nullable=False)
    based_on_forecast_ids: Mapped[List[uuid.UUID]] = mapped_column(JSONB, nullable=False)
    based_on_signal_ids: Mapped[List[uuid.UUID]] = mapped_column(JSONB, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    def __repr__(self) -> str:
        return (
            f"CareerPath(id={self.id!r}, user_id={self.user_id!r}, "
            f"profile_id={self.profile_id!r}, generated_at={self.generated_at!r})"
        )