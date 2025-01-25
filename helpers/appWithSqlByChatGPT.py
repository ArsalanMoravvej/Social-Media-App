from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Initialize FastAPI application
app = FastAPI()

# Database configuration
DATABASE_URL = "sqlite:///./test.db"  # Change to your preferred database URL
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a Post model for the database
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    optional_field = Column(String, nullable=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

# Retrieve all posts
@app.get("/posts")
async def get_posts(db: Session = next(get_db())):
    posts = db.query(Post).all()
    return {"data": posts}

# Retrieve a specific post by ID
@app.get("/posts/{id}")
async def get_post(id: int, db: Session = next(get_db())):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} was not found."
        )
    return {"data": post}

# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = next(get_db())):
    new_post = Post(
        title=post.title,
        content=post.content,
        published=post.published,
        optional_field=post.optional_field
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# Delete a post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = next(get_db())):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} was not found."
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
