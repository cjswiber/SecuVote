from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Email of the user")
    dni: int = Field(..., ge=1000, le=999999999999, description="DNI of the user")
    password: str = Field(..., min_length=5, max_length=50, description="Password of the user")


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    
class UserOut(BaseModel):
    user_id: UUID
    dni: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: Optional[bool] = False


class UserOutVote(BaseModel):
    id: str
    dni: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: Optional[bool] = False

