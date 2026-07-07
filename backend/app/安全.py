# 安全.py — 密码加密与JWT令牌（主要代码）
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import os

SECRET_KEY = "smartagro-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480


def hash_password(password: str) -> str:
    salt = os.urandom(32).hex()
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}${h.hex()}"


def verify_password(plain: str, hashed: str) -> bool:
    try:
        salt, stored = hashed.split("$", 1)
        h = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt.encode(), 100000)
        return h.hex() == stored
    except (ValueError, AttributeError):
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
