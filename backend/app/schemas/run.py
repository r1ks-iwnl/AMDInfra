from pydantic import BaseModel, ConfigDict
from .coverpoint import CoverpointOut
from datetime import datetime

class RunSummary(BaseModel):
    id: int
    filename: str
    run_date: datetime
    result: str
    overall_coverage: float
    model_config = ConfigDict(from_attributes=True)

class RunDetail(BaseModel):
    checks: int
    uploaded_at: datetime
    uploaded_by: str | None
    total_bins: int
    missed_bins: int
    coverpoints: list[CoverpointOut] = []
    model_config = ConfigDict(from_attributes=True)