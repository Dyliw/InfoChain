from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.scenario import (
    ScenarioResponse, ScenarioStart, ScenarioStep, 
    ScenarioComplete, InstanceResponse
)
from app.services.scenario_service import ScenarioService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

@router.get("", response_model=List[ScenarioResponse])
def get_scenarios(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return ScenarioService.get_all_scenarios(db, skip, limit)

@router.get("/{slug}", response_model=ScenarioResponse)
def get_scenario(slug: str, db: Session = Depends(get_db)):
    return ScenarioService.get_scenario_by_slug(db, slug)

@router.post("/{slug}/start", response_model=InstanceResponse)
def start_scenario(
    slug: str,
    start_data: ScenarioStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure user_id matches current user
    if str(current_user.id) != str(start_data.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot start scenario for another user"
        )
    return ScenarioService.start_scenario(db, slug, start_data)

@router.post("/{slug}/step", response_model=InstanceResponse)
def process_step(
    slug: str,
    step_data: ScenarioStep,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure user_id matches current user
    if str(current_user.id) != str(step_data.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot process step for another user"
        )
    return ScenarioService.process_step(db, slug, step_data)

@router.post("/{slug}/complete", response_model=InstanceResponse)
def complete_scenario(
    slug: str,
    complete_data: ScenarioComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure user_id matches current user
    if str(current_user.id) != str(complete_data.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot complete scenario for another user"
        )
    return ScenarioService.complete_scenario(db, slug, complete_data)

@router.get("/instance/{instance_id}", response_model=InstanceResponse)
def get_instance(
    instance_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    instance = ScenarioService.get_instance(db, instance_id)
    # Security check: ensure user owns this instance
    if str(current_user.id) != str(instance.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot access this instance"
        )
    return instance
