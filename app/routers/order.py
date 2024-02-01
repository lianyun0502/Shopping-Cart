from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi.exceptions import HTTPException
from schema import order
from typing import List
from DataBase import table
from DataBase.base import Session, get_db
from sqlalchemy import select


router = APIRouter(prefix="/orders", tags=["Order"])

@router.post("", response_model=order.OutOrder)
async def create_order(order: order.CreateOrder=Body(...),
                       db: Session = Depends(get_db)):
    '''
    Create Order API
    透過 body 傳入訂單資訊, 並在資料庫中新增訂單
    '''
    order = table.Orders(**order.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=List[order.OutOrder])
async def get_all_orders(db: Session = Depends(get_db),
                         skip: int = 0,
                         limit: int = 10):
    '''
    Get All Orders API
    取得所有訂單資訊
    '''
    orders = db.query(table.Orders).offset(skip).limit(limit).all()
    return orders


@router.get("/", response_model=order.OutOrder)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    '''
    Get Order API
    透過 Qurey 選擇訂單，並取得訂單資訊
    '''
    order = db.query(table.Orders).filter(table.Orders.id == order_id).scalar()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@router.get("/users/", response_model=List[order.OutOrder])
async def get_user_orders(user_id: str, skip: int = 0,
                         limit: int = 10, db: Session = Depends(get_db)):
    '''
    Get User Orders API
    透過 Qurey 選擇使用者，並取得使用者的所有訂單
    '''
    orders = db.query(table.Orders).filter(table.Orders.user_id == user_id).offset(skip).limit(limit).all()
    return orders