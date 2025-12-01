from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from .core.config import settings
from .db.session import engine, Base
from .api.routers import auth, users, blogs, follows, messages

# Ensure uploads folder exists
os.makedirs("uploads/avatars", exist_ok=True)
os.makedirs("uploads/covers", exist_ok=True)

# Create DB tables (simple auto-create for development)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Blog API")

# CORS - allow local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(blogs.router, prefix="/blogs", tags=["blogs"])
app.include_router(follows.router, prefix="/follows", tags=["follows"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])

@app.get("/")
def read_root():
    return {"message": "Personal Blog API is running"}