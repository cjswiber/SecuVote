from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user_schema import UserAuth, UserOut#, UserUpdate
from app.services.user_service import UserService
from app.models.user_model import User
from pymongo import MongoClient, errors
# from app.api.deps.user_deps import get_current_user


user_router = APIRouter()


@user_router.post("/create", summary="Create a new user", response_model=UserOut)
async def create_user(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )

