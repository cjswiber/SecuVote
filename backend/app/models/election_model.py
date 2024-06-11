from uuid import UUID, uuid4
from beanie import Document, Link, Indexed
from pydantic import Field
import datetime as dt
from typing import Optional, List


class ElectionModel(Document):
    election_id: UUID = Field(default_factory=uuid4)
    name: Indexed(str, unique=True) #type: ignore
    description: Optional[str] = None
    start_date: Optional[dt.datetime] = None
    end_date: Optional[dt.datetime] = None
    candidates: Optional[Link["CandidateModel"]] = None


    def __repr__(self) -> str:
        return f"<Election {self.name}>"

    def __hash__(self) -> int:
        return hash(self.election_id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ElectionModel):
            return self.election_id == other.election_id
        return False


    @classmethod
    async def by_name(cls, name: str) -> "ElectionModel":
        return await cls.find_one(cls.name == name)
    
    @classmethod
    async def by_id(cls, id: UUID) -> "ElectionModel":
        return await cls.find_one(cls.election_id == id)


    class Settings:
        name = "elections"


from app.models.candidate_model import CandidateModel
