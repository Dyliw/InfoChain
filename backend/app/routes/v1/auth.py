from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, TokenRefresh, UserResponse
from app.services.auth_service import AuthService
from app.utils.security import get_current_user, create_access_token, verify_refresh_token, create_refresh_token


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = AuthService.register(db, user_data)
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login(db, user_data.email, user_data.password)

@router.post("/refresh", response_model=Token)
def refresh(token_data: TokenRefresh):
    # Verify refresh token and create new tokens
    user_id = verify_refresh_token(token_data.refresh_token)
    access_token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return AuthService.get_user(db, str(current_user.id))
