from pydantic import BaseModel, Field
from datetime import datetime

#location schema

class TrackPoint(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)                    #широта
    longitude: float = Field(..., ge=-180, le=180)                 #долгота   
    timestamp: datetime = Field(default_factory=datetime.utcnow)
