from app.db.base import Base
import uuid
from datetime import datetime
from sqlalchemy import func,String,ForeignKey,Text,DateTime,Float
from sqlalchemy.dialects.postgresql import UUID,JSONB
from typing import Optional
from sqlalchemy.orm import mapped_column,Mapped
class User_Profile(Base):
    __tablename__ ="user_profile"
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True),nullable = True,server_default = func.uuid_generate_v4())
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"),nullable =False)
    source_filename:Mapped[str]=mapped_column(String(100),nullable = True)
    original_file_storage_key:Mapped[str]=mapped_column(String(100),nullable = True)
    raw_text:Mapped[Text] = mapped_column(Text)
    current_role:Mapped[str] = mapped_column(String(100))
    field:Mapped[str]= mapped_column(String(50))   
    region:Mapped[str] = mapped_column(String(50))
    skills:Mapped[dict] = mapped_column(JSONB,nullable = True)
    years_experience: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    parsed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    last_checked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
