from typing import Optional, List
from beanie import Document, Indexed, Link


class CandidateModel(Document):
    # candidate_id: UUID = Field(default_factory=uuid4)
    name: str
    party: str
    bio: Optional[str] = None
    elections: Optional[Link["ElectionModel"]] = None # Reference to the ID of the election

    def __repr__(self) -> str:
        return f"<Candidate {self.name}>"


    class Settings:
        name = "candidates"


from app.models.election_model import ElectionModel
