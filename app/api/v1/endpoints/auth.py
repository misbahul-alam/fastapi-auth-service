from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.schemas.token import RefreshTokenRequest
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, RegisterRequest
from app.core.dependencies import get_db
from fastapi import Depends

router = APIRouter()

@router.post("/register")
def register(data: RegisterRequest, db : Session = Depends(get_db)):
    return AuthService.register_user(data, db)

@router.post("/login")
def login(data: LoginRequest, db : Session = Depends(get_db)):
    return AuthService.login_user(data, db)

@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest, db : Session = Depends(get_db)):
    return AuthService.refresh_token(data, db)