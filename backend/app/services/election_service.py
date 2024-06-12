from app.schemas.election_schema import ElectionCreate, ElectionUpdate, ElectionOut
from app.models.election_model import ElectionModel
from app.models.candidate_model import CandidateModel
from fastapi import HTTPException, status
from typing import Optional, List
from uuid import UUID
from pymongo.errors import DuplicateKeyError
import json


class ElectionService:
    @staticmethod
    async def create_election(data: ElectionCreate) -> ElectionModel:
        election = ElectionModel(
            name=data.name,
            description=data.description,
            start_date=data.start_date,
            end_date=data.end_date
        )

        try:
            await election.insert()
            election_out = ElectionOut(
                id=str(election.id),
                name=election.name,
                description=election.description,
                start_date=election.start_date,
                end_date=election.end_date
            )
            return election_out

        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Election already registered"
            )
        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def get_election_by_id(id: str) -> Optional[ElectionOut]:
        election = await ElectionModel.find_one(ElectionModel.id == id)
        if not election:
            return None

        return ElectionOut(
            id=str(election.id),
            name=election.name,
            description=election.description,
            start_date=election.start_date,
            end_date=election.end_date,
            candidates=election.candidates
        )


    @staticmethod
    async def update_election(id: str, data: ElectionUpdate) -> ElectionOut:
        election = await ElectionModel.find_one(ElectionModel.id == id)
        if not election:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Election not found"
            )

        update_data = json.loads(data.model_dump(exclude_unset=True))
        for key, value in update_data.items():
            setattr(election, key, value)
        await election.save()

        return ElectionOut(
            id=str(election.id),
            name=election.name,
            description=election.description,
            start_date=election.start_date,
            end_date=election.end_date,
            candidates=election.candidates
        )


    @staticmethod
    async def add_candidate_to_election(id: str, candidate_id: UUID) -> ElectionModel:
        try:
            election = await ElectionModel.find_one(ElectionModel.id == id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")

            candidate = await CandidateModel.find_one(CandidateModel.candidate_id == candidate_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            election["candidates"].append(candidate)
            await election.save()
            return election

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def remove_candidate_from_election(id: str, candidate_id: UUID) -> ElectionModel:
        try:
            election = await ElectionModel.find_one(ElectionModel.id == id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")
            await election.delete()
            candidate = await CandidateModel.find_one(CandidateModel.candidate_id == candidate_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            election.candidates = [c for c in election.candidates if c != candidate_id]
            await election.save()
            return election

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def delete_election(id: str) -> None:
        election = await ElectionModel.find_one(ElectionModel.id == id)
        if not election:
            raise HTTPException(status_code=404, detail="Election not found")
        await election.delete()

