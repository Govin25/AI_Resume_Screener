from datetime import timezone, timedelta
from passlib.context import CryptContext


IST = timezone(timedelta(hours=5, minutes=30))  # Define IST timezone once


def format_datetime_to_ist(dt):
    """Convert a datetime object to IST timezone and format it as a string."""
    return dt.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")


# utils/hash.py
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
