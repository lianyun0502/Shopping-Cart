from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from schema import cart
from typing import List
from DataBase import table
from DataBase.base import Session, get_db


router = APIRouter(prefix="/carts", tags=["Cart"])

@router.post("/{cart_id}/items", response_model=cart.OutCartItem)
async def add_item(cart_id: int, cart_item: cart.CreateCartItem=Body(...), db: Session = Depends(get_db)):
    '''
    Add Item to Cart API
    透過 Path 選擇購物車，並在資料庫中新增商品至購物車
    一次一種商品
    '''
    cart_item = table.CartItems(cart_id=cart_id, **cart_item.model_dump())
    cart = db.query(table.Carts).filter(table.Carts.id == cart_id).scalar()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.put("/items", response_model=cart.OutCartItem)
async def update_item(id: int, cart_item: cart.UpdateCartItem=Body(...),
                      db: Session = Depends(get_db)):
    '''
    Update Item in Cart API
    透過 Path 選擇購物車及商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
    '''
    db.query(table.CartItems).filter(table.CartItems.id == id).update(cart_item.model_dump())
    db.commit()
    out_cart_item = db.query(table.CartItems).filter(table.CartItems.id == id).scalar()
    return out_cart_item


@router.delete("/items/", response_model=List[cart.OutCartItem])
async def delete_item(id: int, db: Session = Depends(get_db)):
    '''
    Delete Item in Cart API
    透過 Path 選擇購物車及商品，並在資料庫中刪除商品
    '''
    query = db.query(table.CartItems).filter(table.CartItems.id == id)
    out_cart_item = query.scalar()
    if out_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    query.delete()
    db.commit()
    return out_cart_item


@router.get("/{cart_id}/items", response_model=List[cart.OutCartItem])
async def get_all_items(cart_id: int, db: Session = Depends(get_db)):
    '''
    Get All Items in Cart API
    透過 Path 選擇購物車，並取得購物車中所有商品資訊
    '''
    cart_items = db.query(table.CartItems).filter(table.CartItems.cart_id == cart_id).all()
    return cart_items


@router.get("/{cart_id}/items/", response_model=cart.OutCartItem)
async def get_item(cart_id: int, id: int, db: Session = Depends(get_db)):
    '''
    Get Item in Cart API
    透過 Path 選擇購物車及商品，並取得商品資訊
    '''
    cart_item = db.query(table.CartItems).filter(table.CartItems.id == id and table.CartItems.cart_id == cart_id).scalar()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    return cart_item

@router.post("", response_model=cart.OutCart)
async def create_cart(cart: cart.CreateCart=Body(...), db: Session = Depends(get_db)):
    '''
    Create Cart API
    透過 body 傳入購物車資訊, 並在資料庫中新增購物車
    '''
    cart = table.Carts(**cart.model_dump())
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

@router.get("", response_model=List[cart.Cart])
async def get_all_carts(db: Session = Depends(get_db)):
    '''
    Get All Carts API
    取得所有購物車資訊
    '''
    carts = db.query(table.Carts).all()
    return carts

@router.get("/", response_model=cart.Cart)
async def get_cart(id: int, db: Session = Depends(get_db)):
    '''
    Get Cart API
    透過 Path 選擇購物車，並取得購物車資訊
    '''
    cart = db.query(table.Carts).filter(table.Carts.id == id).scalar()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart



