from app.schemas.candidate_schema import CandidateCreate, CandidateUpdate, CandidateOut
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel
from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie import Link
import json


class CandidateService:
    @staticmethod
    async def create_candidate(data: CandidateCreate) -> CandidateModel:
        candidate = CandidateModel(
            name=data.name,
            party=data.party,
            bio=data.bio,
        )
        try:
            await candidate.insert()
            return CandidateModel(
                candidate_id=candidate.candidate_id,
                name=candidate.name,
                party=candidate.party,
                bio=candidate.bio,
                election_id=[]
            )
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Candidate already registered"
            )
        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def get_candidate_by_id(candidate_id: UUID) -> Optional[CandidateOut]:
        candidate = await CandidateModel.find_one(CandidateModel.candidate_id == candidate_id)
        if not candidate:
            return None

        return CandidateOut(
            candidate_id=candidate.candidate_id,
            name=candidate.name,
            party=candidate.party,
            bio=candidate.bio,
            election_id=candidate.elections
        )


    @staticmethod
    async def update_candidate(candidate_id: UUID, data: CandidateUpdate) -> CandidateOut:
        candidate = await CandidateModel.find_one(CandidateModel.candidate_id == candidate_id)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )

        update_data = json.loads(data.json(exclude_unset=True))
        for key, value in update_data.items():
            setattr(candidate, key, value)
        await candidate.save()

        return CandidateOut(
            candidate_id=candidate.candidate_id,
            name=candidate.name,
            party=candidate.party,
            bio=candidate.bio,
            election_id=candidate.elections
        )


    @staticmethod
    async def delete_candidate(candidate_id: UUID) -> None:
        candidate = await CandidateModel.find_one(CandidateModel.candidate_id == candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        await candidate.delete()

