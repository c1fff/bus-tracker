from fastapi import APIRouter
from .schemas import TrackPoint

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.post("/point")
def add_point(point: TrackPoint):
    return {"message": "ok", "data": point}

#@router.get("/last_point")
#def get_point(point: )