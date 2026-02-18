from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Bus

class BusRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, bus: Bus) -> Bus:
        self.db.add(bus)
        await self.db.commit()
        await self.db.refresh(bus)
        return bus

    async def list_all(self) -> list[Bus]:
        res = await self.db.execute(select(Bus).order_by(Bus.route_number, Bus.unit_code))
        return list(res.scalars().all())

    async def get_by_unit_code(self, unit_code: str) -> Bus | None:
        res = await self.db.execute(select(Bus).where(Bus.unit_code == unit_code))
        return res.scalars().first()

    async def list_by_route_number(self, route_number: str) -> list[Bus]:
        stmt = (
            select(Bus)
            .where(Bus.route_number == route_number)
            .order_by(Bus.unit_code)
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())