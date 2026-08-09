from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    last_active = Column(DateTime, nullable=True)
    total_scenarios_completed = Column(Integer, default=0)
    avg_confidence_calibration = Column(DECIMAL(3,2), nullable=True)
