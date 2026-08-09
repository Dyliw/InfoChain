from sqlalchemy import Column, String, Integer, Text, DateTime, UUID, JSONB, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid

class RelayChain(Base):
    __tablename__ = "relay_chains"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id = Column(PG_UUID(as_uuid=True), ForeignKey("scenarios.id", ondelete="SET NULL"))
    original_text = Column(Text, nullable=False)
    max_links = Column(Integer, default=5)
    status = Column(String(20), default='open') 
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

class RelayTransmission(Base):
    __tablename__ = "relay_transmissions"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chain_id = Column(PG_UUID(as_uuid=True), ForeignKey("relay_chains.id", ondelete="CASCADE"))
    position = Column(Integer, nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    text = Column(Text, nullable=False)
    elapsed_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint('chain_id', 'position'),)
