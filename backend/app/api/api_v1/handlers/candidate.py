from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.candidate_schema import CandidateCreate, CandidateOut, CandidateUpdate
from app.services.candidate_service import CandidateService
from app.models.candidate_model import CandidateModel
from pymongo import errors
from uuid import UUID
from beanie import PydanticObjectId


candidate_router = APIRouter()


@candidate_router.post("/create", summary="Create a new candidate", response_model=CandidateOut)
async def create_candidate(data: CandidateCreate):
    try:
        candidate = await CandidateService.create_candidate(data)
        return CandidateOut(
            candidate_id=str(candidate.candidate_id),  # Convertir a cadena
            name=candidate.name,
            party=candidate.party,
            bio=candidate.bio,
            elections=[str(election) for election in candidate.elections]  # Convertir a cadena
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@candidate_router.get("/{candidate_id}", summary="Get candidate details", response_model=CandidateOut)
async def get_candidate(candidate_id: str):
    try:
        candidate = await CandidateService.get_candidate_by_id(PydanticObjectId(candidate_id))
        return CandidateOut(
            candidate_id=str(candidate.candidate_id),  # Convertir a cadena
            name=candidate.name,
            party=candidate.party,
            bio=candidate.bio,
            elections=[str(election) for election in candidate.elections]  # Convertir a cadena
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


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

