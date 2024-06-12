from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.vote_schema import VoteCreate, VoteUpdate, VoteOut
from app.services.vote_service import VoteService
from app.models.vote_model import VoteModel
from pymongo import errors
from uuid import UUID


vote_router = APIRouter()


@vote_router.post("/create-vote", summary="Create a new vote", response_model=VoteOut)
async def create_vote(user_id: str, candidate_id: str, election_id: str):
    try:
        return await VoteService.create_vote(user_id, candidate_id, election_id)
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote already registered"
        )


@vote_router.get("/vote/{id}", summary="Get vote details", response_model=VoteOut)
async def get_vote(id: str):
    vote = await VoteService.get_vote_by_id(id)
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote not found"
        )
    return vote


@vote_router.delete("/delete-vote/{id}", summary="Delete Vote")
async def delete_vote(id: str):
    try:
        await VoteService.delete_vote(id)
        return {"detail": "Vote deleted successfully"}
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote does not exist"
        )



'''
@vote_router.post("/update-vote/{id}", summary="Update Candidate", response_model=CandidateOut)
async def update_candidate(id: str, data: CandidateUpdate):
    try:
        return await CandidateService.update_candidate(id, data)
    except errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate does not exist"
        )
    


@candidate_router.post("/add-election-to-candidate/{candidate_id}/{election_id}", summary="Add Election to Candidate", response_model=CandidateOut)
async def add_election_to_candidate(candidate_id: str, election_id: str):
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
async def remove_election_from_candidate(candidate_id: str, election_id: str):
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
'''