from uuid import UUID
from beanie import Document, Indexed
from pydantic import Field, EmailStr

class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    # dni: str = Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    first_name: str = Indexed(str)
    last_name: str = Indexed(str)
    role: str
    disabled : bool


    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
    
    class Collection:
        name = "users"