from .schemas import TrackPoint

class TrackingRepository:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def set_last_point(self, unit_code: str, route_number: str, point: TrackPoint, ttl: int = 120) -> None:
        key = f"bus:last:{unit_code}"
        await self.redis.set(key, point.model_dump_json(), ex=ttl)
        await self.redis.sadd(f"route:{route_number}:units", unit_code)

    async def get_last_point(self, unit_code: str) -> TrackPoint | None:
        key = f"bus:last:{unit_code}"
        raw = await self.redis.get(key)
        if not raw:
            return None
        return TrackPoint.model_validate_json(raw)

    async def get_route_points(self, route_number: str) -> list[dict]:
        route_key = f"route:{route_number}:units"
        unit_codes = await self.redis.smembers(route_key)
        results = []
        for unit_code in unit_codes:
            bus_key = f"bus:last:{unit_code}"
            raw = await self.redis.get(bus_key)
            if not raw:
                # If expired → remove from route index
                await self.redis.srem(route_key, unit_code)
                continue
            point = TrackPoint.model_validate_json(raw)
            results.append({
                "unit_code": unit_code,
                "data": point
            })
        return results