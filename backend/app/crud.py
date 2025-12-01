from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

from . import models, schemas
from .utils.security import get_password_hash, verify_password

# User CRUD
def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = get_password_hash(user_in.password)
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        phone=user_in.phone,
        hashed_password=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, user: models.User, updates: dict):
    for k, v in updates.items():
        setattr(user, k, v)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()

# Blog CRUD
def create_blog(db: Session, author: models.User, title: str, content: str, cover_image: Optional[str]=None):
    blog = models.Blog(title=title, content=content, author_id=author.id, cover_image=cover_image)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def list_blogs(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Blog).order_by(models.Blog.created_at.desc()).offset(skip).limit(limit).all()

def update_blog(db: Session, blog: models.Blog, title: Optional[str], content: Optional[str], cover_image: Optional[str]):
    if title is not None:
        blog.title = title
    if content is not None:
        blog.content = content
    if cover_image is not None:
        blog.cover_image = cover_image
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def delete_blog(db: Session, blog: models.Blog):
    db.delete(blog)
    db.commit()

# Follow
def follow(db: Session, follower_id: int, following_id: int):
    if follower_id == following_id:
        return None
    exists = db.query(models.Follow).filter(models.Follow.follower_id==follower_id, models.Follow.following_id==following_id).first()
    if exists:
        return exists
    f = models.Follow(follower_id=follower_id, following_id=following_id)
    db.add(f)
    db.commit()
    db.refresh(f)
    return f

def unfollow(db: Session, follower_id: int, following_id: int):
    f = db.query(models.Follow).filter(models.Follow.follower_id==follower_id, models.Follow.following_id==following_id).first()
    if not f:
        return False
    db.delete(f)
    db.commit()
    return True

def list_followers(db: Session, user_id: int):
    return db.query(models.Follow).filter(models.Follow.following_id==user_id).all()

def list_following(db: Session, user_id: int):
    return db.query(models.Follow).filter(models.Follow.follower_id==user_id).all()

# Messages
def send_message(db: Session, sender_id: int, receiver_id: int, content: str):
    m = models.Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def list_conversation(db: Session, user1: int, user2: int, limit=50):
    return db.query(models.Message).filter(
        ((models.Message.sender_id==user1) & (models.Message.receiver_id==user2)) |
        ((models.Message.sender_id==user2) & (models.Message.receiver_id==user1))
    ).order_by(models.Message.created_at.asc()).limit(limit).all()

# OTP handling
def create_otp(db: Session, phone: str, code: str, expires_at: datetime):
    otp = models.OTP(phone=phone, code=code, expires_at=expires_at)
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp

def verify_otp(db: Session, phone: str, code: str):
    now = datetime.utcnow()
    otp = db.query(models.OTP).filter(models.OTP.phone==phone, models.OTP.code==code, models.OTP.used==False, models.OTP.expires_at > now).order_by(models.OTP.expires_at.desc()).first()
    if not otp:
        return False
    otp.used = True
    db.add(otp)
    db.commit()
    return True

# Token revocation
def revoke_token(db: Session, jti: str, expires_at: datetime):
    rt = models.RevokedToken(jti=jti, expires_at=expires_at)
    db.add(rt)
    db.commit()
    return rt

def is_token_revoked(db: Session, jti: str):
    rt = db.query(models.RevokedToken).filter(models.RevokedToken.jti==jti).first()
    if not rt:
        return False
    return True