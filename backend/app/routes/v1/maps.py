from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.reasoning import (
    GenerateMapRequest, GenerateMapResponse,
    SaveMapRequest, ReasoningMapResponse
)
from app.services.reasoning_mapper import ReasoningMapper
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/maps", tags=["maps"])
mapper = ReasoningMapper()

@router.post("/generate", response_model=GenerateMapResponse)
async def generate_map(
    request: GenerateMapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generar mapa de razonamiento desde un análisis"""
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot generate map for another user"
        )
    
    try:
        result = await mapper.generate_map(
            db,
            str(request.user_id),
            str(request.analysis_id),
            request.include_sources,
            request.max_depth
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{analysis_id}", response_model=ReasoningMapResponse)
async def get_map(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener mapa de razonamiento para un análisis"""
    try:
        result = await mapper.get_map(db, analysis_id)
        if result["user_id"] != str(current_user.id):
            raise HTTPException(
                status_code=403,
                detail="Cannot access this map"
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save", response_model=Dict[str, Any])
async def save_map(
    request: SaveMapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Guardar mapa con ajustes del usuario"""
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot save map for another user"
        )
    
    try:
        result = await mapper.save_map_with_adjustments(
            db,
            str(request.user_id),
            str(request.analysis_id),
            request.nodes,
            request.edges,
            request.confidence_breakdown,
            request.final_conclusion,
            request.user_adjustments or {}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
