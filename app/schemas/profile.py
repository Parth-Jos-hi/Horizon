from uuid import UUID
from pydantic import BaseModel,ConfigDict
from datetime import date,datetime
from typing import Optional,List
class Profile_response(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id:UUID
    user_id:UUID
    source_filename:Optional[str]=None
    current_role:Optional[str]=None
    field: Optional[str] = None
    region: Optional[str] = None
    skills: Optional[List[str]] = None
    years_experience: Optional[float] = None
    uploaded_at: datetime
    parsed_at: Optional[datetime] = None


class ProfileUploadAccepted(BaseModel):
    """Returned immediately by POST /profile/upload, before the pipeline
    finishes — assumes async/polling per horizon-api-design.md's open
    decision. If you build it as a blocking call instead, this schema
    isn't needed; ProfileResponse would be returned directly instead."""
    id: UUID
    status: str = "processing"
    uploaded_at: datetime