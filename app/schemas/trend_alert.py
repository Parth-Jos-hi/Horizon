from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,ConfigDict
from typing import List,Optional
class TrendAlertResponse(BaseModel):
    id:UUID
    user_id:UUID
    profile_id:str
    summary:str
    based_on_signal_ids:List[UUID]
    triggered_reason:Optional[str]= None
    created_at:datetime

