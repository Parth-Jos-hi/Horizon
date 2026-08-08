import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models.market_data_points import MetricType
class DataPointResponse(BaseModel):
    """
    Schema for responding with a single MarketDataPoint.
    Mirrors the fields of models/market_data_point.py directly.
    """
    id: int = Field(..., description="Unique identifier for the data point.")
    data_source_id: int = Field(..., description="Identifier of the source of this data.")
    metric_type: MetricType = Field(..., description="The type of metric recorded (e.g., salary, headcount).")
    region: str = Field(..., description="The geographical region the data point pertains to.")
    sector: Optional[str] = Field(None, description="The industry sector (optional).")
    role_category: Optional[str] = Field(None, description="The category of role (optional).")
    value: float = Field(..., description="The numeric value of the data point.")
    period_date: datetime.date = Field(..., description="The date to which the data point's value pertains.")
    ingested_at: datetime.datetime = Field(..., description="Timestamp when the data point was ingested.")
    raw_metadata: dict = Field(..., description="Raw, unparsed metadata associated with the data point.")
    class Config:
        # This setting tells Pydantic to read data directly from Python object attributes
        from_attributes = True
        # This provides example data for API documentation tools (like FastAPI's Swagger UI).
        json_schema_extra = {
            "example": {
                "id": 1,
                "data_source_id": 101,
                "metric_type": "salary",
                "region": "EMEA",
                "sector": "Tech",
                "role_category": "Engineering",
                "value": 120000.0,
                "period_date": "2023-01-01",
                "ingested_at": "2023-01-05T10:30:00Z",
                "raw_metadata": {"source_file": "report_q1_2023.csv", "original_value": "120k"},
            }
        }