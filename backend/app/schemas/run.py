from pydantic import BaseModel, ConfigDict, Field, computed_field
from .coverpoint import CoverpointOut
from datetime import datetime

class RunSummary(BaseModel):
    id: int = Field(..., examples=[1], description="Database assigned unique ID")
    filename: str = Field(..., examples=["78_5_overall_FCOV.txt"], description="Log file name")
    run_date: datetime = Field(..., examples=["2026-07-08T14:30:00"], description="Date and time of run")
    result: str = Field(..., examples=["PASSED", "FAILED"], description="Result of run")
    overall_coverage: float = Field(..., examples=[78.5], description="Total functional coverage percentage")
    
    model_config = ConfigDict(from_attributes=True)


# inherits summary fields so the detail response also identifies which run it is
class RunDetail(RunSummary):
    checks: int = Field(..., examples=[1450], description="Number of checks ran")
    uploaded_at: datetime = Field(..., examples=["2026-07-08T18:11:00"], description="Timestamp at the moment of upload")
    uploaded_by: str | None = Field(None, examples=["john.doe@gmail.com"], description="Uploader's email address")
    coverpoints: list[CoverpointOut] = Field(description="Complete list of coverpoints associated with run")
    
    model_config = ConfigDict(from_attributes=True)

    @computed_field(description="Total bins across all coverpoints")
    @property
    def total_bins(self) -> int:
        return sum(cp.total_bins for cp in self.coverpoints)

    @computed_field(description="Number of bins with zero hits")
    @property
    def missed_bins(self) -> int:
        return sum(cp.missed_bins for cp in self.coverpoints)
