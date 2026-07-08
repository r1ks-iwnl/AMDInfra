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

# inherits summary fields so the detail response also identifies which run it is
class RunDetail(RunSummary):
    checks: int
    uploaded_at: datetime
    uploaded_by: str | None
    total_bins: int
    missed_bins: int
    coverpoints: list[CoverpointOut] = []
    model_config = ConfigDict(from_attributes=True)
