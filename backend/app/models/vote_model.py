from typing import Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field
import datetime as dt

class Vote(Document):
    vote_id: UUID = Field(default_factory=uuid4)
    voter_id: Indexed(UUID) # Reference to the ID of the user who voted
    candidate_id: Indexed(UUID) # Reference to the ID of the candidate being voted for
    election_id: Indexed(UUID) # Reference to the ID of the election
    timestamp: dt.datetime = Field(default_factory=dt.datetime.now(dt.timezone.utc))
    
    class Settings:
        name = "votes"

    def __repr__(self) -> str:
        return f"<Vote {self.vote_id}>"

    def __str__(self) -> str:
        return str(self.vote_id)

    def __hash__(self) -> int:
        return hash(self.vote_id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vote):
            return self.vote_id == other.vote_id
        return False

