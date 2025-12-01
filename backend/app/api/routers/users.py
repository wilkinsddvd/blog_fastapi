from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..deps import get_current_user, get_db_dep
from ... import crud, schemas, models
from ...utils.storage import save_upload_file, AVATAR_DIR

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def read_my_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserOut)
def update_my_profile(updates: schemas.UserUpdate, db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    update_data = updates.dict(exclude_unset=True)
    user = crud.update_user(db, current_user, update_data)
    return user

@router.post("/me/avatar", response_model=schemas.UserOut)
async def upload_avatar(file: UploadFile = File(...), db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    path = await save_upload_file(file, AVATAR_DIR)
    # store relative path for serving
    current_user.avatar = "/" + path.replace("\\", "/")
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me")
def delete_account(db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    crud.delete_user(db, current_user)
    return {"status": "deleted"}