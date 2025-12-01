from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from ..deps import get_current_user, get_db_dep
from ... import crud, schemas, models
from ...utils.storage import save_upload_file, COVERS_DIR

router = APIRouter()

@router.post("/", response_model=schemas.BlogOut)
async def create_blog(title: str = Form(...), content: str = Form(...), cover: Optional[UploadFile] = File(None), db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    cover_path = None
    if cover:
        cover_path = await save_upload_file(cover, COVERS_DIR)
        cover_path = "/" + cover_path.replace("\\", "/")
    blog = crud.create_blog(db, author=current_user, title=title, content=content, cover_image=cover_path)
    return blog

@router.get("/", response_model=List[schemas.BlogOut])
def list_blogs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db_dep)):
    return crud.list_blogs(db, skip=skip, limit=limit)

@router.get("/{blog_id}", response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db_dep)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{blog_id}", response_model=schemas.BlogOut)
async def edit_blog(blog_id: int, title: Optional[str] = Form(None), content: Optional[str] = Form(None), cover: Optional[UploadFile] = File(None), db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    cover_path = blog.cover_image
    if cover:
        cover_path = await save_upload_file(cover, COVERS_DIR)
        cover_path = "/" + cover_path.replace("\\", "/")
    updated = crud.update_blog(db, blog, title=title, content=content, cover_image=cover_path)
    return updated

@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db_dep), current_user: models.User = Depends(get_current_user)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    crud.delete_blog(db, blog)
    return {"status": "deleted"}