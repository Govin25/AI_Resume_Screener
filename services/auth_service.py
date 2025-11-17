from models.user import User
from utils.jwt_handler import create_access_token
from utils.utility import verify_password
from models.base import session
from utils.log_config import logger


async def authenticate_user(email: str, password: str):
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            logger.warning(f"Login failed: user {email} not found.")
            return None

        if not verify_password(password, user.password_hash):
            logger.warning(f"Login failed: incorrect password for {email}.")
            return None

        return user

    except Exception as e:
        logger.error(f"Auth error: {e}")
        return None





