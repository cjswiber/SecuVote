from app.schemas.candidate_schema import CandidateCreate, CandidateUpdate
from app.models.candidate_model import CandidateModel
from app.models.election_model import ElectionModel
from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from beanie import Link, PydanticObjectId


class CandidateService:
    @staticmethod
    async def create_candidate(candidate: CandidateCreate) -> CandidateModel:
        try:
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
                elections=candidate.elections
            )

            # Guardar el candidato
            await candidate_in.save()

            # Actualizar cada elección con el nuevo candidato
            for election_id in candidate.elections:
                election = await ElectionModel.find_one(ElectionModel.election_id == election_id)
                if election:
                    election.candidates.append(candidate_in.candidate_id)
                    await election.save()

            return candidate_in

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def get_candidate_by_id(id: PydanticObjectId) -> Optional[CandidateModel]:
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

