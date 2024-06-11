from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
import datetime as dt
from app.models.candidate_model import CandidateModel
from beanie import Link


class ElectionCreate(BaseModel):
    name: str = Field(..., description="Name of the election")
    description: Optional[str] = Field(..., description="Description of the election")
    start_date: dt.datetime = Field(..., description="Start date of the election")
    end_date: dt.datetime = Field(..., description="End date of the election")    


class ElectionUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the election")
    description: Optional[str] = Field(None, description="Description of the election")
    start_date: Optional[dt.datetime] = Field(None, description="Start date of the election")
    end_date: Optional[dt.datetime] = Field(None, description="End date of the election")



class ElectionOut(BaseModel):
    election_id: UUID
    name: str
    description: Optional[str]
    start_date: dt.datetime
    end_date: dt.datetime


