from fastapi import APIRouter, Body, Path, Query
from schema import order
from typing import List


router = APIRouter(prefix="/orders", tags=["Order"])

@router.post("", response_model=order.OutOrder)
async def create_order():
    '''
    Create Order API
    透過 body 傳入訂單資訊, 並在資料庫中新增訂單
    '''
    return {"message": "Create Order"}


@router.get("", response_model=List[order.OutOrder])
async def get_all_orders():
    '''
    Get All Orders API
    取得所有訂單資訊
    '''
    return {"message": "Get All Orders"}


@router.get("/", response_model=order.OutOrder)
async def get_order(order_id: int):
    '''
    Get Order API
    透過 Path 選擇訂單，並取得訂單資訊
    '''
    return {"message": "Get Order"}