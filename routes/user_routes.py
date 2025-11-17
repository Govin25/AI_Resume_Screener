from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.user_schema import UserCreate, UserCreateResponse, UserResponse, UserLogin
from services.user_services import create_user, get_all_users, get_user_by_id, delete_user_by_id, get_user_by_email, EmailAlreadExists
from uuid import UUID
from utils.log_config import logger
from utils.jwt_handler import create_access_token, get_authenticated_user
from utils.utility import verify_password

router = APIRouter()

@router.post("/register_user", response_model=UserCreateResponse)
async def register_user(user_data: UserCreate):
    
    # Logic to create a new user
    try:
        response = await create_user(user_data)
    except EmailAlreadExists as e:
        raise HTTPException(400, "Email already exist")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise e
    return response


@router.get("/get_users", response_model=List[UserResponse])
async def get_users(user_id: UUID = Depends(get_authenticated_user)):
    try:
        resp = await get_all_users()
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail="Error get users")
    return resp


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id:UUID, user: UUID = Depends(get_authenticated_user)):
    logger.info(f"GET user with ID:{user_id}") 
    try:
        row = await get_user_by_id(user_id)
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving user")

    if not row:
        raise HTTPException(status_code=404, detail=f"User not found for id: {user_id}")
    
    return row


@router.delete("/user")
async def delete_user(user_id: UUID = Depends(get_authenticated_user)):
    logger.info(f"delete user by id:{user_id}")
    
    result = await delete_user_by_id(user_id)


    if result:
        return {"message": "User deleted successfully", "user_id": user_id}

    raise HTTPException(status_code=400, detail="Unable to delete user")



@router.post("/user/login")
async def user_login(user: UserLogin):
    user_obj = await get_user_by_email(user.email)

    if not user_obj:
        raise HTTPException(400, "Invalid email")
    
    if not verify_password(user.password, user_obj.password_hash):
        raise HTTPException(401, "Invalid password")

    token = create_access_token({"user_id": str(user_obj.user_id)})
    return { "token": token}

