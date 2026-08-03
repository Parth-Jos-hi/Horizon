from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column
import uuid
from typing import List
from datetime import datetime
from sqlalchemy import func,ForeignKey,Text,DateTime
from sqlalchemy.dialects.postgresql import UUID,JSONB,ARRAY
# from app.models import user
class career_paths(Base):
    __tablename__ = "career_path"
    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=func.uuid_generate_v4()
        )
    user_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("user.id"),
            nullable=False
        )
    profile_id: Mapped[uuid.UUID] = mapped_column(
                ForeignKey("user_profile.id"),
                nullable=False
            )
    declining_signals:Mapped[dict] = mapped_column(JSONB,nullable  = False)
    rising_signals:Mapped[dict] = mapped_column(JSONB,nullable  = False)
    recomended_path:Mapped[Text] = mapped_column(Text,nullable = False)
    based_on_forecast_ids: Mapped[List[uuid.UUID]] = mapped_column(JSONB, nullable=False)
    based_on_signal_ids: Mapped[List[uuid.UUID]] = mapped_column(JSONB, nullable=False)
    generated_at:Mapped[datetime] = mapped_column(DateTime(timezone = True),server_default = func.now(),nullable = False)

    