from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from schema import cart
from typing import List, Optional, Annotated
from DataBase import table
from DataBase.base import Session, get_db
from routers import auth


router = APIRouter(prefix="/carts", tags=["Cart"])


def is_user_exist(user_id:str, db:Session)->Optional[table.Users]:
    user = db.query(table.Users).filter(table.Users.id == user_id).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/items", response_model=cart.OutCartItem)
async def add_item(
    user: Annotated[table.Users, Depends(auth.get_current_user)], 
    cart_item: cart.CreateCartItem=Body(...), 
    db: Session = Depends(get_db)):
    '''
    Add Item to Cart API

        新增商品至User的購物車
        一次一種商品
        cart_item: 要加入購物車的商品資訊
    '''
    # user = is_user_exist(user_id=user_id, db=db)
    cart = db.query(table.Carts).filter(table.Carts.user_id == user.id).scalar()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = table.CartItems(cart_id=cart.id, **cart_item.model_dump())
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.put("/items", response_model=cart.OutCartItem)
async def update_item(
    user: Annotated[table.Users, Depends(auth.get_current_user)], 
    id: int, 
    cart_item: cart.UpdateCartItem=Body(...),
    db: Session = Depends(get_db)
    ):
    '''
    Update Item in Cart API

        並根據body更新user在購物車中的商品資訊，只能更新部分欄位
        如果購物車或商品不存在，則回傳 404, Cart or Item not found


    '''
    cart = db.query(table.Carts).filter(table.Carts.user_id == user.id).scalar()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item_query = db.query(table.CartItems).filter(table.CartItems.cart_id == cart.id and table.CartItems.id == id)
    out_cart_item = cart_item_query.scalar()
    if out_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    cart_item_query.update(cart_item.model_dump())
    db.commit()
    db.refresh(out_cart_item)

    return out_cart_item


@router.delete("/items", response_model=cart.OutCartItem)
async def delete_item(
    user: Annotated[table.Users, Depends(auth.get_current_user)], 
    id: int, 
    db: Session = Depends(get_db)):
    '''
    Delete Item in Cart API

        刪除user購物車中的商品
        如果商品不存在，則回傳 404, Cart Item not found
        如果購物車不存在，則回傳 404, Cart not found
    '''
    cart = db.query(table.Carts).filter(table.Carts.user_id == user.id).scalar()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item_query = db.query(table.CartItems).filter(table.CartItems.id == id and table.CartItems.cart_id == cart.id)
    out_cart_item = cart_item_query.scalar()
    if out_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    cart_item_query.delete()
    db.commit()
    # db.refresh(out_cart_item)
    return out_cart_item


@router.get("/items", response_model=List[cart.OutCartItem])
async def get_all_items(user: Annotated[table.Users, Depends(auth.get_current_user)], db: Session = Depends(get_db)):
    '''
    Get All Items in Cart API

        並取得user購物車中所有商品資訊
    '''
    cart_items = db.query(table.CartItems).join(table.Carts, table.CartItems.cart_id == table.Carts.id)
    cart_items = cart_items.filter(table.Carts.user_id == user.id).all()
    return cart_items


@router.get("/all", response_model=List[cart.OutCart])
async def get_all_carts(db: Session = Depends(get_db)):
    '''
    Get All Carts API

        取得所有購物車資訊
    '''
    carts = db.query(table.Carts).all()
    return carts

@router.get("", response_model=cart.OutCart)
async def get_cart(user: Annotated[table.Users, Depends(auth.get_current_user)], db: Session = Depends(get_db)):
    '''
    Get Cart API

        取得user購物車資訊
        如果購物車不存在，則回傳 404, Cart not found
    '''
    cart = db.query(table.Carts).filter(table.Carts.user_id == user.id).scalar()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get("/orders", response_model=List[cart.OutCartItem])
async def order_by_cart(user: Annotated[table.Users, Depends(auth.get_current_user)], db: Session = Depends(get_db)):
    '''
    Get order by cart API

        送出購物車裡 is_checkout=true商品的訂單
        如果購物車是空的，則回傳 404, Cart items is empty

    '''
    user = is_user_exist(user_id=user.id, db=db)
    cart_cartitem_query  = db.query(table.CartItems).join(table.Carts, table.CartItems.cart_id == table.Carts.id).filter(table.Carts.user_id == user.id)
    cartitems = cart_cartitem_query.all()
    if cartitems == [] :
        raise HTTPException(status_code=404, detail="Cart items is empty")
    order_item = cart_cartitem_query.filter(table.CartItems.is_checked_out == True).all()
    
    for item in order_item:
        product_query = db.query(table.Products).filter(table.Products.id == item.product_id)
        product = product_query.scalar()
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.investory < item.quantity:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} investory not enough")
        
        product_query.update({"investory": product.investory - item.quantity})
        db.add(table.Orders(user_id=user.id, product_id=item.product_id, quantity=item.quantity))
    db.commit()
    
    return order_item


