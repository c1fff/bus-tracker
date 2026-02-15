from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

from src.database.db import Base



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    phone = Column(String(50))
    full_name = Column(String(255))
    role = Column(String(50))
    is_active = Column(Boolean, default=True)

    refresh_token_hash = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), 
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
                        DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))