from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.services.user_service import UserService

router = APIRouter()

@router.get("/me")
def get_user_profile(current_user = Depends(get_current_user)):
    return UserService.get_user_profile(current_user)