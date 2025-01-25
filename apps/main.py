from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote

#models.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

# Another path example
@app.get("/anotherpath")
async def another_path():
    return {"message": "This is another example path!"}

