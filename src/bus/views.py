from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from .schemas import BusCreate, BusRead
from .repository import BusRepository
from .services import BusService

router = APIRouter(prefix="/buses", tags=["Buses"])

@router.post("", response_model=BusRead)
async def create_bus(payload: BusCreate, db: AsyncSession = Depends(get_db)):
    service = BusService(BusRepository(db))
    bus = await service.create_bus_service(payload)
    return bus

@router.get("", response_model=list[BusRead])
async def list_buses(db: AsyncSession = Depends(get_db)):
    service = BusService(BusRepository(db))
    buses = await service.list_buses()
    return buses

@router.get("/route/{route_number}", response_model=list[BusRead])
async def get_buses_by_route_number(route_number: str, db: AsyncSession = Depends(get_db)):
    service = BusService(BusRepository(db))
    return await service.get_buses_by_route_number(route_number)
