from typing import Optional
from beanie import Document, Link
from pydantic import Field
import datetime as dt
from app.models.user_model import UserModel
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel


class VoteModel(Document):
    voter: Optional[Link[UserModel]] # Reference to the ID of the user who voted
    candidate: Optional[Link[CandidateModel]] # Reference to the ID of the candidate being voted for
    election: Optional[Link[ElectionModel]] # Reference to the ID of the election
    timestamp: dt.datetime = Field(default_factory=dt.datetime.now(dt.timezone.utc))


    class Settings:
        name = "votes"

