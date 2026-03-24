from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token,decode_token
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.token import RefreshTokenRequest
from app.schemas.token import RefreshTokenRequest


class AuthService:

    @staticmethod
    def register_user(data: RegisterRequest, db: Session):
        existing_user = UserRepository.get_user_by_email(db, data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(data.password)

        user = UserRepository.create_user(
            db,
            data.first_name,
            data.last_name,
            data.email,
            password=hashed_password
        )

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }

    @staticmethod
    def login_user(data: LoginRequest, db: Session):
        user = UserRepository.get_user_by_email(db, data.email)

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def refresh_token(data: RefreshTokenRequest, db: Session):
        payload = decode_token(data.refresh_token)

        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")

        return {
            "access_token": create_access_token({"sub": user_id}),
            "token_type": "bearer"
        }