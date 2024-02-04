from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi.exceptions import HTTPException
from schema import order
from typing import List, Optional
from DataBase import table
from DataBase.base import Session, get_db
from sqlalchemy import select
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["Order"])

@router.post("", response_model=order.OutOrder)
async def create_order(
    user_id: str,
    order: order.CreateOrder=Body(...),
    db: Session = Depends(get_db)):
    '''
    Create Order API
    
        透過 body 傳入訂單資訊, 並在資料庫中新增訂單, 並更新商品庫存
        若商品庫存不足則回傳 400, indvestory not enough
        若商品不存在則回傳 404 ,  Product not found

    '''

    product_query = db.query(table.Products).filter(table.Products.id == order.product_id)
    product = product_query.scalar()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.investory < order.quantity:
        raise HTTPException(status_code=400, detail="investory not enough")
    
    product_query.update({"investory": product.investory - order.quantity})
    
    order = table.Orders(user_id=user_id, **order.model_dump())
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
        可透過 Query 參數選擇分頁
        skip: 起始位置
        limit: 取得筆數
    '''
    orders = db.query(table.Orders).offset(skip).limit(limit).all()
    return orders


@router.get("/{user_id}", response_model=List[order.OutOrder])
async def get_user_orders(user_id: str, skip: int = 0,
                         limit: int = 10, 
                         start_date: Optional[datetime] = None,
                         end_date: datetime = datetime.now(),
                         db: Session = Depends(get_db)):
    '''
    Get User Orders API

        透過 Path 選擇使用者，並取得使用者的訂單
        可透過 Query 參數選擇時間區間
        start_date: 起始時間
        end_date: 結束時間
        可透過 Query 參數選擇分頁
        skip: 起始位置
        limit: 取得筆數
    '''
    query = db.query(table.Orders).join(table.Users, table.Orders.user_id == table.Users.id).filter(table.Users.id == user_id)
    if start_date:
        orders = query.filter(table.Orders.order_date >= start_date,
                              table.Orders.order_date <= end_date).offset(skip).limit(limit).all()
    else:
        orders = query.filter(table.Orders.order_date <= end_date).offset(skip).limit(limit).all()
    return orders