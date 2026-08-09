from sqlalchemy import Column, String, Integer, Text, DateTime, UUID, JSONB, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(100), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(Integer, default=1)
    type = Column(String(50), nullable=True)
    config = Column(PG_JSONB, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class ScenarioInstance(Base):
    __tablename__ = "scenario_instances"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    scenario_id = Column(PG_UUID(as_uuid=True), ForeignKey("scenarios.id", ondelete="CASCADE"))
    status = Column(String(20), default="in_progress")
    current_step = Column(Integer, default=0)
    user_actions = Column(PG_JSONB, nullable=True)
    chain_data = Column(PG_JSONB, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    score = Column(DECIMAL(5,2), nullable=True)
    mistakes_identified = Column(Integer, nullable=True)
