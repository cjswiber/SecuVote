from sqlalchemy import Column, Integer, String


class Candidate():
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    votes = Column(Integer, default=0)

