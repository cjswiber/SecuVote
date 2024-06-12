from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.election_schema import ElectionCreate, ElectionOut, ElectionUpdate
from app.services.election_service import ElectionService
from app.models.election_model import ElectionModel
from pymongo import errors
from uuid import UUID


election_router = APIRouter()


@election_router.post("/create", summary="Create a new election", response_model=ElectionOut)
async def create_election(data: ElectionCreate):
    try:
        return await ElectionService.create_election(data)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election already registered"
        )


@election_router.get("/{id}", summary="Get election details", response_model=ElectionOut)
async def get_election(id: str):
    election = await ElectionService.get_election_by_id(id)
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Election not found"
        )
    return election


@election_router.post("/update/{id}", summary="Update Election", response_model=ElectionOut)
async def update_election(id: str, data: ElectionUpdate):
    try:
        return await ElectionService.update_election(id, data)
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election does not exist"
        )


@election_router.delete("/delete/{id}", summary="Delete Election")
async def delete_election(id: str):
    try:
        await ElectionService.delete_election(id)
        return {"detail": "Election deleted successfully"}
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election does not exist"
        )


@election_router.post("/add-candidate-in-election/{id}/{candidate_id}", summary="Add Candidate to Election", response_model=ElectionOut)
async def add_candidate_to_election(id: str, candidate_id: UUID):
    try:
        return await ElectionService.add_candidate_to_election(id, candidate_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@election_router.delete("/remove-candidate-in-election/{id}/{candidate_id}", summary="Remove Candidate from Election")
async def remove_candidate_from_election(id: str, candidate_id: UUID):
    try:
        await ElectionService.remove_candidate_from_election(id, candidate_id)
        return {"detail": "Candidate removed from election successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

