from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user_id = payload.get("sub")
    user = UserRepository.get_user_by_email(db, user_id) 
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user