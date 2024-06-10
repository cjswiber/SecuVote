from typing import Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link
from pydantic import Field


class CandidateModel(Document):
    candidate_id: UUID = Field(default_factory=uuid4)
    name: str
    party: str
    bio: Optional[str] = None
    election: Optional[Link["ElectionModel"]] = None # Reference to the ID of the election

    def __repr__(self) -> str:
        return f"<Candidate {self.name}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CandidateModel):
            return self.candidate_id == other.candidate_id
        return False


    class Settings:
        name = "candidates"


from app.models.election_model import ElectionModel
