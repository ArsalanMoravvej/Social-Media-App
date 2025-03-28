from fastapi  import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils

from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

#User Registration Path
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):

    #hash the password
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Retrieve a specific user by ID
@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID {id} was not found.")
    
    return user