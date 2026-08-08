from uuid import UUID
from pydantic import BaseModel,ConfigDict
from typing import List
from datetime import datetime
class CareerPathResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id:UUID
    user_id : UUID
    profile_id:UUID
    declining_signals:List[dict]
    rising_signals:List[dict]
    recomended_path:str
    based_on_forecasts_ids:List[UUID]
    based_on_signal_ids:List[UUID]
    generated_at:datetime
