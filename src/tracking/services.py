from fastapi import HTTPException, status
from .schemas import TrackPoint
from .repository import TrackingRepository

def require_driver(current_user: dict):
    if current_user.get("role") != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only drivers can send bus location")

class TrackingService:
    def __init__(self, repo: TrackingRepository):
        self.repo = repo

    async def add_point(self, *, point: TrackPoint, bus_id: str, current_user: dict) -> None:
        require_driver(current_user)
        await self.repo.set_last_point(bus_id, point, ttl=120)

    async def get_last(self, *, bus_id: str) -> TrackPoint | None:
        return await self.repo.get_last_point(bus_id)
