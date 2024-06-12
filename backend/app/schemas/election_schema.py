from pydantic import BaseModel, Field
from typing import Optional
import datetime as dt


class ElectionCreate(BaseModel):
    name: str = Field(..., description="Name of the election")
    description: Optional[str] = Field(..., description="Description of the election")
    start_date: dt.datetime = Field(..., description="Start date of the election")
    end_date: dt.datetime = Field(..., description="End date of the election")    


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


class ElectionOutVote(BaseModel):
    id: str
    name: str
    description: str

