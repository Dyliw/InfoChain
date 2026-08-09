from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.llm import (
    ChatRequest, ChatResponse,
    AuditRequest, AuditResponse,
    FeedbackRequest, LLMInteractionResponse
)
from app.services.llm_service import LLMService
from app.utils.security import get_current_user
from app.models.user import User
from app.models.llm import LLMInteraction

router = APIRouter(prefix="/llm", tags=["llm"])
llm_service = LLMService()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat con IA con sistema de roles y modos"""
    # Ensure user_id matches current user
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot chat on behalf of another user"
        )
    
    try:
        result = await llm_service.chat(
            db,
            str(request.user_id),
            request.message,
            request.mode,
            request.context,
            request.conversation_history
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audit", response_model=AuditResponse)
async def audit_response(
    request: AuditRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Auditar respuesta de IA"""
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot audit for another user"
        )
    
    try:
        result = await llm_service.audit_response(
            db,
            str(request.user_id),
            request.ai_response,
            request.original_query,
            request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def provide_feedback(
    request: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Usuario corrige o da feedback a la IA"""
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot provide feedback for another user"
        )
    
    try:
        result = await llm_service.process_feedback(
            db,
            str(request.user_id),
            str(request.interaction_id),
            request.correct_response,
            request.feedback_type,
            request.explanation
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interactions", response_model=List[LLMInteractionResponse])
async def get_interactions(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener historial de interacciones con IA del usuario"""
    interactions = db.query(LLMInteraction).filter(
        LLMInteraction.user_id == current_user.id
    ).order_by(LLMInteraction.created_at.desc()).offset(skip).limit(limit).all()
    
    return interactions

@router.get("/interactions/{interaction_id}", response_model=LLMInteractionResponse)
async def get_interaction(
    interaction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener una interacción específica"""
    interaction = db.query(LLMInteraction).filter(
        LLMInteraction.id == interaction_id
    ).first()
    
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    if interaction.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Cannot access this interaction"
        )
    
    return interaction
