from pydantic import BaseModel, ConfigDict

class BinOut(BaseModel):
    name: str
    value: str | None
    hits: int
    hit: bool
    model_config = ConfigDict(from_attributes=True)
