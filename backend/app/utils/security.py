from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt, uuid

from ..core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: int, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    expire = now + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = str(uuid.uuid4())
    payload = {
        "sub": str(subject),
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": jti
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except Exception:
        raise