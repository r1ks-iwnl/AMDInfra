from pydantic import BaseModel, ConfigDict, Field

class BinOut(BaseModel):
    name: str = Field(..., examples=["vec[10]"], description="Name of the coverage bin")
    value: str | None = Field(None, examples=["1'b1", "0:15"], description="Specific digital value")
    hits: int = Field(..., examples=[8], description="Number of times the bin was hit during simulation")
    hit: bool = Field(..., examples=[True], description="Flag indicating if the bin was hit at least once")
    
    model_config = ConfigDict(from_attributes=True)
