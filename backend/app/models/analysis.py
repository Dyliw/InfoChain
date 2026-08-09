from sqlalchemy import Column, String, Integer, Text, DateTime, UUID, JSONB, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    instance_id = Column(PG_UUID(as_uuid=True), ForeignKey("scenario_instances.id", ondelete="CASCADE"))
    claim = Column(Text, nullable=False)
    source_claim = Column(Text, nullable=True)
    decomposition = Column(PG_JSONB, nullable=True) 
    comparison_result = Column(PG_JSONB, nullable=True) 
    confidence_level = Column(Integer, nullable=True) 
    created_at = Column(DateTime, server_default=func.now())

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(PG_UUID(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
    claim_type = Column(String(30), nullable=True)
    confidence = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
