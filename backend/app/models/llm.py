from sqlalchemy import Column, String, Integer, Text, DateTime, UUID, JSONB, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid

class LLMInteraction(Base):
    __tablename__ = "llm_interactions"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    scenario_id = Column(PG_UUID(as_uuid=True), ForeignKey("scenarios.id", ondelete="SET NULL"))
    interaction_type = Column(String(50), nullable=False)
    model = Column(String(100), nullable=True)
    input_hash = Column(String(128), nullable=True)
    output_metadata = Column(PG_JSONB, nullable=True)
    evaluation = Column(PG_JSONB, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
