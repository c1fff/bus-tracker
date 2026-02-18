from .schemas import TrackPoint

class TrackingRepository:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def set_last_point(self, bus_id: str, point: TrackPoint, ttl: int = 120) -> None:
        key = f"bus:last:{bus_id}"
        await self.redis.set(key, point.model_dump_json(), ex=ttl)

    async def get_last_point(self, bus_id: str) -> TrackPoint | None:
        key = f"bus:last:{bus_id}"
        raw = await self.redis.get(key)
        if not raw:
            return None
        return TrackPoint.model_validate_json(raw)
