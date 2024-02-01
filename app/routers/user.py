from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi.exceptions import HTTPException
from schema import user
from typing import List
from DataBase import table
from DataBase.base import Session, get_db
from uuid import uuid4



router = APIRouter(prefix="/users", tags=["User"])


@router.post("", response_model=user.OutUser)
async def create_user(user: user.CreateUser=Body(...), 
                      db_session: Session = Depends(get_db)):
    '''
    Create User API
    透過 body 傳入使用者資訊, 並在資料庫中新增使用者然後新建一個購物車
    '''

    if db_session.query(table.Users).filter(table.Users.id == user.id).scalar():
        raise HTTPException(status_code=400, detail="User already registered")
    
    db_session.add(table.Users(**user.model_dump()))
    db_session.commit()
    # db_session.refresh(user)

    return user

@router.delete("/", response_model=user.OutUser)
async def delete_user(user_id: str, 
                      db_session: Session = Depends(get_db)):
    '''
    Delete User API
    透過 Path 選擇使用者，並在資料庫中刪除使用者
    '''

    user = db_session.query(table.Users).filter(table.Users.id == user_id).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_session.delete(user)
    return user

@router.get("", response_model=List[user.OutUser])
async def get_all_users(db_session: Session = Depends(get_db)):
    '''
    Get All Users API
    取得所有使用者資訊
    '''
    users = db_session.query(table.Users).all()
    return users


@router.get("/", response_model=user.OutUser)
async def get_user(user_id: str, db_session: Session = Depends(get_db)):
    '''
    Get User API
    透過 Path 選擇使用者，並取得使用者資訊
    '''
    user = db_session.query(table.Users).filter(table.Users.id == user_id).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user