from fastapi  import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. import models, schemas, oauth2

from ..database import get_db
from sqlalchemy.orm import Session

from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Retrieve all posts
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ""):
    
    #previously it was:
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit)\.all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
              .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
              .group_by(models.Post.id)\
              .filter(models.Post.title.contains(search))\
              .offset(skip)\
              .limit(limit)\
              .all()

    return posts

# Retrieve a specific post by ID
@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int,
                   db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)):

    #previously without join
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
              .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
              .group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found.")
    
    return post

# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate,
                      db:Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):

    new_post = models.Post(
        **post.model_dump(),
        owner_id=current_user.id)
    
    # Alternatively parameters can be passed to model as an unpacked dictionary 
    # [specially recommended for when there are many parameters]
    # new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# Delete a post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,
                      db:Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found.")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post by ID
@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int,
                      post: schemas.PostCreate,
                      db:Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found.")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")
    
    

    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()

    return post_query.first()
