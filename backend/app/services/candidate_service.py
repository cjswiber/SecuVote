from app.schemas.candidate_schema import CandidateCreate, CandidateUpdate
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel
from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class CandidateService:
    @staticmethod
    async def create_candidate(candidate: CandidateCreate) -> CandidateModel:
        try:
            '''
            election = await ElectionModel.get(candidate.election_id)
            election = await ElectionModel.get(ObjectId(candidate.election_id))
            election = await ElectionModel.find_one(ElectionModel.id == candidate.election_id) 
            if not election:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Election not found"
                )
            '''
            
            existing_candidate = await CandidateModel.find_one(CandidateModel.name == candidate.name)
            if existing_candidate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Candidate already registered"
                )
            
            candidate_in = CandidateModel(
                name=candidate.name,
                party=candidate.party,
                bio=candidate.bio,
                election=candidate.election_id
            )
            await candidate_in.save()
            return candidate_in

        except HTTPException as http_exc:
            # Re-raise HTTPException to avoid capturing it as a 500 error
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def get_candidate_by_id(id: UUID) -> Optional[CandidateModel]:
        candidate = await CandidateModel.get(id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return candidate


    @staticmethod
    async def update_candidate(id: UUID, data: CandidateUpdate) -> CandidateModel:
        try:
            candidate = await CandidateModel.get(id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            update_data = {k: v for k, v in data if v is not None}
            await candidate.update({"$set": update_data})
            return candidate
        except DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Duplicate key error")


    @staticmethod
    async def delete_candidate(id: UUID) -> None:
        candidate = await CandidateModel.get(id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        await candidate.delete()

