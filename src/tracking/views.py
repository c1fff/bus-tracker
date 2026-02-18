from fastapi import APIRouter, Request, Depends
from src.auth.dependencies import get_current_user

from .schemas import TrackPoint
from .repository import TrackingRepository
from .services import TrackingService

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.post("/point")
async def add_point(point: TrackPoint, bus_id: str, request: Request, current_user: dict = Depends(get_current_user)):
    repo = TrackingRepository(request.app.state.redis)
    service = TrackingService(repo)

    await service.add_point(point=point, bus_id=bus_id, current_user=current_user)

    return {"message": "ok"}

@router.get("/bus/{bus_id}/last")
async def get_last(bus_id: str, request: Request):
    repo = TrackingRepository(request.app.state.redis)
    service = TrackingService(repo)

    point = await service.get_last(bus_id=bus_id)

    if not point:
        return {"bus_id": bus_id, "online": False, "data": None}

    return {"bus_id": bus_id, "online": True, "data": point}

