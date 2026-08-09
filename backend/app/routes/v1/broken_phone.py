from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.relay import (
    StartRelayRequest, StartRelayResponse,
    TransmitRequest, TransmitResponse,
    RelayChainResponse
)
from app.services.broken_phone import BrokenPhoneService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/broken-phone", tags=["broken-phone"])
broken_phone = BrokenPhoneService()

@router.post("/start", response_model=StartRelayResponse)
async def start_chain(
    request: StartRelayRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Iniciar cadena de teléfono roto"""
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot start chain for another user"
        )
    
    try:
        result = await broken_phone.start_chain(
            db,
            str(request.user_id),
            request.original_text,
            request.max_links,
            str(request.scenario_id) if request.scenario_id else None
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transmit", response_model=TransmitResponse)
async def transmit(
    request: TransmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Transmitir mensaje en la cadena"""
    if str(current_user.id) != str(request.user_id):
        raise HTTPException(
            status_code=403,
            detail="Cannot transmit for another user"
        )
    
    try:
        result = await broken_phone.transmit(
            db,
            str(request.chain_id),
            str(request.user_id),
            request.text,
            request.elapsed_time_ms
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chain/{chain_id}", response_model=RelayChainResponse)
async def get_chain(
    chain_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ver cadena completa de transmisiones"""
    try:
        result = await broken_phone.get_chain(db, chain_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    So0yUnaratitaMuycurioseta1
