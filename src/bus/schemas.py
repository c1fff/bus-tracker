from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class BusCreate(BaseModel):
    route_number: str = Field(min_length=1, max_length=20)   # "1"
    route_variant: Optional[str] = Field(default=None, max_length=20)  # "A" / None
    unit_code: str = Field(min_length=1, max_length=50)      # "1-A-03"

class BusRead(BaseModel):
    id: UUID
    route_number: str
    route_variant: Optional[str] = None
    unit_code: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
