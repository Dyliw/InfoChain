from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List

class NodeCreate(BaseModel):
    id: str
    type: str
    text: str
    parentId: Optional[str] = None

class EdgeCreate(BaseModel):
    from_node: str
    to_node: str
    label: Optional[str] = None

class GenerateMapRequest(BaseModel):
    analysis_id: UUID
    user_id: UUID
    include_sources: bool = True
    max_depth: Optional[int] = None

class GenerateMapResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    confidence_breakdown: Dict[str, float]
    final_conclusion: str
    analysis_summary: str

class SaveMapRequest(BaseModel):
    analysis_id: UUID
    user_id: UUID
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    confidence_breakdown: Dict[str, float]
    final_conclusion: str
    user_adjustments: Optional[Dict[str, Any]] = None

class ReasoningMapResponse(BaseModel):
    id: UUID
    user_id: UUID
    analysis_id: UUID
    nodes: List[Dict[str, Any]]
    edges: Optional[List[Dict[str, Any]]]
    confidence_breakdown: Optional[Dict[str, float]]
    final_conclusion: Optional[str]
    user_adjustments: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
