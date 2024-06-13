from typing import Optional
from beanie import Document, Link
from pydantic import Field
from datetime import datetime, timezone
from app.models.user_model import UserModel
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel


class VoteModel(Document):
    # voter: Optional[Link[UserModel]] # Reference to the ID of the user who voted
    voter: Optional[dict]
    candidate: Optional[dict] # Reference to the ID of the candidate being voted for
    election: Optional[dict] # Reference to the ID of the election
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    class Settings:
        name = "votes"