from typing import Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link
from pydantic import Field
import datetime as dt
from app.models.user_model import UserModel
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel


class Vote(Document):
    # vote_id: UUID = Field(default_factory=uuid4)
    voter: Link[UserModel] # Reference to the ID of the user who voted
    candidate: Link[CandidateModel] # Reference to the ID of the candidate being voted for
    election: Link[ElectionModel] # Reference to the ID of the election
    timestamp: dt.datetime = Field(default_factory=dt.datetime.now(dt.timezone.utc))


    def __str__(self) -> str:
        return str(self.vote_id)
    

    class Settings:
        name = "votes"

