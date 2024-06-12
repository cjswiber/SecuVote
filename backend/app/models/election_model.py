from uuid import UUID, uuid4
from beanie import Document, Link, Indexed
from pydantic import Field
import datetime as dt
from typing import Optional, List


class ElectionModel(Document):
    # election_id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    start_date: Optional[dt.datetime] = None
    end_date: Optional[dt.datetime] = None
    candidates: Optional[Link["CandidateModel"]] = None


    def __repr__(self) -> str:
        return f"<Election {self.name}>"


    class Settings:
        name = "elections"


from app.models.candidate_model import CandidateModel
