from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.candidate_schema import CandidateCreate, CandidateOut, CandidateUpdate
from app.services.candidate_service import CandidateService
from app.models.candidate_model import CandidateModel
from pymongo import errors
from uuid import UUID


candidate_router = APIRouter()


@candidate_router.post("/create", summary="Create a new candidate", response_model=CandidateOut)
async def create_candidate(data: CandidateCreate):
    try:
        return await CandidateService.create_candidate(data)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate already registered"
        )


@candidate_router.get("/{candidate_id}", summary="Get candidate details", response_model=CandidateOut)
async def get_candidate(candidate_id: UUID):
    candidate = await CandidateService.get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    return candidate


@candidate_router.post("/update/{candidate_id}", summary="Update Candidate", response_model=CandidateOut)
async def update_candidate(candidate_id: UUID, data: CandidateUpdate):
    try:
        return await CandidateService.update_candidate(candidate_id, data)
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate does not exist"
        )


@candidate_router.delete("/delete/{candidate_id}", summary="Delete Candidate")
async def delete_candidate(candidate_id: UUID):
    try:
        await CandidateService.delete_candidate(candidate_id)
        return {"detail": "Candidate deleted successfully"}
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate does not exist"
        )

