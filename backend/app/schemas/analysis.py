from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List

class DecomposeRequest(BaseModel):
    claim: str
    source_claim: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class DecomposeResponse(BaseModel):
    affirmation: str
    evidence: List[str]
    interpretation: List[str]
    inference: List[str]
    missing_info: List[str]
    confidence_level: int 
    reasoning: str

class CompareRequest(BaseModel):
    claim: str
    sources: Dict[str, str] 

class CompareResponse(BaseModel):
    source: Dict[str, Any]
    article: Dict[str, Any]
    social: Dict[str, Any]
    ia: Dict[str, Any]
    differences: List[Dict[str, Any]]
    consensus: Optional[str]
    confidence_level: int

class SaveAnalysisRequest(BaseModel):
    user_id: UUID
    instance_id: UUID
    claim: str
    source_claim: Optional[str] = None
    decomposition: Optional[Dict[str, Any]] = None
    comparison_result: Optional[Dict[str, Any]] = None
    confidence_level: Optional[int] = None
    claims: Optional[List[Dict[str, Any]]] = None

class AnalysisResponse(BaseModel):
    id: UUID
    user_id: UUID
    instance_id: UUID
    claim: str
    source_claim: Optional[str]
    decomposition: Optional[Dict[str, Any]]
    comparison_result: Optional[Dict[str, Any]]
    confidence_level: Optional[int]
    created_at: datetime
    claims: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True
