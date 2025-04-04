from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Annotated, Optional


# Define a models for request payload validation and serialization

class UserBase(BaseModel):
    email:    EmailStr

class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id:         int
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class PostBase(BaseModel):
    title:     str
    content:   str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id:         int
    owner_id :  int
    owner: UserResponse 
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] | Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]