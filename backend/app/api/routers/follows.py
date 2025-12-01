from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..deps import get_current_user, get_db_dep
from ... import crud, schemas, models

router = APIRouter()

@router.post("/follow/{user_id}")
def follow_user(user_id: int, db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    target = crud.get_user(db, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    f = crud.follow(db, follower_id=current_user.id, following_id=user_id)
    if not f:
        raise HTTPException(status_code=400, detail="Cannot follow self or already following")
    return {"status": "followed"}

@router.post("/unfollow/{user_id}")
def unfollow_user(user_id: int, db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    ok = crud.unfollow(db, follower_id=current_user.id, following_id=user_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Not following")
    return {"status": "unfollowed"}

@router.get("/followers/{user_id}", response_model=List[schemas.FollowOut])
def get_followers(user_id: int, db: Session = Depends(get_db_dep)):
    return crud.list_followers(db, user_id)

@router.get("/following/{user_id}", response_model=List[schemas.FollowOut])
def get_following(user_id: int, db: Session = Depends(get_db_dep)):
    return crud.list_following(db, user_id)