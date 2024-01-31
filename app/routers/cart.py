from fastapi import APIRouter, Body
from schema import cart
from typing import List


router = APIRouter(prefix="/carts", tags=["Cart"])

@router.post("/{cart_id}/items", response_model=List[cart.OutCartItem])
async def add_item(cart_id: int, cart_item: cart.CartItem=Body(...)):
    '''
    Add Item to Cart API
    透過 Path 選擇購物車，並在資料庫中新增商品至購物車
    一次一種商品
    '''
    return {"message": "Add Item to Cart"}

@router.put("/{cart_id}/items", response_model=cart.OutCartItem)
async def update_item(cart_id: int, id: int, cart_item: cart.UpdateCartItem=Body(...)):
    '''
    Update Item in Cart API
    透過 Path 選擇購物車及商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
    '''
    return {"message": "Update Item in Cart"}


@router.delete("/{cart_id}/items/", response_model=List[cart.OutCartItem])
async def delete_item(cart_id: int, id: int):
    '''
    Delete Item in Cart API
    透過 Path 選擇購物車及商品，並在資料庫中刪除商品
    '''
    return {"message": "Delete Item in Cart"}


@router.get("/{cart_id}/items", response_model=List[cart.OutCartItem])
async def get_all_items(cart_id: int):
    '''
    Get All Items in Cart API
    透過 Path 選擇購物車，並取得購物車中所有商品資訊
    '''
    return {"message": "Get All Items in Cart"}


@router.get("/{cart_id}/items", response_model=cart.OutCartItem)
async def get_item(cart_id: int, id: int):
    '''
    Get Item in Cart API
    透過 Path 選擇購物車及商品，並取得商品資訊
    '''
    return {"message": "Get Item in Cart"}


@router.get("", response_model=List[cart.Cart])
async def get_all_carts():
    '''
    Get All Carts API
    取得所有購物車資訊
    '''
    return {"message": "Get All Carts"}

@router.get("/", response_model=cart.Cart)
async def get_cart(id: int):
    '''
    Get Cart API
    透過 Path 選擇購物車，並取得購物車資訊
    '''
    return {"message": "Get Cart"}



