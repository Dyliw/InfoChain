from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List

class ScenarioResponse(BaseModel):
    id: UUID
    slug: str
    title: str
    description: Optional[str]
    difficulty: int
    type: Optional[str]
    config: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

class ScenarioStart(BaseModel):
    user_id: UUID

class ScenarioStep(BaseModel):
    user_id: UUID
    step_data: Dict[str, Any]

class ScenarioComplete(BaseModel):
    user_id: UUID
    score: float
    mistakes_identified: Optional[int] = 0
    final_data: Optional[Dict[str, Any]] = None

class InstanceResponse(BaseModel):
    id: UUID
    user_id: UUID
    scenario_id: UUID
    status: str
    current_step: int
    user_actions: Optional[Dict[str, Any]]
    chain_data: Optional[Dict[str, Any]]
    started_at: datetime
    completed_at: Optional[datetime]
    score: Optional[float]
    mistakes_identified: Optional[int]

    class Config:
        from_attributes = True
