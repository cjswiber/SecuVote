from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password
from fastapi import HTTPException, status


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

