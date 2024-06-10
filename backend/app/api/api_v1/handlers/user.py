from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user_schema import UserAuth, UserOut, UserUpdate
from app.services.user_service import UserService
from app.models.user_model import UserModel
from pymongo import MongoClient, errors
from app.api.deps.user_deps import get_current_user
import pymongo


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


@user_router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: UserModel = Depends(get_current_user)):
    return user


@user_router.post('/update', summary='Update User', response_model=UserOut)
async def update_user(data: UserUpdate, user: UserModel = Depends(get_current_user)):
    try:
        return await UserService.update_user(user.user_id, data)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
    
