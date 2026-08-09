from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List

class ChatRequest(BaseModel):
    user_id: UUID
    scenario_id: Optional[UUID] = None
    message: str
    context: Optional[Dict[str, Any]] = None
    mode: str = "LABORATORY"
    conversation_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: int
    response_time_ms: int
    metadata: Optional[Dict[str, Any]] = None

class AuditRequest(BaseModel):
    user_id: UUID
    ai_response: str
    original_query: str
    context: Optional[Dict[str, Any]] = None

class AuditResponse(BaseModel):
    is_accurate: bool
    confidence_score: int 
    issues: List[Dict[str, Any]]
    corrections: Optional[List[Dict[str, Any]]]
    reasoning: str

class FeedbackRequest(BaseModel):
    user_id: UUID
    interaction_id: UUID
    correct_response: str
    feedback_type: str
    explanation: Optional[str] = None

class LLMInteractionResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    scenario_id: Optional[UUID]
    interaction_type: str
    model: Optional[str]
    output_metadata: Optional[Dict[str, Any]]
    evaluation: Optional[Dict[str, Any]]
    tokens_used: Optional[int]
    response_time_ms: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
