from fastapi import APIRouter, Body, Path, Query
from schema import user
from typing import List



router = APIRouter(prefix="/users", tags=["User"])


@router.post("", response_model=user.OutUser)
async def create_user(user: user.CreateUser=Body(...)):
    '''
    Create User API
    透過 body 傳入使用者資訊, 並在資料庫中新增使用者
    '''
    return {"message": "Create User"}

@router.delete("/", response_model=user.OutUser)
async def delete_user(user_id: str):
    '''
    Delete User API
    透過 Path 選擇使用者，並在資料庫中刪除使用者
    '''
    return {"message": "Delete User"}

@router.get("", response_model=List[user.OutUser])
async def get_all_users():
    '''
    Get All Users API
    取得所有使用者資訊
    '''
    return {"message": "Get All Users"}


@router.get("/", response_model=user.OutUser)
async def get_user(user_id: str):
    '''
    Get User API
    透過 Path 選擇使用者，並取得使用者資訊
    '''
    return {"message": "Get User"}