from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from .db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(30), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    bio = Column(Text, default="")
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    blogs = relationship("Blog", back_populates="author", cascade="all, delete-orphan")
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id", cascade="all, delete-orphan")
    received_messages = relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id", cascade="all, delete-orphan")

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    cover_image = Column(String(255), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User", back_populates="blogs")

class Follow(Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("follower_id", "following_id", name="_follower_following_uc"),)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(30), index=True, nullable=False)
    code = Column(String(10), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(100), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)