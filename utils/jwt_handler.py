from datetime import datetime, timedelta, timezone
from utils.utility import hash_password, verify_password
from fastapi import HTTPException, Depends, status
import jwt
import os
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uuid import UUID

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITUM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 7))

bearer = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    try:
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as err:
        raise HTTPException(400, "invalid data")
    return token


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token.
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")


def get_authenticated_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    token = creds.credentials
    try:
        payload = decode_token(token)
    except Exception as err:
        raise err
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token")
    return UUID(user_id)
