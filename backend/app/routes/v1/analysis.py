from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict, List
from app.database import get_db
from app.schemas.analysis import (
    DecomposeRequest, DecomposeResponse,
    CompareRequest, CompareResponse,
    SaveAnalysisRequest, AnalysisResponse
)
from app.services.analysis_service import AnalysisService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analysis", tags=["analysis"])
analysis_service = AnalysisService()

@router.post("/decompose", response_model=DecomposeResponse)
async def decompose_claim(
    request: DecomposeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Descomponer una afirmación en sus partes componentes"""
    try:
        result = await analysis_service.decompose_claim(
            db,
            str(current_user.id),
            request.claim,
            request.source_claim,
            request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare", response_model=CompareResponse)
async def compare_sources(
    request: CompareRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Comparar diferentes fuentes sobre una afirmación"""
    try:
        result = await analysis_service.compare_sources(
            db,
            str(current_user.id),
            request.claim,
            request.sources
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save", response_model=Dict[str, Any])
async def save_analysis(
    request: SaveAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Guardar un análisis completo"""
    # Ensure user_id matches current user
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot save analysis for another user"
        )
    
    try:
        result = await analysis_service.save_analysis(
            db,
            str(request.user_id),
            str(request.instance_id),
            request.claim,
            request.source_claim,
            request.decomposition,
            request.comparison_result,
            request.confidence_level,
            request.claims
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener un análisis por ID"""
    try:
        result = await analysis_service.get_analysis(db, analysis_id)
      # Security check
        if result["user_id"] != str(current_user.id):
            raise HTTPException(
                status_code=403,
                detail="Cannot access this analysis"
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
