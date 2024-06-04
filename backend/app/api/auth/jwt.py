from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, Optional
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import TokenSchema
from app.schemas.user_schema import UserOut
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user


auth_router = APIRouter()


class OAuth2PasswordRequestFormDNI(OAuth2PasswordRequestForm):
    def __init__(self, dni: int = None, password: str = None):
        super().__init__(username=str(dni), password=password)
        self.dni = dni


@auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestFormDNI = Depends()) -> Any:
    user = await UserService.authenticate(dni=form_data.dni, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect DNI or password"
        )
    
    # create access and refresh tokens
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }


@auth_router.post('/test-token', summary="Test if the access token is valid", response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user

