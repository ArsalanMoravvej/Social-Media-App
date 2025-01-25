from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

# Initialize FastAPI application
app = FastAPI()

# Define a Post model for request payload validation and serialization
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    optional_field: Optional[str] = None

# In-memory database simulation
posts_data = [
    {
        "id": 1,
        "title": "My first post!",
        "content": "This is my first post! And I'm gonna pass some text as my test data!",
        "published": True,
        "optional_field": None,
    },
    {
        "id": 2,
        "title": "My second post!",
        "content": "Here is another post for testing!",
        "published": False,
        "optional_field": None,
    },
]

# Helper function to find the index of a post by its ID
def get_post_index(post_id: int):
    for index, post in enumerate(posts_data):
        if post["id"] == post_id:
            return index
    return None

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

# Another path example
@app.get("/anotherpath")
async def another_path():
    return {"message": "This is another example path!"}

# Retrieve all posts
@app.get("/posts")
async def get_posts():
    return {"data": posts_data}

# Retrieve a specific post by ID
@app.get("/posts/{id}")
async def get_post(id: int):
    post = next((post for post in posts_data if post["id"] == id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} was not found."
        )
    return {"data": post}

# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    new_post = {"id": posts_data[-1]["id"] + 1, **post.dict()}
    posts_data.append(new_post)
    return {"message": new_post}

# Delete a post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post_index = get_post_index(id)
    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} was not found."
        )
    posts_data.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
