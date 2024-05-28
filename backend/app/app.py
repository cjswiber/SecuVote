from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}






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