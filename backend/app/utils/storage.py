import os
from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
AVATAR_DIR = UPLOAD_DIR / "avatars"
COVERS_DIR = UPLOAD_DIR / "covers"

for d in (UPLOAD_DIR, AVATAR_DIR, COVERS_DIR):
    os.makedirs(d, exist_ok=True)

async def save_upload_file(file: UploadFile, folder: Path) -> str:
    ext = Path(file.filename).suffix or ""
    filename = f"{uuid4().hex}{ext}"
    file_path = folder / filename
    # read async and write binary
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    # return path relative to server root
    return str(file_path)