from pydantic import BaseModel
import datetime as dt


class VoteCreate(BaseModel):
    pass


class VoteUpdate(BaseModel):
    pass


class VoteOut(BaseModel):
    user_id: str
    timestamp: dt.datetime

