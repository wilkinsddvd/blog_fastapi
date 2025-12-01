from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str
    bio: Optional[str] = ""
    avatar: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    bio: Optional[str]

# Auth
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[int]
    exp: Optional[int]
    jti: Optional[str]

# Blog
class BlogCreate(BaseModel):
    title: str
    content: str

class BlogOut(BaseModel):
    id: int
    title: str
    content: str
    cover_image: Optional[str] = None
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Follow
class FollowOut(BaseModel):
    follower_id: int
    following_id: int

# Message
class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime
    read: bool

    class Config:
        orm_mode = True