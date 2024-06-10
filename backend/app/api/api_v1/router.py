from fastapi import APIRouter
from app.api.api_v1.handlers import user
from app.api.api_v1.handlers import candidate
from app.api.api_v1.handlers import election
from app.api.auth.jwt import auth_router


router = APIRouter()


router.include_router(user.user_router, prefix="/user", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(candidate.candidate_router, prefix="/candidate", tags=["candidate"])
router.include_router(election.election_router, prefix="/election", tags=["election"])
