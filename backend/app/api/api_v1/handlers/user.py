from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserAuth
from app.services.user_service import UserService
from pymongo import MongoClient, errors

user_router = APIRouter()


@user_router.post("/create", summary="Create a new user")
async def create_user(data: UserAuth):
    try:
        await UserService.create_user(data)
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")



