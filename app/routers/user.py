from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi.exceptions import HTTPException
from schema import user
from typing import List, Annotated
from DataBase import table
from DataBase.base import Session, get_db
from uuid import uuid4
from passlib.context import CryptContext
from routers import auth


router = APIRouter(prefix="/users", tags=["User"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("", response_model=user.OutUser)
async def create_user(user: user.CreateUser=Body(...), 
                      db: Session = Depends(get_db)):
    '''
    Create User API

        透過 body 傳入使用者資訊, 並在資料庫中新增使用者然後新建一個購物車, 並回傳使用者資訊
        預設使用者 id 為 PK, 並且不可重複

    '''
    if db.query(table.Users).filter(table.Users.id == user.id).scalar():
        raise HTTPException(status_code=400, detail="User already registered")
    user.password = pwd_context.hash(user.password)
    db.add(table.Users(**user.model_dump()))
    db.add(table.Carts(user_id=user.id))
    db.commit()
    return user

@router.delete("", response_model=user.OutUser)
async def delete_user(
    user: Annotated[table.Users, Depends(auth.get_current_user)],
    db: Session = Depends(get_db)):
    '''
    Delete User API

        刪除使用者以及使用者的購物車和購物車內的商品
    '''
    cart = db.query(table.Carts).filter(table.Carts.user_id == user.id).scalar()
    cart_query = db.query(table.Carts).join(table.CartItems, table.Carts.id == table.CartItems.cart_id)
    cart_items = cart_query.filter(table.CartItems.cart_id == cart.id).all()
    db.delete(user)
    db.delete(cart)
    for item in cart_items:
        db.delete(item)
    db.commit()
    return user

@router.get("", response_model=user.OutUser)
async def get_user(
    user: Annotated[table.Users, Depends(auth.get_current_user)], 
    db: Session = Depends(get_db)):
    '''
    Get User API

        取得登入使用者資訊
    '''
    return user

@router.get("/all", response_model=List[user.OutUser])
async def get_all_users(db: Session = Depends(get_db)):
    '''
    Get All Users API

        取得所有註冊的使用者資訊
    '''
    users = db.query(table.Users).all()
    return users

