from app.schemas.election_schema import ElectionCreate, ElectionUpdate
from app.models.election_model import ElectionModel
from app.models.candidate_model import CandidateModel
from fastapi import HTTPException, status
from typing import Optional, List
from uuid import UUID
from pymongo.errors import DuplicateKeyError
from beanie import Link, PydanticObjectId


class ElectionService:
    @staticmethod
    async def get_election_by_id(election_id: PydanticObjectId) -> Optional[ElectionModel]:
        election = await ElectionModel.find_one(ElectionModel.election_id == election_id)
        if not election:
            raise HTTPException(status_code=404, detail="Election not found")
        return election


    @staticmethod
    async def create_election(election: ElectionCreate) -> ElectionModel:
        try:
            existing_election = await ElectionModel.find_one(ElectionModel.name == election.name)
            if existing_election:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Election already exists"
                )

            election_in = ElectionModel(
                name=election.name,
                description=election.description,
                start_date=election.start_date,
                end_date=election.end_date,
                candidates=election.candidates
            )
            await election_in.save()
            return election_in

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def update_election(election_id: UUID, data: ElectionUpdate) -> ElectionModel:
        try:
            election = await ElectionModel.find_one(ElectionModel.election_id == election_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")
            update_data = {k: v for k, v in data if v is not None}
            await election.update({"$set": update_data})
            return election

        except DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Duplicate data error")


    @staticmethod
    async def add_candidate_to_election(election_id: UUID, candidate_id: UUID) -> ElectionModel:
        try:
            election = await ElectionModel.find_one(ElectionModel.election_id == election_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")

            candidate = await CandidateModel.find_one(CandidateModel.candidate_id == candidate_id)
            if not candidate:
                raise HTTPException(status_code=404, detail="Candidate not found")

            if candidate_id not in election.candidates:
                election.candidates.append(candidate_id)
                await election.save()
                
                # Add the election to the candidate's list of elections
                if election_id not in candidate.elections:
                    candidate.elections.append(election_id)
                    await candidate.save()
                    
            return election

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def remove_candidate_from_election(election_id: UUID, candidate_id: UUID) -> ElectionModel:
        try:
            election = await ElectionModel.find_one(ElectionModel.election_id == election_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")

            if candidate_id in election.candidates:
                election.candidates = [c for c in election.candidates if c != candidate_id]
                await election.save()

                # Remove the election from the candidate's list of elections
                candidate = await CandidateModel.find_one(CandidateModel.candidate_id == candidate_id)
                if candidate and election_id in candidate.elections:
                    candidate.elections = [e for e in candidate.elections if e != election_id]
                    await candidate.save()
                    
            return election

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    @staticmethod
    async def delete_election(election_id: UUID) -> None:
        try:
            election = await ElectionModel.find_one(ElectionModel.election_id == election_id)
            if not election:
                raise HTTPException(status_code=404, detail="Election not found")
            await election.delete()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        
        