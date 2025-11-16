from fastapi import APIRouter, HTTPException
from typing import List
from schemas.user_schema import UserCreate, UserCreateResponse, UserResponse
from services.user_services import create_user, get_all_users, get_user_by_id, delete_user_by_id
from uuid import UUID
from utils.log_config import logger

router = APIRouter()

@router.post("/register_user", response_model=UserCreateResponse)
async def register_user(user_data: UserCreate):
    
    # Logic to create a new user
    try:
        response = await create_user(user_data)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")
    return response


@router.get("/get_users", response_model=List[UserResponse])
async def get_users():
    try:
        resp = await get_all_users()
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail="Error get users")
    return resp


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id:UUID):
    logger.info(f"GET user with ID:{user_id}") 
    try:
        row = await get_user_by_id(user_id)
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving user")

    if not row:
        raise HTTPException(status_code=404, detail=f"User not found for id: {user_id}")
    
    return row


@router.delete("/user{user_id}/delete_user")
async def delete_user(user_id:UUID):
    logger.info(f"delete user by id:{user_id}")
    
    result = await delete_user_by_id(user_id)


    if result:
        return {"message": "User deleted successfully", "user_id": user_id}

    raise HTTPException(status_code=400, detail="Unable to delete user")





    
   
