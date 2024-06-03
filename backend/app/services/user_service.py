from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password, verify_password
from fastapi import HTTPException, status
from typing import Optional


class UserService:
    @staticmethod
    async def create_user(user: UserAuth) -> User:
        try:
            existing_user = await User.find_one(User.dni==user.dni)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already registered"
                )

            user_in = User(
                dni=user.dni,
                email=user.email,
                hashed_password=get_password(user.password),
            )
            await user_in.save()
            return user_in


        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc


        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def authenticate(dni: int, password: str) -> Optional[User]:
        user = await UserService.get_user_by_dni(dni=dni)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        
        return user
    

    @staticmethod
    async def get_user_by_dni(dni: int) -> Optional[User]:
        user = await User.find_one(User.dni == dni)
        return user
    
