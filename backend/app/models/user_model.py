from typing import Optional
import datetime
from enum import Enum
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, EmailStr


class UserRole(Enum):
    ADMIN = "admin"
    TABLE_AUTHORITY = "table authority"
    CANDIDATE = "candidate"
    CITIZEN = "citizen"


class UserModel(Document):
    user_id: UUID = Field(default_factory=uuid4)
    dni: Indexed(int, unique=True) # type: ignore
    email: Indexed(EmailStr, unique=True) # type: ignore
    hashed_password: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    role: Optional[UserRole] = None
    disabled : Optional[bool] = None


    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UserModel):
            return self.email == other.email
        return False
    
    @classmethod
    async def by_email(self, email: str) -> "UserModel":
        return await self.find_one(self.email == email)
    
    @classmethod
    async def by_dni(self, dni: int) -> "UserModel":
        return await self.find_one(self.dni == dni)
    

    class Settings:
        name = "users"


'''
    @property
    def create(self) -> datetime:
        return self.id.generation_time
'''

