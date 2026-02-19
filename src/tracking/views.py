from fastapi import APIRouter, Request, Depends
from src.auth.dependencies import get_current_user

from .schemas import TrackPoint
from .repository import TrackingRepository
from .services import TrackingService

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.post("/point")
async def add_point(point: TrackPoint, unit_code: str, route_number: str, request: Request, current_user: dict = Depends(get_current_user)):
    repo = TrackingRepository(request.app.state.redis)
    service = TrackingService(repo)
    await service.add_point(point=point, unit_code=unit_code, route_number=route_number, current_user=current_user)
    return {"message": "ok"}

@router.get("/bus/{bus_id}/last")
async def get_last(unit_code: str, request: Request):
    repo = TrackingRepository(request.app.state.redis)
    service = TrackingService(repo)
    point = await service.get_last(unit_code=unit_code)
    if not point:
        return {
            "unit_code": unit_code,
            "online": False,
            "data": None    
        }
    return {
        "unit_code": unit_code,
        "online": True,
        "data": point
    }

@router.get("/route/{route_number}")
async def get_route(route_number: str, request: Request):
    repo = TrackingRepository(request.app.state.redis)
    service = TrackingService(repo)

    buses = await service.get_route(route_number=route_number)

    return {
        "route_number": route_number,
        "active_units": buses
    }
