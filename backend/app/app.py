from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.user_model import User


@asynccontextmanager
# @app.on_event("startup")
async def lifespan(app: FastAPI):
    '''
        initialize crucial app services
    '''

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).secuvote

    await init_beanie(
        database=db_client,
        document_models = [
            User
        ]
    )

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)



'''
@app.get("/")
async def hello():
    return {"message": "Hello World"}
'''





'''
@app.get("/candidate/{id}")
async def get_candidate():
    return {"message": "Showing candidate"}


@app.put("/candidate/{id}")
async def modify_candidate():
    return {"message": "Candidate modified successfully"}


@app.delete("/candidate/{id}")
async def delete_candidate():
    return {"message": "Candidate deleted successfully"}


@app.get("/candidates")
async def get_candidates():
    return {"message": "Showing all candidates"}


@app.post("/candidates")
async def create_candidate():
    return {"message": "Created new candidate"}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
'''