from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.election_schema import ElectionCreate, ElectionOut, ElectionUpdate
from app.services.election_service import ElectionService
from app.models.election_model import ElectionModel
from pymongo import errors
from uuid import UUID
from beanie import PydanticObjectId


election_router = APIRouter()


@election_router.post("/create", summary="Create a new election", response_model=ElectionOut)
async def create_election(data: ElectionCreate):
    try:
        election = await ElectionService.create_election(data)
        return ElectionOut(
            election_id=str(election.election_id),  # Transform to string
            name=election.name,
            description=election.description,
            start_date=election.start_date,
            end_date=election.end_date,
            candidates=election.candidates
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@election_router.get("/{election_id}", summary="Get election details", response_model=ElectionOut)
async def get_election(election_id: str):
    try:
        election = await ElectionService.get_election_by_id(PydanticObjectId(election_id))
        return ElectionOut(
            election_id=str(election.election_id),   # Transform to string
            name=election.name,
            description=election.description,
            start_date=election.start_date,
            end_date=election.end_date,
            candidates=election.candidates
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



@election_router.post("/update/{election_id}", summary="Update Election", response_model=ElectionOut)
async def update_election(election_id: UUID, data: ElectionUpdate):
    try:
        return await ElectionService.update_election(election_id, data)
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election does not exist"
        )


@election_router.delete("/delete/{election_id}", summary="Delete Election")
async def delete_election(election_id: UUID):
    try:
        await ElectionService.delete_election(election_id)
        return {"detail": "Election deleted successfully"}
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election does not exist"
        )


@election_router.post("/add_candidate_in_election/{election_id}/{candidate_id}", summary="Add Candidate to Election", response_model=ElectionOut)
async def add_candidate_to_election(election_id: UUID, candidate_id: UUID):
    try:
        return await ElectionService.add_candidate_to_election(election_id, candidate_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@election_router.delete("/remove_candidate_in_election/{election_id}/{candidate_id}", summary="Remove Candidate from Election")
async def remove_candidate_from_election(election_id: UUID, candidate_id: UUID):
    try:
        await ElectionService.remove_candidate_from_election(election_id, candidate_id)
        return {"detail": "Candidate removed from election successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

