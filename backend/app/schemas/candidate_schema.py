from pydantic import BaseModel, UUID4, EmailStr, Field
from typing import Optional
from uuid import UUID


class CandidateCreate(BaseModel):
    name: str = Field(..., title='Full name', max_length=60, min_length=1, description="Full name of the candidate")
    party: Optional[str] = Field(..., title='Party', max_length=60, min_length=1, description="Party of the candidate")
    bio: Optional[str] = Field(..., title='Biography', max_length=800, min_length=1, description="Biography of the candidate")
    election_id: Optional[UUID]


class CandidateOut(BaseModel):
    candidate_id: UUID
    name: str
    party: str
    bio: str
    election_id: Optional[UUID]


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    party: Optional[str] = None
    bio: Optional[str] = None

