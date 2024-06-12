from pydantic import BaseModel, Field
from typing import Optional
import datetime as dt


class ElectionCreate(BaseModel):
    pass


class ElectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[dt.datetime] = None
    end_date: Optional[dt.datetime] = None


class ElectionOut(BaseModel):
    id: str
    name: str
    description: str
    start_date: dt.datetime
    end_date: dt.datetime




    # vote_id: UUID = Field(default_factory=uuid4)
    voter: Link[UserModel] # Reference to the ID of the user who voted
    candidate: Link[CandidateModel] # Reference to the ID of the candidate being voted for
    election: Link[ElectionModel] # Reference to the ID of the election
    timestamp: dt.datetime = Field(default_factory=dt.datetime.now(dt.timezone.utc))