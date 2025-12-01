from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import jwt

from ..deps import get_db_dep
from ... import crud, schemas, models
from ...utils.security import create_access_token, get_password_hash
from ...core.config import settings

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db_dep)):
    existing = db.query(models.User).filter(
        (models.User.username==user_in.username) |
        (models.User.email==user_in.email) |
        (models.User.phone==user_in.phone)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with that username/email/phone already exists")
    user = crud.create_user(db, user_in)
    return user

@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest = Body(...), db: Session = Depends(get_db_dep)):
    user = crud.authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/request_password_reset")
def request_password_reset(phone: str = Body(...), db: Session = Depends(get_db_dep)):
    # Generate OTP and "send" (dev mode -> return in response)
    code = f"{random.randint(100000, 999999)}"
    expires = datetime.utcnow() + timedelta(minutes=10)
    crud.create_otp(db, phone=phone, code=code, expires_at=expires)
    if settings.SMS_PROVIDER_ENABLED:
        # integrate SMS gateway here
        pass
    # In development return the code so developer can test
    return {"status": "ok", "message": "OTP sent (in development mode OTP is returned)", "otp": code}

@router.post("/reset_password")
def reset_password(phone: str = Body(...), code: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db_dep)):
    valid = crud.verify_otp(db, phone, code)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    user = db.query(models.User).filter(models.User.phone==phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    return {"status": "ok"}

@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db_dep)):
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    token = parts[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        # if expired, still accept logout (no need to store)
        return {"status": "ok", "detail": "token already expired"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")
    jti = payload.get("jti")
    exp = payload.get("exp")
    if not jti or not exp:
        raise HTTPException(status_code=400, detail="Invalid token payload")
    expires_at = datetime.utcfromtimestamp(int(exp))
    crud.revoke_token(db, jti=jti, expires_at=expires_at)
    return {"status": "ok"}