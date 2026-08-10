from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class SourceCreate(BaseModel):
    title: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    source_type: Optional[str] = None
    language: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class SourceFragmentCreate(BaseModel):
    source_id: UUID
    content: str
    location: Optional[str] = None

class SourceResponse(BaseModel):
    id: UUID
    title: str
    author: Optional[str]
    publisher: Optional[str]
    url: Optional[str]
    published_at: Optional[datetime]
    source_type: Optional[str]
    language: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    fragments: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True

class TransformationCreate(BaseModel):
    source_id: Optional[UUID] = None
    previous_text: Optional[str] = None
    resulting_text: Optional[str] = None
    transformation_type: str
    severity: Optional[float] = None
    detected_by: Optional[str] = None
    explanation: Optional[str] = None

class TransformationResponse(BaseModel):
    id: UUID
    source_id: Optional[UUID]
    previous_text: Optional[str]
    resulting_text: Optional[str]
    transformation_type: str
    severity: Optional[float]
    detected_by: Optional[str]
    explanation: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
