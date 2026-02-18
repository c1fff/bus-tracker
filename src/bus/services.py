from fastapi import HTTPException
from .models import Bus
from .schemas import BusCreate
from .repository import BusRepository

class BusService:
    def __init__(self, repo: BusRepository):
        self.repo = repo

    async def create_bus_service(self, data: BusCreate) -> Bus:
        exists = await self.repo.get_by_unit_code(data.unit_code)
        if exists:
            raise HTTPException(status_code=409, detail="Bus with this unit_code already exists")

        bus = Bus(
            route_number=data.route_number,
            route_variant=data.route_variant,
            unit_code=data.unit_code,
            is_active=True,
        )
        return await self.repo.create(bus)

    async def list_buses(self) -> list[Bus]:
        return await self.repo.list_all()
    
    async def get_buses_by_route_number(self, route_number: str) -> list[Bus]:
        return await self.repo.list_by_route_number(route_number)

