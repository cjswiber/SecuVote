from typing import Optional, List
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import Field


class CandidateModel(Document):
    candidate_id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    name: str
    party: str
    bio: Optional[str] = None
    elections: Optional[List[PydanticObjectId]] = None

    def __repr__(self) -> str:
        return f"<Candidate {self.name}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CandidateModel):
            return self.candidate_id == other.candidate_id
        return False


    class Settings:
        name = "candidates"


from app.models.election_model import ElectionModel
