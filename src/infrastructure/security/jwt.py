from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status
from jose import jwt, JWTError

from src.core.config import get_settings

settings = get_settings()
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM


def create_access_token(email: str, user_id: str, expires_delta: timedelta) -> str:
    encode = {"sub": email, "id": user_id}
    encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(encode, JWT_SECRET_KEY, JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
