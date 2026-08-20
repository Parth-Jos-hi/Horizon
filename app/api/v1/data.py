from fastapi import FastAPI,APIRouter
from app.models import market_data_points
from typing import Optional
app = FastAPI()
@app.get("/data")
def market_data(region:Optional[str]=None,sector:Optional[str]=None,
                role_category=Optional[str]=None,metric_type=Enum):
    