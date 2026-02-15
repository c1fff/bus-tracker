from fastapi import APIRouter, Request, Depends, HTTPException
from src.auth.dependencies import get_current_user
from .schemas import TrackPoint
from .services import require_driver
import redis.asyncio as redis

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.post("/point")
async def add_point(point: TrackPoint, bus_id: str, request: Request, current_user = Depends(get_current_user)):
    # Проверяем роль
    require_driver(current_user)

    r = request.app.state.redis
    user_id = current_user.get("sub")
    key = f"bus:last:{bus_id}"
    await r.set(key, point.model_dump_json(), ex=120)

    return {"message": "ok", "data": [point, bus_id]}

@router.get("/bus/{bus_id}/last", response_model=TrackPoint)
async def get_last(bus_id: str, request: Request):
    r = request.app.state.redis
    key = f"bus:last:{bus_id}"
    raw = await r.get(key)

    #later add raise 404, when we get bus tables(if bus_id is invalid)

    if not raw:
        return { "bus_id": "12", "online": False, "data": None }
    return {"bus_id": "12", "online": True, "data": TrackPoint}

