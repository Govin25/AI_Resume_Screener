import uuid
from utils.utility import hash_password
from utils.log_config import logger
from sqlalchemy import desc
from schemas.user_schema import UserCreate
from fastapi import HTTPException
from models.base import session 
from models.user import User

async def get_user_by_email(email: str):
    """
    Validate that the email is unique in the database.
    """
    user = session.query(User).filter(User.email == email).first()
    return user


async def validate_email_unique(email: str):
    """
    Validate that the email is unique in the database.
    """
    existing_user = session.query(User).filter(User.email == email).first()
    if existing_user:
        raise EmailAlreadExists("Email already exists.")
    
    return existing_user



async def create_user(user_data:UserCreate):
    """
    Create a new user in the database.
    """
    try:
        await validate_email_unique(user_data.email)
        # Hash the password before storing
        hashed_password = hash_password(user_data.password)
    
        u_id = uuid.uuid4()
        new_user = User(
            user_id=u_id, 
            email=user_data.email,
            password_hash=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role
        )
        session.add(new_user)
        session.commit()
    
    except EmailAlreadExists as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise e

    return {"user_id":u_id,
            "message":"User created successfully"}


async def get_all_users_db():
    try :
        users = session.query(User).order_by(desc(User.created_at)).all()
    except Exception as e:
        logger.error(f"error fethcing all users:{e}")
        raise HTTPException(status_code=500, detail="Error fetching users")
    return users


async def get_all_users():
    users = await get_all_users_db()
    user_detail=[]
    for u in users:
        user_detail.append({
            "user_id":u.user_id,
            "name":u.full_name,
            "email":u.email 
        })
        
    return user_detail

async def get_user_by_id_into_db(user_id):
    try:
        resp = session.query(User).filter(User.user_id==user_id).first()
    except Exception as e:
        logger.error(f"Error fetching user by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user")

    return resp 

async def get_user_by_id(user_id):

    resp = await get_user_by_id_into_db(user_id)
    
    if resp is None:
        raise HTTPException(status_code=404, detail=f"User not found for id: {user_id}")
    
    user ={"user_id":resp.user_id, "name":resp.full_name, "email":resp.email}

    return user


async def delete_user_by_id(user_id):
    
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    logger.info(f"User deleted successfully: {user_id}")
    return True

    
class EmailAlreadExists(Exception):
    pass

    

    
   
