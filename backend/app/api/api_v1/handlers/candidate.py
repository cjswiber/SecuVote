from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.candidate_schema import CandidateCreate, CandidateOut, CandidateUpdate
from app.services.candidate_service import CandidateService
from app.models.candidate_model import CandidateModel
from pymongo import errors
from uuid import UUID


candidate_router = APIRouter()


@candidate_router.post("/create-candidate", summary="Create a new candidate", response_model=CandidateOut)
async def create_candidate(data: CandidateCreate):
    try:
        return await CandidateService.create_candidate(data)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate already registered"
        )


@candidate_router.get("/candidate/{id}", summary="Get candidate details", response_model=CandidateOut)
async def get_candidate(id: str):
    candidate = await CandidateService.get_candidate_by_id(id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    return candidate


@candidate_router.post("/update-candidate/{id}", summary="Update Candidate", response_model=CandidateOut)
async def update_candidate(id: str, data: CandidateUpdate):
    try:
        return await CandidateService.update_candidate(id, data)
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate does not exist"
        )


@candidate_router.delete("/delete-candidate/{id}", summary="Delete Candidate")
async def delete_candidate(id: str):
    try:
        await CandidateService.delete_candidate(id)
        return {"detail": "Candidate deleted successfully"}
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate does not exist"
        )

@candidate_router.post("/add-election-to-candidate/{candidate_id}/{election_id}", summary="Add Election to Candidate", response_model=CandidateOut)
async def add_election_to_candidate(candidate_id: UUID, election_id: UUID):
    try:
        return await CandidateService.add_election_to_candidate(candidate_id, election_id)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the election to the candidate"
        )


@candidate_router.delete("/remove-election-from-candidate/{candidate_id}/{election_id}", summary="Remove Election from Candidate", response_model=CandidateOut)
async def remove_election_from_candidate(candidate_id: UUID, election_id: UUID):
    try:
        return await CandidateService.remove_election_from_candidate(candidate_id, election_id)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while removing the election from the candidate"
        )
