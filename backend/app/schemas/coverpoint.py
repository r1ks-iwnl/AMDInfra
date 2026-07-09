from pydantic import BaseModel, ConfigDict, Field
from .bin import BinOut

class CoverpointOut(BaseModel):
    name: str = Field(..., examples=["cp_vec"], description="Name of the hardware coverpoint")
    coverage: float = Field(..., examples=[85.5], description="Coverage percentage for this coverpoint")
    total_bins: int = Field(..., examples=[16], description="Total bins defined in this coverpoint")
    missed_bins: int = Field(..., examples=[2], description="Number of bins with zero hits")
    bins: list[BinOut] = Field(default=[], description="List of bins associated with this coverpoint")
    
    model_config = ConfigDict(from_attributes=True)
