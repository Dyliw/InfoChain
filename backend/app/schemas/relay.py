from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class StartRelayRequest(BaseModel):
    scenario_id: Optional[UUID] = None
    original_text: str
    max_links: int = 5
    user_id: UUID

class StartRelayResponse(BaseModel):
    chain_id: UUID
    original_text: str
    max_links: int
    status: str
    current_position: int
    next_user_id: Optional[UUID] = None

class TransmitRequest(BaseModel):
    chain_id: UUID
    user_id: UUID
    text: str
    elapsed_time_ms: Optional[int] = None

class TransmitResponse(BaseModel):
    transmission_id: UUID
    position: int
    is_complete: bool
    chain_status: str
    next_position: Optional[int] = None

class RelayChainResponse(BaseModel):
    id: UUID
    scenario_id: Optional[UUID]
    original_text: str
    max_links: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    transmissions: List[Dict[str, Any]]
    transformations: Optional[List[Dict[str, Any]]]
    distortion_analysis: Optional[Dict[str, Any]]

class TransmissionComparison(BaseModel):
    original: str
    final: str
    transformations: List[Dict[str, Any]]
    distortion_score: float
    key_changes: List[Dict[str, Any]]
