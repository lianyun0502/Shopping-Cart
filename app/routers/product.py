from fastapi import APIRouter, Body, Depends, HTTPException
from schema import product
from typing import List, Optional, Annotated
from DataBase import table
from DataBase.base import get_db, Session
from routers import auth

router = APIRouter(prefix="/products", tags=["Product"])

def is_user_exist(user_id:str, db:Session)->Optional[table.Users]:
    user = db.query(table.Users).filter(table.Users.id == user_id).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=product.OutProduct)
async def add_product(
    user: Annotated[table.Users, Depends(auth.get_current_user)],
    product: product.CreateProduct=Body(...),
    db:Session=Depends(get_db)
    ):
    '''
    Create Product API

        根據 Path 選擇使用者，並透過 body 傳入商品資訊, 並在資料庫中新增商品
    '''
    
    product = table.Products(user_id=user.id, **product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("", response_model=product.OutProduct)
async def update_product(
    user: Annotated[table.Users, Depends(auth.get_current_user)],
    product_id: int, 
    product: product.UpdateProduct=Body(...), 
    db:Session=Depends(get_db)
    ):
    '''
    Update Product API

        透過Path以及Query選擇使用者的商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
        會檢查使用者商品是否存在，若不存在則回傳 404, Product not found
        
    '''
    
    query = db.query(table.Products).filter(table.Products.id == product_id and table.Products.user_id == user.id)
    query_product = query.scalar()    
    if query_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    query.update(product.model_dump())
    db.commit()
    db.refresh(query_product)
    # out_product = db.query(table.Products).filter(table.Products.id == product_id).scalar()
    return query_product

@router.delete("", response_model=product.OutProduct)
async def delete_product(
    user: Annotated[table.Users, Depends(auth.get_current_user)],   
    product_id: int,  
    db:Session=Depends(get_db)):
    '''
    Delete Product API
        透過 Path 選擇使用者商品，並在資料庫中刪除商品
    '''
    query = db.query(table.Products)
    product = query.filter(table.Products.id == product_id and table.Users.id == user.id).scalar()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found") 
    db.delete(product)
    db.commit()
    return product

@router.get("/all", response_model=List[product.OutProduct])
async def get_all_products(
    skip: int = 0, 
    limit: int = 100, 
    db:Session=Depends(get_db)):
    '''
    Get All Products API

        取得所有商品資訊
        user_id: 選擇使用者，如果參數存在則取得該使用者的商品
    '''
    products = db.query(table.Products).offset(skip).limit(limit).all()
    return products

@router.get("", response_model=List[product.OutProduct])
async def get_product(
    user: Annotated[table.Users, Depends(auth.get_current_user)],
    skip: int = 0, 
    limit: int = 100, 
    db:Session=Depends(get_db)):
    '''
    Get Product API
    透過 Path 選擇商品，並取得商品資訊
    '''
    query = db.query(table.Products).join(table.Users, table.Products.user_id == table.Users.id).filter(table.Users.id == user.id)
    products = query.offset(skip).limit(limit).all()
    return products
