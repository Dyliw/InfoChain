from sqlalchemy import Column, String, Integer, Text, DateTime, UUID, JSONB, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Source(Base):
    __tablename__ = "sources"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    author = Column(Text, nullable=True)
    publisher = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    source_type = Column(String(50), nullable=True)
    language = Column(String(20), nullable=True)
    metadata = Column(PG_JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class SourceFragment(Base):
    __tablename__ = "source_fragments"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(PG_UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class InformationTransformation(Base):
    __tablename__ = "information_transformations"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(PG_UUID(as_uuid=True), ForeignKey("sources.id", ondelete="SET NULL"))
    previous_text = Column(Text, nullable=True)
    resulting_text = Column(Text, nullable=True)
    transformation_type = Column(String(50), nullable=False)
    severity = Column(DECIMAL(4,3), nullable=True)
    detected_by = Column(String(30), nullable=True) 
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
