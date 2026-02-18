from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

from src.database.db import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # what a user sees(just bus num)
    route_number = Column(String(20), nullable=False)         # "1", "4", "10"
    route_variant = Column(String(20), nullable=True)         #"A" or "B"
    # uniq code of bus
    unit_code = Column(String(50), unique=True, nullable=False)  # example: 1-A-03

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    last_seen_at = Column(DateTime(timezone=True), nullable=True)
