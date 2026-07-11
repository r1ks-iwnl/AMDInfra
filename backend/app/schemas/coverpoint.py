from pydantic import BaseModel, ConfigDict, Field, computed_field
from .bin import BinOut

class CoverpointOut(BaseModel):
    name: str = Field(..., examples=["cp_vec"], description="Name of the hardware coverpoint")
    coverage: float = Field(..., examples=[85.5], description="Coverage percentage for this coverpoint")
    bins: list[BinOut] = Field(default=[], description="List of bins associated with this coverpoint")
    
    model_config = ConfigDict(from_attributes=True)

    @computed_field(description="Total bins defined in this coverpoint")
    @property
    def total_bins(self) -> int:
        return len(self.bins)

    @computed_field(description="Number of bins with zero hits")
    @property
    def missed_bins(self) -> int:
        return sum(1 for b in self.bins if b.hits == 0)
